# Teal Sourcemap Decoder

This is a short python script that decodes a given source map and annotates a TEAL program to its PC.

**NOTE**: The [Python SDK](https://github.com/algorand/py-algorand-sdk/blob/develop/algosdk/source_map.py) also supports source mapping and is the successor to this script. This script is only provided for reference and may not be actively maintained.

## Usage

Clone this repo, then run the `decode.py` script:

`python decode.py [path to source map] [path to source file] [--verbose] [--tabulate]`

e.g. `python decode.py examples/myprog.teal.tok.map examples/myprog.teal`

A source map can be created using the `-m` flag with `goal clerk compile`, e.g. `goal clerk compile <path-to-source-teal> -m`
