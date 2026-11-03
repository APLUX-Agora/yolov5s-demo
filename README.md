# YOLOv5s

Minimal on-device inference example. [Model resources](https://huggingface.co/APLUX-Agora/YOLOv5s) are hosted separately on Hugging Face.

Targets: QCS6490, QCS8550, QCS8625, IQ8, IQ9. The default is FP16, except QCS6490 uses INT8. QCS8550 requires the QNN 2.48 backend; the other supplied packages require QNN 2.36 (`aidlite-qnn236`).

## 1. Check the environment

Set these two variables in the device terminal. Choose any workspace path/name;
Agora fills in the selected SoC. Use a separate workspace per task.

```bash
export AGORA_WORKSPACE="$HOME/my-yolo-demo"
export AGORA_SOC='QCS8550'
```

```bash
mkdir -p "$AGORA_WORKSPACE" &&
curl -fL https://raw.githubusercontent.com/APLUX-Agora/yolov5s-demo/main/tools/check-environment.py \
  -o "$AGORA_WORKSPACE/check-environment.py" &&
python3 "$AGORA_WORKSPACE/check-environment.py" --soc "$AGORA_SOC" --ubuntu 22.04
```

QCS6490/QCS8550/QCS8625 use Ubuntu 22.04 in this demo; IQ8/IQ9 use Ubuntu 24.04.
`CHECKED` means the expected value matches. Stop at `FAILED`: correct hardware/system selections or workspace/disk problems, then rerun the check.
For `NEEDS_SETUP`, install the dependencies below and rerun the check.

## 2. Get the code

```bash
git clone https://github.com/APLUX-Agora/yolov5s-demo.git "$AGORA_WORKSPACE/code"
cd "$AGORA_WORKSPACE/code"
```

Already cloned? Skip this step, or run `git pull --ff-only` to update.

## 3. Set up dependencies

QCS8550 example; installed system packages can be skipped.

```bash
sudo aid-pkg install aidlite-sdk
sudo aid-pkg install aidlite-qnn248
sudo apt-get update
sudo apt-get install -y git python3-venv
cd "$AGORA_WORKSPACE/code"
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Keep this terminal open. In a new terminal, set the same two variables from step 1 and activate
`$AGORA_WORKSPACE/code/.venv` before continuing.

## 4. Get model resources

```bash
hf download APLUX-Agora/YOLOv5s \
  --include "targets/$AGORA_SOC/*" --local-dir "$AGORA_WORKSPACE/resources"
```

Public download, no login required. All files for the selected SoC stay together.

## 5. Run a test

```bash
cd "$AGORA_WORKSPACE/code"
python examples/detect.py --models "$AGORA_WORKSPACE/resources/targets/$AGORA_SOC" \
  --output "$AGORA_WORKSPACE/result.jpg"
```

Expected: A loading message, inference timing, the detected object count, `COMPLETED`, and an annotated `result.jpg`.

On a cloud device, switch to the remote desktop and open `result.jpg` in your workspace. Use `--image` for another image or `--precision INT8` / `--precision W8A16` when the target supplies it.

### SDK diagnostics

Normal output shows loading, results, and errors. Native SDK diagnostics are kept
off the terminal. If troubleshooting requires them, add an optional private log:

```bash
python examples/detect.py --models "$AGORA_WORKSPACE/resources/targets/$AGORA_SOC" --sdk-log "$AGORA_WORKSPACE/sdk.log"
```

The log is saved with owner-only permissions and may contain device-specific
diagnostic information. Keep it private; report the concise terminal error first.

## Validation

QCS8550 / Ubuntu 22.04: FP16, INT8 and W8A16 tested with AidLite 2.5.0.284 and the QNN 2.48 backend. Other hardware combinations require validation.

## License

AGPL-3.0. See LICENSE and NOTICE.md. AidLite and QNN SDKs are installed separately.
