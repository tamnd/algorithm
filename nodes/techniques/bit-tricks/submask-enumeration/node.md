---
tag: 06FS9F
kind: technique
slug: submask-enumeration
name: Submask enumeration
aliases:
- enumerating submasks
- enumerating submasks of a bitmask
- sub = (sub-1) & mask
- subset enumeration over bitmasks
area: techniques/bit-tricks
level: core
summary: Iterating over all submasks of a mask m with sub = (sub - 1) & m in O(2^k) total time.
---

Iterating over all submasks of a mask m with sub = (sub - 1) & m in O(2^k) total time.
