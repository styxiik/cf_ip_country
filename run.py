import geoip2.database
import ipaddress
import os

GEOIP2_DATABASE_PATH = "./GeoLite2-Country.mmdb"
IP_RANGES_FILE_PATH = "./cfip.data"
# 读取包含IP网段的文件
with open(IP_RANGES_FILE_PATH, 'r') as f:
    lines = f.readlines()

# 加载GeoIP2数据库
reader = geoip2.database.Reader(GEOIP2_DATABASE_PATH)

# 遍历每个IP网段并保存其所属的国家
for line in lines:
    # 解析IP网段
    ip_network = ipaddress.ip_network(line.strip())
    
    # 遍历IP地址范围并查询所属国家
    for ip_address in ip_network.hosts():
        try:
            # 查询IP地址所属国家
            response = reader.country(str(ip_address))
            country_name = response.country.name
            
            # 将IP地址所属国家保存到相应的文件中
            filename = f'{country_name}.txt'
            with open(filename, 'a') as f:
                f.write(str(ip_address) + '\n')
        # 忽略无法找到国家的IP地址
        except geoip2.errors.AddressNotFoundError:
            pass

# 关闭GeoIP2数据库连接
reader.close()
