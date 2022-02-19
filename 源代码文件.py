import os,shutil
import hashlib
import time
import sys
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog, messagebox
import subprocess
import webbrowser
import threading

window = tk.Tk()
window.title('Lor汉化')
window.geometry('800x460')
window.configure(background='white')

def Localization():

    ####变量设置####
    base_language = r'%s' %(Lan_choosen.get()) #读取游戏语言。如果你的基底语言为英语就使用名字为英语的汉化文件（如LocalizedText_ja_jp.bin）
    directory_game = r"%s" %(gamedir_entry.get().replace("/","\\"))
    start_game = r"%s" %(lorexeDir_entry.get().replace("/","\\"))
    chn_file = r"%s" %(LocalizeDir_entry.get().replace("/","\\")) #！！！读取汉化文件所在的目录，启动前自行修改名字文件名为基底语言的文件名，如英语就为：LocalizedText_ja_jp.bin
    print('settings: \n游戏语言：', base_language,'\n游戏语言目录：',directory_game,'\n游戏启动目录：',start_game,'\n汉化文件目录：',chn_file)
    
    directory_chn_file = directory_game + '\LocalizedText_'+base_language+'.bin'
    directory_chn_file = r"%s" %(directory_chn_file)
    print('\n游戏语言文件目录：',directory_chn_file)

    # chn_file_size = os.stat(chn_file)
    subprocess.call(['xcopy', chn_file, directory_game, '/y'])  #1 复制汉化文件到游戏的存放汉化文件的目录 
    # shutil.copy(chn_file,directory_game)   #1 复制汉化文件到游戏的存放汉化文件的目录 

    ####变量设置####

    ####启动游戏####
    # start_game_flag = 1 #是否通过python脚本启动游戏，默认为是

    # if start_game_flag == 1:
    #     f = os.popen(start_game)
    #     data = f.readlines()
    #     f.close()
    cmd = '"%s"' %start_game
    subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # os.system()

    ####启动游戏####

    ####md5检测算法####
    def hash(file_path,Bytes=1024):
        md5_1 = hashlib.md5()                        #创建一个md5算法对象
        with open(file_path,'rb') as f:              #打开一个文件，必须是'rb'模式打开
            while 1:
                data =f.read(Bytes)                  #由于是一个文件，每次只读取固定字节
                if data:                             #当读取内容不为空时对读取内容进行update
                    md5_1.update(data)
                else:                                #当整个文件读完之后停止update
                    break
        ret = md5_1.hexdigest()                      #获取这个文件的MD5值
        return ret
    ####md5检测算法####

    ####循环检查汉化文件是否被修改####
    a = 1
    animation = "|/-\\"
    while a < 2:#循环检查
        for i in range(len(animation)):
            time.sleep(0.1)
            hanhua_status.set("\r汉化中：" + animation[i % len(animation)])
            # sys.stdout.write("\r汉化中：" + animation[i % len(animation)])
            # sys.stdout.flush()
        if hash(chn_file)!=hash(directory_chn_file): #一旦检查到游戏的汉化文件和我们替换的汉化文件不相等（因为被游戏客户端修正了）
            os.remove(directory_chn_file)   #就移除掉被系统替换的汉化文件
                # hanhua_status2.set("\n正在将汉化文件从 %s  复制到 %s"%(chn_file, directory_game))
            print('\n正在将汉化文件从 ',chn_file, ' 复制到 ',directory_game)
            cmd2 = 'xcopy', chn_file, directory_game, '/y'
            subprocess.call(cmd2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #再次替换汉化文件到游戏的存放汉化文件的目录
            # shutil.copy(chn_file,directory_chn_file) #再次替换汉化文件到游戏的存放汉化文件的目录
            # print('tihuanchenggong')
            break  #退出Python脚本
    hanhua_status.set("汉化结束！")
    print("汉化结束！")
    
    ####循环检查汉化文件是否被修改####

    ####保存路径到txt文件####
    with open("preset_path.txt","w") as f:
        f.write(str(base_language) + '\n' + str(directory_game) + '\n' + str(start_game) + '\n' + str(chn_file))

# 查找本地的LoR.exe和GamePlayData文件夹
def search(path,name):
    print('未能找到先前预设路径，正在%s盘中寻找游戏目录...'%disk)
    # print('finding %s in %s'%(name,path))
    path = path +':/Riot Games/LoR/live/Game/'
    for root,dirs,files in os.walk(path,topdown=True):
        if name in dirs or name in files:
            print('找到了')
            # print(root)
            path_oput = str(root)+name
            print('已自动填写游戏路径：', path_oput.replace("/","\\"))
            return path_oput.replace("/","\\")
        else:
            return ""

### 获取文件(夹)路径 ###
def getGameDir(filename):
    fileDir=filedialog.askdirectory()
    if fileDir:
        print('%s：'%filename,fileDir)
        fileDir.replace("/","\\")
        gamedir_v.set(fileDir)
    return fileDir

def getLorexeDir(filename):
    filePath=filedialog.askopenfilename()
    if filePath:
        print('%s：'%filename,filePath)
        filePath.replace("/","\\")
        lorexeDir_v.set(filePath)
    return filePath

def getLocalizeDir(filename):
    filePath=filedialog.askopenfilename()
    if filePath:
        print('%s：'%filename,filePath)
        filePath.replace("/","\\")
        LocalizeDir_v.set(filePath)
        global loc_list
        for i in range(len(loc_list)):
            if loc_list[i] in filePath:
                Lan_choosen.current(i)
    return filePath

#弹窗
def confirm():
    base_language = r'%s' %(Lan_choosen.get())
    chn_file = r"%s" %(LocalizeDir_entry.get().replace("/","\\"))
    chn_file_language = chn_file[-9:-4]
    # print(chn_file_language) 
    if chn_file_language == base_language:
        threading.Thread(target=Localization).start()
    else:
        answer = tk.messagebox.askretrycancel('提示', '游戏语言与汉化文件不符，仍要执行此操作吗？')
        if answer:
            threading.Thread(target=Localization).start()

################ 交互窗口 ################
base_language, directory_game, start_game, chn_file = '','','',''
if os.path.exists("preset_path.txt"):
    try:
        paths = []
        for line in open("preset_path.txt","r"): #设置文件对象并读取每一行文件
            paths.append(line)
        base_language = paths[0].strip()
        directory_game = paths[1].strip()
        start_game = paths[2].strip()
        chn_file = paths[3] #！！！汉化文件所在的目录，启动前自行修改名字文件名为基底语言的文件名，如英语就为：LocalizedText_ja_jp.bin
        print('已加载上次汉化所设路径')
    except Exception:
        print('预设路径文件为空')
        for disk in ['C','D','E','F']:
            start_game = search(disk, 'LoR.exe')
            if start_game:
                directory_game = start_game.replace('Game\LoR.exe','PatcherData\PatchableFiles\GamePlayData')
                break
            else:
                print("未能找到游戏路径，请手动选择。")
else:
    print('无预设路径文件')
    for disk in ['C','D','E','F']:
        print('未能找到先前预设路径，正在%s盘中寻找游戏目录...'%disk)
        start_game = search(disk, 'LoR.exe')
        if start_game:
            directory_game = start_game.replace('Game\LoR.exe','PatcherData\PatchableFiles\GamePlayData')
            break
        else:
            print("未能找到游戏路径，请手动选择。")
header_label = tk.Label(window, text='Lor汉化程序', font=('楷体',15), height=3, width = 20, bg='white')
header_label.pack()

# 以下为 gamedir_frame 群组
gamedir_frame = tk.Frame(window, bg = 'white')
gamedir_frame.pack(side=tk.TOP)
gamedir_label = tk.Entry(gamedir_frame, textvariable = tk.StringVar(value='游戏自带语言文件所在目录（例：D:/Riot Games/LoR/live/PatcherData/PatchableFiles/GamePlayData）'), bg = 'white', state= 'readonly',readonlybackground='white', relief='flat', width=85)
gamedir_label.pack()
gamedir_v = tk.StringVar()
gamedir_v.set(directory_game)
gamedir_entry = tk.Entry(gamedir_frame, width=70, textvariable = gamedir_v)
gamedir_entry.pack(fill='y', side='left')
gamedir_btn = tk.Button(gamedir_frame, width=8, text='选择文件夹', command = lambda: getGameDir('游戏自带语言文件所在目录'))
gamedir_btn.pack(fill='x', padx=10)

# 以下为 lorexeDir_frame 群组
lorexeDir_frame = tk.Frame(window, bg = 'white')
lorexeDir_frame.pack(side=tk.TOP,pady=25)
lorexeDir_label = tk.Entry(lorexeDir_frame, textvariable = tk.StringVar(value='LoR.exe所在的目录（例：D:/Riot Games/LoR/live/Game/LoR.exe）'), bg = 'white', state= 'readonly',readonlybackground='white', relief='flat', width=85)
lorexeDir_label.pack()
lorexeDir_v = tk.StringVar()
lorexeDir_v.set(start_game)
lorexeDir_entry = tk.Entry(lorexeDir_frame, width=70, textvariable = lorexeDir_v)
lorexeDir_entry.pack(fill='y', side='left')
lorexeDir_btn = tk.Button(lorexeDir_frame, width=8, text='选择文件', command = lambda: getLorexeDir('lor.exe所在的目录'))
lorexeDir_btn.pack(fill='x', padx=10)

# 以下为 LocalizeDir_frame 群组
LocalizeDir_frame = tk.Frame(window, bg = 'white')
LocalizeDir_frame.pack(side=tk.TOP)
LocalizeDir_label = tk.Entry(LocalizeDir_frame, textvariable = tk.StringVar(value='简中汉化文件所在的目录（例：C:/Users/你的用户名/Downloads/LocalizedText_zh_tw.bin）'), bg = 'white', state= 'readonly',readonlybackground='white', relief='flat', width=85)
LocalizeDir_label.pack()
LocalizeDir_v = tk.StringVar()
LocalizeDir_v.set(chn_file)
LocalizeDir_entry = tk.Entry(LocalizeDir_frame, width=70, textvariable = LocalizeDir_v)
LocalizeDir_entry.pack(fill='y', side='left')
LocalizeDir_btn = tk.Button(LocalizeDir_frame, width=8, text='选择文件', command = lambda: getLocalizeDir('简中汉化文件所在的目录'))
LocalizeDir_btn.pack(fill='x', padx=10)

# 以下为语言选择模组
Lan_sele_frame = tk.Frame(window, bg = 'white')
Lan_sele_frame.pack(side=tk.TOP)
tk.Label(Lan_sele_frame, text = "选择当前游戏语言地区 :", relief='flat', bg = 'white').grid(column = 0,row = 5, padx = 10, pady = 25)
  
# Combobox creation 
loc_list = ['zh_tw','en_us','ja_jp','ko_kr','de_de','es_es','es_mx','fr_fr','it_it','pl_pl','pt_br','ru_ru','th_th','tr_tr','vi_vn']
n = tk.StringVar() 
Lan_choosen = ttk.Combobox(Lan_sele_frame, width = 10, textvariable = n) 
  
# Adding combobox drop down list 
Lan_choosen['values'] = loc_list
  
Lan_choosen.grid(column = 1, row = 5) 
for i in range(len(loc_list)):
    if base_language == loc_list[i]:
        Lan_choosen.current(i)

Localize_btn = tk.Button(window, text='汉化', font=('楷体',15), height=2, width = 10, command=confirm)
Localize_btn.pack()

# hanhua_status_str = StringVar()
# hanhua_status = tk.Entry(window, text="sada", bg='white',state= 'readonly',readonlybackground='white', relief='flat', font=('黑体',10))
# hanhua_status.pack()
# hanhua_status["text"]="assa"
hanhua_status_frame = tk.Frame(window, bg = 'white')
hanhua_status_frame.pack(side=tk.TOP)
hanhua_status = tk.StringVar()
hanhua_status.set(' ')
hanhua_status_entry = tk.Entry(hanhua_status_frame, width=70, textvariable = hanhua_status, bg = 'white', state= 'readonly',readonlybackground='white', relief='flat',justify='center')
hanhua_status_entry.pack()

website_label = tk.Label(window, text='  汉化教程：https://www.iyingdi.com/web/bbspost/detail/2356245 ', cursor = 'hand2', font=('黑体',10), bg='white')
website_label.pack(side='left')
programmer_label = tk.Label(window, text='营地：yx5932  ', font=('黑体',10), bg='white')
programmer_label.pack(side='right')

def open_url(event):
    webbrowser.open("https://www.iyingdi.com/web/bbspost/detail/2356245", new=0)

website_label.bind("<Button-1>", open_url)

window.mainloop()