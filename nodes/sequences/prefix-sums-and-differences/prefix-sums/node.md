---
tag: 37H2XG
kind: technique
slug: prefix-sums
name: Prefix sums
aliases:
- cumulative sums
- running sums
- summed-area table (1D)
area: sequences/prefix-sums-and-differences
level: intro
summary: Precompute P[i] = a[1]+...+a[i] in O(n) so any range sum a[l..r] is P[r]-P[l-1] in O(1).
---

Precompute P[i] = a[1]+...+a[i] in O(n) so any range sum a[l..r] is P[r]-P[l-1] in O(1).
