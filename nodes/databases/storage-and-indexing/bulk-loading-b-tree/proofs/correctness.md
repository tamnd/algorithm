---
title: Bulk loading builds a valid B+ tree of order d that holds exactly the input entries
proves: [correctness]
status: full
---

Notation as on the page. The keys of $E$ are distinct, $d \ge 1$, and the clamps of lines L2 and L5 give $d \le t \le 2d$ and $d + 1 \le u \le 2d + 1$.

**Lemma 1 (packing).** Let $S$ be a list of $s \ge 1$ items and $lo \le t \le hi$ with $2\,lo - 1 \le hi$. PACK$(S, t, lo, hi)$ returns groups that are consecutive, nonempty, and cover $S$ in order. If it returns one group, that group has $s$ items. If it returns two or more groups, every group has between $lo$ and $hi$ items.

*Proof.* Line L10 cuts $S$ into consecutive groups; all but the last have exactly $t$ items, and $lo \le t \le hi$. The last has between 1 and $t$ items. If there is one group, nothing changes. If there are two or more and the last has at least $lo$ items, all groups are within bounds. Otherwise line L12 joins the last two groups into $m$ with $t < |m| < t + lo$ items. If $|m| \le hi$, line L13 keeps it, and $|m| > t \ge lo$. If $|m| > hi$, line L14 splits it into $\lfloor |m|/2 \rfloor$ and $\lceil |m|/2 \rceil$ items. Since $|m| \ge hi + 1 \ge 2\,lo$, both halves have at least $lo$ items, and since $|m| \le t + lo - 1 \le 2\,hi$, both have at most $hi$. The joins and splits keep the order. $\square$

For leaves, $lo = d$ and $hi = 2d$, so $2\,lo - 1 = 2d - 1 \le hi$. For internal nodes, $lo = d + 1$ and $hi = 2d + 1$, so $2\,lo - 1 = 2d + 1 = hi$. The lemma applies to both.

**Lemma 2 (one level).** Suppose a level is a list of nodes $c_1, \ldots, c_p$ with $p \ge 2$, where each $c_i$ is the root of a subtree with all leaves at depth $h$, the key sets $K(c_i)$ are nonempty, and every key of $K(c_i)$ is smaller than every key of $K(c_{i+1})$. Let $\mathrm{low}(c_i) = \min K(c_i)$. Then the nodes made by lines L7 and L8 satisfy the same conditions with depth $h + 1$, and each new node $x$ with children $g_0, \ldots, g_j$ and separators $s_r = \mathrm{low}(g_r)$ for $r = 1, \ldots, j$ has every key of $K(g_r)$ in $[s_r, s_{r+1})$, with $s_0 = -\infty$ and $s_{j+1} = +\infty$.

*Proof.* By Lemma 1 the groups are consecutive and cover the level, so the new nodes partition the old ones in order. Every leaf below a new node is at depth $h + 1$ from it. The key set of a new node is the union of the key sets of its children, nonempty, and the order between consecutive new nodes follows from the order of the old ones. Its low key is $\mathrm{low}(g_0)$, which line L8 stores, since the children are in increasing order. For the separators: every key of $K(g_r)$ is at least $\min K(g_r) = s_r$. If $r < j$, every key of $K(g_r)$ is smaller than every key of $K(g_{r+1})$, in particular smaller than $s_{r+1}$. $\square$

**Theorem.** BULK-LOAD$(E, d, f)$ returns the empty tree if $E$ is empty, and otherwise a B+ tree of order $d$ whose leaves, read through their links, hold exactly the entries of $E$ in increasing key order.

*Proof.* If $E$ is empty, PACK returns no groups and line L4 returns the empty tree.

Otherwise, line L1 sorts $E$. Line L3 makes one leaf per group of PACK$(E, t, d, 2d)$, in order, and links them left to right. By Lemma 1 the leaves hold all entries in order. If there is one leaf, it is the root and holds $1$ to $2d$ entries, since a single group comes from line L10, with at most $t \le 2d$ items, or from line L13, with at most $2d$ items. If there are several, each holds $d$ to $2d$ entries. The leaves satisfy the conditions of Lemma 2 with $h = 0$, since the keys are distinct and sorted.

Each round of lines L6 to L8 replaces a level of $p \ge 2$ nodes by a level of fewer nodes: every group of PACK has at least 2 items when there are two or more groups (as $lo = d + 1 \ge 2$), and a single group has $p \ge 2$ items. So the loop ends, with one node. By Lemma 2 and induction on the rounds, every level satisfies the conditions, all leaves are at the same depth, and every separator bounds its subtrees as a B+ tree requires.

Fill bounds of internal nodes: a round with two or more groups gives nodes with $d + 1$ to $2d + 1$ children by Lemma 1, so $d$ to $2d$ separators. A round with one group makes the root, whose $p$ children number at least 2 and at most $2d + 1$: a single group comes either from line L10, with at most $u \le 2d + 1$ items, or from line L13, with at most $hi = 2d + 1$ items. $\blacksquare$

**Corollary (search).** Search, which at each internal node goes to child $\mathrm{bisect\_right}(\text{separators}, k)$, finds key $k$ if and only if $k$ is in $E$. This holds because, by the theorem, the chosen child is the only one whose key range $[s_r, s_{r+1})$ can contain $k$.

**Lemma 3 (node count).** With $L \ge 2$ leaves, the number $I$ of internal nodes satisfies $I \le (L + d - 2) / d$.

*Proof.* Each internal node but the root has at least $d + 1$ children, and the root has at least 2. Each of the $L + I - 1$ nodes other than the root has exactly one parent, so $L + I - 1 \ge (d + 1)(I - 1) + 2$, that is $L - 2 + d \ge d I$. $\square$
