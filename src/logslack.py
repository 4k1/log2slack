#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import select
import time
import json
import requests
import yaml
import sys
import os

__PRODUCT_ID = "logslack 1.0 (c) 4k1/logslack"

def get_value(r, key, default=None):
    if key in r:
        if type(r[key]) is int:
            return int(r[key])
        else:
            return str(r[key])
    elif default == None:
        raise
    else:
        return default

if __name__ == '__main__':

    # Initialize
    print ("[ ] " + __PRODUCT_ID)

    # Check args
    if (len(sys.argv) != 2):
        print ("[ ] Usage: " + sys.argv[0] + " service_id");
        exit(0)
    service_id = sys.argv[1]
    print ("[ ] Initializing for '" + sys.argv[1] + "'.");

    # Load logslack.conf
    yml_target = "/etc/logslack.conf"
    try:
        f = open(yml_target)
        conf = yaml.load(f)
        f.close()
    except:
        print ("[-] Cannot load as a yaml by '" + yml_target + "'")
        exit(-1)

    # Check configuration
    if (service_id not in conf):
        print ("[-] Unknown service_id.")
        exit (-1)
    if ("push" not in conf[service_id] or
        "poll" not in conf[service_id] or
        "rules" not in conf[service_id]):
        print ("[-] Illegal yaml format.")
        exit (-1)

    # Check push engine
    try:
        eu = service_id + ".stopfile";           stopfile       = get_value(conf[service_id], "stopfile")
        eu = service_id + ".push.slack";         slack_key      = get_value(conf[service_id]["push"], "slack")
        eu = service_id + ".poll.target";        poll_target    = get_value(conf[service_id]["poll"], "target")
        eu = service_id + ".rules"
        if ("rules" not in conf[service_id]):
            raise
        rules          = conf[service_id]["rules"]
        eu = slack_key +  ".webhook"
        if ("webhook" not in conf[slack_key]):
            raise
        eu = slack_key +  ".webhook.url";        slack_url      = get_value(conf[slack_key]["webhook"], "url")
        eu = slack_key +  ".webhook.username";   slack_username = get_value(conf[slack_key]["webhook"], "username")
        eu = slack_key +  ".webhook.icon_emoji"; slack_icon     = get_value(conf[slack_key]["webhook"], "icon_emoji")
        slackprm = conf[slack_key]["webhook"]
    except:
          print ("[-] Cannot load an entity of '" + eu + "'.")
          exit (-1)

    requests.post(slack_url, data = json.dumps({
        'text': "*Start logslack for " + poll_target + ".*",
        'username': slack_username,
        'icon_emoji': slack_icon,
    }))

    cmd = ('tail -n +1 --follow=name ' + poll_target)

    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    y = select.poll()
    y.register(p.stdout, select.POLLIN)

    slack_flag = 0
    while True:

        if (os.path.exists(stopfile)):
            requests.post(slack_url, data = json.dumps({
                'text': "*Stop logslack for " + poll_target + ".*",
                'username': slack_username,
                'icon_emoji': slack_icon,
            }))
            break

        if y.poll(1):
            da = p.stdout.readline()
        else:
            slack_flag = 1

        if slack_flag != 1:
            continue

        for ar in rules:
            match  = get_value(ar, "match", "")
            notice = get_value(ar, "notice", "")
            level  = get_value(ar, "level", "#dddddd")
            if (match == "" or notice == ""):
                continue

            if (match in da):

                push_data = notice
                push_data = push_data.replace("{$log}", da)
                push_data = push_data.replace("{$keyword}", match)

                requests.post(slack_url, data = json.dumps({
                    'username': slack_username,
                    'icon_emoji': slack_icon,
                    'attachments': [
                        {
                            "title": "logslack detected",
                            "text": push_data,
                            "color": level,
                        }
                    ]
                }))
            else:
                time.sleep(1)
