---
title: Buchberger's criterion, the product criterion and the chain criterion
proves: [statement]
status: full
---

We use the notation of the page. $K$ is a field, $>$ is a monomial order on $K[x_1, \ldots, x_n]$, and $G = \{g_1, \ldots, g_t\}$ is a finite set of nonzero polynomials that generates the ideal $I$. For $i \ne j$ let $x^{\gamma_{ij}} = \operatorname{lcm}(\operatorname{LM}(g_i), \operatorname{LM}(g_j))$ and

$$S(g_i, g_j) = \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_i)} g_i - \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_j)} g_j .$$

The two leading terms cancel, so $S(g_i, g_j) = 0$ or $\operatorname{LM}(S(g_i, g_j)) < x^{\gamma_{ij}}$. A sum $\sum_l A_l g_l$ is an *lcm-representation* of $S(g_i, g_j)$ when it equals $S(g_i, g_j)$ and $\operatorname{LM}(A_l g_l) < x^{\gamma_{ij}}$ for each $l$ with $A_l g_l \ne 0$.

**Lemma 1 (cancellation).** Let $g_{i_1}, \ldots, g_{i_s}$ be distinct elements of $G$, let $c_1, \ldots, c_s \in K$, and let $x^{\alpha(1)}, \ldots, x^{\alpha(s)}$ be monomials with $x^{\alpha(m)} \operatorname{LM}(g_{i_m}) = x^\delta$ for each $m$. If $p = \sum_m c_m x^{\alpha(m)} g_{i_m}$ is zero or has $\operatorname{LM}(p) < x^\delta$, then $p$ is a $K$-linear combination of the polynomials $x^{\delta - \gamma_{i_m i_{m+1}}} S(g_{i_m}, g_{i_{m+1}})$ for $1 \le m < s$, and each of these is zero or has leading monomial less than $x^\delta$.

*Proof.* Let $p_m = x^{\alpha(m)} g_{i_m} / \operatorname{LC}(g_{i_m})$, so $\operatorname{LT}(p_m) = x^\delta$, and let $b_m = c_m \operatorname{LC}(g_{i_m})$, so $p = \sum_m b_m p_m$. The coefficient of $x^\delta$ in $p$ is $\sum_m b_m$, and it is zero by the hypothesis. Summation by parts gives

$$p = \sum_{m=1}^{s-1} (b_1 + \cdots + b_m)(p_m - p_{m+1}) + (b_1 + \cdots + b_s) p_s = \sum_{m=1}^{s-1} (b_1 + \cdots + b_m)(p_m - p_{m+1}).$$

Both $\operatorname{LM}(g_{i_m})$ and $\operatorname{LM}(g_{i_{m+1}})$ divide $x^\delta$, so $x^{\gamma_{i_m i_{m+1}}}$ divides $x^\delta$, and

$$p_m - p_{m+1} = \frac{x^\delta}{\operatorname{LT}(g_{i_m})} g_{i_m} - \frac{x^\delta}{\operatorname{LT}(g_{i_{m+1}})} g_{i_{m+1}} = x^{\delta - \gamma_{i_m i_{m+1}}} S(g_{i_m}, g_{i_{m+1}}).$$

The leading terms of $p_m$ and $p_{m+1}$ are both $x^\delta$, so they cancel, and $p_m - p_{m+1}$ is zero or has leading monomial less than $x^\delta$. $\square$

**Theorem A (Buchberger's criterion).** $G$ is a Gröbner basis of $I$ if and only if each $S(g_i, g_j)$, $i < j$, has an lcm-representation. In particular $G$ is a Gröbner basis if and only if each $S(g_i, g_j)$ has remainder zero on division by $G$.

*Proof of "only if".* Let $G$ be a Gröbner basis. Each $S(g_i, g_j)$ lies in $I$. By the equivalent conditions on the page [Gröbner basis](/groebner-basis/), division by $G$ leaves remainder zero, so $S(g_i, g_j) = \sum_l A_l g_l$ with $\operatorname{LM}(A_l g_l) \le \operatorname{LM}(S(g_i, g_j))$ for each nonzero term, by the degree property of the division algorithm. If $S(g_i, g_j) \ne 0$, its leading monomial is less than $x^{\gamma_{ij}}$, so this is an lcm-representation. If $S(g_i, g_j) = 0$, the empty sum is one.

*Proof of "if".* Assume that each $S(g_i, g_j)$ has an lcm-representation, and let $f \in I$ be nonzero. We show that some $\operatorname{LT}(g_i)$ divides $\operatorname{LT}(f)$, which is condition 2 on the page [Gröbner basis](/groebner-basis/).

Step 1. Because $G$ generates $I$, there are representations $f = \sum_{i=1}^t h_i g_i$. For such a representation let $x^{\delta} = \max \{ \operatorname{LM}(h_i g_i) : h_i g_i \ne 0 \}$. A monomial order is a well-order, so we can choose a representation for which $x^\delta$ is the least possible. Fix it.

Step 2. $\operatorname{LM}(f) \le x^\delta$, because each monomial of $f$ is a monomial of some $h_i g_i$. If $\operatorname{LM}(f) = x^\delta$, then $x^\delta = \operatorname{LM}(h_i) \operatorname{LM}(g_i)$ for some $i$, so $\operatorname{LT}(g_i)$ divides $\operatorname{LT}(f)$ and we are done. So assume, to reach a contradiction, that $\operatorname{LM}(f) < x^\delta$.

Step 3. Let $T = \{ i : \operatorname{LM}(h_i g_i) = x^\delta \}$. Write

$$f = \sum_{i \in T} \operatorname{LT}(h_i) g_i + \sum_{i \in T} (h_i - \operatorname{LT}(h_i)) g_i + \sum_{i \notin T} h_i g_i .$$

Every term of the second and third sums has leading monomial less than $x^\delta$. Since $\operatorname{LM}(f) < x^\delta$, the first sum $p$ is zero or has $\operatorname{LM}(p) < x^\delta$. Each $\operatorname{LT}(h_i) = c_i x^{\alpha(i)}$ with $x^{\alpha(i)} \operatorname{LM}(g_i) = x^\delta$, and the $g_i$ with $i \in T$ are distinct. By Lemma 1, $p = \sum_m e_m x^{\delta - \gamma_m} S_m$ with $e_m \in K$, where each $S_m$ is an S-polynomial of two elements of $G$ and $x^{\gamma_m}$ is its lcm.

Step 4. By the hypothesis, $S_m = \sum_l A_{ml} g_l$ with $\operatorname{LM}(A_{ml} g_l) < x^{\gamma_m}$. So $x^{\delta - \gamma_m} S_m = \sum_l x^{\delta - \gamma_m} A_{ml} g_l$, and each term has leading monomial less than $x^{\delta - \gamma_m} x^{\gamma_m} = x^\delta$, because a monomial order respects multiplication. Put this into the first sum of Step 3. The result is a representation $f = \sum_l h'_l g_l$ in which every $\operatorname{LM}(h'_l g_l)$ is less than $x^\delta$. This contradicts the choice of $x^\delta$ in Step 1. So $\operatorname{LM}(f) = x^\delta$, and Step 2 ends the proof.

