#!/usr/bin/env python
import os, sys
import json

import sys
if len(sys.argv) < 4:
  sys.exit()

runNumber = int(sys.argv[1])
arg1 = sys.argv[2] # EP4/EP3/EP2/EP1/EM1/EM2/EM3/EM4
arg2 = int(sys.argv[3])

inputs = ["rate","disabled", "deadStrip", "toDisable","toEnable"]
inputs2 = ["Rate","Disabled Strips", "Inactive Strips", "strip To Disable","strip To Enable"]
reads = {}
for i in inputs:
  reads[i]=json.loads(open("cache/%d/%sTable.json"%(runNumber,i)).read())

lefts = (reads['rate'][arg1].keys())
lefts[:] = (value for value in lefts if value.find("W")==-1 and value.find("E")==-1)

lefts.sort()

#print lefts
from ROOT import *
gStyle.SetOptStat(0)
gStyle.SetPalette(1)
gStyle.SetPadTopMargin(0.04)
gStyle.SetPadBottomMargin(0.04)
gStyle.SetPadLeftMargin(0.08)
gStyle.SetPadRightMargin(0.07)

arg2s =["C01-C018","C19-C36"]
c1=TCanvas("c1","",1000,800)
c1.Divide(5,1);
h21 = TH2F("h21",arg1+" "+str(arg2s[arg2])+" "+inputs2[0]+" Run"+str(runNumber),len(lefts),0,len(lefts),18,0,18)
h22 = TH2F("h22",arg1+" "+str(arg2s[arg2])+" "+inputs2[1]+" Run"+str(runNumber),len(lefts),0,len(lefts),18,0,18)
h23 = TH2F("h23",arg1+" "+str(arg2s[arg2])+" "+inputs2[2]+" Run"+str(runNumber),len(lefts),0,len(lefts),18,0,18)
h24 = TH2F("h24",arg1+" "+str(arg2s[arg2])+" "+inputs2[3]+" Run"+str(runNumber),len(lefts),0,len(lefts),18,0,18)
h25 = TH2F("h25",arg1+" "+str(arg2s[arg2])+" "+inputs2[4]+" Run"+str(runNumber),len(lefts),0,len(lefts),18,0,18)
c1.cd(1).SetGrid()
c1.cd(2).SetGrid()
c1.cd(3).SetGrid()
c1.cd(4).SetGrid()
c1.cd(5).SetGrid()
for i,ii in enumerate(lefts):
  h21.GetXaxis().SetBinLabel(i+1,ii)
  h22.GetXaxis().SetBinLabel(i+1,ii)
  h23.GetXaxis().SetBinLabel(i+1,ii)
  h24.GetXaxis().SetBinLabel(i+1,ii)
  h25.GetXaxis().SetBinLabel(i+1,ii)
  for j,jj in enumerate(inputs):
    for k in range(0,18):
      #print str(i)+": "+str(ii)+" : "+str(reads[jj][arg1][ii][k+arg2*18])
      h21.GetYaxis().SetBinLabel(k+1,str(k+1+arg2*18))
      h22.GetYaxis().SetBinLabel(k+1,str(k+1+arg2*18))
      h23.GetYaxis().SetBinLabel(k+1,str(k+1+arg2*18))
      h24.GetYaxis().SetBinLabel(k+1,str(k+1+arg2*18))
      h25.GetYaxis().SetBinLabel(k+1,str(k+1+arg2*18))
      if str(reads[jj][arg1][ii][k]).find("C") is -1:
        if j==0: h21.SetBinContent(int(i+1),int(k+1),round(float(reads[jj][arg1][ii][k+arg2*18])*10.)/10.)
        if j==1: h22.SetBinContent(int(i+1),int(k+1),round(float(reads[jj][arg1][ii][k+arg2*18])*10.)/10.)
        if j==2: h23.SetBinContent(int(i+1),int(k+1),round(float(reads[jj][arg1][ii][k+arg2*18])*10.)/10.)
        if j==3: h24.SetBinContent(int(i+1),int(k+1),round(float(reads[jj][arg1][ii][k+arg2*18])*10.)/10.)
        if j==4: h25.SetBinContent(int(i+1),int(k+1),round(float(reads[jj][arg1][ii][k+arg2*18])*10.)/10.)
h21.SetMaximum(20.)
h22.SetMaximum(5.)
h23.SetMaximum(5.)
h24.SetMaximum(5.)
h25.SetMaximum(5.)
h21.SetTitleSize(2)
h22.SetTitleSize(2)
h23.SetTitleSize(2)
h24.SetTitleSize(2)
h25.SetTitleSize(2)

h21.GetXaxis().SetLabelSize(0.1)
h21.GetYaxis().SetLabelSize(0.1)
h22.GetXaxis().SetLabelSize(0.1)
h22.GetYaxis().SetLabelSize(0.1)
h23.GetXaxis().SetLabelSize(0.1)
h23.GetYaxis().SetLabelSize(0.1)
h24.GetXaxis().SetLabelSize(0.1)
h24.GetYaxis().SetLabelSize(0.1)
h25.GetXaxis().SetLabelSize(0.1)
h25.GetYaxis().SetLabelSize(0.1)

h21.SetMinimum(-0.01)
h22.SetMinimum(-0.01)
h23.SetMinimum(-0.01)
h24.SetMinimum(-0.01)
h25.SetMinimum(-0.01)
h21.SetMarkerSize(1.5)
h22.SetMarkerSize(4.5)
h23.SetMarkerSize(4.5)
h24.SetMarkerSize(4.5)
h25.SetMarkerSize(4.5)
#h2.SetBinContent(5,20,-1.);
c1.cd(1), h21.Draw("colz0text")
c1.cd(2), h22.Draw("colz0text")
c1.cd(3), h23.Draw("colz0text")
c1.cd(4), h24.Draw("colz0text")
c1.cd(5), h25.Draw("colz0text")

OutputName = "Run"+str(runNumber)+"_"+arg1+"_"+arg2s[arg2]
c1.Print(OutputName+".pdf")

