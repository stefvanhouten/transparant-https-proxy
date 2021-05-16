# transparant-https-proxy

## Getting started
To get started first clone this project to your computer.
After cloning the project navigate to the folder and open your text editor.
First of all we need to setup a virtual environment, this prevents having shared libraries across multiple projects
and helps manage the packages. To do this we first need to have `Python 3.8` on our computer.
Check your python version with the following commands depending on how you installed Python:

```python
python -V
```

or
```python
python3 -V
```

If you have the correct version installed, run the command with whichever of the above commands gave you the correct version in the directory "transparant-https-proxy" (project directory).
```python
python -m venv env
```

or

```python
python3 venv env
```

This might take a little bit of time to complete. When the command is done with execution, you will now have a new folder called env in your project directory. Now we need to activate this environment in the project directory:

For Windows:
```
env/scripts/activate
```

For Linux (I think):

```source env/bin/activate```

Now that you have your virtual environment activate you should see (env) PS path_to_the_current_directory in your command line interface. The next step is to install all required packages for this project, because we are using a virtual environment, this is really easy to maintain and setup. All you need to do to get started is the following:

```pip install -r requirements.txt```

or depending on your python installation:

```pip3 install -r .\requirements.txt```

If you get the message that your pip version is deprecated use:

```python -m pip install --upgrade pip```

or

```python3 -m pip3 install --upgrade pip```

## Updating the requirements.txt after adding a new package
`pip freeze > requirements.txt`
or
`pip3 freeze > requirements.txt`
## Creating the proxy
Visit https://mitmproxy.org/ and click either "Download Windows Installer" or "Download Linux Binaries (WSL)".
A file will be downloaded. Click on this file and it will execute.

## Configure WiFi settings (transparency has not been implemented yet)
- Left mouse-click on your WiFI icon.
- Click on "Network & internet settings"
- Click on "Proxy"
- Click "Manual Proxy setup"
- Address: `127.0.0.1` (default setting)
- Port: `8080` (default setting)
- Save

## Generate Self signed certificate
Go to http://mitm.it/. If you see the text _"If you can see this, traffic is not passing through mitmproxy."_, it means your proxy is not active and something went wrong during installation.
If everything did go correct, you should see tiles which should look like this:

![tiles](https://user-images.githubusercontent.com/38207747/117337332-89354400-ae9d-11eb-9341-81573eedb531.PNG)

Click on _get mitmproxy (...)_ next to the tile that shows your operating system.
From there on the wizard will prompt you to select for which user (on your computer) this program should be installed and to configure whether you would like to create a password for your private key.

Upon completion of the above, close _mitmpdump_ or _mitmproxy ui_ (if it's running) and close the browser.

Type in the windows search box either _mitmpdump_ or _mitmproxy ui_. Both are proxy servers, _mitmproxy ui_ comes with an interface, whereas _mitmdump_ will give you the console display.
Click on the one you prefer and wait until you see _Web server listening at http://127.0.0.1:8081/
Proxy server listening at http://*:8080_ in the opened console.

Start your favorite browser and type in: https://google.com.
If the installation went correct, you should be able to see google via HTTPS.

To confirm mitm is signing the certificate, click on the key lock next to the Uniform Resource Locator (URL).

Click on _Certificate_ and you should see the following:

![image](https://user-images.githubusercontent.com/38207747/117338929-6dcb3880-ae9f-11eb-8c77-367b76fa823c.png)


## Flask
Setting up and running the flask API server.

Linux:

```export FLASK_APP=flaskr
export FLASK_ENV=development
flask run```

Windows:

```$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
flask run```

## Unittests

To run the unittests:
```python -m pytest tests```
Or:
```make test```
## Congratulations!
Your self signed certificate has been successfully generated and handed out to the website and all the requests and responses are being sent through your proxy.

# Make commands for Linux
Running `make` will setup a virtualenv, this will also keep track of changes in the `requirements.txt` and update accordingly.
