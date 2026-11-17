---
tag: C3YE2Y
kind: technique
slug: temperature-sampling
name: Temperature sampling
aliases:
- softmax temperature
area: natural-language-and-speech/text-generation-and-decoding
level: intro
summary: Sample the next token from softmax(z / T). T below 1 sharpens the distribution toward greedy, T above 1 flattens it toward uniform.
---

Sample the next token from softmax(z / T). T below 1 sharpens the distribution toward greedy, T above 1 flattens it toward uniform.
