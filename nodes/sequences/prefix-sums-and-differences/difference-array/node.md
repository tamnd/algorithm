---
tag: E7GXER
kind: technique
slug: difference-array
name: Difference array
aliases:
- Imos method
- delta array
- difference sequence
area: sequences/prefix-sums-and-differences
level: intro
summary: Store d[i]=a[i]-a[i-1]; a range add becomes two point updates, and one prefix-sum pass recovers the array.
---

Store d[i]=a[i]-a[i-1]; a range add becomes two point updates, and one prefix-sum pass recovers the array.
