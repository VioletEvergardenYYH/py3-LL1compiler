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
            wenfa.append('D -> int ID;D')
            if(table[self.i][0]=='bsf'):
                self.i += 1
                if(table[self.i][1] == ';'):
                    self.i += 1
                    self.d()
                else:
                    error[table[self.i][2]]='缺少分号'
                    
            else:
                 error[table[self.i][2]]='缺少id'
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
                error[table[self.i][2]]='缺少}'
        else:
            error[table[self.i][2]]='invalid syntax'

    def s(self): #S -> if (B) then S1 A S| while (B) do S1 S | {L} S | id = E;S | for(S;B;S) S1 S| read(id);S|write(id);S   |@
        if (table[self.i][1] == 'if'):
            self.i += 1
            wenfa.append('S -> if (B) then S1 A S ')
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
                        error[table[self.i][2]]='缺少then'
                else:
                    error[table[self.i][2]]='缺少)'
            else:
                error[table[self.i][2]]='缺少('
                       
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
                            error[table[self.i][2]]='缺少)'
                    else:
                        error[table[self.i][2]]='缺少;'
                else:
                    error[table[self.i][2]]='缺少;'
            else:
                error[table[self.i][2]]='缺少('
                    
                
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
                            error[table[self.i][2]]='缺少;'
                    else:
                        
                        error[table[self.i][2]]='缺少)'
                else:
                    error[table[self.i][2]]='缺少变量'
            else:
                error[table[self.i][2]]='缺少('
                
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
                            error[table[self.i][2]]='缺少;'
                    else:
                        
                        error[table[self.i][2]]='缺少)'
                else:
                    error[table[self.i][2]]='缺少变量'
            else:
                
                error[table[self.i][2]]='缺少('
                
        elif(table[self.i][1] == 'while'):
            self.i += 1
            wenfa.append('S -> while (B) do S1 S')
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
                        error[table[self.i][2]]='缺少do'
                else:
                    error[table[self.i][2]]='缺少)'
            else:
                error[table[self.i][2]]='缺少('
                        
        elif (table[self.i][1] == '{'):
            self.i += 1
            wenfa.append('S -> {L} S')
            self.l()
            if (table[self.i][1] == '}'):
                self.i += 1
                self.s()
            else:
                error[table[self.i][2]]='缺少}'
        
        elif  table[self.i][0] == 'bsf':
            temp=self.i
            if not(table[temp][1] in symtable.keys()):
                err.append('第'+str(table[temp][2])+'行:'+"变量表中无对应的变量"+table[temp][1])
            self.i += 1
            wenfa.append('S -> id = E; S')
            if (table[self.i][1] == '='):
                self.i += 1
                ret1=self.e()
                
                if (table[self.i][1] == ';'):
                    self.i += 1
                    siyuan.append(('=',ret1,'_',table[temp][1]))
                    self.s()
                else:
                    error[table[self.i][2]]='缺少;'
            else:
                error[table[self.i][2]]='缺少='
        else:
            wenfa.append('S->@')
            
    def a(self):
        if table[self.i][1]=='else':
            wenfa.append('A->else S1')
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
                if ret1=='0':
                    err.append('第'+str(table[self.i][2])+'行除数为0')
                return '/',ret1
            else:
                self.flag+=1
                
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
                error[table[self.i][2]]='缺少)'
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
            error[table[self.i][2]]='invalid syntax'
        
