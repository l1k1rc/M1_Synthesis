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
    echo "  ${BOLD}--enable-poe-port${END}                      TODO "
    echo "  ${BOLD}--disable-poe-port${END}                     TODO "
    echo "  ${BOLD}--add-vlan${END}                             TODO "
    echo "  ${BOLD}--delete-vlan${END}                          TODO "
    echo
}

##################################################
#     CHECKING PARAMETERS                        #
##################################################
getopt_results=$(${GETOPT} -s bash -o h,i --long help,interactive-mode,show-conf,show-interface-status,show-mac-address,show-vlan-conf,enable-poe-port:,disable-poe-port:,add-vlan:,delete-vlan: -- "$@" 2>/dev/null)

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

OPTION=0
PORT=0
VLAN=0

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
            VLAN="$(echo -n ${2})"
	    	let "OPTION++"
	    	shift 2
	    	;;
        --delete-vlan)
			DELETEVLAN=1
            VLAN="$(echo -n ${2})"
	    	let "OPTION++"
	    	shift 2
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
			   	echo "expect enable_poe_port $PORT"
				expect enable_poe_port $PORT
			elif [[ "$PORT" -eq "0" ]]; then
				echo "expect enable_poe_port"
				expect enable_poe_port
			else
				echo "Wrong entry..."
			fi
	    	;;
        $DISABLEPOEPORT)
            if [[ "$PORT" -ge "1" && "$PORT" -le "12" ]]; then
			   	echo "expect disable_poe_port $PORT"
			   	expect disable_poe_port $PORT
			elif [[ "$PORT" -eq "0" ]]; then
				echo "expect disable_poe_port"
				expect disable_poe_port
			else
				echo "Wrong entry..."
			fi
	    	;;
        $ADDVLAN)
            echo "TODO"
	    	;;
        DELETEVLAN)
            echo "TODO"
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
			0) echo "Exit..."
				run=0
				;;
			*) echo "Wrong entry..."
		esac
	done
fi

