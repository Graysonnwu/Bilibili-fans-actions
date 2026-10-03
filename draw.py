import pandas as pd
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import sys
from pathlib import Path

from bilibili import validate_uid

uid = sys.argv[1]
validate_uid(uid)
root = Path(__file__).resolve().parent
# uid = 22245854

df = pd.read_csv(root / 'data' / f'{uid}.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['follower'] = pd.to_numeric(df['follower'], errors='coerce')
df = df.dropna(subset=['date', 'follower'])
df = df[(df['follower'] >= 0) & (df['follower'] % 1 == 0)]
df = df.drop_duplicates('date', keep='first').sort_values('date')
if df.empty:
    raise ValueError('No valid follower observations')
df['diff_follower'] = df['follower'].diff() / df['date'].diff().dt.days
# Compute the earliest visible change from its preceding observation, too.
df = df.tail(200)
# print(df.head(16))

plt.figure(figsize=(15,5))

# https://coolors.co/gradient-palette/fcaed6-7a73ff?number=8
color = pd.Series([
    '#D4221C', '#D3401C', '#D25E1B', '#D17C1B', '#CF9A1B', '#CEB81A',
    '#CDD61A', '#A9D53C', '#86D55E', '#62D480', '#3FD4A2', '#1BD3C4',
    '#FCAED6', '#E9A6DC', '#D79DE2', '#C495E8','#B28CED', '#9F84F3', '#8D7BF9','#7A73FF',
    '#8B6ADF', '#9C61BE','#AE589E', '#BF4F7E', '#D0465D','#E13D3D',
    '#D4221C', '#D3401C', '#D25E1B', '#D17C1B', '#CF9A1B', '#CEB81A',
    '#CDD61A', '#A9D53C', '#86D55E', '#62D480', '#3FD4A2', '#1BD3C4',]) # 12+14+12个颜色
# reverse
color = color[::-1]

inter = pd.Series([
    -1000,-500,-200,-100,-50,-20,
    -10,-5,-3,-2,-1,0,
    1,2,3,4,6,8,11,16,
    23,32,45,64,90,
    128,180,256,360,512,720,
    1024,1440,2048,2880,4096,5760]) # 12+13+12个刻度

# 查找对应颜色
color_index = inter.searchsorted(df['diff_follower'])
color_bar = color[color_index]

# 绘图
plt.bar(df['date'].dt.strftime('%Y-%m-%d'),df['diff_follower'],color=color_bar)
# 底数为2的对数刻度
plt.yscale('symlog',base=2)
# Y轴增加两个额外的刻度

# Y轴标签必须完整展示数字
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
# Y轴标签在右边也加一个
plt.gca().tick_params(labeltop=False, labelright=True)
# 设置X轴最多有13个ticks
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(13))
# 坐标及标签设为白色，网格为灰色
plt.gca().tick_params(axis='x', colors='white')
plt.gca().tick_params(axis='y', colors='white')
plt.gca().spines['bottom'].set_color('white')
plt.gca().spines['left'].set_color('white')
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.grid(color='gray', linestyle='-', linewidth=0.5)
# 背景透明并输出
(root / 'img').mkdir(exist_ok=True)
plt.savefig(root / 'img' / f'{uid}_diff_follower.png', transparent=True)
# plt.savefig('test/%s_diff_follower.png'%uid, transparent=True)

plt.yscale('linear')
plt.savefig(root / 'img' / f'{uid}_diff_follower_ori.png', transparent=True)
plt.close()
# plt.savefig('test/%s_diff_follower_ori.png'%uid, transparent=True)
