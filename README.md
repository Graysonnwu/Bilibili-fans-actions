# Bilibili-fans-actions（仅保留基础模式）
用 Github Actions 更新 bilibili 粉丝数

![本人粉丝数变化](img/22245854_diff_follower_ori.png?raw=true)
本人近期粉丝数变化图：（透明底白字，黑暗模式适用）


代码改编自：https://github.com/guodongxiaren/py （改编得很水，期待大佬完善）

---
## 说明
- **【基础】只更新粉丝数，无需SESSDATA：**
  > `bilibili.py` + `bilibili.sh`  + `uid.txt` --> `./data` 

- **【画图】粉丝数变化图**
  > `draw.py` + `draw.sh` + `uid.txt` --> `./img`

- <del>【完整】更新uid.txt中用户的粉丝数、获赞数、播放量、阅读量，需要每月更新SESSDATA：（由于B站似乎更改了SESSDATA的刷新频率，此条弃用）</del>
  > `general.py` + `general.sh` +`uid.txt` --> `./csv` + `./txt`




---
## 用法
如果要自己用，可以直接复制后新开repo，也可以Fork之后：
- 修改 `uid.txt` 里要监控的uid列表
- 记得修改几个 yml 文件里面 commit 的账号啊！！不然每次都是我在提交
- [可选]最后根据需要修改 `./.github/workflows/bilibili.yml` 中的监控频率，目前为每天北京时间23:50爬一次
- <del>修改 `general.py` 中的SESSDATA（完整，已弃用）</del>

---
## 其它
