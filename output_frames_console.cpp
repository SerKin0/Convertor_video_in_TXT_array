#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <windows.h>

int main() {
    std::vector<std::string> frames;

    for (int i = 0; i < 2377; i++) {
        std::string filePath = "D:\\Development\\Convertor_video_in_TXT_array\\Neymark (3)\\" + std::to_string(i) + ".txt";
        std::ifstream myfile(filePath);
        std::string frameData;
        std::string combinedFrames;

        if (myfile.is_open()) {
            while (std::getline(myfile, frameData)) {
                combinedFrames += frameData + "\n";
            }
            frames.push_back(combinedFrames);
            myfile.close();
        }
    }

    // Вывод информации
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD bufferSize = { 200, 500 };  // устанавливаем размер буфера консоли
    SetConsoleScreenBufferSize(hConsole, bufferSize);

    for (int i = 0; i < 2400; i++) {
        system("cls");
        std::cout << i << std::endl;
        if (i < frames.size()) {
            std::cout << frames[i] << std::endl;
        }
    }

    return 0;
}
