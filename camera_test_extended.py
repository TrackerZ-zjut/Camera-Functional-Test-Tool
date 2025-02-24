import cv2
import time
import os
from jinja2 import Template

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

def generate_report(test_results, test_date, output_dir="reports"):
    """生成测试报告"""
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

def main():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    test_results = []
    test_date = time.strftime("%Y-%m-%d %H:%M:%S")

    # 测试分辨率
    width, height = test_camera_resolution(cap, 640, 480)
    test_results.append({
        "name": "Resolution Test",
        "result": "Pass" if width == 640 and height == 480 else "Fail",
        "details": f"Set: 640x480, Actual: {width}x{height}"
    })

    # 测试帧率
    fps = test_camera_fps(cap)
    test_results.append({
        "name": "FPS Test",
        "result": "Pass" if fps > 20 else "Fail",
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
        "result": "Pass" if focus_value > 500 else "Fail",
        "details": f"Focus Value: {focus_value:.2f}"
    })

    # 生成报告
    generate_report(test_results, test_date)

    # 释放摄像头
    cap.release()
    print("测试完成，报告已生成。")

if __name__ == "__main__":
    main()