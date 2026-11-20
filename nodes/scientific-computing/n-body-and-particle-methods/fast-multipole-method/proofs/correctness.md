---
title: The FMM counts each pair once, its translations are exact or bounded, and its error is controlled by p
proves: [correctness]
status: full
---

We use exact complex arithmetic. The charges $q_i$ sit at $z_i$ in the unit square. The tree is uniform: level $l$ has the $4^l$ boxes of side $w_l = 2^{-l}$, and the leaves are at level $L \ge 2$. Two boxes of one level are *near neighbours* if their closed squares share at least one point; a box is its own near neighbour. The *interaction list* of a box $b$ at level $l \ge 2$ is the set of children of the near neighbours of the parent of $b$ that are not near neighbours of $b$. For a box $b$ at level $l$, $b_k$ is its ancestor at level $k \le l$. The potential is $u(z) = \sum_i q_i \log|z - z_i|$, the real part of $\phi(z) = \sum_i q_i \log(z - z_i)$.

**Lemma 1 (each pair is counted once).** Let $t$ and $c$ be two leaves. If $t$ and $c$ are near neighbours, no level $l \in \{2, \ldots, L\}$ has $c_l$ in the interaction list of $t_l$. Otherwise exactly one level $l \in \{2, \ldots, L\}$ has $c_l$ in the interaction list of $t_l$.

*Proof.* If $c_k$ and $t_k$ are not near neighbours, then $c_{k+1}$ and $t_{k+1}$ are not near neighbours, because they lie inside $c_k$ and $t_k$, and a shared point of the children would be a shared point of the parents. So the set of levels $k$ at which $c_k$ and $t_k$ are near neighbours is an initial segment $\{0, 1, \ldots, k^*\}$. It contains 0 and 1, because the root is one box and the four boxes of level 1 share the center point. By the definition, $c_l$ is in the interaction list of $t_l$ exactly when $c_{l-1}$ and $t_{l-1}$ are near neighbours and $c_l$ and $t_l$ are not, that is, exactly when $l = k^* + 1$. If $t$ and $c$ are near neighbours, $k^* = L$ and no such $l \le L$ exists. Otherwise $k^* \in \{1, \ldots, L - 1\}$ and $l = k^* + 1$ is the only level. $\square$

So, for a target in leaf $t$, every charge is used exactly once: in the near field of line L6 if its leaf is a near neighbour of $t$, and otherwise through the one box $c_l$ that line L3 converts into the local expansion of $t_l$.

**Lemma 2 (the multipole shift is exact).** Let $a_0, \ldots, a_p$ be the multipole coefficients of a set of charges about $z_0$, that is $a_0 = \sum q_i$ and $a_k = -\sum q_i (z_i - z_0)^k / k$. Then the coefficients $b_0, \ldots, b_p$ of line L2 (Lemma 4.6 of Beatson and Greengard) are the multipole coefficients of the same charges about $0$.

*Proof.* Write $\zeta_i = z_i - z_0$. The multipole coefficient of order $l \ge 1$ about $0$ is $-\sum_i q_i (\zeta_i + z_0)^l / l$. By the binomial theorem this is $-\sum_i q_i \left( z_0^l + \sum_{k=1}^{l} \binom{l}{k} \zeta_i^k z_0^{l-k} \right) / l$. The first term gives $-a_0 z_0^l / l$. For the second, $\binom{l}{k} / l = \binom{l-1}{k-1} / k$, so it gives $\sum_{k=1}^{l} \binom{l-1}{k-1} z_0^{l-k} \left( -\sum_i q_i \zeta_i^k / k \right) = \sum_{k=1}^{l} a_k z_0^{l-k} \binom{l-1}{k-1}$. The coefficient of order 0 is $\sum q_i = a_0$ for both centers. Only $a_0, \ldots, a_l$ appear in $b_l$, so the truncation at $p$ loses nothing. $\square$

