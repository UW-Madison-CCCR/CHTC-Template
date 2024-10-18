# CHTC Python Project Template

This project provides a basic guide to running a Python project through UW's Center for High-Throughput Computing.

This guide will show you how to:
1. Configure your project's packages through a **build** file
2. Set up your primary Python scripts, shell scripts, and a **submit** file
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

Below, you can configure the different Python packages you want to include. The installation command is `python3 -m pip install pandas`, the same command you would run to install packages in the terminal. Adding additional packages would simply require you to separate each package with a space: `python3 -m pip install pandas openpyxl numpy`. 

Examples of different software and package builds can be found on [the CHTC GitHub](https://github.com/CHTC/recipes/tree/main/software).

### Setting Up your Submit File

The definition file alone can't configure software. Instead, you need to run a script to use this definition to build your software and install necessary packages. In the **build** folder, open **build.sub** to see an example.

This file is a submit file for CHTC HTCondor system. This tells CHTC to run a specific **job** or process, in this case, building our container.

There are a few important parts of this submit file.

First, the line `transfer_input_files = build/pandas.def` tells CHTC what files to bring into its network of computers when running your job. In this case, it looks into your **build** folder and transfers a file called **pandas.def**, our definition file.

The two statements for `request_memory` and `request_disk` specify how much RAM and storage space your job needs. Change these values for bigger jobs.

For more information about the build submit file, see [CHTC's overview](https://chtc.cs.wisc.edu/uw-research-computing/inter-submit). 

### Running your Build Job