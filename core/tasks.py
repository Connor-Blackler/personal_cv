import json
import base64
import asyncio
import aiohttp
import os
from .models import GitRepo, Language


import os
import subprocess
import requests

github_username = 'Connor-Blackler'
github_url = f'https://api.github.com/users/{github_username}/repos'
file_path_in_repo = 'thumbnail.json'


def _fetch_with_docker() -> list[dict]:
    """
    Testing power of docker on simple tasks like this
    """
    docker_username = os.environ.get('DOCKER_USERNAME')
    docker_password = os.environ.get('DOCKER_PASSWORD')

    # Log into Docker
    subprocess.call(
        ['docker', 'login', '-u', docker_username, '-p', docker_password])

    # Get a list of all repositories for the given user
    response = requests.get(github_url)
    data = response.json()
    repos = [repo['name'] for repo in data]

    # Build Docker image, ensure no-cache in case of docker build caching
    dockerfile_path = os.path.abspath(os.path.dirname(__file__))
    subprocess.call(['docker', 'build', '-t',
                    'my_docker_image', dockerfile_path])

    ret = []
    for repo in repos:
        # Clone the repository
        clone_command = ['docker', 'run', "--net=host", '-dit',
                         '--name', f'docker_container_{repo}', 'my_docker_image', "/bin/sh"]

        subprocess.check_output(
            clone_command, stderr=subprocess.STDOUT, universal_newlines=True)

        git_clone_command = [
            'docker', 'exec', "-it", f'docker_container_{repo}', 'git', 'clone', f'https://github.com/{github_username}/{repo}.git']
        git_clone_command_result = subprocess.run(
            git_clone_command, capture_output=True)
        print("Git clone:")
        print(git_clone_command_result.stdout.decode('utf-8'))

        check_file_command = [
            'docker', 'exec', "-it", f'docker_container_{repo}', 'test', '-f', f"{repo}/{file_path_in_repo}"]
        file_exists = subprocess.call(check_file_command) == 0

        if file_exists:
            cat_command = [
                'docker', 'exec', "-it", f'docker_container_{repo}', 'cat', f"{repo}/{file_path_in_repo}"]
            file_content = subprocess.check_output(cat_command).decode('utf-8')

            print(f'Content of {file_path_in_repo} in {repo}:')
            print(file_content)
            ret.append({
                'repo': repo,
                'file_content': file_content,
                'url': f"https://github.com/{github_username}/{repo}"
            })
        else:
            print(f'The file {file_path_in_repo} does not exist in {repo}.')
        subprocess.call(['docker', 'rm', '-f', f'docker_container_{repo}'])

    return ret


def scrape_and_save():
    print("lets scrape")
    scraped_data = _fetch_with_docker()

    for item in scraped_data:
        print(item)
        file_content = json.loads(item["file_content"])

        this_repo, created = GitRepo.objects.get_or_create(
            url=item["url"]
        )

        for index, this_lang in enumerate(file_content["language"]):
            lang, created = Language.objects.get_or_create(
                title=this_lang
            )
            lang.color = file_content["language_bg"][index]
            lang.save()

            this_repo.languages.add(lang)

        this_repo.title = file_content["title"]
        this_repo.image = file_content["image"]
        this_repo.description = file_content["description"]
        this_repo.save()
