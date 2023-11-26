import os
import cv2
import numpy as np

path_file = "Neymark.mp4"  # Путь к видео
scale = 3  # Фактор уменьшения
path_folder = f"Neymark"  # Путь к папке

# Проверяем наличие папки
path_folder += f" ({scale})"
folder_exists = os.path.exists(path_folder)

if not folder_exists:
    os.makedirs(path_folder)
    print(f"New folder '{path_folder}' created!")


# Алгоритм дизеринга Флойда-Штейнберга
def floyd_steinberg_dithering(image):
    height, width = image.shape
    output_image = np.empty((height, width), dtype=str)

    for y in range(height - 1):
        for x in range(1, width - 1):
            old_pixel = image[y, x]
            new_pixel = '#' if old_pixel > 128 else ' '
            output_image[y, x] = new_pixel
            error = old_pixel - (255 if new_pixel == '#' else 0)

            # Распространение ошибки
            image[y, x + 1] += (error * 7) // 16
            image[y + 1, x - 1] += (error * 3) // 16
            image[y + 1, x] += (error * 5) // 16
            image[y + 1, x + 1] += (error * 1) // 16

    return output_image


# Функция для подсчёта количества кадров в видео
def count_frame(video):
    frame_counter = 0
    while True:
        ret, _ = video.read()  # Считывание кадра, чтобы узнать, есть ли ещё кадры
        if not ret:  # Если кадр не считался, значит видео закончилось
            break
        frame_counter += 1  # Увеличиваем счётчик кадров
    return frame_counter  # Возвращаем общее количество кадров в видео


# Функция для списка последних кадров, которые нужно обработать
def last_frame(count: int) -> list:
    # Получаем список обработанных кадров
    files = [int(f.split(".")[0]) for f in os.listdir(path_folder) if f.split(".")[0].isdigit()]
    # Если все кадры ещё не обработаны, возвращаем список всех кадров, иначе только непрошедшие обработку
    return list(range(count)) if not files else [x for x in range(count) if x not in files]


# Функция для уменьшения размера и преобразования кадра в черно-белый
def resize_frame(frame, scale):
    small_frame = cv2.resize(frame, (frame.shape[1] // scale, frame.shape[0] // scale))  # Уменьшаем размер кадра
    small_frame_bw = np.mean(small_frame, axis=2)  # Преобразовываем в оттенки серого, усредняя значения по третьей оси
    return floyd_steinberg_dithering(small_frame_bw)  # Применяем алгоритм дизеринга


# Функция для обработки отдельного кадра
def handle_frame(frame_number, video, frame_count):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  # Устанавливаем позицию чтения на нужный кадр
    is_success, frame = video.read()  # Считываем кадр
    if not is_success:  # Если кадр не считался, выводим сообщение об ошибке
        print(f"Error reading frame {frame_number}")
        return
    small_frame = resize_frame(frame, scale)  # Получаем уменьшенный черно-белый кадр
    with open(f'{path_folder}/{frame_number}.txt', 'w') as f:  # Открываем файл для записи кадра
        for row in small_frame:
            row_str = ' '.join(map(str, row))  # Преобразование каждой строки в строку
            f.write(row_str + '\n')  # Запись строки в файл
    print(f"Finish: {frame_number}/{frame_count}")  # Выводим сообщение об окончании обработки кадра


# Основная функция
def main():
    video = cv2.VideoCapture(path_file)  # Открываем видеофайл
    if not video.isOpened():  # Проверяем, успешно ли открыт видеофайл
        print("Error opening video")
        return
    else:
        print("Opening video Finish")

    frame_count = count_frame(video)  # Получаем количество кадров в видео
    frames_to_process = last_frame(frame_count)  # Получаем кадры для обработки
    for f in frames_to_process:
        handle_frame(f, video, frame_count)  # Обрабатываем каждый кадр

    video.release()  # Закрываем видеофайл


# Вызов основной функции
main()
