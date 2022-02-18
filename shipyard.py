class Shipyard:
    class Container:
        class Package:
    
            def __init__(self, name, weight, next_p=None, prev_p=None):
                '''
                Package class initializer. 
                Parameters: owner, weight, next_p, prev_p
                '''
                self._name = name
                self._p_weight = int(weight)
                self._pID = 'P' + str(id(self))
                self._p_next = next_p
                self._p_prev = prev_p
            
            def __str__(self):
                '''
                Convert package object into a readable string
                '''
                return('Name: ' + str(self._name) + '\nWeight: ' + 
                       str(self._p_weight) +' lbs' + '\nPackage ID: ' + 
                       str(self._pID) + '\n')        
        
        
        
        # Container class: 
        def __init__(self, Destination, Sizes, next_c=None, prev_c=None):
            '''
            Container initializer
            Parameters: destination, sizes, next_c (next container), 
                        prev_c (previous container)
            '''
            self._destination = Destination
            self._c_weight = 0
            self._size = 0
            self._Front = None # First package
            self._Back = None  # Last package
            self._c_prev = prev_c
            self._c_next = next_c
            self._cID = 'C' + str(id(self)) 
        
        def add_package(self, name, weight, pID):
            '''
            Adds a package to the container. 
            Parameter: name, weight, pID
            '''
            if self._size == 0:
                self._Back = self.Package(name, weight)
                self._Front = self._Back
                self._c_weight += int(weight)
                self._size += 1
            else:
                current = self._Front
                for i in range(self._size):
                    # If current package is lighter:
                    if current._p_weight <= weight:
                        if (current._p_next != None) and \
                        (current._p_next._p_weight >= weight):
                            package = self.Package(name, weight, 
                                                   current._p_next, current)
                            current._p_next = package
                            current._p_next._p_prev = package
                            self._c_weight += weight
                            self._size += 1
                            return
                        current = current._p_next
                    # If current package if heavier:
                    else:
                        package = self.Package(name, weight, current)
                        current._p_prev = package
                        self._Front = package
                        self._size += 1
                        self._c_weight += weight
                        return
                self._Back._p_next = self.Package(name, weight, None,
                                                  self._Back)
                self._Back = self._Back._p_next
                self._c_weight += weight
                self._size += 1
        
        def __str__(self):
            '''
            Converts Container class into a readable string. 
            '''
            return('Container ID: ' + str(self._cID) + '\nWeight: ' + 
                   str(self._c_weight) + '/2000 lbs used' + '\nDestination: ' + 
                   str(self._destination) + '\n')

    
    
    
    # Shipyard class: 
    def __init__(self):
        '''
        Shipyard initializer
        '''
        self._first = None
        self._last = None
        self._s_id = 0
        self._s_size = 0
    
    def is_empty(self):
        '''
        Determine if the shipyard is empty or not
        '''
        if self._s_size == 0:
            return True
        else: return False 
    
    def position(self, destination):
        '''
        Finds container to insert after based on alphabetical order. 
        Parameters: destination
        return: Container to insert after. 
        '''
        if self._last._destination < destination:
            return self._last
        current = self._first
        for i in range(self._s_size):
            # If current destination is higher in alphabetical order:
            if current._destination >= destination:
                return current._c_prev
            else: current = current._c_next
    
    def add_container(self, destination, next_s=None):
        '''
        Finds the proper location, then inserts a new container. 
        Parameters: destination, next_s
        return: container
        '''
        if self.is_empty():
            container = self.Container(destination, self._s_size)
            self._first = container
            self._last = container
            self._s_size += 1
            return container
        past = self.position(destination)
        if past == None:
            container = self.Container(destination, self._s_size, 
                                       self._first)
            self._first._c_prev = container
            self._first = container
        elif self._last == past:
            container = self.Container(destination, self._s_size,
                                       self._last)
            container._c_prev._c_next = container
            self._last = container
        else:
            container = self.Container(destination, self._s_size, past._c_next, 
                                       past)
            container._c_prev._c_next = container
            container._c_next._c_prev = container
        
        self._s_size += 1
        return container
    
    #adds a new package with name, destination, weight to the system
    def add(self, name, destination, weight):
        '''
        Looks for a container in linked list and adds a package to it.
        If there is no container, it calls add_container to make one. 
        Parameters: name, destination, weight
        '''
        if self.is_empty() == True:
            # Creates new container if none 
            container = self.add_container(destination)
            self._first = container
            self._last = container
            # Create package 
            container.add_package(name, weight, self._s_id)
            self._s_id += 1
        else:
            # If already a container available:
            current = self._first
            for i in range(self._s_size):
                if current._destination == destination:
                    if ((current._c_weight + weight) <= 2000):
                        current.add_package(name, weight, self._s_id)
                        self._s_id += 1
                        return
                    else:
                        if (current._c_next != None) and \
                        (current._c_next._destination != destination):
                            container = self.add_container(destination, 
                                                           current._c_next)
                            container.add_package(name, weight, self._s_id)
                            self._s_id += 1
                            return
                if current._c_next != None and current._c_next._cID <= \
                (destination + str(self._s_size)):
                    current = current._c_next
                else: break
            
            container = self.add_container(destination, current)
            container.add_package(name, weight, self._s_id)
            self._s_id += 1
    
    #prints manifest of whole system
    def printAll(self):
        '''
        Prints entire shipyard manifest. 
        '''
        if self.is_empty():
            print('\nNo containers in shipyard.')
            return
        current = self._first
        print('\nContainers:')
        for i in range(self._s_size): #loop through list
            print(current) 
            package = current._Front
            print('Packages: ')
            for i in range(current._size):
                print(package)
                package = package._p_next
            if current._c_next != None:
                current = current._c_next
                print(' ')
            else:
                break
    
    #prints container info list
    def printContainers(self): 
        '''
        Prints container manifest
        '''
        print('\nContainers:')
        current = self._first
        print(current,'\n')
        for i in range(self._s_size-1):
            current = current._c_next
            print(current,'\n')    
    
    #prints manifest of a single destination
    def printDest(self, destination):
        '''
        Prints a destinations manifest.
        Parameters: destination
        '''
        found = False
        current = self._first
        print('\n' + destination + ':')
        for i in range(self._s_size):
            if current._destination == destination:
                print(current, '\n')
                found = True
            if current._c_next == None:
                break
            current = current._c_next
        if found == False:
            print("No containers going to that destination.")
    
    #search the system for a package given its id. 
    #This function should report found or not found, if found, display the 
    #package info (including id #)    
    def search(self, pID):
        '''
        Searches for a package based on the ID number given. 
        Parameters: pID 
        '''
        found = False
        current = self._first
        for i in range(self._s_size):
            package = current._Front
            for i in range(current._size):
                if package._pID == pID:
                    found = True
                    print("\nFound package with ID " + str(pID) + ':\n' +  
                          str(package))
                    break
                package = package._p_next
            if current._c_next != None:
                current = current._c_next
            else: break
        if not found: 
            print("No package found with that ID.")
    
    #remove a package given its id number
    def remove(self, pID):
        '''
        Removes a package based on the ID number given.
        Parameters: pID
        '''
        found = False
        current = self._first
        for i in range(self._s_size):
            package = current._Front
            for i in range(current._size):
                if package._pID == pID:
                    found = True
                    if current._size == 1:
                        self.delete(current)
                    elif current._Front == package:
                        current._Front = current._Front._p_next
                        current._Front._p_prev = None
                        current._size -= 1
                    elif current._Back == package:
                        current._Back._p_next = None
                        current._size -= 1
                    else:
                        package._p_prev._p_next = package._p_next
                        package._p_next._p_prev = package._p_prev
                        current._size -= 1
                    break
                package = package._p_next
            if current._c_next != None:
                current = current._c_next
            else:
                print("\nPackage with ID", pID, "has been removed.")
                break
        if not found: 
            print("\nNo packages with that ID.")
    
    
    def delete(self, container):
        '''
        Deletes a container. 
        Called on when a container is empty. 
        '''
        if self._s_size == 1:
            pass
        elif self._first == container:
            self._first = self._first._c_next
            self._first._c_prev = None
        elif self._last == container:
            self._last = self._last._c_prev
            self._last._c_next = None
        else: 
            print(container)
            container._c_next._c_prev = container._c_prev
            container._c_prev._c_next = container._c_next
        self._s_size -= 1
    
    #ship out all containers to a given destination
    def ship(self, destination):
        '''
        Ships out the items heading to the destination specified and 
        prints out the information about it. 
        Parameters: destination
        '''
        shipped = 0
        ship_weight = 0
        current = self._first
        found = False
        for i in range(self._s_size):
            if current._destination == destination:
                shipped += 1
                ship_weight += current._c_weight
                self.delete(current)
                found = True
            if current._c_next != None:
                current = current._c_next
            else:
                break
        if not found:
            print("\nNo containers for that destination.")
            return
        print("\nShipped " + str(shipped) + " containers with a total mass of: " +
              str(ship_weight))


