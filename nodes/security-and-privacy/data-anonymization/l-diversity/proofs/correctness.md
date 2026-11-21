---
title: The l-diversity test is exact, and the three instances survive the merging of blocks
proves: [correctness]
status: full
---

We use the notation of the page. A block $E$ has the sorted positive counts $r_1 \ge \cdots \ge r_m$ of its sensitive values, with $r_1 + \cdots + r_m = |E|$. For a count vector $x$ over the sensitive values (zeros allowed), write $N(x) = \sum_s x_s$, $M(x) = \max_s x_s$, and $T_j(x)$ for the sum of the $j$ largest entries of $x$. Then recursive $(c, l)$-diversity of a block with vector $x$ reads $M(x) < c\,(N(x) - T_{l-1}(x))$. If $x$ has fewer than $l$ positive entries, then $T_{l-1}(x) = N(x)$, the right side is 0, and the block fails, which agrees with the page.

**Claim 1 (the test).** L-DIVERSE returns true if and only if every block of $T$ satisfies the chosen instance.

*Proof.* Line L1 puts two rows in the same group exactly when they agree on $Q$, so the groups are the blocks. Line L3 computes the sorted counts of the block of line L2. The test returns false only at lines L4 to L6, and only for a block that breaks the instance, provided that each line tests the instance exactly. Line L4 is the definition of distinct $l$-diversity. Line L6 is the definition of the recursive form, because $r_l + \cdots + r_m = |E| - T_{l-1}$. For line L5, use $\sum_i r_i = |E|$:
$$|E| \cdot H(E) = \sum_i r_i \log \frac{|E|}{r_i} = \log \frac{|E|^{|E|}}{r_1^{r_1} \cdots r_m^{r_m}}.$$
Since $|E| > 0$ and the logarithm and the exponential are increasing, $H(E) \ge \log l$ holds if and only if $|E|^{|E|} \ge l^{|E|}\, r_1^{r_1} \cdots r_m^{r_m}$, and line L5 returns false exactly when this fails. If no block fails, the loop ends and line L7 returns true. Each block is visited once, so the loop ends. $\square$

**Claim 2 (monotonicity).** Let blocks $A$ and $B$ have count vectors $a$ and $b$, and let $A \cup B$ be the merged block, with vector $a + b$. If $A$ and $B$ are both $l$-diverse in one of the three senses, then $A \cup B$ is $l$-diverse in the same sense.

*Proof.*

1. *Distinct.* Each value that occurs in $A$ occurs in $A \cup B$, so $A \cup B$ has at least as many distinct values as $A$, which is at least $l$.
2. *Entropy.* Let $\lambda = |A| / (|A| + |B|)$. The distribution of $A \cup B$ is $\lambda p_A + (1 - \lambda) p_B$. The function $H$ is concave on distributions, because $-t \log t$ is concave on $[0, 1]$. So $H(A \cup B) \ge \lambda H(A) + (1 - \lambda) H(B) \ge \lambda \log l + (1 - \lambda) \log l = \log l$.
3. *Recursive.* The condition is $M(x) + c\, T_{l-1}(x) < c\, N(x)$. $N$ is additive. $M$ is subadditive: for each value $s$, $a_s + b_s \le M(a) + M(b)$. $T_{l-1}$ is subadditive: let $X$ be the set of $l - 1$ values with the largest entries of $a + b$; then $T_{l-1}(a + b) = \sum_{s \in X} a_s + \sum_{s \in X} b_s \le T_{l-1}(a) + T_{l-1}(b)$. With $c > 0$,
$$M(a + b) + c\, T_{l-1}(a + b) \le \big(M(a) + c\, T_{l-1}(a)\big) + \big(M(b) + c\, T_{l-1}(b)\big) < c\, N(a) + c\, N(b) = c\, N(a + b). \ \square$$

By induction on the number of merges, a generalization whose blocks are unions of the blocks of an $l$-diverse table is $l$-diverse in the same sense.

**Claim 3 (ruling out one value).** Let $l \ge 2$. If a block is recursive $(c, l)$-diverse, then for each value $s$ in it, the block without the rows of value $s$ is recursive $(c, l - 1)$-diverse.

*Proof.* Let $s$ have rank $j$, so its count is $r_j$, and let $r'$ be the sorted counts after the removal. The old condition is $r_1 < c\,(r_l + \cdots + r_m)$.

- If $j = 1$, then $r'_1 = r_2 \le r_1$, and the entries of $r'$ from rank $l - 1$ on are $r_l, \ldots, r_m$. So $r'_1 \le r_1 < c\,(r_l + \cdots + r_m) = c\,(r'_{l-1} + \cdots + r'_{m-1})$.
- If $2 \le j \le l - 1$, then $r'_1 = r_1$, and the entries from rank $l - 1$ on are again $r_l, \ldots, r_m$. The same chain holds.
- If $j \ge l$, then $r'_1 = r_1$, and the entries from rank $l - 1$ on are $r_{l-1}$ and the values $r_l, \ldots, r_m$ without $r_j$. Their sum is $(r_l + \cdots + r_m) + r_{l-1} - r_j \ge r_l + \cdots + r_m$, because $r_{l-1} \ge r_j$. The chain holds again. $\blacksquare$

**Cost.** Line L1 takes $O(n)$ expected time with a hash table, line L3 takes $O(n \log n)$ over all blocks, and lines L4 and L6 take $O(m)$ per block. Line L5 multiplies integers of $O(|E| \log |E|)$ bits.
