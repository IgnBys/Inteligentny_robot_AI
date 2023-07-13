import os
from PIL import Image

# Путь к папке с изображениями JPEG
jpeg_folder = "C:/Users/Lenovo/PycharmProjects/pythonProject/SI2023/TestJp"

# Путь к папке, в которую будут сохранены изображения PNG
png_folder = "C:/Users/Lenovo/PycharmProjects/pythonProject/SI2023/Test"

# Создание папки для PNG-изображений, если она не существует
if not os.path.exists(png_folder):
    os.makedirs(png_folder)

# Проход по каждому файлу в папке с JPEG-изображениями
for filename in os.listdir(jpeg_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        # Загрузка изображения
        image_path = os.path.join(jpeg_folder, filename)
        image = Image.open(image_path)

        # Создание пути для сохранения PNG-изображения
        png_filename = os.path.splitext(filename)[0] + ".png"
        png_path = os.path.join(png_folder, png_filename)

        # Конвертация и сохранение изображения в формате PNG
        image.save(png_path, "PNG")

        print(f"Конвертировано: {filename} -> {png_filename}")

print("Конвертация завершена.")
