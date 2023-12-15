#!/bin/bash
red='\033[0;31m'
plain='\033[0m'

# check root
[[ $EUID -ne 0 ]] && echo -e "请使用ROOT用户运行此脚本" && exit 1

# check os
if [[ -f /etc/redhat-release ]]; then
  release="centos"
elif cat /etc/issue | grep -Eqi "debian"; then
  release="debian"
elif cat /etc/issue | grep -Eqi "ubuntu"; then
  release="ubuntu"
elif cat /etc/issue | grep -Eqi "centos|red hat|redhat"; then
  release="centos"
elif cat /proc/version | grep -Eqi "debian"; then
  release="debian"
elif cat /proc/version | grep -Eqi "ubuntu"; then
  release="ubuntu"
elif cat /proc/version | grep -Eqi "centos|red hat|redhat"; then
  release="centos"
else
  echo -e "无法检测系统 退出" && exit 1
fi

if [[ x"${release}" == x"centos" ]]; then
  yum install wget -y
else
  apt update -y
  apt install wget -y
fi

echo -e "开始解锁"
wget -q "https://raw.githubusercontent.com/110099/cdn/master/jp.toml" -O /etc/soga/routes.toml
soga restart
