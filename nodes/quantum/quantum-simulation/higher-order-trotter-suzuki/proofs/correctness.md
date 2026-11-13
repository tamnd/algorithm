---
title: Suzuki's formula S_2k has error O(t^(2k+1)/r^(2k)) for every k
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = H_1 + \cdots + H_L$ with Hermitian $H_j = c_jP_j$, and $\|\cdot\|$ is the spectral norm. All functions of $x$ below are products of finitely many matrix exponentials $e^{a xH_j}$ with real $a$, so they are entire functions of the complex variable $x$; the time evolution is the value at $x = -i\delta$.

**The circuit is $S_{2k}(-i\delta)^r$.** By induction on $k$, WEIGHTS(2k) returns weights $w_1, \ldots, w_m$, $m = 5^{k-1}$, with $S_{2k}(x) = S_2(w_1x)\cdots S_2(w_mx)$. For $k = 1$ (lines L1 and L2) this is $S_2(x)$. For $k \ge 2$, line L5 lists the weights of $S_{2k-2}(px)$ twice, those of $S_{2k-2}((1-4p)x)$, and those of $S_{2k-2}(px)$ twice, which is the recursion. Lines L9 to L11 lay out $S_2(w\delta)$ for each weight (the pair $(P, \theta)$ is $e^{-i\theta P}$, and $e^{-ic_jw\delta P_j/2} = e^{w x H_j/2}$ at $x = -i\delta$). Line L12 joins neighbors with the same string, which does not change the product since $e^{-i\theta P}e^{-i\theta'P} = e^{-i(\theta+\theta')P}$.

**Lemma 1 (symmetry).** $S_{2k}(x)S_{2k}(-x) = I$ for every $k$ and every $x$.

*Proof.* For $k = 1$, $S_2(x)S_2(-x)$ is $e^{xH_1/2}\cdots e^{xH_L}\cdots e^{xH_1/2}\,e^{-xH_1/2}\cdots e^{-xH_L}\cdots e^{-xH_1/2}$, and the factors cancel in pairs from the middle out. For $k \ge 2$, write $S = S_{2k-2}$, $p = p_k$ and $q = 1 - 4p$. Then
$$S_{2k}(x)S_{2k}(-x) = S(px)S(px)S(qx)S(px)\,S(px)S(-px)\,S(-px)S(-qx)S(-px)S(-px),$$
and by the induction hypothesis the middle pair $S(px)S(-px)$ is $I$; then the next pair is $I$, and so on, five times. $\square$

**Lemma 2 (logarithm).** There is $\rho > 0$ such that for $|x| < \rho$, $S_{2k}(x) = e^{F(x)}$ for a unique analytic $F$ with $F(0) = 0$ and $\|F(x)\| < \ln 2$, and $F$ is odd: $F(-x) = -F(x)$.

*Proof.* $S_{2k}(0) = I$ and $S_{2k}$ is continuous, so for small $|x|$, $\|S_{2k}(x) - I\| < 1/2$, and the series $F(x) = \log S_{2k}(x) = \sum_{m \ge 1} (-1)^{m+1}(S_{2k}(x) - I)^m/m$ converges and is analytic, with $e^{F(x)} = S_{2k}(x)$. The exponential is one to one on matrices of norm less than $\ln 2$ (its inverse there is this series). By Lemma 1, $e^{F(-x)} = S_{2k}(x)^{-1} = e^{-F(x)}$, and both $F(-x)$ and $-F(x)$ are small, so $F(-x) = -F(x)$. $\square$

So $F(x) = xF_1 + x^3F_3 + x^5F_5 + \cdots$ has only odd powers. Comparing with $S_{2k}(x) = I + x\sum_j H_j \cdot (\text{sum of the weights}) + O(x^2)$ gives $F_1 = \big(\sum_i w_i\big) H$, and $\sum_i w_i = 1$ by induction, since $4p + (1 - 4p) = 1$. So $F_1 = H$.

