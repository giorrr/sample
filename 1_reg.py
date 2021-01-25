import pandas as pd
import csv
import sys
import re
import itertools

#正しいコマンドラインの長さかどうかを判別し、正しくないならプログラム終了
def check_argv(len_argv):
    if len_argv != 3:
        print("正しいコマンドラインを入力してください")
        sys.exit(1)

#ファイルがtsvファイルか異なるファイルかを判定し、あっていたらtsvファイルが正しい形式かを判別する
def check(file_name):
    s =file_name.endswith(".tsv")
    if s == False:
        print("このファイルは存在しない、もしくはtsvファイルではありません")
        sys.exit(1)

    #tsvファイルが正しい形式かを判別する
    try:
        df = pd.read_csv( file_name, header = 0 ,na_values=[""],keep_default_na = False,delimiter="\t")
    except:
        print("tsvファイルに誤りがあります")
        sys.exit(1)

#列の最大数が6以上の場合にプログラムを終了させる
def check_col(col):
    if col > 5:
        print("列数に誤りがあります")
        sys.exit(1)

#行列データを判別し、正しいデータならばプログラム続行。正しくないデータならばプログラム終了
def check_col_row(col_row):
    if col_row.isascii() == False:
        print("データにASCII印字可能文字以外の値が含まれています")
        sys.exit(1)
    if len(col_row) > 100:
        print("データに100文字より長い値を含んでいます")
        sys.exit(1)
    if col_row.count(":")>9:
        print("セルに含まれる「:」の数が最大数より多いです")
        sys.exit(1)





check_argv(len(sys.argv))
#コマンドライン引数の順番
#実行ファイル名　第一正規形にするファイル名　ヘッダーの有無(1ならヘッダーあり、0ならヘッダーなし)
data=sys.argv[1]
header_exsist=sys.argv[2]



#header_exsistが1ならヘッダーありのtsvのため、ヘッダーを含んでデータ取得。さらにheader名も取得
#header_exsistが0ならヘッダー無しのtsvファイルなのでヘッダー無しでデータを取得
#空白を欠損値とする(nanという文字列も欠損値扱いになってしまうため）
#コマンドラインが正しくない場合は「正しいコマンドラインを入力してください」と出力
if header_exsist == "1":
    check(data)
    df = pd.read_csv( data, header = 0 ,na_values=[""],keep_default_na = False,delimiter="\t")
elif header_exsist == "0":
    check(data)
    df = pd.read_csv( data, header = None ,na_values=[""],keep_default_na = False,delimiter="\t")
else:
    print("正しいコマンドラインを入力してください")


#dataframeの列名を取得
col_name =df.columns.values

check_col(len(col_name))

#最終的に出力するdataframe(空)
df2= pd.DataFrame(index=[],columns = col_name)
#df内のデータがnullかどうかを判定するdataframe
df_null=df.isnull()


#df2に第一正規形にしたデータを追加する
for i in range(len(df)):
    list_2d=[[] for list_range in range(len(col_name))]
    for j,row in enumerate(col_name):
        
        #dfのi行列row列番目が空ならばリストlist_2dに空で追加
        if df_null[row][i] == True:
            list_2d[j].append("")
        #dfのi行列row列番目にデータがあるならば正しい形式のデータかを判別して正しいならばリストlist_2dに追加
        else:
            check_col_row(df[row][i])
            list_2d[j].append(df[row][i]) 

    #リストlist_2dに入っているデータを「:」で分割して代入
    for b in range(len(list_2d)):
        temp=":".join(list_2d[b])
        temp=re.split(":",temp)
        list_2d[b]=temp

    #リストlist_2dの列数に応じた直積をpに代入
    if len(list_2d) == 1:
        list_p=itertools.product(list_2d[0])
    if len(list_2d) == 2:
        list_p=itertools.product(list_2d[0],list_2d[1])
    if len(list_2d) == 3:
        list_p=itertools.product(list_2d[0],list_2d[1],list_2d[2])
    if len(list_2d) == 4:
        list_p=itertools.product(list_2d[0],list_2d[1],list_2d[2],list_2d[3])
    if len(list_2d) == 5:
        list_p=itertools.product(list_2d[0],list_2d[1],list_2d[2],list_2d[3],list_2d[4])

    #list_pに入っているタプルデータをdataframe型に変換して最終的に出力するdf2に追加する
    for v in list_p:
        df_v=pd.DataFrame(v)
        #df_vは行にデータが積まれていくので.Tで転置
        df_v=df_v.T
        df_v.columns = col_name
        df2=df2.append(df_v)

#df2に入っているデータをヘッダーの有無に応じてend.tsvへ出力
if header_exsist=="1":
    df2.to_csv("1_reg.tsv",index=None,sep="\t")
elif header_exsist=="0":
    df2.to_csv("1_reg.tsv",header=None,index=None,sep="\t")

print("1_reg.tsvに出力されました")
