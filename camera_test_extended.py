import cv2
import time
import os
import csv
from jinja2 import Template
import tkinter as tk
from tkinter import ttk, messagebox

# 测试报告模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Camera Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Camera Test Report</h1>
    <p><strong>Test Date:</strong> {{ test_date }}</p>
    <table>
        <tr>
            <th>Test Item</th>
            <th>Result</th>
            <th>Details</th>
        </tr>
        {% for item in test_results %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.result }}</td>
            <td>{{ item.details }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def test_camera_resolution(cap, width, height):
    """测试摄像头分辨率"""
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return actual_width, actual_height

def test_camera_fps(cap, duration=5):
    """测试摄像头帧率"""
    start_time = time.time()
    frame_count = 0

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

    return frame_count / duration

def test_image_quality(cap, save_path="test_image.jpg"):
    """测试图像质量并保存图像"""
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(save_path, frame)
        return True
    return False

def test_camera_focus(cap):
    """测试摄像头对焦"""
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    return 0

def test_camera_exposure(cap, exposure_value):
    """测试摄像头曝光"""
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
    ret, frame = cap.read()
    if ret:
        return True
    return False

def generate_report(test_results, test_date, output_dir="reports"):
    """生成测试报告（HTML、文本、CSV）"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 生成HTML报告
    template = Template(HTML_TEMPLATE)
    html_report = template.render(test_date=test_date, test_results=test_results)
    with open(os.path.join(output_dir, "camera_test_report.html"), "w") as f:
        f.write(html_report)

    # 生成文本报告
    with open(os.path.join(output_dir, "camera_test_report.txt"), "w") as f:
        f.write(f"Camera Test Report\nDate: {test_date}\n\n")
        for item in test_results:
            f.write(f"{item['name']}: {item['result']}\nDetails: {item['details']}\n\n")

    # 生成CSV报告
    with open(os.path.join(output_dir, "camera_test_report.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Test Item", "Result", "Details"])
        for item in test_results:
            writer.writerow([item["name"], item["result"], item["details"]])

def run_tests():
    """执行测试"""
    # 获取用户输入的标准
    resolution_width = int(resolution_width_entry.get())
    resolution_height = int(resolution_height_entry.get())
    min_fps = float(min_fps_entry.get())
    min_focus = float(min_focus_entry.get())
    exposure_value = float(exposure_entry.get())

    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "无法打开摄像头")
        return

    test_results = []
    test_date = time.strftime("%Y-%m-%d %H:%M:%S")

    # 测试分辨率
    width, height = test_camera_resolution(cap, resolution_width, resolution_height)
    test_results.append({
        "name": "Resolution Test",
        "result": "Pass" if width == resolution_width and height == resolution_height else "Fail",
        "details": f"Set: {resolution_width}x{resolution_height}, Actual: {width}x{height}"
    })

    # 测试帧率
    fps = test_camera_fps(cap)
    test_results.append({
        "name": "FPS Test",
        "result": "Pass" if fps >= min_fps else "Fail",
        "details": f"FPS: {fps:.2f}"
    })

    # 测试图像质量
    if test_image_quality(cap):
        test_results.append({
            "name": "Image Quality Test",
            "result": "Pass",
            "details": "Image saved as test_image.jpg"
        })
    else:
        test_results.append({
            "name": "Image Quality Test",
            "result": "Fail",
            "details": "Failed to capture image"
        })

    # 测试对焦
    focus_value = test_camera_focus(cap)
    test_results.append({
        "name": "Focus Test",
        "result": "Pass" if focus_value >= min_focus else "Fail",
        "details": f"Focus Value: {focus_value:.2f}"
    })

    # 测试曝光
    if test_camera_exposure(cap, exposure_value):
        test_results.append({
            "name": "Exposure Test",
            "result": "Pass",
            "details": f"Exposure Value: {exposure_value}"
        })
    else:
        test_results.append({
            "name": "Exposure Test",
            "result": "Fail",
            "details": "Failed to set exposure"
        })

    # 生成报告
    generate_report(test_results, test_date)

    # 释放摄像头
    cap.release()
    messagebox.showinfo("Success", "测试完成，报告已生成。")

# 创建GUI界面
root = tk.Tk()
root.title("Camera Test Tool")
root.geometry("400x300")

# 分辨率测试标准
ttk.Label(root, text="分辨率宽度:").grid(row=0, column=0, padx=10, pady=5)
resolution_width_entry = ttk.Entry(root)
resolution_width_entry.grid(row=0, column=1, padx=10, pady=5)
resolution_width_entry.insert(0, "640")

ttk.Label(root, text="分辨率高度:").grid(row=1, column=0, padx=10, pady=5)
resolution_height_entry = ttk.Entry(root)
resolution_height_entry.grid(row=1, column=1, padx=10, pady=5)
resolution_height_entry.insert(0, "480")

# 帧率测试标准
ttk.Label(root, text="最小帧率 (FPS):").grid(row=2, column=0, padx=10, pady=5)
min_fps_entry = ttk.Entry(root)
min_fps_entry.grid(row=2, column=1, padx=10, pady=5)
min_fps_entry.insert(0, "20")

# 对焦测试标准
ttk.Label(root, text="最小对焦值:").grid(row=3, column=0, padx=10, pady=5)
min_focus_entry = ttk.Entry(root)
min_focus_entry.grid(row=3, column=1, padx=10, pady=5)
min_focus_entry.insert(0, "500")

# 曝光测试标准
ttk.Label(root, text="曝光值:").grid(row=4, column=0, padx=10, pady=5)
exposure_entry = ttk.Entry(root)
exposure_entry.grid(row=4, column=1, padx=10, pady=5)
exposure_entry.insert(0, "0")

# 执行测试按钮
run_button = ttk.Button(root, text="Run Tests", command=run_tests)
run_button.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()