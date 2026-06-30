# Day 7：ArUco Marker 检测与图像误差可视化

本文件遵循工作区根目录的 [每日学习文件编写规范](../../../每日学习文件编写规范.md)。

官方参考：

- [OpenCV：Detection of ArUco Markers](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [OpenCV：ArucoDetector Class Reference](https://docs.opencv.org/4.x/d2/d1a/classcv_1_1aruco_1_1ArucoDetector.html)

> 说明：本文件恢复为原先“基础 ArUco 编码任务”版本。后续将结合既有项目经历判断是否执行、压缩或替换，不默认要求重复学习。

## 1. 今日目标

将 Day 6 手工给定的 `marker_center` 替换成图像检测结果：

```text
输入图像
-> 检测 ArUco marker
-> 提取四个角点
-> 计算 marker center
-> 计算 image error
-> 绘制检测结果和误差方向
```

完成后应能：

1. 解释 ArUco dictionary、marker ID 和四角点。
2. 使用 OpenCV 生成指定 ID 的 marker。
3. 使用 `ArucoDetector.detectMarkers()` 完成检测。
4. 将角点统一成 `(4, 2)` 数组。
5. 计算 marker center、image center 和 image error。
6. 正确处理未检测到 marker 的情况。

## 2. 今日交付物

```text
data/aruco_marker_23.png
data/aruco_test_scene.png
scripts/01_detect_aruco_marker.py
figures/aruco_detection.png
```

终端打印：

```text
OpenCV version
Detected marker IDs
marker_corners shape
marker_center [u, v]
desired_feature [u*, v*]
image_error [e_u, e_v]
error_norm
```

## 3. 今天明确不做

- 不读取实时摄像头。
- 不做相机标定和畸变校正。
- 不调用 `solvePnP`。
- 不估计三维位姿。
- 不控制真实平台。
- 不实现 PID、IBVS 或 PBVS。

## 4. 环境准备

当前已检查的移动机器人 `.venv` 中没有 `cv2`。建议视觉伺服项目使用独立环境：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\02_视觉伺服_自动对准Demo"
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy opencv-contrib-python
```

验证：

```powershell
python -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'aruco')); print(hasattr(cv2.aruco, 'ArucoDetector'))"
```

不要在同一环境中同时安装 `opencv-python` 和 `opencv-contrib-python`，两者都提供 `cv2`，可能相互覆盖。

## 5. 参数设定

```python
canvas_width = 640
canvas_height = 480
marker_side_pixels = 200
marker_top_left_u = 110
marker_top_left_v = 180
target_marker_id = 23
border_bits = 1
```

Dictionary：

```python
aruco_dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)
```

生成 marker：

```python
marker_image = cv2.aruco.generateImageMarker(
    aruco_dictionary,
    target_marker_id,
    marker_side_pixels,
    borderBits=border_bits,
)
```

## 6. 创建测试图像

Marker 黑色边框不能紧贴图像边缘，否则可能无法形成完整候选四边形。先创建白色 canvas，再把 marker 放入内部：

```python
test_scene = np.full(
    (canvas_height, canvas_width),
    255,
    dtype=np.uint8,
)

test_scene[
    marker_top_left_v:marker_top_left_v + marker_side_pixels,
    marker_top_left_u:marker_top_left_u + marker_side_pixels,
] = marker_image
```

保存：

```text
data/aruco_marker_23.png
data/aruco_test_scene.png
```

## 7. 当前推荐的检测 API

```python
detector_parameters = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(
    aruco_dictionary,
    detector_parameters,
)

detected_corners, detected_ids, rejected_candidates = (
    aruco_detector.detectMarkers(test_scene)
)
```

今天以 `ArucoDetector` 类为主，不以旧版模块级 `cv2.aruco.detectMarkers()` 作为正式实现。

## 8. 输出形状

常见 Python 输出：

```text
detected_ids: shape=(N, 1)，无结果时为 None
detected_corners: 长度为 N 的列表
单个 marker corners: 常见 shape=(1, 4, 2)
```

进入自己的计算前统一为：

```python
marker_corners = np.asarray(
    detected_corners[marker_index],
    dtype=float,
).reshape(4, 2)

assert marker_corners.shape == (4, 2)
```

角点顺序通常为：

```text
top-left -> top-right -> bottom-right -> bottom-left
```

## 9. 查找指定 ID

不能假定 `detected_corners[0]` 永远是目标 marker。

建议实现：

```python
def find_marker_index(detected_ids, target_marker_id):
    ...
```

处理逻辑：

```text
detected_ids is None -> 没有检测结果
detected_ids.flatten() -> 一维 ID 数组
查找 target_marker_id
找不到 -> 明确报告
找到 -> 返回对应 index
```

必须保持：

```text
detected_ids[i] 与 detected_corners[i] 属于同一个 marker
```

## 10. Marker Center 与 Image Error

```python
marker_center = marker_corners.mean(axis=0)

