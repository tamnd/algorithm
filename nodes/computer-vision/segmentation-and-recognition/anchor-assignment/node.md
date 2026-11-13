---
tag: RFHSZS
kind: technique
slug: anchor-assignment
name: IoU-based anchor assignment
aliases:
- anchor matching
- label assignment for detection
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Label each anchor positive when its IoU with some true box exceeds a high threshold or is the best for that box, negative below a low threshold, else ignored.
---

Label each anchor positive when its IoU with some true box exceeds a high threshold or is the best for that box, negative below a low threshold, else ignored.
