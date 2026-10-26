import threading
import pygame
import evdev
from evdev import InputDevice, categorize, ecodes
from queue import Queue, Empty

# Initialize Pygame
pygame.init()

# Set up the drawing window to fill the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Simultaneous Drawing with Multiple Devices")

# Hide the system mouse pointer
pygame.mouse.set_visible(False)

# Create a surface to store drawings
drawing_surface = pygame.Surface((screen_width, screen_height))
drawing_surface.fill((0, 0, 0))  # Fill with black initially

# Colors for different devices
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Queue for drawing commands
draw_queue = Queue()

# Flag to signal threads to stop
stop_threads = threading.Event()

def handle_device(device_path, color, draw_queue, stop_event):
    """Handle input events from a specific device."""
    device = InputDevice(device_path)
    print(f"Listening to {device.name} at {device_path}")

    # Start position for drawing (center of the screen)
    x, y = screen_width // 2, screen_height // 2

    for event in device.read_loop():
        if stop_event.is_set():
            break

        if event.type == ecodes.EV_REL:
            if event.code == ecodes.REL_X:
                x += event.value
            elif event.code == ecodes.REL_Y:
                y += event.value

            # Ensure the position stays within screen boundaries
            x = max(0, min(screen_width, x))
            y = max(0, min(screen_height, y))

            # Add drawing command to the queue
            draw_queue.put((x, y, color, device_path))

def draw_exit_button(screen):
    """Draw an exit button on the screen."""
    button_rect = pygame.Rect(screen_width - 100, 10, 80, 30)
    pygame.draw.rect(screen, (200, 0, 0), button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render('Exit', True, (255, 255, 255))
    screen.blit(text, (screen_width - 90, 15))
    return button_rect

def main():
    # List of device paths (replace with actual paths)
    device_paths = ['/dev/input/event4', '/dev/input/event6']

    threads = []
    for i, path in enumerate(device_paths):
        color = colors[i % len(colors)]  # Cycle through colors
        thread = threading.Thread(target=handle_device, args=(path, color, draw_queue, stop_threads))
        thread.start()
        threads.append(thread)

    # Main loop to keep the Pygame window open and process drawing commands
    running = True
    last_positions = {path: (screen_width // 2, screen_height // 2) for path in device_paths}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                stop_threads.set()  # Signal threads to stop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    running = False
                    stop_threads.set()  # Signal threads to stop

        # Process drawing commands from the queue
        try:
            while True:
                x, y, color, device_path = draw_queue.get_nowait()
                pygame.draw.circle(drawing_surface, color, (x, y), 5)
                last_positions[device_path] = (x, y)
        except Empty:
            pass

        # Draw the persistent drawing surface onto the screen
        screen.blit(drawing_surface, (0, 0))

        # Draw the pointer symbols for each device
        for device_path, (x, y) in last_positions.items():
            pygame.draw.rect(screen, (255, 255, 255), (x - 10, y - 10, 20, 20), 2)

        # Draw the exit button
        exit_button = draw_exit_button(screen)

        pygame.display.flip()

    for thread in threads:
        thread.join()

    pygame.quit()

if __name__ == "__main__":
    main()