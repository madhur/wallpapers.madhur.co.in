#!/bin/sh

base_folder="./wallpapers"
vertical="vertical"
cd $base_folder || exit 1

hour=$(date +%H)
folder=''
if [ "$hour" -lt 05 ] # if hour is less than 05
then
folder="midnight"
elif [ "$hour" -lt 12 ] # if hour is less than  12
then
folder="morning"
elif [ "$hour" -lt 17 ] # if hour is less than  16
then
folder="day"
elif [ "$hour" -lt 20 ] # if hour is less then 20
then
folder="evening"
elif [ "$hour" -le 23 ] # if hour is less then and equal to 23
then
folder="night"
else
folder="night"
fi

filename=$(ls $base_folder/$folder | shuf -n 1)
vertical_filename=$(ls $base_folder/$vertical/$folder | shuf -n 1)
feh --bg-fill  $base_folder/$folder/$filename $base_folder/$vertical/$folder/$vertical_filename


