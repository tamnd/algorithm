---
title: Correctness of the quasi-polynomial discrete logarithm algorithm (toy version)
proves: [correctness, termination]
status: full
---

We prove the version of the main pseudocode. Let $q$ be an odd prime power, $h_0, h_1 \in \mathbb{F}_{q^2}[X]$ with $\gcd(h_0, h_1) = 1$ and $h_1 = c_h \prod_\beta (X + \beta)^{f_\beta}$ a product of linear factors, and $I$ a monic irreducible factor of degree $k \ge 2$ of $h_1 X^q - h_0$. Let $K = \mathbb{F}_{q^2}[X]/(I)$, a field with $Q = q^{2k}$ elements, and $G = K^*$, cyclic of order $N = Q - 1$. Let $g \in G$ have order $r$ and let $h \in G$. Let $\gamma$ be the generator of line L3 and $L(z) \in \mathbb{Z}/N\mathbb{Z}$ the logarithm of $z \in G$ to base $\gamma$. Let $\ell = \prod \rho^e$ over the prime powers $\rho^e \parallel N$ with $\rho \mid r$; then $r \mid \ell \mid N$. For termination we treat the exponents $m$ of lines L9 and L13 as independent and uniform in $[0, N - 1]$.

**Lemma 1 (membership and the trivial target).** Line L1 returns NONE exactly when $h \notin \langle g \rangle$, and line L2 is correct.

*Proof.* $G$ is cyclic, so its only subgroup of order $r$ is $\{z : z^r = 1\}$, which is $\langle g \rangle$. If $h = 1$, then $x = 0$. $\square$

From now on $h = g^{x^*}$ with $0 \le x^* < r$, unique because $g$ has order $r$, and $h \ne 1$, so $r \ge 2$.

**Lemma 2 (the systematic congruence).** Let $a, b, c, d \in \mathbb{F}_{q^2}$ with $ad - bc \ne 0$, $Y = aX + b$ and $Z = cX + d$. Then $Z$ and every $Y - \alpha Z$ with $\alpha \in \mathbb{F}_q$ are nonzero polynomials of degree at most $1$, a polynomial of degree $0$ among them is a nonzero constant, and in $K$

$$h_1 \cdot Z \prod_{\alpha \in \mathbb{F}_q} (Y - \alpha Z) = R_m, \qquad R_m = (a^q h_0 + b^q h_1) Z - Y (c^q h_0 + d^q h_1),$$

where both sides are nonzero.

*Proof.* In any commutative ring of characteristic $p$ containing $\mathbb{F}_q$, $T^q - T = \prod_{\alpha \in \mathbb{F}_q} (T - \alpha)$ holds in $\mathbb{F}_q[T]$, since both sides are monic of degree $q$ and vanish at the $q$ elements of $\mathbb{F}_q$. Homogenizing gives $Y^q Z - Y Z^q = Z \prod_\alpha (Y - \alpha Z)$ in $\mathbb{F}_q[Y, Z]$: for $Z = 1$ this is the identity above, both sides are homogeneous of degree $q + 1$, and both have the coefficient $0$ at $Y^{q+1}$. Substitute $Y = aX + b$ and $Z = cX + d$. Since the characteristic divides $q$, $(aX + b)^q = a^q X^q + b^q$, and in $K$ we have $h_1 X^q = h_0$ because $I$ divides $h_1 X^q - h_0$. So $h_1 Y^q = a^q h_0 + b^q h_1$ and $h_1 Z^q = c^q h_0 + d^q h_1$ in $K$, and multiplying the identity by $h_1$ gives the congruence. If $Y - \alpha Z = 0$ as a polynomial, then $(a, b) = \alpha (c, d)$ and $ad - bc = 0$; if $Z = 0$, then $c = d = 0$. Both are excluded, so all factors are nonzero, and a factor of degree $0$ is a nonzero constant. A nonzero polynomial of degree at most $1 < k$ is a nonzero element of $K$. Also $h_1 \ne 0$ in $K$: otherwise $I \mid h_1$, then $I \mid h_0 = h_1 X^q - (h_1 X^q - h_0)$, against $\gcd(h_0, h_1) = 1$. So the left side is a product of nonzero elements of the field $K$, and it is nonzero; hence so is $R_m$. $\square$

The matrices of line L5 have $ad - bc \ne 0$: for $(1, b, 0, \delta)$ with $\delta \ne 0$ the determinant is $\delta$, and for $(1, s + t, i, s i + t i^q)$ with $t \ne 0$ and $i \notin \mathbb{F}_q$ it is $t (i^q - i) \ne 0$.

**Lemma 3 (relations).** Every row $(e ; v)$ of $R$ satisfies $\sum_\beta e_\beta L(X + \beta) \equiv v \pmod{\ell}$. For every key $Q$ of $E$ with $E[Q] = (e ; v)$, $Q$ is a nonzero element of $K$ and $L(Q) \equiv \sum_\beta e_\beta L(X + \beta) - v \pmod{\ell}$.

*Proof.* The constants: $\omega = \gamma^{N/(q^2-1)}$ has order $q^2 - 1$ and lies in $\mathbb{F}_{q^2}^*$, the only subgroup of $G$ of that order, so it generates $\mathbb{F}_{q^2}^*$ and $L(\omega^j) = j N / (q^2 - 1)$; the table of the implementation holds these values modulo $\ell$. Write each factor $f$ of degree $1$ in Lemma 2 as $f = u (X + w/u)$ with $u \ne 0$, so $L(f) = L(u) + L(X + w/u)$, and each constant factor $w$ has $L(w)$. Taking $L$ of the congruence of Lemma 2 gives, modulo $N$,

