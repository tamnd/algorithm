---
title: Hermite reduction returns g and a squarefree remainder with A/D = g' + a/d
proves: [correctness, termination]
status: full
---

Let $K$ be a field of characteristic 0 and $D \in K[x]$ nonzero, with squarefree factorization $D = c \prod_{i=1}^{m} D_i^{\,i}$, where $c \in K$, the $D_i$ are monic, squarefree and pairwise coprime, and $D_m \ne 1$. All gcds are monic.

**Lemma 1.** For a polynomial $E = c \prod_i E_i^{\,i}$ of this form, $\gcd(E, E') = \prod_i E_i^{\,i-1}$, and $E / \gcd(E, E')$ is $c \prod_i E_i$, a squarefree polynomial.

*Proof.* Let $p$ be a monic irreducible factor of $E_i$, so $p$ divides $E$ exactly $i$ times. Write $E = p^i u$ with $p \nmid u$. Then $E' = p^{i-1}(i p' u + p u')$. Since $\deg p' < \deg p$ and $p' \ne 0$ in characteristic 0, and $p \nmid u$, $p$ does not divide $i p' u$, so it does not divide $i p' u + p u'$. Hence $p$ divides $E'$ exactly $i - 1$ times, and $\gcd(E, E')$ contains $p$ exactly $i - 1$ times. Irreducible factors of $E'$ that do not divide $E$ do not enter the gcd. $\square$

Write $D^-_k$ for the value of $D^-$ at the start of pass $k$ of the loop, $k = 1, 2, \ldots$. By Lemma 1, $D^-_1 = \prod_i D_i^{\,i-1}$ and $D^* = c \prod_i D_i$, and by induction, applying Lemma 1 to $D^-_k$ in line L4,

$$D^-_k = \prod_{i \ge k} D_i^{\,i - k}, \qquad D^{-*}_k = \prod_{i > k} D_i, \qquad D^{--}_k = D^-_{k+1}.$$

**Lemma 2 (line L5 is solvable).** Let $F_k = -D^* D_k^{-\prime} / D^-_k$. Then $F_k$ is a polynomial and $\gcd(F_k, D^{-*}_k) = 1$. Hence there are unique $B, C$ with $B F_k + C D^{-*}_k = A$ and $\deg B < \deg D^{-*}_k$.

*Proof.* From the formula for $D^-_k$, logarithmic differentiation gives $D_k^{-\prime} / D^-_k = \sum_{i > k} (i - k) D_i' / D_i$. Multiplying by $D^* = c \prod_j D_j$ gives $F_k = -c \sum_{i > k} (i - k) D_i' \prod_{j \ne i} D_j$, a polynomial. Let $p$ be an irreducible factor of $D^{-*}_k$, so $p \mid D_l$ for one $l > k$. Every term of the sum with $i \ne l$ contains the factor $D_l$, so it is divisible by $p$. The term with $i = l$ is $(l - k) D_l' \prod_{j \ne l} D_j$. Here $l - k \ne 0$ in characteristic 0, $p \nmid D_l'$ because $D_l$ is squarefree, and $p \nmid D_j$ for $j \ne l$ because the $D_j$ are pairwise coprime. So $p \nmid F_k$. Therefore $F_k$ and $D^{-*}_k$ are coprime. The extended Euclidean algorithm gives $s, t$ with $s F_k + t D^{-*}_k = 1$; then $B = (s A) \bmod D^{-*}_k$ and $C = (A - B F_k)/D^{-*}_k$ satisfy the equation, the division being exact because $B F_k \equiv s F_k A \equiv A$ modulo $D^{-*}_k$. If $(B_1, C_1)$ is another solution with the degree bound, then $(B - B_1) F_k = (C_1 - C) D^{-*}_k$, so $D^{-*}_k \mid B - B_1$ by coprimality, and the degree bound gives $B = B_1$, hence $C = C_1$. $\square$

**Lemma 3 (one pass).** Suppose that before pass $k$, $A_{\text{in}}/D = g' + A / (D^* D^-_k)$ and $\deg A < \deg(D^* D^-_k)$. Then after the pass, $A_{\text{in}}/D = g' + A / (D^* D^-_{k+1})$ with the new values, and $\deg A < \deg(D^* D^-_{k+1})$.

*Proof.* Write $E = D^-_k$, $E^* = D^{-*}_k$ and $E^{-} = D^{-}_{k+1}$, so $E = E^* E^{-}$. By Lemma 2, $A = B F + C E^*$ with $F = -D^* E'/E$. Then

$$\frac{A}{D^* E} - \left(\frac{B}{E}\right)' = \frac{A}{D^* E} - \frac{B'}{E} + \frac{B E'}{E^2} = \frac{A - B' D^* + B D^* E'/E}{D^* E} = \frac{C E^* - B' D^*}{D^* E^* E^{-}} .$$

The term $B D^* E'/E = -B F$ cancels against the part $B F$ of $A$. Now $E^* \mid D^*$, since every $D_i$ with $i > k$ is a factor of $D^*$, so $D^*/E^*$ is a polynomial and the last fraction equals $\left(C - B' D^*/E^*\right) / (D^* E^{-})$. This is the new $A$ of line L6 over $D^* D^-_{k+1}$, and line L7 adds $B/E$ to $g$, so the identity holds after the pass.

For the degrees, let $N = \deg(D^* E)$. Then $\deg F = \deg D^* - 1$ and $\deg B < \deg E^*$, so $\deg(B F) < \deg E^* + \deg D^* - 1 \le N - 1$ because $\deg E^* \le \deg E$. With $\deg A < N$ this gives $\deg(C E^*) < N$, so $\deg C < N - \deg E^* = \deg(D^* E^{-})$. Also $\deg(B' D^*/E^*) < \deg E^* - 1 + \deg D^* - \deg E^* + 1 = \deg D^* \le \deg(D^* E^{-})$. So the new $A$ has degree less than $\deg(D^* D^-_{k+1})$. $\square$

**Theorem.** HERMITE-REDUCE$(A_{\text{in}}, D)$ terminates after $m - 1$ passes and returns $g$ and $a/d$ with $A_{\text{in}}/D = g' + a/d$, where $d = D^*$ is squarefree and $\deg a < \deg d$.

*Proof.* After line L1, $A_{\text{in}} = P D + A$ with $\deg A < \deg D$, and $g = \int P$, so $A_{\text{in}}/D = g' + A/D$. After line L2, $D = D^* D^-_1$, so the hypothesis of Lemma 3 holds for $k = 1$. By Lemma 3 and induction, it holds at the start of every pass. By the formula above, $D^-_k$ has degree 0 exactly when $k \ge m$, so the loop of line L3 runs for $k = 1, \ldots, m - 1$ and stops with $D^- = D^-_m = 1$, a monic polynomial of degree 0. Then the identity reads $A_{\text{in}}/D = g' + A/D^*$ with $\deg A < \deg D^*$, and $D^* = c \prod_i D_i$ is squarefree by Lemma 1. Line L9 returns this. $\blacksquare$
