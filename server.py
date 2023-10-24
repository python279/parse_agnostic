from get_parse_agnostic import get_im_parse_agnostic
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from base64 import b64decode, b64encode
import numpy as np

app = Flask(__name__)


@app.route('/infer', methods=['POST'])
def infer():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    image_parse_v3 = data["image-parse-v3"]
    openpose_json = data["openpose_json"]

    # 从 base64 解码出图片
    image = Image.open(BytesIO(b64decode(image_parse_v3)))

    # 从 openpose_json 中解析出人体姿态数据
    pose_data = openpose_json['people'][0]['pose_keypoints_2d']
    pose_data = np.array(pose_data)
    pose_data = pose_data.reshape((-1, 3))[:, :2]

    # 进行推理
    output_image = get_im_parse_agnostic(image, pose_data, w=image.width, h=image.height)
    buffered = BytesIO()
    output_image.save(buffered, format='PNG')
    output_image = b64encode(buffered.getvalue()).decode('utf-8')
    result = {'result': {'output_image': output_image}}
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
