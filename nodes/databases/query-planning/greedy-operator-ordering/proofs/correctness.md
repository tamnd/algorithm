---
title: Greedy operator ordering builds a valid join tree, without cross products on a connected query graph, and takes the smallest join in each step
proves: [correctness]
status: full
---

**Setting.** The query graph has the relations $R_0, \ldots, R_{n-1}$ with sizes $|R_i|$ and a selectivity $f_e$ on each edge $e$. For a set $S$ of relations, $|S| = \prod_{i \in S} |R_i| \cdot \prod_{e \subseteq S} f_e$ is the estimated size of the join of $S$. For two disjoint sets $A$ and $B$, $f(A, B)$ is the product of $f_e$ over the edges with one end in $A$ and the other in $B$, and $A$ and $B$ are *linked* if there is at least one such edge. A *candidate* in a step is a pair of current trees that are linked, or any pair of current trees if no pair is linked or if cross products are allowed. The cost of a plan is $C_{out}$, the sum of the sizes of its joins. GOO is a heuristic, so the statement to prove is what it builds, not that the result is optimal.

**Lemma 1 (invariant).** At the start of each iteration of line L2, the leaf sets of the trees in $T$ are disjoint and their union is all relations. For each tree $t$ with leaf set $S_t$, the stored size is $|S_t|$, and for two trees $s$ and $t$ the stored value between them is $f(S_s, S_t)$ if they are linked and empty if they are not.

*Proof.* Line L1 makes one tree per relation, with size $|R_i|$, and the stored values between trees are the selectivities of the edges. Suppose the invariant holds and line L3 picks trees $a$ and $b$. The edges inside $S_a \cup S_b$ are those inside $S_a$, those inside $S_b$, and those between them, so $|S_a \cup S_b| = |S_a| \cdot |S_b| \cdot f(S_a, S_b)$, where $f(S_a, S_b) = 1$ if they are not linked. This is the size that line L5 stores. For another tree $c$, the edges between $S_a \cup S_b$ and $S_c$ are those between $S_a$ and $S_c$ and those between $S_b$ and $S_c$, so $f(S_a \cup S_b, S_c) = f(S_a, S_c) \cdot f(S_b, S_c)$, and the two sets are linked exactly when $a$ or $b$ is linked to $c$. The code stores this value. Line L4 replaces $a$ and $b$ by their join, so the leaf sets still partition the relations. $\square$

**Lemma 2 (greedy choice).** In each step, the pair that line L3 picks has the smallest estimated join size among all candidates, and ties go to the pair with the smallest tree numbers.

*Proof.* Line L3 looks at every pair of current trees once, skips the pairs that are not candidates, and computes the size of each candidate as $|S_a| \cdot |S_b| \cdot f(S_a, S_b)$, which is $|S_a \cup S_b|$ by Lemma 1. It keeps a pair only if its size is strictly smaller than the best so far, and it looks at the pairs in increasing order of tree numbers. $\square$

**Lemma 3 (no cross products).** If the query graph is connected and cross products are not allowed, every join that GOO makes has an edge between its two inputs. Then the leaf set of every tree is connected in the query graph.

*Proof.* While $T$ has two or more trees, their leaf sets partition the relations into two or more parts (Lemma 1). The graph is connected, so some edge has its ends in two different parts, and the two trees are linked. So the candidates are the linked pairs, and the chosen pair is linked. A join of two connected leaf sets with an edge between them has a connected leaf set. $\square$

**Theorem.** GOO stops after $n - 1$ joins and returns a join tree whose leaves are $R_0, \ldots, R_{n-1}$, each once. Its returned cost is the $C_{out}$ cost of the tree. If the query graph is connected and cross products are not allowed, the tree has no cross product. Each join is a smallest candidate of its step.

*Proof.* Each iteration of line L2 reduces the number of trees by one, so after $n - 1$ iterations one tree is left, and by Lemma 1 its leaf set is all relations, with each relation in exactly one leaf. The code adds the size of each new join to the cost, and by Lemma 1 this size is $|S_a \cup S_b|$, the size of the join in the plan, so the sum is $C_{out}$. The other two claims are Lemmas 3 and 2. $\blacksquare$

**Small queries.** On a connected query graph with at most three relations, GOO returns an optimal plan without cross products. With one relation there is no join, and with two there is one plan. With three relations, every plan has two joins, and the second one has the size $|\{R_0, R_1, R_2\}|$, which is the same for all plans. The first join of a plan without cross products is a linked pair, and GOO takes a linked pair of smallest size, so no plan has a smaller cost.

**Not optimal in general.** Take the chain $A$-$B$-$C$-$D$ with sizes 20, 10, 1000 and 20 and selectivities 1/5, 1/100 and 1/100 on its edges. The joins of two relations have sizes $|AB| = 40$, $|BC| = 100$ and $|CD| = 200$, so GOO first joins $A$ and $B$. Then $|ABC| = 400$ and $|CD| = 200$, so it joins $C$ and $D$, and the last join has size 80. The total is $40 + 200 + 80 = 320$. The plan $A \bowtie ((B \bowtie C) \bowtie D)$ costs $100 + 20 + 80 = 200$. The step that looked best, the join of size 40, led to a step of size 200, while the join of size 100 led to a step of size 20.

**Work.** With $k$ trees, line L3 looks at fewer than $k^2/2$ pairs, each in $O(1)$ steps with the stored values, and the update after a join takes $O(k)$ steps. Summed over $k = n$ down to 2, this is $O(n^3)$. The stored values between trees take $O(n^2)$ space.
