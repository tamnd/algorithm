---
title: Interval containment by sorting keeps one copy of each maximal interval
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The intervals $I[1], \ldots, I[n]$ are nonempty and of one type, so $I[k] \subseteq I[j]$ holds if and only if $I[j].l \le I[k].l$ and $I[k].r \le I[j].r$. Write $j \prec k$ when $j$ comes before $k$ in $order$. By line L1, $j \prec k$ if and only if $I[j].l < I[k].l$, or the left ends are equal and $I[j].r > I[k].r$, or both end points are equal and $j < k$.

**Claim.** CONTAINMENT-SORT stops after $n$ steps. For each $k$, if $parent[k] = j \ne$ nil, then $j \ne k$ and $I[k] \subseteq I[j]$. And $parent[k] = $ nil if and only if $I[k]$ is maximal (no interval of the family properly contains it) and no index $j < k$ has $I[j] = I[k]$.

**Lemma 1.** If $I[k] \subseteq I[j]$ and $j \ne k$, then $j \prec k$, unless $I[j] = I[k]$ and $j > k$.

*Proof.* We have $I[j].l \le I[k].l$. If $I[j].l < I[k].l$, then $j \prec k$. Otherwise the left ends are equal and $I[j].r \ge I[k].r$. If $I[j].r > I[k].r$, then $j \prec k$. Otherwise the intervals are equal, and $j \prec k$ exactly when $j < k$. $\square$

**Lemma 2.** If $j \prec k$, then $I[j].l \le I[k].l$. So if also $I[k].r \le I[j].r$, then $I[k] \subseteq I[j]$.

*Proof.* The sort is by left end first. $\square$

**Invariant.** Let $P$ be the set of indices processed so far. Before each step of the loop of line L3:

> **(I)** If $P$ is empty, $best = $ nil. Otherwise $best \in P$, $I[best].r = \max_{j \in P} I[j].r$, and $parent[best] = $ nil.

*Initialization.* Line L2 sets $best = $ nil and $P$ is empty.

*Maintenance.* Let $k$ be the next index. If $best = $ nil, then $P$ is empty, line L6 sets $best \leftarrow k$, and $parent[k]$ stays nil, so (I) holds for $P \cup \{k\}$. Otherwise, if $I[k].r \le I[best].r$, line L5 sets $parent[k]$, and $best$ keeps its value, which is still the maximum of the right ends over $P \cup \{k\}$; $parent[best]$ is unchanged, because $best \ne k$. If $I[k].r > I[best].r$, then $I[k].r$ is the new maximum, line L6 sets $best \leftarrow k$, and $parent[k]$ is nil. In both cases (I) holds.

**Each step decides its interval.** Consider the step for $k$, with $P$ the set of indices before $k$ in $order$.

*If line L5 runs*, then $best \in P$, so $best \prec k$ and $best \ne k$, and $I[k].r \le I[best].r$. By Lemma 2, $I[k] \subseteq I[best]$.

*If line L6 runs*, then either $P$ is empty or $I[k].r > \max_{j \in P} I[j].r$ by (I). So no $j \prec k$ has $I[k].r \le I[j].r$, and no $j \prec k$ contains $I[k]$. Suppose $I[j]$ properly contains $I[k]$. Then $I[j] \ne I[k]$, so $j \prec k$ by Lemma 1, a contradiction. Suppose $I[j] = I[k]$ with $j < k$. Then $j \prec k$ by the tie rule, and $I[j]$ contains $I[k]$, a contradiction. So $I[k]$ is maximal and has no equal copy with a smaller index.

**Conversely.** If $I[k]$ is properly contained in some $I[j]$, then $j \prec k$ by Lemma 1, so $P$ is not empty and $I[best].r \ge I[j].r \ge I[k].r$ by (I); line L5 runs. If $I[j] = I[k]$ for some $j < k$, then $j \prec k$, and again $I[best].r \ge I[j].r = I[k].r$; line L5 runs. So in both cases $parent[k] \ne$ nil.

**Termination.** Line L1 is a sort of $n$ keys, and the loop of line L3 runs once for each of the $n$ indices. Each $parent[k]$ is written at most once, in the step for $k$, so later steps do not change it.

*Conclusion.* The two parts above give the claim: every non-nil $parent[k]$ is a container of $I[k]$ with a different index, and $parent[k]$ is nil exactly for the first copy, by index, of each maximal interval. $\blacksquare$
