import PySimpleGUI as sg
import re
from currency_converter import CurrencyConverter
from datetime import date
import random
import matplotlib.pyplot as plt
import pygame
# 功能计算函数
def fixed_deposit_interest(principal, annual_rate, years):
    return principal * annual_rate * years

def get_conv(text1,text2):
    conv = CurrencyConverter()
    c = conv.convert(1, text1, text2)
    return c

def loan_monthly_payment(loan_amount, annual_rate, loan_months):
    monthly_rate = annual_rate / 12
    return loan_amount * monthly_rate * (1 + monthly_rate) ** loan_months / ((1 + monthly_rate) ** loan_months - 1)

def loan_total_amount(monthly_payment, loan_months):
    return monthly_payment * loan_months

def compound_interest(principal, annual_rate, years):
    return principal * ((1 + annual_rate) ** years - 1)

def compound_total(principal, annual_rate, years):
    return principal * (1 + annual_rate) ** years

def monthly_pension_contribution(salary, pension_rate):
    return salary * pension_rate

def total_pension_contribution(monthly_contribution, years):
    return monthly_contribution * years * 12

def monthly_pension(total_pension_amount, months_after_retirement):
    return total_pension_amount / months_after_retirement

def calculate_present_value(investments, rate):
    """
    计算一系列投资的现值。
    :param investments: 一个列表，包含每年的投资额。
    :param rate: 折现率（利率），以小数形式表示，例如 0.05 表示 5%。
    :return: 现值总和。
    """
    present_value = 0
    for year, investment in enumerate(investments):
        present_value += investment / (1 + rate) ** year
    return present_value

def separate_investments(investment_string):
    """
    分离用户输入的投资额字符串，支持多种分隔符。

    :param investment_string: 投资额字符串。
    :return: 一个包含投资额的列表，转换为浮点数。
    """
    # 使用正则表达式分隔字符串，匹配空格、中文逗号、句号和英文逗号
    investments = re.split(r'[,\s，。]+', investment_string)
    return [float(investment.strip()) for investment in investments if investment.strip()]

def calculate_final_return(investments, rate):
    """
    计算一系列投资的最终收益。

    :param investments: 一个列表，包含每年的投资额。
    :param rate: 利率，以小数形式表示，例如 0.05 表示 5%。
    :return: 最终收益总和。
    """
    final_return = 0
    for year, investment in enumerate(investments):
        final_return += investment * (1 + rate) ** year
    return final_return


def gamble(initial_amount, risk_level,count):
    amount = initial_amount
    amounts = [amount]
    past=0
    for _ in range(count):

        bet = amount *  risk_level
        if random.random() < (1/ (risk_level+1)):
            amount += bet
        else:
            amount = amount*(1/ (risk_level+1))

        past+=1
        amounts.append(amount)
        plt.clf()
        plt.plot(amounts, label='资金曲线')
        plt.xlabel('赌博次数')
        plt.ylabel('剩余资金')
        plt.title('赌博资金模拟')
        plt.legend()

        # 保存图像
        plt.savefig('gamble_plot.png')

        # 更新窗口
        window['-IMAGE-'].update(filename='gamble_plot.png')
        window.refresh()
    if amount >= 10*initial_amount:
       window['-report-'].update('赌神附体，快去大A大显身手吧',text_color='red',font=('黑体',20))
       play_sound("D:\AAA_PythonProject\jisuanqi\win_sound.mp3")
    if amount <= 0.5*initial_amount:
       window['-report-'].update('天选韭菜，快去大A大显身手吧',text_color='red',font=('黑体',20))
       play_sound("D:\AAA_PythonProject\jisuanqi\lose_sound.mp3")

def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


def error_popup():
    # 弹出错误窗口，提示重新输入或者退出
    choice = sg.popup_yes_no("程序发生错误，是否重新输入？", title="错误", keep_on_top=True)

    if choice == 'Yes':
        return True  # 用户选择重新输入
    else:
        return False  # 用户选择退出


