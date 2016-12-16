import os
import argparse

def start():
    start_ipcont = "ipcontroller --ip=10.0.0.249 &" 
    os.system(start_ipcont)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start ipcontroller for parallel processing with jupyter')
    #parser.add_argument("engine", help="Number of engines to start", type=int)
    #parser.add_argument("-a", "--authfile", help="File with auth info")
    args = parser.parse_args()
    start()
    
    exit(0)
    
