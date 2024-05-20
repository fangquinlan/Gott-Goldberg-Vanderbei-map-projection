import cupy as cp
import numpy as np
from PIL import Image

# 增加Pillow的图像大小限制
Image.MAX_IMAGE_PIXELS = None

# 加载图像并转换为灰度模式
blue_marble = Image.open("gebco.png").convert("L")
width, height = blue_marble.size

# 将图像数据转换为NumPy数组，然后转换为CuPy数组
blue_marble_array = cp.array(blue_marble)

# 创建北半球和南半球的投影结果的新图像，背景为白色
output_image_north = cp.ones((height, width), dtype=cp.uint8) * 255
output_image_south = cp.ones((height, width), dtype=cp.uint8) * 255

# 定义转换函数
def latlon_to_projection(lat, lon, hemisphere):
    theta = cp.deg2rad(90 - lat) if hemisphere == 'north' else cp.deg2rad(-90 - lat)
    phi = cp.deg2rad(lon)
    
    # 投影公式
    r = theta / cp.pi * height / 2
    x = (r * cp.cos(phi) + width / 2).astype(cp.int32)
    y = (r * cp.sin(phi) + height / 2).astype(cp.int32)
    
    return x, y

# 创建经纬度网格
lon, lat = cp.meshgrid(cp.linspace(-180, 180, width), cp.linspace(90, -90, height))

# 进行投影并生成新图像
north_mask = lat >= 0
south_mask = ~north_mask

north_proj_x, north_proj_y = latlon_to_projection(lat[north_mask], lon[north_mask], hemisphere='north')
south_proj_x, south_proj_y = latlon_to_projection(lat[south_mask], lon[south_mask], hemisphere='south')

# 保证索引一致性
blue_marble_north = blue_marble_array[north_mask].reshape(-1)
blue_marble_south = blue_marble_array[south_mask].reshape(-1)

# 使用索引填充新图像
output_image_north[north_proj_y, north_proj_x] = blue_marble_north
output_image_south[south_proj_y, south_proj_x] = blue_marble_south

# 将CuPy数组转换为NumPy数组，然后转换为Pillow图像
output_image_north = Image.fromarray(cp.asnumpy(output_image_north))
output_image_south = Image.fromarray(cp.asnumpy(output_image_south))

# 保存结果
output_image_north.save("Complete_Northern_Hemisphere_Map.png")
output_image_south.save("Complete_Southern_Hemisphere_Map.png")

# 显示结果
output_image_north.show()
output_image_south.show()
