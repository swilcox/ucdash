#!/usr/bin/python
import sys
import os
import getopt
import subprocess
import shlex
try:
    import simplejson as json
except:
    import json
from datetime import datetime
import httplib
from ConfigParser import ConfigParser

VERSION = "0.5"

class UCTask(object):
    def __init__(self,command,jobname,*args,**kwargs):
        self.starttime = datetime.now()
        self.command = command
        self.jobname = jobname
        self.config = None
        self.results = None
        self.extra = None  
        self.shell = True      
        if 'config' in kwargs:
            self.config = kwargs['config']
        if 'verbose' in kwargs and kwargs['verbose'] == True:
            self.verbose = True
        else:
            self.verbose = False
        if 'extra' in kwargs and kwargs['extra']:
            self.extra = kwargs['extra']
        if 'shell' in kwargs:
            self.shell = kwargs['shell']
        self._load_config()

    def execute(self):
        if self.shell:
            self.p = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        else:
            self.p = subprocess.Popen(shlex.split(command))        
        (out, err) = self.p.communicate()
        self.endtime = datetime.now()
        duration_timedelta = self.endtime - self.starttime
        duration_ms = (duration_timedelta.microseconds / 1000) + (duration_timedelta.seconds * 1000)
        self.results = {'jobname':self.jobname,'result': self.p.returncode, 'log': out, 'duration': duration_ms}
        if self.extra:
            self.results['extra'] = self.extra
        if self.verbose:
            print "job name: " + self.jobname
            print "return code: " + str(self.p.returncode)
            print "output: " + str(out)
            print "extra: " + str(self.extra)
            print "errout: " + str(err)
            print "json: " + str(self.results)
            
    def _load_config(self):
        self.host = 'localhost'
        self.url = '/api/notify/%s/' % self.jobname
        self.port = 8000
        self.http_method = 'POST'        
        if self.config is None or self.config=='':
            if os.name.lower() == 'posix':
                self.config = os.path.join(os.environ['HOME'],'.ucdc','ucdc.config')
            else:
                self.config = os.path.join(os.environ['USERPROFILE'],'ucdc.ini')
        if os.path.exists(self.config):
            config = ConfigParser()
            config.read(self.config)
            if config.has_option('server','host'):
                self.host = config.get('server','host')
            if config.has_option('server','port'):
                self.port = config.get('server','port')
            if config.has_option('server','url'):
                self.url = config.get('server','url')
        else:
            #BAD!!!!
            #todo: raise and exception back up the line...
            print "config file ERROR"
            #EVIL!!!!
        
    def report(self):
        if self.verbose:
            print "server host: " + self.host
            print "server port: " + str(self.port)
            print "server api url: " + str(self.url)
        conn = httplib.HTTPConnection(self.host,port=self.port)
        conn.request(self.http_method,self.url,body=json.dumps(self.results),headers={'Content-Type':'application/json'})
        response = conn.getresponse()
        if self.verbose:
            print "server response: " + str(response.read())


def usage():
    print 'usage: [--version] [-v] [--config=config-file-name] --execute="command-to-execute" jobslug'
    print ' -v verbose'
    print ' --version displays version number of this client and exits'
    print ' --execute= must be specified to run a command. The command should be enclosed in quotes'
    print ' --config= allows for specifying a specific configuration file. If not specified, looks for $HOME/.ucdc/ucdc.config and then /etc/ucdc/ucdc.config'
    print ''' --extra= allows for extra data to be specified and sent via json-style notation like '{"field1":"value","field2":"value2"}' '''
    

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:ve:", ["help", "config=", "verbose", "version", "execute=", "extra="])
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
    extra_data = None
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
        elif o in ("-x","--extra"):
            print "extra: " + a
            extra_string = a
            try:
                extra_data = json.loads(extra_string)
            except:
                extra_data = {'command-line-error':'error in extra part of command, not valid json'}
        else:
            assert False, "unhandled option"
            sys.exit(2)
    if len(exe):
        u = UCTask(exe,args[0],shell=True,verbose=verbose,config=config_file,extra=extra_data)
        u.execute()
        u.report()
        sys.exit()


if __name__ == "__main__":
    main()
