import psutil
import time
import os
from collections import deque
from colorama import init, Fore, Back, Style
import plotext as plt

# Initialize colorama and set background to black
init()
os.system('color 0f' if os.name == 'nt' else 'tput setab 0')
print(Back.BLACK + Fore.WHITE + Style.BRIGHT)

def get_size(bytes):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"
        bytes /= factor

def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

# Increase the number of data points for a more stretched graph
sent_data = deque([0], maxlen=100)
recv_data = deque([0], maxlen=100)
time_data = deque([0], maxlen=100)

last_sent, last_recv = get_network_usage()

def update_plot():
    global last_sent, last_recv

    current_sent, current_recv = get_network_usage()
    sent_diff = max(0, current_sent - last_sent)
    recv_diff = max(0, current_recv - last_recv)
    last_sent, last_recv = current_sent, current_recv

    sent_data.append(sent_diff)
    recv_data.append(recv_diff)
    time_data.append(time_data[-1] + 1)

    plt.clf()
    plt.plotsize(100, 20)
    
    # Create a fully dark background
    plt.canvas_color("black")
    plt.axes_color("black")
    plt.ticks_color("dark_green")
    plt.frame(False)
    plt.grid(False)
    
    plt.plot(time_data, sent_data, color="green", marker="dot", label="Sent")
    plt.plot(time_data, recv_data, color="blue", marker="dot", label="Received")
    
    # Set title with legend
    title = plt.colorize("Network Traffic\n", "dark_green")
    title += plt.colorize("Sent", "green") + "  " + plt.colorize("•• Received", "blue")
    plt.title(title)
    
    plt.xlabel(plt.colorize("Time (seconds)", "dark_green"))
    plt.ylabel(plt.colorize("Traffic (bytes/s)", "dark_green"))
    
    max_y = max(max(sent_data), max(recv_data), 1)  # Ensure max_y is at least 1
    plt.ylim(0, max_y * 1.2)  # Set y-axis limit

def main():
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system('color 0f' if os.name == 'nt' else 'tput setab 0')
            print(Back.BLACK + ' ' * 10000)  # Fill the screen with black
            
            update_plot()
            plt.show()
            
            print(Fore.CYAN + "=== System Statistics ===" + Style.RESET_ALL)
            print(Back.BLACK + f"CPU Usage: {Fore.YELLOW}{psutil.cpu_percent()}%{Style.RESET_ALL}")
            
            memory = psutil.virtual_memory()
            print(Back.BLACK + f"Memory Usage: {Fore.YELLOW}{memory.percent}%{Style.RESET_ALL} ({get_size(memory.used)} / {get_size(memory.total)})")
            
            disk = psutil.disk_usage('/')
            print(Back.BLACK + f"Disk Usage: {Fore.YELLOW}{disk.percent}%{Style.RESET_ALL} ({get_size(disk.used)} / {get_size(disk.total)})")
            
            print(Back.BLACK + f"\nNetwork: Sent: {Fore.GREEN}{get_size(sent_data[-1])}/s{Style.RESET_ALL}, Received: {Fore.BLUE}{get_size(recv_data[-1])}/s{Style.RESET_ALL}")
            
            print(Back.BLACK + Fore.RED + "\nPress Ctrl+C to exit." + Style.RESET_ALL)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        print(Style.RESET_ALL)  # Reset colors when exiting
        os.system('color' if os.name == 'nt' else 'tput sgr0')  # Reset terminal colors

if __name__ == "__main__":
    main()
