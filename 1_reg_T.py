import pandas as pd
import csv
import sys
import re
import itertools
from collections import defaultdict


#正しいコマンドラインの長さかどうかを判別し、正しくないならプログラム終了
def check_argv(len_argv):
    if len_argv != 3:
        print("正しいコマンドラインを入力してください")
        sys.exit(1)

#ファイルがtsvファイルか異なるファイル(もしくはpath)かを判定し、あっていたらtsvファイルが正しい形式かを判別する。
#tsvファイルならば1000行以下かどうかを判別して合致しないならばプログラム終了
def check(file_name):
    s =file_name.endswith(".tsv")
    if s == False:
        print("このファイルは存在しない、もしくはtsvファイルではありません")
        sys.exit(1)

    #tsvファイルが正しい形式かを判別して正しくなければ終了
    try:
        df = pd.read_csv( file_name, header = 0 ,na_values=[""],keep_default_na = False,delimiter="\t")
    except:
        print("tsvファイルに誤りがあります")
        sys.exit(1)

    #正しい行数かを判別。判別できない場合(utf-8の文字が入っている場合等)とデータが1000行以上の場合はプログラム終了
    try:
        if len(open(file_name).readlines()) > 1000:
            print("このtsvファイルの行数は正しくありません")
            sys.exit(1)
    except:
        print("tsvファイルに誤りがあります")
        sys.exit(1)



#列の最大数が2以上の場合にプログラムを終了
def check_col(col):
    if col != 2:
        print("列数に誤りがあります")
        sys.exit(1)



#グループ数を数えて最大数より多い場合にはプログラム終了
def check_len(item):
    if item > 10:
        print("グループ化の上限を越えています")
        sys.exit(1)



#行列データを判別し、正しいデータならばプログラム続行。正しくないデータならばプログラム終了
def check_col_row(col_row):
    if col_row.isascii() == False:
        print("データにASCII印字可能文字以外の値が含まれています")
        sys.exit(1)
    if len(col_row) > 100:
        print("データに100文字より長い値を含んでいます")
        sys.exit(1)
    if col_row.count(":")>0:
        print("データにセルに使用してはいけない値「:」が含まれています")
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

#df内のデータがnullかどうかを判定するdataframe
df_null=df.isnull()



list_2d=[[] for col_range in range(len(df))]

#list_2d内に[key,value][key,value][]…の形でデータを入れていく
for i in range(len(df)):
    for j,row in enumerate(col_name):
        if df_null[row][i] == True:
            list_2d[i].append("")
        else:
            check_col_row(df[row][i])
            list_2d[i].append(df[row][i])

list_dd = defaultdict(list)


#list_2dの[key,value]形式から同じkeyのvalueでまとめる
#list_ddには[(key:[value]),(key:[value])…]の形式でデータが入る
for k, v in list_2d:
     list_dd[k].append(v)

check_len(len(list_dd))

list_keys =list(list_dd.keys())


#ヘッダーが存在している場合、出力されるtsvファイルの先頭にヘッダーを追加
if header_exsist =="1":
    header_name ="\t".join(col_name)
    zip_header=(header_name +"\n")
    with open('1_regT.tsv', 'a') as f:
        f.write(zip_header)


#リストlist_ddに入れたデータをtsvファイルとして出力する
for i,j in enumerate(list_keys):
    list_dd[j]=":".join(list_dd[j])
    temp =str(list_keys[i])
    c=str(list_dd[j])
    z=(temp + "\t"+c+"\n")
    with open('1_regT.tsv', 'a') as f:
        f.write(z)

print("1_regT.tsvに出力しました。")
