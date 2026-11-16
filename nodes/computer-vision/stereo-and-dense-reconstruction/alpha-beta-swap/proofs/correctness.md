---
title: Correctness of alpha-beta swap
proves: [correctness]
status: full
---

The energy is $E(f) = \sum_p D_p(f_p) + \sum_{(p,q) \in \mathcal{N}} w_{pq} V(f_p, f_q)$ with $w_{pq} \ge 0$, and $V$ is a semimetric: $V(a,b) = V(b,a) \ge 0$, and $V(a,b) = 0$ exactly when $a = b$. We prove that each move returns a labeling of least energy among all $\alpha\beta$-swaps of $f$, that the loop stops at a labeling that no swap improves, and that no constant factor bound holds for such labelings.

## 1. Each move is optimal in its move space

Let $P = \{p : f_p \in \{\alpha, \beta\}\}$. An $\alpha\beta$-swap of $f$ is a labeling $g$ with $g_p \in \{\alpha, \beta\}$ for $p \in P$ and $g_p = f_p$ otherwise. Write $g = g(x)$ for $x \in \{0,1\}^P$, with $g_p = \alpha$ if $x_p = 0$ and $g_p = \beta$ if $x_p = 1$. Every swap has this form, and every $x$ gives a swap.

Split $E(g(x))$ into four groups of terms.

- Data terms and pair terms with no end in $P$: they do not depend on $x$, so they are a constant $K$.
- The data term of $p \in P$: $U_p(0) = D_p(\alpha)$ and $U_p(1) = D_p(\beta)$.
- A pair $(p, q)$ with $p \in P$ and $q \notin P$: the label of $q$ is fixed, so the term is a function of $x_p$ alone, $w V(\alpha, f_q)$ or $w V(\beta, f_q)$, and lines L5 add it to $U_p$. The same holds with the roles of $p$ and $q$ exchanged.
- A pair with both ends in $P$: the term is $\theta(x_p, x_q)$ with $\theta(0,0) = w V(\alpha, \alpha) = 0$, $\theta(1,1) = 0$, $\theta(0,1) = w V(\alpha, \beta)$ and $\theta(1,0) = w V(\beta, \alpha)$.

So $E(g(x)) = K + \sum_{p \in P} U_p(x_p) + \sum \theta(x_p, x_q)$. Every pair term is regular, because $\theta(0,0) + \theta(1,1) = 0 \le \theta(0,1) + \theta(1,0)$ by $V \ge 0$. By the [Kolmogorov-Zabih theorem](/graph-representable-energies/), the graph of the code represents this binary energy: the decomposition $\theta = C x_p - C x_q + (B + C)(1 - x_p)\, x_q$ with $B = \theta(0,1)$ and $C = \theta(1,0)$ gives an edge $p \to q$ of capacity $B + C \ge 0$ and linear terms, and each linear coefficient becomes an edge from the source or to the sink. A minimum cut (line L7) gives a minimizer $x$ with $x_p = 0$ on the source side, and line L8 returns $g(x)$, a swap of least energy.

Only $V(a, a) = 0$ and $V \ge 0$ were used. Symmetry is not needed for the move, but it is part of the usual definition.

## 2. Termination and local optimality

Line L9 replaces $f$ only by a labeling of strictly smaller energy, and there are $L^n$ labelings, so the loop stops. In the last cycle $f$ did not change, so for every pair $\{\alpha, \beta\}$ the best swap has energy at least $E(f)$. As $f$ is itself a swap of $f$ (with $x_p = 0$ where $f_p = \alpha$ and $x_p = 1$ where $f_p = \beta$), no swap of any pair lowers the energy.

A change of one site $p$ from $f_p$ to another label $\gamma$ is an $f_p\gamma$-swap. So the output is also a local minimum for changes of one site.

## 3. No constant factor bound

Take two neighboring sites $p, q$ with $w = 1$, three labels $a, b, c$, the Potts model $V = \lambda [\cdot \ne \cdot]$, and numbers $0 < \delta$ and $M \ge \lambda$. Let $D_p = (0, M, \delta)$ and $D_q = (M, 0, \delta)$ for the labels $(a, b, c)$. The labeling $(a, b)$ has $E = \lambda$.

- The $ab$-swaps are $(a,b)$, $(b,a)$, $(a,a)$, $(b,b)$ with energies $\lambda$, $2M + \lambda$, $M$, $M$, all at least $\lambda$.
- The $ac$-swaps change only $p$ (the label of $q$ is $b$): $(c, b)$ has $E = \delta + \lambda$.
- The $bc$-swaps change only $q$: $(a, c)$ has $E = \delta + \lambda$.

So $(a, b)$ is a local minimum for all swaps, and the algorithm started there returns it. The labeling $(c, c)$ has $E = 2\delta$. The ratio $\lambda / (2\delta)$ is unbounded as $\delta \to 0$, so no bound $E(\hat f) \le c' E(f^*)$ with a constant $c'$ holds for swap local minima, even for the Potts model. This is the point of Section 6.2 and Figure 8 of Boykov, Veksler and Zabih (2001). An expansion move to $c$ reaches $(c, c)$ in one step, in line with the bound of [alpha-expansion](/alpha-expansion/). $\square$
