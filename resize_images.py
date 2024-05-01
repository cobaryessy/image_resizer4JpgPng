import os
import argparse
from PIL import Image

# 引数の設定
parser = argparse.ArgumentParser(description='Resize images in a folder')
parser.add_argument('source_folder', type=str, help='Path to the folder containing images')
parser.add_argument('target_folder', type=str, help='Path to the folder to save resized images')
parser.add_argument('width', type=int, help='Desired width of the resized images')
parser.add_argument('height', type=int, help='Desired height of the resized images')
parser.add_argument('--blackback', action='store_true', help='Fill the background with black instead of white')
args = parser.parse_args()

# 出力フォルダーが存在しない場合は作成
os.makedirs(args.target_folder, exist_ok=True)

# 画像をリサイズする関数
def resize_image(image, target_width, target_height, black_background):
    width, height = image.size
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height
    
    # 画像のアスペクト比と目標のアスペクト比を比較
    if aspect_ratio > target_aspect_ratio:
        # 横長の画像
        new_height = int(target_width / aspect_ratio)
        resized_image = image.resize((target_width, new_height), Image.LANCZOS)
    elif aspect_ratio < target_aspect_ratio:
        # 縦長の画像
        new_width = int(target_height * aspect_ratio)
        resized_image = image.resize((new_width, target_height), Image.LANCZOS)
    else:
        # アスペクト比が一致する場合はそのままリサイズ
        resized_image = image.resize((target_width, target_height), Image.LANCZOS)
    
    # 指定のサイズに合わせて画像を作成
    if black_background:
        new_image = Image.new('RGB', (target_width, target_height), (0, 0, 0))
    else:
        new_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))
    
    # 画像を中央に配置
    x_offset = (target_width - resized_image.size[0]) // 2
    y_offset = (target_height - resized_image.size[1]) // 2
    new_image.paste(resized_image, (x_offset, y_offset))
    
    return new_image

# ソースフォルダー内のファイルをループ
for filename in os.listdir(args.source_folder):
    # 拡張子が.jpgまたは.pngの場合のみ処理する
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # 画像ファイルのパスを作成
        img_path = os.path.join(args.source_folder, filename)
        
        # 画像を開く
        img = Image.open(img_path)
        
        # 画像のサイズを取得
        width, height = img.size
        
        # 画像のサイズが指定のサイズと異なる場合のみ処理する
        if width != args.width or height != args.height:
            # 画像をリサイズ
            img = resize_image(img, args.width, args.height, args.blackback)
            
            # 新しいファイル名を作成
            new_filename = os.path.splitext(filename)[0] + '_resized' + os.path.splitext(filename)[1]
            new_path = os.path.join(args.target_folder, new_filename)
            
            # 画像を保存
            img.save(new_path)
            print(f'Resized {filename} to {new_filename}')
