#!/usr/bin/env python
# coding: utf-8

# 1. 사용자로부터 이미지 받아오기
# 2. 방아온 이미지에 대하여 AI 허브의 API를 이용해 객체 구분 및 객체명 표시하기
# 3. 해당 이미지 저장 후 화면으로 출력하기

# html 파일들은 하위의 tamplates 폴더에 넣을것.
# 이미지는 하위 폴더인 static/img/를 생성해 저장해줬다.

# In[1]:


from flask import Flask, render_template, url_for , request
import numpy as np
import os
import time
import urllib3
import json
import sys
import base64
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt


# In[2]:


def draw(fname, fdir):
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"   # API 연결 URL
    accessKey = "56c9feb4-5561-4a72-9988-684bad086e3a"          # 사용자 인증키   
    imageFilePath = fdir + fname# 대상 이미지
    type = imageFilePath.split('.')[-1]

    file = open(imageFilePath, "rb")
    imageContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    # 이미지를 JSON 형식으로 만들어줌. 
    # 딕셔너리 구조
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "type": type,
            "file": imageContents
        }
    }

    # url로 요청하면 줌.
    # request 형태는 POST 형태 
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        # 인증
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    time.sleep(3)
    if response.status != 200:
        sys.exit('데이터를 받아오지 못했습니다.')

    json_data = json.loads(response.data)

    ## 이미지 분석 데이터 가져오기
    json_data = json.loads(response.data)

    # 객체에 대한 이미지 정보
    img_data = json_data['return_object']['data']

    img = Image.open(imageFilePath)

    # 이미지에서 사용할 폰트 설정
    font = ImageFont.truetype("C:/Windows/Fonts/MalangmalangR.ttf", 45)

    # 읽어온 이미지에 선을 추가 가능한 이미지로 변셩
    draw_img = ImageDraw.Draw(img)

    for i in range(len(img_data)):
        info_img = img_data[i]

        # 1. 객체 정보 추출
        thing = info_img['class']
        x = int(info_img['x'])
        y = int(info_img['y'])
        w = int(info_img['width'])
        h = int(info_img['height'])

        # 2. 이미지에 객체 정보를 이용해 선 그리기
        # 2.1. 색상 지정
        if thing == 'person':
            color = (240, 210, 240) 
            draw_img.line([(x, y), (x,y+h), (x+w,y+h), (x+w, y), (x, y)], fill = color, width = 5)
            draw_img.text((x, y-50), thing, font = font, fill = color)
        else:
            color = (0, 200, 0) 
            draw_img.line([(x, y), (x,y+h), (x+w,y+h), (x+w, y), (x, y)], fill = color, width = 5)
            draw_img.text((x, y-50), thing, font = font, fill = color)
    
    img.save('./static/img/d_'+ fname)


# In[3]:


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_loading():
    # request 결과가 GET이면 화면에 뿌리기
    if request.method == 'GET':
        return render_template('home_img.html')

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    # 파일 정보 받아오기
    file = request.files['file']
    fname = file.filename
    
    file.save(os.path.join('static/img/', fname))
    time.sleep(3)
    
    draw(fname, os.path.join('static/img/'))
    f_name = '/img/d_'+ fname
    return render_template('home_img.html', f_name = f_name)
    
if __name__ == '__main__':
    app.run()





