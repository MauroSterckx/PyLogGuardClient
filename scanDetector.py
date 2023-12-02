import socket
import threading

# from PyLogGuardClient import sendLog
import PyLogGuardClient

HostName = "test"


def start_listener(port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    # listener.bind(("0.0.0.0", port))
    listener.bind(("127.0.0.1", port))
    listener.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # listener.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        data = listener.recvfrom(65565)
        packet = data[0]

        # Check for SYN packets (indicative of a TCP connect scan)
        if packet[33] == 0x02:
            # print(f"Portscan detected from {data[1][0]} on port {port}")
            PyLogGuardClient.sendOwnLog(
                data=f"Portscan detected from {data[1][0]} on port {port} ",
                logtype="Portscan",
                hostname=HostName,
            )


def main(ports_to_monitor=[80, 443, 8080, 22, 21, 23, 25, 110, 143, 993, 995]):
    # Start the listener in a separate thread for each port
    listener_threads = [
        threading.Thread(target=start_listener, args=(port,))
        for port in ports_to_monitor
    ]
    for thread in listener_threads:
        thread.start()

    try:
        # Wait for each thread to complete
        for thread in listener_threads:
            thread.join()
    except KeyboardInterrupt:
        pass
    # finally:
    #     # Cleanup code (turn off promiscuous mode)
    #     for port in ports_to_monitor:
    #         listener.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == "__main__":
    main()
