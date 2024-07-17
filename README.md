# 面試機器人 (Interview Bot) 🤖

## 目錄
1. [專案概述](#專案概述)
2. [安裝說明](#安裝說明)
3. [使用技術](#使用技術)
4. [使用說明](#使用說明)
5. [配置說明](#配置說明)
6. [資料庫相關](#資料庫相關)
7. [測試](#測試)
8. [常見問題和故障排除](#常見問題和故障排除)
9. [貢獻指南](#貢獻指南)
10. [授權](#授權)

## 專案概述

面試機器人是一個基於 LangChain 與 RAG 之技術面試 AI 模型並使用 Django 作為整體框架的網頁應用程式，旨在通過提供一個練習面試的聊天機器人讓使用者練習像是 Leetcode 的題目。該應用程式支援多種語言，並為使用者提供了友好的使用介面。

### 主要功能
- 使用者身份驗證和授權
- 實時面試會話和聊天功能
- 根據使用者問題自動生成回應

## 安裝說明

### 系統需求
- Python 3.12
- Django 5.0.4
- SQL Server

以下是安裝步驟：

1. 克隆此倉庫到本地：
   ```bash
   git clone https://github.com/Poyu-Tu/InterviewBot.git
   ```

2. 進入專案目錄：
   ```bash
   cd interview_platform
   ```

3. 建立虛擬環境並激活：
   ```bash
   python3 -m venv venv # 建立虛擬環境
   
   source env/bin/activate # 啟動虛擬環境 (Mac 作業系統)
   source env\Scripts\activate # 啟動虛擬環境 (Windows 作業系統)
   ```

4. 安裝所需的依賴：
   ```bash
   pip install -r requirements.txt
   ```
5. 遷移資料庫：
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. 啟動開發伺服器：
   ```bash
   python manage.py runserver
   ```
## 使用技術

- 前端：HTML、CSS、JavaScript
- 資料庫：SQLite
- 後端：Django(Python)
- AI 模型：GPT-4、LangChain、RAG

## 使用說明

### 存取應用程式
打開您的網頁瀏覽器，並前往 http://localhost:8000/

1. 使用者會先進入主畫面，此時可以選擇註冊、登入或進入 Django 內建的 SQLite 後台系統查詢。
2. 若使用者無帳號，則需先至註冊頁面註冊一個帳號，註冊時若有違反安全性的操作，系統將會跳出提醒。註冊完畢後將會自動回到首頁。
3. 若使用者選擇登入，則輸入帳號及密碼，若正確即可登入面試機器人操作畫面。
4. 進入面試機器人，可以準備你的面試問題與它進行練習。

### 範例使用情境

- 註冊一個新使用者
- 登入使用者
- 開始面試會話

## 配置說明

### 重要設定

- DEBUG: 開發環境設置為 True，生產環境設置為 False
- ALLOWED_HOSTS: 添加您的網域或 IP 地址
- DATABASES: 在 settings.py 中配置您的資料庫設定

## 資料庫相關

### 初始化資料

- 創建一個超級使用者以進行管理操作
```bash
python manage.py createsuperuser
```
### 對資料庫中資料進行操作

1. 進入根目錄並打開終端機。

2. 開始輸入指令🔻
```bash
python manage.py shell
```
```bash
# 查詢全部DB中的資料
from members.models import Member
members = Member.objects.all()
print(f'{"Number":<10} {"Username":<20} {"Password":<20}')  # 打印表頭
for index, member in enumerate(members, start=1):   # 迴圈生成每筆資料
    print(f'{index:<10} {member.username:<20} {member.password:<20}')
    
print(f'------------\n總筆數: {members.count()}')   # 打印總筆數
```
```bash
# 刪除單筆
from members.models import Member 
del = Member.objects.filter(username='xxx').delete()
print('刪除成功')
```
```bash
# 刪除全部
from members.models import Member 
Member.objects.all().delete()
print('刪除成功')
```

## 測試

### 執行測試
```bash
python manage.py test
```

### 測試覆蓋
確保為所有新功能和特性編寫測試

## 常見問題和故障排除

- 請參考 [Django 文檔](https://docs.djangoproject.com/en/5.0/)以獲取常見問題及其解決方案

## 貢獻

歡迎任何形式的貢獻！如果你想要貢獻，請遵循以下步驟：

1. **Fork 本儲存庫**：點擊 GitHub 頁面右上角的 "Fork" 按鈕。
2. **創建分支**：在你的儲存庫中創建一個新分支來開發你的變更。
```bash
git checkout -b feature-branch
```
3. **提交更改**：將你的變更提交到該分支。
```bash
git commit -m "Add some feature"
```
4. **推送到 GitHub**：將你的分支推送到 GitHub。
```bash
git push origin feature-branch
```
5. **開 Pull Request**：在 GitHub 上開一個 Pull Request，描述你的變更，等待維護者的審核與合併。

## 授權

此專案採用 MIT 授權條款。詳情請參閱 [LICENSE 文件](LICENSE)。