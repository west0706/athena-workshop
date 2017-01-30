while read p; do
  ./setup-emr.sh $p
done <students.txt
