---
title: Under independence the Pearson statistic with expected counts from the margins tends to chi-square with (r - 1)(c - 1) degrees of freedom
proves: [correctness]
status: full
---

**Model.** $n$ independent units are classified by a row variable with $r \ge 2$ levels and a column variable with $c \ge 2$ levels. Cell $(i, j)$ has probability $\pi_{ij}$, and the counts $O_{ij}$ are multinomial. Write $R_i$ and $C_j$ for the row and column totals. The null hypothesis of independence is $\pi_{ij} = a_i b_j$ for all $i, j$, where $a_i > 0$ and $b_j > 0$ are the marginal probabilities. The expected counts are $E_{ij} = R_i C_j/n$, and

$$X^2 = \sum_{i, j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}.$$

**Claim 1 (lines L1 to L7 compute the statistic).** Line L1 forms the row totals, the column totals and $n$. Lines L2 and L3 visit every cell and form $E_{ij} = R_i C_j/n$, which is positive because the code rejects a table with an empty row or column. Line L4 adds the cell's term: $(O_{ij} - E_{ij})^2/E_{ij}$, or $(\max(0, \lvert O_{ij} - E_{ij} \rvert - \tfrac12))^2/E_{ij}$ with the Yates correction, or $2 O_{ij} \log(O_{ij}/E_{ij})$ for $G$ (zero when $O_{ij} = 0$). Line L5 sums the terms with `math.fsum`, line L6 sets $\mathrm{df} = (r - 1)(c - 1)$, and line L7 returns the upper tail $P(\chi^2_{\mathrm{df}} > X^2)$ from the regularized incomplete gamma function. $\square$

The value $E_{ij} = R_i C_j/n$ is $n \hat a_i \hat b_j$, where $\hat a_i = R_i/n$ and $\hat b_j = C_j/n$ are the maximum likelihood estimates of the margins under independence. (The log-likelihood $\sum_{ij} O_{ij} (\log a_i + \log b_j) = \sum_i R_i \log a_i + \sum_j C_j \log b_j$ separates, and each part is maximized by the observed proportions.) So the test is the goodness-of-fit test of the family $\{a_i b_j\}$, which has $(r - 1) + (c - 1)$ free parameters, fitted from the counts.

**Claim 2 (the limit law).** Under $H_0$, with $a$ and $b$ fixed and $n \to \infty$, $X^2$ converges in distribution to $\chi^2_{(r - 1)(c - 1)}$.

*Proof.* Put $\alpha_i = \sqrt{a_i}$ and $\beta_j = \sqrt{b_j}$. Then $\lVert \alpha \rVert = \lVert \beta \rVert = 1$. Treat $r \times c$ arrays as matrices and use the Frobenius norm $\lVert A \rVert^2 = \sum_{ij} A_{ij}^2$.

*Step 1: the standardized counts.* Let $\delta_{ij} = O_{ij} - n a_i b_j$ and $U_{ij} = \delta_{ij}/\sqrt{n a_i b_j}$. The cell counts are multinomial with probabilities $a_i b_j$, so the argument of the goodness-of-fit proof (the counts are a sum of $n$ iid unit vectors, and the multivariate [central limit theorem](/central-limit-theorem/) applies) gives $U \to N(0, I - u u^\top)$ in distribution, where $u = \operatorname{vec}(\alpha \beta^\top)$, a unit vector. Equivalently, $U \to Z - \langle \alpha\beta^\top, Z \rangle\, \alpha \beta^\top$ in distribution, where $Z$ is an $r \times c$ matrix of iid standard normals and $\langle A, B \rangle = \sum_{ij} A_{ij} B_{ij}$. Note $\langle \alpha\beta^\top, Z \rangle = \alpha^\top Z \beta$.

*Step 2: the residuals are a linear map of $U$.* Let $\delta_{i\cdot} = R_i - n a_i = \sum_j \delta_{ij}$ and $\delta_{\cdot j} = C_j - n b_j = \sum_i \delta_{ij}$. Then

