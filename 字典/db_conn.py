# import pymysql
#
# f = open('dict.txt')
# db = pymysql.connect('localhost', 'root', '123456','directory')
# cursor = db.cursor()  # 创建游标对象
#
# for line in f:
# # line = f.readline()
#     temp = line.split(' ')
#     word = temp[0] #取出单词
#     # print(word,end='')
#     mean = ' '.join(temp[1:]).strip()
#     # print(mean) #取出解释
#
#     sql = '''insert into words(
#              word,interpret)values("%s","%s")
#     '''%(word, mean)
#     try:
#         cursor.execute(sql)
#         db.commit() #执行成功提交
#
#     except Exception as e:
#         print(e)
#         # break
#         db.rollback()  # 产生异常回滚
#
# f.close()


import pymysql

f = open("dict.txt")
db = pymysql.connect("localhost", "root", "123456", "directory")

cursor = db.cursor()  #创建游标

for line in f:
    tmp = line.split(" ")
    word = tmp[0]
    interpret = " ".join(tmp[1:].strip())
    # print(word.interpret)
    sql = """insert into words (word,interpret) values ("%s", "%s")""" %(word, interpret)

    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        db.rollback()
f.close()