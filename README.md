# Collaborative Multi-User Drawing System

A real-time collaborative drawing application that allows multiple users to draw simultaneously on a shared digital canvas using independently controlled input devices in a Linux environment.

The project explores multithreading, Linux input handling, synchronization, and human-computer interaction using Python, Pygame, evdev, and C++/SDL.

## 🎨 Project Overview

Traditional desktop environments are generally designed around a single mouse pointer.

This project explores an alternative approach by allowing multiple physical input devices to interact with the same drawing canvas simultaneously.

Each input device is handled independently, allowing multiple users to draw at the same time without relying on a single shared cursor.

## ✨ Key Features

- Multiple mouse/input device support
- Simultaneous real-time drawing
- Independent input processing
- Separate colors for different devices
- Persistent shared drawing canvas
- Multithreaded device handling
- Thread-safe drawing command queue
- Full-screen Pygame interface
- Linux input device integration
- Experimental Bluetooth device configuration
- C++/SDL multi-device prototype

## 🛠️ Technologies Used

### Languages

- Python
- C++

### Libraries & Frameworks

- Pygame
- evdev
- Python `threading`
- Python `queue`
- SDL2
- Linux Input API

### Platform & Tools

- Ubuntu / Linux
- `xinput`
- `bluetoothctl`
- Git
- GitHub

## 🧠 System Design

The application separates input collection from rendering.

Each physical input device is assigned its own worker thread. These threads continuously monitor Linux input events and send drawing commands to a shared thread-safe queue.

The main Pygame loop consumes those commands and renders them onto the shared canvas.

```text
Input Device 1 ──> Device Thread ──┐
                                   │
Input Device 2 ──> Device Thread ──┼──> Thread-Safe Queue
                                   │          │
Additional Devices ────────────────┘          ▼
                                        Main Pygame Loop
                                              │
                                              ▼
                                      Shared Drawing Canvas
```

This architecture allows input devices to operate independently while maintaining a centralized rendering process.

## 🧵 Multithreading

One of the main challenges of the project was processing multiple input devices at the same time.

Each configured device runs through an independent Python thread:

```python
thread = threading.Thread(
    target=handle_device,
    args=(path, color, draw_queue, stop_threads)
)
```

This allows the application to continuously monitor multiple Linux input devices without blocking the main graphical interface.

## 🔄 Thread-Safe Communication

Input threads do not draw directly to the Pygame surface.

Instead, each thread sends drawing commands to a shared `Queue`:

```python
draw_queue.put((x, y, color, device_path))
```

The main application loop processes those commands:

```python
x, y, color, device_path = draw_queue.get_nowait()
pygame.draw.circle(drawing_surface, color, (x, y), 5)
```

Using a queue separates device input handling from graphical rendering and provides a safer way for multiple threads to communicate with the main application.

## 🖱️ Linux Input Handling

The project uses the `evdev` library to read events directly from Linux input devices.

Example device paths:

```text
/dev/input/event4
/dev/input/event6
```

Relative movement events are monitored using:

- `REL_X`
- `REL_Y`

Each device maintains its own position on the canvas.

## 🎨 Shared Drawing Canvas

Pygame provides the graphical interface and persistent drawing surface.

Different devices can be assigned different colors so their input can be visually distinguished.

Example colors include:

- Red
- Green
- Blue
- Yellow

The application also displays an independent pointer indicator for each configured device.

## 📡 Bluetooth & Virtual Pointer Experimentation

The project includes an experimental Python utility for interacting with Linux Bluetooth and input-device management tools.

`automate_bluetooth.py` explores:

- Listing Bluetooth devices
- Identifying devices by name
- Connecting through `bluetoothctl`
- Creating virtual pointer devices using `xinput`
- Reattaching input devices to virtual pointers

This component represents experimentation with Linux-level input management rather than a requirement for running the main drawing application.

## 💻 C++ / SDL Prototype

The repository also contains an experimental C++ implementation using SDL2 and the Linux Input API.

The prototype explores:

- Reading `/dev/input/event*` devices directly
- Tracking multiple mouse positions
- Using independent C++ threads
- Atomic position variables
- SDL rendering
- Multiple pointer visualization

This provided another approach for investigating low-level multi-device input handling.

## 📁 Repository Structure

```text
collaborative-drawing-system/
│
├── canvas.py
├── automate_bluetooth.py
├── sdl.cpp
└── README.md
```

### `canvas.py`

Primary Python implementation of the collaborative drawing system.

Handles:

- Multiple input devices
- Multithreading
- Drawing command queue
- Pygame rendering
- Device-specific colors
- Shared canvas interaction

### `automate_bluetooth.py`

Experimental Linux device-management utility for Bluetooth connections and virtual pointer creation.

### `sdl.cpp`

C++/SDL prototype for directly reading Linux input events from multiple devices.

## ▶️ Running the Python Application

### Requirements

The project is designed for a Linux environment.

Install the required Python packages:

```bash
pip install pygame evdev
```

Linux input devices are typically available under:

```text
/dev/input/
```

Update the device paths in `canvas.py` to match the input devices on your system:

```python
device_paths = [
    '/dev/input/event4',
    '/dev/input/event6'
]
```

Then run:

```bash
python3 canvas.py
```

> Accessing `/dev/input/event*` devices may require appropriate Linux permissions. Device paths vary between systems.

## ⚠️ Current Limitations

The project currently has several limitations:

- Designed and tested for Linux/Ubuntu
- Input device paths are configured manually
- Device paths vary between systems
- High input volume may introduce latency
- Collaboration is local rather than network-based
- Bluetooth support remains experimental
- No user authentication
- No persistent user profiles

## 🚀 Potential Improvements

Future improvements could include:

- Automatic input-device discovery
- Cross-platform Windows/macOS support
- Remote network collaboration
- User-specific cursor labels
- Dynamic color assignment
- Improved Bluetooth support
- Drawing tools such as shapes and brushes
- Layers
- Save/load functionality
- User profiles and permissions
- Improved synchronization under high input volume

## 💡 Skills Demonstrated

This project demonstrates practical experience with:

- Python
- C++
- Linux
- Multithreading
- Concurrent programming
- Input device handling
- Event-driven programming
- Thread-safe queues
- Pygame
- SDL2
- Human-computer interaction
- Shared-resource management
- Troubleshooting hardware/software integration

## 🎓 Project Context

This project was developed as a collaborative academic project at the University of South Carolina Upstate.

The goal was to explore operating-system concepts, concurrent input processing, and real-time multi-user interaction through a shared drawing environment.

## 👤 Author

**Alani Hodge**  
Cybersecurity Student | Security Operations | Threat Detection

[LinkedIn](https://www.linkedin.com/in/alani-hodge) | [GitHub](https://github.com/lghcyber)
