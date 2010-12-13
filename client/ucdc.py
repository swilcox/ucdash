import getopt, sys
import subprocess
import shlex
import simplejson as json
from datetime import datetime
import httplib

VERSION = "0.1"

class UCTask(object):
    def __init__(self,command,jobname,*args,**kwargs):
        self.starttime = datetime.now()
        self.command = command
        self.jobname = jobname
        self.config = None
        self.results = None
        if 'config' in kwargs:
            self.config = kwargs['config']
        if 'verbose' in kwargs and kwargs['verbose'] == True:
            self.verbose = True
        else:
            self.verbose = False
        if 'shell' in kwargs and kwargs['shell'] == True:
            self.p = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        else:
            self.p = subprocess.Popen(shlex.split(command))

    def execute(self):
        (out, err) = self.p.communicate()
        self.endtime = datetime.now()
        duration_timedelta = self.endtime - self.starttime
        duration_ms = (duration_timedelta.microseconds / 1000) + (duration_timedelta.seconds * 1000)
        self.results = {'jobname':self.jobname,'result': self.p.returncode, 'log': out, 'duration': duration_ms}
        self.results['extra'] = {'extra_value_1': 2, 'extra_value_2': 4}
        if self.verbose:
            print "job name: " + self.jobname
            print "return code: " + str(self.p.returncode)
            print "output: " + str(out)
            print "errout: " + str(err)
            print "json: " + str(self.results)

    def _load_config(self):
        if self.config is None or self.config=='':
            self.config = '.ucdc/ucdc.config'
            #self.config = '/etc/ucdc/ucdc.config'
        

    def report(self):
        conn = httplib.HTTPConnection("localhost",port=8000)
        conn.request("POST","/api/notify/%s/" % self.jobname,body=json.dumps(self.results),headers={'Content-Type':'application/json'})
        response = conn.getresponse()
        if self.verbose:
            print response.read()


def usage():
    print 'usage: [--version] [-v] [--config=config-file-name] --execute="command-to-execute" jobslug'
    print ' -v verbose'
    print ' --version displays version number of this client and exits'
    print ' --execute= must be specified to run a command. The command should be enclosed in quotes'
    print ' --config= allows for specifying a configuration file. If not specified, looks for $HOME/.ucdc/ucdc.config and then /etc/ucdc/ucdc.config'
    

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:ve:", ["help", "config=", "verbose", "version", "execute="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    config_file = None
    verbose = False
    if len(args) != 1:
        usage()
        sys.exit(2)
    exe = ''
    for o, a in opts:
        if o in ("-v","--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "--config"):
            config_file = a
        elif o in ("--version",):
            print "ucdc client version: %s" % VERSION
            sys.exit()
        elif o in ("-e","--execute"):
            print "execute: " + a
            exe = a
        else:
            assert False, "unhandled option"
            sys.exit(2)
    if len(exe):
        u = UCTask(exe,args[0],shell=True,verbose=verbose,config=config_file)
        u.execute()
        u.report()
        sys.exit()


if __name__ == "__main__":
    main()
