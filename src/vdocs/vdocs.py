import os
import json
import requests
import aiohttp
import asyncio
import aiofiles
import rich_click as click
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

class vDocs():
    def __init__(self,
                url,
                username,
                password):
        self.vManage = url
        self.username = username
        self.password = password

    def vDocs(self):
        self.make_directories()
        self.cookie = self.get_token()
        asyncio.run(self.main())

    def make_directories(self):
        api_list = ['Fabric Devices',
                    'Device Status',
                    'Device Counters',
                    'Template Features',
                    'Template Feature Types',
                    'Template Policy List',
                    'vEdge Devices'
                    ]
        current_directory = os.getcwd()
        for api in api_list:
            final_directory = os.path.join(current_directory, rf'{ api }/JSON')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/YAML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/CSV')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/HTML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Markdown')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Mindmap')
            os.makedirs(final_directory, exist_ok=True)

    def get_token(self):
        url = f"{ self.vManage }/j_security_check"
        payload=f'j_username={ self.username }&j_password={ self.password }'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(f"<Authentication Status code {response.status_code} for { url }>")
        return response.cookies

    api_list = ["/dataservice/device",
                "/dataservice/device/monitor",
                "/dataservice/device/counters",
                "/dataservice/template/feature",
                "/dataservice/template/feature/types",
                "/dataservice/template/policy/vedge/devices",
                "/dataservice/template/policy/list"
                ]

    async def get_api(self, api_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.vManage}{api_url}",cookies = self.cookie, verify_ssl=False) as resp:
                response_dict = await resp.json()
                print(f"{api_url} Status Code {resp.status}")
                return (api_url,response_dict)

    async def main(self):
        results = await asyncio.gather(*(self.get_api(api_url) for api_url in self.api_list))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))

    async def json_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            if api == "/dataservice/device":
                async with aiofiles.open('Fabric Devices/JSON/Fabric Devices.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/device/monitor":
                async with aiofiles.open('Device Status/JSON/Device Status.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/device/counters":
                async with aiofiles.open('Device Counters/JSON/Device Counters.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/template/feature":
                async with aiofiles.open('Template Features/JSON/Template Features.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/template/feature/types":
                async with aiofiles.open('Template Feature Types/JSON/Template Feature Types.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/template/policy/vedge/devices":
                async with aiofiles.open('vEdge Devices/JSON/vEdge Devices.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/template/policy/list":
                async with aiofiles.open('Template Policy List/JSON/Template Policy List.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

    async def yaml_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            clean_yaml = yaml.dump(payload, default_flow_style=False)
            if api == "/dataservice/device":
                async with aiofiles.open('Fabric Devices/YAML/Fabric Devices.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/device/monitor":
                async with aiofiles.open('Device Status/YAML/Device Status.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/device/counters":
                async with aiofiles.open('Device Counters/YAML/Device Counters.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/template/feature":
                async with aiofiles.open('Template Features/YAML/Template Features.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/template/feature/types":
                async with aiofiles.open('Template Feature Types/YAML/Template Feature Types.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/template/policy/vedge/devices":
                async with aiofiles.open('vEdge Devices/YAML/vEdge Devices.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/template/policy/list":
                async with aiofiles.open('Template Policy List/YAML/Template Policy List.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

    async def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vdocs_csv.j2')
        for api, payload in json.loads(parsed_json):        
            csv_output = await csv_template.render_async(api = api,
                                         data_to_template = payload)
            if api == "/dataservice/device":
                async with aiofiles.open('Fabric Devices/CSV/Fabric Devices.csv', mode='w' ) as f:
                    await f.write(csv_output)
                    
            if api == "/dataservice/device/monitor":
                async with aiofiles.open('Device Status/CSV/Device Status.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/device/counters":
                async with aiofiles.open('Device Counters/CSV/Device Counters.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/template/feature":
                async with aiofiles.open('Template Features/CSV/Template Features.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/template/feature/types":
                async with aiofiles.open('Template Feature Types/CSV/Template Feature Types.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/template/policy/vedge/devices":
                async with aiofiles.open('vEdge Devices/CSV/vEdge Devices.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/template/policy/list":
                async with aiofiles.open('Template Policy List/CSV/Template Policy List.csv', mode='w' ) as f:
                    await f.write(csv_output)

    async def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vdocs_markdown.j2')
        for api, payload in json.loads(parsed_json):        
            markdown_output = await markdown_template.render_async(api = api,
                                         data_to_template = payload)
            if api == "/dataservice/device":
                async with aiofiles.open('Fabric Devices/Markdown/Fabric Devices.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/device/monitor":
                async with aiofiles.open('Device Status/Markdown/Device Status.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/device/counters":
                async with aiofiles.open('Device Counters/Markdown/Device Counters.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/template/feature":
                async with aiofiles.open('Template Features/Markdown/Template Features.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/template/feature/types":
                async with aiofiles.open('Template Feature Types/Markdown/Template Feature Types.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/template/policy/vedge/devices":
                async with aiofiles.open('vEdge Devices/Markdown/vEdge Devices.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/template/policy/list":
                async with aiofiles.open('Template Policy List/Markdown/Template Policy List.md', mode='w' ) as f:
                    await f.write(markdown_output)

    async def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vdocs_html.j2')
        for api, payload in json.loads(parsed_json):
            html_output = await html_template.render_async(api = api,
                                             data_to_template = payload)
            if api == "/dataservice/device":
                async with aiofiles.open('Fabric Devices/HTML/Fabric Devices.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/device/monitor":
                async with aiofiles.open('Device Status/HTML/Device Status.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/device/counters":
                async with aiofiles.open('Device Counters/HTML/Device Counters.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/template/feature":
                async with aiofiles.open('Template Features/HTML/Template Features.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/template/feature/types":
                async with aiofiles.open('Template Feature Types/HTML/Template Feature Types.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/template/policy/vedge/devices":
                async with aiofiles.open('vEdge Devices/HTML/vEdge Devices.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/template/policy/list":
                async with aiofiles.open('Template Policy List/HTML/Template Policy List.html', mode='w' ) as f:
                    await f.write(html_output)

    async def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vdocs_mindmap.j2')
        for api, payload in json.loads(parsed_json):
            mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = payload)
            if api == "/dataservice/device":
                async with aiofiles.open('Fabric Devices/Mindmap/Fabric Devices.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/device/monitor":
                async with aiofiles.open('Device Status/Mindmap/Device Status.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/device/counters":
                async with aiofiles.open('Device Counters/Mindmap/Device Counters.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/template/feature":
                async with aiofiles.open('Template Features/Mindmap/Template Features.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/template/feature/types":
                async with aiofiles.open('Template Feature Types/Mindmap/Template Feature Types.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/template/policy/vedge/devices":
                async with aiofiles.open('vEdge Devices/Mindmap/vEdge Devices.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/template/policy/list":
                async with aiofiles.open('Template Policy List/Mindmap/Template Policy List.md', mode='w' ) as f:
                    await f.write(mindmap_output)

    async def all_files(self, parsed_json):
        await asyncio.gather(self.json_file(parsed_json), self.yaml_file(parsed_json), self.csv_file(parsed_json), self.markdown_file(parsed_json), self.html_file(parsed_json), self.mindmap_file(parsed_json))

@click.command()
@click.option('--url',
    prompt="vManage URL",
    help="vManage URL",
    required=True,envvar="URL")
@click.option('--username',
    prompt="vManage Username",
    help="vManage Username",
    required=True,envvar="USERNAME")
@click.option('--password',
    prompt="vManage Password",
    help="vManage Password",
    required=True, hide_input=True,envvar="PASSWORD")
def cli(url,username,password):
    invoke_class = vDocs(url,username,password)
    invoke_class.vDocs()

if __name__ == "__main__":
    cli()
