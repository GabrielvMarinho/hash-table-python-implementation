import hashlib

class HashTable:

    def __init__(self, size):
        self.size = size
        self.hash_table = [() for i in range(self.size)]
        self.register_counting = 0

  
    def get_position(self, key):
        encoded_key = key.encode("utf-8")
        sha_256_key = hashlib.sha256(encoded_key).digest()
        int_number = int.from_bytes(sha_256_key)
        hashed_key =  int_number % self.size
        return hashed_key
    
    def get_next_free_position(self, key, val, position):

      
        if position <= self.size-1: 
            bucket = self.hash_table[position]

            if bucket != () or bucket == ("-", "-"):
                return self.get_next_free_position(key, val, position+1)
            else:
                return position
                
        else:
            return self.get_next_free_position(key, val, 0)
    
    def set_value(self, key, val):

        hashed_key = self.get_position(key)
        bucket = self.hash_table[hashed_key]

        
        if bucket == ():
            self.hash_table[hashed_key] =  (key, val)
            self.register_counting = self.register_counting +1
        
        elif bucket[0] != key:
            position = self.get_next_free_position(key, val, hashed_key+1)
            if(position !=None):
                self.hash_table[position] = (key, val)
                self.register_counting = self.register_counting +1

        elif bucket[0] == key:
            self.hash_table[hashed_key] = (key, val)
        else:
            print("This item already exist!")
        
        if(self.register_counting/self.size*100 >=50):
            self.resize_hastable()


    def get_next_position_equals(self, key, position):
      
        if position <= self.size-1:
            bucket = self.hash_table[position]
            if(bucket):
                key_bucket, value_bucket = self.hash_table[position]
                if(key_bucket == "-" or key_bucket != key):
                    return self.get_next_position_equals(key, position+1)                    
                else:
                    return position

        else:
            return self.get_next_position_equals(key, 0)
            

    def get_value(self, key):
        hashed_key = self.get_position(key)

        

        if(self.hash_table[hashed_key]):
            bucket = self.hash_table[hashed_key]
            key_bucket, value_bucket = bucket
            if(key_bucket == key):
                return bucket
            else:
                position = self.get_next_position_equals(key, hashed_key+1)
                if(position !=None):
                    
                    return self.hash_table[position]
                return
        else:
            print("No record found!")
    
    def delete_val(self, key):
        hashed_key = self.get_position(key)
        key_bucket, value_bucket = self.hash_table[hashed_key]
        if(key_bucket == key):
            self.hash_table[hashed_key] = ("-", "-")
            self.register_counting = self.register_counting -1

        else:
            self.hash_table[self.get_next_position_equals(key, hashed_key+1)] = ("-", "-")
            
    def __str__(self):
        return "--".join(str(item) for item in self.hash_table)
    
    def resize_hastable(self):
        self.size = self.size*2

        old_hash_table = self.hash_table
        
        self.hash_table = [() for i in range(self.size)]
                

        self.register_counting = 0

        for bucket in old_hash_table:
            if(bucket != ()):
                [key, value] = bucket
                self.set_value(key, value)
            

    
hash_tab = HashTable(10)



# Inserting values test
print("-> Inserting values:")
hash_tab.set_value("first_name", "Alice")
hash_tab.set_value("age", "30")
hash_tab.set_value("city", "New York")

# Collision test
print("\n-> Inserting key that causes collision (first_name2):")
hash_tab.set_value("first_name2", "Bob")

# Rewriting values test
print("\n-> Rewrinting values:")
hash_tab.set_value("first_name", "Tom")
hash_tab.set_value("age", "15")
hash_tab.set_value("city", "New Jersey")

# Retrieving values test
print("\n-> Retrieving values:")
print("first_name:", hash_tab.get_value("first_name"))
print("age:", hash_tab.get_value("age"))
print("city:", hash_tab.get_value("city"))
print("nickname (nonexistent):", hash_tab.get_value("nickname"))

# Duplicate value test
print("\n-> Inserting duplicate key (first_name):")
hash_tab.set_value("first_name", "George")

# Deletion test
print("\n-> Deleting a value:")
hash_tab.delete_val("age")
print(hash_tab)

# Read after deletion
print("\n-> Retrieving age after deletion:")
print("age:", hash_tab.get_value("age"))

# Automatic resize test
print("\n-> Forcing a resize:")

hash_tab.set_value("country", "USA")
hash_tab.set_value("hobby", "Reading")
hash_tab.set_value("color", "Blue")
print(hash_tab)