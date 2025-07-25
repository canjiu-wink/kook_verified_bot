from dawg_python.units import value
from khl.card import Card, CardMessage, Module ,Element
from khl import Bot, Message
import secrets
import string

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

def remove_key(secret, file_path= "keys.txt"):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [line for line in lines if secret not in line]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        print("删除卡密成功!")

def Activate_lookup(Key, filename= "keys.txt"):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == Key:
                print("查找到卡密!")
                return True
    print("没有找到卡密！")
    return False

def generate_keys(count, length=32):
   print("生成" + str(count) + "卡密")
   chars = string.ascii_letters + string.digits
   return [''.join(secrets.choice(chars) for _ in range(length)) for _ in range(count)]

def save_keys_to_file(keys, prefix, filename="keys.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        for key in keys:
            f.write(prefix + "-" + key + "\n")
    print(f"已保存 {len(keys)} 个卡密到文件：{filename}")

def save_verified_key(key, filength="已使用的卡密.txt"):
    with open(filength, "a", encoding="utf-8") as f:
        f.write(key + "\n")
        print("激活卡密保存成功 : " + key)

def look_verified_key(filength="已使用的卡密.txt"):
    with open(filength, "r" , encoding="utf-8") as f:
        print("查找到已使用卡密")

def verified_num(file_path="已使用的卡密.txt"):
    with open(file_path, 'r', encoding='utf-8') as file:
        line_count = sum(1 for _ in file)
    print(f"已使用卡密一共有： {line_count} ")
    return line_count

# def verified_reminders(key):
#     @bot.command()
#     async def verified_reminders(msg:Message):
#         channel = await bot.client.fetch_public_channel(config(4,num=4))
#         card = Card(
#             Module.Header(key + "已被使用!💖 ")
#         )
#         ret = await channel.send(CardMessage(card))

bot = Bot(token=config(5, num= 3))

@bot.command(name="create_key", prefixes= ['!', '/', '.'], aliases=['ck','生成卡密'])
async def create_key(meg:Message, prefix:str, quantity:str):
    for admin_id in config(2,num=2):
        if meg.author.id == admin_id :
            num = int(quantity)
            keys = generate_keys(count=num, length=32)
            save_keys_to_file(keys, filename="keys.txt",  prefix=prefix)
            sections = [Module.Section(f"{prefix}-{key}") for key in keys]
            c = Card(
                Module.Header("Keys:"),
                *sections,
                Module.Context("一共" + str(num) + "张卡密😘 "),
            )
            await meg.reply(CardMessage(c))
            break

@bot.command(name="verified", prefixes=['!', '/', '.'], aliases=["vd", "激活"])
async def verified(msg:Message, verified:str):
    if Activate_lookup(Key=verified):
        VerifiedSucceed = Card(
            Module.Header("✅激活成功"),
        )
        user = msg.author
        guild = msg.ctx.guild
        await guild.grant_role(user,config(3, num= 1))
        await msg.reply(CardMessage(VerifiedSucceed))
        remove_key(verified)
        save_verified_key(key=verified)
        channel = await bot.client.fetch_public_channel(config(4, num=1))
        card = Card(
            Module.Header(verified + " | 卡密已被使用! 💖 ")
        )
        ret = await channel.send(CardMessage(card))

    else:
        VerifiedError = Card(
            Module.Header("❌ 激活失败，卡密不正确!或被ban"),
        )
        await msg.reply(CardMessage(VerifiedError))

@bot.command(name="help", prefixes=['!', '/', '.'], aliases=["帮助"])
async def help_user(msg:Message):
    helpcard = Card(
        Module.Header("🙏 帮助菜单"),
        Module.Container(Element.Image(src=config(1, num=1))),
        Module.Section("( ! | / | . ) (create_key | 生成卡密) 卡密前缀 生成卡密数量"),
        Module.Context("生成卡密✅"),
        Module.Section("( ! | / | . ) (ban_key | 删除卡密) 卡密"),
        Module.Context("ban 掉不用的卡密✅"),
        Module.Section("( ! | / | . ) (verified | 激活) 卡密 "),
        Module.Context("用卡密激活获取User身份组✅ "),
        Module.Section("( ! | / | . ) (look_verified_key | 查询已使用卡密)"),
        Module.Context("查询已使用卡密,和计算已使用的卡密，和txt已使用卡密发送✅")
    )
    await msg.reply(CardMessage(helpcard))

@bot.command(name="ban_key", prefixes=['!', '/', '.'], aliases=["删除卡密"])
async def ban_key(msg:Message, key:str):
    for admin_id in config(2, num=2):
        if msg.author.id == admin_id :
            if Activate_lookup(key):
                remove_key(key)
                ban_key_card = Card(
                    Module.Header("删除卡密成功🎉 🎉 "),
                    Module.Section("删除卡密为:" + key))
                await msg.reply(CardMessage(ban_key_card)
                                )
            else:
                ban_key_card = Card(
                    Module.Header("卡密无效，或者已被删除!"),
                )
                await msg.reply(CardMessage(ban_key_card))
                break

@bot.command(name="look_verified_key", prefixes=['!', '/', '.'], aliases=["lvk", "查询已使用卡密"])
async def look_verified_key(msg:Message):
    for admin_id in config(2, num=2) :
        if msg.author_id == admin_id :
            num = verified_num()
            file_url = await bot.client.create_asset("已使用的卡密.txt")
            card = Card(
                Module.Header("已使用" + str(num) + "张卡密"),
                Module.File(type="file", src=file_url, title='已使用的卡密:')
            )
            await msg.reply(CardMessage(card))
            print("查询已使用卡密成功!已发送回复!")
            break

if __name__ == "__main__":
    bot.run()