layoutmain = [
    [sg.T('请选择计算内容',font='黑体')],
    [sg.B('定期存款',font='黑体',size = (30,2))],
    [sg.B('贷款',font='黑体',size = (30,2))],
    [sg.B('复利方式存款',font='黑体',size = (30,2))],
    [sg.B('汇率转换',font='黑体',size = (30,2))],
    [sg.B('PV与FV计算',font='黑体',size = (30,2))],
    [sg.B('赌博模拟器',font='黑体',size = (30,2))]
]
layout_1_1=[
    [sg.T('年利率',size=7,font='黑体'),sg.T('存款年数',size=10,font='黑体'),sg.T('本金',size=20,font='黑体')],
    [sg.In(size=7,key='-1_rate-'),sg.In(size=10,key='-1_year-'),sg.In(size=20,key='-1_capital-')],
    [sg.B('计算',key='-1_calculate-',font='黑体',size=(10))]
]
layout_1_2=[
    [sg.T('所得总利息',font='黑体')],
    [sg.T(size=(30,5),key='-1_fit-',background_color='white',colors='black')],
    [sg.T('到期总金额',font='黑体')],
    [sg.T(size=(30,5),key='-1_total-',background_color='white',colors='black')],
]
layout_1 = [
    [sg.T('定期界面',font='黑体',colors='black')],#定期界面
    [sg.Col(layout_1_1,vertical_alignment='top'),
     sg.Col(layout_1_2)]

]
layout_2_1=[
    [sg.T('年利率',size=7,font='黑体'),sg.T('贷款月数',size=10,font='黑体'),sg.T('贷款金额',size=20,font='黑体')],
    [sg.In(size=7,key='-2_rate-'),sg.In(size=10,key='-2_year-'),sg.In(size=20,key='-2_capital-')],
    [sg.B('计算',key='-2_calculate-',font='黑体',size=(10))]
]
layout_2_2=[
    [sg.T('月供',font='黑体')],
    [sg.T(size=(30,5),key='-2_fit-',background_color='white',colors='black')],
    [sg.T('到期总偿还金额',font='黑体')],
    [sg.T(size=(30,5),key='-2_total-',background_color='white',colors='black')],
]
layout_2 = [    #贷款界面
    [sg.T('贷款界面', font='黑体', colors='black')],
    [sg.Col(layout_2_1, vertical_alignment='top'),
     sg.Col(layout_2_2)]
]
layout_3_1=[
    [sg.T('期利率',size=7,font='黑体'),sg.T('期数',size=10,font='黑体'),sg.T('存款本金',size=20,font='黑体')],
    [sg.In(size=7,key='-3_rate-'),sg.In(size=10,key='-3_year-'),sg.In(size=20,key='-3_capital-')],
    [sg.B('计算',key='-3_calculate-',font='黑体',size=(10))]
]
layout_3_2=[
    [sg.T('到期总获得利息', font='黑体')],
    [sg.T(size=(30, 5), key='-3_fit-', background_color='white', colors='black')],
    [sg.T('到期总金额', font='黑体')],
    [sg.T(size=(30, 5), key='-3_total-', background_color='white', colors='black')],
]
layout_3 = [    #复利界面
    [sg.T('复利界面', font='黑体', colors='black')],
    [sg.Col(layout_3_1, vertical_alignment='top'),
     sg.Col(layout_3_2)]
]
list_4_1=['USD','EUR','CNY','SUR','BRC','INR','CAD','AUD','FRF','DEM','JPY','ITL','MXP','ESP','IDR','TRL','NLG','SAR','SEK','THP','NOK','ZAR','SGD','MYR','PLZ','ATS','GRD']
list_4_2=['USD','EUR','CNY','SUR','BRC','INR','CAD','AUD','FRF','DEM','JPY','ITL','MXP','ESP','IDR','TRL','NLG','SAR','SEK','THP','NOK','ZAR','SGD','MYR','PLZ','ATS','GRD']
layout_4 = [    #汇率界面
    [sg.T('汇率界面', font='黑体', colors='black')],
    [sg.Drop(list_4_1,key='-contry1-',size=5,font=('黑体','25')),sg.T(' ',size=(2,2)),sg.Drop(list_4_2,key='-contry2-',size=5,font=('黑体','25'))],
    [sg.In(key='-YY-',size=5,font=('黑体','25')),sg.T('=',size=(2,1),font=('黑体','25')),sg.In(key='-result4-',size=5,font=('黑体','25'))],
    [sg.B('转换',key='-4_calculate-',font='黑体',size=(10))]
]

layout_5 = [
    [sg.T('PV与FV界面', font='黑体', colors='black')],
    [sg.T('请输入一系列投资额，以逗号为间隔'),sg.T('输入利润率',size=10),sg.T('FV')],
    [sg.In(key='-investments_1-',size=30,pad=5),sg.In(key='-rate_5_1-',size=10),sg.In(key='-fv-',size=10)],
    [sg.B('计算', key='-5_calculate_1-')],
    [sg.T('请输入一系列回报，以逗号为间隔'), sg.T('输入折现率', size=10), sg.T('PV')],
    [sg.In(key='-investments_2-', size=30, pad=5), sg.In(key='-rate_5_2-', size=10), sg.In(key='-pv-', size=10)],
    [sg.B('计算',key='-5_calculate_2-')]
]
list_6=['1','2','3','4','5','6','7']
layout_6_1 = [
    [sg.T('请输入您的初始本金'),sg.T('请选择赔率',size=10),sg.T('请输入模拟次数')],
    [sg.In(key='-initial-',size=10,pad=30),sg.Drop(list_6,key='-risk-',size=10,font=('黑体','10')),sg.In(key='-count-',size=10)],
    [sg.T(' ',key='-report-',font=('黑体','10')),],
    [sg.T(' ')],
    [sg.B('开始模拟',key='-6_calculate-')]

]
layout_6_2 = [
    [sg.T('模拟收益')],
    [sg.Image(filename='', key='-IMAGE-')]
]
layout_6 = [
[sg.T('赌博模拟器界面', font='黑体', colors='black')],
[sg.Col(layout_6_1),sg.Col(layout_6_2)]
]



