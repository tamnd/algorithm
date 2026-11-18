---
title: Shortest separators and stored prefixes keep the prefix B-tree a correct B+ tree
proves: [correctness]
status: full
---

Strings are compared in lexicographic order: $t < u$ if $t$ is a proper prefix of $u$, or if at the first position $j$ where they differ, $t[j] < u[j]$. We use the notation of the page: a node $v$ has fences $low(v)$ and $high(v)$ (either may be open), $p(v)$ is the longest common prefix of the two fences (empty if one is open), and an inner node with children $c_0, \ldots, c_m$ has separators $s_1 < \cdots < s_m$.

**Lemma 1 (shortest separator).** Let $a < b$ and let $s$ be the result of SHORTEST-SEPARATOR$(a, b)$. Then $a < s \le b$, and every string $t$ with $a < t \le b$ has $|t| \ge |s|$.

*Proof.* Let $i$ be the value at which the loop of L2 stops. Then $a[0..i-1] = b[0..i-1]$. Since $a < b$, either $a$ is a proper prefix of $b$, and then $i = |a| < |b|$, or $i < |a|$ and $a[i] < b[i]$, because $i$ is the first difference and $a < b$. In both cases $b$ has a character at position $i$, so $s = b[0..i]$ has length $i + 1$.

$s \le b$ because $s$ is a prefix of $b$. For $a < s$: in the first case $a = s[0..i-1]$ is a proper prefix of $s$; in the second case $s$ and $a$ agree before $i$ and $a[i] < b[i] = s[i]$.

Now let $|t| \le i$ and $t \le b$. If $t$ is a prefix of $b$, then $t = b[0..|t|-1] = a[0..|t|-1]$ is a prefix of $a$, so $t \le a$. Otherwise $t$ is not a prefix of $b$ and $t \le b$, so at the first position $j$ where $t$ and $b$ differ, $j < |t| \le i$ and $t[j] < b[j] = a[j]$, so $t < a$. In both cases $t$ is not in $(a, b]$. $\square$

**Lemma 2 (prefix of an interval).** Let $low < high$, let $p$ be their longest common prefix, and let $low \le k < high$. Then $k$ starts with $p$. If $k$ and $k'$ both lie in $[low, high)$ and $k = p x$, $k' = p x'$, then $k < k'$ if and only if $x < x'$.

*Proof.* Suppose $k$ does not start with $p$. If $k$ is a proper prefix of $p$, then $k$ is a proper prefix of $low$, so $k < low$, which is false. Otherwise $k$ first differs from $p$ at some $j < |p|$. If $k[j] < p[j] = low[j]$, then $k < low$. If $k[j] > p[j] = high[j]$, then $k > high$. Both are false. The second claim holds because removing a common prefix from two strings does not change their order. $\square$

If a fence is open, $p$ is empty and both claims hold trivially.

**Invariant.** (I1) The tree is a B+ tree: every leaf has the same depth, and an inner node with $m$ separators has $m + 1$ children. (I2) The root has open fences, and child $c_i$ of an inner node $v$ has the fences $s_i$ and $s_{i+1}$, where $s_0 = low(v)$ and $s_{m+1} = high(v)$. (I3) Every key in the subtree of $v$, and every separator stored in $v$, lies in $[low(v), high(v))$, and $v$ stores each of them without the prefix $p(v)$, in increasing order.

By Lemma 2, (I3) is well defined: each stored item starts with $p(v)$, and the stored suffixes are in the same order as the full strings.

**Claim 1 (SEARCH).** If the invariant holds, SEARCH$(T, k)$ returns true if and only if $k$ is a key of $T$.

*Proof.* We show that SEARCH visits a node $v$ with $low(v) \le k < high(v)$ at each level. This holds for the root. At an inner node $v$, by Lemma 2 the suffix test at L6 counts exactly the separators $s_i \le k$. So $j$ is the index with $s_j \le k < s_{j+1}$ (with the conventions of I2), which by (I2) means $low(c_j) \le k < high(c_j)$. By (I3) for the siblings, any key equal to $k$ can only be in the subtree of $c_j$, because the fence intervals of the children are disjoint. At the leaf, L8 compares the suffix of $k$ with the stored suffixes, which by Lemma 2 is the same as comparing full keys. $\square$

**Claim 2 (insert keeps the invariant).** Adding a key to the leaf that SEARCH reaches keeps (I3), since that leaf's interval contains the key. Consider SPLIT-LEAF on a leaf $v$ with keys $k_0 < \cdots < k_{n-1}$ in $[low(v), high(v))$, and the split point $j$ with $1 \le j \le n - 1$. By Lemma 1, $s = $ SHORTEST-SEPARATOR$(k_{j-1}, k_j)$ satisfies $k_{j-1} < s \le k_j$. So every key of the left part lies in $[low(v), s)$ and every key of the right part lies in $[s, high(v))$. Also $low(v) \le k_0 \le k_{j-1} < s$ and $s \le k_j < high(v)$, so $s$ lies strictly inside the old interval, and inserting it into the parent just after the pointer to $v$ keeps the separators of the parent sorted. The new fences of the two leaves are exactly $[low(v), s)$ and $[s, high(v))$, as (I2) demands, and L14 stores their keys without the new prefixes, as (I3) demands.

An inner node $v$ with separators $s_1 < \cdots < s_m$ that overflows moves one separator $s_t$ up. The left node keeps $c_0, \ldots, c_{t-1}$ and $s_1, \ldots, s_{t-1}$ with the fences $low(v)$ and $s_t$; the right node keeps $c_t, \ldots, c_m$ and $s_{t+1}, \ldots, s_m$ with the fences $s_t$ and $high(v)$. Every child keeps its old fences, so (I2) and (I3) hold below, and each of the two nodes stores its separators again without its new prefix. A root split makes a new root with open fences and the single separator, which keeps (I1) because both halves have the same height. $\square$

By Claims 1 and 2, after any sequence of inserts, `contains` answers correctly, and the leaves read from left to right give all keys in increasing order, which is what `range` uses. The choice of $j$ inside the split interval does not affect correctness, only the length of $s$: by Lemma 1 the separator at each candidate point is as short as any separator at that point can be.

The tests check Lemma 1 against all strings of length at most 4 over a three-letter alphabet, Lemma 2 against all strings of length at most 4 over two letters, and the invariant, `contains`, the key order and `range` against a Python set after random inserts.
