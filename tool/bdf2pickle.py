#!/usr/bin/env python
#
# bdf2pickle.py -- convert BDF files into a dict and save it in a pickle
#     for later loading
#

import argparse, re, os.path, pickle

def run():
    cmdline = argparse.ArgumentParser(description="Convert BDF files into pickles.")
    cmdline.add_argument('-d', '--destdir', help='Which directory to write the files to, defaults to current dir.', default=".")
    cmdline.add_argument('bdffile', help='BDF file to convert')
    args = cmdline.parse_args()

    convert(args.bdffile, args.destdir)

def convert(bdf, destdir):
    RE = r'STARTCHAR (\S+).+?ENCODING (\S+).+?BBX (\d+) (\d+).+?BITMAP\s+(.*?)\s+ENDCHAR'
    fontname = os.path.basename(bdf).split(".")[0]
    glyphs = {}

    # FIXME: We assume that the BDF font format has the same size
    # bitmap for all font glyphs.  Is this a safe assumption?
    with open(bdf, 'r') as fd:
        for match in re.finditer(RE, fd.read(), re.DOTALL):
            name, encoding, width, height, bitmap = match.groups()
            encoding = int(encoding)
            width = int(width)
            height = int(height)
            shift = 8 - (width % 8)
            bitmap = [ int(t, 16) >> shift for t in bitmap.split("\n") ]

            if len(bitmap) != height:
                raise ValueError(f"{name} bitmap has wrong size")
          
            glyphs[encoding] = bitmap

    data = (
        fontname,
        width,
        height,
        1,
        glyphs,
    )
    with open(os.path.join(destdir, f"{fontname}.pickle"), 'wb') as fd:
        pickle.dump(data, fd)

if __name__ == '__main__':
    run()
