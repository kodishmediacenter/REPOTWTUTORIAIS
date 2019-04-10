

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools

from addon.common.addon import Addon

addonID = 'plugin.video.masterchef'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'


def run():
    plugintools.log("masterchef.run")
    
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

def main_list(params):

    
                
    



		plugintools.log("rsa ===> " + repr(params))
                plugintools.add_item(title = "[B][COLOR red]MasterChef [/COLOR]-[COLOR yellow] BR[/COLOR][COLOR green]ASIL[/COLOR][/B]"         , url = base + "channel/UC2EWGw-KBjEReUbXMJEiaCA/",       thumbnail = icon, folder = True)
                
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')

run()
