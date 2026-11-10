---
title: The Shares join finds each output tuple at exactly one reducer, and its optimal shares
proves: [correctness]
status: full
---

Let $Q = R_1 \bowtie \cdots \bowtie R_n$ be a natural join over the attributes $A_1, \ldots, A_m$, where every attribute occurs in at least one relation. The shares are positive integers $x_1, \ldots, x_m$ with $x_1 x_2 \cdots x_m = k$, the reducers are the cells $(c_1, \ldots, c_m)$ with $0 \le c_j < x_j$, and $h_j$ maps values of $A_j$ to $\{0, \ldots, x_j - 1\}$. The relations are bags, and an output tuple $u$ over all attributes appears in $Q$ once for each choice of one copy, from each $R_i$, of the restriction $u|_{R_i}$. The line numbers refer to the `pseudo id=main` block of the page.

## Correctness

For an output tuple $u$, let $\text{cell}(u) = (h_1(u.A_1), \ldots, h_m(u.A_m))$.

**Lemma 1.** For every relation $R_i$ and every copy of the tuple $u|_{R_i}$ in $R_i$, the reducer $\text{cell}(u)$ receives that copy exactly once.

*Proof.* Line L3 sends a tuple $t$ of $R_i$ to the cells whose coordinate $c_j$ equals $h_j(t.A_j)$ for each attribute $A_j$ of $R_i$, and takes every value for the other coordinates. For $t = u|_{R_i}$, the cell $\text{cell}(u)$ has the coordinate $h_j(u.A_j) = h_j(t.A_j)$ for each attribute of $R_i$, so it is one of these cells. Line L3 lists each cell once. $\square$

**Lemma 2.** If the reducer of a cell $c$ outputs $u$, then $c = \text{cell}(u)$.

*Proof.* Take any attribute $A_j$, and a relation $R_i$ that contains it. The local join at $c$ outputs $u$ only from a tuple $t = u|_{R_i}$ that the cell received. By line L3, every tuple of $R_i$ at cell $c$ has $c_j = h_j(t.A_j) = h_j(u.A_j)$. This holds for every $j$, so $c = \text{cell}(u)$. $\square$

**Theorem 1.** The union of the outputs of the reducers is $Q$, with the right multiplicities.

*Proof.* By Lemma 2, an output tuple $u$ can only come from $\text{cell}(u)$. By Lemma 1, that reducer has every copy of every tuple $u|_{R_i}$, each once, so a correct local join (line L6) outputs $u$ exactly as many times as $Q$ has it. No other reducer outputs $u$. $\blacksquare$

The hash functions can be any functions. Their choice affects only the loads, not the output.

## Communication

**Theorem 2.** The map phase sends exactly $\sum_{i=1}^{n} |R_i| \prod_{A_j \notin R_i} x_j$ pairs.

*Proof.* For a tuple of $R_i$, line L3 fixes the coordinates of the attributes of $R_i$ and lets each other coordinate take its $x_j$ values, so it lists $\prod_{A_j \notin R_i} x_j$ cells. Add over the tuples. $\blacksquare$

## The optimal real shares

Write $\tau_i = |R_i| \prod_{A_j \notin R_i} x_j$ for the term of $R_i$, so the cost is $f(x) = \sum_i \tau_i$. Treat the shares as positive reals with $\prod_j x_j = k$.

**Lemma 3 (the Lagrange condition).** At a minimum of $f$ where $x_j > 1$, the terms of the relations that do not contain $A_j$ add up to the same number $\lambda k$ for every such $j$.

*Proof.* The term $\tau_i$ has the factor $x_j$ exactly when $A_j \notin R_i$, so $\partial \tau_i / \partial x_j = \tau_i / x_j$ in that case and $0$ otherwise. The constraint $g(x) = \prod_j x_j$ has $\partial g / \partial x_j = k / x_j$ on the constraint. At an interior minimum, $\nabla f = \lambda \nabla g$ for some $\lambda$ (the method of [Lagrange multipliers](/lagrange-multiplier/)), so $\sum_{i : A_j \notin R_i} \tau_i / x_j = \lambda k / x_j$. Multiply by $x_j$. $\square$

