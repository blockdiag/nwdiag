#!/bin/sh

EXAMPLES=`dirname $0`
NWDIAG=$EXAMPLES/../bin/nwdiag

for diag in `ls $EXAMPLES/nwdiag/*.diag`
do
    png=$EXAMPLES/nwdiag/`basename $diag .diag`.png
    echo $NWDIAG -Tpng -o $png $diag
    $NWDIAG -Tpng -o $png $diag

    svg=$EXAMPLES/nwdiag/`basename $diag .diag`.svg
    echo $NWDIAG -Tsvg -o $svg $diag
    $NWDIAG -Tsvg -o $svg $diag
done
