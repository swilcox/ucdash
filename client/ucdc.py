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
        if 'config' in kwargs:
            self.config = kwargs['config']
        if 'verbose' in kwargs and kwargs['verbose'] == True:
            self.verbose = True
        else:
            self.verbose = False
        if 'shell' in kwargs and kwargs['shell'] == True:
            self.p = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        else:
            self.p = subprocess.Popen(shlex.split(command))

    def execute(self):
        (out, err) = self.p.communicate()
        self.endtime = datetime.now()
        if self.verbose:
            print "job name: " + self.jobname
            print "return code: " + str(self.p.returncode)
            print "output: " + out
            print "errout: " + err
            print "json: " + json.dumps({'jobname':self.jobname,'returncode': self.p.returncode,
                                         'output':out, 'errout':err,
                                         'starttime':str(self.starttime), 'endtime':str(self.endtime)})

    def _load_config(self):
        if self.config is None:
            self.config = ''

    def report(self):
        self.report_url = 'http://localhost:8000/job/_%s_/post_result/' % self.jobname
        httplib.HTTPConnection


def usage():
    print "usage: ?"


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
