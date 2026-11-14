---
title: The range of the next-state functions under constrain is the image, and the output-splitting recursion computes the range
proves: [correctness]
status: full
---

**Setting.** The present-state variables are $s = (s_1, \ldots, s_m)$, the inputs are $x = (x_1, \ldots, x_k)$, and $z = (s, x)$ ranges over $\{0, 1\}^{m + k}$. The next-state functions form the vector $\delta = (\delta_1, \ldots, \delta_m)$, $\delta_i : \{0, 1\}^{m + k} \to \{0, 1\}$. A set of states $S \subseteq \{0, 1\}^m$ is given by its characteristic function, read as a function of $z$ that does not depend on $x$. The *image* is

$$\mathrm{Img}(S) = \{\delta(s, x) : s \in S,\ x \in \{0, 1\}^k\}.$$

For a vector $g = (g_1, \ldots, g_r)$ of functions of $z$ and a function $c$, write $g(c) = \{g(z) : c(z) = 1\}$ and $\mathrm{Range}(g) = g(1)$. The vector $g \downarrow c$ is $(g_1 \downarrow c, \ldots, g_r \downarrow c)$, where $\downarrow$ is constrain. A set $Y \subseteq \{0, 1\}^r$ is identified with its characteristic function over fresh variables $y_1, \ldots, y_r$. For $r = 0$, $\{0, 1\}^0$ has one element, the empty vector, and $\mathrm{Range}$ of the empty vector is that one-element set, the constant 1.

**Lemma 1 (range under constrain).** For $c \ne 0$, $\mathrm{Range}(g \downarrow c) = g(c)$.

*Proof.* The [generalized cofactor](/generalized-cofactor/) proof shows (its Theorem 2) that $f \downarrow c = f \circ \pi_c$ for every $f$, where $\pi_c$ is the closest-point map of $c$. The map $\pi_c$ depends on $c$ only, so the same map serves every component: $(g \downarrow c)(z) = g(\pi_c(z))$. By its definition, $\pi_c(z)$ is a point of $c$ for every $z$, and $\pi_c(z) = z$ when $c(z) = 1$, since then $z$ itself extends every prefix of $z$.

($\subseteq$) For any $z$, $(g \downarrow c)(z) = g(\pi_c(z))$ and $c(\pi_c(z)) = 1$, so the value is in $g(c)$.

($\supseteq$) For $z$ with $c(z) = 1$, $g(z) = g(\pi_c(z)) = (g \downarrow c)(z)$, which is in $\mathrm{Range}(g \downarrow c)$. $\square$

**Lemma 2 (RANGE).** For every vector $g = (g_1, \ldots, g_r)$ that does not use the variables $y$, RANGE($g$) is the characteristic function of $\mathrm{Range}(g)$.

*Proof.* Induction on $r$.

- *Base, $r = 0$ (line L4).* Both sides are the constant 1.
- *Step, $g_1 = 1$ (line L5).* Every value $g(z)$ has first bit 1, so $\mathrm{Range}(g) = \{(1, w) : w \in \mathrm{Range}(g_2, \ldots, g_r)\}$. By the induction hypothesis this is $y_1 \wedge$ RANGE($g_2, \ldots, g_r$).
- *Step, $g_1 = 0$ (line L6).* The same with first bit 0 and $\neg y_1$.
- *Step, $g_1$ not constant (lines L7 to L9).* Split by the value of $g_1$:
  $$\mathrm{Range}(g) = \{(1, w) : w \in (g_2, \ldots, g_r)(g_1)\} \cup \{(0, w) : w \in (g_2, \ldots, g_r)(\neg g_1)\}.$$
  Since $g_1$ is not constant, $g_1 \ne 0$ and $\neg g_1 \ne 0$. By Lemma 1, the first set of tails is $\mathrm{Range}((g_2, \ldots, g_r) \downarrow g_1)$ and the second is $\mathrm{Range}((g_2, \ldots, g_r) \downarrow \neg g_1)$. Constrain does not add variables that are not in its arguments, so these vectors do not use $y$, and the induction hypothesis applies to the calls of lines L7 and L8. Line L9 returns $(y_1 \wedge \mathrm{hi}) \vee (\neg y_1 \wedge \mathrm{lo})$, which is the characteristic function of the union. $\square$

**Theorem (correctness of IMAGE).** IMAGE($\delta$, $S$) is the characteristic function of $\mathrm{Img}(S)$ over $y$.

*Proof.* If $S = 0$, the image is empty and line L1 returns 0. Otherwise $S$, read as a function of $z$, is not 0, and

$$\mathrm{Img}(S) = \{\delta(z) : S(z) = 1\} = \delta(S) = \mathrm{Range}(\delta \downarrow S)$$

by Lemma 1. Line L2 computes $\delta \downarrow S$, and line L3 returns its range by Lemma 2. $\blacksquare$

**Remark (the variable order).** Lemma 1 holds for every variable order, because the closest-point map is defined for any order. The order changes the BDDs of $\delta \downarrow S$ and their sizes, not the result. Also, constrain does not need $S$ to be independent of $x$; for a constraint on states and inputs together, the same proof gives $\{\delta(z) : c(z) = 1\}$.

**Remark (termination).** Each call of RANGE removes one component, so the recursion has depth $r$ and at most $2^{r + 1} - 1$ calls.
