---
title: Kraft's hierarchical basis is linearly independent, contains each level on its domain, and gives nested spaces
proves: [correctness]
status: full
---

We use the representation of the page. Level $\ell$ has the tensor B-splines $\beta = N^\ell_i(x) N^\ell_j(y)$ of degree $p$ on the knot vector of level $\ell$, and its cells are the squares of side $2^{-\ell}$. The *support cells* of $\beta$ are the cells of level $\ell$ on which $\beta$ is not identically zero; they form a rectangle, and $\beta > 0$ in the interior of each of them. The domains satisfy $\Omega^0 = [0, n_0]^2$, $\Omega^{\ell} \subseteq \Omega^{\ell-1}$, each $\Omega^\ell$ is a union of cells of level $\ell - 1$, and $\Omega^L = \emptyset$. "$\beta \subseteq \Omega$" means that all support cells of $\beta$ lie in $\Omega$. $H$ is the output of lines L1 to L4, $H^\ell$ its functions of level $\ell$, and $S(H)$ their span.

**Lemma 1 (local linear independence).** For a cell $Q$ of level $\ell$, the B-splines of level $\ell$ that are not zero on $Q$ are linearly independent as functions on $Q$.

*Proof.* In one direction, the $p + 1$ B-splines of degree $p$ that are nonzero on a knot interval span the polynomials of degree at most $p$ there, a space of dimension $p + 1$, by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/) restricted to one interval; so they are independent on it. The tensor products of two independent families on two intervals are independent on the rectangle: if $\sum_{ij} c_{ij} N_i(x) N_j(y) = 0$, then for each $y$ the coefficients $\sum_j c_{ij} N_j(y)$ vanish, and then each $c_{ij} = 0$. $\square$

**Lemma 2 (two-scale relation).** Each $\beta$ of level $\ell < L - 1$ is $\sum_\gamma c_\gamma \gamma$ over B-splines $\gamma$ of level $\ell + 1$ with $c_\gamma \ge 0$, and every $\gamma$ with $c_\gamma \ne 0$ has its support inside the support of $\beta$.

*Proof.* Work in one direction; the tensor product of the two directions then gives the claim. The knots of level $\ell + 1$ contain those of level $\ell$, so inserting the new knots one at a time by [Boehm's rule](/boehm-knot-insertion/) writes $N^\ell_i$ in the B-splines of level $\ell + 1$. Each new coefficient is $\alpha c_k + (1 - \alpha) c_{k-1}$ with $0 \le \alpha \le 1$, and the start vector is a unit vector, so all coefficients are nonnegative. The support $[a, b]$ of $N^\ell_i$ runs between two knots of level $\ell$, which are knots of level $\ell + 1$, so $[a, b]$ is a union of fine knot intervals. A fine B-spline $\gamma$ whose support is not inside $[a, b]$ is nonzero on some fine interval $I$ outside $[a, b]$. On $I$ the sum $\sum c_\gamma \gamma$ equals $N^\ell_i = 0$, and the fine B-splines that are nonzero on $I$ are independent there by Lemma 1, so $c_\gamma = 0$. $\square$

**Lemma 3 (each level on its domain).** Every B-spline $\beta$ of level $\ell$ with $\beta \subseteq \Omega^\ell$ lies in $S(H)$.

*Proof.* By downward induction on $\ell$. If $\beta \not\subseteq \Omega^{\ell+1}$, line L3 selects $\beta$. This always happens for $\ell = L - 1$, since $\Omega^L$ is empty. Otherwise $\beta \subseteq \Omega^{\ell+1}$ and $\ell + 1 \le L - 1$. By Lemma 2, $\beta = \sum c_\gamma \gamma$ with each $\gamma$ of level $\ell + 1$ and support inside that of $\beta$, so $\gamma \subseteq \Omega^{\ell+1}$, and by induction $\gamma \in S(H)$. So $\beta \in S(H)$. $\square$

**Theorem 1 (linear independence).** The functions of $H$ are linearly independent.

*Proof.* Let $\sum_{(\ell, \beta) \in H} c_\beta \beta = 0$. We show by induction on $k$ that $c_\beta = 0$ for every $\beta \in H^k$. Assume it for the levels below $k$, so $\sum_{\ell \ge k} \sum_{\beta \in H^\ell} c_\beta \beta = 0$. Let $\beta \in H^k$. Since $\beta \not\subseteq \Omega^{k+1}$, it has a support cell $Q$ of level $k$ that is not in $\Omega^{k+1}$. Since $\Omega^{k+1}$ is a union of cells of level $k$, the interior of $Q$ does not meet $\Omega^{k+1}$. Every function of a level $\ell > k$ in $H$ lies in $\Omega^\ell \subseteq \Omega^{k+1}$, so it is zero on the interior of $Q$. Hence $\sum_{\beta' \in H^k} c_{\beta'} \beta' = 0$ on $Q$. By Lemma 1 every $\beta'$ of level $k$ that is not zero on $Q$ has $c_{\beta'} = 0$, and $\beta$ is one of them. $\square$

**Theorem 2 (the space).** $S(H)$ contains every tensor product spline of level 0 and every B-spline of level $\ell$ whose support lies in $\Omega^\ell$. In particular the constant 1 lies in $S(H)$.

*Proof.* Every level 0 B-spline lies in $\Omega^0$, so Lemma 3 applies to it and to the other levels. The constant is the sum of the level 0 B-splines, by the [partition of unity](/partition-of-unity/) of B-splines on an open knot vector. $\square$

**Theorem 3 (nested spaces).** Let $\hat\Omega^\ell \supseteq \Omega^\ell$ for every $\ell$, both sequences with the properties above, and let $\hat H$ be the selection for $\hat\Omega$. Then $S(H) \subseteq S(\hat H)$. So REFINE never loses a function of the old space.

*Proof.* Each $(\ell, \beta) \in H$ has $\beta \subseteq \Omega^\ell \subseteq \hat\Omega^\ell$, so $\beta \in S(\hat H)$ by Lemma 3 for $\hat H$. $\square$

**Correctness of the operations.** Lines L1 to L4 test exactly the rule of Theorem 1 for each tensor B-spline of each level. Lines L5 to L8 sum the given coefficients times the values of the selected B-splines, computed by the Cox-de Boor recursion on the knot vector of their level. REFINE keeps $\Omega^\ell \subseteq \Omega^{\ell-1}$ and the alignment to cells of level $\ell - 1$, so the hypotheses above hold after every call. The tests check Theorem 1, the containment of Lemma 3 and Theorem 3 by exact ranks of the expansions in the finest level. $\blacksquare$
