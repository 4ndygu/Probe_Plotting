#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      andy
#
# Created:     03/11/2014
# Copyright:   (c) andy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import base64, sys, struct
import fileinput
from string import maketrans

def read_subplot_data(filename):
    data_f = open(filename, "r")
    values = []
    res = []
    print data_f
    for line in data_f:
        line = line.rstrip()
        if line.startswith('#fsdb'):
            expected_schema = '#fsdb -F t block round_no round_start_epoch a_short a_oper a_long status belief n_pos n_neg probe_log'
            if line != expected_schema:
                raise ValueError('input file format has odd schema: ' + line + "\n\tnot " + expected_schema)
        if line.startswith('#'):
            continue
        f = line.strip().split('\t')
        decoded = base64.b64decode(str(f[9]))

        valuenum = map(lambda x: (struct.unpack("B", str(x))), decoded)
        valuenum = map(list, valuenum)

        values1 = []
        for i in range(len(valuenum)):
            values1.append(valuenum[i][0])

        i = 0
        flags = 0
        count = 0

        full_flags = []
        while i < len(values1):
            count = values1[i] >> 3
            flags = values1[i] & 7
            #octets = [values1[j] for j in range(1,count+1)]
            octets = [values1[j] for j in range(1+i,count+i+1)]
            res.append([flags, octets])
            i += count + 1

        for x in res:
            pseq = x
            flags = pseq.pop(0)
            array_set = pseq.pop(0)
            #
            for o in array_set:
              seq = (str(f[2]), str('%08x' % (int(f[0], 16) | o)), str(flags))
              print "\t".join(seq) + "\n"
        del res[:]

probes = read_subplot_data("zff45.e1412154421.a18g.0.r0.001.fsdb")