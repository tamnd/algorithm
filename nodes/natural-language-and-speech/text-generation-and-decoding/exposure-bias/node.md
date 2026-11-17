---
tag: 3Z4XTB
kind: concept
slug: exposure-bias
name: Exposure bias
aliases:
- train-test discrepancy in sequence generation
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: A model trained with teacher forcing sees only gold prefixes, but at test time conditions on its own outputs, so errors can compound.
---

A model trained with teacher forcing sees only gold prefixes, but at test time conditions on its own outputs, so errors can compound.
