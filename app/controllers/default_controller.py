# -*- coding: utf-8 -*-
import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie

@Routing.Route(url='/', method='GET', disabled=True)
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

    number = int(Cookie.get_cookie(request, 'doge', 0))
    Cookie.set_cookie(request, 'doge', str(number+1), expires_after_days=60)

    pass_variables = {
        'name' : 'liteframework', 
        'info' : lines,
        'number' : number+1,
        #list(map(lambda line: line.encode('utf8'), lines))
    }

    
    return Controller.response_view('default.html', pass_variables)