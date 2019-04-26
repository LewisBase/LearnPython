# -*- coding: utf-8 -*- 
import list as lt 
from random import randint

class Novice_Village(object):
    def __init__(self):
        print("欢迎来到白色路理工大学，请输入以下信息完成你的注册")
        self.start='register'
    
    def register(self):
        self.name=input("姓名:\n")
        self.gender=input("性别:\n")
        self.age=input("年龄:\n")
        while True:
            id=randint(1000000,1009999)
            if id not in lt.matesid:
                self.id=id
                break
        print(f"恭喜！{self.name}注册成功！")
        if self.gender in lt.gender_male:
            print(f"{self.name}是一名{self.age}岁的男同学。")
            print(f"学号：{self.id}")
            return 'doom_mate'
        elif self.gender in lt.gender_female:
            print(f"{self.name}是一名{self.age}岁的女同学。")
            print(f"学号：{self.id}")
            return 'doom_mate'
        else:
            print(f"{self.name}是一名{self.age}岁的{self.gender}同学。")
            print(f"学号：{self.id}")
            return 'doom_mate'

    def doom_mate(self):
        if self.gender in lt.gender_female:
            lt.dfdoommates['性别']="女"
        print("这是你的四个室友：\n")
        parter=lt.dfdoommates
        print(parter)
        print("你是否想更换室友？")
        change_mate=input("作出正确的选择把！输入是或否：\n")
        if change_mate == "是":
            print("你可真是个事儿逼，第一天来有啥好挑的。")
            print("不过没办法，为了假装我们学校很尊重你的人权，我还是得让你选。")
            print("就一个名额，你看你要换谁吧。")
            print("A.王朝 B.马汉 C.张龙 D. 赵虎")
            choose=input("选吧，写汉字啊，本学校不识别鸟语。\n")
            lt.dfdoommates=lt.dfdoommates[~lt.dfdoommates['姓名'].isin([choose])]
            lt.dfdoommates=lt.dfdoommates.append(lt.matealternate)
            print("看好了，这是你的新室友，不能再换了。")
            print(lt.dfdoommates)
            r=randint(0,len(lt.abj)-1)
            print(f"OK，准备开始你{lt.abj[r]}大学生活吧！")
            return 'doom_live'
        elif change_mate == "否":
            r=randint(0,len(lt.abj)-1)
            print(f"OK，准备开始你{lt.abj[r]}的大学生活吧！")
            return 'doom_live'
        else:
            print("年轻人，听不懂人话吗？是或否，不要浪费时间！")
            return 'doom_mate'

    def doom_live(self):
        print("你找到了你的宿舍，此时，其他几个室友已经就位了......")
        if "张龙" not in lt.dfdoommates.姓名.values:
            print('赵虎走上来根你说："你居然敢把我兄弟换走，看我不揍死你！"')
            fight()
        elif "赵虎" not in lt.dfdoommates.姓名.values:
            print('张龙走上来根你说："你居然敢把我兄弟换走，看我不揍死你！"')
            fight()
        elif "王朝" not in lt.dfdoommates.姓名.values:
            print('马汉走上来根你说："你居然敢把我兄弟换走，看我不揍死你！"')
            fight()
        elif "马汉" not in lt.dfdoommates.姓名.values:
            print('王朝走上来根你说："你居然敢把我兄弟换走，看我不揍死你！"')
            fight()
        else:
            print('但是王朝马汉，张龙赵虎互相之间都已经很熟悉了。并没有人来搭理你。')
            exit(1)


def fight():
    decision=input('要不要干他娘的一炮呢？')
    if decision in lt.positive:
        print(f"你也不甘示弱，并使出了一招{lt.kongfu[randint(0,len(lt.kongfu)-1)]}")
        win=randint(0,1)
        if win == 0:
            print("你把人打死啦！！！")
            print("你被警察带走了，大学生涯从此结束......")
            exit(1)
        else:
            print("不会功夫还装什么装！你被人打死啦！！！")
            print("你被殡仪馆带走了，大学生涯从此结束......")
            exit(1)
    elif decision in lt.negitive:
        print("他们觉得你太怂了，还是揍了你。\n哎呀！你被人打死啦！！！")
        print("你被殡仪馆带走了，大学生涯从此结束......")
        exit(1)
    else:
        print("没人听得懂你的胡言乱语，大家觉得你是个怪胎，就放过你了。")
        exit(1)

#test=Novice_Village()
#test.doom_mate()
