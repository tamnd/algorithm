---
tag: 7HJ2KD
kind: algorithm
slug: utf-16
name: UTF-16
aliases:
- UTF-16 encoding
- surrogate pairs
area: strings/text-processing-and-typesetting
level: intro
summary: Encode code points below 0x10000 in one 16-bit unit and the rest as a pair of surrogates that carry 10 bits each of the value minus 0x10000.
---

Encode code points below 0x10000 in one 16-bit unit and the rest as a pair of surrogates that carry 10 bits each of the value minus 0x10000.
