---
title: Correctness of the Padé approximation algorithm
proves: [correctness, termination]
status: full
---

Notation: $f(x) = \sum_{k \ge 0} c_k x^k$ is a formal power series, $c_k = 0$ for $k < 0$, and $m, n \ge 0$. Write $[g]_k$ for the coefficient of $x^k$ in a series $g$. The algorithm PADE builds $A = (c_{m+i-j})_{i,j=1}^{n}$ and $b = (-c_{m+i})_{i=1}^{n}$, solves $A q' = b$ for $q' = (q_1, \ldots, q_n)$, sets $q_0 = 1$ and $p_k = \sum_{j=0}^{\min(k,n)} q_j c_{k-j}$ for $0 \le k \le m$.

**Lemma 1 (coefficients of $fq$).** For a polynomial $q = \sum_{j=0}^{n} q_j x^j$ and every $k \ge 0$, $[fq]_k = \sum_{j=0}^{\min(k,n)} q_j c_{k-j}$.

*Proof.* The Cauchy product of $\sum c_i x^i$ and $\sum_{j \le n} q_j x^j$ has $x^k$ coefficient $\sum_{i + j = k} c_i q_j$, with $0 \le j \le n$ and $i = k - j \ge 0$. $\square$

**Lemma 2 (the system is the order condition).** Let $q$ have $q_0 = 1$ and $\deg q \le n$, and let $p$ have $\deg p \le m$. Then $fq - p = O(x^{m+n+1})$ if and only if (a) $\sum_{j=1}^{n} c_{m+i-j} q_j = -c_{m+i}$ for $i = 1, \ldots, n$, and (b) $p_k = [fq]_k$ for $k = 0, \ldots, m$.

*Proof.* $fq - p = O(x^{m+n+1})$ means $[fq - p]_k = 0$ for $0 \le k \le m + n$. For $k \le m$ this is $p_k = [fq]_k$, which is (b). For $k = m + i$ with $1 \le i \le n$, $p$ has no term of degree $k$, so the condition is $[fq]_{m+i} = 0$. By Lemma 1 this is $\sum_{j=0}^{n} q_j c_{m+i-j} = 0$ (terms with $j > m + i$ vanish since $c$ with negative index is 0), and moving the $j = 0$ term, with $q_0 = 1$, to the right gives (a). $\square$

**Lemma 3 (uniqueness of the rational function, Frobenius).** If $(p, q)$ and $(\tilde p, \tilde q)$ have $\deg p, \deg \tilde p \le m$, $\deg q, \deg \tilde q \le n$, $q, \tilde q \ne 0$, and both satisfy $fq - p = O(x^{m+n+1})$, $f\tilde q - \tilde p = O(x^{m+n+1})$, then $p \tilde q = \tilde p q$, so $p/q = \tilde p/\tilde q$ as rational functions.

*Proof.* $p\tilde q - \tilde p q = (fq - p)\tilde q - (f\tilde q - \tilde p) q$. Both terms on the right are $O(x^{m+n+1})$, so the polynomial on the left has no terms of degree at most $m + n$. Its degree is at most $m + n$. Hence it is the zero polynomial. $\square$

**Theorem (correctness).** If $A$ is nonsingular, PADE returns $(p, q)$ with $q_0 = 1$, $\deg p \le m$, $\deg q \le n$ and $fq - p = O(x^{m+n+1})$; this $q$ is the only such denominator with $q_0 = 1$, and $p/q$ is the $[m/n]$ Padé approximant. If $f$ equals a rational function $P/Q$ of type $(m, n)$ with $Q(0) \ne 0$, then $p/q = P/Q$.

*Proof.* Line L3 returns the unique $q'$ with $Aq' = b$, which is condition (a) of Lemma 2, and line L5 enforces (b) by Lemma 1. Lemma 2 gives the order condition. Any other $\tilde q$ with $\tilde q_0 = 1$ and a matching $\tilde p$ must satisfy (a), hence $\tilde q = q$ since $A$ is nonsingular, and then $\tilde p = p$ by (b). For the last claim, scale so that $Q(0) = 1$; then $fQ - P = 0$, so $(P, Q)$ satisfies the order condition, and by Lemma 3, $p Q = P q$, that is $p/q = P/Q$. $\square$

**When $A$ is singular.** The homogeneous system for $(q_0, \ldots, q_n)$ has $n$ equations in $n + 1$ unknowns, so it has a nonzero solution, and Lemma 3 shows that all solutions define the same rational function. A solution with $q_0 = 1$ exists only if $b$ lies in the range of $A$; when it does not, the $[m/n]$ approximant in the sense $q(0) = 1$ does not exist. The implementation does not choose between these cases: it reports the singular matrix (a block of the Padé table) and returns nothing. This is a deliberate restriction, not a gap in the argument above.

**Termination.** Lines L1, L2 and L4 do a fixed number of assignments; Gaussian elimination on an $n \times n$ system finishes after $n$ pivot steps, each with finitely many operations, and either produces the solution or finds a zero pivot column and stops; line L5 is a double loop with at most $(m + 1)(n + 1)$ terms. No step loops or recurses. $\square$
