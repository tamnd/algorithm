---
title: Scatter search for 0-1 knapsack keeps a reference set of distinct feasible maximal solutions, never loses its best one, and stops
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The instance has $n$ items with values $v_i > 0$, weights $w_i > 0$ and a capacity $C \ge 0$. A solution is a vector $x \in \{0, 1\}^n$, with value $v(x) = \sum_i v_i x_i$ and weight $w(x) = \sum_i w_i x_i$. It is *feasible* if $w(x) \le C$ and *maximal* if it is feasible and no item with $x_i = 0$ fits, that is, $w(x) + w_i > C$ for every such $i$. REPAIR removes packed items, the lowest value per weight first, while the weight exceeds $C$. IMPROVE goes through the items once, the highest value per weight first, and packs each item that fits.

**Lemma 1 (repair).** REPAIR returns a feasible $y$ with $y \le x$ in each position, and $y = x$ if $x$ is feasible.

*Proof.* REPAIR only sets entries to 0, so $y \le x$. If $x$ is feasible, it removes nothing. Otherwise it goes on removing items while the weight exceeds $C$; if it removed every packed item, the weight would be $0 \le C$. So it stops at a feasible vector. $\square$

**Lemma 2 (improve).** If $x$ is feasible, IMPROVE returns a maximal $z$ with $z \ge x$ in each position.

*Proof.* IMPROVE packs an item only when it fits, so the weight stays at most $C$, and it never unpacks, so $z \ge x$. Take an item $i$ with $z_i = 0$. When IMPROVE looked at $i$, it did not fit: the load $L$ at that time had $L + w_i > C$. The load only grows after that, so $w(z) + w_i \ge L + w_i > C$. So $z$ is maximal. $\square$

**Lemma 3 (the reference set).** At all times, $R$ is a set of distinct maximal solutions, and its size does not change after line L2.

*Proof.* Line L1 builds each solution by REPAIR and then IMPROVE, so each is maximal by Lemmas 1 and 2, and it drops copies. Line L2 takes distinct members of this pool. Each child added to $N$ at line L7 is IMPROVE(REPAIR($\cdot$)), so it is maximal. Line L9 replaces one member by a child $z \notin R$, so the members stay distinct and the size stays the same. $\square$

**Lemma 4 (progress).** Each replacement at line L9 raises $\sum_{x \in R} v(x)$ by at least 1 and does not lower $\max_{x \in R} v(x)$.

*Proof.* A replacement removes the worst member $r$ and adds $z$ with $v(z) > v(r)$. The values are integers, so the sum rises by $v(z) - v(r) \ge 1$. If $r$ was not the only member of largest value, the maximum is unchanged or rises to $v(z)$. If $r$ was the only member of largest value, it was also the worst, so all members other than $r$ have smaller values, which is possible only if $|R| = 1$; then the new maximum is $v(z) > v(r)$. $\square$

**Theorem (correctness and termination).** Scatter search stops. It returns a maximal, so feasible, solution of largest value in the final reference set, and the largest value in $R$ never decreases during the run.

*Proof.* The sum $\sum_{x \in R} v(x)$ is at most $|R| \sum_i v_i$. By Lemma 4 every round that does not stop at line L10 raises it by at least 1, since such a round makes at least one replacement. So there are at most $|R| \sum_i v_i$ such rounds, and each round is finite: it looks at fewer than $|R|^2$ pairs. Line L11 returns a member of $R$ of largest value, which is maximal by Lemma 3. The last claim is Lemma 4. $\blacksquare$

**What is not claimed.** The result need not be an optimal packing. Maximal is a weak property: no single item can be added, but a swap of items can still give more value. Scatter search has no guarantee of optimality, and the bound on the number of rounds above is not polynomial in the input size, since it depends on the values.
