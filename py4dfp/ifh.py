# emacs: -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set fileencoding=utf-8 ft=python sts=4 ts=4 sw=4 et:

import io
import re
from pyparsing import restOfLine,Group,Literal,Suppress,White,Word, \
    ZeroOrMore


# Standard Interfile keys
kMagic = 'INTERFILE'
ktMagic = Literal(kMagic)
# imaging modality | image modality
kKeysVersion = 'version of keys'
ktKeysVersion = Literal(kKeysVersion)
kConvProg = 'conversion program'
ktConvProg = Literal(kConvProg)
# program author
# program version
# program date
# data description
# data starting block
# data offset in bytes
kDataFileName = 'name of data file'
ktDataFileName = Literal(kDataFileName)
# data compression
# data encode
# comment
# type of data
# total number of images
kByteOrder = 'imagedata byte order'
ktByteOrder = Literal('imagedata byte order')
# number of energy windows
# process status
kMatrixSize = 'matrix size'
kMatrixSize1 = kMatrixSize + ' [1]'
ktMatrixSize1 = Literal(kMatrixSize1)
kMatrixSize2 = kMatrixSize + ' [2]'
ktMatrixSize2 = Literal(kMatrixSize2)
kNumberFormat = 'number format'
ktNumberFormat = Literal(kNumberFormat)
kNBytesPerPixel = 'number of bytes per pixel'
ktNBytesPerPixel = Literal(kNBytesPerPixel)
kScalingFactor = 'scaling factor (mm/pixel)'
kScalingFactor1 = kScalingFactor + ' [1]'
ktScalingFactor1 = Literal(kScalingFactor1)
kScalingFactor2 = kScalingFactor + ' [2]'
ktScalingFactor2 = Literal(kScalingFactor2)
# number of projections
# extent of rotation
# maximum pixel count
# patient orientation
# patient rotation
# SPECT STUDY (acquired data)
# direction of rotation
# start angle
# centre of rotation | center of rotation
# SPEC STUDY (reconstructed data)
# method of reconstruction
# number of slices
# attenuation correction coefficient/cm
#   | method of attenuation correction
#   | scatter corrected
#   | method of scatter correction
# end of interfile
# radius of rotation
# crystal to focus

## Macquarie University extensions
# [mqu] image scale factor | RPAH Scale
# [mqu] phantom description
# [mqu] average count per pixel

## Washington University 4dfp extensions
kMatrixSize3 = kMatrixSize + ' [3]'
ktMatrixSize3 = Literal(kMatrixSize3)
kMatrixSize4 = kMatrixSize + ' [4]'
ktMatrixSize4 = Literal(kMatrixSize4)

kScalingFactor3 = kScalingFactor + ' [3]'
ktScalingFactor3 = Literal(kScalingFactor3)

kOrientation = 'orientation'
ktOrientation = Literal(kOrientation)
kNDimensions = 'number of dimensions'
ktNDimensions = Literal(kNDimensions)
kMmppix = 'mmppix'
ktMmppix = Literal(kMmppix)
kCenter = 'center'
ktCenter = Literal(kCenter)

tKey = ktMagic | ktKeysVersion | ktNumberFormat | ktConvProg \
    | ktDataFileName | ktNBytesPerPixel | ktByteOrder | ktOrientation \
    | ktNDimensions | ktMatrixSize1 | ktMatrixSize2 | ktMatrixSize3 \
    | ktMatrixSize4 | ktScalingFactor1 | ktScalingFactor2 \
    | ktScalingFactor3 | ktMmppix | ktCenter
tAssign = Literal(':=')
tValue = Suppress(White()) + restOfLine

kvpair = tKey + Suppress(tAssign) + tValue

def to_dict(ifh_file):
    """Reads an IFH file as a dictionary.

Reads the named file, a 4dfp-accented Interfile header, and turns
the keys and values into a dictionary.
Args:
    ifh_file: String path to a .4dfp.ifh file

Returns:
    A dict representing the contents of the named IFH file.
    Keys that have array form, such as 'matrix size [i]', are
    altered so that the key does not include the index
    ('matrix size') and the value is a map from numeric index
    to value {1:"48",2:"64",3:"48",4:"497"}.

Raises:
    IOError: An error occurred accessing the IFH file
    ParseException: The IFH file contents are invalid
    """
    d = {}
    f = open(ifh_file, 'r')
    try:
        for line in f:
            kv = kvpair.parseString(line)
            if 2 == len(kv):
                (key,val) = kv;
                mi = re.match('(.*)\s+\[(\d+)\]\Z', key)
                if mi:          # array-element-style key
                    key = mi.group(1)
                    idx = int(mi.group(2))
                    if key in d:
                        d[key][idx] = val
                    else:
                        d[key] = {idx:val}
                else:
                    d[key] = val
            else:               # only key, no value
                d[kv[0]] = None;
        return d
    finally:
        f.close()
