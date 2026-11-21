---
title: MDAV returns a partition into groups of k to 2k - 1 records and a k-anonymous release
proves: [correctness]
status: full
---

The input is a list $X$ of $n$ records $x_1, \ldots, x_n$ in $\mathbb{R}^d$ and an integer $k$ with $1 \le k \le n$. Lines L1 to L14 are those of the page. We write $R$ for the set of indices that are in no group yet, and $G$ for the list of groups.

**Lemma 1 (the loop).** At each test of line L2, the groups of $G$ are pairwise disjoint, each has exactly $k$ indices, $R$ is the set of indices in no group of $G$, and $|R| \ge k$.

*Proof.* By induction on the number of rounds. Before the first test, $G$ is empty, $R = \{1, \ldots, n\}$, and $|R| = n \ge k$.

Assume the claim at a test where $|R| \ge 3k$, so the body runs. Line L4 picks $r \in R$. Line L5 forms $g_r$ from $r$ and $k - 1$ other indices of $R$, which exist because $|R| - 1 \ge 3k - 1 \ge k - 1$. So $|g_r| = k$, $g_r \subseteq R$, and after the removal $|R| \ge 2k$. Line L6 picks $s$ in the new $R$, which is not empty, and line L7 forms $g_s \subseteq R$ with $|g_s| = k$ in the same way, because $|R| - 1 \ge 2k - 1 \ge k - 1$. After the removal $|R| \ge k$. Both new groups are taken from $R$ and then removed from $R$, so they are disjoint from each other and from the old groups, and $R$ is again the set of indices in no group. $\square$

**Lemma 2 (the tail).** At line L11, $k \le |R| \le 2k - 1$.

*Proof.* The loop stops when $|R| < 3k$, and by Lemma 1, $|R| \ge k$ at that test. If $|R| \ge 2k$, lines L9 and L10 take a group of exactly $k$ indices from $R$, as in Lemma 1, and leave $k \le |R| < 2k$. If $|R| < 2k$, line L8 does nothing, and $k \le |R| < 2k$ already holds. $\square$

**Theorem.** MDAV stops after at most $\lfloor n / (2k) \rfloor$ rounds of the loop. It returns a list $G$ of groups that is a partition of $\{1, \ldots, n\}$, in which every group but the last has exactly $k$ indices and the last has between $k$ and $2k - 1$ indices. In the released records of lines L12 and L13, every record value occurs at least $k$ times, so the release is k-anonymous for any set of its attributes taken as the quasi-identifier. The sum of the released records over all $n$ records equals the sum of the original records.

*Proof.* Each round removes $2k \ge 2$ indices from $R$, and the body runs only while $|R| \ge 3k$, so there are at most $\lfloor n / (2k) \rfloor$ rounds, and the algorithm stops.

By Lemma 1 at the last test and by Lemma 2, the groups appended at lines L5, L7 and L10 are disjoint sets of exactly $k$ indices, and line L11 appends the set $R$ of all other indices, with $k \le |R| \le 2k - 1$. So $G$ is a partition of $\{1, \ldots, n\}$ with the stated sizes.

Lines L12 and L13 give every record of a group $g$ the value $\bar{x}_g$, the centroid of $g$. So the value $\bar{x}_g$ occurs at least $|g| \ge k$ times in the release. Two groups can have the same centroid, which only adds occurrences. Any projection of the release onto a set of attributes keeps these repeated values equal, so each combination of quasi-identifier values occurs at least $k$ times.

Last, for each group, $\sum_{i \in g} \bar{x}_g = |g| \bar{x}_g = \sum_{i \in g} x_i$. The groups partition the records, so the sums over all records are equal. $\blacksquare$

**Cost.** Let $m$ be the size of $R$ at the start of a round. Lines L3, L4 and L6 take $O(m d)$ time. Lines L5 and L7 compute $m$ distances in $O(m d)$ time and select the $k - 1$ least with a heap of size $k$ in $O(m \log k)$ time. The sizes of $R$ at the rounds are $n, n - 2k, n - 4k, \ldots$, so their sum is at most $n + n^2 / (4k)$. Lines L8 to L13 take $O(n d + n \log k)$ time. The total is $O(n^2 (d + \log k) / k + n d)$.

**Remark.** The theorem says nothing about the loss. The page gives a table of 10 records where MDAV has an SSE of $593/12$ and the optimal 3-partition has $221/12$. MDAV is a heuristic for the partition; only the sizes of the groups, and so the k-anonymity of the release, are a theorem.
