---
tag: SP0023
kind: technique
slug: visibility-buffer
name: Visibility buffer
aliases:
- deferred texturing
area: graphics-and-signals/real-time-rendering
level: research
summary: Store only a triangle and instance id per pixel and fetch the attributes during shading, which uses less memory and bandwidth than a G-buffer.
---

Store only a triangle and instance id per pixel and fetch the attributes during shading, which uses less memory and bandwidth than a G-buffer.
