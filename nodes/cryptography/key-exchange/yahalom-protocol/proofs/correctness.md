---
title: In an honest run of the Yahalom protocol, A and B accept the same key
proves: [correctness]
status: full
---

We use the notation of the page. The cipher and the encoding satisfy two properties.

- **(E)** For every key $K$ and tuple $m$, decrypting $\{m\}_K$ with $K$ gives $m$.
- **(C)** The encoding of a tuple can be decoded into its parts.

$S$ holds the true $K_{AS}$ and $K_{BS}$, and $A$ and $B$ hold the same keys.

**Theorem.** Suppose $A$, $B$ and $S$ are honest and every message arrives unchanged. Then $A$ does not fail at line L4, $B$ does not fail at line L5, and $A$ and $B$ accept the same key $K$, each with the other as peer.

*Proof.* *Line L1.* $A$ sends $A, N_A$.

*Line L2.* $B$ records $A$ as its peer, makes $N_B$, and sends $B, \{A, N_A, N_B\}_{K_{BS}}$.

*Line L3.* $S$ decrypts with the key of the name $B$ and, by (E) and (C), gets $A$, $N_A$ and $N_B$. It makes $K$ and sends $U = \{B, K, N_A, N_B\}_{K_{AS}}$ and $W = \{A, K\}_{K_{BS}}$.

*Line L4.* $A$ decrypts $U$ with $K_{AS}$ and gets $B$, $K$, $N_A$ and $N_B$. The name is the peer it chose and the nonce is the one it sent at line L1, so $A$ does not fail. It accepts $K$ with peer $B$ and sends $W$ and $\{N_B\}_K$.

*Line L5.* $B$ decrypts $W$ with $K_{BS}$ and gets $A$ and $K$; the name is the peer it recorded at line L2. It decrypts $\{N_B\}_K$ with this $K$, which is the key $A$ used, and by (E) gets $N_B$, its own nonce. So $B$ does not fail and accepts $K$ with peer $A$. Both hold the $K$ that $S$ made at line L3. $\blacksquare$
