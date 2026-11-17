---
title: Each round of EM computes the exact posterior of the phase, never lowers the likelihood, and its fixed points are stationary points
proves: [correctness]
status: full
---

**Setting.** Individuals $i = 1, \ldots, n$ have genotypes $g_i \in \{0, 1, 2\}^m$. The unobserved complete data are the ordered haplotype pairs $(X_i, Y_i)$, independent over $i$, with $X_i$ and $Y_i$ independent draws from $p$ on $\{0, 1\}^m$. We observe $g_i = X_i + Y_i$. Write $S_i = S(g_i)$ for the set of unordered pairs $\{h, h'\}$ with $h + h' = g_i$, and $w(h, h') = 1$ if $h = h'$, else 2. Let $H$ be the set of haplotypes that occur in some $S_i$.

**Lemma 1 (enumeration).** If $g$ has $k \ge 1$ heterozygous sites, then $|S(g)| = 2^{k-1}$, and every pair in $S(g)$ has $h \ne h'$. If $k = 0$, then $S(g)$ has the one pair $\{h, h\}$ with $h_j = g_j / 2$.

*Proof.* At a site with $g_j \in \{0, 2\}$, both haplotypes have the allele $g_j / 2$. At a heterozygous site, one haplotype has 0 and the other 1. An ordered pair is fixed by the choice, at each of the $k$ heterozygous sites, of which haplotype has 1: $2^k$ ordered pairs. When $k \ge 1$, the two haplotypes differ at a heterozygous site, so each unordered pair comes from exactly two ordered pairs. Fixing allele 0 on the first haplotype at the first heterozygous site picks one of the two, which is how the code lists them. $\square$

**Lemma 2 (E-step).** For $\{h, h'\} \in S_i$, $P(\{X_i, Y_i\} = \{h, h'\} \mid g_i, p) = w(h, h') p_h p_{h'} / P_i$ with $P_i = \sum_{\{u, u'\} \in S_i} w(u, u') p_u p_{u'}$.

*Proof.* The event $\{X_i, Y_i\} = \{h, h'\}$ is the union of the ordered events $(h, h')$ and $(h', h)$, which are the same event when $h = h'$. Its probability is $w(h, h') p_h p_{h'}$. These events for the pairs of $S_i$ are disjoint, and their union is the event $X_i + Y_i = g_i$, so $P(g_i \mid p) = P_i$. Bayes' rule gives the ratio. $\square$

So line L7 adds to $c_h$ the posterior expected number of copies of $h$ carried by individual $i$: one copy for each side of the pair, and two copies when $h = h'$. After line L5, $c_h = E[N_h \mid g, p]$, where $N_h$ is the number of the $2n$ haplotypes equal to $h$, and $\sum_h c_h = 2n$.

**Lemma 3 (M-step).** Define $Q(q \mid p) = E[\ln P(X, Y \mid q) \mid g, p] = \sum_{h \in H} c_h \ln q_h$. Over the simplex on $H$, $Q(\cdot \mid p)$ has its maximum at $q_h = c_h / (2n)$.

*Proof.* The complete-data log-likelihood is $\sum_i (\ln q_{X_i} + \ln q_{Y_i}) = \sum_h N_h \ln q_h$, and its conditional mean is the formula. Let $r_h = c_h / (2n)$. For any $q$ on the simplex, $Q(r \mid p) - Q(q \mid p) = 2n \sum_h r_h \ln(r_h / q_h) \ge 0$, since the sum is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of $r$ from $q$, which is non-negative by Gibbs' inequality. $\square$

**Theorem 1 (ascent).** If $p'$ is the result of lines L4 to L8 from $p$, then $\ell(p') \ge \ell(p)$, with equality only if $p' = p$ or the posterior of the phase is the same under $p$ and $p'$.

*Proof.* For each $i$ and each $q$ with $P(g_i \mid q) > 0$, write $\ln P(g_i \mid q) = E[\ln P(X_i, Y_i \mid q) \mid g_i, p] - E[\ln P(X_i, Y_i \mid g_i, q) \mid g_i, p]$, which holds because $P(x, y \mid q) = P(g_i \mid q) P(x, y \mid g_i, q)$ for every $(x, y)$ compatible with $g_i$. Summing over $i$, $\ell(q) = Q(q \mid p) - R(q \mid p)$, where $R(q \mid p)$ is the expected log of the conditional law of the phase under $q$. By Gibbs' inequality, $R(q \mid p) \le R(p \mid p)$, with equality only when the two conditional laws agree. So $\ell(p') - \ell(p) = [Q(p' \mid p) - Q(p \mid p)] + [R(p \mid p) - R(p' \mid p)] \ge 0$, where the first bracket is non-negative by Lemma 3. $\square$

**Corollary (convergence of the values).** Each $P(g_i \mid p) \le 1$, so $\ell \le 0$. The values $\ell(p^{(t)})$ do not decrease and are bounded above, so they converge. This shows the stopping rule of line L9 is met after a finite number of rounds for every $\varepsilon > 0$. It does not show that the limit is the global maximum.

**Theorem 2 (fixed points).** Let $p$ be a fixed point with $p_h > 0$ for all $h \in H$. Then $\partial \ell / \partial p_h = 2n$ for every $h \in H$, so $p$ is a stationary point of $\ell$ on the simplex (the Lagrange condition with multiplier $2n$). If some $p_h = 0$ at a fixed point, that coordinate stays 0 forever.

*Proof.* Differentiate: $\partial P_i / \partial p_h = \sum_{\{h, h'\} \in S_i} w(h, h') p_{h'} \cdot (1 + [h = h'])$, which counts each copy of $h$ in the pair. Then $p_h \, \partial \ell / \partial p_h = \sum_i \sum_{\{h, h'\} \in S_i} (1 + [h = h'])\, w(h, h') p_h p_{h'} / P_i = c_h$ by Lemma 2. At a fixed point, $c_h = 2n p_h$, so $\partial \ell / \partial p_h = 2n$ when $p_h > 0$. If $p_h = 0$, every term of $c_h$ has the factor $p_h$, so $c_h = 0$ and the next value is 0 again. $\square$

**Lemma 4 (allele frequencies).** After one round, $\sum_{h : h_j = 1} p'_h = \frac{1}{2n} \sum_i g_{ij}$ for every site $j$.

*Proof.* Each pair $\{h, h'\}$ in $S_i$ has $h_j + h'_j = g_{ij}$, so it adds $e \cdot g_{ij}$ copies of allele 1 at site $j$ to the counts. The posteriors $e$ of the pairs of individual $i$ sum to 1 by Lemma 2, so individual $i$ adds exactly $g_{ij}$ copies. Line L8 divides by $2n$. $\square$

**Phase-known case.** If every $g_i$ has at most one heterozygous site, Lemma 1 gives $|S_i| = 1$ for all $i$. Then $c_h$ is the number of copies of $h$ in the known pairs, and Lemma 3 says that this count over $2n$ is the maximum of the full likelihood, which now equals the complete-data likelihood. So EM stops at the maximum likelihood estimate after one round.
