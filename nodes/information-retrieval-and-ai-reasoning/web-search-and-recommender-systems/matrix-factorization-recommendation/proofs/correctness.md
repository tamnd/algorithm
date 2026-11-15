---
title: The SGD step of matrix factorization is a scaled gradient step on one term of the regularized objective
proves: [correctness]
status: full
---

The notation is that of the page: $K$ is the set of known ratings, $s = |K|$, $\hat r_{ui} = \mu + b_u + b_i + p_u^\top q_i$, $e_{ui} = r_{ui} - \hat r_{ui}$, and $\theta$ is the vector of all parameters $b_u, b_i, p_u, q_i$, with $\mu$ fixed by line L1. For $(u, i) \in K$ let

$$\ell_{ui}(\theta) = e_{ui}^2 + \lambda \bigl( b_u^2 + b_i^2 + \lVert p_u \rVert^2 + \lVert q_i \rVert^2 \bigr), \qquad J(\theta) = \sum_{(u, i) \in K} \ell_{ui}(\theta).$$

All statements are about exact arithmetic. For the unbiased model, delete the bias terms and $\mu$ everywhere; every proof goes through unchanged.

**Lemma 1 (the gradient of one term).** $\ell_{ui}$ depends only on $b_u$, $b_i$, $p_u$ and $q_i$, and

$$\frac{\partial \ell_{ui}}{\partial b_u} = -2 e_{ui} + 2 \lambda b_u, \quad \frac{\partial \ell_{ui}}{\partial b_i} = -2 e_{ui} + 2 \lambda b_i, \quad \nabla_{p_u} \ell_{ui} = -2 e_{ui} q_i + 2 \lambda p_u, \quad \nabla_{q_i} \ell_{ui} = -2 e_{ui} p_u + 2 \lambda q_i.$$

*Proof.* The prediction $\hat r_{ui}$ and the penalty of the term use only these four parameters. The derivative of $e_{ui}$ is $-1$ in $b_u$ and in $b_i$, $-q_i$ in $p_u$ (since $\nabla_{p} (p^\top q) = q$) and $-p_u$ in $q_i$. By the chain rule the derivative of $e_{ui}^2$ is $2 e_{ui}$ times these, and the derivative of $\lambda \lVert p_u \rVert^2$ is $2 \lambda p_u$, and the same for the other three. $\square$

**Theorem 2 (the step).** Let $\theta$ be the parameters before lines L5 to L7 for the rating $(u, i)$ and $\theta'$ the parameters after them. Then $\theta' = \theta - (\gamma / 2) \nabla \ell_{ui}(\theta)$.

*Proof.* Line L5 computes $e = e_{ui}(\theta)$. Line L6 sets $b_u' = b_u + \gamma (e - \lambda b_u) = b_u - (\gamma / 2)(-2 e + 2 \lambda b_u)$, and the same for $b_i$; by Lemma 1 these are the stated coordinates. Line L7 computes both new vectors from the old $p_u$ and $q_i$, so $p_u' = p_u - (\gamma / 2)(-2 e q_i + 2 \lambda p_u)$ and $q_i' = q_i - (\gamma / 2)(-2 e p_u + 2 \lambda q_i)$, again with all values taken at $\theta$. By Lemma 1 every other coordinate of $\nabla \ell_{ui}(\theta)$ is zero, and lines L5 to L7 do not change the other parameters. $\square$

**Corollary 3 (an unbiased estimate of the full gradient).** If $(u, i)$ is drawn uniformly from $K$, the expected step is $\mathbb{E}[\theta' - \theta] = -\frac{\gamma}{2 s} \nabla J(\theta)$.

*Proof.* By Theorem 2 and linearity, $\mathbb{E}[\theta' - \theta] = -\frac{\gamma}{2} \cdot \frac{1}{s} \sum_{(u, i) \in K} \nabla \ell_{ui}(\theta) = -\frac{\gamma}{2 s} \nabla J(\theta)$. $\square$

In line L4 the ratings come in a random order without replacement, so within one epoch the steps are not independent draws. Each rating is still visited once per epoch, and Corollary 3 holds for the first step of each epoch, whose rating is uniform on $K$.

**Proposition 4 (the penalty counts ratings).** Let $n_u$ be the number of ratings of user $u$ and $n_i$ the number of ratings of item $i$ in $K$. Then

$$J = \sum_{(u, i) \in K} e_{ui}^2 + \lambda \sum_u n_u \bigl( b_u^2 + \lVert p_u \rVert^2 \bigr) + \lambda \sum_i n_i \bigl( b_i^2 + \lVert q_i \rVert^2 \bigr).$$

*Proof.* In the sum over $K$ the term $\lambda (b_u^2 + \lVert p_u \rVert^2)$ appears once for each rating of $u$, that is $n_u$ times, and the term $\lambda (b_i^2 + \lVert q_i \rVert^2)$ appears $n_i$ times. $\square$

**Proposition 5 (rotations).** Let $Q$ be an orthogonal $r \times r$ matrix. Replacing every $p_u$ by $Q p_u$ and every $q_i$ by $Q q_i$ keeps every prediction and the value of $J$. In particular, if some factor is nonzero, then $J$ takes the same value at two different points, so a minimizer with a nonzero factor is never unique.

*Proof.* $(Q p_u)^\top (Q q_i) = p_u^\top Q^\top Q q_i = p_u^\top q_i$, and $\lVert Q p_u \rVert = \lVert p_u \rVert$, $\lVert Q q_i \rVert = \lVert q_i \rVert$. For $Q = -I$, the point changes whenever some factor is nonzero. $\square$

**Proposition 6 (zero factors).** If $p_u = 0$ for all users and $q_i = 0$ for all items, then $\nabla_{p_u} J = 0$ and $\nabla_{q_i} J = 0$ for all $u$ and $i$, whatever the biases, and lines L5 to L7 keep all factors at zero.

*Proof.* By Lemma 1, $\nabla_{p_u} \ell_{ui} = -2 e_{ui} q_i + 2 \lambda p_u = 0$ when $p_u = q_i = 0$, and likewise for $q_i$. Summing over $K$ gives the first claim. By Theorem 2 the factor part of each step is $-(\gamma / 2)$ times these zero vectors, so the factors stay zero, and by induction over the steps they stay zero for the whole run. $\square$

So a start with all factors at zero trains only the biases, and line L2 starts from small random vectors. The page claims no convergence for a fixed step size $\gamma$: $J$ is not convex, and Theorem 2 only says that each step follows the negative gradient of one term.
