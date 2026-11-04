---
title: Balance Sort sorts stably, and keeps every bucket balanced across the disks
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. All items carry their input position, and ties on the key are broken by the position, so all items are distinct and their order is a total order. A sort of the items in this order is a stable sort of the keys.

## Correctness

**Lemma 1 (buckets).** Let $s_1 < \cdots < s_k$ be the splitters, $s_0 = -\infty$ and $s_{k+1} = +\infty$. Lines L6 and L9 put each item $x$ of $F$ in exactly one bucket $j$, the one with $s_j \le x < s_{j+1}$. Every item of bucket $j$ is smaller than every item of bucket $j'$ for $j < j'$.

*Proof.* The intervals $[s_j, s_{j+1})$ for $j = 0, \ldots, k$ are disjoint and cover all values. A write step of line L7 either places a ready block or keeps it ready, and line L9 repeats write steps until no block is ready, so every item is written to its bucket once. If $x$ is in bucket $j$ and $y$ in bucket $j' > j$, then $x < s_{j+1} \le s_{j'} \le y$. $\blacksquare$

**Lemma 2 (progress).** If $N > M$, then $k \ge 1$ and every bucket has fewer than $N$ items.

*Proof.* The first memoryload has $\lfloor M/B \rfloor B \ge M - B + 1$ items, which is at least $5M/6$ because $M \ge 6B$. The step of the sample is $q = \max(2, \lceil M/(4S) \rceil)$, and $2q \le \max(4, 2\lceil M/8 \rceil) \le 5M/6$ for $M \ge 6$. So this load has at least $2q$ items and gives at least 2 sample items. The rank $r \ge 2$ is at most the sample size, so $k \ge 1$. The splitter $s_1$ has rank $r \ge 2$ in the sample, so the sample item $y$ of rank 1 is smaller than $s_1$ and lies in bucket 0. So every bucket $j \ge 1$ misses $y$. Bucket 0 misses $s_1$, which is an item of $F$. $\blacksquare$

**Theorem 1.** BALANCE-SORT returns the items of $F$ in sorted order.

*Proof.* By strong induction on $N$. For $N \le M$, line L1 sorts in memory. Else, by Lemma 2, each bucket is smaller, so by induction line L9 sorts it. By Lemma 1, the buckets in order, each sorted, form the sorted file. $\blacksquare$

## Balance

Fix a bucket $b$, and write $X$ for $X_b$ and $X(d)$ for $X_b(d)$. The invariant is $X(d) \le 2\lceil X/D \rceil$ for all $d$.

**Lemma 3.** Before each placement for bucket $b$, more than $D/2$ disks are allowed for $b$, not counting the disks already used in the same write step.

*Proof.* Let $c = \lceil (X + 1)/D \rceil \ge 1$. A disk $d$ is not allowed if $X(d) + 1 > 2c$, that is, $X(d) \ge 2c$. If $t$ disks are not allowed, then $2ct \le \sum_d X(d) = X \le cD - 1$, because $X + 1 \le cD$. So $t < D/2$, and more than $D/2$ disks are allowed. $\blacksquare$

**Lemma 4 (invariant).** After each placement, $X_b(d) \le 2\lceil X_b/D \rceil$ for all buckets $b$ and disks $d$.

*Proof.* At the start all counts are 0. A placement of a block of $b$ on an allowed disk $d$ makes $X_b(d)$ at most $2\lceil (X_b + 1)/D\rceil$, which is $2\lceil X_b'/D \rceil$ for the new total $X_b' = X_b + 1$. The other counts of $b$ do not change, and $\lceil X_b/D \rceil$ does not decrease. The counts of the other buckets do not change. $\blacksquare$

**Theorem 2.** Each write step places at least $\min(R, \lfloor D/2 \rfloor + 1)$ blocks, where $R$ is the number of ready blocks at its start. At the end of the pass, each bucket of $X$ blocks can be read in at most $2\lceil X/D \rceil$ parallel reads.

*Proof.* Suppose that a write step has placed $u < \lfloor D/2 \rfloor + 1$ blocks when it looks at the next ready block, of bucket $b$. Then $u \le D/2$ disks are used. By Lemma 3, more than $D/2$ disks are allowed for $b$, so at least one of them is unused, and line L7 places the block. So the step places blocks as long as fewer than $\lfloor D/2 \rfloor + 1$ are placed and ready blocks remain. For the second part, a parallel read takes one block from each disk, so a bucket can be read in $\max_d X(d)$ steps, which is at most $2\lceil X/D \rceil$ by Lemma 4. $\blacksquare$
