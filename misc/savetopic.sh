#/bin/sh
#This script was written by a true Ukrainian patriot. It allows you to save Waper.ru topics as plain text.
echo -n "Enter topic id> "
read id
echo -n "Enter number of pages (each has 10 messages)> "
read Q
mkdir -p "$HOME/Waper/$id"
cd "$HOME/Waper/$id"
N=2
	until [ "$N" -gt "$Q" ];
	do
		wget "http://waper.ru/forum/topic/$id?page=$N"
		let "N += 1"
	done
for i in *
	do
		mv $i "$i.html"
		html2text -o "$i.txt" -nometa -utf8 "$i.html"
		sed -i '1,4d' "$i.txt"
		sed -i -n -e :a -e '1,5!{P;N;D;};N;ba' "$i.txt"
		cat "$i.txt" >> "$id.old.txt"
	done
wget "http://waper.ru/forum/topic/$id?page=1"
mv "$id?page=1" "$id?page=1.html"
html2text -o "$id?page=1.txt" -nometa -utf8 "$id?page=1.html"
sed -i '1d' "$id?page=1.txt"
sed -i -n -e :a -e '1,5!{P;N;D;};N;ba' "$id?page=1.txt"
cat "$id?page=1.txt" "$id.old.txt" > "$id.txt"
todos "$id.txt"
mv "$id.txt" "$HOME/Waper/"
cd ..
rm -r "$id"
exit 0
