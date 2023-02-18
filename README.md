[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/automateyournetwork/vDocs)

[![Run in Cisco Cloud IDE](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-runable-icon.svg)](https://developer.cisco.com/devenv/?id=devenv-vscode-base&GITHUB_SOURCE_REPO=https://github.com/automateyournetwork/vDocs)

# vDocs

Business Ready Documents for Cisco SD-WAN vManage

## Current API Coverage

ARP Interfaces

BFD Sessions

BFD Sessions from Device

BFD Summary

CEdge Interfaces

Control Connection

Control Local Property

Control WAN Interface

Device Counters

Device Status

Fabric Devices

Hardware Environment

Hardware Inventory

Interfaces

OMP Peers

System

System Status

Template Feature Types

Template Features

Template Policy List

vEdge Devices

## Installation

```console
$ python3 -m venv sdwan
$ source sdwan/bin/activate
(sdwan) $ pip install vdocs
```

## Usage - Help

```console
(sdwan) $ vdocs --help
```

![vDocs Help](/images/help.png)

## Usage - In-line

```console
(sdwan) $ vdocs --url <url to vManage> --username <vManage username> --password <vManage password>
```

## Usage - Interactive

```console
(sdwan) $ vdocs
vManage URL: <URL to vManage>
vManage Username: <vManage Username>
vManage Password: <vManage Password>
```

## Usage - Environment Variables

```console
(sdwan) $ export URL=<URL to vManage>
(sdwan) $ export USERNAME=<vManage Username>
(sdwan) $ export PASSWORD=<vManage Password>
```

## Recommended VS Code Extensions

Excel Viewer - CSV Files

Markdown Preview - Markdown Files

Markmap - Mindmap Files

Open in Default Browser - HTML Files

## Always On Sandbox

This code works with the always on sandbox! 

https://devnetsandbox.cisco.com/RM/Diagram/Index/a4ab71bc-f7a0-4d63-bedb-05a051818569?diagramType=Topology

```console
export URL=https://sandbox-sdwan-2.cisco.com
export USERNAME=devnetuser
export PASSWORD='RG!_Yw919_83'

(venv)$ pip install vdocs
(venv)$ mkdir vdocs_output
(venv)$ cd vdocs_output
(venv)/vdocs_output$ vdocs
(venv)/vdocs_output$ code . 
(Launches VS Code and you can view the output with the recommended VS Code extensions)
```
## Contact

Please contact John Capobianco if you need any assistance
