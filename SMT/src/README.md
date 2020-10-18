# Requirements
This program requires the installation of some softwares and packages.

***!!! WARNING !!! <br> YOU HAVE TO INSTALL ALL OF THE FOLLOWING REQUIREMENTS IN ORDER TO RUN BOT CP AND SMT, IF YOU MISS ONE OF THEM, THE PYTHON PROGRAM WILL NOT RUN <br>!!! WARNING !!!***

## Python
The program was developed using **Python 3.8**. You have to install it first by downloading this version for your OS from their website.
For this project, some packages are required:
- pyfiglet
- numpy 
- matplotlib
- minizinc
- z3-solver

To make things easier, I'm providing also the Python 3.8 virtual environment I've been using to develop this program. See **Installation** section to know how to install it.

## MiniZinc
You also have to install **MiniZinv 2.4.3** by dowloading this version for your OS from their website.
 
 # Installation
To install the virtual environment, first you have to download and install Python 3.8 from their website.
After doing that, you need to follow these steps to install the virtual environment:
1. Open a CMD/Terminal window (depending on you OS) and move to the main directory of the program using the following command
```bash
cd \path\to\project\main\directory\
```
2. Create a new python virtual environment
```bash
virtualenv <env_name>
```
3. Activate the new virtual environment
```bash
source <env_name>/bin/activate
```
4. Install the packages using the *"requirements.txt"* file in the main directory
```bash
pip install -r requirements.txt
```

After following these steps, you will have a new virtual environment in the main directory of the project with all the required packages installed. To activate and use it, just move again to the main directory of the project using command in point *1.* and activate the virtual environment using command in point *3.*. 

To install MiniZinc, you just need to download the version 2.4.3 for you OS from the software website and install it.

# Usage
After installing and configuring everything, to launch the program, you need to move to the main directory of the program using
```bash
cd \path\to\project\main\directory\
```
Then, activate the virtual environment created before
```bash
source <env_name>/bin/activate
```
After doing this, you can launch the program using the command
```bash
python PWP.py <arguments>
```
The *arguments* you can use are divided into mandatory and optional.

### Mandatory arguments:

**--solve \<file/folder\>**: specify which file(s) to solve
- *file*: specify the path of the *.txt* input instance to solve
- *folder*: specify the path of the folder which contains the *.txt* input instances to solve

**--method \<CP/SMT\>**: specify the solving method
- *CP*: solve the input instance(s) using CP
- *SMT*: solve the input instance(s) using SMT

**--mode \<standard/general\>**: specify the solving mode for the input instance(s)
- *standard*: solve the input instance(s) using the standard mode (using standard model)
- *general*: solve the input instance(s) using the general mode (using general model)

### Optional arguments:

**--timeout \<value\>**: specify timeout for the solving
- *value*: specify a time limit (in seconds)
    - if *value* is not specified or this command is not used, the default timeout is 5 minutes (300 seconds)
    - to disable timeout, use **--timeout 0**

**--stats**: shows solving statistics for each input instance
- if a folder is specified, shows also the average scores for all the instances

**--plot**: plot the solution
- works only if a single input file is specified

The order in which these commands are specified does not matter.

## Command examples for Satisfiability Modulo Theories (SMT)

Solve the input instance with SMT using standard model, also plot the solution virually (if exists) and show solving statistics. Timeout is set to 5 minutes.
```bash
python PWP.py --solve \path\to\file\input_instance.txt --timeout 300 --method SMT --mode standard --stats --plot
```
<br>
Solve the input instances in the specified folder with SMT using general model. Timeout is set to default (5 minutes).

```bash
python PWP.py --solve \path\to\folder\ --method SMT --mode general
```
<br>
Solve the input instances in the specified folder with SMT using standard model and show the solving statistics. Timeout is removed.

```bash
python PWP.py --solve \path\to\folder\ --method SMT --mode standard --timeout 0 --stats
```
