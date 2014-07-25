#/usr/bin/python
#coding=utf-8

from assets.sub_category import Rebot_Game_Info
from config.api_config import game
 
if __name__=='__main__':

    for game_code in ['ares']:
  
        for platform in game[game_code]:
            n = Rebot_Game_Info(game_code, platform)
            n.start()
            n.join()