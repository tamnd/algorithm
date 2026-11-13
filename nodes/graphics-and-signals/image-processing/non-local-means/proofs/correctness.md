---
title: NL-MEANS returns the patch-weighted mean over the cut search window, with every patch distance read correctly from the integral image of its offset
proves: [correctness]
status: full
---

Let $f$ have $W \ge 1$ columns and $H \ge 1$ rows, let $D_0 = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ be its pixels, and let $\tilde f(x) = f[\mathrm{clamp}(x_y, H)][\mathrm{clamp}(x_x, W)]$ be its clamp extension to all integer points, which equals $f$ on $D_0$. Let $A = \{-P, \dots, P\}^2$ be the patch offsets, $|A| = (2P+1)^2$, and $O = \{-S, \dots, S\}^2$ the search offsets. For $p \in D_0$ the cut search window is $N(p) = \{q \in D_0 : q - p \in O\}$, and the patch distance is $d(p, q) = \frac{1}{|A|} \sum_{t \in A} (\tilde f(p + t) - \tilde f(q + t))^2$. Let $\phi$ be the weight function of line L6, with $\phi(0) > 0$ and $\phi \ge 0$; the default is $\phi(d) = e^{-d/h^2}$.

**Lemma 1 (the patch distance).** Fix $o \in O$, and let $D(x) = (\tilde f(x) - \tilde f(x + o))^2$ for $x$ in the grown domain $G = \{-P, \dots, W - 1 + P\} \times \{-P, \dots, H - 1 + P\}$, as line L2 computes. For every $p \in D_0$, line L5 returns $d(p, p + o)$.

*Proof.* Shift the indices of $G$ by $P$, so that $G$ becomes the pixels of an image $D'$ of $W + 2P$ columns and $H + 2P$ rows, $D'[j][i] = D(i - P, j - P)$. Line L3 builds its integral image, and by the lemma for RECT-SUM on the [integral image](/integral-image/) page, a rectangle query returns the sum of $D'$ over the rectangle. The patch of $p$ is $p + A$, which lies in $G$ because $0 \le p_x < W$ and $|t_x| \le P$, and likewise for the rows; in shifted indices it is the rectangle $[p_x, p_x + 2P + 1) \times [p_y, p_y + 2P + 1)$. So the query returns $\sum_{t \in A} D(p + t) = \sum_{t \in A} (\tilde f(p + t) - \tilde f(p + o + t))^2$, and the division by $|A|$ gives $d(p, p + o)$. $\square$

**Lemma 2 (each pair once).** The pairs $(p, q)$ visited by lines L4 to L7 over all offsets are exactly the pairs with $p \in D_0$ and $q \in N(p)$, each once.

*Proof.* Line L1 takes each $o \in O$ once, and line L4 takes each $p \in D_0$ with $p + o \in D_0$ once. The map $(p, o) \mapsto (p, p + o)$ is one to one, and its image is the set of pairs with $p, q \in D_0$ and $q - p \in O$. $\square$

**Theorem.** NL-MEANS returns, for every $p \in D_0$,

$$g(p) = \frac{\sum_{q \in N(p)} \phi(d(p, q))\, f(q)}{\sum_{q \in N(p)} \phi(d(p, q))},$$

the denominator is at least $\phi(0) > 0$, and $g(p)$ lies between the least and the largest value of $f$ on $N(p)$.

*Proof.* The arrays start at 0. When the pair $(p, q)$, $q = p + o$, is visited, Lemma 1 gives $d = d(p, q)$ at line L5, line L6 gives $w = \phi(d(p, q))$, and line L7 adds $w f(q)$ to $\mathrm{num}[p]$ and $w$ to $\mathrm{den}[p]$. By Lemma 2 and the commutativity of addition, after the loops $\mathrm{num}[p]$ and $\mathrm{den}[p]$ are the two sums over $N(p)$. Since $0 \in O$, $p \in N(p)$, and $d(p, p) = 0$, so $\mathrm{den}[p] \ge \phi(0) > 0$ and line L8 is defined. With $\alpha_q = \phi(d(p, q)) / \mathrm{den}[p] \ge 0$ and $\sum_q \alpha_q = 1$, $g(p) = \sum_q \alpha_q f(q)$ is a convex combination of the values on $N(p)$. $\blacksquare$

**Corollary (shifts).** If $f$ is replaced by $f + c$ for a constant $c$, every $D$ and every distance is unchanged, so the weights are unchanged and $g$ becomes $g + c$, because the weights $\alpha_q$ sum to 1. In particular a constant image is kept.
