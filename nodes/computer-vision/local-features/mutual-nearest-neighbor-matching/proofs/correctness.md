---
title: Properties of mutual nearest neighbor matching
proves: [correctness]
status: full
---

Let $A = (a_0, \dots, a_{m-1})$ and $B = (b_0, \dots, b_{n-1})$ be lists of vectors with $m, n \ge 1$, and let $d(i, j) = \lVert a_i - b_j \rVert$. Let $f(i)$ be the smallest index $j$ that minimizes $d(i, j)$, and $g(j)$ the smallest index $i$ that minimizes $d(i, j)$. The output is $M = \{ (i, f(i)) : g(f(i)) = i \}$.

**Lemma 1 (the scan).** `nearest(a, B)` returns the smallest index of a nearest vector.

*Proof.* The scan keeps the smallest value seen so far and replaces it only on a strictly smaller value, so the first index that reaches the minimum is kept. $\square$

**Lemma 2 (a matching).** Each $i$ and each $j$ is in at most one pair of $M$.

*Proof.* Row $i$ is listed only with $f(i)$. If $(i, j)$ and $(i', j)$ are in $M$, then $i = g(j) = i'$. $\square$

**Lemma 3 (the definition).** $(i, j) \in M$ if and only if $d(i, j)$ is the first smallest value of row $i$ and the first smallest value of column $j$, where "first" means the smallest index among equal values.

*Proof.* This is the definition of $f$ and $g$: $j = f(i)$ is the first condition and $i = g(j)$ the second. $\square$

**Lemma 4 (symmetry).** Matching $B$ against $A$ gives $\{(j, i) : (i, j) \in M\}$.

*Proof.* Swapping the lists swaps the roles of $f$ and $g$, and the condition of Lemma 3 is symmetric in rows and columns. $\square$

**Lemma 5 (the closest pair is kept).** Let $\delta = \min_{i, j} d(i, j)$, let $i^*$ be the smallest row that contains the value $\delta$, and let $j^* = f(i^*)$. Then $(i^*, j^*) \in M$. In particular $M$ is not empty.

*Proof.* $d(i^*, j^*) = \delta$ because row $i^*$ contains $\delta$, which is the global minimum. Column $j^*$ has minimum $\delta$, and every row $i$ with $d(i, j^*) = \delta$ has $i \ge i^*$ by the choice of $i^*$. So $g(j^*) = i^*$. $\square$

**Lemma 6 (inside the greedy matching).** Suppose all values $d(i, j)$ are distinct. The greedy matching takes pairs in increasing order of $d$ and keeps a pair when neither end is used. Then $M$ is a subset of the greedy matching.

*Proof.* Take $(i, j) \in M$. By Lemma 3 every other pair in row $i$ or column $j$ has a larger value. So when the greedy method reaches $(i, j)$, it has taken only pairs with smaller values, none of which uses $i$ or $j$. Both ends are free, and it keeps $(i, j)$. $\square$

**Theorem.** `mutual_nn_match` returns the pairs of Lemma 3 in increasing order of $i$. They form a partial matching that contains the closest pair, does not depend on which list is called $A$, and, for distinct distances, is a subset of the greedy matching.

*Proof.* Lines L1 and L2 compute $f$ and $g$ by Lemma 1, and lines L3 and L4 keep exactly the pairs with $g(f(i)) = i$. Lemmas 2 to 6 give the properties. $\blacksquare$
