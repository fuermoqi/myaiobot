# -*- coding: utf-8 -*-
import time
import random
import discord
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import threading
from discord_webhook import DiscordEmbed, DiscordWebhook
from selenium.webdriver.support import expected_conditions as EC

def cart_nike_au(producturl,size):
    options = Options() 
    options.add_argument('--start-maximized') 
    chromedriver = 'C:/DevelopTools/Python/Python38/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver,chrome_options=options)
    driver.get(producturl)
    sizes = driver.find_elements_by_class_name('css-xf3ahq')
    if len(sizes)==0:
        print('Goods do not exist')
        driver.close()
        return '商品不存在'
    for sizeinhtml in (sizes):
        if size in (sizeinhtml.text.split('/')[0]):
            break

    sizeinhtml.click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="buyTools"]/div[2]/button[1]').click()
    time.sleep(3)
    driver.get('https://www.nike.com/au/en/cart')
    while 'cart' not in driver.current_url:
        time.sleep(2)
    time.sleep(2)
    try:
        # driver.find_element_by_xpath('//*[@id="react-root"]/div/div[6]/button').click()
        # driver.find_element_by_xpath('//*[@id="react-root"]/div/div[4]/div/div/button[1]').click()

        # 修改购物车数量
        # driver.find_elements_by_tag_name('select')[1].find_elements_by_tag_name('option')[int(cartnum)-1].click()
        driver.find_element_by_xpath('//*[@id="maincontent"]/div[2]/div[2]/aside/div[5]/div/button[1]').click()
    except:
        print('can not find checkout')
        driver.close()
        return '出错了'
    
    for i in range(3):
        time.sleep(2)
        url=driver.current_url
        if "checkout" in url:
            print("checkout in driver.current_url")
            driver.close()
            return url   
    print("checkout not in driver.current_url")
    driver.close()
    return '出错了'    
            
    



client = discord.Client()

@client.event
async def on_ready():
    print("NIKE AU BOT")
    print('Logged in as %s' %client.user.name)
    print("Client User ID: %s" %client.user.name)
    print('------')
    game = discord.Game("NIKE AU CART")
    await client.change_presence(status=discord.Status.idle, activity=game)
    
@client.event
async def on_message(message):
    if message.content.startswith('!'):
        producturl = 'https://www.nike.com/au/t/xyisthebossman/'+message.content.split(" ")[1]
        cartsize = message.content.split(" ")[2]
        carturl = cart_nike_au(producturl,cartsize)
        embed = discord.Embed(title='Nike AU Cart',description='Wrote by XY in 20 minutes',color=0x36393F)
        embed.add_field(name='Cart Link', value=carturl,inline=True)
        embed.set_author(name=message.author)
        embed.set_footer(text=str(message.author)+' | XiaoDingDangNotify',icon_url='http://www.520touxiang.com/uploads/allimg/160722/3-160H2103649.jpg')
        await message.channel.send(embed=embed)


client.run('')## put your bot token
