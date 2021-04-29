import re

str = "5秒前"
pattern = re.compile(r"\d*秒")
result = re.findall(pattern,str)

print(result)
pattern2 = re.compile(r"\d*")
result = int(re.findall(pattern2,result[0])[0])
print(result)