$$L(c_h) + \sum_\beta f_\beta L(X + \beta) + \sum_{f} L(f) = L(R_m).$$

For a row of line L7, $R_m = c_0 \prod (X + \beta)^{e_\beta}$ as polynomials, so $L(R_m) = L(c_0) + \sum e_\beta L(X + \beta)$. Moving the constants to the right gives the row of line L7, which holds modulo $N$ and so modulo $\ell$. For line L8, $R_m = c_0 \, Q \prod (X + \beta)^{e_\beta}$ with $Q$ monic, irreducible and of degree $2$. Since $R_m \ne 0$ in $K$, its factor $Q$ is nonzero in $K$, and $L(R_m) = L(c_0) + L(Q) + \sum e_\beta L(X + \beta)$. With $(e ; v)$ built as in line L7 from the other factors, this reads $L(Q) = \sum e_\beta L(X + \beta) - v$. A row of line L10 comes from $\gamma^m = c \prod (X + \beta)^{a_\beta}$, so $m = L(c) + \sum a_\beta L(X + \beta)$. $\square$

**Lemma 4 (SOLVE).** Let $M = \rho^e$ with $\rho$ prime and $M \mid N$. If SOLVE$(R, \rho, M)$ returns a vector $\lambda$, then $\lambda_\beta \equiv L(X + \beta) \pmod{M}$ for every $\beta$.

*Proof.* By Lemma 3 the true vector modulo $M$ satisfies every row, because $M \mid \ell$. Lines L18 and L19 swap two rows, multiply a row by a unit modulo $M$ (an entry not divisible by $\rho$ is coprime to $M$), or subtract a multiple of one row from another. Each operation is invertible, so the solution set modulo $M$ does not change, and the true vector stays a solution. After column $j$ is processed, row $j$ has $1$ in column $j$ and every other row has $0$ there, and later steps keep this. At the end row $j$ reads $\lambda_j \equiv$ its right side, so the returned value is the true one. $\square$

**Lemma 5 (scale).** After line L11, $\lambda_\beta \equiv L(X + \beta) \pmod{\ell}$ for every $\beta$.

*Proof.* Line L11 is passed only when every SOLVE succeeded, so Lemma 4 applies to every $\rho^e \parallel \ell$. The moduli are pairwise coprime, and the Chinese remainder theorem gives a unique residue modulo $\ell$ with these reductions. $\square$

**Lemma 6 (individual logarithms).** For $y \in \{g, h\}$, the value of line L15 is $L(y) \bmod \ell$.

*Proof.* Line L14 is passed only when $z = y \gamma^m \bmod I$ equals $c \prod (X + \beta)^{d_\beta} \prod Q_i^{u_i}$ as a polynomial and every $Q_i$ is a key of $E$. Then, modulo $N$, $L(y) + m = L(c) + \sum d_\beta L(X + \beta) + \sum u_i L(Q_i)$. Reducing modulo $\ell$, and replacing $L(X + \beta)$ by $\lambda_\beta$ (Lemma 5) and $L(Q_i)$ by $e_i \cdot \lambda - k_i$ (Lemmas 3 and 5), gives line L15. $\square$

**Lemma 7 (conversion).** With $c = \ell / r$, the residue $L(g) \bmod \ell$ is $c u$ for an integer $u$ coprime to $r$, the residue $L(h) \bmod \ell$ is divisible by $c$, and $(L(h)/c) \, u^{-1} \equiv x^* \pmod r$.

*Proof.* Since $g$ has order $r$ and $\gamma$ has order $N$, $\gcd(L(g), N) = N / r$. For each prime $\rho \mid r$ with $\rho^a \parallel r$ and $\rho^e \parallel N$, the $\rho$-adic valuation of $L(g)$, taken in $[0, N - 1]$, is exactly $e - a$, which is the valuation of $c$ at $\rho$, and $c$ has no other prime factors. Reducing modulo $\ell$ does not change a valuation below $e$, so $L(g) \bmod \ell = c u$ with $u$ coprime to $r$. Next, $h = g^{x^*}$ gives $L(h) \equiv x^* c u \pmod{\ell}$, so $L(h)/c \equiv x^* u \pmod r$, and multiplying by $u^{-1}$ gives $x^*$. $\square$

**Correctness.** By Lemmas 6 and 7, line L17 returns $x^*$. With Lemma 1, the algorithm returns $x^*$ if $h \in \langle g \rangle$ and NONE otherwise.

**Termination.** Lines L5 to L8 run over a finite list. In the loop of lines L9 to L11, for each $\beta$ the draw $m = L(X + \beta)$, which has probability $1/N$ in each trial, gives $z = X + \beta$ and the row with $1$ in column $\beta$, $0$ elsewhere, and right side $m$. With probability $1$ every column eventually has such a unit row. Once these rows are present, every SOLVE succeeds: the unit row of column $j$ has $0$ in every earlier column, so it is never chosen as a pivot for an earlier column and the clearing steps never change it, since they change only rows with a nonzero entry in the pivot column; a swap at column $j' < j$ moves it only to a position at least $j'$, so it is still available at column $j$, where its entry $1$ is a unit pivot. The implementation tries SOLVE each time the number of rows reaches a threshold that grows by a fixed amount after each failure, and rows keep being added, so it tries SOLVE infinitely often and the first try after all unit rows are present succeeds. In the loop of lines L13 and L14, the draw $m = (N - L(y)) \bmod N$ gives $z = 1$, which splits with no $Q_i$, so each loop ends with probability $1$. Hence the algorithm stops with probability $1$. $\blacksquare$
