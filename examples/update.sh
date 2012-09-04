#!/bin/sh

EXAMPLES=`dirname $0`
NWDIAG=$EXAMPLES/../bin/nwdiag
PACKETDIAG=$EXAMPLES/../bin/packetdiag

for diag in `ls $EXAMPLES/nwdiag/*.diag`
do
    png=$EXAMPLES/nwdiag/`basename $diag .diag`.png
    echo $NWDIAG -Tpng -o $png $diag
    $NWDIAG -Tpng -o $png $diag

    svg=$EXAMPLES/nwdiag/`basename $diag .diag`.svg
    echo $NWDIAG -Tsvg -o $svg $diag
    $NWDIAG -Tsvg -o $svg $diag
done

for diag in `ls $EXAMPLES/packetdiag/*.diag`
do
    png=$EXAMPLES/packetdiag/`basename $diag .diag`.png
    echo $PACKETDIAG -Tpng -o $png $diag
    $PACKETDIAG -Tpng -o $png $diag

    svg=$EXAMPLES/packetdiag/`basename $diag .diag`.svg
    echo $PACKETDIAG -Tsvg -o $svg $diag
    $PACKETDIAG -Tsvg -o $svg $diag
done
