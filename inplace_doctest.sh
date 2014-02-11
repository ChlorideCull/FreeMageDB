#!/bin/sh
cd FreeMage
python3 -c "import doctest; doctest.testfile('doctest.txt')" > error.log
ERRORS=`cat error.log | wc -l`
if [ "0" = "${ERRORS}" ]; then
    echo "No errors when executing doctest. All good."
    rm error.log
else
    echo "Errors occured, output has been put into error.log!"
fi
