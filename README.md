# CHTC Python Project Template

This project provides a basic guide to running a Python project through UW's Center for High-Throughput Computing.

This guide will show you how to:
1. Configure your project's packages through a **build** file [(Jump to Section)](#1-configuring-the-projects-build)
2. Set up your primary Python scripts, shell scripts, and a **submit** file [(Jump to Section)](#2-creating-your-scripts)
3. Split your project up into discrete **jobs** [(Jump to Section)](#3-splitting-your-project-into-jobs)
4. Run your project through CHTC [(Jump to Section)](#4-running-your-project)

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

The line `transfer_input_files = scripts/convert_data.py,split_data/$(file)` tells HTCondor what files to bring with it when it runs a job. This line looks for two files in the home directory: **convert_data.py** in the **scripts** folder and a file with the same name as the `$(file)` argument in the **split_data** folder.

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

The final line, `queue file from split_data/file_list.txt`, constructs the `$(file)` argument and queues a set of jobs for the list of files you pass it. The submit file uses the file **file_list.txt** in the **split_data** folder to determine the smaller chunks of data --- stored in multiple files --- that HTCondor will pass to the shell script and other parts of the submit file. 

Setting up **file_list.txt** to queue multiple jobs will be discussed more in the next section.

## 3. Splitting Your Project Into Jobs

Now that we have the necessary code, we need to split our project into small jobs that CHTC can run in parallel. We already set the infrastructure by allowing for the `$(file)` argument to be passed to each stage of our code. Now we need to divide our data up into multiple files and create the list that will pass it to each job.

This section will walk you through all steps necessary for splitting your data and passing arguments to your jobs. All materials can be found in the **job_management** folder.

### Splitting Data

First, we need to split our data into small chunks for each job to run. While this might not be fully necessary for **weather.csv**, a relatively small file, this becomes a much larger problem when you work with bigger datasets or require more computationally intensive operations.

#### a. Tidy Data Structure Informs the Split

One important skill for working with any type of data is creating datasets that follow [tidy data structure](https://r4ds.had.co.nz/tidy-data.html) (if you want more detail, see [Wickham, 2014](http://www.jstatsoft.org/v59/i10/paper)). This structure has three major principles:

1. Each observation has its own row (ex. a survey respsondent in a given year)
2. Each variable has its own column (ex. a respondent's age)
3. Each type of observational unit has its own table (ex. survey respondents vs social media posts)

Tidy data (like the **weather.csv** file) is useful because all data can essentially be treated the same, since the data contains only one type of observational unit (in this case, cities on a given day). Splitting the data can be done by dividing it into even chunks. This method scales well for large datasets, since you do not even need to read all of the data into memory at the same time to divide it like this.

If your data structure *isn't* tidy, this becomes more difficult. Often, you need to develop custom code to split the dataset after reading it all into memory. These solutions are rarely uniform.

> “Tidy datasets are all alike, but every messy dataset is messy in its own way” (Wickham, 2014).

#### b. Splitting Data into Chunks

Since we have a tidy dataset, we can proceed with a chunk-based method of splitting our data. So, we can develop a Python script to read the larger file in chunk-by-chunk and save those chunks to a folder that we can sent to CHTC.

You can follow along for this section by opening the file **split_data.py** in the **job_management** folder.

The following line is a useful starting point, because it determines how many rows will be in each chunk of the data:

```
chunksize = 500
```

This number was selected to demonstrate the chunking process, and it is deliberately small because there are only around 3,000 rows in the full dataset. When adapting this to your own code, the number will be much larger. The number of rows will vary based on the computational intensity of the jobs you want to run.

The next major block of code then uses the parameters we specified to read in the data chunk-by-chunk.

```
count = 0 # sets up an iteration counter to name the files
for chunk in pd.read_csv(filepath, chunksize=chunksize):

    # saves the new chunk as a dataframe to the output folder
    output_filename = os.path.join(output_folder, f'weather_{count}.csv')
    chunk.to_csv(output_filename)

    count += 1 # increases the count
```

The code functions similarly to the traditional `pd.read_csv` function, but it uses the `chunksize` argument to iteratively read in segments of the dataset. We then process the resulting chunks (each its own dataframe) by saving them to a .csv file in our specified output folder.

To split the dataset, simply run **split_data.py** through Python.

#### c. Using Data Splits to Divide Jobs

The last few lines of **split_data.py** complete the final job management step: saving the list of filenames to **file_list.txt**. As mentioned in the [previous section](#2-creating-your-scripts), this list passes the `$(file)` argument to the submit file, the shell script, and the Python file. It essentially manages and cues all jobs we want to run.

Despite its important role, the file is extremely simple. It is a simple text file containing a list of files or job arguments, each separated by a new line.

### Taking Stock of the Split

Now that we've split the data, we can take inventory of what we've set up. Our goal is distribute a number of small jobs across CHTC's network of computational resources, and we've accomplished that by...

1. ... **creating multiple files**. We now have a total of 6 segments of the weather data. Instead of running code on one big dataset, we split it up into multiple pieces for more efficient processing.
2. ... **creating versatile code**. We also have code that can work with any of these 6 segments of the dataset. Instead of needing to create custom code for each split, we simply pass an argument to reuse the underlying functions. This also makes it easier if we run into any problems. We only need to fix bugs in one place.
3. ... **queing jobs through a .txt file**. We take advantage of our split data and versatile code by using a list of files to queue each job converting those files separately. Our system will pass the queued file argument to our code, which will work with the data we want it to.

With this all in mind, we can move forward and run all of our code.

## 4. Running Your Project

We'll be following similar steps in this section to the [Configuring your Build section](#1-configuring-the-projects-build).

### Running the Jobs through CHTC

Like before, if you're using Cyberduck, click "Open Connection" in the top navigation bar. In the first dropdown menu, select "SFTP (SSH File Transfer Protocol)." For "server," input the server your account is associated with, then input your NetID username and password and click "Connect."

Once connected, drag the necessary folders into your CTHC directory. These will include the following folders: **chtc_output** (for managing errors and logs), **scripts** (for the necessary code), and **split_data** (for the datasets and job queing list).

After you get through all the Duo approvals and successfully transfer the folders, open Terminal.

Like with the build, you will need to connect to the CHTC server with the following command:
```
ssh {NetID username}@{CHTC server}
```
Replace {NetID username} with your NetID username and {CHTC server} with the CHTC server your account is associated with (either ap2001.chtc.wisc.edu or ap2002.chtc.wisc.edu). After connecting, enter your NetID password.

After you connect, run the following command in Terminal:
```
condor_submit scripts/convert_data.sub
```

This should display the following lines in Terminal:

> Submitting job(s)......
> 6 job(s) submitted to cluster {cluter ID}.

If you want to check the status of your jobs, run the command:
```
condor_q
```

If you see any "held" jobs, these were prevented from finishing by the system. If you want to see the reasons for this, run the command:
```
condor_q -held
```

If `condor_q` shows that all your jobs have finished running, refresh your Cyberduck directory. You should see your 6 output files. You can download these to your CHTC-Template directory.

If your files ever don't show up, you can check the errors, print logs, or CHTC system logs. We held all of these in the **chtc_output** folder that we sent to Cyberduck.

### Merging the Output Files