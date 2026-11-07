---
title: The subresultants give the Rothstein-Trager logarithms
proves: [correctness, termination]
status: full
---

Let $K$ be a field of characteristic $0$ with algebraic closure $\overline{K}$, and $A, D \in K[x]$ with $D$ square-free, $n = \deg D \ge 1$, $\deg A < n$ and $A \ne 0$. Let $\beta_1, \ldots, \beta_n \in \overline{K}$ be the roots of $D$, which are distinct, so $D'(\beta_k) \ne 0$. Write $B_t = A - t D'$, a polynomial in $x$ of formal degree $n - 1$ with coefficients in $K[t]$, and $r_k = A(\beta_k) / D'(\beta_k)$.

**Fact 1 (residues).** $\dfrac{A}{D} = \displaystyle\sum_{k=1}^{n} \frac{r_k}{x - \beta_k}$.

*Proof.* This is the [partial fraction decomposition](/partial-fraction-decomposition/) over $\overline{K}$ with simple poles. The coefficient of $1/(x - \beta_k)$ is the limit of $(x - \beta_k) A / D$ at $\beta_k$, which is $A(\beta_k) / D'(\beta_k)$ because $D'(\beta_k) = \lim (D(x) - D(\beta_k))/(x - \beta_k)$. $\square$

**Fact 2 (the resultant).** $R(t) = \operatorname{res}_x(D, B_t) = c \prod_{k=1}^{n} (t - r_k)$ with $c \in K^\times$.

*Proof.* For $D$ of degree $n$ and $B$ of formal degree $n - 1$, $\operatorname{res}(D, B) = \operatorname{lc}(D)^{n-1} \prod_k B(\beta_k)$. This is an identity of polynomials in the coefficients of $B$, so it holds for $B_t$ over $K[t]$. Here $B_t(\beta_k) = A(\beta_k) - t D'(\beta_k) = -D'(\beta_k)(t - r_k)$, so $c = \operatorname{lc}(D)^{n-1} \prod_k (-D'(\beta_k))$, which is nonzero, and $c \in K$ because $R \in K[t]$ has leading coefficient $c$. $\square$

For a root $\alpha$ of $R$ let $m(\alpha) = \#\{ k : r_k = \alpha \}$, its multiplicity by Fact 2, and $G_\alpha = \prod_{k : r_k = \alpha} (x - \beta_k)$.

**Fact 3.** $G_\alpha$ is the monic $\gcd(D, B_\alpha)$, of degree $m(\alpha)$.

*Proof.* $D$ is square-free, so its gcd with any polynomial is the product of $x - \beta_k$ over the common roots $\beta_k$. And $B_\alpha(\beta_k) = 0$ exactly when $A(\beta_k) = \alpha D'(\beta_k)$, that is $r_k = \alpha$. $\square$

**Fact 4 (Rothstein-Trager).** $\dfrac{d}{dx} \displaystyle\sum_{R(\alpha) = 0} \alpha \log G_\alpha = \frac{A}{D}$.

*Proof.* $\frac{d}{dx} \log G_\alpha = G_\alpha' / G_\alpha = \sum_{k : r_k = \alpha} 1/(x - \beta_k)$. Each $k$ belongs to exactly one $\alpha$, namely $r_k$, so the sum is $\sum_k r_k / (x - \beta_k) = A/D$ by Fact 1. $\square$

**Fact 5 (gcd property of subresultants).** Let $P, Q \in \overline{K}[x]$, $\deg P = p$, $Q$ of formal degree $q < p$, and let $S_j(P, Q)$ be the subresultants defined by determinants for these formal degrees, with $S_q = Q$. If $g = \gcd(P, Q)$ has degree $e \le q$, then $S_j(P, Q) = 0$ for $j < e$ and $S_e(P, Q)$ is a nonzero constant multiple of $g$. (Von zur Gathen and Gerhard, Chapter 6; Lazard and Rioboo state the case needed here.) Moreover, for a ring homomorphism $\varphi$ that keeps $\operatorname{lc}(P) \ne 0$, $\varphi(S_j(P, Q)) = S_j(\varphi P, \varphi Q)$ with the same formal degrees, because each $S_j$ is built from determinants whose entries are coefficients of $P$ and $Q$.

**Theorem.** Let $i \ge 1$ with $\deg Q_i > 0$, let $S_i$ be the polynomial of line L4 or L5, and let $\alpha$ be a root of $Q_i$. Then $\operatorname{lc}_x S_i(\alpha) \ne 0$, and $S_i(\alpha, x) = \operatorname{lc}_x S_i(\alpha) \cdot G_\alpha$.

*Proof.* By line L2, the roots of $Q_i$ are the roots of $R$ of multiplicity exactly $i$, so $m(\alpha) = i$, and $\deg G_\alpha = i$ by Fact 3.

If $i = n$, then $G_\alpha$ has degree $n$ and divides $D$, so $G_\alpha = D / \operatorname{lc}(D)$, and $S_n = D$ satisfies the claim.

If $i < n$, apply Fact 5 to $\varphi : t \mapsto \alpha$, which keeps $\operatorname{lc}(D)$, a nonzero element of $K$. So $S_i(\alpha, x) = S_i(D, B_\alpha)$, the subresultant for formal degrees $n$ and $n - 1$. Since $\gcd(D, B_\alpha) = G_\alpha$ has degree $i \le n - 1$, Fact 5 says $S_i(D, B_\alpha) = \lambda G_\alpha$ for some $\lambda \ne 0$. The polynomial $S_i$ has degree at most $i$ in $x$, so its coefficient of $x^i$ is $\operatorname{lc}_x S_i$, and comparing the coefficients of $x^i$ gives $\lambda = \operatorname{lc}_x S_i(\alpha) \ne 0$, since $G_\alpha$ is monic of degree $i$. $\blacksquare$

**Lines L6 to L8.** By the theorem, $\operatorname{lc}_x S_i$ does not vanish at any root of $Q_i$, so $\gcd(A_j, Q_i) = 1$ for every square-free factor $A_j$ of $\operatorname{lc}_x S_i$, and line L7 divides by $1$. Since $Q_i$ is square-free and $\operatorname{lc}_x S_i$ has no common root with it, $\operatorname{lc}_x S_i$ is invertible modulo $Q_i$. Reducing the coefficients modulo $Q_i$ and multiplying by this inverse does not change the values at roots of $Q_i$ except for dividing by $\operatorname{lc}_x S_i(\alpha)$. So after line L8, $S_i(\alpha, x) = G_\alpha$ for every root $\alpha$ of $Q_i$.

**Correctness of the output.** The roots of $R$ are partitioned by multiplicity among the $Q_i$, which are square-free and pairwise coprime. So the sum of line L9 is $\sum_{R(\alpha) = 0} \alpha \log G_\alpha$, and its derivative is $A/D$ by Fact 4.

**Termination.** The subresultants are finitely many determinants or a finite pseudo-remainder sequence, the square-free factorizations and gcds are Euclidean computations in $K[t]$, and the loop of line L3 has at most $n$ passes. $\blacksquare$
