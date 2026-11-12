---
title: The incremental algorithm returns exactly the d-splits and their isolation indices
proves: [correctness]
status: full
---

**Setting.** $d$ is a symmetric function on $X = \{x_1, \ldots, x_n\}$ with $d(x, x) = 0$. Write $X_k = \{x_1, \ldots, x_k\}$. For a split $A \mid B$ of a set $Y \subseteq X$, with $A, B$ nonempty, $A \cup B = Y$ and $A \cap B = \emptyset$, and for $a, a' \in A$ and $b, b' \in B$, let

$$\beta(a, a'; b, b') = \max\{d(a, b) + d(a', b'),\ d(a, b') + d(a', b),\ d(a, a') + d(b, b')\} - d(a, a') - d(b, b').$$

The isolation index on $Y$ is $\alpha_Y(A \mid B) = \frac{1}{2} \min \beta(a, a'; b, b')$ over all $a, a' \in A$ and $b, b' \in B$, where $a = a'$ and $b = b'$ are allowed. A *d-split* of $Y$ is a split with $\alpha_Y > 0$. We prove that after the step for $k$, the list `cur` holds exactly the d-splits of $X_k$, each with its index on $X_k$.

**Fact 1 (symmetry).** $\beta(a, a'; b, b') = \beta(a', a; b, b') = \beta(a, a'; b', b)$, and $\beta(a, a'; b, b') = \beta(b, b'; a, a')$.

*Proof.* Swapping $a$ and $a'$ exchanges the first two terms of the maximum and keeps the third term and the subtracted terms. The same holds for $b$ and $b'$. Exchanging the roles of the pairs keeps all three terms, because $d$ is symmetric. $\square$

**Lemma 1 (the terms with the new taxon).** Let $x \in A$. The value computed by `_with_new` with $x$ on the side $A$ is $\frac{1}{2} \min \beta(a, a'; b, b')$ over the terms with $a = x$ or $a' = x$. By Fact 1, the same holds with $x \in B$, after the roles of the sides are exchanged.

*Proof.* The function takes the minimum of $\beta(a, x; b, b')$ over all $a \in A$ and $b, b' \in B$. These are the terms with $a' = x$. A term with $a = x$ is $\beta(x, a'; b, b')$, which equals $\beta(a', x; b, b')$ by Fact 1, so it is in the list. $\square$

**Lemma 2 (restriction).** Let $Y' = Y \cup \{x\}$ with $x \notin Y$, and let $A \mid B$ be a split of $Y'$ with $x \in A$ and $A \ne \{x\}$. Put $A' = A \setminus \{x\}$. Then

$$\alpha_{Y'}(A \mid B) = \min\Big(\alpha_Y(A' \mid B),\ \tfrac{1}{2} \min_{a = x \text{ or } a' = x} \beta(a, a'; b, b')\Big).$$

In particular, $\alpha_{Y'}(A \mid B) \le \alpha_Y(A' \mid B)$, so if $A \mid B$ is a d-split of $Y'$, then $A' \mid B$ is a d-split of $Y$.

*Proof.* The terms of $\alpha_{Y'}(A \mid B)$ are indexed by $a, a' \in A$ and $b, b' \in B$. Those with $a, a' \in A'$ are exactly the terms of $\alpha_Y(A' \mid B)$, and the value of each term depends only on $d$ at its four points, so it is the same in both. The other terms have $a = x$ or $a' = x$. The minimum over a union is the minimum of the two minimums. $\square$

**Lemma 3 (the start).** On $X_2$, the only split is $x_1 \mid x_2$, and $\alpha_{X_2}(x_1 \mid x_2) = d(x_1, x_2)$.

*Proof.* There is one term, $a = a' = x_1$ and $b = b' = x_2$, and $\beta = \max\{2 d(x_1, x_2), 2 d(x_1, x_2), 0\} - 0 - 0$. Line L1 stores the split if this value is positive. $\square$

**Theorem.** For every $k \ge 2$, after the step for $k$ (or after line L1 for $k = 2$), `cur` holds each d-split of $X_k$ exactly once, with its index on $X_k$, and nothing else. So line L8 returns the d-splits of $X$ with their isolation indices.

*Proof.* Induction on $k$. Lemma 3 gives $k = 2$. Assume the claim for $X_{k-1}$, and let $x = x_k$. Line L4 forms these candidates:

1. the split $X_{k-1} \mid \{x\}$, whose index is $\frac{1}{2}$ times the minimum of the terms with $x$, because every term uses $x$ as $b$ or $b'$. By Lemma 1 with the sides exchanged, this is the value of `_with_new`;
2. for each pair $(A' \mid B, \alpha)$ in `cur`, the splits $A' \cup \{x\} \mid B$ and $A' \mid B \cup \{x\}$. For each, line L5 takes the minimum of the stored $\alpha = \alpha_{X_{k-1}}(A' \mid B)$, which is correct by induction, and the value of `_with_new` for the side that holds $x$. By Lemmas 1 and 2, this is the index on $X_k$.

So each candidate gets its exact index, and line L6 keeps it exactly when it is a d-split.

*Every d-split of $X_k$ is a candidate.* Let $A \mid B$ be a d-split of $X_k$ with $x \in A$, say. If $A = \{x\}$, it is candidate 1. Otherwise, by Lemma 2, $A \setminus \{x\} \mid B$ is a d-split of $X_{k-1}$, so by induction it is in `cur`, and $A \mid B$ is one of its two candidates.

*No split appears twice.* Different splits of $X_{k-1}$ give different candidates, because a candidate determines its restriction to $X_{k-1}$. Candidate 1 restricts to no split of $X_{k-1}$, so it differs from all others. And the two candidates of one split differ in the side of $x$. $\blacksquare$

**What the proof does not cover.** Bandelt and Dress (1992) proved that the d-splits form a weakly compatible system, that there are at most $\binom{n}{2}$ of them, and that $d - \sum_S \alpha_S \delta_S$ has no d-splits. The page uses these results for the complexity bound and for the residue. The tests check all three on random inputs against the definition.
