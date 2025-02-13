import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import time

# 检查余额函数
def check_balance(api_key):
    url = 'https://api.siliconflow.cn/v1/user/info'
    headers = {
        'Authorization': f'Bearer {api_key.strip()}'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            if data.get('data', {}).get('balance') is not None:
                return f"✅ {data['data']['balance']} {api_key}"
            else:
                return f"❌ {api_key}, 无效响应数据"
        else:
            return f"❌ {api_key}, HTTP错误 {response.status_code}"
    except requests.exceptions.RequestException as error:
        return f"❌ {api_key}, 请求错误: {error}"

# 点击事件处理
def on_check_balance():
    keys = textarea.get("1.0", tk.END).strip().split('\n')
    keys = [key.strip() for key in keys if key.strip()]
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "正在检查...\n")
    button.config(state=tk.DISABLED)
    start_time = time.time()
    
    def worker():
        results = []
        for key in keys:
            result = check_balance(key)
            results.append(result)
        end_time = time.time()
        total_time = f"{end_time - start_time:.2f}"
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "\n".join(results) + f"\n\n总用时：{total_time} 秒")
        button.config(state=tk.NORMAL)
    
    threading.Thread(target=worker).start()

# 创建UI
root = tk.Tk()
root.title("API余额检查器")
root.geometry("600x500")

container = tk.Frame(root)
container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

textarea = scrolledtext.ScrolledText(container, height=10, width=70, font=("Arial", 12))
textarea.pack(pady=10)
textarea.insert(tk.END, "在此粘贴API密钥，每行一个")

button = tk.Button(container, text="检查余额", command=on_check_balance, font=("Arial", 14), bg="#4CAF50", fg="white")
button.pack(pady=10)

result_text = scrolledtext.ScrolledText(container, height=15, width=70, font=("Arial", 12))
result_text.pack(pady=10)

root.mainloop()
