#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:        practice_plotting
# Purpose:     Plots a /24 block
#
# Author:      andy
#
# Created:     10/10/2014
#-------------------------------------------------------------------------------

import re, sys, StringIO, os, argparse, string, collections
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import matplotlib.ticker as ticker
import numpy as np
import time
from PIL import Image
from datetime import datetime
import dateutil.parser

parser = argparse.ArgumentParser()
parser.add_argument("--img_save_dir", help="Chooses directory to save images", default='sample.images')
parser.add_argument("--use_EB", help="Uses an EB.png file")
parser.add_argument("--UTC_time", help="Selects the start UTC from probing.", default="0")
parser.add_argument("--format", help="Selects the file format for image.", default=".pdf")
args = parser.parse_args()

if not os.path.exists(args.img_save_dir):
    os.makedirs(args.img_save_dir)
    os.chdir(args.img_save_dir)
else:
    os.chdir(args.img_save_dir)

block = {}
min_time = 10000000000000000000000000
max_time = 0

for line in sys.stdin:
  line = line.strip()
  tmp = line.split('\t')

  if tmp[1] in block.keys():
    block[tmp[1]].append(tmp[0])
    block[tmp[1]].append(tmp[2])
  else:
    block[tmp[1]] = [tmp[0], tmp[2]]
  file_name = tmp[1]
  file_name = file_name[0:6]

  if int(min_time) > int(tmp[0]):
    min_time = int(tmp[0])
  elif int(max_time) < int(tmp[0]):
    max_time = int(tmp[0])

block_final = collections.OrderedDict(sorted(block.items()))
ncols = (max_time - min_time)/ 660

for keys, i in block_final.iteritems():
  if len(i) / 2 > ncols:
    ncols = len(i) / 2

fig = plt.figure(num=None, figsize=(11, 3), dpi=100)
rect = fig.add_subplot(111)

nrows = 256
rect_start = 0
length = 0

#setting the background
r1 = ptch.Rectangle((0,0), ncols, nrows, color="blue", fill=True)
rect.add_patch(r1)

#This goes through the file, counting rectangles to find differences and plot
#Across widths
for keys, i in block_final.iteritems():
    if keys == min_time:
      rect_start = min_time
    #for item in i: #THIS SOEMTIMES GOES THRU ERRYTHANG IN A WHOLE LIST pls fix
    #  print item
    keyword = str(keys)
    passer = int(keyword[6:],16)

    for (count, returnval) in enumerate(i[1::2]):
      if len(i) - (count * 2) == 2:
        to_end = ncols - (int(i[count * 2]) - int(min_time)) / 660
      else:
        to_next = (int(i[(count + 1) * 2]) - int(min_time)) / 660 - (int(i[count * 2]) - int(min_time)) / 660
      if returnval == '0':   # block not probed
        if len(i) - (count * 2) == 2:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#ADD8E6")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_end - 1 , 1, color="blue")
          rect.add_patch(r1)
        else:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="ADD8E6")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_next - 1, 1, color="blue")
          rect.add_patch(r1)
      if returnval == '1':
        if len(i) - (count * 2) == 2:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#666666")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_end - 1, 1, color="black")
          rect.add_patch(r1)
        else:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#666666")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_next - 1, 1, color="black")
          rect.add_patch(r1)
      if returnval == '2':
        if len(i) - (count * 2) == 2:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#f49797")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_end - 1, 1, color="red")
          rect.add_patch(r1)
        else:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#f49797")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_next - 1, 1, color="red")
          rect.add_patch(r1)
      if returnval == '3':
        if len(i) - (count * 2) == 2:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#008000")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_end - 1, 1, color="#00FF00")
          rect.add_patch(r1)
        else:
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660, passer), 1, 1, color="#008000")
          rect.add_patch(r1)
          r1 = ptch.Rectangle(((int(i[count * 2]) - int(min_time)) / 660 + 1, passer), to_next - 1, 1, color="#00FF00")
          rect.add_patch(r1)

#layout
plt.xlim([0, ncols])
plt.ylim([0, nrows])
plt.gca().invert_yaxis()
plt.tick_params(axis='y', right='off', direction='out')
plt.xlabel('Time (11-minute rounds) & (UTC Time)')
plt.ylabel('IP address (last octet)')
plt.tight_layout()

"""#title
plot_ip = [0,0,0]
listip = [listx[0][:2], listx[0][2:4], listx[0][4:6]]
for ipnum in range(3):
  plot_ip[ipnum] = str('%02d' % string.atoi(listip[ipnum],16))
title = plot_ip[0] + '.' + plot_ip[1] + '.' + plot_ip[2]
plt.text(-140,20,'Address Survey, block ' + title + '/24', horizontalalignment='center', rotation='vertical', fontsize=12)
"""

#ticks
rect.set_yticks([0, 64, 128, 192, 256])
xaxisbot = [11 * 33 * x for x in range(ncols / 33 + 2)]

xaxistop = [x2 * 110 for x2 in range(ncols / 110 + 1)]
rect.tick_params(axis='both', which='both', labelsize=8, direction='out')
if args.UTC_time != 0:
  xaxisbotlabel = [time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(float(min_time) + 60 * 11 * (ncols / 5) * x))[:-1] for x in range(ncols / 33 + 1)]
  rect.set_xticklabels(xaxisbotlabel, rotation=50, ha="right")
rect.set_xticks(xaxisbot)

rect2 = rect.twiny()
rect2.xaxis.set_ticks(np.arange(0, ncols, 150))
rect2.xaxis.tick_top()
rect2.tick_params(axis='both', which='both', labelsize=8, direction='out')

rect.set_xlim(0, ncols)
rect2.set_xlim(0, ncols)

#Saving with help of the flags
if args.use_EB:
  file_name += ".Eb"
  plt.savefig(file_name + str(args.format), bbox_inches='tight', transparent=True)
  print "Generated image.Eb " + file_name + str(args.format)
else:
  plt.savefig(file_name + str(args.format), bbox_inches='tight', transparent=True)
  print "Generated image " + file_name + str(args.format)