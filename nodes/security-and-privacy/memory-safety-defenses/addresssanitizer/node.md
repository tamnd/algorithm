---
tag: B574DH
kind: algorithm
slug: addresssanitizer
name: AddressSanitizer
aliases:
- ASan
- redzone checking
area: security-and-privacy/memory-safety-defenses
level: core
summary: Puts poisoned redzones around objects and a quarantine for freed memory, and checks each access against shadow memory to find overflows and use after free.
---

Puts poisoned redzones around objects and a quarantine for freed memory, and checks each access against shadow memory to find overflows and use after free.
