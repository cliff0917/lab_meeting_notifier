# send_email

## csv 格式
- 應包含 `老師和助理.csv`、`專題生.csv`、`碩1.csv`、`碩2.csv`、`博士.csv`（放在 `send_email/` 中）
- 每個 `.csv` 至少需要包含 `name`, `email` 欄位（`id` 欄位為學號，沒有也沒差）

  ![image](https://github.com/cliff0917/send_email/assets/79709549/e0e58d2a-5ff0-4bda-804f-fddb6e106f96)

## 安裝環境
- 輸入 `pip install -r requirements.txt`

## 執行
- 輸入 `crontab -u email -e`，並在最下面新增 `@reboot sh /home/email/send_email/run.sh`，這樣每次重開機就會執行此腳本
- 如需手動執行，則輸入 `cd && sh /home/email/send_email/run.sh`

## 查看執行狀況
- 輸入 `tmux a`

## 更改寄信資訊
- 直接修改 `config.json` 即可（下次就會直接套用新設定）
- 如果修改的是寄信日期，則記得輸入 `sh kill.sh && cd && sh /home/email/send_email/run.sh` 重跑程式

## 關閉
- 輸入 `sh kill.sh`
