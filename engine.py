#!/usr/bin/python

import os
import argparse
import client
import sys
import json

def compose_job(controller_json, walltime, queue, auth):
    
    if queue not in ["Test", "Prod"] :
        print "ERROR: Queue is invalid"
        exit(-1)

    job_desc = { "username"           : "aswathy1993@gmail.com",
                 "executable"         : "/bin/bash myscript.sh",
                 "script_name"        : "myscript.sh",
                 "script"             : '''#!/bin/bash
pip install ipyparallel
cat > ipcontroller-engine.json <<END
{0}
END
ipengine --file=ipcontroller-engine.json &
pid=$!
sleep 50
kill -9 $pid
'''.format(open(controller_json, 'r').read()),
                 "jobtype"            : "script",
                 "output_file_stdout" : "STDOUT.txt",
                 "output_file_stderr" : "STDERR.txt",
                 "outputs"            : "",
                 "walltime"           : walltime,
                 "queue"              : queue
    }

    #print json.dumps(job_desc)
    with open('engine_job.json', 'w') as f:
        json.dump(job_desc, f)
    
    client.submit_task("engine_job.json", auth)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start ipcontroller for parallel processing with jupyter')
    parser.add_argument("engine_json", help="Path to ipcontroller-engine.json")
    parser.add_argument("walltime", help="Number of minutes the engine has to run", type=int)
    parser.add_argument("queue", help="Name of queue")
    parser.add_argument("auth", help="Authorization file")

    #parser.add_argument("-a", "--authfile", help="File with auth info")
    args = parser.parse_args()
    #start()
    compose_job(args.engine_json,args.walltime,args.queue, args.auth)
    exit(0)
    

