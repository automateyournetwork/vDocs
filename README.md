# vDocs

Business Ready Documents for Cisco SD-WAN vManage

## Current API Coverage

BFD Sessions

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
(sdwan) $ aceye
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

## Contact

Please contact John Capobianco if you need any assistance
