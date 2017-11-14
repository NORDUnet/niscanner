# NI Scanner

NI Scaner is a tool for processing scan requests from NORDUnets Network Inventory (NI).

Currently it supports nmap scans of hosts. When run it will process all currently queued host scan requrests from NI.

## Installation

1. Create a `lib` folder and add a `__init__.py` to the folder.
2. Symlinks for [nerds](https://github.com/fredrikt/nerds)
  - `producers/nmap_services_py/nmap_services_py.py` into `lib/nerds`
  - `producers/utils/file.py` and `producers/utils/nerds.py` into `lib/utils`
  - Create `__init__.py` file in both sub dirs
3. Copy `settings.conf.dist` to `settings.conf`
4. Fill in settings

## Usage

    python ni_scanner.py -C settings.conf

## Running tests

    python -m unittest discover

## License

NORDUnet License (3-clause BSD). See LICENSE.txt for more details.

## TODO

- Daemonize?
  - http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
  - https://pypi.python.org/pypi/python-daemon/

