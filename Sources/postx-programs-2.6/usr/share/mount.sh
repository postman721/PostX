echo " ------------------------------------------------------------------------"
echo "
    <Simple mount>  Copyright (C) 2015> JJ Posti (techtimejourney.net)
    This program comes with ABSOLUTELY NO WARRANTY; for details see: 
    http://www.gnu.org/copyleft/gpl.html
    This is free software, and you are welcome to redistribute it
    under GPL Version 3, 29 June 2007."

echo " -------------------------------------------------------------------------"
echo "${txtylw}	Welcome to Simple mount. ${txtrst}"
echo ".........................................................................."

# Declare variable choice and assign value 4
choice=4
# Print to stdout

# Declare variable choice and assign value 4
choice=4
# Print to stdout
echo "${txtgrn}1. Mount usb devices"

	echo "${txtgrn}2. Unmount usb devices ${txtrst}"


	echo "${txtgrn}3. Exit immediatelly ${txtrst}"

echo ".........................................................................."

echo "Enter selection: "
# Loop while the variable choice is equal 4
# sh while loop
while [ $choice -eq 4 ]; do
# read user input
read choice
# sh nested if/else
if [ $choice -eq 1 ] ; then
 
while true
do
echo -n "Please confirm (y or n) :"
read CONFIRM
case $CONFIRM in
y|Y|YES|yes|Yes) break ;;
n|N|no|NO|No)
echo Exiting - you entered $CONFIRM
sleep 3
sh /usr/share/mount.sh
;;
*) echo Please enter only y or n
esac
done
echo You entered $CONFIRM. Continuing

#Mount usb devices

#Create directory 

echo "Enter name of the usb mount directory to be created: \c"

read DIR

echo "Locating the usb device."
sleep 2
lsblk
echo "What is the device you want to mount (usually sdb1, sdc1 or sdd1): \c"
read DEV

echo "Mounting the device"
sleep 2

mkdir -p /home/$USER/$DIR && sudo mount /dev/$DEV  /home/$USER/$DIR 

echo "All done. Your device is located within /home/$USER/$DIR" 

sh /usr/share/mount.sh


else

	if [ $choice -eq 2 ] ; then

while true
do
echo -n "Please confirm (y or n) :"
read CONFIRM
case $CONFIRM in
y|Y|YES|yes|Yes) break ;;
n|N|no|NO|No)
echo Exiting - you entered $CONFIRM
sleep 3
sh /usr/share/mount.sh

;;
*) echo Please enter only y or n
esac
done
echo You entered $CONFIRM. Continuing ..

echo "Enter name of the usb directory to be unmounted:  \c"

read UDIR

sudo umount /home/$USER/$UDIR 
sleep 2
echo "Device unmounted from /home/$USER/$UDIR"

sh /usr/share/mount.sh

else
		if [ $choice -eq 3 ] ; then	
echo  Exiting ... 
exit


                        choice=4
                fi   
        fi
fi
done
exit
