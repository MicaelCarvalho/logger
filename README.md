<p align="center">
<b>
This is a free, lightweight, and flexible logger library
</b>
<br/><br/>
Feel free to use it in your projects and to send contributions
</p>

### Getting Started

1. Copy the file logger.py to your project folder
2. Import it inside your code with `from logger import Logger`
3. Instantiate the logger once with `logger = Logger('/path/to/your/log/folder')`

After instantiating it once, you can call it anywhere you want simply with `logger = Logger()`. The same folder as before is used. As of now there is no implemented way of changing the folder without quitting python, although that is simple to be done.

4. Enjoy all the logging capabilities of the library. Please check below for functions and a test code. :-)

### Testing the code

Run the following test to check if everything is working as expected:

```
from logger import Logger
logger = Logger('/tmp')

# This part tests the message types
logger.log_message('Test 1')
logger.log_message('Test 2', Logger.INFO)
logger.log_message('Test 3', Logger.SUMMARY)
logger.log_message('Test 4', Logger.WARNING)
# There should be an exception on the next line, because it is an error
logger.log_message('Test 5', Logger.ERROR)
logger.log_message('Test 6', Logger.SYSTEM)

# This part shows the usage of dictionary logging. This is useful for logging your performances/scores during the training of a neural network, for example
logger.log_dict('trn', {'a': 1, 'b': 2, 'c': 3})
logger.log_dict('trn', {'a': 2, 'b': 3, 'c': 4})
logger.log_dict('trn', {'a': 3, 'b': 4, 'c': 5})
# The next function writes the json file to the disk. Up to now everything is kept in memory
logger.flush()

# Let's just add another entry to "trn"
logger.log_dict('trn', {'a': 4, 'b': 5, 'c': 6})

# There should be an exception on the next line, because we are adding a new key "d" that did not exist before for the group "trn"
logger.log_dict('trn', {'a': 3, 'b': 4, 'c': 5, 'd': 5})

# There should be an exception on the next line, because we are not providing the key "c", required for the group "trn"
logger.log_dict('trn', {'a': 3, 'b': 4})

# No exceptions here, we are creating a new log group called "val" and adding some logs
logger.log_dict('val', {'d': 9, 'e': 8, 'f': 7})
logger.log_dict('val', {'d': 8, 'e': 7, 'f': 6})

# No exceptions here, just adding another entry to "trn" and writing the json file to the disk
logger.log_dict('trn', {'a': 5, 'b': 6, 'c': 7})
logger.flush()

# If you look at the json file now, you will see it is saved in a compact format. No useless spaces nor formatting, simply machine-readable json.
# Now we are going to change it and rewrite the json file in a human-readable format
logger.set_json_compact(False)
logger.flush()
```

### Functions available


#### logger = Logger([log_path])

Instantiates the logger class. It is implemented as a singleton, therefore you only need to pass `log_path` the first time you call it. Subsequent calls will return the same object, and the argument `log_path` becomes optional, and you can call `logger2 = Logger()` later to get the exact same object, which will continue to write on the same file as before.


#### logger.set_level(log_level)

Changes the minimal level for a message to be logged (both on screen and on the log file). Available values are:
1. Logger.INFO (default, everything is logged)
2. Logger.SUMMARY
3. Logger.WARNING
4. Logger.ERROR
5. Logger.SYSTEM

If the log level is set to WARNING, all further INFO and SUMMARY messages will be suppressed until the log level is lowered again.

#### logger.set_json_compact(is_compact)

By default, the JSON is saved in a compact mode. No useless spaces are added for visualization, and the minimum JSON standards are respected. This means the file is still readable by JSON libraries, but it is compact, so it will not be easily read by a human.

If you wish to have prettier, readable JSON files, you can call this function with `is_compact = False`. The file will be heavier, but it will surely be prettier as well, and you will be able to show it to all your friends. :-)


#### logger.log_message(message, [log_level, break_line, print_header])

Prints a message (string) on screen and on the log text file, if it's log level is bigger or equal to the defined view level (set with `logger.set_level(log_level)`).

`log_level` indicates the log level of the message. The same levels of `logger.set_level(log_level)` are accepted here.

`break_line` defines weather we should break the line after printing the message or not (defaults to True). If you need to print other things on the line later, set this to False.

`print_header` controls if the heading part of the log, where log level, timestamp and filename are displayed (defaults to True). If you are continuing a log with `break_line = False`, you probably want to set this to `False`, in order to keep things tidy.


#### logger.log_dict(group, dictionary, [description, should_print, log_level])

Stores a dictionary of values, to be logged later to a JSON file. Please note that the keys of the dictionary must be consistent inside each group.

`group` should be a string representing the name of the logging group (e.g. 'trn', 'val', or 'tst', for standard training, validating and test logs)

`dictionary` contains the dictionary to be logged. All values will be stacked into a list, stored under the key's name, and this will be saved later to a JSON file, should the programmer call the `flush` function.

`description` may contain a message that will not be logged inside the JSON, but printed on the screen if `should_print` is True.

`should_print` specifies wether we should print the pairs key-value of this dictionary as a message on the screen as well. This parameter defaults to False, and nothing is shown on the screen nor on the text log file (only on the JSON, after `flush` is called).

`log_level` defines the log level of the message that will be printed if `should_print` is set to `True`. Defaults to `SUMMARY`.


#### logger.log_dict_message(group, dictionary, [description, log_level])

Formats a dictionary and calls `log_message` in a structured way.

`group` should be a string representing the name of the logging group (e.g. 'trn', 'val', or 'tst', for standard training, validating and test logs)

`dictionary` contains the dictionary to be printed.

`description` may contain a message that will be printed on the screen.

`log_level` defines the log level of the message that will be printed. Defaults to `SUMMARY`.


#### logger.flush()

Writes the JSON file to the disk. The function `log_dict` stores the values in memory until flush is called. This way you can call `log_dict` frequently without having to worry about high I/O consumption, since the file will not be written unless you call `flush`.
