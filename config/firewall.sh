#!/usr/bin/env bash

iptables -I INPUT -m tcp -p tcp -j DROP  # drop all, except that bellow

iptables -I INPUT -m tcp -p tcp --dport 22044 -j ACCEPT  # ssh
#iptables -I INPUT -m tcp -p tcp --dport 5432 -j ACCEPT   # django. Comment after development
iptables -I INPUT -m tcp -p tcp --dport 80 -j ACCEPT     # http
iptables -I INPUT -m tcp -p tcp --dport 443 -j ACCEPT    # https
