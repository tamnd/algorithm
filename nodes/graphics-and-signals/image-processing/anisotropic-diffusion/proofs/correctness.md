---
title: For λ ≤ 1/4 and 0 ≤ g ≤ 1 each explicit Perona-Malik step obeys the discrete maximum principle, and with the reflecting border it conserves the sum of all values
proves: [correctness]
status: full
---

Let $D$ be the pixels of an image with $W \ge 1$ columns and $H \ge 1$ rows, and for $p \in D$ let $N_4(p)$ be the set of the at most four pixels of $D$ at distance 1 from $p$. Then $q \in N_4(p)$ if and only if $p \in N_4(q)$. Let $g \ge 0$ be the conductance, and write $c(p, q) = g(|I(q) - I(p)|)$, which equals $c(q, p)$ because $|I(q) - I(p)| = |I(p) - I(q)|$. One step of lines L2 to L7 maps $I$ to

$$J(p) = I(p) + \lambda \sum_{q \in N_4(p)} c(p, q)\,(I(q) - I(p)),$$

because line L3 starts the flux at 0, lines L4 to L6 add $c(p, q)(I(q) - I(p))$ for each $q \in N_4(p)$, and line L7 reads only the old image $I$.

**Lemma 1 (convex combination).** If $0 < \lambda \le 1/4$ and $0 \le g \le 1$, then for every $p$,

$$J(p) = \Big(1 - \lambda \sum_{q \in N_4(p)} c(p, q)\Big) I(p) + \sum_{q \in N_4(p)} \lambda\, c(p, q)\, I(q),$$

with nonnegative coefficients that sum to 1.

*Proof.* The formula is the update with the terms regrouped. The coefficients of the neighbors are $\lambda c(p, q) \ge 0$. The coefficient of $I(p)$ is at least $1 - \lambda \cdot 4 \cdot 1 \ge 0$, because $|N_4(p)| \le 4$, $c \le 1$ and $\lambda \le 1/4$. The sum of all coefficients is $1 - \lambda \sum_q c(p, q) + \lambda \sum_q c(p, q) = 1$. $\square$

**Theorem 1 (discrete maximum principle).** Under the conditions of Lemma 1, $\min_D I \le J(p) \le \max_D I$ for every $p$, and so, by induction over the steps of line L1, every image the algorithm produces has its values in $[\min_D I_0, \max_D I_0]$ for the input $I_0$.

*Proof.* By Lemma 1, $J(p)$ is a convex combination of values of $I$, and a convex combination lies between the least and the largest of the values it combines, which lie in $[\min_D I, \max_D I]$. Line L8 makes $J$ the current image, so the next step starts from an image whose values lie in this interval, and the same argument applies; the interval never grows. $\square$

**Theorem 2 (mass conservation).** For every $\lambda$ and every $g$, $\sum_{p \in D} J(p) = \sum_{p \in D} I(p)$. So the sum of all values is the same after every step.

*Proof.* Summing the update over $p$,

$$\sum_p J(p) = \sum_p I(p) + \lambda \sum_{p \in D} \sum_{q \in N_4(p)} c(p, q)\,(I(q) - I(p)).$$

The double sum runs over the ordered pairs $(p, q)$ of neighbors in $D$. Since the neighbor relation is symmetric, these pairs split into the two orders $(p, q)$ and $(q, p)$ of each unordered pair, whose terms are $c(p, q)(I(q) - I(p))$ and $c(q, p)(I(p) - I(q)) = -c(p, q)(I(q) - I(p))$. Each pair contributes 0, so the double sum is 0. No term involves a pixel outside $D$, which is the reflecting border. $\blacksquare$

**Remark (the bound on λ).** Theorem 1 can fail for $\lambda > 1/4$. On a checkerboard of the values 0 and 1 with $g(s) = K^2/(K^2 + s^2)$ and $K = 10$, every difference is $\pm 1$ and $c = 100/101$. An interior pixel of value 1 has four neighbors of value 0, so with $\lambda = 3/10$ it goes to $1 - \frac{3}{10} \cdot 4 \cdot \frac{100}{101} = -\frac{19}{101} < 0$, and an interior pixel of value 0 goes to $\frac{120}{101} > 1$. Theorem 2 still holds there, since it needs no bound on $\lambda$.

**Remark (the linear case).** With $g \equiv 1$, $J(p) = I(p) + \lambda \sum_{q \in N_4(p)} (I(q) - I(p))$, which is the 5-point Laplacian step of the heat equation with the clamp rule: a neighbor outside the image, replaced by the nearest pixel $p$ itself, adds $I(p) - I(p) = 0$.
