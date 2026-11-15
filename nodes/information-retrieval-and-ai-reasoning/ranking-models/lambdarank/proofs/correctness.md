---
title: The closed form of the swap change of NDCG, and the lambdas as a local gradient
proves: [correctness]
status: full
---

One query has $n$ documents with labels $y_i \in \{0, 1, \ldots\}$ and scores $s_i$. The ranking sorts by score, highest first, with ties to the smaller index; $r_i \in \{1, \ldots, n\}$ is the rank of document $i$. The gain is $G_i = 2^{y_i} - 1$, and for a cutoff $k$ the discount is $D(r) = 1/\log_2(r + 1)$ if $r \le k$ and $D(r) = 0$ otherwise. Then $\mathrm{DCG@}k = \sum_i G_i D(r_i)$, $\mathrm{IDCG@}k$ is the DCG@$k$ of the order by label, and $\mathrm{NDCG@}k = \mathrm{DCG@}k / \mathrm{IDCG@}k$ when $\mathrm{IDCG@}k > 0$. This is the [NDCG](/normalized-discounted-cumulative-gain/) with the gain $2^g - 1$.

For a pair with $y_i > y_j$, $|\Delta Z_{ij}|$ is the absolute change of NDCG@$k$ when documents $i$ and $j$ swap ranks and every other document keeps its rank.

**Lemma 1 (closed form).**

$$|\Delta Z_{ij}| = \frac{\left| (G_i - G_j) \left( D(r_j) - D(r_i) \right) \right|}{\mathrm{IDCG@}k}.$$

*Proof.* The swap leaves the ideal DCG and the terms of all other documents unchanged. Before the swap the two terms are $G_i D(r_i) + G_j D(r_j)$, after it $G_i D(r_j) + G_j D(r_i)$. The difference is $(G_i - G_j)(D(r_j) - D(r_i))$. Divide by $\mathrm{IDCG@}k$. $\square$

Two consequences follow. If both ranks are beyond $k$, $D(r_i) = D(r_j) = 0$ and the lambda of the pair is 0, so pairs deep in the list do not move. If $G_i = G_j$, the pair is not formed at all, since only pairs with $y_i > y_j$ enter.

**Definition (the lambdas).** With $\rho_{ij} = 1/(1 + e^{\sigma (s_i - s_j)})$, the RankNet gradient of the pair cost $\log(1 + e^{-\sigma(s_i - s_j)})$ in $s_i$ is $-\sigma \rho_{ij}$ (see the [RankNet](/ranknet/) proof). LambdaRank sets

$$\lambda_{ij} = -\sigma \rho_{ij} |\Delta Z_{ij}|, \qquad \lambda_i = \sum_{j : y_i > y_j} \lambda_{ij} - \sum_{j : y_j > y_i} \lambda_{ji}.$$

This is Equation (6) of Burges (2010), Section 4.1, written with the sign of a cost to minimize. Lines L3 to L5 of the code compute the ranks, then $\lambda_{ij}$ by Lemma 1, then $\lambda_i$. Each $\lambda_{ij}$ enters $\lambda_i$ and $\lambda_j$ with opposite signs, so the lambdas of a query sum to zero.

**Lemma 2 (the lambdas are a gradient where the ranking is fixed).** Let $U$ be the open set of score vectors with no ties and the same ranking as a given $s^0$. On $U$ the weights $|\Delta Z_{ij}|$ are constant, and the vector $(\lambda_1, \ldots, \lambda_n)$ is the gradient of

$$C_Z(s) = \sum_{(i, j) : y_i > y_j} |\Delta Z_{ij}| \log\left(1 + e^{-\sigma (s_i - s_j)}\right).$$

*Proof.* On $U$ every rank $r_i$ is constant, so by Lemma 1 every weight is constant. $C_Z$ is then a weighted RankNet cost with fixed weights, and the computation of Lemma 1 of the RankNet proof, term by term, gives $\partial C_Z / \partial s_i = \lambda_i$. $\square$

So on each region of fixed ranking, a LambdaRank step is a gradient step on a convex function of the scores, which is the observation of Burges (2010), Section 4.3. At the boundary of the regions, where two scores tie, the weights jump, and no single function has the lambdas as its gradient everywhere.

**What the lambdas are not.** NDCG@$k$ is constant on each region $U$, so its gradient in $s$ is zero wherever it exists. The lambdas are therefore not the gradient of NDCG. The claim that steps along the lambdas raise NDCG is supported by experiments, which Burges (2010) calls empirical. Wang et al. (2018) later placed LambdaRank in a framework of well-defined losses and described it as the minimization of a coarse upper bound on an NDCG-based cost; that analysis is not repeated here.

The tests in `impl/python/test_lambdarank.py` check, on 200 random queries with several $\sigma$ and $k$, that each $\lambda_{ij}$ equals a finite-difference RankNet gradient times the NDCG change of the swap computed by sorting the swapped list. They also check Lemma 1 against the direct swap, Lemma 2 against finite differences of $C_Z$, the zero lambdas below the cutoff, the zero sum, and the worked example of the page. The rise of NDCG during training is measured on one planted set and is not a theorem.
