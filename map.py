import numpy as np
from PIL import Image

# 加载图像
blue_marble = Image.open("BlueMarbleNG.png")
width, height = blue_marble.size

# 创建北半球和南半球的投影结果的新图像，背景为白色
output_image_north = Image.new('RGB', (width, height), 'white')
output_image_south = Image.new('RGB', (width, height), 'white')
north_pixels = output_image_north.load()
south_pixels = output_image_south.load()

# 定义转换函数
def latlon_to_projection(lat, lon, hemisphere):
    theta = np.deg2rad(90 - lat) if hemisphere == 'north' else np.deg2rad(-90 - lat)
    phi = np.deg2rad(lon)
    
    # 投影公式
    r = theta / np.pi * height / 2
    x = int(r * np.cos(phi) + width / 2)
    y = int(r * np.sin(phi) + height / 2)
    
    return x, y

# 进行投影并生成新图像
for y in range(height):
    lat = 90 - (y / height) * 180  # 从90度到-90度
    for x in range(width):
        lon = (x / width) * 360 - 180  # 从-180度到180度
        if lat >= 0:  # 北半球
            proj_x, proj_y = latlon_to_projection(lat, lon, hemisphere='north')
            if 0 <= proj_x < width and 0 <= proj_y < height:
                # 使用双线性插值
                north_pixels[proj_x, proj_y] = blue_marble.getpixel((x, y))
        else:  # 南半球
            proj_x, proj_y = latlon_to_projection(lat, lon, hemisphere='south')
            if 0 <= proj_x < width and 0 <= proj_y < height:
                # 使用双线性插值
                south_pixels[proj_x, proj_y] = blue_marble.getpixel((x, y))

# 保存结果
output_image_north.save("Complete_Northern_Hemisphere_Map.png")
output_image_south.save("Complete_Southern_Hemisphere_Map.png")

# 显示结果
output_image_north.show()
output_image_south.show()