**Lemma 4 (dominated attributes).** If every relation that contains $A_j$ also contains $A_l$, then changing $(x_j, x_l)$ to $(1, x_j x_l)$ keeps the product $k$ and does not increase the cost. So some optimum has $x_j = 1$.

*Proof.* Look at one relation $R_i$. If it contains $A_j$, it contains $A_l$, and neither share is a factor of $\tau_i$, before or after. If it contains $A_l$ but not $A_j$, the factor $x_j \ge 1$ becomes $1$. If it contains neither, the factor $x_j x_l$ does not change. The case "contains $A_j$ but not $A_l$" does not occur. $\square$

**Theorem 3 (the triangle).** For $R(A, B) \bowtie S(B, C) \bowtie T(C, A)$ with $|R| = r$, $|S| = s$, $|T| = t$, the minimum of the cost over positive real shares with $x_A x_B x_C = k$ is $3 (rstk)^{1/3}$. It is reached exactly when $s x_A = t x_B = r x_C = (rstk)^{1/3}$. If $r = s = t$, the shares are $x_A = x_B = x_C = k^{1/3}$ and the cost is $3 r k^{1/3}$.

*Proof.* $R$ lacks $C$, $S$ lacks $A$ and $T$ lacks $B$, so the cost is $f = r x_C + s x_A + t x_B$. By the inequality of the arithmetic and geometric means,

$$f \ge 3 \left( r x_C \cdot s x_A \cdot t x_B \right)^{1/3} = 3 (rst \, x_A x_B x_C)^{1/3} = 3 (rstk)^{1/3},$$

with equality exactly when the three terms are equal. If they are all equal to $\mu$, then $\mu^3 = rstk$, so $\mu = (rstk)^{1/3}$, and $x_A = \mu / s$, $x_B = \mu / t$, $x_C = \mu / r$, whose product is $\mu^3 / (rst) = k$. So the bound is reached, and only there. These are the points of Lemma 3: each attribute is missing from exactly one relation, so the condition says that the three terms are equal. For $r = s = t$, $\mu = r k^{1/3}$ and each share is $k^{1/3}$. $\blacksquare$

**Theorem 4 (the chain).** For $R(A, B) \bowtie S(B, C) \bowtie T(C, D)$ with sizes $r$, $s$, $t$, the optimal real shares are $x_A = x_D = 1$, $x_B = \sqrt{kr/t}$, $x_C = \sqrt{kt/r}$, and the cost is $s + 2\sqrt{krt}$.

*Proof.* $A$ occurs only in $R$, which also contains $B$, so Lemma 4 gives $x_A = 1$. In the same way, $D$ occurs only in $T$, which contains $C$, so $x_D = 1$. The cost is then $r x_C + s + t x_B$ with $x_B x_C = k$. By the inequality of the arithmetic and geometric means, $r x_C + t x_B \ge 2\sqrt{rt \, x_B x_C} = 2\sqrt{krt}$, with equality when $r x_C = t x_B$. Together with $x_B x_C = k$, this gives $x_B^2 = kr/t$ and $x_C^2 = kt/r$. $\blacksquare$

## The load per reducer

**Corollary 5.** For the triangle with $r = s = t$ and shares $k^{1/3}$, the average reducer input is $3r / k^{2/3}$.

*Proof.* By Theorems 2 and 3, the total input of the reducers is $3 r k^{1/3}$, and there are $k$ reducers. $\square$

The largest reducer input is close to the average when no value is frequent. A tuple of $R$ with $A = a$ and $B = b$ goes to the $x_C$ cells of the line $(h_A(a), h_B(b), \cdot)$. If a value $a$ occurs $d$ times in $R$, those tuples all have the coordinate $h_A(a)$, so they fall on only $x_B$ lines. By the pigeonhole principle, some line gets at least $d / x_B$ of them, and every cell of that line gets all of those. Inputs with such heavy values need the skew-aware methods of Beame, Koutris and Suciu.
