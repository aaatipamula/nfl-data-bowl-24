#/bin/sh

if [ -z $1 ]
then
    echo "please enter a filepath"
    exit 1
fi

filename=$1

if ! [ -f $filename ]
then
    echo "please enter a valid filepath to plays.csv"
    exit 1
fi

if [ -f "remove.txt" ]
then
    echo "backing up existing remove.txt"
    mv "remove.txt" ".~remove.txt"
fi

grep \
    -e " [1-5] yard" \
    -e "scramble" \
    -e "PENALTY" \
    -e "no gain" \
    -e "Horse" \
    $filename \
    | grep -Eo [0-9]{10},[0-9]+ > remove.txt
