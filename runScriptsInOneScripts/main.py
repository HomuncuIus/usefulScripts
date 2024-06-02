import subprocess

class autoRunScripts:
    def __init__(self):
        self.start_server_succeed = False
        self.start_client_succeed = False 
        self.terminate_server_succeed = False
        self.terminate_client_succeed = False
    
    def run_scripts(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return process
    
    def collect_info(self, process):
        result = []
        while True:
            result.append(process.stdout.readline().rstrip())
            if len(result)> 10:
                return result, False
        return result, False
    
    def terminate_process(self, process: subprocess.Popen):
        process.terminate()
        # 检查是否正常退出
        process.wait(10)
        if process.poll() is None:
            return False
        return True
    
    def check_process_status(self, processes:list[subprocess.Popen]):
        check_result = {}
        for process in processes:
            if process.poll() is None:
                continue
            check_result[process.pid] = process.stderr.readline().rstrip()
        return check_result
    
    def run(self, server_cmd, client_cmd):
        # 拉起server
        server_process = self.run_scripts(server_cmd)
        # 确认server正常运行
        while server_process.poll() is None:
            server_output = server_process.stdout.readline().rstrip()
            if 'ready' in server_output:
                print('detect server ready')
                self.start_server_succeed = True
                break
            
        # 拉起client
        client_process = self.run_scripts(client_cmd)
        # 确认client正常运行
        while server_process.poll() is None and client_process.poll() is None:
            client_output = client_process.stdout.readline().rstrip()
            if 'ready' in client_output:
                print('detect client ready')
                self.start_client_succeed = True
                break
                
        # 收集信息
        check_continue = True
        result = []
        while server_process.poll() is None and client_process.poll() is None and check_continue:
            result, check_continue = self.collect_info(server_process)
        
        # 终止client
        res = self.terminate_process(client_process)
        if res: 
            print('terminate client succeed')
            self.terminate_client_succeed = True
        
        # 终止server
        res = self.terminate_process(server_process)
        if res: 
            print('terminate server succeed')
            self.terminate_server_succeed = True
        
        return result
    
    def main(self, iter, server_cmd, client_cmd):
        for i in range(iter):
            print(self.run(server_cmd, client_cmd))
    
s = autoRunScripts()
s.main(50, 'bash ./test_server.sh 8080 0', 'bash ./test_client.sh 8080 0')





