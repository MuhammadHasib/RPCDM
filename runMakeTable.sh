RUN=$1
for i in WM2 WM1 W0 WP1 WP2
do
  for j in {1..12}
  do
    python makeTableBarrel.py $RUN $i $j -b
  done
done 
for i in EN4 EN3 EN2 EN1 EP1 EP2 EP3 EP4
do
  python makeTableEndcap.py $RUN $i 0 -b
  python makeTableEndcap.py $RUN $i 1 -b
done
