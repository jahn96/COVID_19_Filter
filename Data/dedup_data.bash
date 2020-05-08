#!/bin/bash

csv_file="$1"

head -n 1 "$csv_file" > "./Data/deduped_data.csv"

# remove header
data="$(tail -n+2 $csv_file)" 

# merge an article written in multiple lines into a line 
ARRAY=()
echo "$data" |
while read -r p; do
    #echo "p: $p"
    res="$(echo $p | grep -e '\r$')";

    #echo "res: $res"
    if [[ "$res" != "" ]]; then
        ARRAY+=("$res")
        #echo "array: ${ARRAY[@]}"
        echo "${ARRAY[@]}" >> "temp.csv"
        ARRAY=()
    else
        #res="$(echo $p | tr -d '\r')"
        ARRAY+=("$p")
    fi
done 

# remove , inside the quotes and dedup by doi if it has doi else it will dedup by title 
awk -F '"' -v OFS='' '{ for (i=2; i <=NF; i+=2) gsub(",", "", $i) } 1' "temp.csv" | awk -F ',' '{if(($5 != "") && (! doi_seen[$5])){print $0; doi_seen[$5]++} else if(($5 == "") && (! title_seen[$4])){print $0; title_seen[$4]++}}' >> "./Data/deduped_data.csv"

# remove temp.csv
rm temp.csv 
