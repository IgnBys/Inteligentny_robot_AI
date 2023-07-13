from package import Package
# from klient import Klient
class Keeper():
    #TODO:STATES

    def __init__(self,id,inventory_size,posx,posy):
        self.inventory = list()
        self.id=id
        self.inventory_size=inventory_size
        self.inventory_taken = 0
        self.state=0
        self.posx = posx
        self.posy = posy
    def get_id(self):
        return self.id
    def get_inventory(self):
        return self.inventory
    #TODO: choosing package

    def get_wanted_package(self,inventory):
        min_size=inventory[0].get_size()
        candidates=[]
        for i in inventory:
            if i.get_size()<=min_size:
                min_size=i.get_size()
                candidates.append(i)
                break
        return candidates
    def pop_package(self,package:Package):
        self.inventory.remove(package)
        self.inventory_taken -=package.get_size()
        return package
    def insert_package(self,package:Package):
        if(self.inventory_taken+package.get_size()<=self.inventory_size):
            self.inventory.append(package)
            self.inventory_taken+=package.get_size()

    def trade(self, giver):
        try:
            wanted_packages = self.get_wanted_package(giver.get_inventory())
            print(wanted_packages)
            wanted_package=wanted_packages[0]
            print(wanted_packages[0].type)
            if self.inventory_taken + wanted_package.get_size() <= self.inventory_size:
                giver.pop_package(wanted_package)
                self.insert_package(wanted_package)
            else:
                print("taker has no room in inventory")
        except IndexError:
            # TODO
            print("taker has no wanted package")
#szuka paczkę o niezbędnym id (wanted_id)
    def get_wanted_package_by_id(self,inventory, wanted_id):
        for i in range (0,len(inventory)):

            if inventory[i].get_id()==wanted_id:

                return inventory[i],i
            else:
                print('There is no wanted package')
                return None

