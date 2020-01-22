#!/bin/bash
#########################################################
#														#
#						SmartWIFI						#
#					Project team BCDS					#
#														#
#########################################################
# date: 12/17/19
# autor: Team BCDS
# contact: raphael.barrasset@gmail.com; julien.castelain@outlook.fr; g.ducroux@outlook.fr; saint-amand.matthieu@orange.fr;

echo "#######################################
#                                     #
#		SmartWIFI             #
#	   Cisco control tower        #
#                                     #
#######################################

"
run=1
choice=-1
echo "Welcome in control tower
Here you can manage your cisco switch"
echo "------------------------------------------------"

while (($run)) 
do
	echo " 
(1) Show conf
(2) Show interface status
(3) Enable poe port
(4) Disable poe port
(0) Quit"
	read
	case $REPLY in
		1) echo "expect show_conf"
				 expect show_conf
			;;
		2) echo "expect show_interface_status"
				 expect show_interface_status
			;;
		3) echo " 
Which port would you enable (between 1 and 12) ?
(0) Will enable every ports"
		   read
		   if [[ "$REPLY" -ge "1" && "$REPLY" -le "12" ]]; then
		       echo "expect enable_poe_port $REPLY"
			   expect enable_poe_port $REPLY
		   elif [[ "$REPLY" -eq "0" ]]; then
		       echo "expect enable_poe_port"
			   expect enable_poe_port
		   else
		       echo "Wrong entry..."
		   fi
			;;
		4) echo "
Which port would you disable (between 1 and 12) ?
(0) Will disable every ports"
		   read
		   if [[ "$REPLY" -ge "1" && "$REPLY" -le "12" ]]; then
		       echo "expect disable_poe_port $REPLY"
			   expect disable_poe_port $REPLY
		   elif [[ "$REPLY" -eq "0" ]]; then
		       echo "expect disable_poe_port"
		       expect disable_poe_port
		   else
			   echo "Wrong entry..."
		   fi
			;;
		0) echo "Quitting..."
			run=0
			;;
		*) echo "Wrong entry..."
	esac
done
