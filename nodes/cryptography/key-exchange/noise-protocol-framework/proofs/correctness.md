---
title: In an honest run of a Noise handshake, both parties keep the same state and end with the same transport keys
proves: [correctness]
status: full
---

We use the notation of the page and the patterns NN and XX, but the argument is the same for every pattern. We use three facts.

- **(D)** For all private keys $a, b$, $\mathrm{DH}(a, \mathrm{pub}(b)) = \mathrm{DH}(b, \mathrm{pub}(a))$. For X25519 both sides compute the $x$-coordinate of $c_a c_b G$, where $c_a, c_b$ are the clamped scalars, and scalar multiplication on a group commutes.
- **(A)** For every key $k$, nonce $n$, associated data $d$ and plaintext $p$, decrypting $\mathrm{AEAD}_k(n, d, p)$ with $k$, $n$ and $d$ passes the tag check and gives $p$.
- **(F)** HASH and HKDF are functions: equal inputs give equal outputs.

Call the tuple $(h, ck, k, n)$ the symmetric state of a party. Write $\sigma_I$ for the initiator's and $\sigma_R$ for the responder's.

**Lemma.** Suppose both parties use the same pattern and prologue, and every message arrives unchanged. Then after line L2, and after each token and each payload step that both parties have processed, $\sigma_I = \sigma_R$. Also, after each `e` token, the reader's $re$ is the writer's $e.\mathrm{pub}$, and after each `s` token the reader's $rs$ is the writer's $s.\mathrm{pub}$.

*Proof.* By induction over the steps.

*Base.* At line L1 both parties take the same protocol name, so by (F) they get the same $h$, $ck = h$ and no key. At line L2 they hash the same prologue, so by (F) $\sigma_I = \sigma_R$.

*Step.* Suppose $\sigma_I = \sigma_R$ before a step, where one party, the writer $W$, writes and the other, the reader $Q$, reads.

- `e` (line L4). $W$ writes $e.\mathrm{pub}$ and hashes it. $Q$ reads the next 32 bytes, which are the same bytes because the message arrives unchanged, sets $re$ to them and hashes them. By (F) the new $h$ values are equal, and $re = e.\mathrm{pub}$.
- `s` (line L5). $W$ writes $c = \mathrm{EncryptAndHash}(s.\mathrm{pub})$. If there is no key, $c = s.\mathrm{pub}$ and has 32 bytes. If there is a key, $c = \mathrm{AEAD}_k(n, h, s.\mathrm{pub})$ and has 48 bytes. Because $\sigma_Q = \sigma_W$, $Q$ knows which case holds and reads the right number of bytes, which are $c$. With no key it takes $c$ as is. With a key it decrypts with the same $k$, $n$ and $h$, so by (A) the tag check passes and $rs = s.\mathrm{pub}$. Both sides then increase $n$ by one (if there is a key) and do $\mathrm{MixHash}(c)$ on the same $c$, so the states stay equal.
- A DH token $xy$ with $x, y \in \{e, s\}$ (line L6). The first letter names a key of the initiator and the second a key of the responder. The initiator computes $\mathrm{DH}(x_I, y_R.\mathrm{pub})$, using its own $x$ and the received $re$ or $rs$; the responder computes $\mathrm{DH}(y_R, x_I.\mathrm{pub})$. By the second part of the induction hypothesis the received keys are the true public keys, so by (D) the two values are equal. Both do $\mathrm{MixKey}$ on the same value from the same $ck$, so by (F) they get the same $ck$ and $k$, and both set $n = 0$.
- The payload (line L7). As for `s`, with the rest of the message in place of the next 32 or 48 bytes: $Q$ gets the payload $W$ wrote, by (A) if there is a key, and the states stay equal.

This completes the induction. $\square$

**Theorem.** Under the same conditions, no tag check fails during the handshake, each party reads every payload the other wrote, both get the same handshake hash, and the cipher state with which each party sends is equal to the cipher state with which the other party receives. So every transport message is decrypted correctly.

*Proof.* By the lemma and (A), every tag check at lines L5 and L7 passes and each payload is read as written. After the last message both parties have the same $ck$ and $h$, so by (F) line L8 gives both the same $(c_1, c_2)$ and the same handshake hash $h$. The initiator sends with $c_1$ and receives with $c_2$; the responder sends with $c_2$ and receives with $c_1$. So for each direction the sender and the receiver hold a cipher state with the same key, both starting with $n = 0$. If transport messages in each direction are delivered in order and unchanged, the sender's and the receiver's nonces stay equal, since each message increases both by one, and by (A) every transport message is decrypted to the plaintext that was sent. $\blacksquare$
