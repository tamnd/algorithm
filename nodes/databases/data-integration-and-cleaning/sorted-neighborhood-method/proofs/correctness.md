---
title: The sorted neighborhood method compares exactly the pairs inside the window and returns the closure of their matches
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page. $D$ has $n$ records, there are $p$ keys, the window size is $w \ge 1$, and $\mathit{match}$ is any function on pairs of records that always returns. The claims are about what the method computes. Whether its clusters are the true entities depends on the keys and on the match rule, and nothing is proved about that.

**Lemma 1 (the pairs of one pass).** Let $L[1..n]$ be the sorted list of line L3. Lines L4 to L6 call $\mathit{match}$ exactly once on each pair of positions $(j, i)$ with $1 \le i - j \le w - 1$, and on no other pair.

*Proof.* Line L4 visits each $i$ once, and line L5 visits the $j$ with $\max(1, i - w + 1) \le j \le i - 1$, which are exactly the $j < i$ with $i - j \le w - 1$. Two different values of $i$ give disjoint sets of pairs, because the larger position of the pair is $i$. $\square$

**Lemma 2 (the number of calls).** One pass makes $\sum_{i=1}^{n} \min(i - 1, w - 1)$ calls. This is $n(n-1)/2$ if $n \le w$, and $(w - 1) n - w (w - 1)/2$ if $n \ge w$.

*Proof.* The first form is Lemma 1. If $n \le w$, then $i - 1 \le w - 1$ for every $i$, and the sum is $0 + 1 + \cdots + (n - 1)$. If $n \ge w$, the positions $i = 1, \ldots, w - 1$ give $0 + 1 + \cdots + (w - 2) = (w - 1)(w - 2)/2$, and the $n - w + 1$ positions $i \ge w$ give $w - 1$ each. The total is $(w - 1)(n - w + 1) + (w - 1)(w - 2)/2 = (w - 1)(n - w/2)$. $\square$

**Lemma 3 (the output).** Let $P$ be the set after line L6 of the last pass. Then $P$ is the set of pairs $\{x, y\}$ of records such that for some key $K_t$, $x$ and $y$ are less than $w$ positions apart in the order of $K_t$ and $\mathit{match}$ returned true on them. Line L8 returns the connected components of the graph $(D, P)$.

*Proof.* Line L1 starts with $P = \emptyset$, and by Lemma 1 the pass for $K_t$ adds exactly the matching pairs inside its window; the passes only add. Line L7 computes the components with union-find: each union joins the sets of the two ends of an edge of $P$, so two records end in the same set if and only if a path of edges of $P$ joins them. $\square$

**Corollary (the full window).** If $w \ge n$, one pass calls $\mathit{match}$ on all $n(n-1)/2$ pairs, so $P$ is the set of all matching pairs, and the output is the transitive closure of the match relation. For $w < n$, $P$ is a subset of that set, and every cluster of the output lies inside one cluster of the full closure: the method can miss merges but never adds a merge that the full comparison would not make.

**Termination and cost.** Each pass sorts $n$ records in $O(n \log n)$ key comparisons and makes the calls of Lemma 2, so the total is $O(p (n \log n + w n))$ key comparisons and match calls. Line L7 makes at most $|P| \le p (w - 1) n$ unions, each in near constant amortized time. All loops are bounded, so the method stops. $\blacksquare$
