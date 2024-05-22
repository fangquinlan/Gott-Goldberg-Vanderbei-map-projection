import cupy as cp
import numpy as np
from PIL import Image

# 增加Pillow的图像大小限制
Image.MAX_IMAGE_PIXELS = None

# 加载图像
blue_marble = Image.open("eo_base_2020_clean_geo.tif")
width, height = blue_marble.size

# 将图像数据转换为NumPy数组，然后转换为CuPy数组
blue_marble_array = cp.array(blue_marble)

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

# 创建北半球和南半球的投影结果的新图像，背景为透明
output_image_north = cp.zeros((height, width, 4), dtype=cp.uint8)
output_image_south = cp.zeros((height, width, 4), dtype=cp.uint8)

# 将背景设置为完全透明
output_image_north[..., 3] = 0
output_image_south[..., 3] = 0

# 设置有效像素的颜色和不透明度
output_image_north[north_proj_y, north_proj_x, :3] = blue_marble_array[north_mask]
output_image_north[north_proj_y, north_proj_x, 3] = 255

output_image_south[south_proj_y, south_proj_x, :3] = blue_marble_array[south_mask]
output_image_south[south_proj_y, south_proj_x, 3] = 255

# 将CuPy数组转换为NumPy数组，然后转换为Pillow图像
output_image_north_pil = Image.fromarray(cp.asnumpy(output_image_north), mode='RGBA')
output_image_south_pil = Image.fromarray(cp.asnumpy(output_image_south), mode='RGBA')

# 去除透明背景，裁剪到圆形地图
def crop_to_circle(img):
    np_img = np.array(img)
    h, w, _ = np_img.shape
    radius = min(h, w) // 2
    center = (w // 2, h // 2)

    y, x = np.ogrid[:h, :w]
    mask = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2

    cropped_img = np.zeros((2*radius, 2*radius, 4), dtype=np.uint8)
    cropped_img[..., 3] = 0  # 初始化为完全透明
    cropped_img[mask[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]] = np_img[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius][mask[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]]

    return Image.fromarray(cropped_img, mode='RGBA')

output_image_north_cropped = crop_to_circle(output_image_north_pil)
output_image_south_cropped = crop_to_circle(output_image_south_pil)

# 保存结果
output_image_north_cropped.save("Complete_Northern_Hemisphere_Map.png")
output_image_south_cropped.save("Complete_Southern_Hemisphere_Map.png")

# 显示结果
output_image_north_cropped.show()
output_image_south_cropped.show()
