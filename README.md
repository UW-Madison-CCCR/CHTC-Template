# CHTC Python Project Template

This project provides a basic guide to running a Python project through UW's Center for High-Throughput Computing.

This guide will show you how to:
1. Configure your project's packages through a **build** file
2. Set up your primary Python scripts, shell scripts, and a **submit** file
3. Split your project up into discrete **jobs**
4. Run your project through CHTC

This basic example project will use Python and the [pandas](https://pandas.pydata.org) package to run some basic operations on  weather data found in [vega datasets](https://github.com/vega/vega-datasets/tree/main).

If you do not have a CHTC account yet, you can apply for one [here](https://chtc.cs.wisc.edu/uw-research-computing/form.html).

Using a development environment, specifically [Visual Studio Code](https://code.visualstudio.com), is highly recommended for this exercise. 

## 1. Configuring the Project's Build

In order to run any program through CHTC, you need to install the [software](https://chtc.cs.wisc.edu/uw-research-computing/software-overview-htc) that your program needs. 

To bring your necessary software onto CHTC, you need to create a **container**. Containers hold information like general software (like Python) or libraries for this software  (like pandas or numpy in Python). CHTC accepts two forms of containers: Apptainers (which this guide will focus on) and Docker images.

All materials to follow along with this section of the guide can be found in the **build** folder in this repository.

### Setting Up Your Definition File 

In the **build** folder, open **pandas.def**. This is an example of a **definition file**, which specifies the version of your software and the packages you want to include.

At the top of the file, you can see the software and specific version next to "From" (in this case, it's Python version 3.11). If you want to use a different version of Python, you can change it here.

Below, you can configure the different Python packages you want to include. The installation command is `python3 -m pip install pandas`, the same command you would run to install packages in the terminal. Adding additional packages would simply require you to separate each package with a space: `python3 -m pip install pandas openpyxl numpy`. 