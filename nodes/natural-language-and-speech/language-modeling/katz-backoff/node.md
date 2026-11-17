---
tag: 99DA92
kind: algorithm
slug: katz-backoff
name: Katz backoff
aliases:
- Katz smoothing
area: natural-language-and-speech/language-modeling
level: core
summary: Use a discounted n-gram estimate when the n-gram was seen, else back off to the (n-1)-gram estimate scaled to take exactly the left-over mass.
---

Use a discounted n-gram estimate when the n-gram was seen, else back off to the (n-1)-gram estimate scaled to take exactly the left-over mass.
