# ipyparallel_kotta
Integrating ipyparallel with Cloud Kotta

Start engines locally:

1. Start the ipcluster with
python start_engines_local.py <number_of_engines>

2. Start jupyter-notebook with
jupyter notebook --no-browser --port=8889&

3. In local machine, execute command:
ssh -N -f -L localhost:8888:localhost:8889 username@bastion.turing.net

4. Open localhost:8888/tree in browser

*************************************************************************************

Start with controller and engines remotely


1. Start controller:
python controller.py

2. cp ~/.ipython/profile_default/security/ipcontroller-engine.json ipcontroller.json

3. Start engines:
python engine.py <path_to_ipcontroller-engine.json> <walltime_in_mins> <Queue> <auth_file>

4. Start jupyter-notebook with
   jupyter notebook --no-browser --port=8889&

5. In local machine, execute command:
ssh -N -f -L localhost:8888:localhost:8889 username@bastion.turing.net

6. Open localhost:8888/tree in browser
