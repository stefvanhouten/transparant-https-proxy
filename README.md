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
python3 -m venv env
```

This might take a little bit of time to complete. When the command is done with execution, you will now have a new folder called env in your project directory. Now we need to activate this environment in the project directory:

For Windows:
```
env/scripts/activate
```

For Linux:

```bash
source env/bin/activate
```

Now that you have your virtual environment activate you should see (env) PS path_to_the_current_directory in your command line interface. The next step is to install all required packages for this project, because we are using a virtual environment, this is really easy to maintain and setup. All you need to do to get started is the following:

```bash
pip install -r requirements.txt
```

or depending on your python installation:

```bash
pip3 install -r .\requirements.txt
```

If you get the message that your pip version is deprecated use:

```python
python -m pip install --upgrade pip
```

or
```python
python3 -m pip3 install --upgrade pip
```

## Updating the requirements.txt after adding a new package
```bash
pip freeze > requirements.txt
```
or
```bash
pip3 freeze > requirements.txt
```


## Setting up Flask
Setting up and running the flask API server.

Linux:

```bash
export FLASK_APP=api
export FLASK_ENV=development
flask run
```

Windows:

```bash
$env:FLASK_APP = "api"
$env:FLASK_ENV = "development"
flask run
```

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

## Starting the project
Start the project by executing the following command while you are in the project folder.
```bash
mitmproxy -s proxy.py
```

## Generate Self signed certificate
The project will work as-is with http websites, but websites that utilize https (SSL) will require some additional steps as you might otherwise encounter the following error message:

![image](https://user-images.githubusercontent.com/11412480/121014932-c6416e80-c79a-11eb-8862-ac95446e7f2d.png)

By default, mitmproxy will automatically create a root certificate during first launch, so be sure to run the project first before proceeding with the following steps. 

Mitmproxy will put these certificates in the `.mitmproxy` folder of your user. Linux, macOS, and most browsers will need the `mitmproxy-ca-cert.pem` certificate, while Windows requires the `mitmproxy-ca-cert.p12` certificate.

```bash
user@Hostname ~ ls -l /home/user/.mitmproxy
total 24
-rw-r--r-- 1 user user 1318 May 11 14:18 mitmproxy-ca-cert.cer
-rw-r--r-- 1 user user 1140 May 11 14:18 mitmproxy-ca-cert.p12
-rw-r--r-- 1 user user 1318 May 11 14:18 mitmproxy-ca-cert.pem
-rw------- 1 user user 2529 May 11 14:18 mitmproxy-ca.p12
-rw------- 1 user user 3022 May 11 14:18 mitmproxy-ca.pem
-rw-r--r-- 1 user user  770 May 11 14:18 mitmproxy-dhparam.pem
```

You can use the following command to copy the `mitmproxy-ca-cert.pem` file to your Linux/macOS home folder, for easier installation:

```bash
cp /home/$USER/.mitmproxy/mitmproxy-ca-cert.pem .
```

Find the installation instructions for various platforms below:

- [Mozilla Firefox](https://wiki.mozilla.org/MozillaRootCertificate#Mozilla_Firefox)
- [Google Chrome](https://stackoverflow.com/a/15076602/198996)
- [Ubuntu/Debian](https://askubuntu.com/questions/73287/how-do-i-install-a-root-certificate/94861#94861)
- [macOS](https://support.apple.com/guide/keychain-access/add-certificates-to-a-keychain-kyca2431/mac)
- Windows: simply double-click the `mitmproxy-ca-cert.p12` file, and follow the instructions.

After installing the certificate, go to a website that utilizes the https protocol, such as [stackoverflow.com](https://stackoverflow.com/). You should see the padlock in your browser, indicating that your connection is successfully running over https.

![image](https://user-images.githubusercontent.com/11412480/121016912-0144a180-c79d-11eb-83dd-95c8eecb42c7.png)


To confirm mitmproxy is signing the certificate, click on the keypad symbol in your URL bar. Click on _Certificate_ and you should see the following:

![image](https://user-images.githubusercontent.com/11412480/121017091-2b965f00-c79d-11eb-8daa-fb9b76ca3647.png)

## Unittests

To run the unittests:
```python
python -m pytest tests
```
Or:
```bash
make test
```
## Congratulations!
Your self signed certificate has been successfully generated and handed out to the website and all the requests and responses are being sent through your proxy.

# Make commands for Linux
Running `make` will setup a virtualenv, this will also keep track of changes in the `requirements.txt` and update accordingly.
