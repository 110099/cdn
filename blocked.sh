#!/bin/bash

# 写入的内容
content=$(cat <<EOF
regexp:(torrent|\.torrent|peer_id=|info_hash|get_peers|find_node|BitTorrent|announce_peer|announce.php?passkey=)
regexp:(.?)(xunlei|sandai|Thunder|XLLiveUD)(.)
regexp:(Subject|HELO|SMTP)
regexp:(^.*@)(guerrillamail|guerrillamailblock|sharklasers|grr|pokemail|spam4|bccto|chacuo|027168).(info|biz|com|de|net|org|me|la)
regexp:(.+.|^)(360|so).(cn|com)
regexp:(.*.)(dafahao|falundafamuseum|rfa|minghui|mhradio|dongtaiwang|epochtimes|ntdtv|falundafa|wujieliulan).(org|com|net)
regexp:(.*\.)(gash)\.(com|tw)
regexp:(.*\.)(mycard)\.(com|tw)
regexp:.*gov.*
regexp:.*go.kr.*
regexp:(.*.)(cyberpolice|12377|110|12337|12389|jubao|8221110|cctv|81|12388|isc|12339|js12377).(org|com|net|cn|gov)
EOF
)

# 目标文件路径
target_file="/etc/soga/blockList"

# 将内容写入目标文件
echo "$content" > "$target_file"

# 执行 soga restart 命令
soga restart

echo "已完成审计"
