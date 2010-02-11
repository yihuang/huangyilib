import sys
def main(argv):
    print 'args:', argv
    return
    try:
        #while 1:
        data = sys.stdin.readline()
        print data
    except EOFError:
        pass

if __name__ == '__main__':
    main(sys.argv)
