---
title: After a Berkeley round the skew of any two clocks is at most the sum of their estimate errors
proves: [correctness]
status: full
---

We use the pseudocode and the model of the page. Clocks do not drift during the round, so machine $i$ has the clock $H_i(t) = t + c_i$. Each one-way delay is at least $d_{\min}$. For a slave $i$, let $\mathrm{RTT}_i$ be the round trip that the master measures in line L2, and let $e_i = \Delta_i - (c_i - c_0)$ be the error of its estimate. Put $e_0 = 0$ and $\mathrm{RTT}_0 = 2 d_{\min}$.

**Lemma 1 (estimate error).** $|e_i| \le \mathrm{RTT}_i/2 - d_{\min}$ for every machine $i$.

*Proof.* For $i = 0$ both sides are 0. For a slave, let the request leave at real time $s$, let the slave read its clock at real time $r$, and let the reply arrive at real time $t$. Then $T_i = r + c_i$, $\mathrm{RTT}_i = t - s$ (the master clock has rate 1), and line L2 gives $\Delta_i = r + c_i + (t - s)/2 - (t + c_0)$. So $e_i = (t-s)/2 - (t - r)$. As in Lemma 2 of the proof for [Cristian's algorithm](/cristian-algorithm/), $d_{\min} \le t - r \le (t - s) - d_{\min}$. Hence $-( \mathrm{RTT}_i/2 - d_{\min}) \le e_i \le \mathrm{RTT}_i/2 - d_{\min}$. $\square$

**Lemma 2 (new offsets).** Let $a$ be the value of line L5. After machine $i$ applies its adjustment $a - \Delta_i$, its offset is $c_0 + a - e_i$.

*Proof.* The new offset is $c_i + a - \Delta_i = c_i + a - (c_i - c_0 + e_i) = c_0 + a - e_i$. The adjustment is a difference, so the time at which the ADJUST message arrives does not change this value, since clocks do not drift. $\square$

**Theorem 1 (skew).** After the round, for all machines $i$ and $j$, also those outside $G$,
$$|C_i - C_j| = |e_i - e_j| \le \left(\tfrac{\mathrm{RTT}_i}{2} - d_{\min}\right) + \left(\tfrac{\mathrm{RTT}_j}{2} - d_{\min}\right).$$

*Proof.* By Lemma 2, $C_i(t) - C_j(t) = (c_0 + a - e_i) - (c_0 + a - e_j) = e_j - e_i$. The triangle inequality and Lemma 1 give the bound. $\square$

So the skew after a round does not depend on $a$ or on $G$. If every round trip is at most $R$, the skew is at most $R - 2 d_{\min}$. If the estimates are exact, as in the example on the page, all clocks agree exactly.

**Theorem 2 (the fault-tolerant average stays near the good clocks).** Let $B$ be a set of good machines with $|B| > n/2$ and $\max_{i \in B} \Delta_i - \min_{i \in B} \Delta_i \le \gamma$. Let $I = [\min_{i \in B} \Delta_i, \max_{i \in B} \Delta_i]$. Then $a$ lies within distance $\gamma$ of $I$.

*Proof.* The set $B$ is a candidate in line L4, so $|G| \ge |B| > n/2$. Two sets of more than $n/2$ machines share a machine, so some $k \in G \cap B$. Then $\Delta_k \in I$. Every $\Delta_i$ with $i \in G$ is within $\gamma$ of $\Delta_k$, since the spread of $G$ is at most $\gamma$. The average $a$ of these values lies between their minimum and maximum, so $|a - \Delta_k| \le \gamma$, and $a$ is within $\gamma$ of $I$. $\square$

Theorem 2 needs a good majority. If more than half of the machines share a wrong value, $G$ is that group, and the common time follows it, as the page says under Pitfalls.

**Line L4 finds a largest set.** Sort the values. A set with spread at most $\gamma$ is contained in the window of sorted values between its minimum and its maximum, and that window also has spread at most $\gamma$. So some largest set is a window. For each right end, the loop keeps the leftmost left end with spread at most $\gamma$, which is the largest window that ends there. The loop sees every right end, so it finds a largest window. The left end only moves to the right, so the scan takes $O(n)$ steps after an $O(n \log n)$ sort. $\square$
