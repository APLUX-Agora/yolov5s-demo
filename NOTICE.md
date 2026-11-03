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

Additional IQ8, IQ9 and QCS8625 model resources are copied from
https://huggingface.co/APLUX-ModelFarm-IQ9/YOLOv5s at revision
193087ec488613f7d1e3d9357e994b999a194a5e. The Python inference implementation
is identical to the first source package. The upstream W8A8_bak directory is
retained as a backup, without a new qualification claim.
