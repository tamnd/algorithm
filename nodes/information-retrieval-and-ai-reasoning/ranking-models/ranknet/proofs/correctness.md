---
title: The RankNet gradient factorizes into lambdas, and gradient descent with step 1/L never increases the cost
proves: [correctness]
status: full
---

Fix $\sigma > 0$. A query has documents with feature vectors $x_1, \ldots, x_n$ and integer labels $y_1, \ldots, y_n$. The scores are $s_i = w \cdot x_i$. Let $\mathcal P = \{(i, j) : y_i > y_j\}$ be the preferred pairs of the query. The cost of the query is

$$C(w) = \sum_{(i, j) \in \mathcal P} \log\left(1 + e^{-\sigma (s_i - s_j)}\right),$$

and the cost of a training set is the sum over its queries. This is the cross-entropy of Burges et al. (2005) with the target probability $\bar P_{ij} = 1$, since $-\log P_{ij} = \log(1 + e^{-\sigma o_{ij}})$ for $P_{ij} = 1/(1 + e^{-\sigma o_{ij}})$ and $o_{ij} = s_i - s_j$.

**Lemma 1 (the lambdas).** Let $\lambda_{ij} = -\sigma / (1 + e^{\sigma (s_i - s_j)})$ for $(i, j) \in \mathcal P$, and

$$\lambda_i = \sum_{j : (i, j) \in \mathcal P} \lambda_{ij} - \sum_{j : (j, i) \in \mathcal P} \lambda_{ji}.$$

Then $\partial C / \partial s_i = \lambda_i$ and $\nabla_w C = \sum_i \lambda_i x_i$.

*Proof.* The term of the pair $(i, j)$ depends on $s$ only through $o = s_i - s_j$. With $c(o) = \log(1 + e^{-\sigma o})$, $c'(o) = -\sigma e^{-\sigma o} / (1 + e^{-\sigma o}) = -\sigma / (1 + e^{\sigma o})$. So the pair adds $c'(o) = \lambda_{ij}$ to $\partial C / \partial s_i$ and $-c'(o) = -\lambda_{ij}$ to $\partial C / \partial s_j$. Summing over the pairs gives $\partial C / \partial s_i = \lambda_i$. The chain rule with $\partial s_i / \partial w = x_i$ gives the second claim. $\square$

In the code, lines L4 and L5 add $\lambda_{ij}$ to document $i$ and subtract it from document $j$, and line L6 forms $\sum_i \lambda_i x_i$. The cost of one gradient is one pass over the pairs for the lambdas and one pass over the documents for the sum, in place of one vector operation per pair. This is the factorization of Burges (2010), Section 2.1.

**Lemma 2.** The lambdas of one query sum to zero.

*Proof.* Each $\lambda_{ij}$ enters $\lambda_i$ with the sign $+$ and $\lambda_j$ with the sign $-$, and no other lambda. $\square$

**Lemma 3 (convex and smooth).** For the linear model, $C$ is convex in $w$, and its Hessian satisfies $0 \preceq \nabla^2 C \preceq L I$ with

$$L = \frac{\sigma^2}{4} \sum_{(i, j) \in \mathcal P} \lVert x_i - x_j \rVert^2,$$

summed over all queries.

*Proof.* With $z = x_i - x_j$, the pair term is $c(w \cdot z)$ and $c''(o) = \sigma^2 p (1 - p)$ with $p = 1 / (1 + e^{\sigma o})$. So the Hessian of the term is $\sigma^2 p (1 - p) z z^\top$. It is positive semidefinite, and since $p (1 - p) \le 1/4$ and $z z^\top \preceq \lVert z \rVert^2 I$, it is at most $(\sigma^2/4) \lVert z \rVert^2 I$. Sum over the pairs. $\square$

**Theorem (monotone descent).** Let $w_{t+1} = w_t - \frac{1}{L} \nabla C(w_t)$, as in line L7 with $\eta = 1/L$. Then

$$C(w_{t+1}) \le C(w_t) - \frac{1}{2L} \lVert \nabla C(w_t) \rVert^2.$$

*Proof.* By Lemma 3 and Taylor's theorem with the integral remainder, $C(v) \le C(w) + \nabla C(w) \cdot (v - w) + \frac{L}{2} \lVert v - w \rVert^2$ for all $w, v$. Put $w = w_t$ and $v = w_t - \nabla C(w_t)/L$. $\square$

So the cost never increases, and since $C \ge 0$, $\sum_t \lVert \nabla C(w_t) \rVert^2 \le 2 L\, C(w_0)$, so the gradients tend to zero. If $L = 0$, every preferred pair has $x_i = x_j$, the cost is the constant $|\mathcal P| \log 2$, and the code returns $w = 0$.

**Remark (no minimizer).** If some $u$ has $u \cdot (x_i - x_j) > 0$ for every preferred pair, then $C(t u) \to 0$ as $t \to \infty$ while $C > 0$ everywhere. The infimum is not attained and $\lVert w_t \rVert$ grows without bound. The theorem still holds, but the iterates do not converge. A target $\bar P_{ij} < 1$ or a weight penalty gives a minimizer.

**What is not proved.** The theorem is about the pairwise cost. A smaller cost does not imply a larger NDCG, and nothing here bounds the error on new queries. The tests measure NDCG before and after training on one planted set and nothing more.

The tests in `impl/python/test_ranknet.py` check Lemma 1 against central finite differences of $C$, the factorized gradient against the pair-by-pair gradient, Lemma 2, the theorem along 200 steps, and the worked example of the page.
