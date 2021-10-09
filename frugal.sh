#!/bin/bash
source /c/v2/frugal/Scripts/activate


if [ "${@: -1}" != "go" ]
then
    echo "gefetchen..."
    pushd /c/tmp
    python /c/py/frugal_ink/form_it.py $1
    popd
    echo "Hit any key except ^C to post"
    if ! $( read -t 30 )
    then
	echo "not posted"
	exit -1
    fi
fi
grep -i 'can.t find' /c/tmp/deal.txt 2>/dev/null 1>/dev/null
found=$?
echo found is $found
areyousure="SURE"
if [ $found -eq 0 ]
   then
   areyousure="NO"
   echo 'AUTHOR!?!?  type SURE if you want to post'
   if ! $( read areyousure )
      then echo "not posted cause authore"
      exit -1
   fi
fi
# https://unix.stackexchange.com/questions/13466/can-grep-output-only-specified-groupings-that-match
# \K is the lookbehind -- a literal dollar; 0+ digits a dot 2 digits an dclosing bracket
# which matches e.g ($4.99
price=$(grep -oP '\$\K[0-9]*\.[0-9][0-9](?=\))' /c/tmp/deal.txt)
tooExpensive=`echo "$price > 5" | bc -l`
if [ $tooExpensive = 1 ]
    then
	areyousure="NO"
	echo EXPENSIVE TYPE SURE IF YOU ARE SHOUR
	read areyousure
    if [ $areyousure != "SURE" ]
	then
	echo "not posted cause price "
	exit -1
    fi
fi
     

if [ "$areyousure" = "SURE" ]
      then  python /c/py/frugal_ink/post_it.py $*
else
   echo no post
fi


