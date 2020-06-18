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

##################################################
#     ERRORLEVELS (^2 = sum() compliant)         #
##################################################

   ERR_HOSTFILE_NOT_FOUND=1
  ERR_PARAMETERS_CONFLICT=2
ERR_UNPARSEABLE_PARAMETER=4
  ERR_UNRECOGNIZED_OPTION=8

##################################################
#     REQUIRED RUNTIMES                          #
##################################################

GETOPT="$(which getopt)"

##################################################
#     WHEN ERROR OCCURS                          #
##################################################

catch()
{
    usage
    echo "Exit with error #${2} [${BOLD}${1}${END}]"
    echo
    exit ${2}
}

##################################################
#       DISPLAY USAGE OF THIS SCRIPT             #
##################################################

usage()
{
    echo 
    echo "This script allow to control a CISCO switch"
    echo "You can execute it in command line mode or interactive mode"
    echo
    echo "  ${BOLD}--help,-h${END}                              Display help and exit "
    echo "  ${BOLD}--interactive-mode,-i${END}                  Launch script in interactive mode "
	echo " "
    echo "  ${BOLD}--show-conf${END}                            Display configuration of CISCO switch "
    echo "  ${BOLD}--show-interface-status${END}                Display interface list with state (Enable/Disable) "
    echo "  ${BOLD}--show-mac-address${END}                     Display mac address of all devices connected "
    echo "  ${BOLD}--show-vlan-conf${END}                       Disaply the VLAN list "
    echo "  ${BOLD}--enable-poe-port${END}                      Enable a POE port or all POE ports"
    echo "  ${BOLD}--disable-poe-port${END}                     Disable a POE port or all POE ports "
    echo "  ${BOLD}--add-vlan${END}                             Create two vlans "
   #echo "  ${BOLD}--delete-vlan${END}                          Delete two vlans "
    echo
	echo "Examples :"
	echo
	echo "  ./main.bash --enable-poe-port 4 "
	echo "  ./main.bash --disable-poe-port 7 "
	echo "  ./main.bash --add-vlan 20,21 --names connected_vlan,disconnected_vlan "
	echo "  ./main.bash --add-vlan 20,21 -n connected_vlan,disconnected_vlan "
	echo
}

##################################################
#     CHECKING PARAMETERS                        #
##################################################
getopt_results=$(${GETOPT} -s bash -o h,i,n: --long help,interactive-mode,show-conf,show-interface-status,show-mac-address,show-vlan-conf,enable-poe-port:,disable-poe-port:,add-vlan:,delete-vlan:,names: -- "$@" 2>/dev/null)

if test $? != 0
then
	catch "Unrecognized parameter" ${ERR_UNRECOGNIZED_OPTION}
fi

INTERACTIVEMODE=0
SHOWCONF=0
SHOWINTERFACESTATUS=0
SHOWMACADDRESS=0
SHOWVLANCONF=0
ENABLEPOEPORT=0
DISABLEPOEPORT=0
ADDVLAN=0
DELETEVLAN=0
NAMES=0

OPTION=0
PORT=0
VLANS=0
NAMEVLANS=0

eval set -- "${getopt_results}"
while true
do
    case "${1}" in
        -h|--help)
            usage
            exit 0
            ;;
		-i|--interactive-mode)
            INTERACTIVEMODE=1
            shift 1
            ;;
        --show-conf)
            SHOWCONF=1
	    	shift 1
	    	;;
        --show-interface-status)
            SHOWINTERFACESTATUS=1
	    	shift 1
	    	;;
        --show-mac-address)
            SHOWMACADDRESS=1
	    	shift 1
	    	;;
        --show-vlan-conf)
            SHOWVLANCONF=1
	    	shift 1
	    	;;
        --enable-poe-port)
			ENABLEPOEPORT=1
            PORT="$(echo -n ${2})"
	    	let "OPTION++"
	    	shift 2
	    	;;
        --disable-poe-port)
			DISABLEPOEPORT=1
            PORT="$(echo -n ${2})"
	    	let "OPTION++"
	    	shift 2
	    	;;
        --add-vlan)
			ADDVLAN=1
            VLANS="$(echo -n ${2})"
	    	let "OPTION++"
	    	shift 2
	    	;;
        --delete-vlan)
			DELETEVLAN=1
            VLAN="$(echo -n ${2})"
	    	let "OPTION++"
	    	shift 2
	    	;;
		-n|--names)
			if [[ "$ADDVLAN" -eq "1" ]]; then
				NAMES=1
            	NAMEVLANS="$(echo -n ${2})"
	    		let "OPTION++"
	    		shift 2
			else
				catch "Unrecognized parameter" ${ERR_UNRECOGNIZED_OPTION}
			fi
	    	;;
        --)
            shift
	    	break
            ;;
        *) 
            catch "Unparseable option" ${ERR_UNPARSEABLE_PARAMETER}
            ;;
    esac
done

##################################################
#     			SPAWN ACTION                     #
##################################################

