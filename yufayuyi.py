# -*- coding: utf-8 -*-
'''
基本文法：
P ->  begin DS end
D -> int id; D|@
S -> if (B) then S1 A S| while (B) do S1 S | {L} S | id = E;S | for(S;B;S) S1 S| read(id);S|write(id);S   |@
S1->{L}
A -> else S1 |@
L -> SH
H -> L|@
B -> B1B2
B1 -> B3B4
B2 -> '|'B1B2|@
B4 -> &B3B4|@
B3 -> E Q
Q -> relop E|@
E -> E1E2
E2 -> +E1E2|-E1E2|@
E1 -> FE3
E3 -> *FE3|/FE3|@
F -> (E)|num|id 
'''



from cifa import DFA
dic = {}   #符号表
table = []   #单词栈
wenfa = []   #字符串文法
siyuan = []  #四元式
error = {}#语法错误
err=[]#语义错误
process=[]#中间代码执行过程
class Parser():
    def __init__(self):
        self.i=0
        self.flag=0#记录临时变量的数目
        self.lb=0#记录标签的数目
        self.p()
    def p(self): #P -> begin DS end
        if (table[self.i][1] == 'begin'):
            self.i += 1
            wenfa.append('P -> begin DS end')
            self.d()
            self.s()
            '''
            if(table[self.i][1] != 'end'):
                raise Exception
            self.i+=1
            '''
        if (self.i is not len(table)-1):   #语法分析结束时，若单词栈指针与单词表长度不相等，报错
            print ("\n语法分析程序检查到错误")
            print(table[self.i])#识别终止位置
            for key in wenfa:
                print (key)
           
        else:
            print ('\n字符串语法是：')       #若一切正确，则输出语法树文法
            for key in wenfa:
                print (key)
            print ('语法正确')
    def d(self): #D -> int ID; D|&
        if (table[self.i][1] == 'int'):
            self.i += 1
            wenfa.append('D -> int ID;')
            if(table[self.i][0]=='bsf'):
                self.i += 1
                if(table[self.i][1] == ';'):
                    self.i += 1
                    self.d()
                else:
                    error[self.i]='缺少分号'
                    
            else:
                 error[self.i]='缺少id'
        else:
            wenfa.append('D -> @')
            
            
    def s1(self):#S1->{L}
        if table[self.i][1] == '{':
            
            self.i+=1
            wenfa.append('S1->{L}')
            self.l()
            if table[self.i][1] == '}':
                self.i+=1
            else:
                error[i]='缺少}'
        else:
            error[i]='invalid syntax'
            
    
    
    
    
    
    def s(self): #S -> if (B) then S A| while (B) do S | {L} S;S;S; | ID = E;
        if (table[self.i][1] == 'if'):
            self.i += 1
            wenfa.append('S -> if (B) then S ')
            if(table[self.i][1] == '('):
                self.i += 1          
                ret1=self.b()
                if(table[self.i][1] == ')'):
                    self.i += 1
                    if table[self.i][1] == 'then':
                        self.i += 1             
                        self.lb+=1
                        temp1=self.lb
                        self.lb+=1
                        temp2=self.lb
                        siyuan.append(('JZ',ret1,'_','label'+str(temp1)))
                        self.s1()
                        
                        self.lb+=1
                        siyuan.append(('JP','_','_','label'+str(temp2)))
                       
                        siyuan.append('label'+str(temp1))
                        self.a()
                        siyuan.append('label'+str(temp2))
                        self.s()
                    else:
                        error[self.i]='缺少then'
                else:
                    error[self.i]='缺少)'
            else:
                error[self.i]='缺少('
                       
        elif(table[self.i][1] == 'for'):
            self.lb+=1
            temp1=self.lb
            self.lb+=1
            temp2=self.lb
          
            self.lb+=1
            temp4=self.lb
            self.lb+=1
            temp5=self.lb
            self.i+=1
            wenfa.append('S -> for(S;B;S) S1 S')
            if table[self.i][1] == '(':
                self.i+=1
                self.s()
                if table[self.i][1] == ';':
                    self.i+=1
                    siyuan.append('label'+str(temp5))
                    ret1=self.b()
                    siyuan.append(('JZ',ret1,'_','label'+str(temp1)))
                    siyuan.append(('JP','_','_','label'+str(temp2)))
                    siyuan.append('label'+str(temp4))
                    if table[self.i][1] == ';':
                        self.i+=1
                        self.s()
                        siyuan.append(('JP','_','_','label'+str(temp5)))
                        siyuan.append('label'+str(temp2))
                        if table[self.i][1] == ')':
                            self.i+=1
                            self.s1()
                            siyuan.append(('JP','_','_','label'+str(temp4)))
                            siyuan.append('label'+str(temp1))
                            self.s()
                        else:
                            error[i]='缺少)'
                    else:
                        error[i]='缺少;'
                else:
                    error[i]='缺少;'
            else:
                error[i]='缺少('
                    
                
        elif(table[self.i][1] == 'read'):
            self.i += 1
            wenfa.append('S -> read(id); S')
            if table[self.i][1]=='(':
                self.i+=1
                if table[self.i][0]=='bsf':
                    siyuan.append(('read','_','_',table[self.i][1]))
                    self.i+=1
                    if table[self.i][1]==')':
                        self.i+=1
                        if table[self.i][1]==';':
                            self.i+=1
                            self.s()
                        else:
                            error[i]='缺少;'
                    else:
                        
                        error[i]='缺少)'
                else:
                    error[i]='缺少变量'
            else:
                error[i]='缺少('
                
        elif(table[self.i][1] == 'write'):
            self.i += 1
            wenfa.append('S -> write(id); S')
            
            if table[self.i][1]=='(':
                self.i+=1
                if table[self.i][0]=='bsf':
                    siyuan.append(('write','_','_',table[self.i][1]))
                    self.i+=1
                    if table[self.i][1]==')':
                        self.i+=1
                        if table[self.i][1]==';':
                            self.i+=1
                            self.s()
                        else:
                            error[i]='缺少;'
                    else:
                        
                        error[i]='缺少)'
                else:
                    error[i]='缺少变量'
            else:
                
                error[i]='缺少('
                
                
                
                
                
        elif(table[self.i][1] == 'while'):
            self.i += 1
            wenfa.append('S -> while (B) do S')
            if(table[self.i][1] == '('):
                self.i += 1      
                self.lb+=1
                temp1=self.lb
                siyuan.append('label'+str(self.lb))
                ret1=self.b()
                self.lb+=1
                temp2=self.lb
      
                siyuan.append(('JZ',ret1,'_','label'+str(temp2)))
                if(table[self.i][1] == ')'):
                    self.i += 1
                    
                    if table[self.i][1] == 'do':
                        self.i += 1
                        self.s1()
                        siyuan.append(('JP','_','_','label'+str(temp1)))
                        siyuan.append('label'+str(temp2))
                        self.s()
                    else:
                        error[self.i]='缺少do'
                else:
                    error[self.i]='缺少)'
            else:
                error[self.i]='缺少('
                        
        elif (table[self.i][1] == '{'):
            self.i += 1
            wenfa.append('S -> {L}')
            self.l()
            if (table[self.i][1] == '}'):
                self.i += 1
                self.s()
            else:
                error[self.i]='缺少}'
        
        elif  table[self.i][0] == 'bsf':
            temp=self.i
            if not(table[temp][1] in symtable.keys()):
                err.append("变量表中无对应的变量"+table[temp][1])
            self.i += 1
            wenfa.append('S -> id = E')
            if (table[self.i][1] == '='):
                self.i += 1
                ret1=self.e()
                
                if (table[self.i][1] == ';'):
                    self.i += 1
                    siyuan.append(('=',ret1,'_',table[temp][1]))
                    self.s()
                else:
                    error[self.i]='缺少;'
            else:
                error[self.i]='缺少='
            
        
            
        else:
            wenfa.append('S->@')
            
    def a(self):
        if table[self.i][1]=='else':
            wenfa.append('A->else S')
            self.i+=1
            self.s1()
            
        else:
            wenfa.append('A-> @')
        
        
        
        
    def l(self): #L -> SH
        wenfa.append('L -> SH')
        self.s()
        self.h()
    def h(self): #H -> L|@
        if (table[self.i][1] == 'if' or table[self.i][1] == 'while' or table[self.i][1] == '{' or table[self.i][0] == 'bsf'):        
            wenfa.append('H -> L')
            self.l()
            
        else:
            wenfa.append('H -> @')
    
    def b(self):   #B -> B1B2
        wenfa.append('B -> B1B2')
        ret1=self.b1()
        ret2,ret3=self.b2()
        if ret2=='@':
            return ret1
        else:
            self.flag+=1
            siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
            return 'T'+str(self.flag)
    def b1(self):   #B1 -> B3B4
        wenfa.append('B1 -> B3B4')
        ret1=self.b3()
        ret2,ret3=self.b4()
        if ret2=='@':
            return ret1
        else:
            self.flag+=1
            siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
            return 'T'+str(self.flag)
    def b2(self):   #B2 -> |B1B2|@
        if (table[self.i][1] == '|'):
            self.i += 1
            wenfa.append('B2 -> |B1B2')
            ret1=self.b1()
            ret2,ret3=self.b2()
            if ret2=='@':
                return ret1
            else:
                self.flag+=1
                siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
                return '|','T'+str(self.flag)
         
        else:
            wenfa.append('B2 -> @')
            return '@','@'
      
    def b3(self):   #B3 -> E Q
        wenfa.append('B3 -> E Q')
        ret1=self.e()
        ret2,ret3=self.q()
        if ret2=='@':
                return ret1
        else:
            self.flag+=1
            siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
            return 'T'+str(self.flag)
        
        
        
        
        
        
        
    def b4(self):   #B4 -> &B3B4 | @
        if (table[self.i][1] == '&'):
            self.i += 1
            wenfa.append('B4 -> &B3B4')
            ret1=self.b3()
            ret2,ret3=self.b4()
            if ret2=='@':
                return '&',ret1
            else:
                self.flag+=1
                siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
                return '&','T'+str(self.flag)
        else:
            wenfa.append('B4 -> @')
            return '@','@'
    
    def q(self):   #Q -> relop E | @
        if (table[self.i][0] == 'relop'):
            ret1=table[self.i][1]   #运算符号
            wenfa.append('Q -> relop E')
            self.i += 1
            
            ret2=self.e()
            return ret1,ret2
            
            
            
        else:
            wenfa.append('Q -> @')
            return '@','@'
       
        
    def e(self): #E -> e1e2
        wenfa.append('E -> E1E2')
        ret1=self.e1()
        ret2,ret3=self.e2()
        if ret2!='@':
            self.flag+=1
            siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
            return 'T'+str(self.flag)
        else:
            return ret1
        
        
    def e1(self): #E1->FE3
        wenfa.append('E1 -> FE3')
        ret1=self.f()
        ret2,ret3=self.e3()
        if ret2!='@':
            self.flag+=1
            siyuan.append((ret2,ret1,ret3,'T'+str(self.flag)))
            return 'T'+str(self.flag)
        else:
            return ret1
        
        
    def e2(self):#E2->+E1E2/-E1E2/@
        if table[self.i][1] == '+':
            self.i+=1
            wenfa.append('E2->+E1E2')
            ret1=self.e1()
            ret2,ret3=self.e2()
            if ret2=='@':
                return '+',ret1
            else:
                self.falg+=1
                siyuan.append(('+',ret1,ret3,'T'+str(self.flag)))
                return '+','T'+str(self.flag)
        elif table[self.i][1] == '-':
            self.i+=1
            wenfa.append('E2->-E1E2')
            ret1=self.e1()
            ret2,ret3=self.e2()
            if ret2=='@':
                return '-',ret1
            else:
                self.falg+=1
                siyuan.append(('-',ret1,ret3,'T'+str(self.flag)))
                return '-','T'+str(self.flag)
        else:
            wenfa.append('E2->@')
            return '@','@'
            
    def e3(self):#E3->*FE3//FE3/@
        if table[self.i][1] == '*':
            self.i+=1
            wenfa.append('E3->*FE3')
            ret1=self.f()
            ret2,ret3=self.e3()
            if ret2=='@':
                return '*',ret1
            else:
                self.flag+=1
                siyuan.append(('*',ret1,ret3,'T'+str(self.flag)))
                return '*','T'+str(self.flag)
            
        elif table[self.i][1] == '/':
            self.i+=1
            wenfa.append('E3->/FE3')
            ret1=self.f()
            ret2,ret3=self.e3()
            if ret2=='@':
                return '/',ret1
            else:
                self.flag+=1
                if ret3==0:
                    err.append(str(i)+'处除数为0')
                siyuan.append(('/',ret1,ret3,'T'+str(self.flag)))
                return '/','T'+str(self.flag)
        else:
            wenfa.append('E3->@')
            return '@','@'
            
            
    def f(self):#F -> (E)|num|id 
        if table[self.i][1]=='(':
            self.i+=1
            wenfa.append('F->(E)')
            ret1=self.e()
            if table[self.i][1]==')':
                self.i+=1
            else:
                error[self.i]='缺少)'
            return ret1
                
        elif table[self.i][0]=='sz':
            self.i+=1
            wenfa.append('F->num')
            return table[self.i-1][1]
            
        elif table[self.i][0]=='bsf':
            
            self.i+=1
            wenfa.append('F->id')
            return table[self.i-1][1]
            
        else:
            error[self.i]='invalid syntax'
        
