---
tag: 5JRR0P
kind: algorithm
slug: box-non-maximum-suppression
name: Non-maximum suppression for detections
aliases:
- greedy NMS
- box NMS
area: computer-vision/segmentation-and-recognition
level: core
summary: Sort detections by score, keep the best, drop every remaining box whose IoU with it exceeds a threshold, and repeat on what is left.
---

Sort detections by score, keep the best, drop every remaining box whose IoU with it exceeds a threshold, and repeat on what is left.
