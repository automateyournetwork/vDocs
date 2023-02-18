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
        self.device_list = asyncio.run(self.build_device_list())
        asyncio.run(self.add_device_apis())
        asyncio.run(self.main())

    def make_directories(self):
        api_list = ['ARP Interfaces',
                    'BFD Sessions',
                    'BFD Sessions From Device',
                    'BFD Summary',
                    'CEdge Interfaces',
                    'Control Connection',
                    'Control Local Property',
                    'Control WAN Interfaces',
                    'Device Status',
                    'Device Counters',
                    'Fabric Devices',
                    'Hardware Environment',
                    'Hardware Inventory',
                    'Interfaces',
                    'OMP Peers',
                    'System',
                    'System Status',
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

    async def build_device_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.vManage}/dataservice/device",cookies = self.cookie, verify_ssl=False) as resp:
                response_dict = await resp.json()
                print(f"Status Code {resp.status}")
                return (response_dict)    

    async def add_device_apis(self):
        #ARP
        for device in self.device_list['data']:
            arp_api = f"/dataservice/device/arp?deviceId={ device['deviceId'] }"
            self.api_list.append(arp_api)
        #BFD Summary
            bfd_summary_api = f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }"
            self.api_list.append(bfd_summary_api)
        #BFD Sessions from Device
            bfd_session_from_device_api = f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }"
            self.api_list.append(bfd_session_from_device_api)
            
    api_list = ["/dataservice/data/device/state/BFDSessions",
                '/dataservice/data/device/state/CEdgeInterface',
                "/dataservice/data/device/state/ControlConnection",
                "/dataservice/data/device/state/ControlLocalProperty",
                "/dataservice/data/device/state/ControlWanInterface",
                "/dataservice/data/device/state/HardwareEnvironment",
                "/dataservice/data/device/state/HardwareInventory",
                "/dataservice/data/device/state/Interface",
                "/dataservice/data/device/state/OMPPeer",
                '/dataservice/data/device/state/System',
                '/dataservice/data/device/state/SystemStatus',
                "/dataservice/device",
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

            if api == "/dataservice/data/device/state/BFDSessions":
                async with aiofiles.open('BFD Sessions/JSON/BFD Sessions.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/ControlConnection":
                async with aiofiles.open('Control Connection/JSON/Control Connection.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/ControlLocalProperty":
                async with aiofiles.open('Control Local Property/JSON/Control Local Property.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/ControlWanInterface":
                async with aiofiles.open('Control WAN Interfaces/JSON/Control WAN Interfaces.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/HardwareEnvironment":
                async with aiofiles.open('Hardware Environment/JSON/Hardware Environment.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/HardwareInventory":
                async with aiofiles.open('Hardware Inventory/JSON/Hardware Inventory.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/Interface":
                async with aiofiles.open('Interfaces/JSON/Interfaces.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('CEdge Interfaces/JSON/CEdge Interfaces.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/OMPPeer":
                async with aiofiles.open('OMP Peers/JSON/OMP Peer.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/SystemStatus":
                async with aiofiles.open('System Status/JSON/System Status.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if api == "/dataservice/data/device/state/System":
                async with aiofiles.open('System/JSON/System.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            for device in self.device_list['data']:
                if f"/dataservice/device/arp?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"ARP Interfaces/JSON/ARP Interfaces { device['deviceId'] }.json", mode='w') as f:
                        await f.write(json.dumps(payload, indent=4, sort_keys=True))

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Summary/JSON/BFD Summary { device['deviceId'] }.json", mode='w') as f:
                        await f.write(json.dumps(payload, indent=4, sort_keys=True))

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Sessions From Device/JSON/BFD Sessions From { device['deviceId'] }.json", mode='w') as f:
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

            if api == "/dataservice/data/device/state/BFDSessions":
                async with aiofiles.open('BFD Sessions/YAML/BFD Sessions.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/ControlConnection":
                async with aiofiles.open('Control Connection/YAML/Control Connection.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/ControlLocalProperty":
                async with aiofiles.open('Control Local Property/YAML/Control Local Property.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/ControlWanInterface":
                async with aiofiles.open('Control WAN Interfaces/YAML/Control WAN Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/HardwareEnvironment":
                async with aiofiles.open('Hardware Environment/YAML/Hardware Environment.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/HardwareInventory":
                async with aiofiles.open('Hardware Inventory/YAML/Hardware Inventory.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/Interface":
                async with aiofiles.open('Interfaces/YAML/Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('CEdge Interfaces/YAML/CEdge Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/OMPPeer":
                async with aiofiles.open('OMP Peers/YAML/OMP Peers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/SystemStatus":
                async with aiofiles.open('System Status/YAML/System Status.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if api == "/dataservice/data/device/state/System":
                async with aiofiles.open('System/YAML/System.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            for device in self.device_list['data']:
                if f"/dataservice/device/arp?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"ARP Interfaces/YAML/ARP Interfaces { device['deviceId'] }.yaml", mode='w') as f:
                        await f.write(clean_yaml)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Summary/YAML/BFD Summary { device['deviceId'] }.yaml", mode='w') as f:
                        await f.write(clean_yaml)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Sessions From Device/YAML/BFD Sessions From { device['deviceId'] }.yaml", mode='w') as f:
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

            if api == "/dataservice/data/device/state/BFDSessions":
                async with aiofiles.open('BFD Sessions/CSV/BFD Sessions.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/ControlConnection":
                async with aiofiles.open('Control Connection/CSV/Control Connection.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/ControlLocalProperty":
                async with aiofiles.open('Control Local Property/CSV/Control Local Property.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/ControlWanInterface":
                async with aiofiles.open('Control WAN Interfaces/CSV/Control WAN Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/HardwareEnvironment":
                async with aiofiles.open('Hardware Environment/CSV/Hardware Environment.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/HardwareInventory":
                async with aiofiles.open('Hardware Inventory/CSV/Hardware Inventory.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/Interface":
                async with aiofiles.open('Interfaces/CSV/Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('CEdge Interfaces/CSV/CEdge Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/OMPPeer":
                async with aiofiles.open('OMP Peers/CSV/OMP Peers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/SystemStatus":
                async with aiofiles.open('System Status/CSV/System Status.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if api == "/dataservice/data/device/state/System":
                async with aiofiles.open('System/CSV/System.csv', mode='w' ) as f:
                    await f.write(csv_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/arp?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"ARP Interfaces/CSV/ARP Interfaces { device['deviceId'] }.csv", mode='w') as f:
                        await f.write(csv_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Summary/CSV/BFD Summary { device['deviceId'] }.csv", mode='w') as f:
                        await f.write(csv_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Sessions From Device/CSV/BFD Sessions From { device['deviceId'] }.csv", mode='w') as f:
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

            if api == "/dataservice/data/device/state/BFDSessions":
                async with aiofiles.open('BFD Sessions/Markdown/BFD Sessions.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/ControlConnection":
                async with aiofiles.open('Control Connection/Markdown/Control Connection.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/ControlLocalProperty":
                async with aiofiles.open('Control Local Property/Markdown/Control Local Property.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/ControlWanInterface":
                async with aiofiles.open('Control WAN Interfaces/Markdown/Control WAN Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/HardwareEnvironment":
                async with aiofiles.open('Hardware Environment/Markdown/Hardware Environment.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/HardwareInventory":
                async with aiofiles.open('Hardware Inventory/Markdown/Hardware Inventory.md', mode='w' ) as f:
                    await f.write(markdown_output)                    

            if api == "/dataservice/data/device/state/Interface":
                async with aiofiles.open('Interfaces/Markdown/Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output) 

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('CEdge Interfaces/Markdown/CEdge Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/OMPPeer":
                async with aiofiles.open('OMP Peers/Markdown/OMP Peers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/SystemStatus":
                async with aiofiles.open('System Status/Markdown/System Status.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if api == "/dataservice/data/device/state/System":
                async with aiofiles.open('System/Markdown/System.md', mode='w' ) as f:
                    await f.write(markdown_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/arp?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"ARP Interfaces/Markdown/ARP Interfaces { device['deviceId'] }.md", mode='w') as f:
                        await f.write(markdown_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Summary/Markdown/BFD Summary { device['deviceId'] }.md", mode='w') as f:
                        await f.write(markdown_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Sessions From Device/Markdown/BFD Sessions From { device['deviceId'] }.md", mode='w') as f:
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

            if api == "/dataservice/data/device/state/BFDSessions":
                async with aiofiles.open('BFD Sessions/HTML/BFD Sessions.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/ControlConnection":
                async with aiofiles.open('Control Connection/HTML/Control Connection.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/ControlLocalProperty":
                async with aiofiles.open('Control Local Property/HTML/Control Local Property.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/ControlWanInterface":
                async with aiofiles.open('Control WAN Interfaces/HTML/Control WAN Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/HardwareEnvironment":
                async with aiofiles.open('Hardware Environment/HTML/Hardware Environment.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/HardwareInventory":
                async with aiofiles.open('Hardware Inventory/HTML/Hardware Inventory.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/Interface":
                async with aiofiles.open('Interfaces/HTML/Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('CEdge Interfaces/HTML/CEdge Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('OMP Peers/HTML/OMP Peers.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/SystemStatus":
                async with aiofiles.open('System Status/HTML/System Status.html', mode='w' ) as f:
                    await f.write(html_output)

            if api == "/dataservice/data/device/state/System":
                async with aiofiles.open('System/HTML/System.html', mode='w' ) as f:
                    await f.write(html_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/arp?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"ARP Interfaces/HTML/ARP Interfaces { device['deviceId'] }.html", mode='w') as f:
                        await f.write(html_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Summary/HTML/BFD Summary { device['deviceId'] }.html", mode='w') as f:
                        await f.write(html_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Sessions From Device/HTML/BFD Sessions From { device['deviceId'] }.html", mode='w') as f:
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

            if api == "/dataservice/data/device/state/BFDSessions":
                async with aiofiles.open('BFD Sessions/Mindmap/BFD Sessions.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/ControlConnection":
                async with aiofiles.open('Control Connection/Mindmap/Control Connection.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/ControlLocalProperty":
                async with aiofiles.open('Control Local Property/Mindmap/Control Local Property.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/ControlWanInterface":
                async with aiofiles.open('Control WAN Interfaces/Mindmap/Control WAN Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/HardwareEnvironment":
                async with aiofiles.open('Hardware Environment/Mindmap/Hardware Environment.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/HardwareInventory":
                async with aiofiles.open('Hardware Inventory/Mindmap/Hardware Inventory.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/Interface":
                async with aiofiles.open('Interfaces/Mindmap/Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/CEdgeInterface":
                async with aiofiles.open('CEdge Interfaces/Mindmap/CEdge Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/OMPPeer":
                async with aiofiles.open('OMP Peers/Mindmap/OMP Peers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/SystemStatus":
                async with aiofiles.open('System Status/Mindmap/System Status.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if api == "/dataservice/data/device/state/System":
                async with aiofiles.open('System/Mindmap/System.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/arp?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"ARP Interfaces/Mindmap/ARP Interfaces { device['deviceId'] }.md", mode='w') as f:
                        await f.write(mindmap_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/summary?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Summary/Mindmap/BFD Summary { device['deviceId'] }.md", mode='w') as f:
                        await f.write(mindmap_output)

            for device in self.device_list['data']:
                if f"/dataservice/device/bfd/sessions?deviceId={ device['deviceId'] }" in api:
                    async with aiofiles.open(f"BFD Sessions From Device/Mindmap/BFD Sessions From { device['deviceId'] }.md", mode='w') as f:
                        await f.write(mindmap_output)

    async def all_files(self, parsed_json):
        await asyncio.gather(self.json_file(parsed_json),
                             self.yaml_file(parsed_json),
                             self.csv_file(parsed_json),
                             self.markdown_file(parsed_json),
                             self.html_file(parsed_json),
                             self.mindmap_file(parsed_json)
                             )

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
