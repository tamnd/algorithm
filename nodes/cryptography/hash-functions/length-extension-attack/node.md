---
tag: 8W23N6
kind: concept
slug: length-extension-attack
name: Length extension attack
aliases:
- length extension
area: cryptography/hash-functions
level: core
summary: On Merkle-Damgard hashes, anyone holding H(secret||m) can compute H(secret||m||pad||m') without the secret.
---

On Merkle-Damgard hashes, anyone holding H(secret||m) can compute H(secret||m||pad||m') without the secret.
