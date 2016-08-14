#!/bin/bash
if [ "$#" -ne 4 ]; then
  echo "usage: ./get_email.sh <listfile> <outfile> <memberlist> <cookiefile> in relative paths"
  echo "ex) ./get_email.sh results/results-15fa_deans/full-list.tsv results/results-15fa_deans/email-list.txt" \
  "data/member-email-list.txt data/cookies.txt"
  exit 1
fi

studentlist=$1
emaillist=$2
memberlist=$3
cookies=$4

tmp="emaillist.tmp"
rm ${tmp}
rm ${emaillist}

while read line; do
  search_value=$(echo "${line}" | awk -F'\t' '{print $5" "$6" "$4}' | tr -s ' ' '+')
  netid=$(wget -qO- --load-cookies ${cookies} \
  "https://illinois.edu/ds/secSearch?skinId=0&sub=&search=${search_value}&search_type=student" |\
  grep -o 'displayIllinois(\".*\")' | cut -d "\"" -f2 | cut -d "\"" -f1)
  if [ "${netid}" == "" ]
  then
    echo "" >> ${tmp}
  else
    echo "${netid}@illinois.edu" >> ${tmp}
  fi
done <${studentlist}

sort ${tmp} ${memberlist} ${memberlist} | uniq -u > ${emaillist}
rm ${tmp}
total=$(wc -l ${emaillist} | awk -F' ' '{print $1}')
echo "${total} email addresses"