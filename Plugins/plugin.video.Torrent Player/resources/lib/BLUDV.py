# -*- coding: utf-8 -*-

import urllib, urllib2, sys, re, os, unicodedata,urlparse
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
h = HTMLParser()		
##############################################################################################
plugin_handle = int(sys.argv[1])

mysettings = xbmcaddon.Addon(id = 'plugin.video.Torrent Player')
addon_name = 'MMFilmes'
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanarts = xbmc.translatePath(os.path.join(home, 'fanart2.jpg'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
Proxima = xbmc.translatePath(os.path.join(home, 'Proxima.png'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
base = 'https://www.meuguia.tv/'
dialog = xbmcgui.Dialog()    
#############################################################################################
def getUrl(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def Googlebot(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Googlebot/2.1 (+http://www.googlebot.com/bot.html)')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
	
def add_link(name,url,mode,iconimage,fanart,description):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
		cmItems = []
		if mode==4:
			cmItems.append(('[COLOR gold]Próximos Programas[/COLOR]',  'XBMC.RunPlugin(%s?url=%s&mode=3&name=%s&iconimage=%s&description=%s)'%(sys.argv[0],urllib.quote_plus(url),urllib.quote_plus(name),urllib.quote_plus(iconimage),urllib.quote_plus(description))))
		liz.addContextMenuItems(cmItems, replaceItems=False)
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
#############################################################################################	
params = dict(urlparse.parse_qsl(sys.argv[2].replace('/?','/&')))
xbmc.log('%s'  % params)
url = params.get("url")
name = params.get("name")
mode = int(params.get("mode",'0'))
iconimage = params.get("iconimage")
description = params.get("?description")
ignore = ['Lançamentos','Series','Início']
def Home():
	add_link('Lançamentos','http://www.bludv.com/',22,icon, fanarts,'Lançamentos')
	add_link('Séries','http://www.bludv.com/category/series',22,icon, fanarts,'Séries')
	add_link('Categorias','http://www.bludv.com/',23,icon, fanarts,'Categorias')
	add_link('Filmes por resolução','http://www.bludv.com/',23,icon, fanarts,'Filmes por resolução')
	add_link('Pesquisa','http://',24,icon, fanarts,'Categoria')

def Pesquisar():
	keyb = xbmc.Keyboard('', 'Buscar..')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=search.replace(' ','%20')
		urls = 'https://www.google.com.br/search?q={0}&q=+site%3Awww.bludv.com'.format(parametro_pesquisa)
		link = Googlebot(urls)
		soup = BeautifulSoup(link)
		rew = soup.findAll('h3',{'class':'r'})
		for a in rew:
			uri = a.a.get('href')
			nome = a.a.text.encode('utf-8')
			if 'baixar' in uri or 'download' in uri:
				add_link(nome,'https://www.google.com'+uri,100,icon, fanarts,'d')
	else:
		sys.exit()		
	
def Listar_Filmes_E_Series(url):#22
	link = getUrl(url)
	link = link.replace("""<div class="wp-pagenavi"><div class='wp-pagenavi'>""","<div class='wp-pagenavi'>")
	xbmc.log(link, xbmc.LOGNOTICE)
	soup = BeautifulSoup(link)
	rew = re.compile('<div class="title">.*?<a href="(.*?)".*?>(.*?)<.a>.*?<img.*?src="(.*?)" width="').findall(link.replace('\n',''))
	for a in rew:
		try: name = a[1].split(' Torrent ')[0].replace('#8211;','')
		except: name = a[1]
		url = a[0]
		img = a[2]
		add_link(name,url,100,img, fanarts,'BLUDV_Player')
	try:
		matchs = soup('div',{'class':'wp-pagenavi'})
		for a in matchs:
			url_pagina = '%s' % a.findAll('a')[0]['href']
			pagina = '%s' % a.findAll('span',{'class':'pages'})[0].text
			add_link('[COLOR green]'+pagina.encode('utf-8')+'[/COLOR]',url_pagina,22,Proxima, fanarts,'d')
	except:
		pass
		
def Listar_Categorias(url):	
	if description=='Categorias':
		fa = getUrl(url)
		soup = BeautifulSoup(fa)#<div class="main-menu">
		match = soup.find('div',{'class':'menu-category'}).findAll('a')
		for a in match:
			name = a.text.encode('utf-8')
			url = a.get('href')
			add_link(name,url,22,icon, fanarts,'categoria')	
	elif description=='Filmes por resolução':
		fa = getUrl(url)
		soup = BeautifulSoup(fa)#<div class="main-menu">
		match = soup.find('div',{'class':'menu-topo'}).findAll('a')
		for a in match:
			name = a.text.encode('utf-8')
			url = a.get('href')
			if not name in ignore:
				add_link(name,url,22,icon, fanarts,'categoria')	
