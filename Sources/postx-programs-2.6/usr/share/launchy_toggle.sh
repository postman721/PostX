#!/bin/bash

TOGGLE=$HOME/.toggle_launchy

if [ ! -e $TOGGLE ]; then
    touch $TOGGLE
    pkill -f /usr/share/clocktime & 
    pkill tint2 &
	    
else
    rm $TOGGLE
	/usr/share/clocktime &
    tint2 &	
fi
