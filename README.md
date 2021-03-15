# Cube detect

* 此 repo 用來偵測物體是否為魔術方塊
* push 前記得 ```make clean``` 確保把測試照片正確刪除避免 repo 檔案過大

## 檔案說明

* src/main.py : 抓 test/img/ 下的照片測試
* src/cam.py : 開啟相機直接測試
* src/makefile : makefile 預設為執行 main.py
* test/rename.sh : 用來重新命名照片名字方便 main.py 讀檔, 加入新照片後記得先執行一次, **執行之前確保照片副檔是否全部都為 jpg 格式, 不是的話記得先轉檔 不然會爆炸**
* test/img : 放測試照片的地方, 可自行加入測資

## command 說明

* src 下執行:

    ```make``` : 執行 src/main.py, **下此命令之前確保 test/img 的照片已經經過重新命名**

    ```make clean``` : 清除 test/result/ 下資料夾內照片並創見空白資料夾

    ```python3 main.py``` : 執行 main.py

* test 下執行:

    ```./rename.sh``` : 執行前確認一下檔案權限, 權限不夠的話用 ```chmod +x rename.sh```