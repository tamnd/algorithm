---
title: The splitter recursion of Han's sort returns its input in sorted order
proves: [correctness, termination]
status: full
---

We prove the claim for the recursion of the pseudocode, for any sample that line L3 takes from $A$ and any method of line L5 that finds the correct part of each key. The speed of Han's algorithm comes from how it does lines L3 and L5; the correctness does not depend on it.

**Claim.** For each finite list $A$ of integers, HAN-SORT$(A)$ returns the keys of $A$, with their counts, in non-decreasing order.

*Proof.* Induction on $n = |A|$.

**Base.** If $n \le c$, line L1 returns the result of insertion sort, which is correct.

**Step.** Let $n > c$, and assume the claim for all lists with fewer than $n$ keys. The sample $P$ has about $n / k \le \sqrt{n} + 1 < n$ keys (for $n > c \ge 2$), so by the hypothesis line L4 returns $P$ sorted, and after the removal of duplicates $p_1 < \cdots < p_s$ with $s \ge 1$, since $P$ is not empty.

*Each key goes to exactly one set.* For a key $x$, either $x = p_j$ for one $j$, and then $x \in E_j$, or $x$ differs from all splitters, and then there is exactly one $j \in \{0, \ldots, s\}$ with $p_j < x < p_{j+1}$, with $p_0 = -\infty$ and $p_{s+1} = +\infty$, and $x \in B_j$. So the sets $E_1, \ldots, E_s, B_0, \ldots, B_s$ split the keys of $A$, with their counts.

*Each part is smaller.* Each $p_j$ is a key of $A$, and no key of $B_0 \cup \cdots \cup B_s$ is equal to a splitter. So $|B_j| \le n - |E_1| < n$, since $E_1$ contains $p_1$. By the hypothesis, line L7 sorts each $B_j$.

*The order.* Let $x$ come before $y$ in the output of line L8. If they are in the same set, then either the set is some $E_j$ and $x = y = p_j$, or the set is some $B_j$, which is sorted, so $x \le y$. If they are in different sets, the set of $x$ comes first in the order $B_0, E_1, B_1, \ldots, E_s, B_s$. Each key of $B_{j-1}$ is less than $p_j$, each key of $E_j$ equals $p_j$, and each key of $B_j$ is greater than $p_j$. So the sets are in increasing order of their keys: all keys of a set are less than all keys of each later set. Hence $x < y$.

So the output holds the keys of $A$ with their counts, and it is in non-decreasing order.

*Termination.* Each call makes calls only on lists with fewer keys (the sample and the parts), so the recursion is finite. $\blacksquare$
