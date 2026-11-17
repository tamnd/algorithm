---
tag: C12QAQ
kind: technique
slug: causal-language-modeling
name: Causal language modeling
aliases:
- next-token prediction
- autoregressive language modeling
area: natural-language-and-speech/language-modeling
level: core
summary: Train a network to predict each token from the tokens before it, with a triangular attention mask so no position sees the future.
---

Train a network to predict each token from the tokens before it, with a triangular attention mask so no position sees the future.
