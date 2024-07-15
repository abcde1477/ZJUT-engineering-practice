import requests

class NetworkInteract:
    def __init__(self, url):
        self.add_task_url = url + "/post-task"
        self.get_task_url = url + "/get-task"

    def add_task(self, task):
        response = requests.post(self.add_task_url, json=task)
        if response.status_code == 200:
            print("任务添加成功")
        else:
            print("添加任务失败:", response.status_code)

    def get_task(self):
        response = requests.get(self.get_task_url)
        if response.status_code == 200:
            try:
                task = response.json()
                print("获取任务:", task)
                return task
            except ValueError:
                print("响应不是 JSON 格式")
        else:
            print("获取任务失败:", response.status_code)

if __name__ == "__main__":
    network = NetworkInteract("http://192.168.109.127:3000")
    
    # 添加任务示例
    task_to_add = [
         {
        "fid":'A1',
        "color": 'blue',
        "icon": 'mdi-clipboard-text',
        "subtitle": '2024-7-8 7:24',
        "title": '小车前往 A[2][3] 取货',
         
          },
        {
        "fid":'A2',
        "color": 'amber',
        "icon": 'mdi-clipboard-text',
        "subtitle": '2024-7-8 18:02',
        "title": '小车前往 A[4][4] 取货'
        }
    ]
    network.add_task(task_to_add)
    
    # 获取任务示例
    task = network.get_task()
    if task:
        print("处理任务:", task)
    else:
        print("没有可用任务")
        
        
# task的形式1：
        # {
        # "task_id": 321
        # "task_type": "fetch"
        # "from": (4, 5)
        # "description":"前往A2货柜取货"

        # -------------------

        # task的形式2：
        # {
        # "task_id": 322
        # "task_type": "directlyControl"
        # "turn" : "LEFT" 或"RIGHT"
        # "go_ahead" :2
        # "description":"左转，前进2"
        # }