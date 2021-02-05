from proxies_scrapper import Scrapper, Proxy

# to add more sources follow the pattern
# datax =  Scrapper(category='A Category').getProxies()
# data = [..., datax]
# check the proxies_scrapper file for all available categories

# data1 = Scrapper(category='SSL').getProxies()
# data2 = Scrapper(category='NEW').getProxies()
# data3 = Scrapper(category='PROXYLIST_DOWNLOAD_HTTPS').getProxies()

# proxies_data = [data1, data2, data3]

# f = open("proxies.txt", "w")

# for data in proxies_data:
#     for proxy in data.proxies:
#         s = f"https://{proxy.ip}:{proxy.port}\n"
#         f.write(s)

# f.close()

#################################################

scrapper = Scrapper(category='ALL', print_err_trace=False)
data = scrapper.getProxies()
print("Total proxies scraped : ", data.len)
f = open("proxies.txt", "w")

for proxy in data.proxies:
    s = f"https://{proxy.ip}:{proxy.port}\n"
    f.write(s)

f.close()
