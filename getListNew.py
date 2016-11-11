#!/usr/bin/env python
import os, sys
import json

import re
def getLabelB(text):
  Whp = re.compile('W.*\d_RB')
  RBp = re.compile('_RB\d.*_S')
  Sep = re.compile('S\d\d')

  aaa=Whp.findall(text)
  bbb=RBp.findall(text)
  ccc=Sep.findall(text)

  Wh=int(aaa[0].replace("W","").replace("_RB",""))
  RB=int(bbb[0].replace("_S","").replace("_RB","").replace("in","").replace("out","").replace("+","").replace("-",""))
  Se=int(ccc[0].replace("S",""))

  RBsub = bbb[0].replace("_S","").replace("_","")
  DQMname="W"
  if Wh>-1: DQMname+="+"+str(Wh)+"_"+RBsub+"_"+ccc[0]
  else    : DQMname+=    str(Wh)+"_"+RBsub+"_"+ccc[0]

  return {"name":text,"DQMname":DQMname, "Wheel":Wh, "Station":RB, "Sector":Se }
def getLabelE(text):
  DIp = re.compile('RE.*\d_R')
  RIp = re.compile('_R\d.*_CH')
  CHp = re.compile('CH\d\d')

  aaa=DIp.findall(text)
  bbb=RIp.findall(text)
  ccc=CHp.findall(text)

  DI=int(aaa[0].replace("RE","").replace("_R",""))
  RI=int(bbb[0].replace("_CH","").replace("_R",""))
  CH=int(ccc[0].replace("CH",""))
  DQMname="RE"
  CH2 = str(CH)
  if CH<10 : CH2="0"+str(CH)

  if DI>0 : DQMname+="+"+str(DI)+"_R"+str(RI)+"_CH"+str(CH2)
  else    : DQMname+=    str(DI)+"_R"+str(RI)+"_CH"+str(CH2)

  return {"name":text,"DQMname":DQMname, "Disk":DI, "Ring":RI, "Chamber":CH }


def getListB(allBLabels,thB):
  aaaa = []
  selBLabels=[]
  for i in allBLabels:
    if jsBRate['data2'][i]>int(thB):
      ii=i.replace('Backward','B').replace('Forward','F').replace('Middle','M')
      selBLabels.append(ii)
  selBLabels.sort()
  ii=""
  iii=""
  for i in selBLabels:
    if not (ii[0:len(ii)-1] == i[0:len(i)-1]):
      if iii == "" :
        aaaa.append(ii)
      else :
        aaaa.append(ii+""+iii)
      iii=""
      ii=i
    else :
      iii+="/"+i[len(i)-1]
  return aaaa

def getListE(allELabels,thE):
  aaaa = []
  selELabels=[]
  for i in allELabels:
    if jsERate['data2'][i]>int(thE):
      selELabels.append(i)

  selELabels.sort()
  ii=""
  iii=""
  for i in selELabels:
    if not (ii[0:len(ii)-1] == i[0:len(i)-1]):
      if iii == "" :
        aaaa.append(ii)
      else :
        aaaa.append(ii+""+iii)
      iii=""
      ii=i
    else :
      iii+="/"+i[len(i)-1]
  return aaaa



if len(sys.argv) < 2:
	print "Usage: %s RUNNUMBER threshold_B threshold_E" % sys.argv[0]
	sys.exit()

runNumber = sys.argv[1]

