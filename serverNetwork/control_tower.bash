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
(3) Show mac address
(4) Show vlan conf
(5) Enable poe port
(6) Disable poe port
(7) Add vlan
(8) Delete vlan

(0) Quit"
	read
	case $REPLY in
		1) echo "expect show_conf"
				 expect show_conf
			;;
		2) echo "expect show_interface_status"
				 expect show_interface_status
			;;
		3) echo "expect show_mac_address"
				 expect show_mac_address
			;;
		4) echo "expect show_vlan"
				 expect show_vlan
			;;
		5) echo " 
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
		6) echo "
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
		7) echo "Which vlan number would you assign to connected area ?"
		   read
		   connected_area=$REPLY
		   echo "Which vlan number would you assign to disconnected area ?" 
		   read
		   disconnected_area=$REPLY
           if [[ "$connected_area" -gt "1" && "$disconnected_area" -gt "1" ]]; then
		       echo "expect create_vlan"
			   expect create_vlan $connected_area $disconnected_area
		   else
		       echo "Wrong entry..."
		   fi
			;;
		8) 	echo "Which port would you delete ?"
			read
			expect delete_vlan $REPLY
			;;
		0) echo "Quitting..."
			run=0
			;;
		*) echo "Wrong entry..."
	esac
done
