from flask import Flask,jsonify,request,render_template,Response, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
import json
import requests
import shutil
import matplotlib.pyplot as plt
import datetime
from PIL import Image
import base64
import obj_test
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__,  static_folder="result_img")

def img():
    # 下載圖片
    request_data = request.get_json()
    r = requests.get(request_data['url'], stream=True)
    try:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        filename = "./get_img/get_img.jpg"
        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            f.write(r.content)
        print('成功下載圖檔: ', filename)
        """
        這邊呼叫 Yolov4 預測功能
        """
        result = obj_test.main(filename) # type --> dict
        
        return result

    except Exception as e :
        print(e,"\n 下載失敗")

@app.route('/post', methods=['POST','GET'])
def hellFlask_post():
    img_result = img()    
    update_result = {
        "result": img_result['result'],
        "url": "http://10.120.26.240:5000/"+ img_result['url']
    }
    print(update_result)
    return jsonify(update_result)
    
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)