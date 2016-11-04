import sys, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', nargs='?')
parser.add_argument('nums', nargs='*')
args = parser.parse_args()

print args