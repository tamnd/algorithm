---
title: Correctness of graph cut stereo with expansion moves
proves: [correctness]
status: full
---

We use the notation of the page. An assignment $a = (p, d)$ pairs left pixel $p = (u, v)$ with right pixel $q = (u - d, v)$. A configuration is a set $A$ of active assignments, and

$$E(A) = \sum_{a \in A} D(a) + K \cdot \#\{\text{pixels of both images covered by no } a \in A\} + \sum_{\{a_1, a_2\} \in \mathcal{N}} V_{a_1 a_2} [\,|\{a_1, a_2\} \cap A| = 1\,] + \infty \cdot [\text{a pixel is covered twice}],$$

with all costs $D(a), K, V_{a_1 a_2} \ge 0$. $A$ is unique if no pixel is covered twice; only unique configurations have finite energy. We prove that each expansion move returns the configuration of least energy in its move space, that the algorithm stops, and that it returns a unique configuration that no expansion move improves.

## The move space and its variables

Fix a unique $A$ and a disparity $\alpha$. Let $A^0 = \{a \in A : d(a) \ne \alpha\}$ and let $A^\alpha$ be the set of all assignments of disparity $\alpha$. The $\alpha$-expansions of $A$ are the sets $A' = A'_0 \cup A'_\alpha$ with $A'_0 \subseteq A^0$ and $A'_\alpha \subseteq A^\alpha$: old assignments can only be dropped, and assignments of disparity $\alpha$ can be switched on or off freely. $A$ itself is one of them.

Give each $a \in A^0$ a variable $x_a$, with $x_a = 0$ meaning $a \in A'$, and each $a \in A^\alpha$ a variable $x_a$, with $x_a = 1$ meaning $a \in A'$. This is a bijection between $\{0, 1\}^{A^0 \cup A^\alpha}$ and the move space. Write $A'(x)$ for the configuration of $x$, and $x^0$ for the vector of $A$ itself.

## The binary energy

Build $B(x)$ as the sum of the following terms.

1. **Data.** For $a \in A^0$, the unary term $D(a)$ at $x_a = 0$; for $a \in A^\alpha$, $D(a)$ at $x_a = 1$.
2. **Pixels.** Each pixel $s$ of either image is covered in $A'(x)$ only by the assignment of $A^0$ that covers it in $A$ (at most one, since $A$ is unique), call it $a_0$, or by the one assignment of disparity $\alpha$ that contains it, call it $a_\alpha$, if that assignment lies inside the image. Two assignments of disparity $\alpha$ never share a pixel, because the left pixel and $\alpha$ fix the right pixel and the other way round. Every other assignment that contains $s$ is not in $A'(x)$. So:
   - if both $a_0$ and $a_\alpha$ exist, add the pair term $\theta(x_{a_0}, x_{a_\alpha})$ with $\theta(0,0) = 0$, $\theta(0,1) = \beta$, $\theta(1,0) = K$ and $\theta(1,1) = 0$. Here $(0, 1)$ means both cover $s$, and $(1, 0)$ means neither does. $\beta$ is a number larger than $E(A)$, used in place of $\infty$;
   - if only $a_0$ exists, add $K$ at $x_{a_0} = 1$; if only $a_\alpha$ exists, add $K$ at $x_{a_\alpha} = 0$; if neither exists, add the constant $K$.
3. **Smoothness.** A neighbor pair $\{a_1, a_2\}$ has one disparity $d$. If $d = \alpha$, both are variables with the same meaning of $x$, so add $V [x_{a_1} \ne x_{a_2}]$. If $d \ne \alpha$ and both are in $A^0$, the same term works, because both use $x = 0$ for active. If exactly one, say $a_1$, is in $A^0$, then $a_2 \notin A$ has $d \ne \alpha$ and stays inactive, so add $V$ at $x_{a_1} = 0$. If neither is in $A^0$, both stay inactive and the term is 0.

**Claim 1.** If $A'(x)$ is unique, $B(x) = E(A'(x))$. If not, $B(x) \ge \beta > E(A)$.

*Proof.* The data, occlusion and smoothness parts of $E(A'(x))$ are split above by assignment, by pixel and by neighbor pair, and each part is written as a term of $B$ that takes the same value for every $x$, except for the value $\beta$ in item 2. A pixel is covered twice in $A'(x)$ only if it is covered by both $a_0$ and $a_\alpha$: two assignments of $A^0$ cannot share a pixel because $A$ is unique, and two of disparity $\alpha$ cannot either. That is exactly the case $(x_{a_0}, x_{a_\alpha}) = (0, 1)$ of item 2, which adds $\beta$, while all other terms are nonnegative. If $A'(x)$ is unique, that case never happens and all terms equal those of $E$. $\square$

**Claim 2.** Every pair term of $B$ is regular: $\theta(0,0) + \theta(1,1) \le \theta(0,1) + \theta(1,0)$.

*Proof.* Item 2 gives $0 + 0 \le \beta + K$, and item 3 gives $0 + 0 \le V + V$. $\square$

## Each move is optimal

By Claim 2 and the Kolmogorov-Zabih construction (see [graph-representable energies](/graph-representable-energies/)), one minimum cut on a graph with a node per variable gives a minimizer $x^*$ of $B$. By Claim 1, $B(x^*) \le B(x^0) = E(A) < \beta$, so $A'(x^*)$ is unique, and for every unique $A'(x)$ we have $E(A'(x^*)) = B(x^*) \le B(x) = E(A'(x))$. Non-unique configurations have infinite energy. So $A'(x^*)$ has the least energy in the move space, and $E(A'(x^*)) \le E(A)$.

## Termination and the final state

The algorithm starts from $A = \emptyset$, which is unique, and replaces $A$ only by a move result of strictly lower energy, which is unique by the last section. There are finitely many configurations and the energy drops strictly at each change, so no configuration repeats and the loop stops. With integer costs it stops after at most $E(\emptyset) = 2 K W H$ changes. It stops after a cycle over all $\alpha$ in which no move lowered the energy. In that cycle $A$ did not change, and each move returned the best configuration in its move space, which contains $A$; so no $\alpha$-expansion of the final $A$ has lower energy, for any $\alpha$. $\square$

## What is not claimed

The result is a local minimum for expansion moves, not a global minimum. The factor $2c$ of [alpha-expansion](/alpha-expansion/) is proved for energies with one label per site and a metric pairwise term; this energy has binary variables per assignment and a uniqueness constraint, so that bound does not apply to it as stated.
