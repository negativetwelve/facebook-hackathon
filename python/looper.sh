while true; do
  python fileIO.py;
  mv raw_data/output.txt raw_data/output-`date +%s`.txt;
  sleep 3;
done;