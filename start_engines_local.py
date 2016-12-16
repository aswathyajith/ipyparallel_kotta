import os
import argparse

def start_cluster(engines):
    start_ipcluster = "ipcluster start -n " + `engines` + " &" 
    os.system(start_ipcluster)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start engines for parallel processing with jupyter')
    parser.add_argument("engine", help="Number of engines to start", type=int)
    #parser.add_argument("-a", "--authfile", help="File with auth info")
    args = parser.parse_args()
    start_cluster(args.engine)
    
    exit(0)
    
