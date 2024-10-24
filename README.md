# CHTC Python Project Template

This project provides a basic guide to running a Python project through UW's Center for High-Throughput Computing.

This guide will show you how to:
1. Configure your project's packages through a **build** file [(Jump to Section)](#1-configuring-the-projects-build)
2. Set up your primary Python scripts, shell scripts, and a **submit** file [(Jump to Section)](#2-creating-your-scripts)
3. Split your project up into discrete **jobs**
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

When listing the additional packages you want to included, **do not** list any packages that are part of the Python standard library. These will cause the build to fail. For a complete list of the Python standard library packages, check this [link](https://docs.python.org/3/library/index.html), but a few notable packages would be:
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

The final line of the script, `python3 convert_data.py "$1"`, calls for Python to run your .py file, passing in a system-level argument from the submit fill (which will be a .csv filepath).