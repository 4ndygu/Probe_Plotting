#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:        practice_plotting
# Purpose:     Plots a /24 block
#
# Author:      andy
#
# Created:     10/10/2014
#-------------------------------------------------------------------------------

import re, sys, StringIO, os, argparse, string
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

for line in sys.stdin:
  fig = plt.figure(num=None, figsize=(11, 3), dpi=100)
  rect = fig.add_subplot(111)
  #I used the same tools as the old code to strip the text.
  line = line.strip()

  if line.find('\t') == -1:
    continue
  tmp = line.split('\t')
  file_name = tmp[0]
  file_name = file_name[0:6]
  listx = tmp[1].split(' ')
  ncols = len(listx[1])
  nrows = 256
  rect_start = 0
  length = 0

  #setting the background
  r1 = ptch.Rectangle((0,0), ncols, nrows, color="blue", fill=True)
  rect.add_patch(r1)

  #This goes through the file, counting rectangles to find differences and plot
  #Across widths
  for i in range(nrows):
    for (count, num) in enumerate(listx[2 * i + 1]):
      if count == 0:
          rect_start = count
      elif num == listx[2 * i + 1][count-1]:
          length += 1
      elif listx[2 * i + 1][count] != listx[2 * i + 1][count-1]:
          if listx[2 * i + 1][count-1] == '0':   # block not probed
              r1 = ptch.Rectangle((rect_start,i), length, 1, color="blue")
              rect.add_patch(r1)
              # add_rect(start,rect_length)
              length = 1
              rect_start = count
          if listx[2 * i + 1][count-1] == '1':   # block non-reply
              r1 = ptch.Rectangle((rect_start,i), length, 1, color="black")
              rect.add_patch(r1)
              length = 1
              rect_start = count
          if listx[2 * i + 1][count-1] == '2':   # block negative reply
              r1 = ptch.Rectangle((rect_start,i), length, 1, color="red")
              rect.add_patch(r1)
              length = 1
              rect_start = count
          if listx[2 * i + 1][count-1] == '3':   # block normal reply
              r1 = ptch.Rectangle((rect_start,i), length, 1, color="#00FF00") #lime green
              rect.add_patch(r1)
              length = 1
              rect_start = count
          if not listx[2 * i + 1][count-1].isdigit(): #block duplicates
              r1 = ptch.Rectangle((rect_start,i), length, 1, color="yellow")
              rect.add_patch(r1)
              length = 1
              rect_start = count

  #layout
  plt.xlim([0, ncols])
  plt.ylim([0, nrows])
  plt.gca().invert_yaxis()
  plt.tick_params(axis='y', right='off', direction='out')
  plt.xlabel('Time (11-minute rounds) & (UTC Time)')
  plt.ylabel('IP address (last octet)')
  plt.tight_layout()

  #title
  plot_ip = [0,0,0]
  listip = [listx[0][:2], listx[0][2:4], listx[0][4:6]]
  for ipnum in range(3):
    plot_ip[ipnum] = str('%02d' % string.atoi(listip[ipnum],16))
  title = plot_ip[0] + '.' + plot_ip[1] + '.' + plot_ip[2]
  plt.text(-140,20,'Address Survey, block ' + title + '/24', horizontalalignment='center', rotation='vertical', fontsize=12)


  #ticks
  rect.set_yticks([0, 64, 128, 192, 256])
  xaxisbot = [11 * 33 * x for x in range(ncols / 33 + 2)]

  xaxistop = [x2 * 110 for x2 in range(ncols / 110 + 1)]
  rect.tick_params(axis='both', which='both', labelsize=8, direction='out')
  if args.UTC_time != 0:
    xaxisbotlabel = [time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(float(args.UTC_time) + 60 * 11 * (ncols / 5) * x))[5:-1] for x in range(ncols / 33 + 1)]
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