def main(argv):
    print 'args:', argv
    try:
        while 1:
            data = raw_input()
            print data
    except EOFError:
        pass

if __name__ == '__main__':
    import sys
    main(sys.argv)
