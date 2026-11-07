---
title: The pivots of the Macaulay matrix are the leading monomials of its row space
proves: [correctness, termination]
status: full
---

Let $K$ be a field, $S = K[x_1, \ldots, x_n]$, $>$ a monomial order, $F = (f_1, \ldots, f_s)$ and $D \ge 0$. Let $c_1 > c_2 > \cdots > c_N$ be the column monomials. Identify a polynomial $g$ with all monomials among the $c_j$ with its coefficient vector, and write $\operatorname{lead}(v)$ for the least index $j$ with $v_j \ne 0$. Because the columns are decreasing, $\operatorname{lead}(g)$ is the column of $\operatorname{LM}(g)$ for $g \ne 0$.

**Claim 1 (row space).** The row space of $M_D(F)$ is $V_D = \{ \sum_i h_i f_i : h_i \in S, \ \deg(h_i f_i) \le D \text{ or } h_i = 0 \}$.

*Proof.* Each row $m f_i$ is in $V_D$, and $V_D$ is a $K$-vector space, so the row space is contained in $V_D$. Conversely, if $\deg(h_i f_i) \le D$ then each term $c\, m$ of $h_i$ has $\deg(m f_i) \le D$, so $h_i f_i = \sum c\, (m f_i)$ is a combination of rows. $\square$

**Claim 2 (elimination).** Line L6 terminates, keeps the row space, and produces rows $e_1, \ldots, e_\rho$ with pivot columns $p_1 < \cdots < p_\rho$ such that $e_k$ has entry $1$ in column $p_k$, entry $0$ in every other pivot column, and entry $0$ in every column left of $p_k$.

*Proof.* The loop runs over the $N$ columns once, with finitely many row operations each, so it stops. Swapping, scaling a row by a nonzero scalar, and adding a multiple of one row to another are invertible, so the row space does not change. When column $j$ is processed and a pivot row is chosen, that row is scaled to have entry $1$ in column $j$, and column $j$ is cleared in all other rows, so it stays $1$ in its row and $0$ elsewhere; later steps only add multiples of later pivot rows, which have $0$ in column $j$. When column $j$ is processed, the unused rows are all zero in columns $< j$: each earlier column was either cleared by its pivot, or had no nonzero entry in any unused row. So a pivot row chosen at column $j$ is zero left of $j$, and later steps add multiples of rows that are zero left of their own pivot, which is to the right of $j$. At the end every unused row is zero, because each of its entries was zero when its column was processed and stayed zero. $\square$

**Claim 3 (pivots are leading monomials).** $\{ c_{p_1}, \ldots, c_{p_\rho} \} = \operatorname{LM}(V_D)$, and $e_1, \ldots, e_\rho$ is a basis of $V_D$.

*Proof.* By Claims 1 and 2, the $e_k$ span $V_D$. They are independent, because $e_k$ is the only one with a nonzero entry in column $p_k$. Each $e_k$ is in $V_D$ with $\operatorname{lead}(e_k) = p_k$, so $c_{p_k} \in \operatorname{LM}(V_D)$. Conversely let $0 \ne g = \sum_k \lambda_k e_k \in V_D$, and let $k_0$ be the least $k$ with $\lambda_k \ne 0$. Column $p_{k_0}$ of $g$ equals $\lambda_{k_0} \ne 0$, because the other $e_k$ vanish there. Every column $j < p_{k_0}$ of $g$ is $0$: each $e_k$ with $k \ge k_0$ is zero left of $p_k \ge p_{k_0}$. So $\operatorname{LM}(g) = c_{p_{k_0}}$. $\square$

**Claim 4 (membership).** MEMBER returns true if and only if $g \in V_D$.

*Proof.* Line L8 replaces $g$ by $g - \sum_k \mu_k e_k$ for some scalars, and after the step for $e_k$ the entry in column $p_k$ is $0$, and later steps do not change it, since the later rows vanish there. So the final $g^\ast$ satisfies $g^\ast_{p_k} = 0$ for all $k$, and $g^\ast \equiv g$ modulo $V_D$. If $g \in V_D$ then $g^\ast \in V_D$, and a nonzero element of $V_D$ has its leading column at some $p_k$ by Claim 3, where $g^\ast$ is $0$. So $g^\ast = 0$. If $g \notin V_D$ then $g^\ast \ne 0$ since $g - g^\ast \in V_D$. $\square$

**Claim 5 (homogeneous case).** If every $f_i$ is homogeneous and the rows are the $m f_i$ with $\deg(m f_i) = D$, the row space is $I_D = I \cap S_D$ for $I = \langle F \rangle$. So the number of columns minus the rank is $\dim_K (S/I)_D$, and the pivots are the monomials of degree $D$ in $\langle \operatorname{LT}(I) \rangle$ for a graded order.

*Proof.* The rows lie in $I_D$. Let $g \in I_D$, so $g = \sum_i h_i f_i$ for some $h_i \in S$. Taking the homogeneous component of degree $D$ on both sides, and writing $h_i^{(k)}$ for the component of degree $k$, gives $g = \sum_i h_i^{(D - d_i)} f_i$, where $d_i = \deg f_i$ and the term is absent if $D < d_i$. Each summand is a combination of rows $m f_i$ with $\deg m = D - d_i$. So the row space is $I_D$, and $\dim (S/I)_D = \dim S_D - \dim I_D$ is the number of columns minus the rank. By Claim 3 the pivots are $\operatorname{LM}(I_D)$. For a graded order and homogeneous $I$, a monomial $u$ of degree $D$ lies in $\langle \operatorname{LT}(I) \rangle$ exactly when $u = \operatorname{LM}(g)$ for some $g \in I$, and then also for the homogeneous component of $g$ of degree $D$, which is in $I_D$ because $I$ is homogeneous. $\blacksquare$
