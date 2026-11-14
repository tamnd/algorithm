---
title: Two-way ANOVA sums of squares are differences of nested residual sums of squares with exact F laws, orthogonal in balanced layouts
proves: [correctness, termination]
status: full
---

We prove that each sum of squares the code returns is the squared length of a projection, that each F statistic has an exact F law under the hypothesis that this projection of the mean is zero, that the three types coincide in balanced layouts, and that in unbalanced layouts they test different hypotheses. Factor A has levels $i = 1, \dots, a$, factor B has levels $j = 1, \dots, b$, and cell $(i, j)$ holds $n_{ij} \ge 1$ observations, $N = \sum n_{ij}$. The model is $y_{ijl} = \mu_{ij} + e_{ijl}$ with iid $N(0, \sigma^2)$ errors. For a set $S$ of columns, $V(S)$ is their span in $\mathbb R^N$, $P_S$ its orthogonal projection, and $RSS(S) = \|(I - P_S)y\|^2$.

**Lemma 1 (nested differences).** If $V(S) \subset V(L)$, then $RSS(S) - RSS(L) = \|(P_L - P_S)y\|^2$, and $P_L - P_S$ is the orthogonal projection onto $V(L) \ominus V(S)$, of rank $\dim V(L) - \dim V(S)$.

*Proof.* $P_LP_S = P_SP_L = P_S$ because $V(S) \subset V(L)$. So $P_L - P_S$ is symmetric and idempotent. By Pythagoras, $\|(I - P_S)y\|^2 = \|(I - P_L)y\|^2 + \|(P_L - P_S)y\|^2$, since $(I - P_L)y$ and $(P_L - P_S)y$ are orthogonal ($(I - P_L)(P_L - P_S) = 0$). $\square$

**Lemma 2 (exact F law).** Let $F$ denote the full model: the intercept, the $a - 1$ effect columns of A, the $b - 1$ of B and their $(a-1)(b-1)$ products, with $p = ab$ columns. Every cell holds data, so these columns are linearly independent and $V(F)$ is the set of vectors that are constant on each cell. For nested $V(S) \subset V(L) \subset V(F)$ with $d = \dim V(L) - \dim V(S)$, the statistic

$$\frac{(RSS(S) - RSS(L))/d}{RSS(F)/(N - ab)}$$

has the $F_{d, N - ab}$ law whenever $(P_L - P_S)\mu = 0$, where $\mu$ is the vector of cell means $\mu_{ij}$.

*Proof.* $\mu \in V(F)$, so $(I - P_F)\mu = 0$. $(P_L - P_S)(I - P_F) = 0$ because both $P_L$ and $P_S$ project into $V(F)$. Lemma 2 of the [one-way ANOVA](/one-way-anova/) proof (projections of a normal vector) gives independent $\chi^2_d$ and $\chi^2_{N-ab}$ laws after division by $\sigma^2$. $\square$

The code (L3 to L6) computes exactly these differences: type I uses the chain $\{1\} \subset \{1, A\} \subset \{1, A, B\}$, type II compares $\{1, B\}$ with $\{1, A, B\}$ for A and $\{1, A\}$ with $\{1, A, B\}$ for B, type III compares $\{1, B, AB\}$ with the full model for A, and the interaction compares $\{1, A, B\}$ with the full model. The residual sums of squares come from modified Gram-Schmidt with reorthogonalization: the residual of $y$ after subtracting its components along an orthonormal basis of $V(S)$ is $(I - P_S)y$.

**Lemma 3 (what type III tests).** With the sum-to-zero (effect) coding, the type III hypothesis for A, $(P_F - P_{\{1,B,AB\}})\mu = 0$, is $\bar\mu_{1\cdot} = \dots = \bar\mu_{a\cdot}$, where $\bar\mu_{i\cdot} = \frac1b\sum_j\mu_{ij}$ is the unweighted mean of the cell means of row $i$.

*Proof.* Every vector of cell means can be written uniquely as $\mu_{ij} = m + \alpha_i + \beta_j + \gamma_{ij}$ with $\sum_i\alpha_i = 0$, $\sum_j\beta_j = 0$ and $\sum_i\gamma_{ij} = \sum_j\gamma_{ij} = 0$: take $m = \bar\mu_{\cdot\cdot}$, $\alpha_i = \bar\mu_{i\cdot} - \bar\mu_{\cdot\cdot}$, $\beta_j = \bar\mu_{\cdot j} - \bar\mu_{\cdot\cdot}$ and $\gamma_{ij}$ the rest. The effect columns of A, B and AB span exactly the vectors of the forms $\alpha_i$, $\beta_j$ and $\gamma_{ij}$ with these constraints, by the coding. So the full model has $\mu$ in it with unique coefficients, and $\mu \in V(\{1, B, AB\})$ if and only if $\alpha = 0$. Because $V(\{1, B, AB\}) \subset V(F)$ and $\mu \in V(F)$, $(P_F - P_{\{1,B,AB\}})\mu = 0$ holds if and only if $\mu \in V(\{1, B, AB\})$, that is if and only if every $\alpha_i = \bar\mu_{i\cdot} - \bar\mu_{\cdot\cdot}$ is 0. $\square$

With treatment (0/1) coding the columns of B and AB span a different subspace, and the same comparison tests the A differences at the last level of B only. The test file shows that the two codings give different "type III" sums of squares on the same data. Type II for A, by contrast, is the same for every coding, because it depends only on the subspaces $V(\{1, A, B\})$ and $V(\{1, B\})$; its hypothesis is "no A effect" in the additive model, and in general it is a weighted hypothesis on the cell means whose weights depend on the $n_{ij}$.

