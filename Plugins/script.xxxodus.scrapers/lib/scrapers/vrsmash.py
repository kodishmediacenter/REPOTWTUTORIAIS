import xbmc,xbmcplugin,os,urlparse,re,base64
import client
import kodi
import dom_parser2
import log_utils
import lover
from resources.lib.modules import utils
from resources.lib.modules import helper
buildDirectory = utils.buildDir

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'https://www.vrsmash.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'vr'
menu_mode    = 284
content_mode = 285
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'video/search?query=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    lover.checkupdates()

    try:
        url = urlparse.urljoin(base_domain,'category/all')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': 'videoThumbnailHolder'})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img', req=['src','alt'])) \
              for i in r if i]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[1][0].attrs['alt'], urlparse.urljoin(base_domain,i[1][0].attrs['src'])) for i in r]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8'))
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': i[2], 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst)    
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()
        
@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

    try:
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': 'videoThumbnailHolder'})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img', req=['src','alt']), \
              dom_parser2.parse_dom(i, 'div', {'class': 'videoTimecode'})) \
              for i in r if i]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[1][0].attrs['alt'], urlparse.urljoin(base_domain,i[1][0].attrs['src']), i[2][0].content if i[2] else 'Unknown') for i in r]
        if ( not r ) and ( not searched ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        if ( not searched ):
            log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
            kodi.notify(msg='Fatal Error', duration=4000, sound=True)
            quit()    
        else: pass
        
    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8'))
            name = name.title() + ' - [ %s ]' % kodi.sortX(i[3].encode('utf-8'))
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[2], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[0].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))
    
    if not searched:
        search_pattern = '''<li\s*class=['"]next['"]><a\s*href=['"]([^'"]+)'''
        parse = base_domain
        
        helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)