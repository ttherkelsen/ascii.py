#!/usr/bin/env python
#
# bdf2pickle.py -- convert BDF files into a dict and save it in a pickle
#     for later loading
#

import argparse, re, os.path, pickle, gzip

def run():
    cmdline = argparse.ArgumentParser(description="Convert a BDF file into a pickle in current directory.")
    cmdline.add_argument('bdffile', help='BDF file to convert, file can end in .gz and will be uncompressed in memory')
    cmdline.add_argument('fontname', help='Name of the font, <bdffile until first . in filename>.', default=None, nargs="?")
    args = cmdline.parse_args()

    convert(args.bdffile, args.fontname)

def convert(bdf, fontname):
    RE = r'STARTCHAR (\S+).+?ENCODING (\S+).+?BBX (\d+) (\d+).+?BITMAP\s+(.*?)\s+ENDCHAR'
    if fontname is None:
        fontname = os.path.basename(bdf).split(".")[0]
        
    glyphs = {}

    if bdf.endswith(".gz"):
        with gzip.open(bdf, 'rb') as FD:
            data = FD.read().decode()
    else:
        with open(bdf, 'r') as FD:
            data = FD.read()
        
    
    # FIXME: We assume that the BDF font format has the same size
    # bitmap for all font glyphs.  Is this a safe assumption?
    for match in re.finditer(RE, data, re.DOTALL):
        name, encoding, width, height, bitmap = match.groups()
        encoding = int(encoding)
        width = int(width)
        height = int(height)
        shift = 8 - (width % 8)
        bitmap = [ int(t, 16) >> shift for t in bitmap.split("\n") ]

        if len(bitmap) != height:
            raise ValueError(f"{name} bitmap has wrong size")
          
        glyphs[encoding] = bitmap
        print(f"{encoding:x}")

    data = (
        fontname,
        width,
        height,
        1,
        glyphs,
    )
    with open(f'{fontname}.pickle', 'wb') as fd:
        pickle.dump(data, fd)

if __name__ == '__main__':
    run()
