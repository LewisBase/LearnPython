# -*- coding: utf-8 -*- 
class Engine(object):
    def __init__(self):
        pass

    def play(self,mapinmaps):
        next_x=mapinmaps.start 
        while True:
            print("\n-------")
            room=getattr(mapinmaps,next_x)
            next_x=room()
