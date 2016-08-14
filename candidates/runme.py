#!/usr/bin/python
import os
import sys


semesters = ["14fa", "15sp", "15fa"]

def main():
    outdir = "results"
    try:
        os.makedirs(outdir)
    except OSError:
        if not os.path.exists(outdir):
            print("check result directory")
            sys.exit(1)

    c = 6

    lastnamefile_option = ""
    for sem in semesters:
        filename = "data/{}_deans.tsv".format(sem)
        print("going through {} dean\'s list ...".format(sem))
        command = "python3 find_koreans.py -i {} {} -o {} -c {}".format(filename, lastnamefile_option, outdir, c)
        os.system(command)
        print("  done")
        lastnamefile_option = "-l {}/results-{}_deans/lastnames.txt".format(outdir, sem)

if __name__ == "__main__":
    main()