if [[ $INTERACTIVEMODE -eq 0 ]]; then
	case "1" in
        $SHOWCONF)
            echo "expect show_conf"
		    expect show_conf
            ;;
		$SHOWINTERFACESTATUS)
			echo "expect show_interface_status"
			expect show_interface_status
            ;;
        $SHOWMACADDRESS)
			echo "expect show_mac_address"
			expect show_mac_address
	    	;;
        $SHOWVLANCONF)
			echo "expect show_vlan"
			expect show_vlan
	    	;;
        $ENABLEPOEPORT)
            if [[ "$PORT" -ge "1" && "$PORT" -le "12" ]]; then
			   	#echo "expect enable_poe_port $PORT"
				#expect enable_poe_port $PORT
			   	echo "expect enable_poe_port_switch_simulation.expect $PORT"
				expect enable_poe_port_switch_simulation.expect $PORT
			elif [[ "$PORT" -eq "0" ]]; then
				echo "expect enable_poe_port"
				expect enable_poe_port
			else
				echo "Wrong entry..."
			fi
	    	;;
        $DISABLEPOEPORT)
            if [[ "$PORT" -ge "1" && "$PORT" -le "12" ]]; then
			   	#echo "expect disable_poe_port $PORT"
			   	#expect disable_poe_port $PORT
			   	echo "expect disable_poe_port_switch_simulation.expect $PORT"
				expect disable_poe_port_switch_simulation.expect $PORT
			elif [[ "$PORT" -eq "0" ]]; then
				echo "expect disable_poe_port"
				expect disable_poe_port
			else
				echo "Wrong entry..."
			fi
	    	;;
        $ADDVLAN)
			vlan1=$(echo $VLANS | awk 'BEGIN { FS = "," } ; { print $1 }')
			vlan2=$(echo $VLANS | awk 'BEGIN { FS = "," } ; { print $2 }')
			name1=$(echo $NAMEVLANS | awk 'BEGIN { FS = "," } ; { print $1 }')
			name2=$(echo $NAMEVLANS | awk 'BEGIN { FS = "," } ; { print $2 }')
            if [[ "$vlan1" -gt "99" || "$vlan1" -lt "1" || "$vlan2" -gt "99" || "$vlan2" -lt "1" || -z $name1 || -z $name2 ]]; then
				catch "Unparseable option" ${ERR_PARAMETERS_CONFLICT}
			else
				#echo "expect create_vlan $vlan1 $vlan2 $name1 $name2"
				#expect create_vlan $vlan1 $vlan2 $name1 $name2
				echo "expect create_vlan_switch_simulation.expect $vlan1 $vlan2 $name1 $name2"
				expect create_vlan_switch_simulation.expect $vlan1 $vlan2 $name1 $name2
			fi
	    	;;
        DELETEVLAN)
			vlan1=$(echo $VLANS | awk 'BEGIN { FS = "," } ; { print $1 }')
			vlan2=$(echo $VLANS | awk 'BEGIN { FS = "," } ; { print $2 }')
			name1=$(echo $NAMEVLANS | awk 'BEGIN { FS = "," } ; { print $1 }')
			name2=$(echo $NAMEVLANS | awk 'BEGIN { FS = "," } ; { print $2 }')
            if [[ "$vlan1" -gt "99" || "$vlan1" -lt "1" || "$vlan2" -gt "99" || "$vlan2" -lt "1" || -z $name1 || -z $name2 ]]; then
				catch "Unparseable option" ${ERR_PARAMETERS_CONFLICT}
			else
				echo "expect delete_vlan $vlan1 $vlan2 $name1 $name2"
				expect delete_vlan $vlan1 $vlan2 $name1 $name2
			fi
	    	;;
        *) 
            catch "Unparseable option" ${ERR_UNPARSEABLE_PARAMETER}
            ;;
    esac
else
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
				   #echo "expect enable_poe_port $REPLY"
				   #expect enable_poe_port $REPLY
				   echo "expect enable_poe_port_switch_simulation.expect $REPLY"
				   expect enable_poe_port_switch_simulation.expect $REPLY
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
				   #echo "expect disable_poe_port $REPLY"
				   #expect disable_poe_port $REPLY
				   echo "expect disable_poe_port_switch_simulation.expect $REPLY"
				   expect disable_poe_port_switch_simulation.expect $REPLY
			   elif [[ "$REPLY" -eq "0" ]]; then
				   echo "expect disable_poe_port"
				   expect disable_poe_port
			   else
				   echo "Wrong entry..."
			   fi
				;;
			7) echo "Which vlan number would you assign to the connected area ?"
			   read
			   connected_area=$REPLY
			   echo "Which name would you assign to the connected area ?"
			   read
			   connected_name=$REPLY
			   echo "Which vlan number would you assign to the disconnected area ?" 
			   read
			   disconnected_area=$REPLY
			   echo "Which name would you assign to the disconnected area ?"
			   read
			   disconnected_name=$REPLY
               if [[ "$connected_area" -gt "99" || "$connected_area" -lt "0" || "$disconnected_area" -gt "99" || "$disconnected_area" -lt "0" || -z $connected_name || -z $disconnected_name ]]; then
			       echo "Wrong entry..."
			   else
				   #echo "expect create_vlan $connected_area $disconnected_area $connected_name $disconnected_name"
				   #expect create_vlan $connected_area $disconnected_area $connected_name $disconnected_name
				   echo "expect create_vlan_switch_simulation.expect $connected_area $disconnected_area $connected_name $disconnected_name"
				   expect create_vlan_switch_simulation.expect $connected_area $disconnected_area $connected_name $disconnected_name
			   fi
				;;
			8) 	echo "Which port would you delete ?"
				read
				expect delete_vlan $REPLY
				;;
			0) echo "Exit..."
				run=0
				;;
			*) echo "Wrong entry..."
		esac
	done
fi

