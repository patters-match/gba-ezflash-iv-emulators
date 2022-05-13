#!/bin/bash

cat YieAr.gba header.dat i08.10d i07.8d g16_1.bin g15_2.bin g04_5.bin g03_6.bin g06_3.bin g05_4.bin yiear.clr a12_9.bin header2.dat d12_8.bin d14_7.bin g16_1.bin g15_2.bin g04_5.bin g03_6.bin g06_3.bin g05_4.bin yiear.clr a12_9.bin > YieArDouble.gba
cp ../ez4/blank.sav ./YieArDouble.sav
cp ../ez4/emupatch.pat ./YieArDouble.pat