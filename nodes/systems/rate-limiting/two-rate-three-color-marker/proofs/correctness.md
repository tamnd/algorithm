---
title: The trTCM follows RFC 2698, its non-red packets are a peak token bucket, and its colors obey the interval bounds
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a sequence of packets $j = 1, \ldots, n$ with arrival times $t_1 \le \cdots \le t_n$, sizes $B_j > 0$ and precolors $p_j$; in color-blind mode every $p_j$ is green. The parameters satisfy $0 < CIR \le PIR$, $PBS > 0$ and $CBS > 0$. At the time $t_1$ both buckets are full: $T_p = PBS$ and $T_c = CBS$.

**The token process of the RFC.** RFC 2698 increments $T_p$ by one PIR times per second up to PBS, and $T_c$ by one CIR times per second up to CBS. The two buckets do not exchange tokens. In the *discrete* reading, the tokens of P come at the times $t_1 + k/PIR$ and those of C at the times $t_1 + k/CIR$, and the tokens of a time at or before a packet are added before the packet is metered. In the *fluid* reading, P fills at rate PIR and C at rate CIR, each up to its depth.

**Lemma 1 (the lazy refill).** Suppose that at time $s$ the counts are $T_p \in [0, PBS]$ and $T_c \in [0, CBS]$, and that no packet arrives in $(s, t)$. In the fluid reading the counts at time $t$, before the packet at $t$ is metered, are $\min(PBS, T_p + PIR(t - s))$ and $\min(CBS, T_c + CIR(t - s))$. The same holds in the discrete reading when the numbers of tokens $PIR(t-s)$ and $CIR(t-s)$, the counts and the depths are integers. Lines L1 to L3 compute exactly these values.

*Proof.* Each bucket is on its own. In the fluid reading a bucket rises at its rate until it reaches its depth and then stays there, which is the capped sum. In the discrete reading each of the $a$ tokens adds one while the count is below the depth, and the count is an integer, so the result is $\min(\text{depth}, T + a)$. Lines L1 and L2 compute the two capped sums. $\square$

**Lemma 2 (ranges).** At every moment, $0 \le T_p \le PBS$ and $0 \le T_c \le CBS$.

*Proof.* The counts start at the depths, and a refill keeps them in range. Line L6 runs only when line L4 failed, so $T_p \ge B$ and $T_p - B \ge 0$. Line L7 runs only when lines L4 and L5 both failed, so $T_p \ge B$ and $T_c \ge B$. Nothing else changes the counts. $\square$

**Theorem 1 (agreement with RFC 2698).** For each input, TRTCM-METER gives each packet the color that the rules of RFC 2698, Section 3, give it, and leaves the same token counts.

*Proof.* By induction on $j$; both processes start with full buckets. By Lemma 1, lines L1 to L3 give the counts that the RFC process has at $t_j$. Color-blind mode: $p_j$ is green, so line L4 tests $T_p - B < 0$, line L5 tests $T_c - B < 0$, and the three outcomes are red with no change, yellow with $T_p$ decremented by $B$, and green with both decremented by $B$. These are the three color-blind rules of the RFC, in the same order. Color-aware mode: line L4 tests "precolored red or $T_p - B < 0$", line L5 tests "precolored yellow or $T_c - B < 0$", with the same three outcomes. These are the three color-aware rules. So the colors and the counts agree after packet $j$. $\square$

**Theorem 2 (no upgrade).** In color-aware mode, the color of a packet is never better than its precolor, in the order green, yellow, red.

*Proof.* A precolored red packet returns red at line L4. A precolored yellow packet that passes line L4 returns yellow at line L6. Only a precolored green packet can reach line L8. $\square$

**Theorem 3 (the non-red packets are a token bucket).** Let TB$(r, b)$ be the token bucket policer that starts full, refills by $x \leftarrow \min(b, x + r \cdot \Delta t)$, and passes a packet of size $L$ when $x \ge L$, then takes $L$ tokens. In color-blind mode, packet $j$ is not red if and only if TB$(PIR, PBS)$, run on all packets, passes it. In color-aware mode, packet $j$ is not red if and only if $p_j$ is not red and TB$(PIR, PBS)$, run on the subsequence of the packets that are not precolored red, passes it.

