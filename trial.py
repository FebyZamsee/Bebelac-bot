import requests as r
import os,platform,re,random,time,json
from pprint import pprint as pp
def swap():
	if platform.system() == 'Windows':
		os.system('cls')
	elif platform.system() == 'Linux':
		os.system('clear')
def gw(t1,t2,s):
	try:
		regexPattern = t1 + '(.+?)' + t2
		str_found = re.search(regexPattern,str(s)).group(1)
		return str_found.strip()
	except AttributeError:
		return ''
def bound(bid,datapack):
	data = ''
	for inc,exc in datapack.items():
		data += f'------WebKitFormBoundary{bid}\r\nContent-Disposition: form-data; name="{inc}"\r\n\r\n{exc}\r\n'
	data += f'------WebKitFormBoundary{bid}--'
	return data
def log(no,pw):
	url = 'https://rewards.bebeclub.co.id/Auth/Login?isSuccess=-1'
	c = r.get(url).cookies
	head = {
	'Accept':'*/*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
	'Connection': 'keep-alive',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Host': 'rewards.bebeclub.co.id',
	'Origin': 'https://rewards.bebeclub.co.id',
	'Referer': 'https://rewards.bebeclub.co.id/Auth/Login?Area=&isSuccess=-1',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-origin',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
	'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"'
	}
	data = f'__RequestVerificationToken=&urlCallback=&token_lazada=&username={no}&password={pw}&g-recaptcha-response=&captcha='
	head.update({'Content-Length':str(len(str(data)))})
	rlog = r.post(url,headers=head,data=data,cookies=c)
	if not ('/Auth/Login' in rlog.text):
		print('\n [ok] Login Sukses')
		return rlog.cookies
	else:
		print('\n [x] Login Gagal')
		return None
def katalog(kuki):
	url = 'https://rewards.bebeclub.co.id/katalog'
	cata = r.get(url,cookies=kuki)
	if (cata.status_code == 200):
		rvt = gw('<input name="__RequestVerificationToken" type="hidden" value="','"',cata.text)
		if (len(rvt) == 108):
			cekatalog(cata.cookies,rvt)
def cekatalog(kuki,rvt):
	url = 'https://rewards.bebeclub.co.id/Catalogue/GetCatalogue'
	bid = ''.join([random.choice('abcdefghijklmopqrstuvwxyz0123456789') for _ in range(16)])
	headers = {
	'x-requested-with':'XMLHttpRequest',
	'content-type':f'multipart/form-data; boundary=----WebKitFormBoundary{bid}'
	}
	data = bound(bid,{
	'__RequestVerificationToken':rvt,
	'Search':'',
	'Page':'1',
	'TotalRowPerPage':'8',
	'OrderByColumnName':'Points',
	'OrderByDirection':'Asc',
	'CatalogueCategoryID':catID})
	ctlog = r.post(url,headers=headers,data=data,cookies=kuki)
	if (ctlog.status_code):
		if ('An error occurred while processing your request.' in ctlog.text):
			print(f' [{ctlog.status_code}] An error occurred while processing your request')
		else:
			print(f' [{ctlog.status_code}] Checking Rewards for ({tipe})')
			res = ctlog.json()
			if (res['catalogue'] != None):
				pp(res['catalogue'])
				kode = input(' [?] Kode -> ')
				if (len(kode) == 0):
					cekatalog(kuki,rvt)
				redem(ctlog.cookies,kode)
			else:
				print(f' [-] Reward Kosong\n [-] {res}')
				time.sleep(5)
				for _ in range(300):
					cekatalog(kuki,rvt)
				print('---[Limit Request Reached]---\n')
				login(no,pw)
def redem(kuki,kode):
	url = f'https://rewards.bebeclub.co.id/checkoutdetail/{kode}'
	c = r.get(url,cookies=kuki).cookies
	url = 'https://rewards.bebeclub.co.id/Catalogue/CheckoutProsesDetail'
	bid = ''.join([random.choice('abcdefghijklmopqrstuvwxyz0123456789') for _ in range(16)])
	headers = {
	'x-requested-with':'XMLHttpRequest',
	'content-type':f'multipart/form-data; boundary=----WebKitFormBoundary{bid}'
	}
	data = bound(bid,{
	'dis_rewards_code':kode,
	'dis_qty':'1',
	'dis_digital_number_destination':no,
	'dis_type':'2',
	'redemption_type':'2',
	'progressid':''
	})
	rdm = r.post(url,headers=headers,data=data,cookies=kuki)
	if ('An error occurred while processing your request.' in rdm.text):
		print(' [x] Data Salah')
	else:
		print(rdm.text)
def editprfl(kuki):
	#cek
	url = 'https://rewards.bebeclub.co.id/Account/Profile'
	rcek = r.get(url,cookies=kuki)

def menu1():
	print('------[ Daftar Akun ]------')
	pw = conf['regist_password']
	reff = conf['Referal']
	no = input(' [?] Nomer : ')
	cekno = r.get(f'https://rewards.bebeclub.co.id/Account/ValidatePhone?phone={no}&_={round(time.time() * 1000)}')
	if (cekno.json()):
		if (cekno.json()['isValid'] == True):
			data = bound()
		else:
			print(f" [x] {cekno.json()['message']}")
			menu1()
	else:
		print(' [x] Situs Tidak Dapat Dijangkau')
def menu2():
	login = input(' Login ([1] Auto Redeem / [2] Edit Profil): ')
	if (login == '1'):
		no = '0895400628785'
		#no = '085702577112'
		pw = '112299Gm'
		inid = input(' Redeem ke ([1] Gopay / [2] OVO) : ') #GP = GOPAY, OV = OVO
		if (inid == '1'):
			catID = 'GP'
			tipe = 'GOPAY'
		elif (inid == '2'):
			catID = 'OV'
			tipe = 'OVO'
		else:
			catID = inid
			tipe = inid
		log(no,pw)
	elif (login == '2'):
		editprfl()
swap()
cf = 'config.json'
if not os.path.exists(cf):
	with open(cf,'w') as ff:
		ff.write('{\n"User":"YourName/@NickTelegram",\n"Apikey":"",\n"regist_password":"AkuAdalahAku11",\n"Referal":""\n}')
	ff.close()
else:
	rcon = open(cf,'r').read()
	conf = json.loads(rcon)
print(' Bebelac Auto\n  By @itsaoda\n')
menu = input(' Menu ([1] Regist / [2] Login): ')
if (menu == '1'):
	menu1()
	print('_'*38)
elif (menu == '2'):
	menu2()

print('\n\n')
