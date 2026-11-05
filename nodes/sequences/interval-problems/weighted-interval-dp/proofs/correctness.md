---
title: The weighted interval DP returns a disjoint set of largest weight
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. After line L1 the intervals are $I_1, \ldots, I_n$ with $r_1 \le r_2 \le \cdots \le r_n$, all of one type, with weights $w_j > 0$. Say that $I_i$ *ends in time* for $I_j$ when $r_i \le l_j$ for half-open and open intervals and $r_i < l_j$ for closed intervals; this is the test counted on line L2. For a set $A$ of indices let $w(A) = \sum_{i \in A} w_i$. A set is *feasible* when its intervals are pairwise disjoint. Let $\mathrm{OPT}(j)$ be the largest weight of a feasible subset of $\{1, \ldots, j\}$, with $\mathrm{OPT}(0) = 0$.

**Lemma 1 (disjoint means ends in time).** For $i < j$, $I_i \cap I_j = \emptyset$ if and only if $I_i$ ends in time for $I_j$.

*Proof.* If $I_i$ ends in time, every point of $I_i$ is at most $r_i$, and less than $r_i$ for half-open and open intervals, while every point of $I_j$ is at least $l_j$, and greater than $l_j$ for open intervals. In each type the two sets are separated, so they are disjoint. Conversely, suppose that $I_i$ does not end in time: $r_i \ge l_j$ for closed intervals, $r_i > l_j$ for the others. Since $i < j$, $r_i \le r_j$. For closed intervals, the point $\max(l_i, l_j)$ lies in both: it is at least both left ends and at most $r_i \le r_j$, because $l_i \le r_i$ and $l_j \le r_i$. For half-open and open intervals, let $L = \max(l_i, l_j)$; then $L < r_i \le r_j$, since $l_i < r_i$ and $l_j < r_i$, and the points strictly between $L$ and $r_i$ lie in both intervals. $\square$

**Lemma 2 (prefix).** The indices $i$ that end in time for $I_j$ are exactly $1, \ldots, p[j]$, and $p[j] < j$.

*Proof.* If $I_i$ ends in time for $I_j$, then $r_i < r_j$: for closed intervals $r_i < l_j \le r_j$, and for the others $r_i \le l_j < r_j$. So $i < j$ in the sorted order, whatever the order of equal right ends. The test "ends in time" depends on $r_i$ only through a threshold, $r_i \le l_j$ or $r_i < l_j$, and the $r_i$ are sorted, so the indices that pass form a prefix, of length $p[j]$ by line L2. Index $j$ itself fails, so $p[j] < j$. $\square$

**Lemma 3 (recurrence).** For $j \ge 1$, $\mathrm{OPT}(j) = \max(\mathrm{OPT}(j - 1), w_j + \mathrm{OPT}(p[j]))$.

*Proof.* ($\ge$) A feasible subset of $\{1, \ldots, j - 1\}$ is a feasible subset of $\{1, \ldots, j\}$. If $B$ is a feasible subset of $\{1, \ldots, p[j]\}$, then by Lemmas 2 and 1 every interval of $B$ is disjoint from $I_j$, so $B \cup \{j\}$ is feasible, with weight $w_j + w(B)$.

($\le$) Let $A$ be a feasible subset of $\{1, \ldots, j\}$ with $w(A) = \mathrm{OPT}(j)$. If $j \notin A$, then $A \subseteq \{1, \ldots, j - 1\}$ and $w(A) \le \mathrm{OPT}(j - 1)$. If $j \in A$, every other $i \in A$ has $i < j$ and is disjoint from $I_j$, so by Lemmas 1 and 2, $i \le p[j]$. So $A \setminus \{j\}$ is a feasible subset of $\{1, \ldots, p[j]\}$, and $w(A) \le w_j + \mathrm{OPT}(p[j])$. $\square$

**Theorem 1 (the table).** After lines L3 to L5, $M[j] = \mathrm{OPT}(j)$ for $0 \le j \le n$.

*Proof.* By induction on $j$. $M[0] = 0 = \mathrm{OPT}(0)$. For $j \ge 1$, line L5 reads $M[j - 1]$ and $M[p[j]]$ with $p[j] < j$ by Lemma 2, which equal $\mathrm{OPT}(j - 1)$ and $\mathrm{OPT}(p[j])$ by induction, so $M[j] = \mathrm{OPT}(j)$ by Lemma 3. $\square$

**Theorem 2 (the traceback).** Lines L6 to L9 terminate and return a feasible set $S$ with $w(S) = \mathrm{OPT}(n)$.

*Proof.* Invariant at the test of line L7: (a) $w(S) + M[j] = M[n]$, and (b) $S$ is feasible and every interval of $S$ is disjoint from every $I_i$ with $i \le j$.

It holds at the start with $S = \emptyset$ and $j = n$. Suppose it holds with $j > 0$.

*Line L8 takes $j$.* Then $w_j + M[p[j]] \ge M[j - 1]$, so by line L5, $M[j] = w_j + M[p[j]]$, and $w(S \cup \{j\}) + M[p[j]] = w(S) + M[j] = M[n]$, which is (a). By (b), $j$ is disjoint from every interval of $S$, so $S \cup \{j\}$ is feasible. For $i \le p[j]$, $I_i$ is disjoint from $I_j$ by Lemmas 2 and 1, and from every interval of $S$ by (b), since $i \le p[j] < j$. So (b) holds with $p[j]$ in place of $j$.

*Line L9 skips $j$.* Then $w_j + M[p[j]] < M[j - 1]$, so $M[j] = M[j - 1]$, and (a) holds for $j - 1$. (b) holds for $j - 1$ since it held for $j$.

Each pass lowers $j$, by Lemma 2 in the first case, so the loop stops with $j = 0$. Then (a) gives $w(S) = M[n] - M[0] = \mathrm{OPT}(n)$ by Theorem 1, and (b) says that $S$ is feasible.

**Termination of the rest.** Line L1 sorts $n$ keys, line L2 does $n$ binary searches, and the loop of line L4 runs $n$ times. $\blacksquare$
