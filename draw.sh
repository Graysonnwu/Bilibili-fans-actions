while IFS= read -r line; do
    python3 draw.py $line
done < uid.txt
