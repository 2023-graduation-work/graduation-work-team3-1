# import tkinter as tk
# import sqlite3
# from tkinter import messagebox


# def click_insert(date,textbox , weather,erichment,action):

#     # SQLite3データベースへの接続をここで行う
#     conn = sqlite3.connect('daiaryapp.splite3')
#     cur = conn.cursor()
    
#     try:
#         # テーブル "user" が存在しない場合、CREATE TABLE ステートメントで作成
#         create_table_sql = "CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,textbox TEXT,weather TEXT,enrichment INTEGER,action TEXT)"
#         print('テーブルを作成')
#         cur.execute(create_table_sql)
#         conn.commit()
        
#         print(f'conn:{conn}')   

#         # テーブルにデータ\を挿入
#         sql_statement = "INSERT INTO diary VALUES (default,?,?,?,?,?)"
#         cur.execute(sql_statement,(date,textbox,weather,erichment,action))
#         conn.commit()
        

#         messagebox.showinfo("Success", "データが正常に挿入されました。")
#     except sqlite3.Error as e:
#         messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))

# # Tkinterウィンドウの設定
# root = tk.Tk()
# root.title("SQLite3接続確認")

# # ボタンを作成して関数を実行
# check_button = tk.Button(root, text="SQLite3接続を確認", command=click_insert)
# check_button.pack(pady=20)

# root.mainloop()
