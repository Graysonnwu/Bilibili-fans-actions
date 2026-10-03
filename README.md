# Bilibili-fans-actions
用 Github Actions 更新 bilibili 粉丝数

![本人粉丝数变化](img/22245854_diff_follower_ori.png?raw=true)
本人近期粉丝数变化图：（透明底白字，黑暗模式适用）


代码改编自：https://github.com/guodongxiaren/py

---
## 说明
- **更新粉丝数**
  > `bilibili.py` + `bilibili.sh`  + `uid.txt` --> `./data` 

- **画图**
  > `draw.py` + `draw.sh` + `uid.txt` --> `./img`

## 本地维护说明

- `python3 bilibili.py <UID>` 只打印一次观测；`--record` 才写入本地历史。
- 日期明确采用北京时间（UTC+8）。API 超时、HTTP 错误、业务错误或无效粉丝数会退出失败，不写入历史。
- 同一天重复运行保留最后一次有效观测；TXT 按日期正序，CSV 倒序。写入使用临时文件替换，避免半行数据。
- `sh bilibili.sh` 会处理所有 UID；任一 UID 失败则返回非零状态。`sh draw.sh` 可在任意当前目录运行。
- 图表显示最近 200 次有效观测的变化；如果两次观测之间有缺失日期，柱高是观测期间日均增长。
- `python3 -m unittest -v test_bilibili.py` 是离线回归，不请求 API、不修改现有粉丝历史。
