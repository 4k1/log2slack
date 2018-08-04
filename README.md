# log2slack
An agent for monitoring any log files and send notification to Slack based on rules you configured.

## Slack notification
Example of Postfix:  
![1-gh-001](https://github.com/4k1/log2slack/blob/master/doc/1-gh-001.jpg)

## Installation
As root, run the following commands:
```
# apt update
# apt install curl python3 python3-pip
# pip3 install requests pyyaml
# curl https://raw.githubusercontent.com/4k1/log2slack/master/src/logslack.py > /opt/logslack.py
# curl https://raw.githubusercontent.com/4k1/log2slack/master/tmpl/logslack.conf > /etc/logslack.conf
```

## Configuration
```
# vi /etc/logslack.conf
```

## Simply Start
```
# nohup python3 /opt/logslack.py your_service &
```

## Simply Stop
```
# touch /var/run/logslack.your_service.stop
# rm /var/run/logslack.your_service.stop
```
