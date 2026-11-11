---
title: In an honest and timely run of the shared-key protocol, A and B accept the same key
proves: [correctness]
status: full
---

We use the notation of the page. The cipher and the encoding satisfy two properties.

- **(E)** For every key $K$ and tuple $m$, decrypting $\{m\}_K$ with $K$ gives $m$.
- **(C)** The encoding of a tuple can be decoded into its parts.

**Timing assumption.** At every moment, the clocks of $A$ and $B$ differ from the clock of $S$ by at most $\delta_1$, and all clocks run at the true rate. Each check at lines L3 and L4 happens at most $\delta_2$ of real time after $S$ reads its clock at line L2.

**Theorem.** Suppose $A$, $B$ and $S$ are honest, every message arrives unchanged, and the timing assumption holds. Then neither $A$ nor $B$ fails, and both accept the same key $K$, with $B$ accepting $A$ as peer.

*Proof.* *Line L2.* $S$ makes $K$, reads $T$ from its clock, and sends $\{B, K, T, W\}_{K_{AS}}$ with $W = \{A, K, T\}_{K_{BS}}$.

*Line L3.* $A$ decrypts with $K_{AS}$ and, by (E) and (C), gets $B$, $K$, $T$ and $W$. The name is the peer it asked for at line L1. Let $t$ be the real time of the check and $t_0$ the real time at which $S$ read $T$, so $0 \le t - t_0 \le \delta_2$. The clock of $S$ read $T$ at time $t_0$ and runs at the true rate, so the clock of $S$ reads $T + (t - t_0)$ at time $t$, and $A$'s clock reads a value within $\delta_1$ of that. So $|\mathrm{clock}_A - T| \le \delta_1 + (t - t_0) \le \delta_1 + \delta_2$, and $A$ does not fail. It stores $K$ and sends $W$.

*Line L4.* $B$ decrypts $W$ with $K_{BS}$ and, by (E) and (C), gets $A$, $K$ and $T$. By the same argument, $|\mathrm{clock}_B - T| \le \delta_1 + \delta_2$, so $B$ does not fail. It accepts $K$ with peer $A$, which is the $K$ that $A$ stored at line L3. $\blacksquare$

**Remark.** If the clocks may drift during the run, the drift over the run must be added to $\delta_1$.
