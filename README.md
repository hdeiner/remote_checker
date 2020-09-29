### Building Our Own DevOps Tools.

##### Concept
DevOps calls for creative thinking about how to use the tools in front of use to solve problems.  Too many teams don't have the tools that they need, and/or are forced to use (sometimes) expensive tools to do their jobs.

For this project, we have three machines running on platforms that we can ssh into.  Each machine will be tested to see if it's function in the environment is "running" by
<ul>
<li>Checking the output of "ps -ef" to see if a particular string is in the output</li>
<li>Checking the output of "sudo lsof -i -P -n | grep LISTEN" to see if a particular port is being listened to</li>
</ul>

For this project, we will use Python to build our tool.

##### Usage
```bash
python3 main.py ; echo $?
```
This executes remote_checker and outputs some diagnostics.  The echo $? shows us what the system exit code was, which you normally don't see in bash processing.

```bash
connecting to ec2-54-237-50-195.compute-1.amazonaws.com
executed ps -ef and looking for vault server -config=/vault/config -dev-root-token-id= -dev-listen-address=0.0.0.0:8200
executed sudo lsof -i -P -n | grep LISTEN and looking for 8200

connecting to ec2-34-239-107-33.compute-1.amazonaws.com
executed ps -ef and looking for mysqld --default-authentication-plugin=mysql_native_password
executed sudo lsof -i -P -n | grep LISTEN and looking for 3306

connecting to ec2-52-205-75-84.compute-1.amazonaws.com
Exception: [Errno None] Unable to connect to port 22 on 52.205.75.84
retry...
connecting to ec2-52-205-75-84.compute-1.amazonaws.com
executed ps -ef and looking for /bin/sh -c java -jar zipster-1.0-SNAPSHOT.jar
executed sudo lsof -i -P -n | grep LISTEN and looking for 8080

0
```
This execution shows a zero exit code for the conditions at the time of execution.  

The program uses the paramiko package, which appears to have a problem when repeated used, and the ssh_for_application_and_port.py was enhanced to retry the operations when a such a generalized exception as "Exception: [Errno None] Unable to connect to port 22 on 52.205.75.84" was encountered.