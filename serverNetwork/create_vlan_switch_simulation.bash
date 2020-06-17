#!/bin/bash
 
echo "Simulated ssh connection to admin@192.168.1.1 succeed"
 
read $REPLY
sleep 3
echo "Configuring from terminal, memory, or network ? "
 
read $REPLY
sleep 3
echo ">(config)#"
 
read $REPLY
sleep 3
echo ">(config-vlan)#"
 
read $REPLY
sleep 3
echo ">(config-vlan)#"
 
read $REPLY
sleep 3
echo ">(config)#"
 
read $REPLY
sleep 3
echo ">(config-vlan)#"
 
read $REPLY
sleep 3
echo ">(config-vlan)#"
 
read $REPLY
sleep 3
echo ">#"

