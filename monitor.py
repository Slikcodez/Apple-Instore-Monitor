import json.decoder
import random
from discord_webhook import DiscordWebhook
import time
import tls_client

# Make sure to test your proxies to apple before hand, Residentials work better, although, if using resis lower delay at bottom loop


discordhook = 'yourhookhere'
webhook = DiscordWebhook(
    url=discordhook,
    rate_limit_retry=True,
    content=f'monitor is online')
webhook.execute()
session = tls_client.Session(
    client_identifier="chrome_105"
)
myfile = open('proxies.txt','r')
proxy1 = myfile.read()
proxies = proxy1.split("\n")
def webhook(link):
    webhook = DiscordWebhook(
        url=discordhook,
        rate_limit_retry=True,
        content=link)
    webhook.execute()
def checkStock(sku,zipcode,startingnum):
    proxy = proxies[startingnum]
    proxyip = proxy.split(":")[0]
    proxyport = proxy.split(":")[1]
    proxyuser = proxy.split(":")[2]
    proxypass = proxy.split(":")[3]
    proxy = "http://" + f"{proxyuser}:{proxypass}@{proxyip}:{proxyport}"
    res = session.get(
        f"https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&cppart=UNLOCKED/US&parts.0={sku}&location={zipcode}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "gzip, deflate",
            "Connection": "keep-alive"
        },
        proxy=proxy
    )
    if res.status_code == 403 or res.status_code == 503:
        print(f"Proxy {proxy} is banned from endpoint")
    else:
        time.sleep(1)
        json1 = res.json()
        json2 = json1['body']
        pickupSearchQuote = json1['body']['content']['pickupMessage']['stores'][0]['partsAvailability'][sku]['pickupSearchQuote']
        pickupDisplay = json1['body']['content']['pickupMessage']['stores'][0]['partsAvailability'][sku]['pickupDisplay']

        if pickupSearchQuote == 'Available Today':
            print(sku, 'is available at',zipcode)
            webhook = DiscordWebhook(url=discordhook, rate_limit_retry=True,
                                     content=f'@everyone{sku} in stock at {zipcode}')
            print(sku, "not available at", zipcode, proxy.split(":")[2])
startingnum = 0 #goes off of a list of 500 proxies
while True:
    skus = ["MQ8R3LL/A","MQ8W3LL/A","MQ8N3LL/A","MQ8T3LL/A","MQ8Q3LL/A","MQ8V3LL/A","MQ8P3LL/A","MQ8U3LL/A"]
    zipcodes = ['97204','97223','97224']
    for zipcode in zipcodes:
        for sku in skus:
            startingnum = startingnum + 1
            if startingnum == 500: #based off 500 proxies, once hits 500 restarts list
                startingnum = 0
            try:
                checkStock(sku,zipcode,startingnum)
            except:
                print("didnt recieve resposne from apple")
            time.sleep(.5)
    


