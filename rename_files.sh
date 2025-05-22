#!/bin/bash

echo "Renaming files to sequential order..."

# Define the mapping of old names to new names
declare -A rename_map
rename_map["01-introduzione.tex"]="01-introduzione.tex"
rename_map["02-networking.tex"]="02-networking.tex"
rename_map["02-aritmetica-binaria.tex"]="03-aritmetica-binaria.tex"
rename_map["03-ip-subnetting.tex"]="04-ip-subnetting.tex"
rename_map["04-ipv4-vlsm.tex"]="05-ipv4-vlsm.tex"
rename_map["05-application-layer.tex"]="06-application-layer.tex"
rename_map["06-security.tex"]="07-security.tex"
rename_map["07-wireless-1.tex"]="08-wireless-1.tex"
rename_map["07-wireless-2.tex"]="09-wireless-2.tex"
rename_map["08-wireless-protocols.tex"]="10-wireless-protocols.tex"
rename_map["09-routing.tex"]="11-routing.tex"
rename_map["10-esercitazioni.tex"]="12-esercitazioni.tex"

# Also update the content files if they exist
declare -A content_rename_map
content_rename_map["01-introduzione-content.tex"]="01-introduzione-content.tex"
content_rename_map["02-networking-content.tex"]="02-networking-content.tex"
content_rename_map["02-aritmetica-binaria-content.tex"]="03-aritmetica-binaria-content.tex"
content_rename_map["03-ip-subnetting-content.tex"]="04-ip-subnetting-content.tex"
content_rename_map["04-ipv4-vlsm-content.tex"]="05-ipv4-vlsm-content.tex"
content_rename_map["05-application-layer-content.tex"]="06-application-layer-content.tex"
content_rename_map["06-security-content.tex"]="07-security-content.tex"
content_rename_map["07-wireless-1-content.tex"]="08-wireless-1-content.tex"
content_rename_map["07-wireless-2-content.tex"]="09-wireless-2-content.tex"
content_rename_map["08-wireless-protocols-content.tex"]="10-wireless-protocols-content.tex"
content_rename_map["09-routing-content.tex"]="11-routing-content.tex"
content_rename_map["10-esercitazioni-content.tex"]="12-esercitazioni-content.tex"

# Perform the renaming
for old_name in "${!rename_map[@]}"; do
  new_name="${rename_map[$old_name]}"
  if [ -f "$old_name" ]; then
    echo "Renaming: $old_name -> $new_name"
    mv "$old_name" "$new_name"
  else
    echo "File not found: $old_name (skipping)"
  fi
done

# Rename content files if they exist
for old_name in "${!content_rename_map[@]}"; do
  new_name="${content_rename_map[$old_name]}"
  if [ -f "$old_name" ]; then
    echo "Renaming content file: $old_name -> $new_name"
    mv "$old_name" "$new_name"
  fi
done

echo "Updating generate_notes.sh with new file names..."

# Update the FILES array in generate_notes.sh
sed -i '/^FILES=(/,/^)/ c\
FILES=(\
  "01-introduzione.tex"\
  "02-networking.tex"\
  "03-aritmetica-binaria.tex"\
  "04-ip-subnetting.tex"\
  "05-ipv4-vlsm.tex"\
  "06-application-layer.tex"\
  "07-security.tex"\
  "08-wireless-1.tex"\
  "09-wireless-2.tex"\
  "10-wireless-protocols.tex"\
  "11-routing.tex"\
  "12-esercitazioni.tex"\
)' generate_notes.sh

# Update input commands in appunti_completi.tex if the file exists
if [ -f "appunti_completi.tex" ]; then
  echo "Updating appunti_completi.tex with new file names..."

  # Update each \input line
  sed -i 's/\\input{02-aritmetica-binaria-content}/\\input{03-aritmetica-binaria-content}/g' appunti_completi.tex
  sed -i 's/\\input{03-ip-subnetting-content}/\\input{04-ip-subnetting-content}/g' appunti_completi.tex
  sed -i 's/\\input{04-ipv4-vlsm-content}/\\input{05-ipv4-vlsm-content}/g' appunti_completi.tex
  sed -i 's/\\input{05-application-layer-content}/\\input{06-application-layer-content}/g' appunti_completi.tex
  sed -i 's/\\input{06-security-content}/\\input{07-security-content}/g' appunti_completi.tex
  sed -i 's/\\input{07-wireless-1-content}/\\input{08-wireless-1-content}/g' appunti_completi.tex
  sed -i 's/\\input{07-wireless-2-content}/\\input{09-wireless-2-content}/g' appunti_completi.tex
  sed -i 's/\\input{08-wireless-protocols-content}/\\input{10-wireless-protocols-content}/g' appunti_completi.tex
  sed -i 's/\\input{09-routing-content}/\\input{11-routing-content}/g' appunti_completi.tex
  sed -i 's/\\input{10-esercitazioni-content}/\\input{12-esercitazioni-content}/g' appunti_completi.tex
fi

echo "Renaming completed successfully!"
