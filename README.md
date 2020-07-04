# JSON to XML with Secure Transfer 

## Introduction
This project does the following:
- Creates two Docker containers
- Reads in JSON files
- Converts the JSON files to XML
- Encrypts the files
- Transfers the XML files between containers
- Writes the files to disk

## Requirements
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [OpenSSL](https://www.openssl.org/)


## Usage:

Invoke `transfer.sh` and pass the names of the files to be sent. Files must be in the same directory as `transfer.sh` and have the extension `.json`

```
transfer.sh [<filename>.json, ...]
```