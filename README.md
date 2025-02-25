# Camera-Functional-Test-Tool

# 摄像头功能测试工具

## 概述
本工具用于自动化测试相机的分辨率、帧率、图像质量、对焦和曝光等功能，并生成详细的测试报告（HTML、文本和CSV格式）。

## 功能
- 自动化测试多项相机功能。  
      - 分辨率测试：支持多种分辨率设置，验证摄像头是否支持。  
      - 帧率测试：计算摄像头的平均帧率（FPS），评估性能。  
      - 图像质量测试：捕获并保存图像，检查清晰度和完整性。  
      - 对焦测试：使用拉普拉斯算子计算图像对焦值，评估对焦性能。  
      - 曝光测试：调整曝光值，检查图像亮度变化。   
- 基于GUI的配置界面，操作简单。  
- 生成详细的测试报告和分析。  

## 安装
1. 克隆仓库：
   ```bash
   git clone https://github.com/TrackerZ-zjut/Camera-Functional-Test-Tool.git
2. 安装依赖  
   pip install -r requirements.txt  
## 项目结构
1. 主程序  
  camera_test_tool.py     
2. 测试报告目录 reports              
     camera_test_report.html  
     camera_test_report.txt  
     camera_test_report.csv  
3. 测试图像  
  test_image.jpg
4. .gitignore