desired_feature = np.array([
    (canvas_width - 1) / 2.0,
    (canvas_height - 1) / 2.0,
])

current_feature = marker_center
image_error = desired_feature - current_feature
error_norm = np.linalg.norm(image_error)
```

保持浮点数进行计算，只在 OpenCV 绘图前转换成整数坐标。

理论结果约为：

```text
marker_center ≈ [209.5, 279.5] pixels
desired_feature = [319.5, 239.5] pixels
image_error ≈ [110.0, -40.0] pixels
error_norm ≈ 117.05 pixels
```

实际值以检测器返回的角点为准，不要为匹配理论值手工覆盖结果。

## 11. 结果图

保存：

```text
figures/aruco_detection.png
```

必须包含：

- Marker 边框和 ID。
- 四个角点。
- Marker center。
- Desired feature。
- 从 marker center 指向 desired feature 的误差箭头。
- Image error 数值。

注意 OpenCV 图像通道为 BGR；使用 `cv2.imwrite()` 可直接保存，使用 Matplotlib 显示前需要转换为 RGB。

## 12. 建议函数结构

```python
from pathlib import Path

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"


def create_aruco_dictionary():
    ...


def generate_marker_image(...):
    ...


def create_test_scene(...):
    ...


def detect_aruco_markers(...):
    ...


def find_marker_index(...):
    ...


def compute_marker_center(marker_corners):
    ...


def compute_image_error(current_feature, desired_feature):
    ...


def draw_detection_result(...):
    ...


def main():
    ...


if __name__ == "__main__":
    main()
```

统一变量名：

```text
aruco_dictionary
aruco_detector
detected_corners
detected_ids
target_marker_id
marker_corners
marker_center
current_feature
desired_feature
image_error
error_norm
```

## 13. 推荐实现顺序

1. 验证 `cv2.aruco`、`ArucoDetector` 和 `generateImageMarker`。
2. 生成 `aruco_marker_23.png`。
3. 创建有白色边距的测试场景。
4. 检测并打印 IDs、角点数量和 rejected candidates 数量。
5. 选择 ID 23，并把角点规范成 `(4, 2)`。
6. 计算 marker center、desired feature、image error 和 error norm。
7. 绘制并保存标注结果。
8. 使用一张空白白图测试检测失败分支。

## 14. 常见错误

### 14.1 `cv2` 或 `cv2.aruco` 不存在

先检查虚拟环境与 OpenCV wheel，不要修改算法绕过环境问题。

### 14.2 生成成功但检测不到

检查白色 margin、dictionary 是否一致、marker 是否被裁切或错误缩放。

### 14.3 `detected_ids is None`

这是合法的无检测结果，不能直接调用 `.flatten()`。

### 14.4 角点 shape 混乱

先打印 shape，再统一 reshape 为 `(4, 2)`，不要依靠连续 `[0][0]` 猜测维度。

### 14.5 BGR/RGB 混淆

`cv2.imwrite` 使用 BGR，`plt.imshow` 期望 RGB。

### 14.6 将 pixel 当成 mm

今天还没有相机—平台映射，image error 只能使用 pixel 单位。

## 15. 验收标准

文件验收：

- `data/aruco_marker_23.png` 存在。
- `data/aruco_test_scene.png` 存在。
- `scripts/01_detect_aruco_marker.py` 能从项目根目录运行。
- `figures/aruco_detection.png` 存在。

结果验收：

- 检测到 marker ID 23。
- `marker_corners.shape == (4, 2)`。
- Marker center 位于 marker 内部。
- 误差箭头由 marker center 指向 image center。
- 空白图测试不会抛出异常。

理解验收：

- 能解释 dictionary、marker ID 和角点顺序。
- 能解释为什么 marker 周围需要白色 margin。
- 能解释 marker center 如何成为视觉反馈特征。
- 能解释为什么 image error 不能直接当成平台物理位移。

## 16. 必答问题

1. ArUco marker 的边框和内部编码分别有什么作用？
2. 为什么生成与检测必须使用相同 dictionary？
3. `detected_ids[i]` 与 `detected_corners[i]` 如何对应？
4. 为什么要把单个 marker 角点统一为 `(4, 2)`？
5. 为什么中心坐标应保留浮点数？
6. 为什么检测失败时不能把 marker center 设置为 `[0, 0]`？
7. 当前 image error 为什么还不能作为真实平台位移？

## 17. 今日记录（完成后填写）

```text
完成日期：
实际投入时间：
Python version：
OpenCV version：
ArUco dictionary：
Target marker ID：
Detected IDs：
Marker corners shape：
Marker center：
Desired feature：
Image error：
Error norm：
空白图测试是否通过：
遇到的问题：
解决方法：
```

## 18. 下一步

原计划 Day 8：

```text
二维对准仿真
-> P control
-> marker center 更新
-> error convergence curve
```

在检查既有项目经历后，应重新判断是否跳过这一基础仿真，直接进入 IBVS、坐标映射、手眼标定或真实闭环接口。
