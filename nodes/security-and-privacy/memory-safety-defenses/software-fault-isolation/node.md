---
tag: BDGPFB
kind: technique
slug: software-fault-isolation
name: Software fault isolation
aliases:
- SFI
- address sandboxing
area: security-and-privacy/memory-safety-defenses
level: core
summary: Rewrites untrusted machine code so that every store and jump is masked or checked to stay inside its own region of memory.
---

Rewrites untrusted machine code so that every store and jump is masked or checked to stay inside its own region of memory.
