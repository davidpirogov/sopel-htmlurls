# Sopel HtmlUrls

A module that generates a HTML page of the most recently posted urls in a channel

## Installation

Tested on Ubuntu 22.04 LTS. Requires python 3.7 and [Sopel 7.1](https://github.com/sopel-irc/sopel),
and [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)

Highly recommended to create a separate [pyenv environment](https://realpython.com/intro-to-pyenv/)
for the Sopel bot and use pip to install the repository. The plugin will be available to Sopel
as an [Entry point plugin](https://sopel.chat/docs/plugin.html#term-Entry-point-plugin)

```bash
pyenv virtualenv sopel_7_1
pip install sopel
cd .../sopel-htmlurls
pip install .
pip install -r requirements.txt
```

## Configuration

The plugin has several configuration options with sensible defaults where appropriate

### template_file

Type: `string`

This is the path to the template file that is included in this repository. This file is used by
Jinja2 to generate the output HTML files on a per-channel basis. It can be an absolute path or a
relative path to the python working directory, and is used by pathlib.Path.

### output_dir

Type: `string`

This is the path to the public, output directory that should be accessible by your webserver.
This directory will contain a set of HTML files, one for each channel configured further below.
Similar to ```template_file```, it can be an absolute or relative path.

### channels

Type: `list`

This is a list of channels that the plugin will create url history for and output each channel into
its own separate HTML file inside the ```output_dir```.

For example, if you configure:
```ini
channels =
    "#channelA"
    "##channelB"
```

There will be two files in the ```output_dir``` directory called ```#channelA.html``` and
```##channelB.html```. They will contain the formatted HTML based on the supplied template.


### allow_only_public_urls

Type: `bool`

Whether or not to allow urls that are publicly accessible. If **True**, then any url that cannot be
accessed publicly, such as ```http://localhost:8080/``` or ```file:///foo.log``` will be ignored.

### page_refresh_seconds

Type: `int`

The number of seconds between each refresh of the page. This will be used in the HTML page's
```http-equiv="refresh"``` parameter. Making this shorter will update the page quicker but will
increase load on the server.

### max_output_urls

Type: `int`

The maximum number of urls to render into each channel's HTML file. Older urls are dropped off and
newer urls take their place


### Alternative Configuration

For those who don't like running interactive `sopel -w` you need to add to the default.cfg file

```ini
[htmlurls]
template_file = ...path/to/your/sopel-htmlurls/sopel_htmlurls/template.html
output_dir = ...path/to/your/webserver/public/
allow_only_public_urls = True
page_refresh_seconds = 30
max_output_urls = 35
channels =
  "#channelA"
  "##channelB"
```

## Usage

For a directory-based approach, create a symlink to one of the channel files.

E.g. if you want ```https://channelA.com/urls``` to show the page, create a symlink:
```bash
ln -s path/to/webserver/public/#channelA.html path/to/webserver/public/index.html
```

### IRC commands

There are no user-triggered IRC commands.

## Testing

Tests are run via Python unittests and are stored in the `tests/` directory.

```bash
python -m unittest
```
