---
title: BILATERAL returns the normalized bilateral sum over the cut window, and its output stays inside the range of the window
proves: [correctness]
status: full
---

Let $f$ have $W \ge 1$ columns and $H \ge 1$ rows, let $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ be its pixels, and let $O = \{-R, \dots, R\}^2$ be the offsets. For $p \in D$ the cut window is $N(p) = \{q \in D : q - p \in O\}$. The weights satisfy $w_s \ge 0$ and $w_r \ge 0$ everywhere, and $w_s(0, 0) > 0$, $w_r(0) > 0$. Write $\omega(p, q) = w_s(q - p)\, w_r(f(q) - f(p))$.

**Lemma 1 (each pair once).** The pairs $(p, q)$ that lines L1 to L5 visit are exactly the pairs with $p \in D$ and $q \in N(p)$, each once.

*Proof.* Line L1 picks each $o \in O$ once, and for this $o$ line L3 picks each $p \in D$ with $p + o \in D$ once. So the visited pairs are $(p, p + o)$ with $o \in O$, $p \in D$ and $p + o \in D$. The map $(p, o) \mapsto (p, p + o)$ is one to one, with the inverse $(p, q) \mapsto (p, q - p)$, and its image is the set of pairs with $p \in D$, $q \in D$ and $q - p \in O$, which is $q \in N(p)$. $\square$

**Lemma 2 (the sums).** After line L5 has run for the last time, for every $p \in D$,

$$\mathrm{num}[p] = \sum_{q \in N(p)} \omega(p, q)\, f(q), \qquad \mathrm{den}[p] = \sum_{q \in N(p)} \omega(p, q).$$

*Proof.* Both arrays start at 0. When the pair $(p, p + o)$ is visited, line L2 has set $s = w_s(o)$, so line L4 sets $w = \omega(p, q)$ with $q = p + o$, and line L5 adds $w f(q)$ to $\mathrm{num}[p]$ and $w$ to $\mathrm{den}[p]$; no other entry changes. Addition is associative and commutative, so by Lemma 1 the final values are the sums over $q \in N(p)$, in any order of the visits. $\square$

**Theorem.** BILATERAL returns, for every $p \in D$,

$$g(p) = \frac{\sum_{q \in N(p)} \omega(p, q)\, f(q)}{\sum_{q \in N(p)} \omega(p, q)},$$

the division is defined, and $\min_{q \in N(p)} f(q) \le g(p) \le \max_{q \in N(p)} f(q)$.

*Proof.* Line L6 divides the sums of Lemma 2. The pixel $p$ itself lies in $N(p)$, since $0 \in O$, and its term in the denominator is $w_s(0, 0)\, w_r(0) > 0$. All other terms are nonnegative, so $\mathrm{den}[p] > 0$ and the division is defined. Put $\alpha_q = \omega(p, q) / \mathrm{den}[p]$. Then $\alpha_q \ge 0$, $\sum_q \alpha_q = 1$ and $g(p) = \sum_q \alpha_q f(q)$, a convex combination of the values in the window, which lies between their minimum and their maximum. $\blacksquare$

**Corollary (two limits).** If $w_r \equiv 1$, the output is the filter with the normalized spatial weights over the cut window, $g(p) = \sum_{q \in N(p)} w_s(q - p) f(q) / \sum_{q \in N(p)} w_s(q - p)$. If $f$ is constant on $N(p)$, then $g(p) = f(p)$, whatever the weights are, because a convex combination of equal values is that value.