The second sentence of the theorem follows: a remainder of zero gives an lcm-representation, as in the proof of "only if", and if $G$ is a Gröbner basis every remainder of an element of $I$ is zero. $\square$

**Theorem B (product criterion).** If $\operatorname{LM}(g_i)$ and $\operatorname{LM}(g_j)$ have no common variable, then $S(g_i, g_j)$ has an lcm-representation in terms of $g_i$ and $g_j$ only.

*Proof.* Scaling $g_i$ and $g_j$ by nonzero constants changes neither the S-polynomial nor the condition, so assume $\operatorname{LC}(g_i) = \operatorname{LC}(g_j) = 1$. Write $g_i = \operatorname{LM}(g_i) + r_i$ and $g_j = \operatorname{LM}(g_j) + r_j$, where $r_i$ is zero or $\operatorname{LM}(r_i) < \operatorname{LM}(g_i)$, and the same for $r_j$. The two leading monomials are coprime, so $x^{\gamma_{ij}} = \operatorname{LM}(g_i) \operatorname{LM}(g_j)$ and

$$S(g_i, g_j) = \operatorname{LM}(g_j) g_i - \operatorname{LM}(g_i) g_j = (g_j - r_j) g_i - (g_i - r_i) g_j = r_i g_j - r_j g_i .$$

If $r_i \ne 0$, then $\operatorname{LM}(r_i g_j) = \operatorname{LM}(r_i) \operatorname{LM}(g_j) < \operatorname{LM}(g_i) \operatorname{LM}(g_j) = x^{\gamma_{ij}}$. In the same way $\operatorname{LM}(r_j g_i) < x^{\gamma_{ij}}$ if $r_j \ne 0$. So $r_i g_j - r_j g_i$ is an lcm-representation. $\square$

**Theorem C (chain criterion).** Let $i, j, k$ be distinct, and assume that $\operatorname{LM}(g_k)$ divides $x^{\gamma_{ij}}$. If $S(g_i, g_k)$ and $S(g_j, g_k)$ have lcm-representations, then so does $S(g_i, g_j)$.

*Proof.* $\operatorname{LM}(g_i)$ and $\operatorname{LM}(g_k)$ both divide $x^{\gamma_{ij}}$, so $x^{\gamma_{ik}}$ divides $x^{\gamma_{ij}}$. In the same way $x^{\gamma_{jk}}$ divides $x^{\gamma_{ij}}$. Then

$$x^{\gamma_{ij} - \gamma_{ik}} S(g_i, g_k) - x^{\gamma_{ij} - \gamma_{jk}} S(g_j, g_k) = \Big( \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_i)} g_i - \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_k)} g_k \Big) - \Big( \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_j)} g_j - \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_k)} g_k \Big) = S(g_i, g_j).$$

Multiply each term of the lcm-representation of $S(g_i, g_k)$ by $x^{\gamma_{ij} - \gamma_{ik}}$. Each leading monomial was less than $x^{\gamma_{ik}}$, so now it is less than $x^{\gamma_{ij}}$. Do the same with $S(g_j, g_k)$. The difference is an lcm-representation of $S(g_i, g_j)$. $\square$

**Corollary (use in an algorithm).** Let $B$ be a set of pairs $\{i, j\}$. Assume that for each pair not in $B$, either Theorem B applies, or $S(g_i, g_j)$ has remainder zero on division by $G$, or there is a $k$ with $\operatorname{LM}(g_k) \mid x^{\gamma_{ij}}$ such that the pairs $\{i, k\}$ and $\{j, k\}$ are not in $B$ and were justified before $\{i, j\}$ in some fixed order of the pairs. If $B$ is empty, then $G$ is a Gröbner basis.

*Proof.* Take the pairs in the fixed order. By induction on the position, each pair has an lcm-representation: the first two cases give one directly (Theorem B, or the "only if" argument for a remainder of zero), and the third gives one by Theorem C from the two earlier pairs. Theorem A then applies. $\blacksquare$

The order in the corollary is necessary. Without it, three pairs could each be removed by the other two, and nothing would be checked. The page gives an example.
