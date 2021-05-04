# transparant-https-proxy

## Getting started
To get started first clone this project to your computer.
After cloning the project navigate to the folder and open your text editor.
First of all we need to setup a virtual environment, this prevents having shared libraries across multiple projects
and helps manage the packages. To do this we first need to have `Python 3.8` on our computer.
Check your python version with the following commands depending on how you installed Python:

`python -V`
or
`python3 -V`

If you have the correct version installed, run the command with whichever of the above commands gave you the correct version in the directory "transparant-https-proxy" (project directory). 

`python -m venv env`
or
`python3 venv env`

This might take a little bit of time to complete. When the command is done with execution, you will now have a new folder called env in your project directory. Now we need to activate this environment in the project directory:

For Windows:
`env/scripts/activate`
For Linux (I think):
`source env/bin/activate`

Now that you have your virtual environment activate you should see (env) PS path_to_the_current_directory in your command line interface. The next step is to install all required packages for this project, because we are using a virtual environment, this is really easy to maintain and setup. All you need to do to get started is the following:

`pip install -r requirements.txt`
or depending on your python installation:
`pip3 install -r .\requirements.txt`

If you get the message that your pip version is deprecated use:
`python -m pip install --upgrade pip`
or
`python3 -m pip3 install --upgrade pip`

## Updating the requirements.txt after adding a new package
`pip freeze > requirements.txt`
or
`pip3 freeze > requirements.txt`

## Unittests
To run the unittests:
`python -m pytest tests`

## Running the project in its current state
`python htmlparser\parser.py`
or
`python3 .\htmlparser\parser.py`
