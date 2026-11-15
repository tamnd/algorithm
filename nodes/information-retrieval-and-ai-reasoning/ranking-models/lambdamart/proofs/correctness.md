---
title: The LambdaMART targets, weights and leaf values are the derivatives and the diagonal Newton step of the frozen lambda cost
proves: [correctness]
status: full
---

Fix $\sigma > 0$ and a cutoff $k$. For one query with labels $y$ and current scores $s = F(x)$, let $|\Delta Z_{ij}|$ be the absolute change of NDCG@$k$ when documents $i$ and $j$ swap ranks, for each pair with $y_i > y_j$. The [LambdaRank](/lambdarank/) proof gives its closed form. Freeze these weights at the current ranking and define

$$C(s) = \sum_{(i, j) : y_i > y_j} |\Delta Z_{ij}| \log\left(1 + e^{-\sigma (s_i - s_j)}\right), \qquad \rho_{ij} = \frac{1}{1 + e^{\sigma (s_i - s_j)}}.$$

The cost of a round is the sum of $C$ over the queries. The code computes, for each document,

$$g_i = \sum_{j : y_i > y_j} \sigma |\Delta Z_{ij}| \rho_{ij} - \sum_{j : y_j > y_i} \sigma |\Delta Z_{ji}| \rho_{ji}, \qquad h_i = \sum_{\text{pairs } p \ni i} \sigma^2 |\Delta Z_p| \rho_p (1 - \rho_p).$$

**Lemma 1 (targets and weights).** $g_i = -\partial C / \partial s_i$ and $h_i = \partial^2 C / \partial s_i^2$. So $g_i = -\lambda_i$ for the LambdaRank lambdas $\lambda_i$.

*Proof.* Let $c(o) = \log(1 + e^{-\sigma o})$ with $o = s_i - s_j$. Then $c'(o) = -\sigma \rho$ and $c''(o) = \sigma^2 \rho (1 - \rho)$, because $d\rho / do = -\sigma \rho (1 - \rho)$. The pair term $v\, c(s_i - s_j)$, with $v = |\Delta Z_{ij}|$, has the derivative $-\sigma v \rho$ in $s_i$ and $+\sigma v \rho$ in $s_j$, and the second derivative $\sigma^2 v \rho (1 - \rho)$ in each of $s_i$ and $s_j$. Lines L3 and L4 add exactly these amounts, with the sign of $g$ reversed. $\square$

Burges (2010), Section 7, writes $y_i = \lambda_i$ and $w_i = \partial y_i / \partial F$ for a utility to be maximized. The code uses a cost to be minimized, so its target is $g_i = -\lambda_i$ and its weight $h_i$ is positive. The two conventions give the same step.

**Lemma 2 (leaf value).** Let a tree send the set $R$ of documents to one leaf. Line L6 sets

$$\gamma_R = \frac{\sum_{i \in R} g_i}{\sum_{i \in R} h_i},$$

and $\gamma_R = 0$ when the denominator is 0. This is the value $\gamma$ that minimizes the quadratic model

$$q_R(\gamma) = C(s) - \gamma \sum_{i \in R} g_i + \frac{\gamma^2}{2} \sum_{i \in R} h_i,$$

which is the second-order Taylor model of $C$ along the move $s_i \leftarrow s_i + \gamma$ for $i \in R$ with the mixed second derivatives dropped.

*Proof.* $q_R$ is a parabola with positive leading coefficient when $\sum_R h_i > 0$, and its derivative $-\sum_R g_i + \gamma \sum_R h_i$ vanishes at $\gamma_R$. The first-order term is exact by Lemma 1. The exact second derivative of $\gamma \mapsto C(s + \gamma \mathbf 1_R)$ at 0 is $\sum_{i, l \in R} \partial^2 C / \partial s_i \partial s_l$, and $q_R$ keeps only the terms with $i = l$. $\square$

When both documents of a pair are in $R$, moving them together does not change $s_i - s_j$, so the exact one-dimensional Newton step would not count the pair at all, while $\sum_R h_i$ counts it twice. The leaf value of Burges's formula is therefore a diagonal Newton step, as in MART, and not the exact Newton step on the leaf. In the worked example of the page, the leaf $\{0, 1\}$ gets $\gamma = 3.1196$, while the exact step would be $4.2863$; the leaf $\{2, 3\}$ has no pair inside it and both values are $-4.2863$. A denominator of 0 means that no document of the leaf is in a pair with a nonzero weight, so $g_i = 0$ on the leaf and $\gamma = 0$ is the only sensible value.

**Lemma 3 (the split).** For one node with the document set $I$, line L5 returns the split $(f, \theta)$ that minimizes, over all features $f$ and all thresholds $\theta$ that split $I$ into two nonempty parts, the sum of squared errors of the targets $g$ around the mean of each part.

*Proof.* A threshold $\theta$ splits $I$ into $\{x_f \le \theta\}$ and $\{x_f > \theta\}$, and this partition depends only on which consecutive pair of distinct values of $x_f$ in $I$ the threshold falls between. The code tries one threshold, the midpoint, for each such pair, so it tries every distinct nonempty partition by a threshold, and keeps the one of least error. The depth-2 tree applies the same rule to each child. $\square$

**Lemma 4 (scale).** If $\sigma$ is multiplied by $c > 0$, every $g_i$ is multiplied by $c$ times a factor that depends on $c$ only through $\rho$, and every $h_i$ by $c^2$ times such a factor. At $s = 0$, where $\rho = 1/2$ for every pair, $\gamma_R$ is exactly divided by $c$.

*Proof.* Read the factors off the definitions of $g_i$ and $h_i$. $\square$

This is the $1/\sigma$ scaling that Burges (2010) mentions for the leaf values.

**What is not proved.** Each round reduces the frozen cost $C$ only approximately: the tree is fitted by least squares, the step is a diagonal Newton step, the shrinkage $\eta$ scales it, and the weights $|\Delta Z|$ change once the ranking changes. Nothing here shows that NDCG rises, and nothing bounds the error on new queries. The rise of NDCG in the tests is measured on one planted set.

The tests in `impl/python/test_lambdamart.py` check Lemma 1 against central finite differences of the frozen cost on 100 random queries, the leaf values of a fitted depth-2 tree against the ratio of the finite-difference derivatives summed over each leaf, Lemma 3 against a brute force over all thresholds, a query with one label value, and the worked example of the page.