$$E_{ij} = \frac{(n a_i + \delta_{i\cdot})(n b_j + \delta_{\cdot j})}{n} = n a_i b_j + a_i \delta_{\cdot j} + b_j \delta_{i\cdot} + \frac{\delta_{i\cdot} \delta_{\cdot j}}{n}.$$

Let $V_{ij} = (O_{ij} - E_{ij})/\sqrt{n a_i b_j}$. Dividing term by term, and using $\delta_{\cdot j}/\sqrt n = \sum_k \alpha_k \beta_j U_{kj}$ and $\delta_{i\cdot}/\sqrt n = \sum_l \alpha_i \beta_l U_{il}$,

$$V = U - \alpha \alpha^\top U - U \beta \beta^\top - W_n, \qquad W_{n, ij} = \frac{\delta_{i\cdot} \delta_{\cdot j}}{n \sqrt{n a_i b_j}}.$$

Each $\delta_{i\cdot}/\sqrt n$ and $\delta_{\cdot j}/\sqrt n$ is bounded in probability (they are linear in $U$), so $W_n = O_P(n^{-1/2})$.

*Step 3: the limit of the residuals.* Let $L(U) = U - \alpha\alpha^\top U - U \beta\beta^\top$, a fixed linear map. By Step 1, the continuous mapping theorem and Slutsky's theorem, $V \to L(U_\infty)$ in distribution with $U_\infty = Z - (\alpha^\top Z \beta)\, \alpha\beta^\top$. Write $P_\alpha = \alpha\alpha^\top$, $Q_\alpha = I - P_\alpha$, and the same for $\beta$. A direct expansion gives $L(U) = Q_\alpha U Q_\beta - P_\alpha U P_\beta$. For $U = U_\infty$:

- $P_\alpha U_\infty P_\beta = (\alpha^\top U_\infty \beta)\, \alpha\beta^\top$ and $\alpha^\top U_\infty \beta = \alpha^\top Z \beta - (\alpha^\top Z \beta) \lVert\alpha\rVert^2 \lVert\beta\rVert^2 = 0$;
- $Q_\alpha U_\infty Q_\beta = Q_\alpha Z Q_\beta - (\alpha^\top Z \beta)\, (Q_\alpha \alpha)(Q_\beta \beta)^\top = Q_\alpha Z Q_\beta$, because $Q_\alpha \alpha = 0$.

So $V \to Q_\alpha Z Q_\beta$ in distribution.

*Step 4: the law of the limit.* The map $Z \mapsto Q_\alpha Z Q_\beta$ is linear, symmetric for the inner product $\langle \cdot, \cdot \rangle$, and idempotent, so it is an orthogonal projection on the space of $r \times c$ matrices. Its range is the set of matrices whose columns are orthogonal to $\alpha$ and whose rows are orthogonal to $\beta$. Taking orthonormal bases $\alpha, g_2, \ldots, g_r$ of $\mathbb{R}^r$ and $\beta, h_2, \ldots, h_c$ of $\mathbb{R}^c$, the matrices $g_k h_l^\top$ with $k, l \ge 2$ form an orthonormal basis of that range, so it has dimension $(r - 1)(c - 1)$. As in the goodness-of-fit proof, the squared norm of the projection of a standard normal vector onto a subspace of dimension $d$ is a sum of $d$ squared iid standard normals, so $\lVert Q_\alpha Z Q_\beta \rVert^2 \sim \chi^2_{(r - 1)(c - 1)}$.

*Step 5: the statistic.* $X^2 = \sum_{ij} V_{ij}^2 \cdot n a_i b_j/E_{ij}$. By the law of large numbers, $E_{ij}/(n a_i b_j) = \hat a_i \hat b_j/(a_i b_j) \to 1$ in probability, so $X^2 = \lVert V \rVert^2 + o_P(1)$, and by Step 3, Step 4 and the continuous mapping theorem, $X^2 \to \chi^2_{(r - 1)(c - 1)}$ in distribution. $\square$