*Proof.* For $x \le b$ and $a_1, a_2 \ge 0$ we have $\min(b, \min(b, x + a_1) + a_2) = \min(b, x + a_1 + a_2)$: if $x + a_1 \le b$ both sides are $\min(b, x + a_1 + a_2)$, and otherwise both are $b$. So the capped refills of $T_p$ between two packets of the subsequence combine into one capped refill. $T_p$ changes only at line L1 and by $-B$ at lines L6 and L7, and lines L6 and L7 run exactly for the packets that are not red. A packet is not red exactly when it is not precolored red and $T_p \ge B$. Let $g_1 < g_2 < \cdots$ be the packets that are not precolored red (all packets in color-blind mode). A precolored red packet changes $T_p$ only by its refill. By induction on $i$, the value of $T_p$ after line L1 at packet $g_i$ equals the tokens of TB after its refill at $g_i$: at $i = 1$ both start at PBS and make the same combined refill, and from $g_i$ to $g_{i+1}$ both take $B$ on the same condition and then make the same combined refill. So the decisions agree. $T_c$ plays no part in this argument. $\square$

**Theorem 4 (interval bounds).** For a closed interval $I$ of length $\tau$, let $G(I)$ and $Y(I)$ be the total sizes of the green and of the yellow packets with arrival times in $I$. In both modes,

$$G(I) \le CBS + CIR \cdot \tau, \qquad G(I) + Y(I) \le PBS + PIR \cdot \tau.$$

*Proof.* Let packets $p, \ldots, q$ be those with times in $I$. Take $Q = T_c$ with depth $M = CBS$, rate $R = CIR$, charged by the green packets (line L7 is the only step that lowers $T_c$), or $Q = T_p$ with $M = PBS$, $R = PIR$, charged by the green and the yellow packets (lines L6 and L7). Write $Q_j^-$ for the value after line L3 at packet $j$ and $Q_j^+$ for the value at the end of packet $j$. Then $Q_j^+ = Q_j^- - B_j$ for a charged packet and $Q_j^+ = Q_j^-$ otherwise, and by Lemma 1, $Q_{j+1}^- \le Q_j^+ + R(t_{j+1} - t_j)$. Adding from $p$ to $q$ gives

$$\sum_{\text{charged } j \in [p, q]} B_j \le Q_p^- - Q_q^+ + R (t_q - t_p) \le M + R\tau,$$

by Lemma 2 and $t_q - t_p \le \tau$. $\square$

Since green packets are also charged to P, the green bytes satisfy both bounds: $G(I) \le \min(CBS + CIR\tau,\ PBS + PIR\tau)$. In particular, if $PBS < CBS$, a burst of green traffic at one instant is at most PBS bytes.

**Tightness.** Assume $PBS \ge CBS$, integer depths, unit packets and color-blind mode. At time 0 send PBS packets: the first CBS are green, the next $PBS - CBS$ are yellow, and both buckets are then empty. Then send one packet at each time $k/PIR$, $k = 1, 2, \ldots$. Each time P has gained exactly one token, so each of these packets passes line L4, and $G + Y = PBS + k = PBS + PIR\tau$ on $[0, \tau]$ with $\tau = k/PIR$. C gains $CIR/PIR \le 1$ tokens per step, and a packet is green as soon as $T_c \ge 1$, so $T_c$ stays below 1 after each packet. The number of green packets after the burst is an integer equal to $CIR \cdot \tau - T_c$, so whenever $CIR \cdot \tau$ is an integer, $T_c = 0$ and $G = CBS + CIR\tau$. So both bounds are reached on the same trace.

**Corollary (long-term rates).** The green traffic has a long-term rate of at most CIR, and the green and yellow traffic together a long-term rate of at most PIR, because $(M + R\tau)/\tau$ tends to $R$.

**Cost.** Each call runs at most eight lines once, with no loop, so it takes $\Theta(1)$ time in the word RAM, and $n$ packets take $\Theta(n)$ time. The state is $T_p$, $T_c$ and the time of the last update. $\blacksquare$
