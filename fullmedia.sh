#!/bin/bash

read -p "请输入选项（hk/sg/tw/jp/us/de/uk）: " option

case $option in
  hk)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/hkmedia.sh | bash
    ;;
  sg)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/sgmedia.sh | bash
    ;;
  tw)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/twmedia.sh | bash
    ;;
  jp)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/jpmedia.sh | bash
    ;;
  us)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/usmedia.sh | bash
    ;;
  de)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/demedia.sh | bash
    ;;
  uk)
    wget -qO- https://raw.githubusercontent.com/110099/cdn/master/ukmedia.sh | bash
    ;;
  *)
    echo "无效的选项！"
    exit 1
    ;;
esac
