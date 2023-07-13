import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img

class_names = ['Bluza', 'Telefon', 'Pilka']


def train():
    # Задайте пути к каталогам и создайте список названий классов
    train_directory = 'C:/Users/Lenovo/PycharmProjects/pythonProject/SI2023/Train'
    validation_directory = 'C:/Users/Lenovo/PycharmProjects/pythonProject/SI2023/Validation'

    # Создание генератора данных для обучения и валидации
    train_datagen = ImageDataGenerator(rescale=1./255)
    validation_datagen = ImageDataGenerator(rescale=1./255)

    # Загрузка обучающих и валидационных изображений из каталогов
    train_generator = train_datagen.flow_from_directory(
        train_directory,
        target_size=(256, 256),
        batch_size=32,
        class_mode='categorical'
    )

    validation_generator = validation_datagen.flow_from_directory(
        validation_directory,
        target_size=(256, 256),
        batch_size=32,
        class_mode='categorical'
    )

    # Создание модели
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=( 256,256, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(class_names), activation='softmax')
    ])

    # Компиляция модели
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Обучение модели
    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size,
        epochs=10
    )
    model.save(r"C:\Users\Lenovo\PycharmProjects\pythonProject\SI2023\model.h5")
def load():
    results_df = pd.DataFrame(columns=['File_Name', 'Class'])

    model=keras.models.load_model(r"C:\Users\Lenovo\PycharmProjects\pythonProject\SI2023\model.h5")
    # Задайте путь к каталогу Test
    test_directory = 'C:/Users/Lenovo/PycharmProjects/pythonProject/SI2023/Test'

    # Проход по файлам в каталоге Test
    for filename in os.listdir(test_directory):
        if filename.endswith(".png"):
            file_path = os.path.join(test_directory, filename)
            image = load_img(file_path, target_size=(256, 256))
            image_array = img_to_array(image) / 255.0
            image_array = tf.expand_dims(image_array, axis=0)

            # Получение предсказаний от модели
            predictions = model.predict(image_array)
            predicted_class_index = tf.argmax(predictions[0])
            predicted_class = class_names[predicted_class_index]

            # Запись результатов в фрейм данных
            results_df = pd.concat([results_df, pd.DataFrame({'File_Name': [filename], 'Class': [predicted_class]})], ignore_index=True)


    # Подсчет количества файлов для каждого класса
    class_counts = results_df['Class'].value_counts()

    # Получение названия класса с наибольшим количеством файлов
    most_common_class = class_counts.idxmax()
    if os.path.exists('data.csv'):
        os.remove('data.csv')
    # Запись результатов в файл data.csv
    results_df.to_csv('data.csv', index=False)

    print(f"Класс с наибольшим количеством сходств: {most_common_class}")
if __name__ == "__main__":
    load()