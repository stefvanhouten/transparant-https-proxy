# Setting up the API
## Setting up the database
Before the API can be used we need to setup the database. Setting up the database is simple, all you need to do is to get started is creating an empty MySQL database.

Run:

```bash
make venv
```

After this is completed activate the virtualenvironment with:

```bash
. .venv/bin/activate
```

Set the following environment variables:

```bash
export username=yourdbusername
export password=yourdbpassword
export host=localhost
export database=yourdbname
```

Then run:
```bash
make setup
```

## Manually initializing the  database
When running the app for the first time and you want to set up the database use the following commands to setup the database:

Linux:

```bash
export FLASK_APP=api
export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI=mysql+pymsql://{username}:{password}@{host}/{databasename}
flask init-db
```
### Running the API
```bash
make run
```
Or:

```bash
export FLASK_APP=api
export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI=mysql+pymsql://{username}:{password}@{host}/{databasename}
flask run
```
# Creating a custom config for the proxy
```bash
127.0.0.1:5000/proxy/create_config

{
    "ip": "127.0.0.1", # or any ip for that matter
    "name": "mytestconfig",
    "block_iso": "true",
    "exclude_elements": ["noscript", "script", "style", "h1", "p"]
}
```
# Using the proxy with a custom config
To run the proxy with a custom config that was created with the `create_config` api endpoint, all you need to do is pass the following headers with every request to the proxy:

```bash
config_ip: 127.0.0.1
config_name: mytestconfig
```

# Setting up the proxy
Mitmproxy should be installed if you followed the install process of the api.
To run mitmproxy use:

```bash
make run
```

Or:

```bash
mitmproxy -s proxy.py
```

## Generate Self signed certificate
The project will work as-is with http websites, but websites that utilize https (SSL) will require some additional steps as you might otherwise encounter the following error message:

![image](https://user-images.githubusercontent.com/11412480/121014932-c6416e80-c79a-11eb-8862-ac95446e7f2d.png)

By default, mitmproxy will automatically create a root certificate during first launch, so be sure to run the project first before proceeding with the following steps.

Mitmproxy will put these certificates in the `.mitmproxy` folder of your user. Linux, macOS, and most browsers will need the `mitmproxy-ca-cert.pem` certificate.

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

After installing the certificate, go to a website that utilizes the https protocol, such as [stackoverflow.com](https://stackoverflow.com/). You should see the padlock in your browser, indicating that your connection is successfully running over https.

![image](https://user-images.githubusercontent.com/11412480/121016912-0144a180-c79d-11eb-83dd-95c8eecb42c7.png)


To confirm mitmproxy is signing the certificate, click on the keypad symbol in your URL bar. Click on _Certificate_ and you should see the following:

![image](https://user-images.githubusercontent.com/11412480/121017091-2b965f00-c79d-11eb-8daa-fb9b76ca3647.png)


# Unittests
```bash
make test
```
Or:

```python
python -m pytest tests
```