jsBRate = json.loads(open("cache/%s/Brate.json" % runNumber).read())
jsERate = json.loads(open("cache/%s/Erate.json" % runNumber).read())
DataSet={"273402":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273425":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273446":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273502":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273523":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273537":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273554":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273589":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273590":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273592":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "273725":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274094":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274102":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274103":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274104":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274105":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274106":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274107":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274108":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274146":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274172":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274198":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274240":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274250":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274284":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274314":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274335":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274387":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274440":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274954":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274968":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "274998":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275059":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275124":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275282":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275309":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275319":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275337":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275344":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275370":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275375":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO", "275657":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "275886":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "275890":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "275911":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "275912":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "275963":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "276092":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "276282":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "276283":"SingleMuon/Run2016C-23Sep2016-v1/DQMIO", "276315":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276355":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276437":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276495":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276525":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276542":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276581":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276653":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276775":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276807":"SingleMuon/Run2016D-23Sep2016-v1/DQMIO", "276870":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "276940":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "277094":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "277126":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "277166":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "277180":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "277420":"SingleMuon/Run2016E-23Sep2016-v1/DQMIO", "278017":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278167":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278288":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278308":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278345":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278509":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278801":"SingleMuon/Run2016F-23Sep2016-v1/DQMIO", "278820":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "278957":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "278962":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "278969":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279024":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279080":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279115":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279488":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279681":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279715":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279760":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279823":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279887":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279966":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "279993":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO", "280383":"SingleMuon/Run2016G-23Sep2016-v1/DQMIO","273492":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO","274159":"SingleMuon/Run2016B-23Sep2016-v3/DQMIO"}


#https://cmsweb.cern.ch/dqm/offline/plotfairy/archive/273402/SingleMuon/Run2016B-23Sep2016-v3/DQMIO/RPC/AllHits/Barrel/Wheel_-2/sector_1/station_1/Occupancy_W-2_RB1out_S01?session=1lvh8D;v=1477947284567439838;w=946;h=489
DQMlink=""#"https://cmsweb.cern.ch/dqm/offline/plotfairy/archive/"+runNumber+"/"+DataSet[runNumber]+"/RPC/AllHits/"
DQMlink2="?session=mhEYG5;v=1477947284567439838;w=946;h=489"
allBLabels=jsBRate['data2'].keys()
selBLabels = []
IMGlinks=[]
for i in ["40","35","30","25","20"]:
  aaa = getListB(allBLabels,i)
  if len(aaa)>1:
    aaa.remove("")
    if len(aaa)>4 or i =="20":
      print "8-1. Barrel Occupancy "
      print "Chambers with high occupancy levels (rate>"+i+"Hz)"
      for aa in aaa:
        print aa
        a=getLabelB(aa)
        barrel="Barrel/Wheel_"+str(a["Wheel"])+"/sector_"+str(a["Sector"])+"/station_"+str(a["Station"])+"/Occupancy_"+str(a["DQMname"])
        #print DQMlink+barrel+DQMlink2
        dicc = {"l":DQMlink+barrel+DQMlink2,"s":"Occupancy_"+str(a["DQMname"]) }
        IMGlinks.append(dicc)
        #print a
     
      break
    aaa=[]

#https://cmsweb.cern.ch/dqm/offline/plotfairy/archive/273402/SingleMuon/Run2016B-23Sep2016-v3/DQMIO/RPC/AllHits/Endcap%2B/Disk_1/ring_2/sector_1/Occupancy_RE%2B1_R2_CH01?session=mhEYG5;v=1477947284567439838;w=946;h=489
allELabels=jsERate['data2'].keys()
selELabels = []
for i in ["40","35","30","25","20","15"]:
  bbb=getListE(allELabels,i)
  if len(bbb)>1:
    bbb.remove("")
    if len(bbb)>7 or i=="15":
      print "8-2. Endcap Occupancy "
      print "Chambers with high occupancy levels (rate>"+i+"Hz)"
      for bb in bbb:
        print bb
        b=getLabelE(bb)
        endcap=""
        if b['Ring']>1:
          if b["Disk"]>0:  endcap="Endcap+/Disk_"+str(b["Disk"])+"/ring_"+str(b["Ring"])+"/sector_"+str(int((b["Chamber"]-1)/6+1))+"/Occupancy_"+b["DQMname"]
          else:            endcap="Endcap-/Disk_"+str(b["Disk"])+"/ring_"+str(b["Ring"])+"/sector_"+str(int((b["Chamber"]-1)/6+1))+"/Occupancy_"+b["DQMname"]
        #print endcap
          dicc = {"l":DQMlink+endcap+DQMlink2,"s":"Occupancy_"+b["DQMname"]} 
          IMGlinks.append(dicc)
        #print b
     
      break
    bbb=[]
#for i in IMGlinks:
#  print "$CURL "+i["l"]+" -o $WORKDIR/cache/"+runNumber+"/"+i["s"]+".png"

