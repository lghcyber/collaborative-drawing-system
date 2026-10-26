#include <SDL2/SDL.h>
#include <linux/input.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <thread>
#include <atomic>

std::atomic<int> mouseX1(0), mouseY1(0);
std::atomic<int> mouseX2(100), mouseY2(100);

bool running = true;

// Function to read from a mouse device and update position
void trackMouse(const char* device, std::atomic<int>& mouseX, std::atomic<int>& mouseY) {
    int fd = open(device, O_RDONLY);
    if (fd < 0) {
        std::cerr << "Failed to open " << device << std::endl;
        return;
    }

    struct input_event ie;
    while (running) {
        read(fd, &ie, sizeof(ie));
        if (ie.type == EV_REL) {
            if (ie.code == REL_X) {
                mouseX += ie.value;
            } else if (ie.code == REL_Y) {
                mouseY += ie.value;
            }
        }
    }

    close(fd);
}

// Function to draw a filled circle
void drawCircle(SDL_Renderer* renderer, int centerX, int centerY, int radius, SDL_Color color) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
    for (int w = 0; w < radius * 2; w++) {
        for (int h = 0; h < radius * 2; h++) {
            int dx = radius - w; // horizontal offset
            int dy = radius - h; // vertical offset
            if ((dx * dx + dy * dy) <= (radius * radius)) {
                SDL_RenderDrawPoint(renderer, centerX + dx, centerY + dy);
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "SDL_Init Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Collaborative Canvas", 100, 100, 1920, 1200, SDL_WINDOW_SHOWN);
    if (window == nullptr) {
        std::cerr << "SDL_CreateWindow Error: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (renderer == nullptr) {
        SDL_DestroyWindow(window);
        std::cerr << "SDL_CreateRenderer Error: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }

    // Launch threads to track each mouse
    std::thread mouse1_thread(trackMouse, "/dev/input/eventX", std::ref(mouseX1), std::ref(mouseY1)); // Replace 'eventX'
    std::thread mouse2_thread(trackMouse, "/dev/input/eventY", std::ref(mouseX2), std::ref(mouseY2)); // Replace 'eventY'

    bool quit = false;
    SDL_Event e;

    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = true;
            }
        }

        // Clear screen
        SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);
        SDL_RenderClear(renderer);

        // Draw the pointers
        drawCircle(renderer, mouseX1, mouseY1, 10, {255, 0, 0, 255});  // Red for first mouse
        drawCircle(renderer, mouseX2, mouseY2, 10, {0, 0, 255, 255});  // Blue for second mouse

        // Update screen
        SDL_RenderPresent(renderer);
    }

    // Stop the threads and wait for them to finish
    running = false;
    mouse1_thread.join();
    mouse2_thread.join();

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}