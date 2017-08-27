#################################################################################
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#################################################################################

import os
import sys
import json
import inspect
import datetime
import collections

class Logger(object):
    INFO = 0
    SUMMARY = 1
    WARNING = 2
    ERROR = 3
    SYSTEM = 4
    __instance = None

    class Colors:
        END = '\033[0m'
        BOLD = '\033[1m'
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'
        GREY = '\033[90m'
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        PURPLE = '\033[95m'
        SKY = '\033[96m'
        WHITE = '\033[97m'

    indicator = {INFO: 'I', SUMMARY: 'S', WARNING: 'W', ERROR: 'E', SYSTEM: 'S'}
    colorcode = {INFO: Colors.GREY, SUMMARY: Colors.BLUE, WARNING: Colors.YELLOW, ERROR: Colors.RED, SYSTEM: Colors.WHITE}

    compactjson = True
    g_log_level = None
    g_logs_file = None
    g_json_path = None
    g_logs_path = None
    perf_memory = {}

    def __new__(self, log_path=None):
        if not Logger.__instance:
            if not log_path:
                print('Error: Please specify log_path for the first call.')
            else:
                Logger.__instance = object.__new__(Logger)
                try:
                    Logger.__instance.set_level(Logger.__instance.INFO)
                    Logger.__instance.g_logs_file = open(os.path.join(log_path, 'logs.txt'), 'a+')
                    Logger.__instance.g_json_path = os.path.join(log_path, 'logs.json')
                    Logger.__instance.g_logs_path = log_path
                    Logger.__instance.reload_json()
                except:
                    Logger.__instance = None
                    raise
        return Logger.__instance

    def __call__(self, *args, **kwargs):
        return self.log_message(*args, **kwargs, stack_displacement=2)

    def set_level(self, log_level):
        self.g_log_level = log_level

    def set_json_compact(self, is_compact):
        self.compactjson = is_compact

    def log_message(self, message, log_level=INFO, break_line=True, print_header=True, stack_displacement=1):
        if log_level < self.g_log_level:
            return -1
        if not self.g_logs_file:
            raise Exception('Critical: Log file not defined. Do you have write permissions for {}?'.format(self.g_logs_path))
        
        caller_info = inspect.getframeinfo(inspect.stack()[stack_displacement][0])

        if print_header:
            message_header = '[{} {:%Y-%m-%d %H:%M:%S}]'.format(self.indicator[log_level],
                                                                datetime.datetime.now())
            filename = caller_info.filename
            if len(filename) > 25:
                filename = '...{}'.format(filename[-22:])

            message_locate = '{}.{}:'.format(filename, caller_info.lineno)
            message_logger = '{} {} {}'.format(message_header, message_locate, message)
            message_screen = '{}{}{}{} {} {}'.format(self.Colors.BOLD,
                                                     self.colorcode[log_level],
                                                     message_header,
                                                     self.Colors.END,
                                                     message_locate,
                                                     message)
        else:
            message_logger = message
            message_screen = message

        if break_line:
            print(message_screen)
            self.g_logs_file.write('%s\n' % message_logger)
        else:
            print(message_screen, end='')
            sys.stdout.flush()
            self.g_logs_file.write(message_logger)
        
        self.g_logs_file.flush()
        if log_level==self.ERROR:
            raise Exception(message)

    def log_dict(self, group, dictionary, description='', should_print=False, log_level=SUMMARY):
        if group not in self.perf_memory:
            self.perf_memory[group] = {}
        else:
            for key in self.perf_memory[group].keys():
                if key not in dictionary.keys():
                    self.log_message('Key "{}" not in the dictionary to be logged'.format(key), log_level=self.ERROR)
            for key in dictionary.keys():
                if key not in self.perf_memory[group].keys():
                    self.log_message('Key "{}" is unknown. New keys are not allowed'.format(key), log_level=self.ERROR)

        for key in dictionary.keys():
            if key in self.perf_memory[group]:
                self.perf_memory[group][key].extend([dictionary[key]])
            else:
                self.perf_memory[group][key] = [dictionary[key]]

        if should_print:
            def print_subitem(prefix, subdictionary, stack_displacement=3):
                for key, value in subdictionary.items():
                    message = prefix + key + ':'
                    if not isinstance(value, collections.Mapping):
                        message += ' ' + str(value)
                    self.log_message(message, log_level, stack_displacement=stack_displacement)
                    if isinstance(value, collections.Mapping):
                        print_subitem(prefix + '  ', value, stack_displacement=stack_displacement+1)

            self.log_message('{}: {}'.format(group, description), log_level, stack_displacement=2)
            print_subitem('  ', dictionary, stack_displacement=3)

    def reload_json(self):
        if os.path.isfile(self.g_json_path):
            with open(self.g_json_path, 'r') as json_file:
                self.perf_memory = json.load(json_file)

    def flush(self):
        with open(self.g_json_path, 'w') as json_file:
            if self.compactjson:
                json.dump(self.perf_memory, json_file, separators=(',', ':'))
            else:
                json.dump(self.perf_memory, json_file, indent=4)
