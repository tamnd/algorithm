---
title: The Horowitz-Ostrogradsky system has exactly one solution
proves: [correctness, termination]
status: full
---

Let $K$ be a field of characteristic $0$ and $A, D \in K[x]$ with $D \ne 0$, $d = \deg D \ge 1$ and $\deg A < d$. Write $D = c \prod_{i=1}^{r} p_i^{e_i}$ with $c \in K^\times$, distinct monic irreducible $p_i$ and $e_i \ge 1$.

**Fact 1.** $\gcd(D, D') = \prod_i p_i^{e_i - 1}$. Hence $D^- = \prod_i p_i^{e_i - 1}$ and $D^* = D / D^- = c \prod_i p_i$, which is square-free.

*Proof.* Fix $i$ and write $D = p_i^{e_i} R$ with $p_i \nmid R$. Then $D' = p_i^{e_i - 1} (e_i p_i' R + p_i R')$, so $p_i^{e_i - 1} \mid D'$. The factor $e_i p_i' R$ is not divisible by $p_i$: $e_i \ne 0$ in characteristic $0$; $p_i' \ne 0$ has degree less than $\deg p_i$, so $p_i \nmid p_i'$; and $p_i \nmid R$. Since $p_i$ is prime, $p_i \nmid e_i p_i' R + p_i R'$, so $p_i^{e_i} \nmid D'$. As every irreducible factor of $\gcd(D, D')$ divides $D$, the gcd is $\prod_i p_i^{e_i - 1}$. $\square$

**Fact 2.** $E = D^* (D^-)' / D^-$ is a polynomial of degree less than $m = \deg D^*$.

*Proof.* By the product rule, $(D^-)' = \sum_i (e_i - 1) p_i^{e_i - 2} p_i' \prod_{j \ne i} p_j^{e_j - 1}$, where terms with $e_i = 1$ vanish. Multiplying the $i$-th term by $D^* = c \prod_j p_j$ gives $c (e_i - 1) p_i' \prod_{j \ne i} p_j \cdot p_i^{e_i - 1} \prod_{j \ne i} p_j^{e_j - 1}$, a multiple of $D^-$. So $D^- \mid D^* (D^-)'$. If $(D^-)' \ne 0$, $\deg E = m + (n - 1) - n = m - 1$, where $n = \deg D^-$. $\square$

**Fact 3.** Let $P, Q \in K[x]$ with $Q \ne 0$, $\gcd(P, Q) = 1$, and let $p$ be irreducible with $p^k \| Q$, $k \ge 1$. Then in lowest terms the denominator of $(P/Q)'$ is divisible by $p^{k+1}$.

*Proof.* $(P/Q)' = (P' Q - P Q') / Q^2$. Write $Q = p^k R$ with $p \nmid R$. Then $P'Q - PQ' = p^{k-1} N$ with $N = P' p R - P (k p' R + p R')$, and $N \equiv -k P p' R \pmod p$. Here $p \nmid P$ because $\gcd(P, Q) = 1$, and $p \nmid k p' R$ as in Fact 1. So $p \nmid N$, and $p^{k-1} \| P'Q - PQ'$, while $p^{2k} \| Q^2$. After cancelling, $p^{2k - (k-1)} = p^{k+1}$ remains in the denominator. $\square$

**Lemma (equivalence).** For $B, C \in K[x]$, $\dfrac{A}{D} = \left(\dfrac{B}{D^-}\right)' + \dfrac{C}{D^*}$ holds if and only if $A = B' D^* - B E + C D^-$.

*Proof.* Multiply by $D = D^- D^*$: $D \cdot (B / D^-)' = D^- D^* (B' D^- - B (D^-)') / (D^-)^2 = B' D^* - B E$, and $D \cdot C / D^* = C D^-$. Multiplication by $D \ne 0$ is invertible in $K(x)$. $\square$

**Theorem.** The linear map $\Phi(B, C) = B' D^* - B E + C D^-$ from $V = \{ (B, C) : \deg B < n, \deg C < m \}$ to $W = \{ P : \deg P < d \}$ is a bijection. Hence the system of line L5 has exactly one solution.

*Proof.* $\Phi$ maps into $W$: $\deg(B' D^*) \le (n - 2) + m$, $\deg(BE) \le (n - 1) + (m - 1)$ by Fact 2, and $\deg(C D^-) \le (m - 1) + n$, all less than $d = n + m$. Both $V$ and $W$ have dimension $d$ over $K$. So it suffices to show $\Phi$ is injective.

Suppose $\Phi(B, C) = 0$. By the lemma with $A = 0$, $(B / D^-)' = -C / D^*$. Write $B / D^- = P / Q$ in lowest terms with $Q$ monic. If $\deg Q \ge 1$, pick an irreducible $p$ with $p^k \| Q$, $k \ge 1$. By Fact 3, $p^{k+1}$, and so $p^2$, divides the reduced denominator of $(P/Q)'$. But the reduced denominator of $-C / D^*$ divides $D^*$, which is square-free by Fact 1, so $p^2$ does not divide it. This is a contradiction, so $Q = 1$ and $B / D^-$ is a polynomial. Since $\deg B < \deg D^-$, this forces $B = 0$. Then $C D^- = 0$, so $C = 0$. $\blacksquare$

**Correctness of the algorithm.** Lines L1 and L2 compute $D^-$ and $D^*$ (Fact 1). Line L5 writes the identity of the lemma coefficient by coefficient for $x^0, \ldots, x^{d-1}$, which is the equation $\Phi(B, C) = A$ in $W$, because $A \in W$. By the theorem the matrix is nonsingular, so Gaussian elimination at line L6 finds a pivot in every column and returns the unique solution. By the lemma, the returned $B$ and $C$ satisfy the output specification, and $D^*$ is square-free by Fact 1.

**Termination.** The Euclidean algorithm, the exact division and Gaussian elimination on a $d \times d$ system each perform finitely many steps. $\blacksquare$
