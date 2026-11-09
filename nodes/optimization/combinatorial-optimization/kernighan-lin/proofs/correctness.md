---
title: Kernighan-Lin keeps the side sizes, lowers the cut in every applied pass, terminates, and returns a partition that no single swap improves
proves: [correctness, termination, local optimality, gain formula]
status: full
---

Let $G = (V, E)$ have symmetric non-negative weights $w(u, v)$, with $w(u, v) = 0$ for non-edges and $w(v, v) = 0$. For a partition $(A, B)$ of $V$ write $\mathrm{cut}(A, B) = \sum_{u \in A, v \in B} w(u, v)$. For a vertex $v$ let $E(v)$ be the total weight of the edges from $v$ to the other side and $I(v)$ the total weight of the edges from $v$ to its own side, and let $D(v) = E(v) - I(v)$.

**Lemma 1 (gain of a swap).** For $a \in A$ and $b \in B$, let $(A', B') = (A - a + b, B - b + a)$. Then
$$ \mathrm{cut}(A, B) - \mathrm{cut}(A', B') = D(a) + D(b) - 2 w(a, b). $$

*Proof.* An edge that touches neither $a$ nor $b$ has the same status, cut or not cut, before and after the swap. The edge $\{a, b\}$ is cut before and after, because both ends change sides. Consider the other edges at $a$. Before the swap, the cut edges among them have weight $E(a) - w(a, b)$ and the uncut ones have weight $I(a)$. After the swap, $a$ is on the other side, so exactly these two groups exchange status. Their contribution to the cut changes by $I(a) - (E(a) - w(a, b))$. In the same way the edges at $b$ other than $\{a, b\}$ change the cut by $I(b) - (E(b) - w(a, b))$. No edge is counted twice, since $\{a, b\}$ is excluded from both groups. The total change of the cut is
$$ I(a) - E(a) + I(b) - E(b) + 2 w(a, b) = -(D(a) + D(b) - 2 w(a, b)). \qquad \square $$

**Lemma 2 (update of D).** In the situation of Lemma 1, let $D'$ be the $D$ values for $(A', B')$. For $x \in A \setminus \{a\}$ and $y \in B \setminus \{b\}$,
$$ D'(x) = D(x) + 2 w(x, a) - 2 w(x, b), \qquad D'(y) = D(y) + 2 w(y, b) - 2 w(y, a). $$

*Proof.* The vertex $x$ stays in its side. Only the edges from $x$ to $a$ and to $b$ change status. The edge $\{x, a\}$ was internal and becomes external, so $E$ grows by $w(x, a)$ and $I$ falls by $w(x, a)$, and $D$ grows by $2 w(x, a)$. The edge $\{x, b\}$ was external and becomes internal, so $D$ falls by $2 w(x, b)$. The case of $y$ is the same with the roles of $a$ and $b$ exchanged. $\square$

**Lemma 3 (one pass).** Consider one pass of lines L2 to L8, started from the partition $(A, B)$ with $m = \min(|A|, |B|)$. Let $(a_1, b_1), \ldots, (a_m, b_m)$ and $g_1, \ldots, g_m$ be the pairs and gains of line L5, and let $(A_k, B_k)$ be the partition obtained from $(A, B)$ by moving $a_1, \ldots, a_k$ to $B$ and $b_1, \ldots, b_k$ to $A$. Then for each $k$:

1. $a_1, \ldots, a_k$ are distinct elements of $A$, and $b_1, \ldots, b_k$ are distinct elements of $B$;
2. $|A_k| = |A|$ and $|B_k| = |B|$;
3. $\mathrm{cut}(A_k, B_k) = \mathrm{cut}(A, B) - G_k$, where $G_k = g_1 + \cdots + g_k$;
4. after step $k$, the stored value $D(v)$ of each unlocked vertex $v$ equals its $D$ value for $(A_k, B_k)$.

