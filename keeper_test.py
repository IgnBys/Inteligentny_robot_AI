#TODO: add real test
import random

from keeper import Keeper
from package import Package
from manager import Manager
#this is just a demonstration on how the keeper and manager classes work
if __name__ == "__main__":
   Alice=Keeper(1,10)
   print(Alice.get_id())
   kwiatek=Package(2)
   print("Alice:", Alice.get_inventory())
   Alice.insert_package(kwiatek)
   Bob=Keeper(2,10)
   Mango=Manager()
   print("Alice:", Alice.get_inventory())
   print("Bob:", Bob.get_inventory())
   Mango.Trade(Alice,Bob)
   print("Alice:",Alice.get_inventory())
   print("Bob:",Bob.get_inventory())
   Mango.Trade(Alice,Bob)
   print("Alice:", Alice.get_inventory())
   print("Bob:", Bob.get_inventory())
   Palma=Package(9)
   Bob.insert_package(Palma)
   print("Alice:", Alice.get_inventory())
   print("Bob:", Bob.get_inventory())
   Palma = Package(8)
   Bob.insert_package(Palma)
   print("Alice:", Alice.get_inventory())
   print("Bob:", Bob.get_inventory())


   Storage=Keeper(3,100000)
   rnd=random.Random()
   for i in range(0,100):
    paczka=Package(rnd.randint(a=1,b=10))
    Storage.insert_package(paczka)
   print(Storage.get_inventory())
