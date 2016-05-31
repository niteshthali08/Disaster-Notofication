
debug = 1

def console_log( *args):
     if debug:
        for param in args:
            print param,
     print ''