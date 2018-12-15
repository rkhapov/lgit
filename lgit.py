import sys


def main(argv):
    if len(argv) < 2:
        print('Invalid parameters')
        return

    name = argv[1]
    args = argv[2:]


if __name__ == '__main__':
    main(sys.argv)
