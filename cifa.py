# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 20:20:05 2018

@author: MFR
"""

class DFA:
    file_obj = '' #文件
    line_number = 0 #行号
    state = 0 #状态
    
    ResWord = ['int', 'if', 'then', 'else', 'end', 'while', 'do', 'begin', 'read', 'write','for']
    error_message = []  #保存错误信息,存储元组,元组第一个参数是行号,第二个参数是错误字符
    annotate_message = [] #注释信息,存储元组,元组第一个参数是行号,第二个参数是注释
    char_message = [] #识别的字符串,存储元组,元组第一个参数是类型,第二个参数是该字符串
    
    def __init__(self, file_name):
        self.file_obj = file_name
        self.state = 0
        self.line_number = 0
        self.error_message = []
        self.annotate_message = []
        self.char_message = []#特殊符号tsfh，关键字gjz，标识符bsf，数字sz
        self.symtable={}
        self.last=' '
        
    def get_symtable(self):
        i=1
  
        while(self.char_message[i][1]=='int'):      
            self.symtable[self.char_message[i+1][1]]=0
    
            i=i+3
        
        return self.symtable
        
    
    def start_convert(self):
        for line in self.file_obj:    #每一行的最后一个符号必须是可以直接识别的
            line = line.strip('\n')
            line = line.strip('\t')
            line = line.strip(' ')
            self.line_number += 1
            line_length = len(line)
            
            i = 0
            string = ''
            while i < line_length:
                ch = line[i] #读取一个字符
                i += 1
                if self.state == 0:#初始状态
                    string = ch#累加字符
 
                    if ch.isalpha():  #字母
                        self.state = 1
                    elif ch.isdigit():#数字
                        self.state = 3
                    elif ch == '+':
                        self.state = 5
                    elif ch == '-':
                        self.state = 9
                    elif ch == '*':
                        self.state = 13
                    elif ch == '/':
                        self.state = 16
                    elif ch == '=':
                        self.state = 20
                  
                    elif ch == '<':
                        self.state = 21
                  
                    elif ch == '>':
                        self.state = 31
                 
                    elif ch == '{':
                        self.state = 22
                        i -= 1
                    elif ch == '}':
                        self.state = 23
                        i -= 1
                    elif ch=='(':
                        self.state=32
                        i-=1
                    elif ch==')':
                        self.state=33
                        i-=1
                        
                    elif ch=='&':
                        self.state=34
                        i-=1
                    
                    elif ch=='|':
                        self.state=35
                        i-=1
                        
                    elif ch=='!':
                        self.state=42
                    
                        
                        
                        
                    
                    
                    elif ch == ';':
                        self.state = 24
                        i -= 1
                    elif ch.isspace():
                        self.state = 25
                    else:
                        self.state = 26 #不可识别
                        i -= 1
                        
                    if (i==line_length) and not(self.last=='begin' or self.last=='end' or self.last=='then' or self.last=='do' or ch=='{' or ch=='}' or self.last=='else'):  #一行中最后的一个单个字符单词不可直接识别
                        print('第',self.line_number,'行缺少;或)或}')
                        
                        
                
                elif self.state == 1: #判断字母数
                    while ch.isalpha() or ch.isdigit():
                        string += ch
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:       #ch读到了末尾字符
                            break
                    self.state = 2
                    i -= 2 #回退2个字符,回退到即将被归约的末尾字符
                elif self.state == 2: 
                    if string in self.ResWord:
                        content = ('gjz',string)
                    else:
                        content = ('bsf',string)
                    #print (content)
                    if string !='':
                        self.char_message.append(content)
                    self.last=string
                    string = '' #回到初始状态
                    self.state = 0
                
                elif self.state == 3: #判断数字
                    while ch.isdigit():
                        string += ch
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break
                    self.state = 4
                    i -= 2
                elif self.state == 4:
                    content = ('sz',string)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                
                elif self.state == 5: #遇加号
                    if ch == '+':
                        self.state = 6
                        i -= 1
                    elif ch == '=':
                        self.state = 7
                        i -= 1 
                    else:
                        self.state = 8
                        i -= 2
                elif self.state == 6: #判断++
                    content = ('tsfh',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 7: #判断+=
                    content = ('tsfh',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 8: #判断+
                    content = ('tsfh',ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                
                elif self.state == 9: #遇减号
                    if ch == '-':
                        self.state = 10
                        i -= 1
                    elif ch == '=':
                        self.state = 11
                        i -= 1 
                    else:
                        self.state = 12
                        i -= 2
                elif self.state == 10: #判断--
                    content = ('tsfh',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 11: #判断-=
                    content = ('tsfh',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 12: #判断-
                    content = ('tsfh','-')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                
                elif self.state == 13: #遇乘号
                    if ch == '=':
                        self.state = 14
                        i -= 1
                    else:
                        self.state = 15
                        i -= 2
                elif self.state == 14: #判断*=
                    content = ('tsfh',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 15: #判断*
                    content = ('tsfh',ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                
                elif self.state == 16: #遇除号
                    if ch == '/':
                        self.state = 17
                        i -= 1
                    elif ch == '=':
                        self.state = 18
                    else:
                        self.state = 19
                        i -= 2
                elif self.state == 17: #判断//
                    
                    content = ('zs', line[i:] )
            
                    self.annotate_message.append(content)
                    i=999
                    self.state=0
                    break
                elif self.state == 18: #判断/=
                    content = ('tsfh',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 19: #判断/
                    content = ('tsfh',ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                
                elif self.state==20:
                    if ch=='=':
                        self.state=40
                        i-=1
                    else:
                        self.state=41
                        i-=2
                        
                elif self.state==40:  #==
                    content = ('relop',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 41:#<
                    content = ('relop','=')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                    
                
                elif self.state==42:
                    if ch=='=':
                        self.state=43
                        i-=1
                    else:
                        self.state=26
                        i-=2
                 
                        
                elif self.state==43:  #!=
                    content = ('relop',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
         
                    
                    
                    
                elif self.state==21:
                    if ch=='=':
                        self.state=36
                        i-=1
                    else:
                        self.state=37
                        i-=2
                        
                elif self.state==36:  #<=
                    content = ('relop',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 37:#<
                    content = ('relop','<')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                
                
                
                
                
                elif self.state==31:
                    if ch=='=':
                        self.state=38
                        i-=1
                    else:
                        self.state=39
                        i-=2
                        
                elif self.state==38:  #>=
                    content = ('relop',string+ch)
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 39:#>
                    content = ('relop','>')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                    
                    
                    
                    
                elif self.state == 22:
                    content = ('tsfh','{')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 23:
                    content = ('tsfh','}')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                    
                    
                elif self.state == 32:
                    content = ('tsfh','(')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 33:
                    content = ('tsfh',')')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                 
                elif self.state == 34:
                    content = ('tsfh','&')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 35:
                    content = ('tsfh','|')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                    
                    
                    
                    
                elif self.state == 24:
                    content = ('tsfh',';')
                    self.char_message.append(content)
                    string = ''
                    self.state = 0
                elif self.state == 25:
                    while ch.isspace():
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break
                    self.state = 0
                    i -= 1
                
                elif self.state == 26: #不可识别字符
                    content = ( str(self.line_number),  ch )
                    self.error_message.append(content)
                    self.state= 0
                    string = ''
                
    def Get_error(self):#获取错误信息
        return self.error_message
    
    def Get_annotate(self):#获取注释信息
        return self.annotate_message
    
    def Get_char(self):#获取识别信息
        return self.char_message

if __name__ == '__main__':
    try:
        file_obj = open('input0.txt',encoding='utf-8')
        dfa = DFA(file_obj)
        dfa.start_convert()     #填满char_message
        dfa.get_symtable()
        content = dfa.Get_char()
        for item in content:
            print (item)
        print ("*************注释信息*************")
        content = dfa.Get_annotate()
        for item in content:
            print (item)
        print ("*************错误字符*************")
        content = dfa.Get_error()
        for item in content:
            print (item)
        print(dfa.symtable)

    finally:
        file_obj.close()
            
                    