---
title: CMP stacking groups each trace into its midpoint bin, returns the mean of the live NMO-corrected samples, and under independent noise lowers the noise standard deviation by the square root of the fold
proves: [correctness]
status: full
---

**Setting.** A 2D line has $m$ traces. Trace $i$ has the source position $s_i$, the receiver position $g_i$ and $n$ samples at times $k\,\Delta t$. The midpoint is $(s_i + g_i)/2$ and the offset is $x_i = |g_i - s_i|$. The bins have width $b$ and start at the origin $o$. NMO with a stretch mute (line L5) returns, for each output sample $j$, a value $c_{ij}$ and a flag $\ell_{ij} \in \{0, 1\}$: $\ell_{ij} = 0$ when the sample is muted or when its input time is after the end of the record. The fold of a bin at sample $j$ is $F_j = \sum_i \ell_{ij}$ over the traces of the bin.

**Claim 1 (sorting).** Line L1 puts every trace in exactly one bin, the bin $\operatorname{round}(((s_i + g_i)/2 - o)/b)$, with its offset $x_i$.

*Proof.* The function midpoint_bin is a function of the trace, so each trace gets one index, and sort_by_midpoint appends the pair $(x_i, \text{samples})$ to the list of that index and to no other list. $\square$

**Claim 2 (the stack is the mean of the live samples).** For each bin, lines L3 to L7 return $S_j = \frac{1}{F_j}\sum_i \ell_{ij} c_{ij}$ when $F_j > 0$ and $S_j = 0$ when $F_j = 0$, and they return $F_j$ as the fold.

*Proof.* Line L3 starts with zero sums and zero counts. Each pass of the loop L4 corrects one trace (L5), and the loop L6 adds $c_{ij}$ to the sum of sample $j$ and $1$ to its count exactly when $\ell_{ij} = 1$. After the last trace, the sum of sample $j$ is $\sum_i \ell_{ij} c_{ij}$ and the count is $F_j$. Line L7 divides when $F_j > 0$. Dividing by the live fold, not by the number of traces, keeps the amplitude of an event that is muted on some traces: if every live sample equals $a$, then $S_j = a$. $\square$

**Claim 3 (signal and noise).** Assume that after NMO every live sample of the bin at time $j$ is $c_{ij} = a_j + e_{ij}$, where $a_j$ is the same on all traces (the event is flat, Claim 2 of the NMO proof) and the $e_{ij}$, $i = 1, \ldots, F_j$, are independent with mean $0$ and variance at most $\sigma^2$. Then $S_j$ has mean $a_j$ and variance at most $\sigma^2 / F_j$. So the ratio of the signal amplitude to the noise standard deviation grows by at least the factor $\sqrt{F_j}$ over one trace with noise variance $\sigma^2$.

*Proof.* By Claim 2, $S_j = a_j + \frac{1}{F_j}\sum_i e_{ij}$. Its mean is $a_j$ because each $e_{ij}$ has mean $0$. The variance of a sum of independent terms is the sum of the variances, so $\operatorname{Var} S_j = \frac{1}{F_j^2}\sum_i \operatorname{Var} e_{ij} \le \sigma^2/F_j$. $\square$

The hypothesis holds for noise that is independent from trace to trace and white with variance $\sigma^2$ on each input trace. NMO reads the output sample $j$ of trace $i$ from two neighboring input samples of the same trace, with weights $1 - f$ and $f$, so the noise of that sample has variance $((1 - f)^2 + f^2)\sigma^2 \le \sigma^2$, and samples of different traces stay independent. The hypothesis fails for coherent noise (ground roll, multiples, noise from one shot recorded on many traces): such noise is not independent between the traces of a bin, and the stack does not reduce it by $\sqrt{F_j}$.

**Claim 4 (the nominal fold).** Let every shot use the same spread of $n_r$ receivers with spacing $\Delta g$ at fixed offsets $o_0 + q\,\Delta g$, $q = 0, \ldots, n_r - 1$, from the shot, and let the shots be $\Delta s$ apart. Let the bin width be $h = \Delta g/2$, and let $r = \Delta s / h = 2\Delta s/\Delta g$ be an integer that divides $n_r$. Then every bin that is not near the ends of the line holds exactly $n_r/r = n_r \Delta g / (2 \Delta s)$ traces.

*Proof.* Shot $k$ is at $k\,\Delta s$, and its trace $q$ has the midpoint $k\,\Delta s + o_0/2 + q\,h$. In units of $h$ from the midpoint $o_0/2$ of trace $0$ of shot $0$, this is the integer $p = k r + q$. A bin $p$ receives the trace $(k, q)$ exactly when $q = p - k r$ and $0 \le q \le n_r - 1$, that is when $k r$ lies in the set of $n_r$ consecutive integers $\{p - n_r + 1, \ldots, p\}$. When $r$ divides $n_r$, any $n_r$ consecutive integers contain exactly $n_r/r$ multiples of $r$. Away from the ends of the line, every such multiple $k r$ belongs to a recorded shot, so the bin holds $n_r/r$ traces. $\square$

**Claim 5 (cost).** With $m$ traces of $n$ samples, the stack of the whole line costs $O(m n)$ operations plus the cost of sorting, which is $O(m)$ expected with a hash table and $O(m \log m)$ with a comparison sort of the bin indices.

*Proof.* Every trace is corrected once (Claim 6 of the NMO proof, $O(n)$) and added once ($O(n)$). The divisions of line L7 cost $O(n)$ per bin, and there are at most $m$ bins. $\square$
