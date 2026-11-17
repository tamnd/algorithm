---
tag: 5QHTPW
kind: technique
slug: hierarchical-softmax
name: Hierarchical softmax
aliases:
- tree softmax
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Compute a softmax over V words as a product of O(log V) binary decisions along the path to the word in a tree, such as a Huffman tree.
---

Compute a softmax over V words as a product of O(log V) binary decisions along the path to the word in a tree, such as a Huffman tree.
