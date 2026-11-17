---
title: Greedy NMS returns the unique set of boxes that no higher kept box suppresses and that suppresses every other box
proves: [correctness]
status: full
---

We use the notation of the page. The input is $n$ boxes $B_1, \ldots, B_n$ with scores $s_1, \ldots, s_n$, a threshold $t$ and an overlap function $o$, by default IoU. The rank order $\pi$ of line L1 sorts the indices by decreasing score and breaks ties by the smaller index, so it is a total order. We write $i \prec j$ when $i$ comes before $j$ in $\pi$, and we say that $i$ *suppresses* $j$ when $i \prec j$ and $o(B_i, B_j) > t$.

**Claim.** Let $K$ be the list that GREEDY-NMS returns in line L9. Then

1. (no conflict) no member of $K$ is suppressed by another member of $K$;
2. (cover) every index not in $K$ is suppressed by some member of $K$;
3. (uniqueness) $K$ is the only subset of $\{1, \ldots, n\}$ with properties 1 and 2;
4. $K$ is in rank order, and its first member is the box with the highest score.

**Lemma 1 (what the flags mean).** When line L3 reaches an index $j$, $\mathit{removed}[j]$ is true exactly when some index $i \prec j$ that is already in $K$ suppresses $j$.

*Proof.* Line L8 is the only line that sets a flag, and it sets $\mathit{removed}[j]$ only for an index $j$ after the current kept index $i$ in the order, with $o(B_i, B_j) > t$; so a set flag has such an $i$. For the converse, let $i \in K$ with $i \prec j$ and $o(B_i, B_j) > t$. When line L5 added $i$, the loop of lines L6 to L8 visited every index after $i$, including $j$. Either $j$ was flagged before that visit, or the test of line L7 is true and line L8 flags it. Flags are never cleared. $\square$

**Lemma 2 (the loop decides each index once).** Each index is visited once by line L3, in the order $\pi$, and it goes into $K$ exactly when its flag is false at that visit.

*Proof.* Line L3 iterates over $\pi$ once. Line L4 skips a flagged index and line L5 appends an unflagged one. A flag can change only for indices after the current one, so the flag of $j$ that line L4 reads is final for every decision about $j$. $\square$

*Proof of the claim.* Parts 1 and 2 follow from Lemmas 1 and 2. If $j \in K$, its flag was false at its visit, so no earlier member of $K$ suppresses it; a later member cannot suppress it because suppression needs $i \prec j$. If $j \notin K$, its flag was true, so an earlier member of $K$ suppresses it.

For part 3, let $S$ be any subset with properties 1 and 2. We show by induction along $\pi$ that $j \in S$ exactly when $j \in K$. Assume that $S$ and $K$ agree on all indices before $j$. Then the members of $S$ that come before $j$ are the members of $K$ that come before $j$; call this set $P$. Only members of $P$ can suppress $j$. If some member of $P$ suppresses $j$, then $j \notin S$ by property 1 of $S$ and $j \notin K$ by property 1 of $K$. If no member of $P$ suppresses $j$, then $j \in S$ by property 2 of $S$ and $j \in K$ by property 2 of $K$. So $S$ and $K$ agree on $j$, and by induction $S = K$.

For part 4, line L5 appends in the order of line L3, which is $\pi$. The first index of $\pi$ has a false flag at its visit, because no index comes before it. $\square$

**Remark (the threshold).** Part 3 describes the output without the loop, which is what the tests compare with a search over all subsets. It also shows why the output is not monotone in $t$. With a lower $t$, an index of high rank can be suppressed, and then a later index that it suppressed before may have no suppressor left and join the output. The example on the page shows this: at $t = 0.5$ box 5 is removed by box 3, and at $t = 0.2$ box 3 is removed by box 1, so box 5 stays.

**Remark (symmetry).** The proof never uses $o(B_i, B_j) = o(B_j, B_i)$, so it holds for the coverage overlap of the deformable part model code as well. Property 1 then refers to the direction of the rank order.

**Cost.** Line L1 sorts in $O(n \log n)$ comparisons. For each kept index, lines L6 to L8 visit the indices after it, at most $n - 1$, and each visit costs one overlap, $O(1)$ for two boxes. With $k$ kept boxes the loop costs $O(n k)$, so $O(n^2)$ in the worst case. If the $n$ boxes are pairwise disjoint, every box is kept and line L7 evaluates all $n (n - 1) / 2$ pairs, so the bound is tight.
