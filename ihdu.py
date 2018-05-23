import urllib
import urllib2
import cookielib
import httplib
import requests

url="http://2.2.2.2"

#username = raw_input("userName: ")
#pwd=raw_input("pwd: ")

#to index
# conn = httplib.HTTPConnection("2.2.2.2",80)
# conn.request("GET", "ac_portal/default/pc.html?tabs=pwd")
# httpres = conn.getresponse()
# print httpres.status
# print httpres.reason
#print httpres.read()
# conn.close()

username = raw_input("userName: ")
pwd=raw_input("pwd: ")
headers = {"Host": "2.2.2.2", "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",\
	"Accept-Language": "en-US,en;q=0.5",\
	"Accept-Encoding": "gzip, deflate",\
	"Content-type":"application/x-www-form-urlencoded; charset=UTF-8",\
	"Accept":"*/*",\
	"Referer":"http://2.2.2.2/ac_portal/default/pc.html?tabs=pwd",\
	"X-Requested-With":"XMLHttpRequest",\
	"connection":"keep-alive"}
data={"opr":"pwdLogin","userName":username,"pwd":pwd,"rememberPwd":"1"}

url="http://2.2.2.2/ac_portal/login.php"


#req=urllib2.Request(url)
# req.add_header('Host',"2.2.2.2")
# req.add_header("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0")
# req.add_header("Accept-Language","en-US,en;q=0.5")
# req.add_header("Accept-Encoding","gzip, deflate")
# req.add_header("Content-type","application/x-www-form-urlencoded;charset=UTF-8")
# req.add_header("Referer","http://2.2.2.2/ac_portal/default/pc.html?tabs=pwd")
# req.add_header("X-Requested-With","XMLHttpRequest")

data = urllib.urlencode(data)

# conn = httplib.HTTPConnection("2.2.2.2",80)
# conn.request("POST", "/ac_portal/login.php", data, headers)
# httpres = conn.getresponse()
# print httpres.status
# print httpres.reason
# print httpres.read()
# conn.close()

#urllib2
req = urllib2.Request(url, data, headers)
try:
    res = urllib2.urlopen(req)
except e:
    print e.reason
print res.read()


# html=requests.post(url, data=data, headers=headers)
# print html.status_code
print "OK^^^^^^"
