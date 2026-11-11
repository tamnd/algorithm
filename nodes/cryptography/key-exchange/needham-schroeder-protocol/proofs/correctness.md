---
title: In an honest run of the shared-key protocol, B accepts the key that S made, with A as peer
proves: [correctness]
status: full
---

We use the notation of the page. The cipher and the encoding satisfy two properties.

- **(E)** For every key $K$ and tuple $m$, decrypting $\{m\}_K$ with $K$ gives $m$.
- **(C)** The encoding of a tuple can be decoded into its parts.

$S$ holds the true keys $K_{AS}$ and $K_{BS}$, and $A$ and $B$ hold the same keys.

**Theorem.** Suppose $A$, $B$ and $S$ are honest and every message arrives unchanged. Then $A$ does not fail at line L3, $B$ does not fail at line L6, and $B$ accepts the key $K$ that $S$ made at line L2, with peer $A$. $A$ holds the same $K$.

*Proof.* *Line L2.* $S$ receives $(A, B, N_A)$ from line L1, makes $K$, and sends $\{N_A, B, K, T\}_{K_{AS}}$ with $T = \{K, A\}_{K_{BS}}$.

*Line L3.* $A$ decrypts with $K_{AS}$. By (E) and (C) it gets $N_A$, $B$, $K$ and $T$. The nonce is the one it sent at line L1 and the name is the peer it asked for, so $A$ does not fail. It stores $K$ and sends $T$.

*Line L4.* $B$ decrypts $T$ with $K_{BS}$ and, by (E) and (C), gets $K$ and $A$. It makes $N_B$ and sends $\{N_B\}_K$.

*Line L5.* $A$ decrypts with the $K$ it stored at line L3. This is the same $K$, so by (E) it gets $N_B$, and sends $\{N_B - 1\}_K$.

*Line L6.* $B$ decrypts with $K$ and gets $N_B - 1$, which equals the value it computes from its own $N_B$. So $B$ does not fail, and accepts $K$ with peer $A$. $A$ holds the same $K$ from line L3. $\blacksquare$

**Remark.** The theorem is about honest runs only. The Denning-Sacco attack on the page is a run in which line L1 to line L3 never happened: $B$'s steps L4 and L6 succeed for any ticket under $K_{BS}$ and any party that knows the key inside it, which is why $B$ gets no freshness guarantee.
