my_minipack is a Python package that provides two modules to help you with your projects: progress and logger.

The progress module provides a simple progress bar that you can use to track the progress of a loop in your program.
Here's an example of how to use it:

from my_minipack.progress import ft_progress

my_list = range(100)

for item in ft_progress(my_list): 
    # do something with item 
    pass 
The ft_progress function takes an iterable as an argument and returns a generator that you can use to iterate over
the items in the iterable. As you iterate over the items, the progress bar will be displayed in the console.

The logger module provides a simple logging utility that you can use to write messages to a file. Here's an example
of how to use it:

from my_minipack.logger import Logger

log_file = 'my_log.txt' 
logger = Logger(log_file)

logger.info('Starting my program')
# do something

logger.info('Something happened')
# do more things

logger.info('Program complete') 
The Logger class takes the name of a file as an argument and provides several methods for writing different types
of messages to the file, including debug, info, warning, error, and critical.