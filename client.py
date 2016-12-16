#!/usr/bin/env python

import sys
import json
import time
import uuid
import argparse
import bottle
import os
import ast
from urlparse import urlparse
import requests
import urllib

SERVER_URL="http://ec2-52-2-217-165.compute-1.amazonaws.com:8888"
SUBMIT_URL=SERVER_URL+"/rest/v1/submit_task"
STATUS_URL=SERVER_URL+"/rest/v1/status_task"
CANCEL_URL=SERVER_URL+"/rest/v1/cancel_task"
LIST_URL  =SERVER_URL+"/rest/v1/list_tasks"

def debug_print(string):
    if GLOBAL_VERBOSE :
        print string

def download_file(URL, filename):
    urllib.urlretrieve(URL, filename)

def get_access_token(authfile):
    url  = open(authfile, 'r').read()
    url_parts = urlparse(url)
    parts = url_parts.query.split('&')
    auth  = {}
    for p in parts:
        args = p.split('=')
        auth[args[0]] = args[1]        
    return auth

def submit_task(task_desc_file, auth_file):

    auth = get_access_token(auth_file)

    with open(task_desc_file, 'r') as f:
        task_desc = f.read()
    data                 = ast.literal_eval(task_desc)
    data["access_token"] = auth['access_token']
    r = requests.post(SUBMIT_URL, data=data)

    return r.json()

def cancel_task(jobid):
    debug_print("Cancelling task : {0}".format(jobid))
    debug_print ("{0} - {1} - {2}".format(record["job_id"], record["status"], record["reason"]))
    return True

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def status_task(jobid):
    debug_print("Status task : {0}".format(jobid))
    status = {}
    record = requests.get(STATUS_URL + "/{0}".format(jobid))
    if record.status_code != 200:
        print "[ERROR] Failed to fetch job, please check jobid"
        exit(-1)

    results = record.json()
    for index in results['items']:
        k = results['items'][index].keys()[0]
        v = results['items'][index][k]
        if k == "outputs" :
            if v.startswith('<a href'):
                v = bcolors.OKGREEN + v.strip('</a>').split('>')[-1]  + bcolors.ENDC
            elif v.startswith('<i>'):                
                v = bcolors.FAIL + v.strip('<i>').strip('</i>') + bcolors.ENDC
            else :
                v = bcolors.WARNING + v + bcolors.ENDC

        print "{0:20}  | {1:50}".format(k, str(v).strip())
        
    return results

def fetch_outputs(jobid):
    debug_print("Status task : {0}".format(jobid))
    status = {}
    record = requests.get(STATUS_URL + "/{0}".format(jobid))
    
    results = record.json()
    if results['status'] != 'completed':
        print "JOB[{0}] is not in completed state. Results cannot be fetched".format(jobid)
        exit(-1)

    try:
        print "Creating directory : {0}".format(jobid)
        os.makedirs(jobid)
    except:
        pass

    for index in results['items']:
        k = results['items'][index].keys()[0]
        v = results['items'][index][k]

        if k == "outputs" :
            if v.startswith('<a href='):
                url = v.strip('<a href=').split('">')[0].strip('\"')
                fname = "{0}/{1}".format(jobid, v.strip('</a>').split('>')[-1])
                print "Downloading file   : {0}".format(bcolors.OKGREEN + fname +bcolors.ENDC)
                download_file('{0}'.format(url), fname)
            else:
                v = v.strip('<i>').strip('</i>')
                print "File not available : {0}".format(bcolors.FAIL + v + bcolors.ENDC)
        
    return results
    
def list_jobs(authfile):
    auth = get_access_token(authfile)

    data = {"access_token" : auth['access_token']}
    r = requests.get(LIST_URL, data=data)

    print r
    results =  r.json()
    if results['status'] == "Success":
        print "{0:40}|{1:15}|{2:10}|{3:20}".format("JOBID", "STATUS", "JOBTYPE", "SUBMIT_STAMP")
        for index in results['items']:
            print "{0:40}|{1:15}|{2:10}|{3:20}".format(results['items'][index]["job_id"],
                                                       results['items'][index]["status"],
                                                       results['items'][index]["jobtype"],
                                                       results['items'][index]["submit_stamp"])

    return results
    
GLOBAL_VERBOSE=False


if __name__ == "__main__":

    parser   = argparse.ArgumentParser()
    parser.add_argument("-j", "--jobinfo",  help="json job description or jobid", required=True)
    parser.add_argument("-a", "--authfile", help="File with auth info")
    parser.add_argument("-r", "--request",  help="Request type [submit, status, cancel, fetch, list]", required=True)
    parser.add_argument("-v", "--verbose",  dest='verbose', action='store_true', help="Verbose output")
    args   = parser.parse_args()


    if args.verbose is True:
        GLOBAL_VERBOSE=True

    if args.request.lower() == "submit":
        if not args.authfile :
            print "[ERROR] Authfile missing. Cannot submit job without authfile"
            exit(-1)
            
        uid = submit_task(args.jobinfo, args.authfile)
        if uid["status"] == "Success":
            print "[{0}] Job_id: {1}".format(uid["status"], uid["job_id"])
        else:
            print "[{0}] Reason: {1}".format(uid["status"], uid["reason"])

    elif args.request.lower() == "status":
        results= status_task( args.jobinfo)
        print results["status"]

    elif args.request.lower() == "cancel":
        cancel_task( args.jobinfo)

    elif args.request.lower() == "fetch":
        fetch_outputs( args.jobinfo)

    elif args.request.lower() == "list":
        if not args.authfile :
            print "[ERROR] Authfile missing. Cannot submit job without authfile"
            exit(-1)

        list_jobs( args.authfile)

    else:
        print "Unknown request"
        exit(-1)
    
    exit(0)


    

