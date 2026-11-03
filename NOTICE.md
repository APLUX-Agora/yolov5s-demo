# Source and license notice

This repository is an Agora copy of the YOLOv5s package from
https://huggingface.co/APLUX-ModelFarm/YOLOv5s at revision
66a7926ac030fe6cdc204e17635690d4a308e5e6.

The upstream model architecture is Ultralytics YOLOv5:
https://github.com/ultralytics/yolov5.

The source package declares AGPL-3.0 for the source and deployable models.
The AGPL-3.0 license text is included in LICENSE. Existing upstream rights
and applicable AidLite/QNN SDK terms continue to apply to those components.
AidLite and Qualcomm QNN SDK binaries are not included in this repository.

Agora separates Python inference code (GitHub) from model binaries (Hugging Face).
Model binaries are copied without modification. Python inference behavior is
preserved; only the default model path is updated to match the published layout.
