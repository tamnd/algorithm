---
title: Feldman and Pedersen VSS accept honest shares, fix one secret, and Pedersen's view is independent of the secret
proves: [correctness]
status: full
---

Let $p = 2q + 1$ with $p, q$ prime, and let $G = \langle g \rangle$ be the subgroup of $\mathbb{Z}_p^*$ of order $q$, with $h \in G$, $h \ne 1$. All exponents are mod $q$. The dealer's polynomials are $f(X) = \sum_{j<t} a_j X^j$ with $a_0 = s$, and for Pedersen $r(X) = \sum_{j<t} b_j X^j$. Line numbers refer to the pseudocode on the page.

**Lemma 1 (completeness).** If the dealer follows lines L1 to L3, every share passes line L4.

*Proof.* For Feldman, $\prod_j C_j^{i^j} = \prod_j g^{a_j i^j} = g^{\sum_j a_j i^j} = g^{f(i)} = g^{s_i}$, since $g$ has order $q$ and exponents can be reduced mod $q$. For Pedersen, in the same way $\prod_j (g^{a_j} h^{b_j})^{i^j} = g^{f(i)} h^{r(i)} = g^{s_i} h^{r_i}$. $\square$

**Lemma 2 (Feldman: one secret is fixed).** Let $C_0, \ldots, C_{t-1} \in G$ be any broadcast, and write $C_j = g^{c_j}$ (each element of $G$ is a power of $g$, even if nobody can compute $c_j$). Let $F(X) = \sum_j c_j X^j$. A value $x$ passes line L4 for party $i$ if and only if $x = F(i)$. So any $t$ shares that pass L4 lie on $F$, and line L6 returns $F(0)$, the same value for every set of $t$ accepted shares.

*Proof.* Line L4 checks $g^x = \prod_j g^{c_j i^j} = g^{F(i)}$. As $g$ has prime order $q$, $g^x = g^y$ if and only if $x \equiv y \pmod q$. So exactly $x = F(i)$ passes. Any $t$ such shares are $t$ points of $F$, which has degree less than $t$, and by the correctness of Shamir's scheme (uniqueness of interpolation) line L6 returns $F(0)$. If the dealer is honest, $F = f$ and $F(0) = s$. $\square$

**Lemma 3 (Pedersen: binding).** Suppose two different pairs $(x, y) \ne (x', y')$ both pass line L4 for the same party $i$. Then $\log_g h = (x - x') / (y' - y) \bmod q$.

*Proof.* Both pairs satisfy $g^x h^y = \prod_j C_j^{i^j} = g^{x'} h^{y'}$, so $g^{x - x'} = h^{y' - y}$. If $y = y'$ then $g^{x - x'} = 1$ and $x = x'$, a contradiction. So $y' - y$ is invertible mod $q$, and $h = g^{(x - x')/(y' - y)}$. $\square$

**Corollary 5 (Pedersen: one secret is fixed, computationally).** Let $A$ be a set of $t$ parties whose pairs $(x_i, y_i)$ pass line L4, and let $\lambda_i$ be the Lagrange coefficients at 0 for $A$. Since $\sum_{i \in A} \lambda_i i^j$ is 1 for $j = 0$ and 0 for $1 \le j < t$,
$$\prod_{i \in A} (g^{x_i} h^{y_i})^{\lambda_i} = \prod_{i \in A} \prod_j C_j^{\lambda_i i^j} = \prod_j C_j^{\sum_i \lambda_i i^j} = C_0.$$
So $(X_A, Y_A) = (\sum_i \lambda_i x_i, \sum_i \lambda_i y_i)$ is an opening of $C_0$, and $X_A$ is the value that line L6 returns for $A$. If two sets $A$ and $A'$ gave different values $X_A \ne X_{A'}$, then $g^{X_A} h^{Y_A} = C_0 = g^{X_{A'}} h^{Y_{A'}}$ with $X_A \ne X_{A'}$, and the computation of Lemma 3 gives $\log_g h$. So a dealer, together with the dishonest parties, that makes two sets of honest parties reconstruct different secrets computes $\log_g h$.

**Lemma 4 (Pedersen: perfect secrecy).** Let $B$ be a set of $t - 1$ parties. For each secret $s$, the view $(C_0, \ldots, C_{t-1}, (s_i, r_i)_{i \in B})$ has the same distribution.

*Proof.* Write $h = g^w$ with $w \ne 0$ (unknown to the parties, but fixed). Then $C_j = g^{a_j + w b_j}$. Define $e_j = a_j + w b_j$ and $E(X) = \sum_j e_j X^j = f(X) + w\, r(X)$. The view is determined by $(e_0, \ldots, e_{t-1})$ and $(f(i), r(i))_{i \in B}$. Since $f(i) = E(i) - w\, r(i)$, it is equally determined by $E$ and $(r(i))_{i \in B}$. Now count. The dealer's randomness is $(a_1, \ldots, a_{t-1}, b_0, \ldots, b_{t-1})$, uniform in $\mathbb{Z}_q^{2t-1}$. For fixed $s$, the map to $(e_0, \ldots, e_{t-1}, (r(i))_{i \in B})$, an element of $\mathbb{Z}_q^{2t-1}$, is affine. It is a bijection: given the target, $(r(i))_{i \in B}$ and $b_0 = (e_0 - s)/w$ fix $r$ by interpolation on the $t$ points $\{0\} \cup B$, and then $a_j = e_j - w b_j$ for $j \ge 1$. So the image is uniform in $\mathbb{Z}_q^{2t-1}$ for every $s$, and the view has the same distribution for every secret. $\square$

**Remark (Feldman is not perfectly hiding).** In Feldman's scheme $C_0 = g^s$ is a function of $s$, different for each $s \in \mathbb{Z}_q$. So the view determines $s$ information-theoretically, and secrecy holds only in the sense that computing $s$ from $g^s$ (and $t - 1$ shares, which are uniform and independent of $s$ by the secrecy of Shamir's scheme) is as hard as the discrete logarithm problem. $\blacksquare$
