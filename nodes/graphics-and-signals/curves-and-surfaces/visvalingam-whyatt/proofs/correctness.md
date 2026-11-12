---
title: The heap version of Visvalingam-Whyatt removes the points in the order of the direct rule, keeps both ends, and gives nested results
proves: [correctness, termination, nested-thresholds, monotone-values]
status: full
---

We use the pseudocode of the page. The input is $P_0, \dots, P_{n-1}$ in the plane with $n \ge 3$ and a threshold $A \ge 0$. For $n \le 2$ there are no inner points, the loop does not run, and all claims hold trivially. We write $\mathrm{alive}$ for the set of indices that are not removed. For an inner alive index $i$, its *effective value* $e(i)$ is twice the area of the triangle $P_{\mathrm{prev}[i]} P_i P_{\mathrm{next}[i]}$, where $\mathrm{prev}$ and $\mathrm{next}$ are the current links.

**The direct rule.** The reference process is: while the current polyline has an inner point, remove the inner point with the least effective value, the smallest index on ties, and record that value. This gives a sequence $(i_1, v_1), \dots, (i_{n-2}, v_{n-2})$, the *removal order*.

An entry $(v, i)$ of the heap $H$ is *valid* when $i$ is alive and $v = a[i]$. All other entries are *stale*.

**Invariant (I).** Each time line L3 tests $H$:

1. $0$ and $n - 1$ are alive, and $\mathrm{prev}$ and $\mathrm{next}$ link the alive indices in increasing order;
2. for each inner alive $i$, $a[i] = e(i)$, and $(a[i], i)$ is in $H$;
3. the removed indices, in the order of removal, are the first entries of the removal order of the direct rule, with the same values.

*Initialization.* Line L1 links all indices in order and sets $a[i] = e(i)$. Line L2 puts each pair $(a[i], i)$ in $H$. No index is removed. So (I) holds.

*Maintenance.* Line L4 pops the least entry $(v, i)$ of $H$ in the order of pairs. If it is stale, line L5 skips it, nothing else changes, and (I) holds. Suppose it is valid. Every inner alive $j$ has the valid entry $(a[j], j) = (e(j), j)$ in $H$ by part 2, and $(v, i)$ is the least entry, so $(e(i), i) \le (e(j), j)$ for all inner alive $j$. So $i$ is the index that the direct rule removes next, and $v = e(i)$ is its value. If line L6 does not stop the loop, line L7 removes $i$ and links $p = \mathrm{prev}[i]$ to $q = \mathrm{next}[i]$, which keeps part 1 and extends part 3 by $(i, v)$. The effective value of an index depends only on its two links. Only $p$ and $q$ change links, so only $e(p)$ and $e(q)$ can change. Lines L8 and L9 set $a[j] = e(j)$ for those of them that are inner, and push $(a[j], j)$. So part 2 holds again. $\blacksquare$

*Termination.* Line L2 puts $n - 2$ entries in $H$, and each removal pushes at most 2 more. There are at most $n - 2$ removals, so at most $3(n - 2)$ entries are pushed. Each pass pops one entry, so the loop runs at most $3(n - 2)$ times and stops.

**Theorem 1 (full order).** If $A$ is larger than every value, the removed indices and their values are exactly the removal order of the direct rule.

*Proof.* Part 2 of (I) says that while an inner index is alive, $H$ has a valid entry, so the loop does not end with $H$ empty before all $n - 2$ inner indices are removed. Part 3 gives the claim. $\blacksquare$

**Theorem 2 (threshold).** Let $m$ be the least index with $v_m \ge 2A$, or $m = n - 1$ if there is none. Line L10 returns the input without $P_{i_1}, \dots, P_{i_{m-1}}$. In particular $P_0$ and $P_{n-1}$ are kept.

*Proof.* By part 3 of (I), the valid pops come in the removal order. The first $m - 1$ of them have values below $2A$, so line L6 does not stop them, and they are removed. The next valid pop has value $v_m \ge 2A$, and line L6 stops the loop before it removes anything. A stale pop does not change the state. The indices $0$ and $n - 1$ are never put in $H$, so they are never removed. $\blacksquare$

**Corollary (nested results).** If $A \le B$, the output for $B$ is a subset of the output for $A$.

*Proof.* The removal order does not depend on the threshold. The prefix of values below $2A$ is a prefix of the prefix of values below $2B$, because every value below $2A$ is below $2B$, and the prefix stops at the first value that is not. So the output for $B$ removes every point that the output for $A$ removes. $\blacksquare$

**Lemma (monotone values).** With the rule of the 1993 paper, which replaces a recomputed value $w$ below the last removed value $\ell$ by $\ell$, the recorded values never decrease.

*Proof.* At a valid pop of $(v, i)$, every valid entry of $H$ is at least $v$, because $v$ is the least entry. After the removal, $\ell = v$, and the two recomputed values are $\max(w, \ell) \ge \ell$. So every valid entry is still at least $\ell$, and the next valid pop has a value at least $\ell$. $\blacksquare$

With raised values the effective values are no longer the true areas, so the order can differ from the direct rule when two raised neighbors tie. The lemma still gives nested results for a filter by value, because a filter of a non-decreasing sequence is always a prefix.
