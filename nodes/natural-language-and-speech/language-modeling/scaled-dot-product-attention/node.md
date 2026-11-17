---
tag: YMRYDZ
kind: algorithm
slug: scaled-dot-product-attention
name: Scaled dot-product attention
aliases:
- softmax attention
- QKV attention
area: natural-language-and-speech/language-modeling
level: core
summary: Output softmax(Q K^T / sqrt(d)) V, a mix of value vectors weighted by how well each key matches each query. Costs O(n^2 d) for n tokens.
---

Output softmax(Q K^T / sqrt(d)) V, a mix of value vectors weighted by how well each key matches each query. Costs O(n^2 d) for n tokens.
