import sys, os


class args:
    program = sys.argv[0]
    logfile = '/var/log/irondome/irondome.log'
    basepath = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    init_integrity = False

    watchpath = None
    extensions = []
    maxmemory = 100

    events = [
        'modify',
        'attrib',
        'create',
        'delete',
        'delete self',
        'move from',
        'move to'
    ]

def parse_arguments():
    options = [ '-event', '-logfile', '-init-integrity', '-help' ]
    options = sys.argv[1:]
    logger = Logger()
    events = []
    if len(options) <= 0:
        logger.halt_with_doc('', __doc__.format(program=args.program,logfile=args.logfile))
    
    while len(options) > 0:
        data = options.pop(0)
        if data in ['-events','-logfile']:
            value = options.pop(0)
            if data == '-events': events = value.split(',')
            if data == '-logfile': args.logfile = value
        
        elif data == '-init-integrity':
            args.init_integrity = True
        elif data == '-help':
            logger.halt_with_doc('', __doc__.format(program=args.program,logfile=args.logfile))
        
        else:
            if data:
                args.watchpath = [os.path.abspath(x.rstrip()) for x in data.split(',')]
            if len(options) > 0:
                args.extensions = [ x for x in options ]
                options.clear()
            
    if not args.watchpath:
        logger.halt('ERROR: set directory to monitoring')
    
    if len(args.watchpath) > 0:
        for path in args.watchpath:
            if not os.path.exists(path):
                logger.log((-2, f'ERROR: {path} not found'))
    for event in events:
        if event not in args.events:
            logger.halt(f'ERROR: {event} not recognized')
    #endfor

        if len(events) > 0:
            args.events = events
#parse_arguments

def main():
    parse_arguments()
    logger = Logger()
    logger.debug(f'args {args.__dict__}')