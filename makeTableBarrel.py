#!/usr/bin/env python
import os, sys
import json

import sys
if len(sys.argv) < 4:
  sys.exit()

runNumber = int(sys.argv[1])
arg1 = sys.argv[2] # WM2/WM1/W0/WP1/WP2
arg2 = int(sys.argv[3])

inputs = ["rate","disabled", "deadStrip", "toDisable","toEnable"]
inputs2 = ["Rate","Disabled Strips", "Inactive Strips", "strip To Disable","strip To Enable"]
reads = {}
for i in inputs:
  reads[i]=json.loads(open("cache/%d/%sTable.json"%(runNumber,i)).read())

lefts = (reads['rate'][arg1].keys())
lefts[:] = (value for value in lefts if value.find("W")==-1 and value.find("E")==-1)

if arg2!=4:
  lefts.remove('RB4++_F')
  lefts.remove('RB4++_B')
  lefts.remove('RB4--_F')
  lefts.remove('RB4--_B')
if arg2==9 or arg2==11:
  lefts.remove('RB4+_F')
  lefts.remove('RB4+_B')


lefts.sort()

#print lefts
from ROOT import *
gStyle.SetOptStat(0)
gStyle.SetPalette(1)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadBottomMargin(0.05)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadRightMargin(0.05)


c1=TCanvas("c1","",400,600)
h2 = TH2F("h2",arg1+" S"+str(arg2)+" Run"+str(runNumber),5,0,5,len(lefts),0,len(lefts))
c1.SetGrid()
for i,ii in enumerate(lefts):
  h2.GetYaxis().SetBinLabel(i+1,ii)
  for j,jj in enumerate(inputs):
    #print str(i)+": "+str(ii)+" : "+str(reads[jj][arg1][ii][arg2-1])
    h2.GetXaxis().SetBinLabel(j+1,inputs2[j])
    if reads[jj][arg1][ii][arg2-1] is None:
      continue
#      h2.SetBinContent(int(j+1),int(i+1),-1.)
    elif str(reads[jj][arg1][ii][arg2-1]).find("S") is -1:
      a0 = 0.0
      h2.SetBinContent(int(j+1),int(i+1),round(float(reads[jj][arg1][ii][arg2-1])*10.)/10.+a0)
h2.SetMaximum(5.)
h2.SetMinimum(-0.01)
h2.SetMarkerSize(2.5)
h2.GetYaxis().SetLabelSize(0.05)
#h2.SetBinContent(5,20,-1.);
h2.Draw("colz0text")

OutputName = "Run"+str(runNumber)+"_"+arg1+"_S"+str(arg2)
c1.Print(OutputName+".pdf")
