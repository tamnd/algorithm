---
title: Correctness of orthogonal matching pursuit
proves: [correctness]
status: full
---

We prove that OMP always returns the least squares fit on its support, that it never picks a column twice while the residual is nonzero, and that it recovers every $s$-sparse vector exactly when the columns have norm $1$ and the mutual coherence satisfies $\mu < 1/(2s - 1)$.

## Setup

Let $A \in \mathbb R^{m \times n}$ have columns $a_1, \ldots, a_n$. For a list $S$ of indices, $A_S$ is the matrix of those columns. Write $S_k$ for the list after $k$ passes of the loop, $x^{(k)}$ for the fit of line L5 and $r_k = y - A_{S_k} x^{(k)}_{S_k}$ for the residual of line L6, with $r_0 = y$.

## Lemma 1 (orthogonal residual)

For every $k \ge 1$ and every $j \in S_k$, $\langle a_j, r_k \rangle = 0$.

*Proof.* Line L5 minimizes $\|A_{S_k} z - y\|_2^2$. A minimizer satisfies the normal equations $A_{S_k}^{\mathsf T}(A_{S_k} z - y) = 0$, so $A_{S_k}^{\mathsf T} r_k = 0$, whose entries are the inner products $\langle a_j, r_k \rangle$ for $j \in S_k$. $\square$

**Consequence.** On line L3, every chosen column scores $0$. So whenever some column has a positive score, the chosen index is new. Line L3 also skips chosen indices, so $S_k$ always has $k$ distinct entries.

## Lemma 2 (monotone residual)

$\|r_{k+1}\|_2 \le \|r_k\|_2$ for every $k$.

*Proof.* $S_k$ is a sublist of $S_{k+1}$, so the vector $x^{(k)}$, padded with a zero for the new index, is feasible for the least squares problem of step $k + 1$, with residual $r_k$. The minimum is at most this value. $\square$

## Lemma 3 (the residual stays in the span of the true support)

Let $y = A x_0$ and $T = \operatorname{supp}(x_0)$. If $S_k \subseteq T$ (as sets), then $r_k \in \operatorname{span}\{a_i : i \in T\}$.

*Proof.* $y = A_T x_{0,T}$ lies in this span, and $A_{S_k} x^{(k)}_{S_k}$ lies in the span of a subset of the same columns. Their difference $r_k$ lies in the span too. $\square$

## Lemma 4 (a correct pick)

Let the columns have norm $1$, $\mu = \max_{i \ne j} |\langle a_i, a_j \rangle|$, $|T| \le s$ and $(2s - 1)\mu < 1$. Let $r = A_T c$ with $c \ne 0$. Then

$$\max_{i \in T} |\langle a_i, r \rangle| > \max_{i \notin T} |\langle a_i, r \rangle|.$$

*Proof.* Let $k \in T$ with $|c_k| = \|c\|_\infty > 0$. Then

$$|\langle a_k, r \rangle| = \Big| c_k + \sum_{j \in T, j \ne k} c_j \langle a_k, a_j \rangle \Big| \ge |c_k| - (|T| - 1)\mu \|c\|_\infty \ge \big(1 - (s - 1)\mu\big)\|c\|_\infty.$$

For $i \notin T$, every term of $\langle a_i, r \rangle = \sum_{j \in T} c_j \langle a_i, a_j \rangle$ has size at most $\mu\|c\|_\infty$, so $|\langle a_i, r \rangle| \le s\mu\|c\|_\infty$. Finally, $1 - (s - 1)\mu > s\mu$ is the same as $(2s - 1)\mu < 1$, and $\|c\|_\infty > 0$, so the first bound is strictly larger. $\square$

## Lemma 5 (independent columns)

Under the conditions of Lemma 4, the columns $a_i$ for $i \in T$ are linearly independent.

*Proof.* The Gram matrix $G = A_T^{\mathsf T} A_T$ has ones on the diagonal and off-diagonal entries of size at most $\mu$. By the Gershgorin disc theorem each eigenvalue $\lambda$ satisfies $|\lambda - 1| \le (|T| - 1)\mu \le (s - 1)\mu < 1$, so $\lambda > 0$ and $G$ is nonsingular. $\square$

## Theorem (exact recovery)

Let the columns of $A$ have norm $1$, $(2s - 1)\mu < 1$, $x_0$ be $s$-sparse with support $T$, $y = Ax_0$, and $\tau = 0$. Then OMP stops after exactly $|T|$ passes, with $S$ equal to $T$ as a set and $x = x_0$.

*Proof.* We show by induction on $k$, for $0 \le k \le |T|$, that $S_k$ is a list of $k$ distinct elements of $T$.

For $k = 0$ the list is empty. Let $k < |T|$ and $S_k \subseteq T$ with $k$ distinct elements. First, $r_k \ne 0$. If $r_k = 0$, let $z$ be $x^{(k)}$ on $S_k$ and $0$ elsewhere. Then $A_T z_T = y = A_T x_{0,T}$, and by Lemma 5, $z = x_0$. But $z$ has at most $k < |T|$ nonzero entries, and $x_0$ has $|T|$, a contradiction. So the loop runs again, since $\|r_k\|^2 > 0 = \tau$. By Lemma 3, $r_k = A_T c$, and $c \ne 0$ since $r_k \ne 0$. By Lemma 4, the largest score on line L3 is reached only inside $T$. By Lemma 1, the indices in $S_k$ score $0$, while the best score is positive, so the chosen index is in $T$ and not in $S_k$. This proves the step.

After $|T|$ passes, $S$ holds all of $T$. The fit on line L5 is the least squares solution on $A_T$, which is unique by Lemma 5, and $x_{0,T}$ gives residual $0$, so $x = x_0$ and $r = 0$. The loop then stops because $\|r\|^2 = 0 \le \tau$, or because $s$ passes are done when $|T| = s$. Line L7 returns $x_0$. $\square$

## Remark (the exact recovery condition)

The proof uses the coherence only through Lemma 4. Tropp (2004) shows that Lemma 4 holds for every residual in the span of $A_T$ exactly when $\max_{i \notin T} \|A_T^{+} a_i\|_1 < 1$, where $A_T^{+}$ is the pseudoinverse, and that the same condition also makes basis pursuit succeed for vectors supported on $T$. The examples on the page show that without such a condition, either method can succeed where the other fails.
