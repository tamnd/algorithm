---
title: Correctness of sparse distributed addition and heap multiplication
proves: [correctness]
status: full
---

**Setting.** $R$ is a commutative ring and $>$ is a monomial order on the monomials of $R[x_1, \ldots, x_n]$: a total order with $x^\alpha > x^\beta \Rightarrow x^{\alpha+\gamma} > x^{\beta+\gamma}$. A list $[(\alpha_1, c_1), \ldots, (\alpha_t, c_t)]$ meets (D) when $x^{\alpha_1} > \cdots > x^{\alpha_t}$ and all $c_i \ne 0$.

**Lemma 1 (uniqueness).** Each polynomial $p$ has exactly one list that meets (D). *Proof.* The monomials with nonzero coefficient in $p$ form a finite set, and the order is total, so there is exactly one strictly decreasing listing of them. The coefficients are those of $p$. $\square$

So it is enough to show that each operation returns a list that meets (D) and whose terms sum to the right polynomial.

**ADD.** Let $f$ and $g$ meet (D). Loop invariant at line A2: $h$ meets (D); every monomial in $h$ is larger than every monomial of $f[i..]$ and of $g[j..]$; and $h$ represents the part of $f + g$ on the monomials larger than both $\operatorname{LM}(f[i])$ and $\operatorname{LM}(g[j])$ (with a missing entry treated as below every monomial). It holds at the start with $h$ empty. In case A3, $\operatorname{LM}(f[i])$ is larger than every monomial left in $g$, so the coefficient of that monomial in $f + g$ is that of $f$, which is nonzero, and it is smaller than every monomial of $h$; appending keeps (D) and the invariant. Case A4 is symmetric. In case A5 to A7 the monomial occurs in both, its coefficient in $f + g$ is $u$, and it is appended exactly when $u \ne 0$. Each step increases $i + j$, so the loop ends. At line A8 one list is exhausted, the rest of the other list is smaller than everything in $h$ and has nonzero coefficients that equal those of $f + g$, so the output meets (D) and equals $f + g$. $\square$

**MUL.** Let $f = [(\alpha_i, a_i)]_{i \le s}$ and $g = [(\beta_j, b_j)]_{j \le t}$ meet (D), with $s, t \ge 1$ (line L1 handles the empty case, since the product with $0$ is $0$). Write $P_{ij} = a_i b_j x^{\alpha_i + \beta_j}$ and $\mu_{ij} = x^{\alpha_i + \beta_j}$. Then $fg = \sum_{i,j} P_{ij}$. By compatibility, $\mu_{i1} > \mu_{i2} > \cdots > \mu_{it}$ for each row $i$.

*Invariant (H).* At line L4, for each row $i$ there is a number $j_i \in \{1, \ldots, t+1\}$ such that the products $P_{i1}, \ldots, P_{i, j_i - 1}$ have been used (each exactly once), the others have not, and the heap holds exactly one entry $(\mu_{i j_i}, i, j_i)$ for each row with $j_i \le t$, and nothing else. Line L2 sets $j_i = 1$ for all rows. One pass of the loop extracts the entry of some row $i$, uses $P_{i j_i}$ and, at line L9, inserts the entry of the next column if there is one. So (H) holds again with $j_i$ increased by 1.

*Order of extraction.* Let $M$ be the monomial extracted in some pass. Each unused product $P_{kl}$ has $l \ge j_k$, so $\mu_{kl} \le \mu_{k j_k} \le M$, because $M$ is the maximum of the heap. Every product used later is unused now, so its monomial is at most $M$. Hence the extracted monomials form a non-increasing sequence $M_1 \ge M_2 \ge \cdots \ge M_{st}$, and all products with the same monomial are extracted in consecutive passes.

*Invariant (O).* After each pass, $h$ is a list of pairs with strictly decreasing monomials; all pairs except the last have nonzero coefficient; and $h$ represents exactly the sum of the used products. Before the first pass $h$ is empty. In a pass with monomial $M$: if the last monomial of $h$ is $M$, line L7 adds the new product to it, and the sum is still right. Otherwise $M$ is smaller than the last monomial of $h$, by the order of extraction; the run of products with that last monomial is complete, so its coefficient is final, and line L8 deletes it if it is zero, which changes no sum. Then $(M, c)$ is appended, and the monomials stay strictly decreasing. So (O) holds.

*Termination and result.* Each pass uses one product and no product is used twice, so the loop runs exactly $st$ times. Then all products are used, and by (O) $h$ represents $\sum P_{ij} = fg$. The coefficient of each monomial $\mu$ in $h$ is the sum of all $P_{ij}$ with $\mu_{ij} = \mu$, which is the coefficient of $\mu$ in $fg$. Every pair except the last has a nonzero coefficient, and line L10 deletes the last if it is zero. So the output meets (D), and by Lemma 1 it is the representation of $fg$. $\square$

**Cost.** By (H) the heap has at most $s$ entries at all times. There are $st$ extractions and at most $st - s$ insertions, each with $O(\log s)$ comparisons of monomials, and $st$ coefficient products and at most $st$ additions. Swapping the factors so that $s \le t$ does not change the product, because $R$ is commutative.

**mul_term.** For a term $c x^\gamma$, the list $[(\alpha_i + \gamma, c c_i)]$ is strictly decreasing by compatibility, and it represents $c x^\gamma f$. Dropping the entries with $c c_i = 0$ gives (D). $\blacksquare$
