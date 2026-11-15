---
title: The SVD++ update is a scaled gradient step on one term of its objective and reduces to biased matrix factorization
proves: [correctness]
status: full
---

The notation is that of the page. For a user $u$ let $\nu_u = |N(u)|^{-1/2}$ when $N(u)$ is not empty and $\nu_u = 0$ otherwise, and $z_u = p_u + \nu_u \sum_{j \in N(u)} y_j$. Then $\hat r_{ui} = \mu + b_u + b_i + q_i^\top z_u$, $e_{ui} = r_{ui} - \hat r_{ui}$, and for $(u, i) \in K$

$$\ell_{ui} = e_{ui}^2 + \lambda_b \bigl( b_u^2 + b_i^2 \bigr) + \lambda_f \Bigl( \lVert p_u \rVert^2 + \lVert q_i \rVert^2 + \sum_{j \in N(u)} \lVert y_j \rVert^2 \Bigr), \qquad J = \sum_{(u, i) \in K} \ell_{ui}.$$

The parameters are $\theta = (b, p, q, y)$; $\mu$ is fixed by line L1, and $N$ is part of the input. All statements are about exact arithmetic.

**Lemma 1 (the gradient of one term).** $\ell_{ui}$ depends only on $b_u$, $b_i$, $p_u$, $q_i$ and the $y_j$ with $j \in N(u)$, and

$$\frac{\partial \ell_{ui}}{\partial b_u} = -2 e_{ui} + 2 \lambda_b b_u, \qquad \frac{\partial \ell_{ui}}{\partial b_i} = -2 e_{ui} + 2 \lambda_b b_i,$$

$$\nabla_{q_i} \ell_{ui} = -2 e_{ui} z_u + 2 \lambda_f q_i, \qquad \nabla_{p_u} \ell_{ui} = -2 e_{ui} q_i + 2 \lambda_f p_u, \qquad \nabla_{y_j} \ell_{ui} = -2 e_{ui} \nu_u q_i + 2 \lambda_f y_j \ (j \in N(u)).$$

*Proof.* The prediction uses only the listed parameters, and so do the penalties of the term. Since $z_u$ is linear in $p_u$ and in each $y_j$, with $\partial z_u / \partial p_u = I$ and $\partial z_u / \partial y_j = \nu_u I$, the derivative of $e_{ui}$ is $-z_u$ in $q_i$, $-q_i$ in $p_u$, $-\nu_u q_i$ in $y_j$, and $-1$ in each bias. The chain rule gives $2 e_{ui}$ times these for $e_{ui}^2$, and the penalties add $2 \lambda$ times the parameter. Item $i$ may itself be in $N(u)$; then $q_i$ and $y_i$ are still two separate parameters, and the formulas hold as stated. $\square$

**Theorem 2 (the step).** Let $\theta$ be the parameters before lines L4 to L8 for the rating $(u, i)$, and $\theta'$ after them. Then $\theta' = \theta - (\gamma / 2) \nabla \ell_{ui}(\theta)$.

*Proof.* Line L4 computes $z = z_u(\theta)$ and line L5 computes $e = e_{ui}(\theta)$. Line L6 sets $b_u' = b_u - (\gamma / 2)(-2 e + 2 \lambda_b b_u)$, and the same for $b_i$. Line L7 sets $q_i' = q_i - (\gamma / 2)(-2 e z + 2 \lambda_f q_i)$ and $p_u' = p_u - (\gamma / 2)(-2 e q_i + 2 \lambda_f p_u)$ with the old $q_i$ and $p_u$, and line L8 sets $y_j' = y_j - (\gamma / 2)(-2 e \nu_u q_i + 2 \lambda_f y_j)$ with the old $q_i$. By Lemma 1 these are the coordinates of $\theta - (\gamma / 2) \nabla \ell_{ui}(\theta)$, and all other coordinates of the gradient are 0, matching the parameters that the lines do not touch. $\square$

As for matrix factorization, if $(u, i)$ is drawn uniformly from $K$, the expected step is $-(\gamma / 2 s) \nabla J(\theta)$, by linearity.

**Proposition 3 (reduction to biased matrix factorization).** If $N(u)$ is empty for every user, then $\hat r_{ui} = \mu + b_u + b_i + p_u^\top q_i$, $J$ is the objective of biased matrix factorization with the penalty $\lambda_b$ on the biases and $\lambda_f$ on the vectors, inside the sum over the ratings, and lines L4 to L8 make the step of that method, with no change to any $y_j$.

*Proof.* With $N(u)$ empty, $\nu_u = 0$ and the sum is empty, so $z_u = p_u$ and the penalty on $y$ in $\ell_{ui}$ is 0. Line L7 becomes $q_i' = q_i + \gamma (e p_u - \lambda_f q_i)$ and $p_u' = p_u + \gamma (e q_i - \lambda_f p_u)$ with old values, which is line L7 of matrix factorization, and line L8 has no $j$ to visit. $\square$

**Proposition 4 (rotations).** For an orthogonal $r \times r$ matrix $Q$, replacing every $p_u$, $q_i$ and $y_j$ by $Q p_u$, $Q q_i$ and $Q y_j$ keeps every prediction and $J$.

*Proof.* $z_u$ becomes $Q z_u$ by linearity, $(Q q_i)^\top (Q z_u) = q_i^\top z_u$, and orthogonal matrices keep norms. $\square$

**Proposition 5 (cost).** One step costs $O((|N(u)| + 1) r)$, so one epoch costs $O(r \sum_{(u, i) \in K} (|N(u)| + 1))$, which is at most $O(s d r)$ with $d = \max_u |N(u)|$.

*Proof.* Line L4 adds $|N(u)|$ vectors of length $r$, lines L5 to L7 cost $O(r)$, and line L8 updates $|N(u)|$ vectors of length $r$. Line L3 visits each rating once per epoch, and the random order costs $O(s)$. $\square$

If the ratings of one user are processed together with $z_u$ computed once and the updates of the $y_j$ added up and applied after the last rating of the user, the cost of an epoch drops to $O(s r + r \sum_u |N(u)|)$. Theorem 2 does not cover that schedule: within one user, its later steps use the old $z_u$ and the old $y_j$, so it is a different sequence of steps. No convergence result is claimed for either schedule; $J$ is not convex.