def explain(symtable):
    i=0
    while i<len(siyuan):
        process.append(i)
        if type(siyuan[i])==str:  #遇到标签
            i+=1
            
            
            
        elif siyuan[i][0] == '=':
            if siyuan[i][3] in symtable.keys():
                
                if siyuan[i][1] in symtable.keys():
                    symtable[siyuan[i][3]] = int(symtable[siyuan[i][1]])
                else:
                    symtable[siyuan[i][3]] = int(siyuan[i][1])
                i=i+1
            else:
                err.append("变量表中无对应的变量"+siyuan[i][3])
                i+=1
        
        
        elif siyuan[i][0] == 'read':
            if siyuan[i][3] in symtable.keys():
                temp=int(input("请为"+siyuan[i][3]+'赋值:'))
                symtable[siyuan[i][3]]=temp
                i+=1
            else:
                err.append("变量表中无对应的变量"+siyuan[i][3])
                i+=1
        elif siyuan[i][0] == 'write':
        
            if siyuan[i][3] in symtable.keys():
          
                print(siyuan[i][3]+'='+str(symtable[siyuan[i][3]]))
                i+=1
            else:
                err.append("变量表中无对应的变量"+siyuan[i][3])
                i+=1
        
                
                
        elif siyuan[i][0]=='+':
            if siyuan[i][1] in symtable.keys():
                a = int(symtable[siyuan[i][1]])
            else:
                a = int(siyuan[i][1])
            if siyuan[i][2] in symtable.keys():
                b = int(symtable[siyuan[i][2]])
            else:
                b = int(siyuan[i][2])
            symtable[siyuan[i][3]] = a + b
            i=i+1
            
            
            
        elif siyuan[i][0] == '-':
            if siyuan[i][1] in symtable.keys():
                a = int(symtable[siyuan[i][1]])
            else:
                a = int(siyuan[i][1])
            if siyuan[i][2] in symtable.keys():
                b = int(symtable[siyuan[i][2]])
            else:
                b = int(siyuan[i][2])
            symtable[siyuan[i][3]] = a - b
            i+=1
        elif siyuan[i][0] == '*':
            if siyuan[i][1] in symtable.keys():
                a = int(symtable[siyuan[i][1]])
            else:
                a = int(siyuan[i][1])
            if siyuan[i][2] in symtable.keys():
                b = int(symtable[siyuan[i][2]])
            else:
                b = int(siyuan[i][2])
            symtable[siyuan[i][3]] = a * b
            i+=1
        elif siyuan[i][0] == '/':
            if siyuan[i][1] in symtable.keys():
                a = float(symtable[siyuan[i][1]])
            else:
                a = float(siyuan[i][1])
            if siyuan[i][2] in symtable.keys():
                b = float(symtable[siyuan[i][2]])
            else:
                b = float(siyuan[i][2])
          
            symtable[siyuan[i][3]] = a / b
            i+=1
        elif siyuan[i][0] == '<':
            if symtable[siyuan[i][1]] < symtable[siyuan[i][2]]:
                t = 1
            else:
                t = 0
            symtable[siyuan[i][3]] = t
            i+=1
        elif siyuan[i][0] == '<=':
            if symtable[siyuan[i][1]] <= symtable[siyuan[i][2]]:
                t = 1
            else:
                t = 0
            symtable[siyuan[i][3]] = t
            i+=1
        elif siyuan[i][0] == '>':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] > symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) > int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] > int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) > symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
            
            
            
        elif siyuan[i][0] == '&':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] and symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) and int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] and int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) and symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
            
            
            
            
        elif siyuan[i][0] == '|':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] or symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) or int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] or int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) or symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
        elif siyuan[i][0] == '>=':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] >= symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) >= int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] >= int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) >= symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
            
            
        elif siyuan[i][0] == '!=':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] != symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) != int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] != int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) != symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
            
            
        elif siyuan[i][0] == '==':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] == symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and  not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) == int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] == int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) == symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
        elif siyuan[i][0] == "JZ":
          
            if siyuan[i][1] in symtable.keys():
                if symtable[siyuan[i][1]] == 0:
                    
                    i = siyuan.index(siyuan[i][3])
                    i+=1
                else:
                    i+=1
            else:
                err.append("变量表中无对应的变量"+siyuan[i][1])
                i+=1
        elif siyuan[i][0] == "JP":
            i = siyuan.index(siyuan[i][3]) 
            i+=1
if __name__ == '__main__':
    try:
        file_obj = open('input3.txt',encoding='utf-8')
       
    except Exception:
        print(file_obj, ': This FileName Not Found!')
        

         
    dfa = DFA(file_obj)
    dfa.start_convert()     #填满char_message
    symtable=dfa.get_symtable()  #初始变量表
    table = dfa.Get_char()   #符号栈
    for item in table:
        print (item)
    print ("*************注释信息*************")
    content = dfa.Get_annotate()
    for item in content:
        print (item)
    print ("*************错误字符*************")
    content = dfa.Get_error()
    for item in content:
        print (item)
    print ("*************初始变量表*************")
    print(dfa.symtable)
    print ("*************语法分析*************")
    Parser()
    print ("*************语法错误*************")
    print(error)
    print ("*************中间代码*************")
    for i in siyuan:
        print(i)
    print ("*************解释程序*************")
    if not(len(err)):
        
        explain(symtable)
        print(symtable)
    print ("*************语义错误*************")
    print(err)
    print ("*************中间代码执行过程*************")
    print(process)
    file_obj.close()
            