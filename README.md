### Building Our Own DevOps Tools.

##### Concept
DevOps calls for creative thinking about how to use the tools in front of us to solve problems.  Too many teams don't have the tools that they need, and/or are forced to use (sometimes) expensive tools to do their jobs.

For this project, we have three machines running on platforms that we can ssh into.  Each machine will be tested to see if it's function in the environment is "running" by
<ul>
<li>Checking the output of "ps -ef" to see if a particular string is in the output</li>
<li>Checking the output of "sudo lsof -i -P -n | grep LISTEN" to see if a particular port is being listened to</li>
</ul>

For this project, we will use Python to build our tool.

#### Installation
Make sure that Python is installed and usable from the command line.

This project was developed under Python 3.6.9.  You can check with
```bash
python --version
```

Once the project files have been put in place (git clone is your friend here), install all the PyPi dependencies by
```bash
python -m pip install -r requirements.txt
```

##### Usage
```console
./checkAWSQA.sh
```
This executes remote_checker and outputs some diagnostics.  

```bash
#!/bin/bash

if python3 remote_checker.py
then
echo "AWSQA environment is good"
else
echo "AWSQA environment is NOT good"
fi
```
This minimal bash script shows how the exit code from main.py integrates with bash for powerful tools that we can compose in bash or some other execution environment.

```console
connecting to ec2-100-25-134-180.compute-1.amazonaws.com
executed ps -ef and looking for vault server -config=/vault/config -dev-root-token-id= -dev-listen-address=0.0.0.0:8200
executed sudo lsof -i -P -n | grep LISTEN and looking for 8200

connecting to ec2-100-25-22-192.compute-1.amazonaws.com
executed ps -ef and looking for mysqld --default-authentication-plugin=mysql_native_password
executed sudo lsof -i -P -n | grep LISTEN and looking for 3306

connecting to ec2-54-144-140-173.compute-1.amazonaws.com
Exception: [Errno None] Unable to connect to port 22 on 54.144.140.173
retry...
connecting to ec2-54-144-140-173.compute-1.amazonaws.com
executed ps -ef and looking for /bin/sh -c java -jar zipster-1.0-SNAPSHOT.jar
executed sudo lsof -i -P -n | grep LISTEN and looking for 8080

AWSQA environment is good
```
And if something went wrong, such as an 8081 substituted for the 8080 at the end of line 3 in the machines.csv, we get
```console
connecting to ec2-100-25-134-180.compute-1.amazonaws.com
executed ps -ef and looking for vault server -config=/vault/config -dev-root-token-id= -dev-listen-address=0.0.0.0:8200
executed sudo lsof -i -P -n | grep LISTEN and looking for 8200

connecting to ec2-100-25-22-192.compute-1.amazonaws.com
executed ps -ef and looking for mysqld --default-authentication-plugin=mysql_native_password
executed sudo lsof -i -P -n | grep LISTEN and looking for 3306

connecting to ec2-54-144-140-173.compute-1.amazonaws.com
Exception: [Errno None] Unable to connect to port 22 on 54.144.140.173
retry...
connecting to ec2-54-144-140-173.compute-1.amazonaws.com
executed ps -ef and looking for /bin/sh -c java -jar zipster-1.0-SNAPSHOT.jar
executed sudo lsof -i -P -n | grep LISTEN and looking for 8081
did not find port

AWSQA environment is NOT good
```

The program uses the paramiko package, which appears to have a problem when repeated used, and the ssh_for_application_and_port.py was enhanced to retry the operations when a such a generalized exception as "Exception: [Errno None] Unable to connect to port 22 on 52.205.75.84" was encountered.