---
title: The srTCM follows RFC 2697, its green packets are a token bucket, and its colors obey the interval bounds
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a sequence of packets $j = 1, \ldots, n$ with arrival times $t_1 \le \cdots \le t_n$, sizes $B_j > 0$ and precolors $p_j$; in color-blind mode every $p_j$ is green. The parameters satisfy $CIR > 0$, $CBS \ge 0$, $EBS \ge 0$ and $CBS + EBS > 0$. At the time $t_1$ both buckets are full: $T_c = CBS$ and $T_e = EBS$.

**The token process of the RFC.** RFC 2697 adds one token CIR times per second: to C if $T_c < CBS$, else to E if $T_e < EBS$, else to no bucket. We read this in two ways. In the *discrete* reading, one token arrives at each time $t_1 + k/CIR$ for $k = 1, 2, \ldots$, and the tokens of a time at or before a packet are added before the packet is metered. In the *fluid* reading, tokens flow at rate CIR: into C while $T_c < CBS$, then into E while $T_e < EBS$. When all packet times are on the grid $t_1 + k/CIR$ and all sizes and bucket depths are integers, the two readings give the same token counts at each packet, by Lemma 1.

**Lemma 1 (the lazy refill).** Suppose that at time $s$ the counts are $T_c \in [0, CBS]$ and $T_e \in [0, EBS]$, that no packet arrives in the open interval $(s, t)$, and let $a = CIR \cdot (t - s)$. In the fluid reading, the counts at time $t$, before the packet at $t$ is metered, are

$$T_c' = \min(CBS,\ T_c + a), \qquad T_e' = \min\big(EBS,\ T_e + \max(0,\ a - (CBS - T_c))\big).$$

The same holds in the discrete reading when $a$, $T_c$ and $CBS$ are integers. Lines L1 to L4 compute exactly $T_c'$ and $T_e'$.

*Proof.* Fluid reading: C fills at rate CIR. If $a \le CBS - T_c$, C does not reach CBS before $t$ and gets all $a$ tokens, so $T_c' = T_c + a$ and E gets nothing. Otherwise C is full after $(CBS - T_c)/CIR$ seconds, and from then on the flow of the remaining $a - (CBS - T_c)$ tokens goes to E until E is full; tokens after that are lost. Both cases give the formulas. Discrete reading: the $a$ tokens of $(s, t]$ come one at a time. Each of the first $\min(a, CBS - T_c)$ tokens finds $T_c < CBS$ and goes to C. After them, either all tokens are used or $T_c = CBS$, and each later token goes to E while $T_e < EBS$. This gives the same formulas. For the code: line L2 sets $f = \min(a, CBS - T_c) \ge 0$, so line L3 gives $T_c + f = \min(CBS, T_c + a)$. Also $a - f = \max(0, a - (CBS - T_c))$, so line L4 gives $T_e'$. $\square$

**Lemma 2 (ranges).** At every moment, $0 \le T_c \le CBS$ and $0 \le T_e \le EBS$. In particular, the decrements of lines L7 and L9 never go below 0, so the phrase "down to the minimum value of 0" of the RFC never changes a result.

*Proof.* The counts start at $CBS$ and $EBS$. By Lemma 1 a refill takes a value in range to a value in range, because it adds a non-negative amount and caps at the depth. Line L7 runs only when $T_c - B \ge 0$ (line L6), so it leaves $T_c \ge 0$; line L9 runs only when $T_e - B \ge 0$ (line L8). Nothing else changes the counts. $\square$

**Theorem 1 (agreement with RFC 2697).** For each input, SRTCM-METER gives each packet the color that the rules of RFC 2697, Section 3, give it, and leaves the same token counts.

*Proof.* By induction on $j$. Before packet $j$, both processes have the same counts (at the start, both buckets are full). By Lemma 1, line L5 gives the counts that the RFC process has at $t_j$. Color-blind mode: $p_j$ is green, so line L6 tests $T_c - B \ge 0$, line L8 tests $T_e - B \ge 0$, and line L10 returns red with no change: these are the three rules of the color-blind mode, in the same order, with the same decrements by Lemma 2. Color-aware mode: line L6 tests "precolored green and $T_c - B \ge 0$", line L8 tests "precolored green or yellow and $T_e - B \ge 0$", and line L10 returns red with no change: these are the three rules of the color-aware mode. So packet $j$ gets the same color and both processes have the same counts after it. $\square$

**Theorem 2 (no upgrade).** In color-aware mode, the color of a packet is never better than its precolor, in the order green, yellow, red.

*Proof.* Line L7 returns green only after line L6 found $p_j$ green. Line L9 returns yellow only after line L8 found $p_j$ green or yellow. A red precolor fails both tests and reaches line L10. $\square$

