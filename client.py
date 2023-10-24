import requests
from PIL import Image
from io import BytesIO
import base64
import json

# 读取待推理的图像文件
image_path = './datasets/image-parse-v3.png'
with open(image_path, 'rb') as f:
    image_data = f.read()

# 将图像数据进行 base64 编码
encoded_image = base64.b64encode(image_data).decode('utf-8')

# 读取 openpose_json.json 文件
with open('./datasets/openpose_json.json', 'r') as f:
    openpose_json = json.load(f)

# 构造请求数据
data = {'image-parse-v3': encoded_image, 'openpose_json': openpose_json}
headers = {'Content-Type': 'application/json'}

# 发送 POST 请求到服务器
url = 'http://10.12.120.176:5004/infer'  # 根据实际情况修改 URL
response = requests.post(url, data=json.dumps(data), headers=headers)

# 解析服务器返回的 JSON 数据
result = response.json()

# 推理结果图像数据
output_image_data = result['result']['output_image']

# 解码返回的图像数据
decoded_image = base64.b64decode(output_image_data)

# 将解码后的图像数据加载为 PIL 图像对象
output_image = Image.open(BytesIO(decoded_image))

# 展示图像
output_image.show()
