---
title: After a monotone presort, every window tuple of SFS is a skyline tuple, and SFS outputs the skyline in exactly the ceiling of |S|/w passes
proves: [correctness, termination, complexity]
status: full
---

Setting. The input is a finite sequence of $n$ tuples in $\mathbb{R}^d$, told apart by position. Tuple $p$ *dominates* $q$, written $p \prec q$, if $p_i \le q_i$ for all $i$ and $p_i < q_i$ for some $i$; this relation is irreflexive and transitive. The skyline $S$ is the set of tuples that no tuple dominates. A score $s: \mathbb{R}^d \to \mathbb{R}$ is *monotone* if $p \prec q$ implies $s(p) \le s(q)$. The sum and the entropy $E(p) = \sum_i \ln(1 + p_i)$ (for $p_i > -1$) are strictly monotone. In floating point, rounding can turn $s(p) < s(q)$ into $s(p) = s(q)$, which is why the sort key breaks ties by the tuple; the proof assumes only that the computed score is monotone. Line L1 sorts by the key $(s(p), p)$, with $p$ compared in lexicographic order. The window holds at most $w \ge 1$ tuples. Pass $j$ scans the source $F_j$ in order; $F_1$ is the sorted input, and $F_{j+1}$ is the temporary file $T_j$ of pass $j$.

**Lemma 1 (presort).** If $p \prec q$, then $p$ comes before $q$ in the sorted order.

*Proof.* By monotonicity, $s(p) \le s(q)$. If $s(p) = s(q)$, compare the tuples: $p \ne q$ and $p_i \le q_i$ for all $i$, so at the first coordinate where they differ, $p_i < q_i$, and $p$ is smaller in lexicographic order. $\square$

So no tuple is dominated by a tuple that comes later in the sorted order. Each $F_j$ is a subsequence of the sorted order, since line L7 appends in scan order.

**Lemma 2 (shape of a pass).** In each pass, the window only grows. Once it is full, every later tuple of the pass is dropped or written to $T_j$. The window is emptied only at line L3, at the start of the next pass.

*Proof.* No line removes a tuple from the window during a pass. $\square$

**Lemma 3 (window tuples are skyline tuples).** If $p$ enters the window, then $p \in S$.

*Proof.* Suppose $p$ enters the window in pass $j$, and some tuple dominates $p$. The set of tuples that dominate $p$ is finite and nonempty; let $r$ be minimal in it under $\prec$. Then nothing dominates $r$ (it would also dominate $p$), so $r \in S$, and a tuple that nothing dominates is never dropped at line L5. By Lemma 1, $r$ comes before $p$ in the sorted order.

Since $p$ is in $F_j$, it is in every earlier source too. Consider the pass $j'$ in which $r$ enters the window, if there is one, or else note that $r$ is in $F_{j+1}$.

- If $j' < j$: in pass $j'$, $p$ is in $F_{j'}$ after $r$. When $p$ is scanned, $r$ is in the window (Lemma 2), so the loop at line L5 finds a window tuple that dominates $p$, either $r$ or one before it, and drops $p$. Then $p$ is not in $F_j$, a contradiction.
- If $j' = j$: $r$ is scanned before $p$ in pass $j$, and again $p$ is dropped.
- Otherwise $r$ was written to $T_j$ in pass $j$, before $p$ was scanned. When $r$ was written, the window was full, and by Lemma 2 it was still full when $p$ was scanned, so $p$ could not enter it.

Each case contradicts the assumption. $\blacksquare$

**Theorem 1 (correctness).** SFS outputs each skyline tuple exactly once, and no other tuple. Each tuple is output at the moment it enters the window.

*Proof.* Line L6 outputs a tuple when it enters the window, and by Lemma 3 it is in $S$. A tuple is never in the window and in $T_j$ at once, and the window tuples are not copied to the next source, so each tuple enters the window at most once. A skyline tuple is never dropped. In a pass with a nonempty source, the first tuple enters the empty window, so the source shrinks by at least one in each pass; when it is empty, every tuple has been dropped or has entered the window. So every skyline tuple enters the window once. $\blacksquare$

**Theorem 2 (passes).** If $n \ge 1$, SFS makes exactly $\lceil |S| / w \rceil$ passes.

*Proof.* A pass that writes a tuple to the temporary file has a full window at that point, so it outputs exactly $w$ tuples (Lemma 2 and Theorem 1). The last pass writes nothing and outputs at least one tuple, the first of its source, and at most $w$. So with $P$ passes, $(P - 1) w < |S| \le P w$. $\blacksquare$

**Theorem 3 (dominance tests).** Each unordered pair of tuples is tested for dominance at most once, so there are at most $n(n - 1)/2$ tests.

*Proof.* A test compares a scanned tuple $p$ with a tuple $q$ in the window. Then $q$ comes before $p$ in the source, so in the sorted order, and the pair is never tested with the roles swapped. And $q$ is in the window during one pass only, in which $p$ is scanned once. $\blacksquare$

With the sort, the total time is $O(n \log n)$ key comparisons, $O(d n)$ to compute the scores, and $O(d n^2)$ for the dominance tests in the worst case. Each pass reads its source once and writes at most that many tuples.