**Theorem 3 (the green packets are a token bucket).** Let TB$(r, b)$ be the token bucket policer that starts full at $t_1$, refills by $x \leftarrow \min(b, x + r \cdot \Delta t)$ and passes a packet of size $L$ when $x \ge L$, then takes $L$ tokens. In color-blind mode, packet $j$ is green if and only if TB$(CIR, CBS)$, run on all packets, passes packet $j$. In color-aware mode, packet $j$ is green if and only if $p_j$ is green and TB$(CIR, CBS)$, run on the subsequence of the precolored green packets, passes packet $j$.

*Proof.* We use the identity $\min(b, \min(b, x + a_1) + a_2) = \min(b, x + a_1 + a_2)$ for $x \le b$ and $a_1, a_2 \ge 0$. If $x + a_1 \le b$, both sides are $\min(b, x + a_1 + a_2)$. Otherwise the left side is $\min(b, b + a_2) = b$, and the right side is $b$ because $x + a_1 + a_2 > b$. So several capped refills in a row equal one capped refill over the total time.

$T_c$ changes only at line L3, which is the capped refill $T_c \leftarrow \min(CBS, T_c + a)$, and at line L7. Neither step reads $T_e$. Line L7 runs only for a precolored green packet with $T_c \ge B$. A packet that is not precolored green, or that is red, changes $T_c$ only by the refill at its time. Let $g_1 < g_2 < \cdots$ be the precolored green packets (all packets in color-blind mode). We show by induction on $i$ that the value of $T_c$ after line L5 at packet $g_i$ equals the tokens $x$ of TB after its refill at packet $g_i$. For $i = 1$: $T_c$ starts at $CBS$ and its refills before $g_1$ combine into one capped refill over $t_{g_1} - t_1$ by the identity; TB starts with $CBS$ and makes this refill. Both then make the same test: line L6 tests $T_c \ge B$, TB tests $x \ge B$, and both take $B$ on success. For the step, between $g_i$ and $g_{i+1}$ the value $T_c$ undergoes only capped refills, which combine into the one capped refill of TB over $t_{g_{i+1}} - t_{g_i}$. So the two values agree at $g_{i+1}$, and so do the decisions. $\square$

**Theorem 4 (interval bounds).** For a closed interval $I = [u, v]$ of length $\tau = v - u$, let $G(I)$ and $Y(I)$ be the total sizes of the green and of the yellow packets with arrival times in $I$. In both modes,

$$G(I) \le CBS + CIR \cdot \tau, \qquad Y(I) \le EBS + CIR \cdot \tau, \qquad G(I) + Y(I) \le CBS + EBS + CIR \cdot \tau.$$

*Proof.* Let packets $p, \ldots, q$ be the packets with times in $I$; if there are none, the sums are 0. Let $Q$ stand for one of $T_c$, $T_e$ and $T_c + T_e$, with bound $M$ equal to $CBS$, $EBS$ and $CBS + EBS$, and let the charged packets be the green packets, the yellow packets, and both, in the same order. Write $Q_j^-$ for the value of $Q$ after line L5 at packet $j$, and $Q_j^+$ for its value at the end of packet $j$. By lines L7 and L9, $Q_j^+ = Q_j^- - B_j$ if packet $j$ is charged, and $Q_j^+ = Q_j^-$ otherwise. By Lemma 1, the refill at packet $j + 1$ adds $f \le a$ to $T_c$, at most $a - f \le a$ to $T_e$, and at most $a$ to $T_c + T_e$, where $a = CIR (t_{j+1} - t_j)$. So $Q_{j+1}^- \le Q_j^+ + CIR (t_{j+1} - t_j)$. Adding these steps from $p$ to $q$,

$$Q_q^+ \le Q_p^- + CIR \cdot (t_q - t_p) - \sum_{\text{charged } j \in [p, q]} B_j.$$

By Lemma 2, $Q_q^+ \ge 0$ and $Q_p^- \le M$, and $t_q - t_p \le \tau$. So the charged total is at most $M + CIR \cdot \tau$. $\square$

**Tightness.** All three bounds are reached. Take integer depths, unit packets, and color-blind mode. At time 0 send $CBS + EBS$ packets: the first $CBS$ are green and the next $EBS$ are yellow. Then send one packet at each time $k/CIR$, $k = 1, 2, \ldots$. Both buckets are empty after the burst, so each token goes to C (Lemma 1) and each later packet is green. On $[0, k/CIR]$, $G = CBS + k = CBS + CIR \tau$ and $G + Y = CBS + EBS + CIR \tau$. If instead CBS is 0, every token after the burst goes to E, every later packet is yellow, and $Y = EBS + CIR \tau$.

**Corollary (long-term rate).** Over an interval of length $\tau$, the green and yellow packets carry at most $CBS + EBS + CIR \cdot \tau$ bytes, so their average rate is at most $CIR + (CBS + EBS)/\tau$, which tends to $CIR$. The excess bucket allows larger bursts, but no extra long-term rate.

**Cost.** Each call of SRTCM-METER runs at most ten lines once, with no loop, so it takes $\Theta(1)$ time in the word RAM, and $n$ packets take $\Theta(n)$ time. The state is $T_c$, $T_e$ and the time of the last update. $\blacksquare$
