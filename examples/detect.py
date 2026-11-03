# SPDX-License-Identifier: AGPL-3.0-only
"""Run one image through a YOLOv5s target package."""
import argparse
import json
from pathlib import Path
import cv2
from yolov5s import Yolov5s
from utils import draw_detect_res


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models', type=Path, required=True, help='Downloaded targets/<SoC> directory')
    parser.add_argument('--precision', help='FP16, INT8 or W8A16; defaults to the target package default')
    parser.add_argument('--image', type=Path, default=Path(__file__).with_name('bus.jpg'))
    parser.add_argument('--output', type=Path, default=Path('result.jpg'))
    args = parser.parse_args()
    manifest = json.loads((args.models / 'model.json').read_text())
    precision = args.precision or manifest['default_precision']
    if precision not in manifest['variants']:
        parser.error(f'Unsupported precision {precision}; available: {", ".join(manifest["variants"])}')
    model_path = args.models / manifest['variants'][precision]
    if not model_path.is_file():
        parser.error(f'Missing model: {model_path}; download the complete SoC directory')
    image = cv2.imread(str(args.image))
    if image is None:
        parser.error(f'Cannot read image: {args.image}')
    model = Yolov5s(str(model_path))
    try:
        detections = model(image)
        result = draw_detect_res(image, detections)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(args.output), result):
            raise RuntimeError(f'Could not save {args.output}')
        print(f'Detected {len(detections)} objects. Saved {args.output}')
        print('COMPLETED')
    finally:
        if model.interpreter is not None:
            model.interpreter.destory()
            model.interpreter = None


if __name__ == '__main__':
    main()
