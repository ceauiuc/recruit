#!/usr/bin/python
import sys
import os
from optparse import OptionParser
from collections import defaultdict

column = {"state": 0, "city": 1, "zipcode": 2,
          "lastname": 3, "firstname": 4, "midname": 5,
          "class": 6, "college": 7, "major": 8}


def write_to_file(data, filename):
    with open(filename, 'w') as f:
        for line in data:
            line = "\t".join(line)
            f.write("{}\n".format(line))


def init_students(infile):
    students = []
    with open(infile, 'r') as f:
        for line in f:
            line = line.strip().lower().split('\t')
            students.append(line)
    return students


def check_dir(dirname, dir_type):
    try:
        os.makedirs(dirname)
    except OSError:
        if not os.path.exists(dirname):
            print("check {} directory".format(dir_type))
            sys.exit(1)


def find_koreans(students, outdir):
    last_names = []
    others = []
    filename = "{}/koreans.tsv".format(outdir)
    f_korean = open(filename, 'w')

    for s in students:
        if "korea" in s[column["state"]]:
            last_name = s[column["lastname"]]
            last_names.append(last_name)
            line = "\t".join(s)
            f_korean.write("{}\n".format(line))
        else:
            others.append(s)
    f_korean.close()
    last_names = list(set(last_names))
    filename = "{}/lastnames.txt".format(outdir)
    with open(filename, 'w') as f:
        for name in last_names:
            f.write("{}\n".format(name))
    return others, last_names


def find_by_name(students, last_names, outdir):
    others = []
    filename = "{}/koreans_maybe.tsv".format(outdir)
    f = open(filename, 'w')

    for s in students:
        last_name = s[column["lastname"]]
        if last_name in last_names:
            line = "\t".join(s)
            f.write("{}\n".format(line))
        else:
            others.append(s)
    f.close()
    return others


def group_by_length(students):
    length_dict = defaultdict(list)
    for s in students:
        length = len(s[column["lastname"]])
        length_dict[length].append(s)
    for key, value in length_dict.items():
        length_dict[key] = sorted(value, key=lambda k: k[column["lastname"]])
    return dict(length_dict)


def main(infile, lastnamefile, outdir, c):
    # read student list
    students = init_students(infile)

    # generate output directory
    filename = infile.rsplit('/', 1)[-1]
    outdir = "{}/results-{}".format(outdir, filename.rsplit('.', 1)[0])
    check_dir(outdir, "output")

    # find koreans
    students, last_names = find_koreans(students, outdir)

    # append existing lastnames, if present
    if lastnamefile is not None and lastnamefile != "":
        with open(lastnamefile, 'r') as f:
            for line in f:
                last_name = line.strip()
                last_names.append(last_name)
        last_names = list(set(last_names))

    # find students with same last names
    students = find_by_name(students, last_names, outdir)

    # group by last name length
    length_dict = group_by_length(students)

    # students with last name length c or less
    filename = "{}/{}-or-less.tsv".format(outdir, c)
    outdir = "{}/group-by-length".format(outdir)
    check_dir(outdir, "group-by-length")
    with open(filename, 'w') as f:
        for key in length_dict.keys():
            value = length_dict[key]
            filename = "{}/lastname-{}.tsv".format(outdir, key)
            write_to_file(value, filename)
            if key <= c:
                for line in value:
                    line = "\t".join(line)
                    f.write("{}\n".format(line))


if __name__ == '__main__':
    # set options
    optparser = OptionParser()
    optparser.add_option('-i', '--infile',
                         dest='infile',
                         help='relative path to input file',
                         default=None)
    optparser.add_option('-l', '--lastnamefile',
                         dest='lastnamefile',
                         help='relative path to last name list',
                         default=None)
    optparser.add_option('-o', '--outdir',
                         dest='outdir',
                         help='relative path to output directory',
                         default=None)
    optparser.add_option('-c', '--c',
                         dest='c',
                         help='maximum length of last name to consider as korean',
                         default=6,
                         type='int')
    (options, args) = optparser.parse_args()

    # check input file path
    if options.infile is not None:
        if not os.path.isfile(options.infile):
            print("error: specified input file does not exist. relative path expected.")
            sys.exit(1)
    else:
        print("error: input file is not specified. use option -i or --infile.")
        sys.exit(1)

    # check lastname file path
    if options.lastnamefile is not None and options.lastnamefile != "":
        if not os.path.isfile(options.lastnamefile):
            print("error: specified lastname file does not exist. relative path expected.")
            sys.exit(1)

    # check maximum length of last name
    if options.c < 1:
        print("error: maximum lnegth of last name should be at least 1.")
        sys.exit(1)

    main(options.infile, options.lastnamefile, options.outdir, options.c)
