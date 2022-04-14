#!/usr/bin/env python3

import argparse
import json
from typing import Dict, List

import vlq


class Decoder:
    def __init__(self) -> None:
        self.line_delimiter = ";"
        # Can specify rules on how the raw string could be decoded
        # or inherit rules from this class.

    def decode_int_value(self, value: str) -> int:
        decoded_value = vlq.base64vlq_decode(value)
        return decoded_value[2] if decoded_value else None

    def decode_mapping(self, raw_map: str) -> List[int]:
        raw_mapping = raw_map.split(self.line_delimiter)
        converted_mapping = []

        for raw_val in raw_mapping:
            # TODO: delete the try catch here.
            try:
                converted_mapping.append(self.decode_int_value(raw_val))
            except ValueError:
                converted_mapping.append(None)

        return converted_mapping


def get_raw_source_map(source_map_path: str) -> str:
    with open(source_map_path) as json_file:
        data = json.load(json_file)

    return data["mapping"]


def line_to_pc_map(l: List[int]) -> Dict[int, List[int]]:
    line_map = {}
    for index, line_num in enumerate(l):
        if line_num is not None:  # be careful for '0' checks!
            if line_num not in line_map:
                line_map[line_num] = []
            line_map[line_num].append(index)
    return line_map


def annotate_map_to_source(source_map: Dict[int, List[int]], source_file_path: str):
    source_lines = []
    output_path = source_file_path.split(".")
    output_path[0] += "_annotated"
    output_path = ".".join(output_path)

    with open(source_file_path, "r") as f:
        source_lines = [line.strip() for line in f.readlines()]

    # Format the PC lines to a uniform length
    col_max = len(max(source_lines, key=len))

    with open(output_path, "w") as f:
        for line_index, line_literal in enumerate(source_lines):
            if line_index in source_map:
                whitespace = " " * (col_max - len(line_literal))
                line = f"{line_literal}{whitespace}// PC: {source_map[line_index]}\n"
            else:
                line = f"{line_literal}\n"
            f.write(line)

    print(f"Annotated output saved to {output_path}")
    return


def decode_source_map(
    source_map_path: str,
    source_file_path: str,
    tabulate: bool = False,
    verbose: bool = False,
):
    decoder = Decoder()
    raw_source_map = get_raw_source_map(source_map_path)
    pc_list = decoder.decode_mapping(raw_source_map)
    line_map = line_to_pc_map(pc_list)
    annotate_map_to_source(line_map, source_file_path)

    if verbose:
        print(f"Raw source map: {raw_source_map}")
        print(f"PC list: {pc_list}")
        print(f"Line map: {line_map}")

    if tabulate:
        print("Tabulating is not supported yet :(")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python script to parse and decode a source map in TEAL"
    )
    parser.add_argument("map", help="path to the source map from PC->TEAL")
    parser.add_argument("source", help="path to the source file in TEAL")
    parser.add_argument("-t", "--tabulate", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    # TODO: Offer support for different maps?
    args = parser.parse_args()

    decode_source_map(args.map, args.source, args.tabulate, args.verbose)
