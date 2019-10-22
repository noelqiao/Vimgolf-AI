#! /usr/bin/python3
import tempfile, subprocess
import sys, os

print('Hello, World!')

EDITOR = os.environ.get('EDITOR', 'vim')

def main(start_file, end_file):
    # Try and run vim with subprocesses
    with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
        with open(start_file, 'r') as start:
            line = str.encode(start.readline())
            tmp.write(line)
        tmp.flush()
        subprocess.call([EDITOR, tmp.name])
      

if __name__ == '__main__':
    print(sys.argv[1])
    print(sys.argv[2])
    main(sys.argv[1], sys.argv[2])
