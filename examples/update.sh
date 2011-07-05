#!/bin/sh

EXAMPLES=`dirname $0`
NWDIAG=$EXAMPLES/../bin/nwdiag

for diag in `ls $EXAMPLES/*.diag`
do
    png=$EXAMPLES/`basename $diag .diag`.png
    echo $NWDIAG -Tpng -o $png $diag
    $NWDIAG -Tpng -o $png $diag

    svg=$EXAMPLES/`basename $diag .diag`.svg
    echo $NWDIAG -Tsvg -o $svg $diag
    $NWDIAG -Tsvg -o $svg $diag
done
