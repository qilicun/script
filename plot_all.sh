#!/bin/sh
    ./plot_fpr.py -f output_norne_simple_c5_morewells -e NORNE_SIMPLE_C5_MORE_PERFORATION -p output_norne_simple_c5_morewells/porevolume/000.txt
    ./plot_wct.py -f output_norne_simple_c5_morewells/NORNE_SIMPLE_C5_MOREWELLS -e NORNE_SIMPLE_C5_MORE_PERFORATION -v C-1H C-2H C-3H F-1H F-2H F-3H B-2H K-2H K-1H E-4AH E-1H E-2H E-3H
    ./plot_wbhp.py -f output_norne_simple_c5_morewells/NORNE_SIMPLE_C5_MOREWELLS -e NORNE_SIMPLE_C5_MORE_PERFORATION -v C-1H C-2H C-3H F-1H F-2H F-3H B-2H K-2H K-1H E-4AH E-1H E-2H E-3H
    ./cell_press.py -f output_norne_simple_c5_morewells -m 26 44 20 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./cell_press.py -f output_norne_simple_c5_morewells -m 12 85 20 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./cell_press.py -f output_norne_simple_c5_morewells -m 12 85 21 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./cell_press.py -f output_norne_simple_c5_morewells -m 12 85 22 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./cell_press.py -f output_norne_simple_c5_morewells -m 8 26 3 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./cell_press.py -f output_norne_simple_c5_morewells -m 17 31 9 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./cell_press.py -f output_norne_simple_c5_morewells -m 38 96 2 -e NORNE_SIMPLE_C5_MORE_PERFORATION
    ./plot_wellrates.py -f output_norne_simple_c5_morewells/NORNE_SIMPLE_C5_MOREWELLS -e NORNE_SIMPLE_C5_MORE_PERFORATION -v  WOIR:C-1H WWIR:C-1H WOIR:C-2H WWIR:C-2H WOIR:C-3H WWIR:C-3H WOIR:F-1H WWIR:F-1H WOIR:F-2H WWIR:F-2H WOIR:F-3H WWIR:F-3H WOPR:B-2H WWPR:B-2H WOPR:K-2H WWPR:K-2H WOPR:K-1H WWPR:K-1H WOPR:E-4AH WWPR:E-4AH WOPR:E-1H WWPR:E-1H WOPR:E-2H WWPR:E-2H WOPR:E-3H WWPR:E-3H
