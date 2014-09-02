'''

@author: jipingzh
'''



def hello():
    
    i = 1
    
    running = True
    while running:
        while i < 10:
            print ('i %d' % i)
            i = i+1
            
            if i == 3:
                running = False
                return
        
hello()