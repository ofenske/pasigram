# PaSiGraM

This is the official repository for the PaSiGraM algorithm. Currently it is under development. A paper with some
benchmarks and detailed description of the algorithm will be published soon.
The repository is organized as follows:
* "distributed/": contains the code for the distributed version, which can be executed on a spark cluster.
* "local/": contains the version which can be executed on a single computer. Here you can additionally choose between 
the execution in single core or mutlicore mode (execution_mode).
  
If you want to execute the respective algorithm you just have to run the run.py script. Here you have to define the data
source from which you want to load the nodes and edges of your input graph. 

For the local mode you also have to choose between "single_core" or "multicore" execution mode. For the distributed 
version you have to specifiy the adress of your spark master node and the number of data nodes/cluster nodes you are 
using in your cluster. Examples of can be found in the respective run.py files inside the two folders.

Both versions (distributed and local) are organized by a modificated version of MVC pattern. The used data structures 
are located in the model package. The method for every data structure can be found in the service package. And the the
single parts (candidate generation and significance computation) and main method of PaSiGraM are part of the controller 
package.