By Lemma 2 and induction from the leaves up, after line L2 each box holds the exact $p$-term multipole coefficients of the charges inside it.

**Lemma 3 (the local shift is exact).** The Horner loop of line L4 (Lemma 4.8) maps the coefficients of a polynomial $\sum_{k=0}^{p} b_k (w - z_0)^k$ to the coefficients of the same polynomial in powers of $w$.

*Proof.* Each pass of the outer loop is one step of synthetic division by $w - z_0$ in the variable $w - z_0$, so after $p$ passes the coefficients are those of the Taylor expansion of the same polynomial about the new center (the triangle of the passes is the scheme of Horner for a shift of origin). A polynomial of degree $p$ is its own Taylor polynomial of degree $p$, so nothing is lost. $\square$

**Lemma 4 (one M2L step).** Let a box $c$ at level $l$ be in the interaction list of $t$, with side $w = w_l$. The charges of $c$ lie in the disk of radius $R = w / \sqrt{2}$ about its center, and the distance of the two centers is at least $2w = 2\sqrt{2}\, R$. Let $\gamma = 2\sqrt{2} - 1 \approx 1.83$. Then for each $z$ in the disk of radius $R$ about the center $z_t$ of $t$, which contains the closed square of $t$ and of all its descendants, the $p$-term local expansion produced at line L3 from the $p$-term multipole expansion of $c$ satisfies

$$\left| \phi_c(z) - \sum_{l'=0}^{p} b_{l'} (z - z_t)^{l'} \right| \le A_c \, \frac{4e(p + \gamma)(\gamma + 1) + \gamma^2}{\gamma (\gamma - 1)} \left(\frac{1}{\gamma}\right)^{p+1},$$

where $\phi_c$ is the complex potential of the charges of $c$ and $A_c = \sum_{i \in c} |q_i|$.

*Proof.* Two boxes of one level that are not near neighbours have centers at least two sides apart in one coordinate. Move $z_t$ to the origin. For each $\gamma'$ with $1 < \gamma' < \gamma$ the distance of the centers is $2w > (\gamma' + 1) R$, so Lemma 4.7 of Beatson and Greengard (their $c$ is our $\gamma'$) gives the bound with $\gamma'$ in place of $\gamma$, as a strict inequality. The right side is continuous in $\gamma'$, so the bound with $\gamma$ follows as $\gamma' \to \gamma$. The real part of the left side is the error of the potential $u$, and it is at most the modulus. $\square$

**Theorem.** Let $u_j$ be the output of line L7 for the charge $j$ in leaf $t$. Then

$$|u_j - u(z_j)| \le \left( \sum_{i} |q_i| \right) \frac{4e(p + \gamma)(\gamma + 1) + \gamma^2}{\gamma (\gamma - 1)} \left(\frac{1}{\gamma}\right)^{p+1},$$

where $u(z_j)$ is the exact potential without the self term. The bound tends to $0$ as $p \to \infty$, so the FMM converges to direct summation.

*Proof.* By Lemma 1 the far charges for $t$ are split into the disjoint boxes $c_l$ of the interaction lists of the ancestors $t_l$, $2 \le l \le L$, and the near charges are summed exactly at line L6, without $i = j$. By Lemma 2 each box holds its exact multipole coefficients. Line L3 makes a local expansion for each pair, with the error of Lemma 4. Line L4 moves these expansions down without error by Lemma 3, and line L5 evaluates the sum at $z_j$, which lies in the disk of radius $w_l / \sqrt{2}$ about the center of each ancestor $t_l$. The errors add, and $\sum_c A_c \le \sum_i |q_i|$ because the boxes are disjoint. $\square$

The same argument with the derivatives gives the convergence of the field. The bound is a worst case; the measured error falls faster, by about a factor of 2.5 for each extra term in the example on the page. The cost bound of the page is a separate statement and needs a bounded number of charges per leaf.
