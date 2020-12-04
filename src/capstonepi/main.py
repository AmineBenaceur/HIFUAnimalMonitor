#!/usr/bin/env python3
"""
Usage: cappi <something> [--foo=<bar>]

Options: 
--foo=<bar>  my flag [default: bardefault]
"""

from docopt import *

idef main():
    args = docopt(__doc__)
    print(args)

if __name__ == '__main__':
    main()