################################################################################


def menu():
    menu_input = input("\nSelect an option: \na. Add Package"
                     "\nb. Shipyard Manifest"
                     "\nc. Container Manifest"
                     "\nd. Destination Manifest"
                     "\ne. Search for Package with ID"
                     "\nf. Remove Package via ID"
                     "\ng. Ship Off to Destination"
                     "\nh. Exit\n\nSelection: ")    
    return menu_input


def user_input(menu_input, s):
    
    while menu_input != "h":
        
        if menu_input == "a":
            name = input("Enter the name of the owner: ").strip().lower()
            destination = input("Enter a destination: ").strip().lower()
            weight = int(input("Enter the weight (lbs): "))
            s.add(name, destination, weight)
            
        if menu_input == "b":
            if s._s_size != 0:
                print("\nShipyard: ")
                s.printAll()
            else:
                print("\nPlease add a package first.")
                break
        
        if menu_input == "c":
            if s._s_size != 0:
                s.printContainers()
            else:
                print("\nPlease add a package first.")   
                break
        
        if menu_input == "d":
            if s._s_size != 0:
                destination = input(
                    "\nEnter the shipment destination to search for: ").lower()
                s.printDest(destination)
            else:
                print("\nPlease add a package first.")   
                break
            
        if menu_input == "e":
            if s._s_size != 0:
                pID = input("Enter the ID of the package to search for: ")
                s.search(pID)

        if menu_input == "f":
            if s._s_size != 0:
                pID = input("Enter the ID of the package to remove: ")
                s.remove(pID)
            else:
                print("\nPlease add a package first.")
                break
        
        if menu_input == "g":
            if s._s_size != 0:
                destination = input(
                    "\nWhich destination would you like to ship? ")
                s.ship(destination)
            else:
                break
        
        else:
            break


def main():
    s = Shipyard()
    while True:
        menu_input = menu()
        end = user_input(menu_input, s)
        if end:
            break


################################################################################


def test():
    s = Shipyard()
    print("\nAdding 4 shipments...")
    s.add("Isaac", "Japan", 1200)
    s.add("Chris", "Italy", 300)
    s.add("Isaac", "Japan", 900)
    s.add("Mark", "Italy", 800)
    
    print("\nPrinting all...")
    s.printAll()
    print("\nPrinting Italy...")
    s.printDest("Italy")
    print("\nPrinting Containers...")
    s.printContainers()
    print("\nShipping to Japan...\n")
    s.ship("Japan")
    print("\nPrinting all again...")
    s.printAll()
