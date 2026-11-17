---
tag: XK6ZQN
kind: algorithm
slug: per-pixel-linked-lists
name: Per-pixel linked list transparency
aliases:
- per-pixel fragment lists
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Append every transparent fragment to a linked list per pixel on the GPU with an atomic counter, then sort and blend each list in a resolve pass.
---

Append every transparent fragment to a linked list per pixel on the GPU with an atomic counter, then sort and blend each list in a resolve pass.
