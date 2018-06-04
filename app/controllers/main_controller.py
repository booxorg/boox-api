# -*- coding: utf-8 -*-
import liteframework.controller as Controller 
import liteframework.routing as Routing 

@Routing.Route(url='/', method='GET')
def index(variables={}, request={}):
    lines = r'''
               __.                                              
            .-".'                      .--.            _..._    
          .' .'                     .'    \       .-""  __ ""-. 
         /  /                     .'       : --..:__.-""  ""-. \
        :  :                     /         ;.d$$    sbp_.-""-:_:
        ;  :                    : ._       :P .-.   ,"TP        
        :   \                    \  T--...-; :d$b   :d$b        
         \   `.                   \  `..'    ;$ $   ;$ $        
          `.   "-.                 ).        :T$P   :T$P        
            \..---^..             /           `-'    `._`._     
           .'        "-.       .-"                     T$$$b    
          /             "-._.-"               ._        '^' ;   
         :                                    \.`.         /    
         ;                                -.   \`."-._.-'-'     
        :                                 .'\   \ \ \ \         
        ;  ;                             /:  \   \ \ . ;        
       :   :                            ,  ;  `.  `.;  :        
       ;    \        ;                     ;    "-._:  ;        
      :      `.      :                     :         \/         
      ;       /"-.    ;                    :                    
     :       /    "-. :                  : ;                    
     :     .'        T-;                 ; ;        
     ;    :          ; ;                /  :        
     ;    ;          : :              .'    ;       
    :    :            ;:         _..-"\     :       
    :     \           : ;       /      \     ;      
    ;    . '.         '-;      /        ;    :      
    ;  \  ; :           :     :         :    '-.      
    '.._L.:-'           :     ;    bug   ;    . `. 
                         ;    :          :  \  ; :  
                         :    '-..       '.._L.:-'  
                          ;     , `.                
                          :   \  ; :                
                          '..__L.:-'
    '''

    pass_variables = {
        'name' : 'liteframework', 
        'info' : lines
        #list(map(lambda line: line.encode('utf8'), lines))
    }
    return Controller.response_view('default.html', pass_variables)