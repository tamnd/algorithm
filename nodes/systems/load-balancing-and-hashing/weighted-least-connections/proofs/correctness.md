---
title: Weighted least connections picks the smallest load per unit of weight and, with no departures, never exceeds the upper quota
proves: [correctness, termination]
status: full
---

We use the pseudocode WLC-PICK and WLC-DONE of the page. There are $n \ge 0$ backends with integer weights $w[j] \ge 0$, counters $a[j]$, all 0 at the start, and flags $up[j]$. A backend is *eligible* if $up[j]$ holds and $w[j] > 0$. The caller runs WLC-DONE$(j)$ once for each connection to $j$ that closes, and only for such connections.

**Claim 1 (exact counters).** Between calls, $a[j]$ is the number of open connections to $j$.

*Proof.* The same induction as for [least connections](/least-connections/): line L6 adds 1 to the counter of the backend that WLC-PICK returns, line L8 subtracts 1 from the counter of the backend whose connection closes, and nothing else changes a counter. A close happens only for an open connection, so $a[j] \ge 1$ before line L8 and no counter becomes negative. $\square$

**Claim 2 (cross-multiplication).** For eligible $i$ and $j$, the test $a[j] \cdot w[i] < a[i] \cdot w[j]$ holds if and only if $a[j] / w[j] < a[i] / w[i]$.

*Proof.* Multiply both sides of $a[j]/w[j] < a[i]/w[i]$ by $w[i]\,w[j]$. This number is positive, because both backends are eligible, so the direction of the inequality stays the same. The step is reversible. All values are integers, so the test is exact. $\square$

**Claim 3 (the choice).** WLC-PICK returns none if no backend is eligible. Otherwise it returns the smallest index $j^*$ among the eligible backends with the smallest ratio $a[j]/w[j]$.

*Proof.* Invariant at the test of line L2 for index $j$: $best$ is none if no backend among $0, \ldots, j-1$ is eligible; else $best$ is the smallest index of an eligible backend in that range whose ratio is the smallest in that range. *Initialization:* for $j = 0$ the range is empty and line L1 set $best$ to none. *Maintenance:* if $j$ is not eligible, line L3 skips it and the invariant stays true for the range up to $j$. If $j$ is eligible and $best$ is none, line L4 sets $best = j$, the only eligible backend so far. Otherwise, by Claim 2 the test of line L4 is true exactly when the ratio of $j$ is strictly smaller than the ratio of $best$; then $j$ is the unique index with the new smallest ratio and line L5 stores it. When the ratio of $j$ is equal or larger, $best$ keeps the smallest ratio, and on a tie the smaller index $best < j$ stays. *Termination:* the loop makes exactly $n$ passes, one for each value of $j$, and the invariant for the full range is the claim. $\square$

**Claim 4 (upper quota).** Suppose the weights and the flags stay fixed, at least one backend is eligible, all counters start at 0, and no connection closes. Let $W$ be the sum of the eligible weights. Then after $k$ picks, for each eligible $j$,

$$a[j] \le \left\lceil \frac{k\, w[j]}{W} \right\rceil .$$

*Proof.* By induction on $k$. For $k = 0$ every counter is 0. Suppose the bound holds after $k$ picks and pick $k + 1$ goes to $j$. Only eligible backends receive picks, so the eligible counters add up to $k$. Let $m = a[j]/w[j]$. By Claim 3, $a[i] \ge m\, w[i]$ for each eligible $i$. Summing over the eligible backends gives $k \ge m W$, so $a[j] = m\, w[j] \le k\, w[j]/W < (k+1)\, w[j]/W$. The integer $a[j]$ is strictly less than $(k+1)\,w[j]/W$, so $a[j] \le \lceil (k+1)\, w[j]/W \rceil - 1$, and after the pick $a[j] \le \lceil (k+1)\, w[j]/W \rceil$. Every other counter is unchanged, and its bound did not fall when $k$ grew. $\square$

**Claim 5 (lower bound and exact cycles).** Under the hypotheses of Claim 4, with $e$ eligible backends, $a[j] \ge k\, w[j]/W - (e - 1)$ for each eligible $j$. If $W$ divides $k$, then $a[j] = k\, w[j]/W$ exactly.

*Proof.* For each eligible $i$, Claim 4 and $\lceil x \rceil < x + 1$ give $a[i] < k\, w[i]/W + 1$. The eligible counters add up to $k$, so $a[j] = k - \sum_{i \ne j} a[i] \ge k - \sum_{i \ne j} (k\, w[i]/W + 1) = k\, w[j]/W - (e - 1)$, where both sums run over the eligible $i \ne j$. If $W$ divides $k$, each bound of Claim 4 is the integer $k\, w[i]/W$, and these bounds add up to $k$. A sum of integers that are each at most their bound, and that equals the sum of the bounds, has each term equal to its bound. $\square$

**Tightness of Claim 5.** Take one backend of weight $M$ and $e - 1$ backends of weight 1. All counters start at 0, and a backend with counter 0 has ratio 0, so the first $e$ picks go to the $e$ backends in index order, one each. After $k = e$ picks the heavy backend has 1 connection, and its quota is $eM/(M + e - 1)$, which tends to $e$ as $M$ grows. So its shortfall tends to $e - 1$, and the lower bound cannot be raised by a constant.

**Termination.** WLC-PICK runs one loop of $n$ passes, and each pass does a constant number of steps. WLC-DONE has one step. $\blacksquare$

Claims 4 and 5 are deterministic and hold for any arrival times, because without departures the arrival times do not change the picks. With departures, Claim 3 still holds at each pick, but the share of each backend then depends on how long its connections last, which is the point of the policy.