**Lemma 4 (balanced layouts are orthogonal).** If $n_{ij} = n$ for every cell, then $\mathbb R^N$ is the orthogonal sum $V_0 \oplus V_A \oplus V_B \oplus V_{AB} \oplus V_E$, where $V_0$ holds the constant vectors, $V_A$ the vectors $v_{ijl} = \alpha_i$ with $\sum\alpha_i = 0$, $V_B$ the vectors $\beta_j$ with $\sum\beta_j = 0$, $V_{AB}$ the vectors $\gamma_{ij}$ with zero row and column sums, and $V_E$ the vectors with zero sum in every cell. So for every term the type I (in either order), type II and type III sums of squares are all equal to the squared length of the projection onto that term's own subspace:

$$SS_A = bn\sum_i(\bar y_{i\cdot\cdot} - \bar y)^2, \quad SS_B = an\sum_j(\bar y_{\cdot j\cdot} - \bar y)^2, \quad SS_{AB} = n\sum_{i,j}(\bar y_{ij\cdot} - \bar y_{i\cdot\cdot} - \bar y_{\cdot j\cdot} + \bar y)^2,$$

and $SSE = \sum(y_{ijl} - \bar y_{ij\cdot})^2$.

*Proof.* Inner products: $\langle\alpha, \beta\rangle = \sum_{i,j,l}\alpha_i\beta_j = n\sum_i\alpha_i\sum_j\beta_j = 0$. $\langle\alpha, \gamma\rangle = n\sum_i\alpha_i\sum_j\gamma_{ij} = 0$, and $\langle\beta, \gamma\rangle = 0$ the same way. The constant vector is orthogonal to $V_A$, $V_B$ and $V_{AB}$ because their entries sum to $n$ times a zero sum. Every vector of $V_0$, $V_A$, $V_B$ and $V_{AB}$ is constant on cells, and a vector of $V_E$ sums to zero on each cell, so $V_E$ is orthogonal to the other four. The dimensions $1 + (a-1) + (b-1) + (a-1)(b-1) + (N - ab)$ add up to $N$, so the sum is all of $\mathbb R^N$. The span of the effect columns of A is $V_A$, and similarly for B and AB. Every model in Lemma 2 is a sum of some of $V_0, V_A, V_B, V_{AB}$, and for orthogonal subspaces $P_{U \oplus W} = P_U + P_W$. So each difference $P_L - P_S$ is the projection onto the one subspace that $L$ adds, whatever else is in the model. The closed forms are the projections: the projection onto $V_A$ is $\bar y_{i\cdot\cdot} - \bar y$ at every unit of row $i$, and so on. $\square$

**Lemma 5 (unbalanced layouts are not orthogonal).** In general the types differ. In the 2 x 2 layout with cells $(1,1) = \{3, 5\}$, $(1,2) = \{7\}$, $(2,1) = \{6\}$ and $(2,2) = \{10, 12, 11\}$:

- type I with A first: $SS_A = 1083/28$, $SS_{B|A} = 1587/68$;
- type I with B first: $SS_B = 1024/21$, $SS_{A|B} = 676/51$;
- type II: $SS_A = 676/51$, $SS_B = 1587/68$;
- type III: $SS_A = 216/17$, $SS_B = 384/17$;
- the interaction: $24/17$ in every type, and $SSE = 4$ on 3 degrees of freedom.

*Proof.* These are exact rational computations of the residual sums of squares of the nested models by the normal equations, done in the test file with `fractions.Fraction`; the code's floating point values agree to $10^{-9}$. For type III, Lemma 3 gives a closed form to compare with. The row marginal contrast is $\hat\psi = \frac12(\bar y_{11} + \bar y_{12}) - \frac12(\bar y_{21} + \bar y_{22}) = \frac12(4 + 7) - \frac12(6 + 11) = -3$, with variance $\sigma^2\sum c^2/n = \sigma^2\cdot\frac14(\frac12 + 1 + 1 + \frac13) = \frac{17}{24}\sigma^2$. The sum of squares of a one degree of freedom hypothesis is $\hat\psi^2/(\sum c^2/n) = 9 \cdot 24/17 = 216/17$, which matches. The A columns and the B columns are not orthogonal after the constant is removed, because the cell counts are not proportional, so the sum of squares of A depends on whether B is in the model. $\square$

The order of the type I chain matters, but each chain still adds up: $1083/28 + 1587/68 = 1024/21 + 676/51$, since both equal $RSS(\{1\}) - RSS(\{1, A, B\})$.

**Termination.** Each residual sum of squares orthogonalizes at most $ab$ columns of length $N$ against each other, two passes each, and the code computes at most five of them. So it stops after $O(N(ab)^2)$ arithmetic operations. The F tails stop as in the one-way proof.

**Theorem.** For a two-way layout with every cell nonempty and $N > ab$, the code returns for each term the difference of residual sums of squares of the two nested models named by the chosen type, and each F statistic has the exact $F_{d, N-ab}$ law under the normal model when the corresponding projection of the cell means is zero. In balanced layouts the three types coincide and equal the classical closed forms; in unbalanced layouts they test different hypotheses, and type III with effect coding tests equal unweighted marginal means.

*Proof.* Lemmas 1 to 5. $\blacksquare$
