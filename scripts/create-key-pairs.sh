while read p; do
  aws ec2 create-key-pair --key-name $p > $p.pem
done <students.txt
