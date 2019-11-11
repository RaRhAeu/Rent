import sys
import math
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt


def shannon(data):
    """Returns shannon entropy of given iterable 'data'"""
    entropy = 0
    if data:
        length = len(data)
        d = defaultdict(int)
        for byte in data:
            d[byte] += 1
        for x in range(0, 256):
            p_x = d[x]/length
            if p_x > 0:
                entropy -= p_x * math.log(p_x, 2)
    return entropy/8


def read_file(fname):
    """Wrapper for reading data from the file"""
    try:
        with open(fname, 'rb') as f:
            data = list(f.read())
        return data
    except FileNotFoundError:
        print(f"File '{fname}' not found!")
        sys.exit(1)


def split_data(data, chksz):
    """Generator for splitting data into chunks"""
    for i in range(0, len(data), chksz):
        yield data[i:i+chksz]


def draw_plot(data, chksz, out_file):
    """Actual plotting function"""
    y = [shannon(val) for val in split_data(data, chksz)]
    x = [i*chksz for i in range(len(y))]
    plt.ylim(-0.1, 1.2)
    plt.ylabel("Entropy", fontsize=14)
    plt.xlabel("Offset", fontsize=14)
    plt.plot(x, y, color='black')
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()


def main():
    desc = "Tiny program that plots shannon entropy of a given file"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--in', help="Input file to process",
                        dest="i_file", required=True, type=str)
    parser.add_argument('--out', help="Output file to save results",
                        dest="o_file", required=False, default=None, type=str)
    parser.add_argument('--chk', help="Chunk size", default=256,
                        dest="chksz", required=False, type=int)
    args = parser.parse_args()
    in_file = args.i_file
    out_file = args.o_file
    chksz = args.chksz
    data = read_file(in_file)
    draw_plot(data, chksz, out_file)


if __name__ == '__main__':
    sys.exit(main())
