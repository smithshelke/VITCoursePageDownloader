# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 12:49:41 2018

@author: SMITH
"""
from json import load,dumps
from os.path import join
from bs4 import BeautifulSoup as soup
import requests
from os import fsync,remove, makedirs
from os.path import  isfile, exists,abspath
from base64 import b64decode
from PIL import Image
import pprint
from myParser import parse_captcha
from re import findall

def func(s,classid,sub,semid,mpath):
      data ={
              'classId':classid,
              'praType':'source',
              'paramReturnId':'getSlotIdForCoursePage',
              'semSubId':sem_id
              }
      
      r = s.post('https://vtopbeta.vit.ac.in/vtop/getSlotIdForCoursePage',data=data,headers = headers, cookies=cookie)
      c = soup(r.content,"html.parser")
#      print(c.find_all('button'))
      params = 0
      for button in c.find_all('button'):
          javascriptFunc = button['onclick']
          if classid in javascriptFunc:
              params = javascriptFunc
#              print(params)
              break
      formdata = findall("'(.*?)'",params)
      #print(formdata)
      
      data={
              'semSubId': formdata[0],
              'erpId': formdata[1],
              'courseType':formdata[2],
              'roomNumber': formdata[3],
              'buildingId': formdata[4],
              'slotName': formdata[5],
              'classId':formdata[6],
              'courseCode':formdata[7],
              'courseTitle': formdata[8],
              'allottedProgram':formdata[9],
              'classNum':formdata[10],
              'facultyName':formdata[11],
              'facultySchool': formdata[12],
              'courseId': formdata[13]              
      }
            
# =============================================================================
#       GET COURSE PAGE /processViewStudentCourseDetail
# =============================================================================
      r = s.post('https://vtopbeta.vit.ac.in/vtop/processViewStudentCourseDetail',data=data,headers = headers, cookies=cookie)
      c = soup(r.content,"html.parser")
#    pprint.PrettyPrinter(indent=4).pprint(c.find_all('div',{'class':'form-group'}))     
      
# =============================================================================
#       DOWNLOAD FILE BEGINS!!!
#       TEMPORARIRLY DOES NOT NAME ANY FILES
# =============================================================================
      h={}
      h={
        'Host':'vtopbeta.vit.ac.in',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://vtopbeta.vit.ac.in/vtop/executeApp/?gsid=7142641',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
      }
      h['Cookie'] = headers['Cookie']
      h['Referer'] = headers['Referer']
     
      #pprint.PrettyPrinter(indent=4).pprint(h)
      to_download = [];
      count = 0;
      path = mpath+'/VtopFiles/'+semid+'/'+sub
      print("Download path: "+path)
      if not exists(path):
          makedirs(path)
      links = c.find_all('a')
      #print(links)
      links = links[1:]
      print('Please wait...')
      #print(c.prettify())
      for link in links:
          
          if link.has_attr('href'):
              count+=1
#              print(link['href'])
              to_download.append(link)
              #print(link['href'])
              #print(url[:-6]+link['href'])
                
              
              r = s.get(url[:-6]+link['href'],headers=h,cookies=cookie)
              filename = r.headers['Content-disposition']
              filename = findall("filename=(.+)",filename)
              filename = str(count)+" "+str(filename[0])

              print(filename)
              #print(r.headers)
              open(join(path,filename), 'wb').write(r.content)
              
# =============================================================================
#               STARTS HERE
# =============================================================================
path=""
reg=""
pswd=""


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)


#if isfile():
if exists(resource_path('config.json')):
    with open(resource_path('config.json')) as f:
        print('Config found')
        data = load(f)
        reg=data['registeration_no']
        path=data['path']
        pswd=data['password']
        
else:
    pathToDownload = input("Enter path to download: ")
    pathToDownload=pathToDownload.replace('\\', '/')
    print(pathToDownload)
    reg = input("Enter registeration number: ")
    pswd = input("Enter password: ")
    data={
          'path':pathToDownload,
          'registeration_no':reg,
          'password':pswd
          }
    with open(resource_path('config.json'),'w')  as f:
              f.write(dumps(data))
              f.flush()
              fsync(f)
              f.close()
    
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest'

        }

cookie = 0
gsid = 0

with requests.Session() as s:
    url = "https://vtopbeta.vit.ac.in/vtop/"
    r = s.get(url,headers=headers)
    c = soup(r.content,'html.parser')
    #print(r.content)
    #var gsid=3152146;
    r1 = findall("var gsid=[0-9]{7};",c.text)
    gsid = r1[0][9:-1];
    #print(s.cookies.get_dict())
    cookie = s.cookies.get_dict();
    params = {
      "gsid" : gsid
    }
#    print(gsid)
    header = {'Cookie':'JSESSIONID='+cookie['JSESSIONID']+
              '; SERVERID='+cookie['SERVERID'],
              'Referer':'https://vtopbeta.vit.ac.in/vtop/executeApp/?gsid='+gsid}
    headers.update(header)
#    print('---mystery request header---')
#    print(headers)
#    print('---mystery request cookies---')
#    print(cookie)
      #------------MYST-RE-QUEST----------
    r = s.get('https://vtopbeta.vit.ac.in/vtop/executeApp/',headers=headers,cookies=cookie,params=params)
#    print(r.cookies)
    s.close()   


with requests.Session() as s:
      r = s.post('https://vtopbeta.vit.ac.in/vtop/getLogin',headers = headers,cookies=cookie)
      #print("------")
      #print(s.cookies.get_dict())
      cookie.update(s.cookies.get_dict())
      #print(cookie)
      pc = soup(r.content,"html.parser")
      imgdata = pc.find("img",{"alt":'vtopCaptcha'})["src"].split(', ')[1]
      img = b64decode(imgdata)
      ipath = resource_path(s.cookies.get_dict()['JSESSIONID']+'.bmp')
      with open(ipath,'wb')  as f:
          f.write(img)
          f.flush()
          fsync(f)
          f.close()
          #print('File is written')
      #print('-----------headers----------')
      #print(s.headers)
      header = {'Cookie':'JSESSIONID='+cookie['JSESSIONID']+'; SERVERID='+cookie['SERVERID']}
      headers.update(header)
      #print(headers)
      img = Image.open(ipath)
      #print('------WORKED-----')
      captcha = parse_captcha(img)
      if exists(ipath):
          remove(ipath)
      else:
          print("The file does not exist")
      #print("Captcha: "+captcha)
      #i = input('Captcha: ')
      #print(i)
      
      r = s.post('https://vtopbeta.vit.ac.in/vtop/processLogin',data={'uname':reg,'passwd':pswd,'captchaCheck':captcha}, headers = headers, cookies=cookie)
      cookie.update(s.cookies.get_dict())
      ##print(r.content)
      header = {'Cookie':'JSESSIONID='+cookie['JSESSIONID']+'; SERVERID='+cookie['SERVERID']}
      headers.update(header)
      #print(headers)
      data={'verifyMenu':'true'}
      r = s.post('https://vtopbeta.vit.ac.in/vtop/academics/common/StudentTimeTable',data=data,headers = headers, cookies=cookie)
      content = soup(r.content,'html.parser')
      list_of_sem = content.find_all('option')
      sem_id=''
      for sem in list_of_sem:
          if "Fall" in sem.string:
              #print(sem)
              #print(sem["value"])
              sem_id=sem["value"]
              break

      data = {'semesterSubId':sem_id}
      
# =============================================================================
#       GET TIMETABLE /processViewTimeTable
# =============================================================================
      
      r = s.post('https://vtopbeta.vit.ac.in/vtop/processViewTimeTable',data=data,headers = headers, cookies=cookie)
      c = soup(r.content,"html.parser")
      #print(r.content)
      
# =============================================================================
#       STRUCTURE OF TIMETABLE
#       count = 0 -> serial number
#       count = 1 -> class group (general semester)
#       count = 2 -> course code
#       count = 3 -> course title
#       count - 4 -> course type
#       count = 5 -> ltpjc
#       count = 6 -> course option
#       count = 7 -> class number 
#       count = 8 -> slot
#       count = 9 -> venue
#       count = 10 -> faculty
#       count = 11 -> status
# =============================================================================
      tt = []
      subCount=0
      for row in c.find_all('tr'):
          count=0    
          sub={}
          for td in row.find_all('td'):
              if td.find('p'):                
                  if count == 0:
                      sub['sr'] = td.find('p').text
                  if count == 1:
                      sub['sem_goup'] = td.find('p').text
                  if count == 2:
                      sub['courseCode'] = td.find('p').text
                  if count == 3:    
                      sub['courseTitle'] = td.find('p').text
                  if count == 4:
                      sub['courseType'] = td.find('p').text
                  #if count == 5:
#                      sub['sr'] = td.find('p').text
                  if count == 6:
                      sub['courseOption'] = td.find('p').text
                  if count == 7:
                      sub['classNum'] = td.find('p').text
                  if count == 8:
                      sub['slotName'] = td.find('p').text
                  if count == 9:
                      sub['roomNumber'] = td.find('p').text
                  if count == 10:
                      sub['facultyName'] = td.find('p').text
                  if count == 11:
                      tt.append(sub)
                      subCount+=1
                      break
                      #sub['sr'] = td.find('p').text
              count+=1    
              
      print('############### TIME TABLE ##############')
      pprint.PrettyPrinter(indent=4).pprint(tt)
      print('################')
      
      
# =============================================================================
#       GET ALL COURSES /getSlotIdForCoursePage
# =============================================================================
      
      r = s.post('https://vtopbeta.vit.ac.in/vtop/academics/common/StudentCoursePage',data={'verifyMenu':'true'},headers = headers, cookies=cookie)
      c = soup(r.content,"html.parser")
      options = c.find_all('options')
      for option in options:
          if "Fall" in option.text:
              sem_id = option['value']
              break
      #print(sem_id)
      
          
# =============================================================================
#       GET SLOT /getSlotIdForCoursePage   For now classid aka classno is static
# =============================================================================
      for sub in tt:
          subname = sub['courseTitle']
          classid = sub['classNum']
          subname+= " "+sub['courseType']
          countTry = 0
          print("======Downloading====="+subname)
          try:
              countTry+=1
              #print(classid,subname,path)
              func(s,classid,subname,sem_id,path)
          except:
              print("Error...")
              print("Trying again")
              try:
                  countTry+=1
                  #func(s,classid,subname)
                  func(s,classid,subname,sem_id,path)
              except Exception as e:
                  print("Error...")
                  print("Trying again")
                  print(e)
      print("##COMPLETE##")
      s.close()
      
      