**Claim 3 (the size).** For fixed $\alpha \in (0, 1)$ the size of the test that rejects when $p \le \alpha$ tends to $\alpha$, because the limit law is continuous and the p-value is a strictly decreasing function of $X^2$. $\square$

**Claim 4 (the 2 x 2 table).** For the table with rows $(a, b)$ and $(c, d)$, row totals $r_1, r_2$, column totals $c_1, c_2$ and $n = r_1 + r_2$:

1. $X^2 = n(ad - bc)^2/(r_1 r_2 c_1 c_2)$.
2. $X^2 = z^2$, where $z = (\hat p_1 - \hat p_2)/\sqrt{\hat p (1 - \hat p)(1/r_1 + 1/r_2)}$ is the pooled two-proportion statistic, with $\hat p_1 = a/r_1$, $\hat p_2 = c/r_2$ and $\hat p = c_1/n$.
3. The Yates statistic is $n(\max(0, \lvert ad - bc \rvert - n/2))^2/(r_1 r_2 c_1 c_2)$.

*Proof.* $O_{11} - E_{11} = a - r_1 c_1/n = (a(a + b + c + d) - (a + b)(a + c))/n = (ad - bc)/n$. The margins of $O - E$ are zero, so in a $2 \times 2$ table every cell has $\lvert O_{ij} - E_{ij} \rvert = \lvert ad - bc \rvert/n$. Also $\sum_{ij} 1/E_{ij} = n\,(r_1 + r_2)(c_1 + c_2)/(r_1 r_2 c_1 c_2) = n^3/(r_1 r_2 c_1 c_2)$. Multiplying gives part 1, and with $\lvert ad - bc \rvert/n - 1/2$ in place of $\lvert ad - bc \rvert/n$ it gives part 3. For part 2, $\hat p_1 - \hat p_2 = (a r_2 - c r_1)/(r_1 r_2) = (ad - bc)/(r_1 r_2)$ and $\hat p(1 - \hat p)(1/r_1 + 1/r_2) = c_1 c_2/(n r_1 r_2)$, so $z^2 = n(ad - bc)^2/(r_1 r_2 c_1 c_2)$. $\square$

Part 1 shows that, given all four margins, $X^2$ is an increasing function of $\lvert a - r_1 c_1/n \rvert$. Given the margins, $a$ is hypergeometric under the null, so the chi-squared test of a $2 \times 2$ table approximates a two-sided [Fisher exact test](/fisher-exact-test/) that orders the tables by their distance from the expected count.

**Other sampling schemes (cited).** With the row totals fixed in advance (independent multinomial samples, one per row), the null hypothesis is that the rows have the same distribution, and $X^2$ has the same $\chi^2_{(r - 1)(c - 1)}$ limit. The same holds when both margins are fixed, by the limit of the multiple hypergeometric law. Agresti's book treats both cases. For $r = c = 2$ with fixed rows, part 2 of Claim 4 gives the limit directly from the normal limit of the two-proportion statistic.

**The G statistic.** The Taylor bound of the goodness-of-fit proof, applied with $E_{ij}$ in place of $E_i$ and $d_{ij} = O_{ij} - E_{ij} = O_P(\sqrt n)$ with $\sum_{ij} d_{ij} = 0$, gives $G - X^2 = O_P(n^{-1/2})$, so $G$ has the same limit.

**Cost.** Line L1 takes $\Theta(rc)$ additions. Lines L2 to L4 do $\Theta(1)$ work per cell, so $\Theta(rc)$ in all. The code keeps the $rc$ terms for the exact summation in line L5, so it uses $\Theta(rc)$ extra space; a running sum would use $\Theta(r + c)$ for the margins. Line L7 is one incomplete gamma evaluation.