layout = [    #主界面
    [
     sg.Col(layoutmain,key='-main-'),
     sg.Col(layout_1,visible = False,key='-1-'),
     sg.Col(layout_2,visible = False,key='-2-'),
     sg.Col(layout_3,visible = False,key='-3-'),
     sg.Col(layout_4,visible = False,key='-4-'),
     sg.Col(layout_5,visible = False,key='-5-'),
     sg.Col(layout_6,visible = False,key='-6-')],
     [sg.B('回到首页',key='-back_to_front-')#,sg.B('更换主题',key='-change_theme-')
       ]

]


window = sg.Window('菠萝牌金融计算器', layout)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == '定期存款':
       window['-1-'].update(visible=True)
       window['-2-'].update(visible=False)
       window['-3-'].update(visible=False)
       window['-4-'].update(visible=False)
       window['-5-'].update(visible=False)
       window['-6-'].update(visible=False)
       window['-main-'].update(visible=False)

    if event == '贷款':
        window['-1-'].update(visible=False)
        window['-2-'].update(visible=True)
        window['-3-'].update(visible=False)
        window['-4-'].update(visible=False)
        window['-5-'].update(visible=False)
        window['-6-'].update(visible=False)
        window['-main-'].update(visible=False)

    if event == '复利方式存款':
        window['-1-'].update(visible=False)
        window['-2-'].update(visible=False)
        window['-3-'].update(visible=True)
        window['-4-'].update(visible=False)
        window['-5-'].update(visible=False)
        window['-6-'].update(visible=False)
        window['-main-'].update(visible=False)

    if event == '汇率转换':
        window['-1-'].update(visible=False)
        window['-2-'].update(visible=False)
        window['-3-'].update(visible=False)
        window['-4-'].update(visible=True)
        window['-5-'].update(visible=False)
        window['-6-'].update(visible=False)
        window['-main-'].update(visible=False)

    if event == 'PV与FV计算':
        window['-1-'].update(visible=False)
        window['-2-'].update(visible=False)
        window['-3-'].update(visible=False)
        window['-4-'].update(visible=False)
        window['-5-'].update(visible=True)
        window['-6-'].update(visible=False)
        window['-main-'].update(visible=False)

    if event == '赌博模拟器':
        window['-1-'].update(visible=False)
        window['-2-'].update(visible=False)
        window['-3-'].update(visible=False)
        window['-4-'].update(visible=False)
        window['-5-'].update(visible=False)
        window['-6-'].update(visible=True)
        window['-main-'].update(visible=False)

    if event == '-back_to_front-':
        window['-1-'].update(visible=False)
        window['-2-'].update(visible=False)
        window['-3-'].update(visible=False)
        window['-4-'].update(visible=False)
        window['-5-'].update(visible=False)
        window['-6-'].update(visible=False)
        window['-main-'].update(visible=True)
    try:

        if event == '-1_calculate-':
            fit = fixed_deposit_interest(float(values['-1_capital-']), float(values['-1_rate-']),
                                         float(values['-1_year-']))
            window['-1_fit-'].update(fit)
            window['-1_total-'].update(fit + float(values['-1_capital-']))

        if event == '-2_calculate-':
            fit = loan_monthly_payment(float(values['-2_capital-']), float(values['-2_rate-']),
                                       float(values['-2_year-']))
            window['-2_fit-'].update(fit)
            window['-2_total-'].update(fit * float(values['-2_year-']))

        if event == '-3_calculate-':
            total = compound_total(float(values['-3_capital-']), float(values['-3_rate-']), float(values['-3_year-']))
            window['-3_fit-'].update(total - float(values['-3_capital-']))
            window['-3_total-'].update(total)

        if event == '-4_calculate-':
            result = get_conv(values['-contry1-'], values['-contry2-']) * float(values['-YY-'])
            window['-result4-'].update(result)

        if event == '-5_calculate_1-':
            investments_1 = separate_investments(values['-investments_1-'])
            result_5_1 = calculate_present_value(investments_1, float(values['-rate_5_1-']))
            window['-fv-'].update(result_5_1)

        if event == '-5_calculate_2-':
            investments_2 = separate_investments(values['-investments_2-'])
            result_5_2 = calculate_final_return(investments_2, float(values['-rate_5_2-']))
            window['-pv-'].update(result_5_2)

        if event == '-6_calculate-':
            window['-report-'].update(' ')
            initial_amount = float(values['-initial-'])
            risk_level = int(values['-risk-'])
            gamble(initial_amount, risk_level, int(values['-count-']))


    except Exception as e:
       # sg.popup_error(f'程序出现了一个错误', title="错误", keep_on_top=True)
        if error_popup():  # 用户选择重新输入
            continue
        else:  # 用户选择退出
            break



window.close()

