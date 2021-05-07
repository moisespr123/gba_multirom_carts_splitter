# GBA MultiROM Carts Splitter

This is a Python script written to split GBA ROMS inside those bootleg carts.

Requires Python 3

Usage:  
```
python splitGBARom.py -i "input GBA file.gba" -o "Output directory" [-s] [-d]
```

Because some legit ROMS may contain additional ROMs, the script will not, by default, split bad GBA header ROMS. 

To split bad headers, pass the `-s` flag. This will split emulator ROMs inside the multicart, but will not split the ROMS inside it.

To split duplicate ROM names, pass the `-d` flag. In some cases, you may need to merge the resulting consecutive ROMs to make it work, as this may produce < 1kb files.

Also, please note that the first ROM will contain the Multicart menu. It is not splitted.

Pull Requests that may fix or improve the above issues are appreciated.

## Full command line documentation
```
usage: splitGBARom.py [-h] -i INPUT -o OUTPUT [-s] [-d]

GBA Multirom cart splitter

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input GBA file
  -o OUTPUT, --output OUTPUT
                        Output directory
  -s, --split_bad_headers
                        Splits bad headers, but may also corrupt legit roms
  -d, --do_not_remove_duplicates
                        Does not remove duplicate ROM names, but may also
                        corrupt legit roms
 ```