*Proof.* By induction on $k$. For $k = 0$, line L2 computes $D$ for $(A_0, B_0) = (A, B)$, nothing is locked, and claims 1 to 3 hold trivially. Let $k \ge 1$. The tentative partition before step $k$ is $(A_{k-1}, B_{k-1})$. An unlocked vertex of $A_{k-1}$ has never been moved, since every moved vertex is locked at once, so it is in $A$. In the same way an unlocked vertex of $B_{k-1}$ is in $B$. There are $|A| - (k-1) \ge 1$ unlocked vertices in $A_{k-1}$ and $|B| - (k-1) \ge 1$ in $B_{k-1}$, so line L4 finds a pair. This gives claim 1. Claim 2 holds because one vertex leaves each side and one enters it. By claim 4 for $k - 1$, the value $g_k$ computed in line L4 is $D(a_k) + D(b_k) - 2 w(a_k, b_k)$ with the true $D$ values of $(A_{k-1}, B_{k-1})$. Lemma 1 gives $\mathrm{cut}(A_k, B_k) = \mathrm{cut}(A_{k-1}, B_{k-1}) - g_k$, which with claim 3 for $k - 1$ gives claim 3. Lines L6 and L7 apply exactly the formulas of Lemma 2 to the unlocked vertices, so claim 4 holds. $\square$

**Lemma 4 (a full balanced pass).** If $|A| = |B| = m$, then $G_m = 0$.

*Proof.* By claim 1 of Lemma 3, after $m$ steps all of $A$ has moved to $B$ and all of $B$ to $A$. So $(A_m, B_m) = (B, A)$, which has the same cut as $(A, B)$, and claim 3 gives $G_m = 0$. $\square$

**Theorem.** Let the algorithm start from a partition $(A, B)$.

1. Every partition that the algorithm holds in lines L1 to L10 has sides of sizes $|A|$ and $|B|$.
2. Each execution of line L10 lowers the cut by $G_{k^*} > 0$, where $k^*$ is the index chosen in line L8.
3. The algorithm terminates. With integer weights it runs at most $\mathrm{cut}(A, B) + 1$ passes.
4. The output partition $(A^*, B^*)$ is a local optimum for single swaps: for all $a \in A^*$ and $b \in B^*$, swapping $a$ and $b$ does not lower the cut.

*Proof.* Line L10 replaces the current partition by $(A_{k^*}, B_{k^*})$ in the notation of Lemma 3. Claim 2 of Lemma 3 gives part 1, and claim 3 gives a new cut of $\mathrm{cut}(A, B) - G_{k^*}$. Line L10 runs only if line L9 did not stop, that is, if $G_{k^*} > 0$. This is part 2.

For part 3, the cut takes values in a finite set, since there are finitely many partitions, and by part 2 it strictly falls with each pass except the last. So no partition repeats and the loop ends. With integer weights each applied pass lowers the cut by at least 1, and the cut is never negative, so at most $\mathrm{cut}(A, B)$ passes apply a change, and one more pass ends the loop.

For part 4, consider the last pass, which starts from $(A^*, B^*)$ and stops at line L9. If $A^*$ or $B^*$ is empty, there is no swap and nothing to prove. Otherwise, in its first step all vertices are unlocked and $D$ is exact by Lemma 3, so by Lemma 1 the value $g_1$ of line L4 is the largest decrease of the cut over all pairs $a \in A^*$, $b \in B^*$. Line L8 takes the largest $G_k$ over $k \ge 0$, with $G_0 = 0$, and line L9 stops only if this maximum is at most 0. In particular $g_1 = G_1 \le 0$. So no single swap lowers the cut. $\blacksquare$

**Remark.** Part 4 is weaker than what the algorithm achieves: the output also admits no improving prefix of a pass, which is a much larger neighborhood. It does not imply global optimality. By Lemma 4, in a balanced pass the gains of all $m$ swaps add up to 0, so the last step of such a pass never gives a better prefix than $k = 0$, and an implementation can stop the pass after $m - 1$ steps.
