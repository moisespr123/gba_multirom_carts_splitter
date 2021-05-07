import struct
from pathlib import Path
from functools import partial
from io import DEFAULT_BUFFER_SIZE
import os
import argparse

# This is incomplete but it works
GBA_HEADER = b'\x24\xff\xae\x51\x69\x9a\xa2\x21\x3d\x84\x82\x0a\x84\xe4\x09\xad' \
             b'\x11\x24\x8b\x98\xc0\x81\x7f\x21\xa3\x52\xbe\x19\x93\x09\xce\x20' \
             b'\x10\x46\x4a\x4a\xf8\x27\x31\xec\x58\xc7\xe8\x33'

rom_positions = []


def file_byte_iterator(path):
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read1, DEFAULT_BUFFER_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            yield from chunk


def split_rom(file):
    print("Splitting ROM")
    file_bytearray = bytearray(file_byte_iterator(file))
    offset = 4
    p_offset = 0
    while True:
        p = file_bytearray.find(GBA_HEADER, p_offset)
        if p > -1:
            if p - offset not in rom_positions:
                rom_position = p - offset
                print("ROM found at {0}".format(rom_position))
                rom_positions.append(rom_position)
        else:
            break
        p_offset = p + 4


def remove_dups(rom, args):
    last_rom = ""
    rom_positions_copy = rom_positions.copy()
    with open(rom, 'rb') as file:
        for p in rom_positions_copy:
            file.seek(p + 160)
            rom_name = file.read(12).decode("latin1").rstrip('\x00')
            print("Verifying rom {0}".format(rom_name))
            file.seek(p)
            if file.read(3) == b'\x2e\x00\x00' and not args.split_bad_headers:
                rom_positions.remove(p)
                print("ROM at {0} is part of the before ROM. Removing".format(p))
            elif last_rom == rom_name and not args.do_not_remove_duplicates:
                rom_positions.remove(p)
                print("Duplicate ROM name. Removing")
            elif rom_name == "":
                rom_positions.remove(p)
                print("Bad ROM name. Removing")
            else:
                print("ROM OK")
            last_rom = rom_name
    print(rom_positions)


def write_rom(rom, output_folder):
    counter = 1
    with open(rom, 'rb') as file:
        for p in rom_positions:
            file.seek(p + 160)
            rom_name = file.read(12).decode("latin1").rstrip('\x00')
            print(file.seek(p))
            filename = os.path.join(output_folder, str(counter) + "- " + rom_name + ".gba")
            print("Writing {0}".format(filename))
            end = False
            with open(filename, "wb") as output_rom:
                if counter == len(rom_positions):
                    end = True
                if not end:
                    output_rom.write(file.read(rom_positions[counter] - rom_positions[counter - 1]))
                else:
                    output_rom.write(file.read(os.stat(rom).st_size - rom_positions[counter - 1]))
            print(end)
            counter += 1


def main():
    parser = argparse.ArgumentParser(description='GBA Multirom cart splitter')
    parser.add_argument('-i', "--input", help='Input GBA file', required=True)
    parser.add_argument('-o', "--output", help='Output directory', required=True)
    parser.add_argument('-s', "--split_bad_headers", help='Splits bad headers, but may also corrupt legit roms',
                        action='store_true')
    parser.add_argument('-d', "--do_not_remove_duplicates",
                        help='Does not remove duplicate ROM names, but may also corrupt legit roms',
                        action='store_true')
    args = parser.parse_args()
    split_rom(args.input)
    remove_dups(args.input, args)
    write_rom(args.input, args.output)


if __name__ == "__main__":
    main()
