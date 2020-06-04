#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by shanfenglan on 2020/5/27
import curses,random,time,sys,re
#Todo 技能模块。




def game():
    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_GREEN) # initialize the color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)


    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    curses.noecho()
    w.noutrefresh()
    # w.timeout(150)

    bonus = []

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [[snk_y, snk_x]]
    snakee = [[snk_y, snk_x]]
    food = [sh // 2, sw // 2]
    score=3

    cishu = 0

    damage = 7
    defence = 7
    hp = int(100)
    master_defence = 1
    master_damage = 1
    master_hp = 1
    master_skill = '无'
    rank = 1
    flagg = 0
    baoxiang1=[sh // 8,sw // 4]
    baoxiang2=[sh // 8,(sw // 4)*2]
    baoxiang3=[sh // 8,(sw // 4)*3]

    flag4 = 0
    # def zhandoukuang(char):
    #     pad = curses.newpad(sh, sw)
    #     pad.bkgd(curses.color_pair(1))
    #     pad.addstr(1, 1, char)
    #     pad.refresh(0, 0,sh // 2, sw // 2 - 6, (sh // 2)+2, (sw // 2)+4)
    #     w.getch()
    #     pad = curses.newpad(sh, sw)
    #     pad.bkgd(' ', curses.color_pair(3))
    #     pad.refresh(0, 0,sh // 2, sw // 2 - 6, (sh // 2)+2, (sw // 2)+4)

    def initial():
        if rank % 3 != 0:
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
        else:
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
        w.addstr(0, 0, '金币：{0}    攻击力：{1}   防御力：{2}   生命值：{3}  关卡：{4}'.format(score, damage, defence, str(hp) + ' ', rank))
        w.addch(snake[0][0], snake[0][1], curses.ACS_SSSS, curses.color_pair(1))

    def shouye():
        pad = curses.newpad(sh, sw)
        pad.bkgd(' ', curses.color_pair(1))
        pad.addstr(sh // 8, sw // 6,'''
                             _        
             _ __ ___   ___ | |_ __ _ 
            | '_ ` _ \ / _ \| __/ _` |
            | | | | | | (_) | || (_| |
            |_| |_| |_|\___/ \__\__,_| 
     
     
     
             魔塔 v1.0    z键打开帮助面板             
                通关条件： 通过30关
        ''',curses.A_BLINK)
        pad.refresh(0, 0,sh // 8, sw // 6, (sh // 8)*7, (sw // 6)*5)
        w.getch()
        pad = curses.newpad(sh, sw)
        pad.bkgd(' ',curses.color_pair(3))
        pad.refresh(0, 0,sh // 8, sw // 6, (sh // 8)*7, (sw // 6)*5)
        initial()
    shouye()
    def choujiangkuang_delete(charstr):
        pad = curses.newpad(sh, sw)
        pad.bkgd(' ', curses.color_pair(3))
        pad.refresh(0, 0, baoxiang1[0], baoxiang1[1], baoxiang1[0] + 4, baoxiang1[1] + 12)
        pad.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 4, baoxiang2[1] + 12)
        pad.refresh(0, 0, baoxiang3[0], baoxiang3[1], baoxiang1[0] + 4, baoxiang3[1] + 12)

        if charstr != None:
            pad = curses.newpad(sh, sw)
            pad.bkgd(' ', curses.color_pair(1))
            pad.addstr(0, 0, charstr, curses.A_BLINK)
            pad.refresh(0, 0, baoxiang1[0], baoxiang1[1], baoxiang1[0], baoxiang1[1] + 42)
            w.getch()
            pad = curses.newpad(sh, sw)
            pad.bkgd(' ', curses.color_pair(3))
            pad.refresh(0, 0, baoxiang1[0], baoxiang1[1], baoxiang1[0], baoxiang1[1] + 42)
        if rank % 3 != 0:
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
        else:
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
    def choujiangkuang_appear():
        pad = curses.newpad(sh, sw)
        pad.bkgd(' ', curses.color_pair(1))
        pad.addstr(2, 4, '宝箱1', curses.A_BLINK)
        pad.refresh(0, 0, baoxiang1[0], baoxiang1[1], baoxiang1[0] + 4, baoxiang1[1] + 12)
        pad.addstr(2, 4, '宝箱2', curses.A_BLINK)
        pad.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 4, baoxiang2[1] + 12)
        pad.addstr(2, 4, '宝箱3', curses.A_BLINK)
        pad.refresh(0, 0, baoxiang3[0], baoxiang3[1], baoxiang1[0] + 4, baoxiang3[1] + 12)

    def helpbox():
        pad = curses.newpad(sh, sw)
        pad.bkgd(' ', curses.color_pair(1))
        pad.addstr(1, 0, 'b：抽奖 五块一次', curses.A_BLINK)
        pad.addstr(2, 0, 'c：加100快', curses.A_BLINK)
        pad.addstr(3, 0, 's：查看宝箱内容 15块一次', curses.A_BLINK)
        pad.addstr(4, 0, 'k：查看技能', curses.A_BLINK)
        pad.addstr(5, 0, 'q：退出游戏', curses.A_BLINK)
        pad.addstr(6, 0, 'h：查看怪物信息', curses.A_BLINK)
        pad.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 16, baoxiang2[1] + 30)
        w.getch()
        pad = curses.newpad(sh, sw)
        pad.bkgd(' ', curses.color_pair(3))
        pad.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 16, baoxiang2[1] + 30)
        if rank % 3 != 0:
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
        else:
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
        w.addch(snake[0][0], snake[0][1], curses.ACS_SSSS,curses.color_pair(1))
    while True:
        next_key = w.getch()
        key = next_key
        new_head = [snake[0][0], snake[0][1]]
        if key == ord('b'): # 抽奖
            if baoxiang1[0]<=snake[0][0]<=baoxiang1[0]+4 and baoxiang1[1]<=snake[0][1]<=baoxiang3[1]+12:

                choujiangkuang_delete('不能站在这个区域抽奖哦！往下挪一点就好啦～')

                flag4 = 1
            else:
                b_score =score - 5
                if b_score >= 0:
                    if rank % 3 != 0:
                        w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
                    else:
                        w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
                    cishu += 1
                    if cishu !=1:
                        choujiangkuang_delete('按一次b抽一次奖，乱按只会让钱变少！')
                        cishu = 0
                    else:
                        flag_bonus = 3
                        while flag_bonus:
                            ran = random.randint(1, 15)
                            if 0<ran<3:
                                present = '攻击+{0}  '.format(ran)
                                bonus.append(present)

                            if 3<=ran<9:
                                present = '防御+{0}  '.format(ran-2)
                                bonus.append(present)

                            if 9<=ran<16:
                                present = '谢谢再见！'
                                bonus.append(present)
                            flag_bonus-=1
                        choujiangkuang_appear()
                else:
                    choujiangkuang_delete('金币不够别点了！！五个金币抽一次不知道吗？？')
                    if rank % 3 != 0:
                        w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
                    else:
                        w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
        elif key == ord('k'): #技能模块
            pad2 = curses.newpad(sh, sw)
            pad2.bkgd(' ', curses.color_pair(1))
            pad2.addstr(0, 0, '技能1：效果',curses.A_BLINK)
            pad2.addstr(1, 0, '技能2：效果',curses.A_BLINK)
            pad2.addstr(2, 0, '技能3：效果',curses.A_BLINK)
            pad2.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 16, baoxiang2[1] + 20)
            w.getch()
            pad2.bkgd(' ', curses.color_pair(3))
            pad2.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 16, baoxiang2[1] + 20)
            if rank % 3 != 0:
                w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
            else:
                w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
        elif key == ord('z'):# 帮助模块
            helpbox()
        elif key == ord('c'):# 金手指无限钱
            score+=100
        elif key == ord('h'): #  查看怪物属性
            pad3 = curses.newpad(sh, sw)
            pad3.bkgd(' ', curses.color_pair(1))
            pad3.addstr(0, 0, '生命：{0}'.format(master_hp), curses.A_BLINK)
            pad3.addstr(1, 0, '防御：{0}'.format(master_defence), curses.A_BLINK)
            pad3.addstr(2, 0, '攻击：{0}'.format(master_damage), curses.A_BLINK)
            pad3.addstr(3, 0, '技能：{0}'.format(master_skill), curses.A_BLINK)
            if rank % 3 != 0:
                pad3.addstr(5, 2, '小怪{0}号'.format(rank), curses.A_BLINK)
            else:
                pad3.addstr(5, 2, '精英怪{0}号'.format(rank), curses.A_BLINK)
            pad3.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 16, baoxiang2[1] + 20)
            w.getch()
            pad3.bkgd(' ', curses.color_pair(3))
            pad3.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 16, baoxiang2[1] + 20)
            if rank % 3 != 0:
                w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
            else:
                w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
        elif key == curses.KEY_DOWN:
            new_head[0] += 1

        elif key == curses.KEY_UP:
            new_head[0] -= 1

        elif key == curses.KEY_LEFT:
            new_head[1] -= 1

        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        elif key == ord('q'): #退出游戏
            curses.endwin()
            quit()

        if flag4 == 0:
            snake.insert(0,new_head)
        else:
            flag4 = 0
            snake.insert(0,snakee[0])

        if cishu == 1:
            if key == ord('s'):  #查看宝箱内容
                score -= 15
                pad = curses.newpad(sh, sw)
                pad.bkgd(' ', curses.color_pair(1))
                pad.addstr(2, 0, '{0}'.format(bonus[0]), curses.A_BLINK)
                pad.refresh(0, 0, baoxiang1[0], baoxiang1[1], baoxiang1[0] + 4, baoxiang1[1] + 12)

                pad.addstr(2, 0, '{0}'.format(bonus[1]), curses.A_BLINK)
                pad.refresh(0, 0, baoxiang2[0], baoxiang2[1], baoxiang1[0] + 4, baoxiang2[1] + 12)

                pad.addstr(2, 0, '{0}'.format(bonus[2]), curses.A_BLINK)
                pad.refresh(0, 0, baoxiang3[0], baoxiang3[1], baoxiang1[0] + 4, baoxiang3[1] + 12)

            if baoxiang1[0] <= snake[0][0] <= baoxiang1[0] + 4 and baoxiang1[1] <=snake[0][1]<=baoxiang1[1]+12:
                choujiangkuang_delete(None)
                jieguo = bonus[0]
                if re.search(r'谢谢', jieguo):
                    pass
                else:
                    b = re.findall(r'(\w*?)\+(\d)', jieguo)
                    b = list(b[0])
                    if b[0] == '攻击':
                        damage += int(b[1])
                    elif b[0] == '防御':
                        defence += int(b[1])
                    else:
                        pass
                if rank % 3 != 0:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
                else:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
                cishu = 0
                bonus.clear()
            if baoxiang2[0] <= snake[0][0] <= baoxiang2[0] + 4 and baoxiang2[1] <=snake[0][1]<=baoxiang2[1]+12:
                choujiangkuang_delete(None)
                jieguo = bonus[1]
                if re.search(r'谢谢',jieguo):
                    pass
                else:
                    b = re.findall(r'(\w*?)\+(\d)',jieguo)
                    b = list(b[0])
                    if b[0] == '攻击':
                        damage+=int(b[1])
                    elif b[0] == '防御':
                        defence+=int(b[1])
                    else:
                        pass
                if rank % 3 != 0:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
                else:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
                cishu = 0
                bonus.clear()

            if baoxiang3[0] <= snake[0][0] <= baoxiang3[0] + 4 and baoxiang3[1] <=snake[0][1]<=baoxiang3[1]+12:
                choujiangkuang_delete(None)
                jieguo = bonus[2]
                if re.search(r'谢谢', jieguo):
                    pass
                else:
                    b = re.findall(r'(\w*?)\+(\d)', jieguo)
                    b = list(b[0])
                    if b[0] == '攻击':
                        damage += int(b[1])
                    elif b[0] == '防御':
                        defence += int(b[1])
                    else:
                        pass
                if rank % 3 != 0:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
                else:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
                cishu = 0
                bonus.clear()

        if snake[0] == food: # 战斗判断
            real_damage = damage - master_defence
            change_hp = int(master_damage - defence)
            if change_hp < 0:
                pass
            else:
                hp = (hp - change_hp)

            if real_damage <= 0:
                pad3 = curses.newpad(sh, sw)
                pad3.bkgd(' ', curses.color_pair(1))
                pad3.addstr(0, 0, '攻击力没人家防御力高，怎么打？？')
                pad3.refresh(0, 0, sh // 2, sw // 2, sh // 2, sw // 2 + 28)
                w.getch()
                pad3.bkgd(' ', curses.color_pair(3))
                pad3.refresh(0, 0, sh // 2, sw // 2, sh // 2, sw // 2 + 28)
                w.refresh()
                snake[0] = snake[1]
                if rank % 3 != 0:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
                else:
                    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(4))
            else:
                food = None
                # zhandoukuang('战斗中！')
                rank += 1
                master_damage += 2
                master_defence += 2
                damage+=1
                defence+=1
                if (rank-1) % 3 != 0:
                    score += 1
                else:
                    score += 3
            while food is None:
                nf = [
                    random.randint(3, sh - 3),
                    random.randint(3, sw - 3)
                ]
                if food == snakee:
                    food = None
                else:
                    food = nf if nf not in snake else None


            if (rank) % 3 !=0:
                w.addch(food[0], food[1], curses.ACS_DIAMOND,curses.color_pair(2))
            else:
                w.addch(food[0], food[1], curses.ACS_DIAMOND,curses.color_pair(4))
            t = snake.pop()
            w.addch(t[0], t[1], " ")
        else:
            t = snake.pop()
            w.addch(t[0], t[1], " ")

        if snake[0][0]<3 or snake[0][1]<3 or snake[0][0]>sh - 3 or snake[0][1]>sw - 3:#边界判定
            score-=1
            snake = [[snk_y, snk_x]]

        if hp == 0:#失败判定
            pad = curses.newpad(100, 100)
            pad.bkgd(' ', curses.color_pair(1))
            pad.addstr(2, 2, '游戏结束，你太菜了！', curses.A_BLINK)
            pad.refresh(0,0, 5,5, 20,75)
            flagg = 2 # 失败判定 #

        if flagg == 2:
            time.sleep(3)
            curses.endwin()
            quit()

        if rank == 31:
            pad = curses.newpad(100, 100)
            pad.bkgd(' ', curses.color_pair(2))
            pad.addstr(2, 2, '恭喜通关！', curses.A_BLINK)
            pad.refresh(0, 0, 5, 5, 20, 75)
            curses.endwin()
            quit()

        w.addch(snake[0][0], snake[0][1], curses.ACS_SSSS,curses.color_pair(1))
        w.addstr(0, 0, '金币：{0}    攻击力：{1}   防御力：{2}   生命值：{3}  关卡：{4}'.format(score,damage,defence,str(hp)+' ', rank))
        w.refresh()

curses.wrapper(game())