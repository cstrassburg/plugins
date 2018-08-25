#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#  Copyright 2018       Christian Strassburg      c.strassburg(a)gmx.de


from lib.model.smartplugin import *
import types
from lib.item import Item
from lib.item import Items

ITEM_TAG = "history"
SIZE_TAG = "history_size"

class ItemHistory(SmartPlugin):
    PLUGIN_VERSION='1.5.1'
    size = 5
    def __init__(self, sh, *args, **kwargs):
        print("1")
        self.logger = logging.getLogger(__name__)
        #self.size =

    def run(self):
        print ("2")
        self.alive = True


    def stop(self):
        print("3")
        #nothing to cleanup
        self.alive = False

    def parse_logic(self, logic):
        print("4")


    def update_item(self, item, caller=None, source=None, dest=None):
        print("5")
        new_history = item.history_item._value.copy()
        if len(new_history) == item.history_size:
            del new_history[-1]
        new_history.insert(0,item.prev_value())
        item.history_item(new_history)
        print(new_history)

    def parse_item(self, item):
        print("6")
        if self.has_iattr(item.conf, ITEM_TAG):
            try:
                item.history_size = int(self.get_iattr_value(item.conf, ITEM_TAG))
            except ValueError as e:
                self.logger.warning(e)
                item.history_size = self.size

            i = Item(self.get_sh(),item,item.path()+'.history_item',{'type':'foo', 'name':'history'} )
            i([])
            item.history_item= i
            Items.get_instance().add_item(item.path()+'.history_item', i)
            item.get__children().append(i)
            return self.update_item

        return None
