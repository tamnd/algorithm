---
title: In an honest run of the Otway-Rees protocol, A and B accept the same key
proves: [correctness]
status: full
---

We use the notation of the page. The cipher and the encoding satisfy two properties.

- **(E)** For every key $K$ and plaintext $w$, decrypting $\{w\}_K$ with $K$ gives $w$.
- **(C)** The receiver of a plaintext of a known form decodes it into the fields that the sender put in. (In the code, both the typed and the untyped forms have this property for honest messages, because the lengths of nonces, run identifiers and names are fixed.)

$S$ holds the true $K_{AS}$ and $K_{BS}$, and $A$ and $B$ hold the same keys.

**Theorem.** Suppose $A$, $B$ and $S$ are honest and every message arrives unchanged. Then $S$ does not fail at line L3, $B$ does not fail at line L4, $A$ does not fail at line L5, and $A$ and $B$ accept the same key $K$, each with the other as peer.

*Proof.* *Line L1.* $A$ sends $M, A, B, U$ with $U = \{N_A, M, A, B\}_{K_{AS}}$.

*Line L2.* $B$ forwards $M, A, B, U$ and adds $V = \{N_B, M, A, B\}_{K_{BS}}$, with the $M$, $A$ and $B$ it received.

*Line L3.* $S$ decrypts $U$ with $K_{AS}$ and $V$ with $K_{BS}$ (the keys of the names $A$ and $B$ in clear). By (E) and (C) it gets $(N_A, M, A, B)$ and $(N_B, M, A, B)$, and both triples equal the clear values $M, A, B$. So $S$ does not fail. It makes $K$ and sends $M$, $\{N_A, K\}_{K_{AS}}$ and $\{N_B, K\}_{K_{BS}}$.

*Line L4.* $B$ decrypts the second part with $K_{BS}$ and gets $N_B$ and $K$. The nonce is its own, so $B$ accepts $K$ with peer $A$ (the name it received at line L2) and forwards $M, \{N_A, K\}_{K_{AS}}$.

*Line L5.* $A$ decrypts with $K_{AS}$ and gets $N_A$ and $K$. The nonce is its own, so $A$ accepts $K$ with peer $B$. Both parties hold the $K$ that $S$ made at line L3. $\blacksquare$

**Remark.** The type flaw attack does not contradict the theorem: there, message 4 is not the server's message, and property (C) fails because $A$ decodes a plaintext of one form as one of another form.