**Lemma 3 (order).** For every $k \ge 1$, $F(x) = xH + O(x^{2k+1})$ for $S_{2k}$, so $S_{2k}(x) = e^{xH} + O(x^{2k+1})$.

*Proof.* By induction on $k$. For $k = 1$, $F$ is odd with $F_1 = H$, so $F(x) = xH + O(x^3)$. Let $k \ge 2$ and assume $S_{2k-2}(y) = e^{yH + y^{2k-1}E + O(y^{2k+1})}$ for some matrix $E$ (true by the hypothesis and oddness). Then
$$S_{2k-2}(y) = e^{yH}\big(I + y^{2k-1}E + O(y^{2k})\big),$$
since $e^{A + B} = e^{A}(I + B) + O(\|A\|\|B\| + \|B\|^2)$ for small $A$ and $B$, and here $\|A\|\|B\| = O(y^{2k})$. Take the five stages with $y_i = w_ix$, $(w_1, \ldots, w_5) = (p, p, q, p, p)$. Moving the factor $e^{y_jH}$ past a term $y_i^{2k-1}E$ changes it only at order $x^{2k}$, because $e^{yH}Ee^{-yH} = E + O(y)$. So
$$S_{2k}(x) = e^{(4p + q)xH}\Big(I + \big(4p^{2k-1} + q^{2k-1}\big)x^{2k-1}E + O(x^{2k})\Big).$$
Now $4p + q = 1$, and $q = 1 - 4p = -4^{1/(2k-1)}p$ because $p(4 - 4^{1/(2k-1)}) = 1$. Hence $q^{2k-1} = -4p^{2k-1}$ and the bracket is $I + O(x^{2k})$. So $e^{F(x)} = e^{xH} + O(x^{2k})$. If $F(x) - xH$ had a lowest nonzero term $x^jG_j$ with $j < 2k$, then $e^{F(x)} - e^{xH} = x^jG_j + O(x^{j+1})$, a contradiction; so $F(x) = xH + O(x^{2k})$. By Lemma 2 $F$ is odd, and $2k$ is even, so $F(x) = xH + O(x^{2k+1})$. Finally $e^{F(x)} - e^{xH} = O(\|F(x) - xH\|) = O(x^{2k+1})$ for bounded $x$. $\square$

**From one step to $r$ steps.** By Lemma 3 and analyticity there are constants $C$ and $\delta_0 > 0$, depending on the $H_j$ and on $k$, with $\|S_{2k}(-i\delta) - e^{-iH\delta}\| \le C\delta^{2k+1}$ for $0 \le \delta \le \delta_0$. Each stage $S_2(-iw\delta)$ is a product of unitaries $e^{-iwc_j\delta P_j/2}$ and $e^{-iwc_L\delta P_L}$ with real $w$ (negative $w$ is allowed), so $S_{2k}(-i\delta)$ is unitary. For unitaries $\|S^r - U^r\| \le r\|S - U\|$, because $S^r - U^r = \sum_{j=0}^{r-1} S^{r-1-j}(S - U)U^j$. With $\delta = t/r \le \delta_0$,
$$\big\|S_{2k}(-it/r)^r - e^{-iHt}\big\| \le r\,C\,(t/r)^{2k+1} = C\,\frac{t^{2k+1}}{r^{2k}}.$$
So the error tends to zero with order $2k$ in the step size, and $r = \lceil (C t^{2k+1}/\epsilon)^{1/(2k)} \rceil$ steps suffice for error $\epsilon$. Explicit values of $C$ are Lemma 1 of Berry, Ahokas, Cleve and Sanders (2007), with norms of the terms, and Theorem 11 of Childs, Su, Tran, Wiebe and Zhu (2021), with nested commutators.

**Commuting terms.** If all $H_j$ commute, every $e^{a xH_j}$ commutes with every other, and $S_{2k}(x) = e^{(\sum_i w_i)xH} = e^{xH}$ exactly. $\blacksquare$
