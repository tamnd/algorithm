---
tag: 828D84
kind: technique
slug: stack-canary
name: Stack canary
aliases:
- stack cookie
- StackGuard
area: security-and-privacy/memory-safety-defenses
level: intro
summary: Places a secret value before the return address and checks it before the function returns, to detect a linear stack overflow.
---

Places a secret value before the return address and checks it before the function returns, to detect a linear stack overflow.
