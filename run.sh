#!/bin/bash

if [ $# != 2 ]; then
  echo "RPC simple e-log generator"
  echo "Usage: $0 DATATYPE RUNNUMBER"
  exit 1
fi
TYPE=$1
RUN=$2

if [ $TYPE != Cosmics ] && [ $TYPE != Collisions ]; then
  echo "DATATYPE must be Cosmics or Collisions"
  exit 1
fi

## Define global variables
WORKDIR=`pwd`
OUTDIR=$WORKDIR/cache/$RUN
COOKIENTL=$WORKDIR/cache/cookiefile-ntl.txt
URLNTL="https://rpcbackground.web.cern.ch/rpcbackground/Plots/GR2014"
COOKIEWBM=$WORKDIR/cache/cookiefile-wbm.txt
URLWBM="https://cmswbm.web.cern.ch/cmswbm"
if [ $TYPE == Cosmics ]; then
  if [ $RUN -le 262455 ]; then ## 262455 is the latest run visible in the DQM
    DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2015/Cosmics"
    #DQM2="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Commissioning2015/StreamExpressCosmics"
  elif [ $RUN -le 263797 ]; then ## 263797 is the latest HI cosmic run visible in the DQM
    DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/HIRun2015/Cosmics"
  else ## FIXME: similar elif have to be added after Run2016's
    DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2016/Cosmics"
    DQM2="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Commissioning2016/Cosmics"
  fi
else
  # NOTE : Dataset name /SingleMu/ is changed to /SingleMuon/ from Run2015B
  if [ $RUN -le 251155 ]; then
     DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2015/SingleMu"
  elif [ $RUN -le 261422 ]; then
    DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2015/SingleMuon"
    DQM2="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2015/SingleMuon_0T"
  elif [ $RUN -le 263757 ]; then
    DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/HIRun2015/HIOniaL1DoubleMu0"
  else
    ## Placeholder for the 2016 runs
    DQM1="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2016/SingleMuon"
    DQM2="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2016/SingleMuon_0T"
  fi
  #DQM2="https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2015/StreamExpress"
fi
#DQM3="https://cmsweb.cern.ch/dqm/online/data/browse/ROOT"

if [ -d $OUTDIR ]; then
  echo "Erasing old files for run ${RUN}"
  rm -rf $OUTDIR
fi

mkdir -p $OUTDIR

## Setup CMSSW
echo "@@@ Setting up CMSSW @@@"
cd /cvmfs/cms.cern.ch/slc6_amd64_gcc493/cms/cmssw/CMSSW_8_0_1
eval `scram runtime -sh`
cd $WORKDIR

## Check voms
echo "@@@ Checking user certificate @@@"
USERKEY=~/.globus/userkey.pem
USERCERT=~/.globus/usercert.pem
if [ ! -f $USERKEY -o ! -f $USERCERT ]; then
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "!! Cannot find usercert.pem or userkey.pem !!"
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  exit 2
fi

voms-proxy-info > /dev/null
if [ $? != 0 ]; then
  voms-proxy-init -voms cms
  voms-proxy-info > /dev/null
  if [ $? != 0 ]; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "!!VOMS proxy is not initialized!!"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    exit 2
  fi
fi
VOMS_PROXY=`voms-proxy-info | grep ^path | sed 's/^path *: *//g'`

[ -f $COOKIENTL ] || cern-get-sso-cookie --krb -u $URLNTL -o $COOKIENTL
[ -f $COOKIEWBM ] || cern-get-sso-cookie --krb -u $URLWBM -o $COOKIEWBM

## Download NoiseTool pages
echo "@@@ Retrieving data from NoiseTool @@@"
CURL="curl -s -L --cookie $COOKIENTL --cookie-jar $COOKIENTL"
if [ ! -f $OUTDIR/index.html ]; then
  $CURL $URLNTL/run${RUN}/index.html -o $OUTDIR/index.html
  $CURL $URLNTL/run${RUN}/barrel.root -o $OUTDIR/barrel.root
  $CURL $URLNTL/run${RUN}/endcap.root -o $OUTDIR/endcap.root
fi
grep -q "404 - Not found" $OUTDIR/index.html
if [ $? -eq 0 ]; then
  echo "!!! Noise analysis not found in web server !!!"
  rm -f $OUTDIR/index.html
  rm -f $OUTDIR/barrel.root
  rm -f $OUTDIR/endcap.root
fi

## Download WBM JSON files
echo "@@@ Retrieving data from RPC WBM @@@"
CURL="curl -s -L --cookie $COOKIEWBM --cookie-jar $COOKIEWBM"
if [ ! -f $OUTDIR/runSummary.json ]; then
  $CURL "$URLWBM/cmsdb/servlet/RPCRunSummary2?TopMenu=RPCRunSummary2&TopMenu2=ZeroPage&Run=${RUN}" -o $OUTDIR/runSummary.json

  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=0&isHist=1&SubMenu=0&Run=${RUN}" -o $OUTDIR/Brate.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=0&isHist=1&SubMenu=1&Run=${RUN}" -o $OUTDIR/BtoEnable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=0&isHist=1&SubMenu=2&Run=${RUN}" -o $OUTDIR/BtoDisable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=0&isHist=1&SubMenu=3&Run=${RUN}" -o $OUTDIR/BdeadStrip.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=0&isHist=1&SubMenu=4&Run=${RUN}" -o $OUTDIR/Bdisabled.json

  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=1&isHist=1&SubMenu=0&Run=${RUN}" -o $OUTDIR/Erate.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=1&isHist=1&SubMenu=1&Run=${RUN}" -o $OUTDIR/EtoEnable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=1&isHist=1&SubMenu=2&Run=${RUN}" -o $OUTDIR/EtoDisable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=1&isHist=1&SubMenu=3&Run=${RUN}" -o $OUTDIR/EdeadStrip.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isSP=1&isHist=1&SubMenu=4&Run=${RUN}" -o $OUTDIR/Edisabled.json

  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isHist=0&SubMenu=0&Run=${RUN}" -o $OUTDIR/rateTable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isHist=0&SubMenu=1&Run=${RUN}" -o $OUTDIR/toEnableTable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isHist=0&SubMenu=2&Run=${RUN}" -o $OUTDIR/toDisableTable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isHist=0&SubMenu=3&Run=${RUN}" -o $OUTDIR/deadStripTable.json
  $CURL "$URLWBM/cmsdb/servlet/RPCBackground?isHist=0&SubMenu=4&Run=${RUN}" -o $OUTDIR/disabledTable.json


fi

## Download DQM
echo "@@@ Retrieving data from DQM @@@"
CURL="curl -s -L --cert $VOMS_PROXY --key $VOMS_PROXY -k"
DQMSUBDIR1="$DQM1/`printf "%07dxx" $(($RUN/100))`"
DQMSUBDIR2="$DQM2/`printf "%07dxx" $(($RUN/100))`"
#DQMSUBDIR3="$DQM3/`printf "%05dxxxx" $(($RUN/10000))`/`printf "%07dxx" $(($RUN/100))`"

$CURL $DQMSUBDIR1 -o $OUTDIR/DQMFileList.html
DQMFILE=""

for F in `cat $OUTDIR/DQMFileList.html | grep -o "DQM_V[0-9]\+_R0*${RUN}__[^><']*.root" | grep "23Sep2016"`; do
  ## Loop over $DQMFILES but break to be safe for multiple matching
  DQMFILE=$F
  DQMSUBDIR=$DQMSUBDIR1
  echo $DQMFILE
  break ## Loop over $DQMFILES but break to be safe for multiple matching
done

if [ _$DQMFILE == "_" ]; then
    if [ ! -f $OUTDIR/DQMFileList2.html ]; then
	$CURL $DQMSUBDIR2 -o $OUTDIR/DQMFileList2.html
    fi
    for F in `cat $OUTDIR/DQMFileList2.html | grep -o "DQM_V[0-9]\+_R0*${RUN}__[^><']*.root"`; do
   ## Loop over $DQMFILES but break to be safe for multiple matching
	DQMFILE=$F
	DQMSUBDIR=$DQMSUBDIR2
	echo $DQMFILE
	
	break ## Loop over $DQMFILES but break to be safe for multiple matching
    done
fi
#if [ ! -f $OUTDIR/DQMFileLis3.html ]; then
#  $CURL $DQMSUBDIR3 -o $OUTDIR/DQMFileList3.html
#fi
#for F in `cat $OUTDIR/DQMFileList3.html | grep -o "DQM_V[0-9]\+_RPC_R0*${RUN}.root"`; do
#  ## Loop over $DQMFILES but break to be safe for multiple matching
#  DQMFILE3=$F
#  if [ _$DQMFILE == "_" ]; then
#    DQMFILE=$F
#    DQMSUBDIR=$DQMSUBDIR3
#  fi
#  echo $DQMFILE3
#  $CURL "$DQMSUBDIR3/$DQMFILE3" -o $OUTDIR/$DQMFILE3
#  break ## Loop over $DQMFILES but break to be safe for multiple matching
#done
if [ _$DQMFILE == "_" ]; then
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "!!Cannot find DQM root file!!"
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  exit 3
fi
## Now we are ready to download DQM.root
$CURL "$DQMSUBDIR/$DQMFILE" -o $OUTDIR/$DQMFILE

echo "@@@ All files are ready. Start analysis @@@"
echo "@@@ Start analysis of $RUN @@@"
python analyze.py $TYPE $RUN
