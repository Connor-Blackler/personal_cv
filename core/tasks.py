import json
import base64
import asyncio
import aiohttp
import os
from .models import GitRepo, Language


github_username = 'Connor-Blackler'
github_url = f'https://api.github.com/users/{github_username}/repos'
file_path_in_repo = 'thumbnail.json'


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

    print("about to start")
    print(headers)
    async with aiohttp.ClientSession() as session:
        response = await session.get(github_url, headers=headers)
        data = await response.json()
        repos = [repo['name'] for repo in data]

        tasks = [fetch_repo_detail(session, repo, headers) for repo in repos]
        repo_data = await asyncio.gather(*tasks)

        # Remove None values in case of failed requests
        repo_data = [data for data in repo_data if data is not None]
        print(repo_data)
        return repo_data


def get_repo_thumnails() -> dict:
    loop = asyncio.get_event_loop()
    repo_data = loop.run_until_complete(get_repo_details())

    return repo_data


def scrape_and_save():
    print("lets scrape")
    scraped_data = get_repo_thumnails()

    for item in scraped_data:
        print(item)
        this_repo, created = GitRepo.objects.get_or_create(
            url=item["url"]
        )

        for this_lang in item["file_content"]["language"]:
            lang, created = Language.objects.get_or_create(
                title=this_lang["title"]
            )
            lang.color = this_lang["language_bg"]
            this_repo.languages.add(lang)

        this_repo.image = item["file_content"]["image"]
        this_repo.description = item["file_content"]["description"]
        this_repo.save()
