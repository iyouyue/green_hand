

def get_valid_img(request):
    # from utils.random_code import get_random_code
    #
    # data=get_random_code()
    #
    # print()

    import random
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 方式1：
    # f=open("egon.jpg","rb")
    # data=f.read()

    # 方式2;
    from PIL import Image
    # from io import BytesIO
    #
    # image=Image.new(mode="RGB",size=(120,80),color=get_random_color())
    # f=open("code.png","wb")
    # image.save(f,"png")
    #
    # f=open("code.png","rb")
    # data=f.read()

    # 方式3：
    # from io import BytesIO
    # image = Image.new(mode="RGB", size=(120, 80), color=get_random_color())
    # f=BytesIO()
    # image.save(f, "png")
    # data=f.getvalue()


    # 方式4：
    from io import BytesIO
    from PIL import ImageDraw, ImageFont
    f = BytesIO()

    image = Image.new(mode="RGB", size=(120, 80), color=get_random_color())
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("blog/static/fonts/kumo.ttf", size=36)

    temp = []
    for i in range(5):
        random_char = random.choice(
            [str(random.randint(0, 9)), chr(random.randint(65, 90)), chr(random.randint(97, 122))])
        draw.text((i * 24, 26), random_char, get_random_color(), font=font)
        temp.append(random_char)

    width = 120
    height = 80

    # for i in range(80):
    #     draw.point((random.randint(0,width),random.randint(0,height)),fill=get_random_color())
    #
    # for i in range(10):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    # for i in range(40):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    image.save(f, "png")
    data = f.getvalue()

    #######保存随机字符串
    # global random_code_str
    # random_code_str = "".join(temp)
    # print("random_code_str",random_code_str)
    #######


    return data,temp
