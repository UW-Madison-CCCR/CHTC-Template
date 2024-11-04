# CHTC Python Project Template

This project provides a basic guide to running a Python project through UW's Center for High-Throughput Computing.

This guide will show you how to:
1. Configure your project's packages through a **build** file [(Jump to Section)](#1-configuring-the-projects-build)
2. Set up your primary Python scripts, shell scripts, and a **submit** file [(Jump to Section)](#2-creating-your-scripts)
3. Split your project up into discrete **jobs** [(Jump to Section)](#3-splitting-your-project-into-jobs)
4. Run your project through CHTC

This basic example project will use Python and the [pandas](https://pandas.pydata.org) package to run some basic operations on  weather data found in [vega datasets](https://github.com/vega/vega-datasets/tree/main).

If you do not have a CHTC account yet, you can apply for one [here](https://chtc.cs.wisc.edu/uw-research-computing/form.html).

Using a development environment, specifically [Visual Studio Code](https://code.visualstudio.com), is highly recommended for this exercise. Also, software to aid with file transfers between CHTC and your computer is highly recommended. [CHTC](https://chtc.cs.wisc.edu/uw-research-computing/transfer-files-computer) recommends [Cyberduck](https://cyberduck.io) for both Mac and Windows. Finally, if you want to access CHTC off-campus, you need to [connect to UW-Madison's VPN](https://kb.wisc.edu/ns/page.php?id=108255).

## 1. Configuring the Project's Build

In order to run any program through CHTC, you need to install the [software](https://chtc.cs.wisc.edu/uw-research-computing/software-overview-htc) that your program needs. 

To bring your necessary software onto CHTC, you need to create a **container**. Containers hold information like general software (like Python) or libraries for this software  (like pandas or numpy in Python). CHTC accepts two forms of containers: Apptainers (which this guide will focus on) and Docker images.

All materials to follow along with this section of the guide can be found in the **build** folder in this repository.

### Setting Up your Definition File 

In the **build** folder, open **pandas.def**. This is an example of a **definition file**, which specifies the version of your software and the packages you want to include.

At the top of the file, you can see the software and specific version next to "From" (in this case, it's Python version 3.11). If you want to use a different version of Python, you can change it here.

Below, you can configure the different Python packages you want to include. The installation command is `python3 -m pip install pandas`, the same command you would run to install packages in the terminal. Adding additional packages would simply require you to separate each package with a space: `python3 -m pip install pandas openpyxl`. 

When listing the additional packages you want to included, **do not** list any packages that are part of the Python standard library. (Note: the standard library will vary based on your version of Python.) Including these will cause the build to fail. For a complete list of the Python standard library packages, check this [link](https://docs.python.org/3/library/index.html), but a few notable packages would be:
* `os`
* `re`
* `sys`
* `datetime`

Remember, do not include these in your definition file. Check the [list](https://docs.python.org/3/library/index.html) of the Python standard library packages for your version of Python before finalizing the definition.

Examples of different software and package builds can be found on [the CHTC GitHub](https://github.com/CHTC/recipes/tree/main/software).

### Setting Up your Submit File

The definition file alone can't configure software. Instead, you need to run a script to use this definition to build your software and install necessary packages. In the **build** folder, open **build.sub** to see an example.

This file is a submit file for CHTC HTCondor system. This tells CHTC to run a specific **job** or process, in this case, building our container.

There are a few important parts of this submit file.

First, the line `transfer_input_files = build/pandas.def` tells CHTC what files to bring into its network of computers when running your job. In this case, it looks into your **build** folder and transfers a file called **pandas.def**, our definition file.

The two statements for `request_memory` and `request_disk` specify how much RAM and storage space your job needs. Change these values for bigger jobs.

For more information about the build submit file, see [CHTC's overview](https://chtc.cs.wisc.edu/uw-research-computing/inter-submit). 

### Running your Build Job

This step will give you some exposure to running basic jobs through CHTC. In this case, we want to transfer our build files to CHTC and create a container for our version of Python and the packages we want to install. This will create a file called **container.sif** that will be used in running Python scripts.

First, you need to open Cyberduck (or your file transfer application of choice) and [connect to CHTC](https://chtc.cs.wisc.edu/uw-research-computing/connecting).

If you're using Cyberduck, click "Open Connection" in the top navigation bar. In the first dropdown menu, select "SFTP (SSH File Transfer Protocol)" instead of the default "FTP (File Transfer Protocol)." For "server," input the server your account is associated with. In most cases, this will be "ap2001.chtc.wisc.edu." Finally, input your NetID username and password, then click "Connect."

After confirming the connection, drag the **build** folder from this repository into the home directory in Cyberduck.

Next, open Terminal. You will need to connect to the CHTC server with the following command:
```
ssh {NetID username}@{CHTC server}
```
Replace {NetID username} with your NetID username and {CHTC server} with the CHTC server your account is associated with (either ap2001.chtc.wisc.edu or ap2002.chtc.wisc.edu). After connecting, enter your NetID password.

After you connected to the CHTC server, run the following command in Terminal:
```
condor_submit -i build/build.sub
```
This will open an interactive job using the **build.sub** submit file in the **build** folder.

After the interactive job begins, run the following command:
```
apptainer build container.sif pandas.def
```

You will see a several lines of text and progress bars in Terminal as the system builds your container. This process will create a container file in your CHTC working directory from the **pandas.def** file you transfered via the submit file. Once you refresh the directory in Cyberduck, you should see the file **container.sif**. This is the file you need to run your future Python code.

After the container finishes building, type the following command in Terminal to exit the interactive session:

```
exit
```

## 2. Creating Your Scripts

Running a Python file requires three layers of scripts: the Python file you want to run, a shell script to run that file, and a submit file telling HTCondor to execute the shell script. 

This section will walk you through all steps necessary for building these three files. All materials can be found in the **scripts** folder.

### The Big Picture

First, it's important to lay out the specifics of what we need the three layers of scripts (.py, .sh, and .sub) to do.

CHTC helps create more efficient computing workflows by breaking up your data into small chunks and running your code on them in parallel. So, to create the code for this type of workflow, you need it to be versatile. 

Our goals for this section are to create three layers of scripts that all take a general **file** argument for a small chunk of the data. When given this argument, the program uses it to send that file to CHTC and convert it. The .sub file will pass the list of file arguments for each chunk of the data.

### Creating the Python Script

In this example script, say we want to convert the temperature data to Fahrenheit and calculate the wind chill for the weather data in **weather.csv**. We would want to use the wind chill formula from [weather.gov](https://www.weather.gov/safety/cold-wind-chill-chart):

$Wind Chill = 35.74 + 0.6215T - 35.75(V^{0.16}) + 0.4275T(V^{0.16})$

Where $T$ is the temperature in Fahrenheit and $V$ is the wind speed

There are a few major requirements we want for the Python file:
* We want to enclose most of the major operations in a function
* We want the function call to take a system argument (passed through the shell script)

You can follow along for this section by opening the file **convert_data.py** in the **scripts** folder.

#### a. Setting Up the Function

The first section of **convert_data.py** shows the basic function setup: the primary operations of the code is encased in a single function, taking an argument for the path for the file to convert. This design allows the program to be widely applicable: it will perform this same basic conversion on any file that is passed to it.

#### b. Passing a System Argument

The second section of the Python script shows how this can be applied: it calls the function using the argument `sys.argv[1]`. This will pass the system-level argument in the first slot (which will be a .csv filepath) from the shell script to the Python function.

### Creating the Shell Script

Next, we need to create a script that will pass the argument to the Python function. This will be a shell script that calls for the computer to execute the Python script with a particular argument.

You can follow along for this section by opening the file **convert_data.sh** in the **scripts** folder.

#### a. The Shebang

The first line of the script, `#!/bin/bash`, is called "the shebang." This is the part of the script that tells the computer to use `bash` to run the script. If this line is omitted, the computer will not be able to process the rest of the shell script.

#### b. Exporting Paths

The next three lines export in the necessary paths to your version of Python, your Python packages, and your home directory. These will need to be adjusted if you are using software other than Python.

#### c. Running your Script

The final line of the script, `python3 convert_data.py "$1"`, calls for Python to run your .py file, passing in a system-level argument from the submit file (which will be a .csv filepath).

### Creating the Submit File

Finally, we need to create a submit file. Like when creating the Python container, we need a submit file to tell CHTC to run our jobs.

[Submit files](https://chtc.cs.wisc.edu/uw-research-computing/multiple-jobs) can be used to send one job, like with the container build, but they can also be used to queue *multiple different jobs*. While you could create multiple submit files, shell scripts, and Python scripts, this approach to designing your jobs will allow you to queue multiple different jobs with just one file at each level (.py, .sh, and .sub).

You can follow along for this section by opening the file **convert_data.sub** in the **scripts** folder.

#### a. Setting the Executable File and its Arguments

The first two lines relate to the executable file, or the program that the submit file will run. In this case, the line `executable = convert_data.sh` tells HTCondor to run your shell script. The line `arguments = $(file)` tells the system to pass a file argument, specified in the last line of the submit file, to the shell script. In this case, since the shell script needed a `"$1"` argument to pass to the Python script, this line gives the script the argument it needs.

#### b. Setting the Container Image

The next line `container_image = container.sif` passes the container you built in the [previous section](#1-configuring-the-projects-build) to HTCondor, which will allow you to run Python scripts with the packages you need.

#### c. Setting the CHTC Output Structure

The following lines specify where HTCondor will put the log, error, and console output files:

```
log = chtc_output/logs/$(file).log
error = chtc_output/errors/$(file).err
output = chtc_output/output/$(file).out
```

These lines require the file structure to be in your CHTC home directory (you need a **chtc_output** folder with subfolders for **logs**, **errors**, and **output**). This code will take the `$(file)` argument and use it to name the log, error, and output files.

#### d. Transfering Necessary Files

The line `transfer_input_files = scripts/convert_data.py,data/$(file)` tells HTCondor what files to bring with it when it runs a job. This line looks for two files in the home directory: **convert_data.py** in the **scripts** folder and a file with the same name as the `$(file)` argument in the **data** folder.

The list of files is separated with a comma with no space.

#### e. Requesting Computational Resources

The following lines tell HTCondor what resources to give your jobs:

```
request_cpus = 1
request_memory = 3GB
request_disk = 5GB
```

Python scripts typically do not run well on multiple cores, so you will rarely need to request more than one CPUs. However, the memory (RAM) and disk space you need could vary substantially based on the type of job. You may need to test one job iteratively to determine the memory it needs to finish executing.

#### f. Queuing Multiple Jobs from a File

The final line, `queue file from file_list.txt`, constructs the `$(file)` argument and queues a set of jobs for the list of files you pass it. The submit file uses the file **file_list.txt** to determine the smaller chunks of data --- stored in multiple files --- that HTCondor will pass to the shell script and other parts of the submit file. 

Setting up **file_list.txt** to queue multiple jobs will be discussed more in the next section.

## 3. Splitting Your Project Into Jobs

