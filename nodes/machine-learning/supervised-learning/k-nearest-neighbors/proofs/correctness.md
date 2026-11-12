---
title: KNN-PREDICT returns the vote or the mean of the k smallest keys
proves: [correctness]
status: full
---

We use the pseudocode of the page. The key of training point $i$ is $\kappa_i = (\rho(x_i, q), i)$, ordered lexicographically. The keys are distinct, because the indices are distinct. Let $K_i$ be the set of the $\min(k, i)$ smallest keys among $\kappa_1, \ldots, \kappa_i$, with $K_0 = \emptyset$.

**Claim.** For $1 \le k \le n$, the list $N$ of line L7 holds the keys of $K_n$ in increasing order. Line L8 returns $\sum_{(\delta, i) \in N} w(\delta) y_i / \sum_{(\delta, i) \in N} w(\delta)$, and line L11 returns a class $c$ that maximizes $v_c$; among such classes it returns the one that has the member with the smallest key in $N$.

*Proof.* We use this invariant of the loop of line L2.

> **(I)** Before the iteration for $i$, with $1 \le i \le n + 1$, the set of keys in $H$ is $K_{i-1}$.

*Initialization.* Line L1 makes $H$ empty, and $K_0 = \emptyset$.

*Maintenance.* Assume (I) before iteration $i \le n$. Line L3 computes $\delta = \rho(x_i, q)$, so the new key is $\kappa_i = (\delta, i)$.

1. If $|H| < k$, then $|K_{i-1}| = i - 1 < k$, so $K_{i-1}$ holds all of the first $i - 1$ keys. Then $K_i$ holds all of the first $i$ keys, because $i \le k$. Line L4 inserts $\kappa_i$, and $H$ becomes $K_i$.
2. If $|H| = k$, let $(\delta_m, j)$ be the maximum key of $H$. Then $j \le i - 1 < i$. The set $K_i$ is the $k$ smallest keys of $K_{i-1} \cup \{\kappa_i\}$, because a key outside $K_{i-1}$ among the first $i - 1$ is larger than all $k$ keys of $K_{i-1}$ and so cannot be among the $k$ smallest of the first $i$.
   - If $\delta < \delta_m$, then $\kappa_i < (\delta_m, j)$, so $(\delta_m, j)$ is the largest of the $k + 1$ keys of $K_{i-1} \cup \{\kappa_i\}$, and $K_i = K_{i-1} \setminus \{(\delta_m, j)\} \cup \{\kappa_i\}$. Line L6 makes exactly this change.
   - If $\delta \ge \delta_m$, then $\kappa_i > (\delta_m, j)$: either $\delta > \delta_m$, or $\delta = \delta_m$ and $i > j$. So $\kappa_i$ is larger than each key of $K_{i-1}$, and $K_i = K_{i-1}$. Lines L4 to L6 do nothing.

In each case (I) holds before iteration $i + 1$.

*Termination.* The loop stops with $i = n + 1$, so $H$ holds $K_n$, and $|K_n| = k$ because $k \le n$. Line L7 sorts these keys. Lines L8 and L9 compute the stated sums over $N$ by their definitions. Line L10 collects the classes with the largest $v_c$, and line L11 scans $N$ in increasing key order and stops at the first label in $T$, which is the tied class that has the member with the smallest key. $\square$

**Cost.** Line L3 costs $\Theta(d)$ for the Euclidean distance, so the loop spends $\Theta(n d)$ on distances. The heap has at most $k$ items, so each insert or replace costs $O(\log k)$, and there are at most $n$ of them. Line L7 costs $O(k \log k)$ and lines L8 to L11 cost $O(k)$ with a hash table of classes. Since $k \le n$, the total is $O(n d + n \log k)$. Each of the $n$ distances is needed, since a point that is not read may be the nearest one, so the time is $\Omega(n d)$ for a brute force rule.
