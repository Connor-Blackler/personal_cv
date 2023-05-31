import os
import aiohttp
import asyncio
import subprocess
import base64
import json

github_username = 'Connor-Blackler'
github_url = f'https://api.github.com/users/{github_username}/repos'
file_path_in_repo = 'thumbnail.json'


def _fetch_with_docker() -> dict:
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

    # Build Docker image, ensure no-cache incase of docker build caching
    dockerfile_path = os.path.abspath(os.path.dirname(__file__))
    subprocess.call(['docker', 'build', '--no-cache', '-t',
                    'my_docker_image', dockerfile_path])

    for repo in repos:
        subprocess.call(['docker', 'run', '-d', '--name', f'docker_container_{repo}', 'my_docker_image',
                         '/bin/sh', '-c', f'git clone https://github.com/{github_username}/{repo}.git'])

        check_file_command = [
            'docker', 'exec', f'docker_container_{repo}', 'test', '-f', f'{repo}/{file_path_in_repo}']
        file_exists = subprocess.call(check_file_command) == 0

        if file_exists:
            cat_command = [
                'docker', 'exec', f'docker_container_{repo}', 'cat', f'{repo}/{file_path_in_repo}']
            file_content = subprocess.check_output(cat_command).decode('utf-8')

            print(f'Content of {file_path_in_repo} in {repo}:')
            print(file_content)
        else:
            print(f'The file {file_path_in_repo} does not exist in {repo}.')
        subprocess.call(['docker', 'rm', '-f', f'docker_container_{repo}'])


async def fetch_repo_detail(session, repo, headers):
    file_url = f'https://api.github.com/repos/{github_username}/{repo}/contents/{file_path_in_repo}'
    async with session.get(file_url, headers=headers) as file_response:
        if file_response.status == 200:
            file_data = await file_response.json()
            file_content = base64.b64decode(
                file_data['content']).decode('utf-8')
            file_content = json.loads(file_content)
            return {
                'repo': repo,
                'file_content': file_content,
                'url': f"https://api.github.com/repos/{github_username}/{repo}"
            }


async def get_repo_details():
    headers = {
        'Authorization': os.environ.get('GITHUB_ACCESS_TOKEN'),
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(github_url, headers=headers)
        data = await response.json()
        repos = [repo['name'] for repo in data]

        tasks = [fetch_repo_detail(session, repo, headers) for repo in repos]
        repo_data = await asyncio.gather(*tasks)

        # Remove None values in case of failed requests
        repo_data = [data for data in repo_data if data is not None]

        return repo_data


def get_repo_thumnails() -> dict:
    loop = asyncio.get_event_loop()
    repo_data = loop.run_until_complete(get_repo_details())

    return repo_data


if __name__ == "__main__":
    print(get_repo_thumnails())
