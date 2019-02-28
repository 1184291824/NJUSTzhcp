from PIL import Image, ImageDraw, ImageFont  # 引入绘图模块
import random  # 引入随机函数模块
from django.shortcuts import render, HttpResponse
from io import BytesIO  # 在内存中创建


def get_random_color():
    """
    获取随机颜色
    :return:
    """
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color


def verification_code(request):
    """
    生成一张验证码图片
    :param request:
    :return:
    """
    # 1.1 定义变量，宽，高，背景颜色
    width = 200
    height = 60
    background_color = get_random_color()
    # 1.2 创建画布对象
    image = Image.new('RGB', (width, height), background_color)
    # 1.3 创建画笔对象
    draw = ImageDraw.Draw(image)
    # 1.4 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        draw.point(xy, fill=get_random_color())
    # 1.5 调用画笔的line()函数制造线
    for i in range(0, 10):
        xy_start = (random.randrange(0, width), random.randrange(0, height))
        xy_end = (random.randrange(0, width), random.randrange(0, height))
        draw.line((xy_start, xy_end), fill=get_random_color())

    # 2 用draw.text书写文字
    rand_python = ''
    for i in range(4):
        random_number = str(random.randint(0, 9))
        random_lower_letter = chr(random.randint(97, 122))
        random_upper_letter = chr(random.randint(65, 90))
        rand_python += random.choice([random_number, random_lower_letter, random_upper_letter, ])
        color = get_random_color()
        text_color = [0, 0, 0]
        #
        for j in range(2):
            if color[j]-background_color[j] <= 80:
                text_color[j] = 255-color[j]
            else:
                text_color[j] = color[j]
        draw.text((i * (width/4) + 10, 2),
                  rand_python[i],
                  tuple(text_color),
                  font=ImageFont.truetype(r'C:\Windows\Fonts\BRADHITC.TTF', 50),
                  align='center')

    # 3 释放画笔
    del draw
    # 存入session,用于做进一步的验证
    request.session['verification_code'] = rand_python
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    image.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
