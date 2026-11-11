---
title: In an honest and timely run of the wide-mouthed frog protocol, B accepts A's key
proves: [correctness]
status: full
---

We use the notation of the page. The cipher and the encoding satisfy two properties.

- **(E)** For every key $K$ and tuple $m$, decrypting $\{m\}_K$ with $K$ gives $m$.
- **(C)** The encoding of a tuple can be decoded into its parts.

**Timing assumption.** The clocks of $A$ and $B$ differ from the clock of $S$ by at most $\delta_1$, all clocks run at the true rate, each message takes at most $\delta_2$ to arrive, and $\Delta \ge \delta_1 + \delta_2$.

**Theorem.** Suppose $A$, $B$ and $S$ are honest, every message arrives unchanged, and the timing assumption holds. Then $S$ does not fail at line L2, $B$ does not fail at line L3, and $B$ accepts the key $K$ that $A$ made at line L1, with peer $A$.

*Proof.* *Line L1.* $A$ reads $T_A$ from its clock at real time $t_1$, makes $K$, and sends $A, \{T_A, B, K\}_{K_{AS}}$.

*Line L2.* $S$ receives the message at real time $t_2$ with $0 \le t_2 - t_1 \le \delta_2$. It decrypts with $K_{AS}$, the key of the name in clear, and by (E) and (C) gets $T_A$, $B$ and $K$. At time $t_1$ the clock of $S$ read a value within $\delta_1$ of $T_A$, and it has advanced by $t_2 - t_1$ since. So $|\mathrm{clock}_S - T_A| \le \delta_1 + \delta_2 \le \Delta$, and $S$ does not fail. It reads $T_S$ from its clock at time $t_2$ and sends $\{T_S, A, K\}_{K_{BS}}$.

*Line L3.* $B$ receives the message at time $t_3$ with $0 \le t_3 - t_2 \le \delta_2$, decrypts with $K_{BS}$ and gets $T_S$, $A$ and $K$. At time $t_2$ the clock of $B$ read a value within $\delta_1$ of $T_S$, and it has advanced by $t_3 - t_2$ since, so $|\mathrm{clock}_B - T_S| \le \delta_1 + \delta_2 \le \Delta$. So $B$ does not fail, and it accepts $K$, the key from line L1, with peer $A$. $\blacksquare$
