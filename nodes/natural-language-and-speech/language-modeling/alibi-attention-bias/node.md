---
tag: FKDFWV
kind: technique
slug: alibi-attention-bias
name: Attention with linear biases
aliases:
- ALiBi
area: natural-language-and-speech/language-modeling
level: research
summary: Add to each attention score a penalty linear in the distance between query and key, with a fixed slope per head, instead of position vectors.
---

Add to each attention score a penalty linear in the distance between query and key, with a fixed slope per head, instead of position vectors.
