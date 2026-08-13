#!/usr/bin/env python
#
# hex2pickle.py -- convert HEX font files into a dict and save it in a pickle
#     for later loading
#

import argparse, re, os.path, pickle, gzip

def run():
    cmdline = argparse.ArgumentParser(description="Convert a HEX font file into a pickle in current directory.  NOTE: Wide glyphs are NOT supported!")
    cmdline.add_argument('hexfile', help='HEX file to convert')
    cmdline.add_argument('size', help='Size of font. Format <w>x<h>, eg., 8x16.  Both height and width must be divisible by 8')
    cmdline.add_argument('fontname', help='Name of the font, default is <hexfile until first . in filename>.', default=None, nargs="?")
    cmdline.add_argument('--wide', help="Support wide glyphs.  A wide glyph will have it's first half stored in the specified encoding, and its second half at encoding+0x80000.", action='store_true')
    cmdline.add_argument('--firsthalf', help="Used in combination with --wide.  Only store the first half of wide glyphs.", action="store_true")
    cmdline.add_argument('--skipwide', help="Skip generation of wide glyphs.", action='store_true')
    args = cmdline.parse_args()

    convert(args)

def convert(args):
    fontname = args.fontname if args.fontname is not None else os.path.basename(args.hexfile).split(".")[0]

    width, height = [ int(t) for t in args.size.split("x") ]
    glyphs = {}

    with open(args.hexfile, 'r') as FD:
        for line in FD:
            line = line.strip()
            if not line:
                continue

            encoding, bitmap = line.split(":")
            encoding = int(encoding, 16)

            if len(bitmap) == (width//8)*2*height:
                bitmap = [ int(t, 16) for t in re.findall("."*((width//8)*2), bitmap) ]
            elif args.skipwide and len(bitmap) == (width//8)*4*height:
                print(f"skipped encoding {encoding:x} because it is a wide glyph")
                continue
            elif args.wide and len(bitmap) == (width//8)*4*height:
                if not args.firsthalf:
                    bwide = [ int(t, 16) for t in re.findall("."*((width//8)*2)+"("+"."*((width//8)*2)+")", bitmap) ]
                    glyphs[encoding + 0x1000000] = bwide
                bitmap = [ int(t, 16) for t in re.findall("("+"."*((width//8)*2)+")"+"."*((width//8)*2), bitmap) ]
                print(f"created wide glyph for encoding {encoding:x} ({encoding+0x1000000:x})")
            else:
                raise ValueError(f"encoding {encoding:x} bitmap size mismatch")
         
            glyphs[encoding] = bitmap

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
