echo " ------------------------------------------------------------------------"
echo "
    <Memory status>  Copyright (C) 2016> JJ Posti (techtimejourney.net)
    This program comes with ABSOLUTELY NO WARRANTY; for details see: 
    http://www.gnu.org/copyleft/gpl.html
    This is free software, and you are welcome to redistribute it
    under GPL Version 3, 29 June 2007."

echo " -------------------------------------------------------------------------"
echo "${txtylw}	Welcome to Memory status 0.1 ${txtrst}"
echo ".........................................................................."

echo ""

echo "First we are going to print some general system information." 
echo "Then comes the memory usage status."
echo "And finally, we are going to fetch information about the RAM memory type."
echo "The results will be shown 25 seconds when the program reaches its end."
sleep 5


echo "------------------------------------------"
echo "System information:"  
echo "------------------------------------------"

echo ""
uname -a && sleep 8
echo ""

echo "------------------------------------------"
echo "Memory usage:"  
echo "------------------------------------------"
echo ""
free -m && sleep 10
echo ""

echo "------------------------------------------"
echo "RAM memory type:" 
echo "------------------------------------------"
echo ""
sleep 4
sudo dmidecode -t 17
sleep 25
echo "Time to Exit"
sleep 4 
