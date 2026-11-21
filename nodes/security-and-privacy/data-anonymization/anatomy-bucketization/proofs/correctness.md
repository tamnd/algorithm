---
title: Anatomize returns an l-diverse partition of every eligible table
proves: [correctness]
status: full
---

Let $T$ have $n \ge 1$ tuples and let $l \ge 1$. The table is eligible if at most $n/l$ tuples share a sensitive value. A partition is l-diverse if in each group $G$ every value $v$ has $c_G(v) \le |G| / l$. During the group creation phase (lines L3 to L7), let $R$ be the number of tuples left in the buckets, $N$ the number of non-empty buckets, $c_1$ the size of the largest bucket and $j$ the number of buckets of size $c_1$.

**Claim 0 (eligibility is necessary).** If an l-diverse partition exists, the table is eligible.

*Proof.* For a value $v$, $c_T(v) = \sum_G c_G(v) \le \sum_G |G| / l = n / l$. $\square$

**Claim 1 (invariant).** Before each test of line L3, either $c_1 \le 1$ or $R - j \ge l (c_1 - 1)$.

*Proof.* At the start, $R = n$ and $l c_1 \le n$. If $j \le l$, then $R - j \ge l c_1 - l$. If $j > l$, then $R \ge j c_1$, so $R - j \ge j (c_1 - 1) \ge l (c_1 - 1)$.

Now take an iteration with $c_1 \ge 2$ (if $c_1 \le 1$, every bucket still has at most one tuple afterwards, so the claim holds). Line L5 takes the $l$ largest buckets and line L7 removes one tuple from each, so $R' = R - l$.

- If $j > l$, all $l$ chosen buckets have size $c_1$. Then $c_1' = c_1$ and $j' = j - l$, and $R' - j' = R - j \ge l (c_1' - 1)$.
- If $j \le l$, all $j$ buckets of size $c_1$ are chosen and drop to $c_1 - 1$, so $c_1' = c_1 - 1$. Let $u$ be the number of buckets of size $c_1 - 1$ that are not chosen; then $j' = j + u$. If $u = 0$, $R' - j' = R - l - j \ge l (c_1 - 1) - l = l (c_1' - 1)$. If $u > 0$, a bucket of size $c_1 - 1$ was passed over, so all $l$ chosen buckets have size at least $c_1 - 1$, and $R \ge j c_1 + (l - j)(c_1 - 1) + u (c_1 - 1) = l (c_1 - 1) + j + u (c_1 - 1)$. Hence $R' - j' = R - l - j - u \ge l (c_1 - 2) + u (c_1 - 2) \ge l (c_1' - 1)$. $\square$

**Claim 2 (Property 1).** When line L3 stops the loop, each bucket holds at most one tuple, and $g = \lfloor n / l \rfloor$ groups exist.

*Proof.* The loop stops with $N < l$. Suppose $c_1 \ge 2$. The $j$ largest buckets hold $j c_1$ tuples and the other $N - j$ hold at most $c_1 - 1$ each, so $R - j \le N (c_1 - 1) < l (c_1 - 1)$, which contradicts Claim 1. So $c_1 \le 1$ and $R = N < l$. Each iteration removed $l$ tuples, so $g l = n - R$ with $0 \le R < l$, which gives $g = \lfloor n/l \rfloor$. $\square$

**Claim 3 (Property 2).** For each residue tuple $t$, the set $S'$ of line L10 is not empty.

*Proof.* Let $v$ be the value of $t$. Since $c_T(v) \le n / l$ and $c_T(v)$ is an integer, $c_T(v) \le g$. Each group made by lines L4 to L7 takes at most one tuple from each bucket, so it holds $v$ at most once, and $t$ itself is in no group yet. The residue tuples have distinct values by Claim 2, so no earlier residue tuple added $v$. Hence at most $c_T(v) - 1 \le g - 1$ groups hold $v$. Since $n \ge l$ for an eligible non-empty table (otherwise $c_T(v) \ge 1 > n / l$), $g \ge 1$ and at least one group lacks $v$. $\square$

**Claim 4 (Property 3 and correctness).** If the table is eligible, the groups form a partition of $T$ into groups of at least $l$ tuples with pairwise distinct values, so the partition is l-diverse.

*Proof.* Every tuple leaves its bucket exactly once, at line L7 or at line L9, and joins exactly one group, so the groups partition $T$. Each group starts with $l$ tuples from $l$ different buckets, so with $l$ distinct values, and grows only at line L11, by a tuple whose value it does not hold (Claim 3). So in each group every value occurs once, and $c_G(v) = 1 \le |G| / l$. Lines L12 to L14 write exactly the rows of Definition 3 of Xiao and Tao for this partition. With Claim 0, an l-diverse partition exists if and only if the table is eligible, and the code raises an error exactly when it is not. $\blacksquare$

**The error.** In a group of size $G$ where all counts are 1, each tuple has error $(1 - 1/G)^2 + (G - 1)/G^2 = (G - 1)/G$, so the group contributes $G - 1$ and the release has $RCE = n - g = n - \lfloor n/l \rfloor$. Since $\lfloor n / l \rfloor \ge (n - l + 1)/l$, this is at most $n (1 - 1/l) + (l - 1)/l$, which is $1 + 1/n$ times the lower bound $n (1 - 1/l)$ of Theorem 2 of the paper.

**Cost.** Line L2 is $O(n)$ with hashing. The heap holds at most $m$ entries, and each of the $g$ iterations does $l$ pops and at most $l$ pushes, so the first phase is $O(n \log m)$. The residue phase handles fewer than $l$ tuples and scans at most $g$ groups for each, with a set of values per group, which is $O(n)$. Lines L12 to L14 are $O(n \log n)$ with the sorting inside groups. The extra space is $O(n)$.
