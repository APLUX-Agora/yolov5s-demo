from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from utils import draw_detect_res
from yolov5s import Yolov5s


def parse_args():
    parser = argparse.ArgumentParser(description="Run YOLOv5s QNN model with AidLite.")
    parser.add_argument(
        "--target_model",
        type=str,
        default="./resources/models/QCS8550/FP16/yolov5s_qcs8550_fp16.qnn248.ctx.bin",
    )
    parser.add_argument("--imgs", type=str, default="./code/python/bus.jpg")
    parser.add_argument("--height", type=int, default=640)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--cls_num", type=int, default=80)
    parser.add_argument("--invoke_nums", type=int, default=10)
    parser.add_argument("--model_type", type=str, default="QNN")
    parser.add_argument("--conf_thres", type=float, default=0.25)
    parser.add_argument("--iou_thres", type=float, default=0.45)
    parser.add_argument("--save_path", type=str, default="./code/python/result.jpg")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frame = cv2.imread(args.imgs)
    if frame is None:
        raise FileNotFoundError(args.imgs)

    model = Yolov5s(args.target_model, args.width, args.height, args.cls_num, args.model_type)
    detections = model(frame, args.invoke_nums, args.conf_thres, args.iou_thres)
    print("===================")
    print(f"Detect {len(detections)} targets.")
    result = draw_detect_res(frame, detections)
    Path(args.save_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.save_path, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
