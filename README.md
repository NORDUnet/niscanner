# NI Scanner

NI Scaner is a tool for processing scan requests from NORDUnets Network Inventory (NI).

Currently it supports nmap scans of hosts. When run it will process all currently queued host scan requrests from NI.

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