''' #预测分析表法
class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"LL(1)分析器", pos=wx.DefaultPosition,
                          size=wx.Size(460,327), style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL, name=u"Main")
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        
        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"请选择文法文件的位置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))
        
        fgSizer2.Add(self.m_staticText3, 0, wx.ALL, 5)
        
        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, wx.Size(300, -1),
                                                wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL)
        fgSizer2.Add(self.m_filePicker1, 0, wx.ALL, 5)
        
        bSizer1.Add(fgSizer2, 0, wx.EXPAND, 5)
        
        fgSizer4 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"请输入要分析的字符串", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        fgSizer4.Add(self.m_staticText4, 0, wx.ALL, 5)
        
        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.Size(200, -1), 0)
        str1 = self.m_textCtrl3.GetValue()
        
        fgSizer4.Add(self.m_textCtrl3, 0, wx.ALL, 5)
        
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"分析", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer4.Add(self.m_button3, 0, wx.ALL, 5)
        
        bSizer1.Add(fgSizer4, 0, wx.EXPAND, 5)
        
        fgSizer5 = wx.FlexGridSizer(0, 1, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.m_ListCtrl1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT, size=wx.Size(445, 210))
        self.m_ListCtrl1.InsertColumn(0, "分析栈")
        self.m_ListCtrl1.InsertColumn(1, "剩余输入串")
        self.m_ListCtrl1.InsertColumn(2, "所用产生式")
        self.m_ListCtrl1.InsertColumn(3, "动作")
        fgSizer5.Add(self.m_ListCtrl1, 0, wx.ALL, 5)
        
        bSizer1.Add(fgSizer5, 0, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.m_button3.Bind(wx.EVT_BUTTON, self.m_button3OnButtonClick)
        
    def __del__(self):
        pass
    
    def get_lan(self):#非终结符tab串1|串2|...
        file_path = self.m_filePicker1.GetPath()
        file = open(file_path, "r") #读文法文件
        for line in file.readlines():
          
            splitlist = line[2:].replace("\n", "").split("|")
            LAN[line[0]] = splitlist
           
    def get_first(self):
        for k in LAN:
            l = LAN[k]#列表
            FIRST[k] = list()
            for s in l:
                if not (s[0].isupper()): #终结符
                    FIRST[k].append(s[0])
        for i in range(2):
            for k in LAN:
                l = LAN[k]
                for s in l:
                    if (s[0].isupper()): #非终结符
                        FIRST[k].extend(FIRST[s[0]])
                        FIRST[k] = list(set(FIRST[k]))# 去重
        print ("文法为: %s" % LAN)
        print ("FIRST集为：%s" % FIRST)
        
    def get_follow(self):
        condition = lambda t: t != 'ε'  # 过滤器用于过滤空串
        for k in LAN: #新建list
            FOLLOW[k] = list()
            if k == list(LAN.keys())[0]:
                FOLLOW[k].append('#')
        for i in range(2):
            for k in LAN:
                l = LAN[k]
                for s in l:
                    if s[len(s) - 1].isupper():
                        FOLLOW[s[len(s) - 1]].extend(FOLLOW[k]) # 若A→αB是一个产生式，则把FOLLOW(A)加至FOLLOW(B)中
                        FOLLOW[s[len(s) - 1]] = list(filter(condition, FOLLOW[s[len(s) - 1]]))  # 去除空串
                    for index in range(len(s) - 1):
                        if s[index].isupper():
                            if s[index + 1].isupper():# 若A→αBβ是一个产生式，则把FIRST(β)\{ε}加至FOLLOW(B)中；
                                FOLLOW[s[index]].extend(FIRST[s[index + 1]])
                                FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))# 去除空串
                            if not (s[index + 1].isupper()) and (s[index + 1] != 'ε'):
                                FOLLOW[s[index]].append(s[index + 1])
                            emptyflag = 1
                            for i in range(index + 1, len(s)):
                                if not (s[i].isupper()) or (s[i].isupper() & ('ε' not in FIRST[s[i]])):
                                    emptyflag = 0
                                    break
                            if emptyflag == 1:
                                FOLLOW[s[index]].extend(FOLLOW[k])  # A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中
                                FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串
        for k in FOLLOW: #去重
            FOLLOW[k] = list(set(FOLLOW[k]))
        print('FOLLOW集为：%s' % FOLLOW)
        
    def get_VT(self):
        VT.add('#')
        for l in LAN.values():
            for s in l:
                for c in s:
                    if not (c.isupper()) and (c != 'ε'): VT.add(c)
        print('终结符为：%s' % VT)
        
    def generate_table(self):
        self.get_VT()
        for k in LAN: # 初始化分析表
            Table[k] = dict()
            for e in VT:
                Table[k][e] = None
        
        for k in LAN:
            l = LAN[k]
            for s in l:
                if s[0].isupper():
                    for e in VT:
                        if e in FIRST[s[0]]: Table[k][e] = s
                if s[0] in VT:
                    Table[k][s[0]] = s
                if (s[0].isupper() and ('ε' in FIRST[s[0]])) or (s == 'ε'):
                    for c in FOLLOW[k]:
                        Table[k][c] = s
        print('分析表为：%s' % Table)
        
    def analyze(self):
        inputstr = self.m_textCtrl3.GetValue()  # 输入任意字符串
        inputstr = inputstr[1:]
        inputstr = list(inputstr[::-1])
        print (inputstr)
        process = list()
        process.append('#') # #入栈
        process.append(list(LAN.keys())[0]) #开始符入栈
        errorflag = 0
        count = 0 #输入列表时的索引
        ProcessList.clear()
        ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', '初始化')
        while True:
            count += 1
            current = process.pop()
            if current == inputstr[-1] == '#': #分析成功结束
                ProcessList[count] = ('√', '√', '恭喜你', '成功')
                break;
            
            if (current in VT) and (current == inputstr[-1]): # 遇到终结符
                inputstr.pop()
                ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', 'GETNEXT')
                continue
            
            if inputstr[-1] in VT: # 判断是不是终结符
                new = Table[current][inputstr[-1]]
            else:
                errorflag = 1
                ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', 'Error:输入不合法！')
                break
            if (new == None): # 没有找到对应产生式
                errorflag = 1
                ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', 'Error:没有找到对应产生式!')
                break
            if (new == 'ε'):  # 产生式为空串
                ProcessList[count] = (''.join(process), ''.join(inputstr), current+'->ε', 'POP')
                continue
            
            for c in reversed(new): # 将产生式入栈
                process.append(c)
            ProcessList[count] = (''.join(process), ''.join(inputstr), current+'->'+''.join(new), 'POP,PUSH')
            
        if errorflag == 0:
            print("分析成功！")
        else:
            print("分析失败！")
            
        items = ProcessList.items()
        self.m_ListCtrl1.DeleteAllItems()
        for key, data in items:
            index = self.m_ListCtrl1.InsertItem(self.m_ListCtrl1.GetItemCount(), str(key))
            self.m_ListCtrl1.SetItem(index, 0, data[0])
            self.m_ListCtrl1.SetItem(index, 1, data[1])
            self.m_ListCtrl1.SetItem(index, 2, data[2])
            self.m_ListCtrl1.SetItem(index, 3, data[3])
            self.m_ListCtrl1.SetColumnWidth(0, 80)
            self.m_ListCtrl1.SetColumnWidth(1, 80)
            self.m_ListCtrl1.SetColumnWidth(2, 100)
            self.m_ListCtrl1.SetColumnWidth(3, 175)
    
    def m_button3OnButtonClick(self, event):
        self.get_lan()  # 得到文法
        self.get_first()  # 得到FIRST集
        self.get_follow()  # 得到FOLLOW集
        self.generate_table()  # 得到分析表
        self.analyze()  # 对输入字符串进行分析
'''

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
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] < symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) < int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] < int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) < symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
                
            
            symtable[siyuan[i][3]] = t
            i+=1
        elif siyuan[i][0] == '<=':
            
            
            if siyuan[i][1] in symtable.keys() and siyuan[i][2] in symtable.keys():
                if symtable[siyuan[i][1]] <= symtable[siyuan[i][2]]:
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and not(siyuan[i][2] in symtable.keys()):
                if int(siyuan[i][1]) <= int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif siyuan[i][1] in symtable.keys() and not(siyuan[i][2] in symtable.keys()):
                if symtable[siyuan[i][1]] <= int(siyuan[i][2]):
                    t = 1
                else:
                    t = 0
            elif not(siyuan[i][1] in symtable.keys()) and siyuan[i][2] in symtable.keys():
                if int(symtable[siyuan[i][1]]) <= symtable[siyuan[i][2]]:
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
        file_obj = open('input1.txt',encoding='utf-8')
       
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
    if dfa.flag==0:
        Parser()
    print ("*************语法错误*************")
    print(error)
    print ("*************语义错误*************")
    print(err)
    print ("*************中间代码*************")
    for i in siyuan:
        print(i)
    print ("*************解释程序*************")

    if not(len(err)) and not(len(error)):
        
        explain(symtable)
        print(symtable)

    print ("*************中间代码执行过程*************")
    print(process)
    file_obj.close()
            