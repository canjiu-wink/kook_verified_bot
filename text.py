import secrets
import string

from dawg_python.units import value


def generate_keys(count=5, length=32):
    chars = string.ascii_letters + string.digits
    return [''.join(secrets.choice(chars) for _ in range(length)) for _ in range(count)]

def save_keys_to_file(keys, filename="keys.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        for key in keys:
            f.write(key + "\n")
    print(f"已保存 {len(keys)} 个卡密到文件：{filename}")

# def config(target_line, filename="config.cfg", num = 0):
#     with open(filename, "r", encoding="utf-8") as f:
#         for current_line, line in enumerate(f, start=1):
#             if current_line == target_line:
#                 line = line.strip().split("=")
#                 value = line[1].strip()
#             if num == 1 :
#                 return value
#             else:
#                 if len(value) > 1:
#                     value = value[1].strip()
#                     return value
#keys = generate_keys(count=10, length=32)
#save_keys_to_file(keys, filename="key")

def config(target_line, filename="config.cfg", num = 0):
    with open(filename, "r", encoding="utf-8") as f:
        for current_line, line in enumerate(f, start=1):
            if current_line == target_line:
                if num == 1 :
                    line = line.strip().split("=")
                    parts = line
                    value = parts[1].strip()
                    return value
                elif num == 2 :
                    line = line.strip().split("=")
                    parser = line
                    value = parser[1].strip().split(":")
                    return value
                elif num == 3 :
                    parser = line
                    value = parser.split(":")
                    values = value[1].strip()
                    return values

def Activate_lookup(Key, filename= "keys.txt"):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == Key:
                print("查找到卡密!")
                return True
    print("没有找到卡密！")
    return False


i = config(5, num=3)
print(i)
