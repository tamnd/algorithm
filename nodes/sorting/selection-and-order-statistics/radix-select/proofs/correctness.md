---
title: Radix select returns the k-th smallest key and stops
proves: [correctness, termination]
status: full
---

Let the keys be integers in $[0, 2^w)$, let $d = \lceil w / r \rceil$, and write $\operatorname{dig}_j(x) = \lfloor x / 2^{rj} \rfloor \bmod 2^r$ for $0 \le j < d$. Each key is $x = \sum_{j=0}^{d-1} \operatorname{dig}_j(x) \, 2^{rj}$, because $x < 2^w \le 2^{rd}$. For a list $S$ and $1 \le k \le |S|$, write $\operatorname{sel}(S, k)$ for the $k$-th entry of the sorted order of $S$. The claim is: for $1 \le k \le n$, RADIX-SELECT$(A, k)$ stops and returns $\operatorname{sel}(A, k)$.

**Termination.** The loop of line L2 runs at most $d$ passes, and each pass is a finite number of steps: line L5 reads $|S|$ keys, and line L7 stops, as shown below, before $b$ passes $2^r - 1$.

**Lemma (order by digits).** Let $x$ and $y$ have the same digits $\operatorname{dig}_i$ for all $i > j$. If $\operatorname{dig}_j(x) < \operatorname{dig}_j(y)$ then $x < y$.

*Proof.* The common higher digits contribute the same amount $H$ to both. Then $x \le H + \operatorname{dig}_j(x) 2^{rj} + (2^{rj} - 1)$, since the lower digits add at most $\sum_{i < j} (2^r - 1) 2^{ri} = 2^{rj} - 1$, and $y \ge H + \operatorname{dig}_j(y) 2^{rj} \ge H + (\operatorname{dig}_j(x) + 1) 2^{rj} > x$. $\square$

**Invariant.** At the test of line L3 in the pass for digit $j$:

> **(R)** $1 \le k \le |S|$; all keys of $S$ have the same digits $\operatorname{dig}_i$ for each $i > j$; and $\operatorname{sel}(S, k) = \operatorname{sel}(A, k_0)$, where $k_0$ is the rank given as input.

1. *Initialization.* Before the first pass, $j = d - 1$, $S = A$ and $k = k_0$. There are no digits above $d - 1$, so (R) holds.
2. *Maintenance.* Assume (R) at the pass for $j$, and $|S| > 1$. After line L5, $C[c]$ is the number of keys of $S$ with digit $j$ equal to $c$, and $\sum_c C[c] = |S| \ge k$. Line L7 keeps $k \ge 1$ and stops at the least $b$ with $k \le C[b]$; such a $b$ exists because the sums $C[0] + \cdots + C[c]$ reach $|S|$. Write $k'$ for the value of $k$ after line L7 and $c_0 = C[0] + \cdots + C[b-1]$; then $k' = k - c_0$ and $1 \le k' \le C[b]$. Let $B$ be the list of line L8. By (R) and the lemma, each key of $S$ with digit $j$ less than $b$ is less than each key of $B$, and each key with digit $j$ greater than $b$ is greater. So the sorted order of $S$ is the $c_0$ keys of the lower buckets, then the sorted $B$, then the rest, and $\operatorname{sel}(S, k) = \operatorname{sel}(B, k - c_0) = \operatorname{sel}(B, k')$. All keys of $B$ agree on the digits above $j$ and on digit $j$. So (R) holds for the next pass, with $j - 1$, $S = B$ and $k = k'$.

**Conclusion.** If line L3 returns, then $|S| = 1$, so $k = 1$ by (R), and $S[1] = \operatorname{sel}(S, 1) = \operatorname{sel}(A, k_0)$. Otherwise the loop ends after the pass for $j = 0$; by the maintenance step, the keys of $S$ then agree on all digits $\operatorname{dig}_0, \ldots, \operatorname{dig}_{d-1}$, so they are all equal, and $1 \le k \le |S|$. Hence $S[1] = \operatorname{sel}(S, k) = \operatorname{sel}(A, k_0)$, which line L9 returns. $\blacksquare$
