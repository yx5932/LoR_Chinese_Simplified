import csv
simpC=[]
tradC=[]
with open('lor繁简对照.csv', encoding='UTF-8-sig') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        simpC.append(row[0])
        tradC.append(row[1])
print(simpC)
print(tradC)

f = open("LocalizedText_zh_tw.bin", 'r+',encoding='utf-8', errors='ignore')

s = f.read()
# for i in range(len(simpC)):
print(s)
for i in range(15):
    print(str(tradC[i]),str(simpC[i]))
#     s.replace(str(tradC[i]), str(simpC[i]))
# print(s)
# f.write(s)

# print(s3)