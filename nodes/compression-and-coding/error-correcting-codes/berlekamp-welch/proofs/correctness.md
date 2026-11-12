---
title: The Berlekamp-Welch decoder returns the unique message within distance e
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $F$ be a field, $a_1, \ldots, a_n \in F$ distinct, $1 \le k \le n$, and $e = \lfloor (n-k)/2 \rfloor$, so $2e + k \le n$. A pair $(Q, E)$ is *admissible* if $E$ is monic of degree $e$, $\deg Q < e + k$, and $Q(a_i) = y_i E(a_i)$ for $1 \le i \le n$. Lines L2 and L3 find an admissible pair if one exists, since the conditions are exactly the linear system of line L2 in the coefficients $Q_0, \ldots, Q_{e+k-1}, E_0, \ldots, E_{e-1}$, and Gaussian elimination finds a solution of a linear system whenever one exists.

**Lemma 1 (existence).** If some $f$ with $\deg f < k$ satisfies $f(a_i) \ne y_i$ for at most $e$ indices, then an admissible pair exists.

*Proof.* Let $B = \{a_i : f(a_i) \ne y_i\}$ and $E^*(x) = x^{e - |B|} \prod_{b \in B}(x - b)$, which is monic of degree $e$. Let $Q^* = E^* f$, with $\deg Q^* \le e + k - 1$. If $a_i \in B$, then $E^*(a_i) = 0$ and $Q^*(a_i) = 0 = y_i E^*(a_i)$. Otherwise $f(a_i) = y_i$ and $Q^*(a_i) = E^*(a_i) f(a_i) = y_i E^*(a_i)$. $\square$

**Lemma 2 (all admissible pairs give the same quotient).** If $(Q, E)$ and $(Q', E')$ are admissible, then $Q E' = Q' E$.

*Proof.* For each $i$, $Q(a_i) E'(a_i) = y_i E(a_i) E'(a_i) = Q'(a_i) E(a_i)$. So $D = Q E' - Q' E$ vanishes at the $n$ distinct points $a_i$. Its degree is at most $(e + k - 1) + e = 2e + k - 1 < n$. A nonzero polynomial of degree less than $n$ has fewer than $n$ roots, so $D = 0$. $\square$

**Lemma 3 (soundness).** If line L5 passes, the returned $f$ satisfies $\deg f < k$ and $f(a_i) \ne y_i$ for at most $e$ indices.

*Proof.* Line L5 passes only if $Q = E f$. Since $\deg Q < e + k$ and $\deg E = e$, $\deg f < k$. If $E(a_i) \ne 0$, then $f(a_i) = Q(a_i)/E(a_i) = y_i$. The monic polynomial $E$ of degree $e$ is nonzero and has at most $e$ roots, so at most $e$ indices have $f(a_i) \ne y_i$. $\square$

**Theorem.** If a polynomial $f$ with $\deg f < k$ is within distance $e$ of $y$, it is unique and the algorithm returns it. Otherwise the algorithm returns FAIL.

*Proof.* Uniqueness: if $f$ and $g$ are both within distance $e$ of $y$, then $f(a_i) = g(a_i)$ for at least $n - 2e \ge k$ indices. Then $f - g$ has degree less than $k$ and at least $k$ roots, so $f = g$.

Suppose such an $f$ exists. By Lemma 1, the pair $(Q^*, E^*) = (E^* f, E^*)$ is admissible, so line L3 finds some admissible $(Q, E)$. By Lemma 2, $Q E^* = Q^* E = E^* f E$. Since $F[x]$ has no zero divisors and $E^* \ne 0$, $Q = E f$. So line L4 gives the quotient $f$ and the remainder 0, line L5 passes, and line L6 returns $f$.

Suppose no such $f$ exists. If line L3 finds no solution, the algorithm returns FAIL. If it finds one and line L5 passes, Lemma 3 gives a polynomial of degree less than $k$ within distance $e$ of $y$, a contradiction. So line L5 fails, and the algorithm returns FAIL.

**Termination.** Line L2 builds $n$ equations, Gaussian elimination on a finite system ends, and the division of line L4 ends after at most $k$ steps. $\blacksquare$
