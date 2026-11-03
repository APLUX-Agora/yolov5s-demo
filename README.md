# YOLOv5s on Qualcomm devices

Python object-detection example using the AidLite SDK and precompiled QNN models.
This is an Agora copy of the ModelFarm YOLOv5s package; the inference implementation
is preserved. Model binaries are hosted separately on Hugging Face.

- Code: https://github.com/APLUX-Agora/yolov5s-demo
- Models: https://huggingface.co/APLUX-Agora/YOLOv5s
- ModelFarm information and performance: https://aiot.aidlux.com/en/models/detail/16
- Input: 640 x 640 RGB; output: [1, 25200, 85]; COCO 80 classes.

## Available model files

| SoC | QNN backend | Precisions |
| --- | --- | --- |
| QCS6490 | 2.36 | W8A8 (INT8), W8A16 |
| QCS8550 | 2.48 | FP16, W8A8 (INT8), W8A16 |
| QCS8625 | 2.36 | FP16, W8A16 |
| IQ8 | 2.36 | FP16, W8A16 |
| IQ9 | 2.36 | FP16, W8A16 |

IQ8, IQ9 and QCS8625 resources are copied from APLUX-ModelFarm-IQ9/YOLOv5s.
The original filenames are retained (IQ8 uses `qcs8275`, IQ9 uses `qcs9100`).
`models/IQ9/W8A8_bak/` is retained as an upstream backup, not a qualified INT8
release. Use the backend matching the selected model file; QCS8550 uses QNN 2.48
and the other supplied packages use QNN 2.36. No new Agora board qualification
has been performed; ModelFarm performance records may use other backend versions.

## Get the code

```bash
git clone https://github.com/APLUX-Agora/yolov5s-demo.git
cd yolov5s-demo
```

## Prepare the environment

On an AidLux-supported Ubuntu device, install the SDK and the selected QNN backend.
For the QCS8550 example below:

```bash
sudo aid-pkg update
sudo aid-pkg install aidlite-sdk
sudo aid-pkg install aidlite-qnn248
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import aidlite; print(aidlite.get_py_library_version())"
```

QCS6490 models require `aidlite-qnn236` instead. SDK availability depends on your
board's package sources. AidLite setup: https://rhinopi.docs.aidlux.com/software/ai-sdk/aidlite_guide

## Get model resources

Download only the selected SoC directory with the official Hugging Face CLI.
The repository is public and does not require a Hugging Face login.

```bash
hf download APLUX-Agora/YOLOv5s --include "models/QCS8550/*" --local-dir ./resources
```

For another device, replace `QCS8550` with `QCS6490`, `QCS8625`, `IQ8` or `IQ9`. Keep the `models/<SoC>/<precision>/`
layout inside `resources`; the source binary filenames are unchanged.

## Run a test

From the repository root with the virtual environment active:

```bash
python code/python/run_test.py \
  --target_model ./resources/models/QCS8550/FP16/yolov5s_qcs8550_fp16.qnn248.ctx.bin \
  --imgs ./code/python/bus.jpg \
  --invoke_nums 10 \
  --save_path ./result.jpg
```

Expected output: inference timing, the detected object count and an annotated
`result.jpg`. Timing and detection counts depend on the device and selected model.
For another precision or SoC, pass the corresponding model file explicitly.

## License and provenance

AGPL-3.0. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). AidLite and QNN SDKs
are separate dependencies with their own terms. The copied upstream package
version is `2026.09.28-v1.0.0`.
