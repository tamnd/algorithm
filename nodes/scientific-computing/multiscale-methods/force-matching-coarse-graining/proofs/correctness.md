---
title: Force matching returns the least squares fit, and in expectation the projection of the mean force
proves: [correctness]
status: full
---

Setup. The basis has $K$ hat functions $\phi_1, \dots, \phi_K$, and the CG pair force is $f_c(r) = \sum_k c_k \phi_k(r)$. There are $T$ configurations $R^{(t)}$ of $N$ sites, with reference forces $F^{(t)}$ (one number per site and Cartesian component). The force residual is $\chi^2(c) = \sum_t \sum_{i, \alpha} (F_{i \alpha}(R^{(t)}; c) - F^{(t)}_{i \alpha})^2$, where $F_{i}(R; c) = \sum_{j \ne i} f_c(r_{ij}) e_{ij}$ and $e_{ij} = (x_i - x_j) / r_{ij}$ with the minimum image. We assume exact arithmetic.

**Lemma 1 (the design rows).** For each configuration, site $i$ and component $\alpha$, the row $a$ built by line L3 satisfies $a \cdot c = F_{i \alpha}(R; c)$ for every $c$.

*Proof.* $F_{i \alpha}(R; c) = \sum_{j \ne i} \sum_k c_k \phi_k(r_{ij}) (e_{ij})_\alpha = \sum_k c_k \sum_{j \ne i} \phi_k(r_{ij}) (e_{ij})_\alpha$. So the row is $a_k = \sum_{j \ne i} \phi_k(r_{ij}) (e_{ij})_\alpha$. The code visits each unordered pair $\{i, j\}$ once, adds $\phi_k(r_{ij}) (e_{ij})_\alpha$ to the row of $i$ and subtracts it from the row of $j$. Since $e_{ji} = -e_{ij}$ and $r_{ji} = r_{ij}$, the row of $j$ gets $\phi_k(r_{ji}) (e_{ji})_\alpha$, the right term. Distances outside $[r_0, r_c]$ give $\phi_k = 0$ for all $k$ and add nothing. $\square$

Stack all rows into a matrix $A$ with $TN d$ rows ($d = 2$) and the reference forces into a vector $F$. By Lemma 1, $\chi^2(c) = \lVert A c - F \rVert^2$.

**Lemma 2 (the normal equations).** After the loop of lines L2 to L5, $G = A^T A$ and $b = A^T F$.

*Proof.* $A^T A = \sum_{\text{rows } a} a a^T$ and $A^T F = \sum_{\text{rows}} a f$, where $f$ is the reference force of the row. Line L5 adds $a_p a_q$ to $G_{pq}$ and $a_p f$ to $b_p$ for every row and every $p$ with $a_p \ne 0$. The skipped terms have $a_p = 0$, so they are zero. $\square$

**Lemma 3 (the minimizer).** $\chi^2$ is a convex quadratic with gradient $2 (A^T A c - A^T F)$. So $c$ minimizes $\chi^2$ if and only if $G c = b$. If the columns of $A$ are linearly independent, $G$ is positive definite and the minimizer is unique.

*Proof.* $\chi^2(c + h) = \chi^2(c) + 2 h^T (A^T A c - A^T F) + \lVert A h \rVert^2$. If $G c = b$, the middle term is zero for every $h$, and $\chi^2(c + h) \ge \chi^2(c)$. If $G c \ne b$, take $h = -s (G c - b)$ with a small $s > 0$; the middle term is $-2 s \lVert G c - b \rVert^2$ and the last term is $O(s^2)$, so $\chi^2$ decreases. If the columns are independent, $h^T G h = \lVert A h \rVert^2 > 0$ for $h \ne 0$. $\square$

**Lemma 4 (unused basis functions).** If no distance in the data falls in the support of $\phi_p$, then column $p$ of $A$ is zero, row and column $p$ of $G$ are zero, and $b_p = 0$. Lines L6 and L7 then return $c_p = 0$, and the other coefficients solve the normal equations of the reduced problem without $\phi_p$.

*Proof.* Column $p$ of $A$ is zero, so $G_{pq} = G_{qp} = 0$ for all $q$ and $b_p = 0$. After line L6 sets $G_{pp} = 1$, equation $p$ reads $c_p = 0$, and $c_p$ appears in no other equation. $\chi^2$ does not depend on $c_p$, so the choice $c_p = 0$ keeps the minimum. $\square$

**Theorem (correctness).** If the columns of $A$ that are not zero are linearly independent, line L7 returns the unique minimizer of $\chi^2$ with $c_p = 0$ for every unused basis function. In particular, if the reference forces are $F = A c^*$ for some $c^*$ (the true pair force lies in the basis), the result is $c^*$ on the used basis functions. If the used columns are dependent, $G$ is singular and scimat.solve raises ValueError.

*Proof.* Lemmas 1 to 4. For $F = A c^*$, $\chi^2(c^*) = 0$, so $c^*$ is a minimizer, and by uniqueness it is the result. $\square$

**Lemma 5 (what the fit approximates).** Let the configurations be samples of a random coarse configuration $R$ with reference forces $F$, with $\mathbb{E} \lVert F \rVert^2 < \infty$, and let $\bar F(R) = \mathbb{E}[F \mid R]$. Then for every $c$,
$$\mathbb{E} \lVert A(R) c - F \rVert^2 = \mathbb{E} \lVert F - \bar F(R) \rVert^2 + \mathbb{E} \lVert A(R) c - \bar F(R) \rVert^2 .$$
So the minimizer of the expected residual is the least squares projection of the conditional mean force $\bar F$ onto the span of the basis forces, and the first term, the part of the force that the coarse configuration does not determine, cannot be fitted by any $c$.

*Proof.* Write $A c - F = (A c - \bar F) + (\bar F - F)$ and expand the square. The cross term is $2 \mathbb{E}[(A(R) c - \bar F(R))^T (\bar F(R) - F)]$. Condition on $R$: the first factor is fixed, and $\mathbb{E}[\bar F(R) - F \mid R] = 0$. So the cross term is zero. $\square$

Remark. Noid et al. (2008) show that, when the map from atoms to sites and the site masses satisfy their consistency conditions and the samples come from the canonical ensemble of the atomistic model, $\bar F(R)$ is the force of the many-body potential of mean force, $-\nabla_R W(R)$. With Lemma 5 this gives the statement that force matching projects the many-body mean force onto the pair basis. The identification of $\bar F$ with $-\nabla W$ is taken from that paper and is not proved here. With finitely many samples, $\chi^2 / T$ converges to the expected residual by the law of large numbers, so the fitted $c$ converges to the minimizer of Lemma 5 when that minimizer is unique. $\blacksquare$
