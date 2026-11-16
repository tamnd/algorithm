---
title: On exact data with a one-dimensional null space of M, EPnP returns the true pose
proves: [correctness]
status: full
---

We use the notation of the page. The world points $\mathbf{X}_1, \ldots, \mathbf{X}_n$, $n \ge 4$, are not coplanar. The true pose $(R, \mathbf{t})$ puts every point in front of the camera, $Z_i = (R\mathbf{X}_i + \mathbf{t})_3 > 0$, and the data are exact: $\mathbf{y}_i = (u_i, v_i)$ with $u_i = (R\mathbf{X}_i + \mathbf{t})_1/Z_i$ and $v_i = (R\mathbf{X}_i + \mathbf{t})_2/Z_i$. The arithmetic is exact (real RAM). We write $\mathbf{x} \in \mathbb{R}^{12}$ for a stack of four 3-vectors $\mathbf{x}_1, \ldots, \mathbf{x}_4$, and $\mathbf{x}^\ast$ for the true camera control points, $\mathbf{x}^\ast_j = R\mathbf{c}_j + \mathbf{t}$.

**Claim.** Assume that the null space of $M$ has dimension 1. Then the candidate of case $N = 1$ is the true pose, the output has reprojection error 0, and the output is the true pose.

**Lemma 1 (control points and weights).** The four control points of line L1 are affinely independent, so each point has unique weights with $\mathbf{X}_i = \sum_j \alpha_{ij}\mathbf{c}_j$ and $\sum_j \alpha_{ij} = 1$.

*Proof.* The centered points are not coplanar, so their scatter matrix $\sum_i (\mathbf{X}_i - \mathbf{c}_1)(\mathbf{X}_i - \mathbf{c}_1)^{\mathsf T}$ is positive definite and its three eigenvalues $\lambda_k$ are positive. The vectors $\mathbf{c}_{k+1} - \mathbf{c}_1 = \sqrt{\lambda_k/n}\,\mathbf{e}_k$, with orthonormal eigenvectors $\mathbf{e}_k$, are therefore linearly independent. So the $3 \times 3$ matrix $B$ with these columns is invertible, and line L2 finds the unique $(\alpha_{i2}, \alpha_{i3}, \alpha_{i4}) = B^{-1}(\mathbf{X}_i - \mathbf{c}_1)$, with $\alpha_{i1} = 1 - \alpha_{i2} - \alpha_{i3} - \alpha_{i4}$. $\square$

**Lemma 2 (the weights hold in every frame).** For any rotation $R'$ and translation $\mathbf{t}'$, $R'\mathbf{X}_i + \mathbf{t}' = \sum_j \alpha_{ij}(R'\mathbf{c}_j + \mathbf{t}')$.

*Proof.* $\sum_j \alpha_{ij}(R'\mathbf{c}_j + \mathbf{t}') = R'\sum_j\alpha_{ij}\mathbf{c}_j + (\sum_j\alpha_{ij})\mathbf{t}' = R'\mathbf{X}_i + \mathbf{t}'$. $\square$

**Lemma 3 (the meaning of $M\mathbf{x} = \mathbf{0}$).** For $\mathbf{x} \in \mathbb{R}^{12}$ put $\mathbf{p}_i = \sum_j \alpha_{ij}\mathbf{x}_j$. Then $M\mathbf{x} = \mathbf{0}$ if and only if $p_{i,1} = u_i p_{i,3}$ and $p_{i,2} = v_i p_{i,3}$ for every $i$. In particular, if a pose $(R', \mathbf{t}')$ projects every $\mathbf{X}_i$ exactly onto $\mathbf{y}_i$ with positive depth, then $\mathbf{x}' = (R'\mathbf{c}_j + \mathbf{t}')_j$ satisfies $M\mathbf{x}' = \mathbf{0}$.

*Proof.* The two rows of point $i$ in line L3 applied to $\mathbf{x}$ give $\sum_j \alpha_{ij}(x_{j,1} - u_i x_{j,3}) = p_{i,1} - u_ip_{i,3}$ and $p_{i,2} - v_ip_{i,3}$. For the second statement, Lemma 2 gives $\mathbf{p}_i = R'\mathbf{X}_i + \mathbf{t}'$, whose projection is $\mathbf{y}_i$. $\square$

**Proof of the claim.** By Lemma 3, $M\mathbf{x}^\ast = \mathbf{0}$, and $\mathbf{x}^\ast \ne \mathbf{0}$. By the assumption, the null space of $M$, which is also the null space of $M^{\mathsf T}M$, is $\operatorname{span}(\mathbf{x}^\ast)$. $M^{\mathsf T}M$ is positive semidefinite, so its eigenvalue 0 is the smallest one and is simple, and line L4 gives $\mathbf{v}_1 = s\,\mathbf{x}^\ast/\|\mathbf{x}^\ast\|$ with $s = \pm 1$.

*Case $N = 1$, line L6.* For a pair $p = (a, b)$ of control points, $\mathbf{dv}_p = \mathbf{v}_1^{[a]} - \mathbf{v}_1^{[b]} = s(R\mathbf{c}_a - R\mathbf{c}_b)/\|\mathbf{x}^\ast\|$. A rotation keeps lengths, so $\|\mathbf{dv}_p\| = \sqrt{\rho_p}/\|\mathbf{x}^\ast\|$, where $\rho_p = \|\mathbf{c}_a - \mathbf{c}_b\|^2$. The formula of line L6 then gives
$$\beta_1 = \frac{\sum_p \|\mathbf{dv}_p\|\sqrt{\rho_p}}{\sum_p \|\mathbf{dv}_p\|^2} = \frac{\sum_p \rho_p/\|\mathbf{x}^\ast\|}{\sum_p \rho_p/\|\mathbf{x}^\ast\|^2} = \|\mathbf{x}^\ast\| .$$
The sums are positive because the control points are distinct (Lemma 1).

*Line L7.* At $\boldsymbol\beta = (\beta_1, 0, 0, 0)$ every residual $\|\sum_k \beta_k\mathbf{dv}_{p,k}\|^2 - \rho_p = \beta_1^2\|\mathbf{dv}_p\|^2 - \rho_p$ is 0. A Gauss-Newton step solves $J^{\mathsf T}J\,\boldsymbol\delta = -J^{\mathsf T}\mathbf{r}$ with $\mathbf{r} = \mathbf{0}$, so it is $\boldsymbol\delta = \mathbf{0}$; if $J^{\mathsf T}J$ is singular, the code stops. In both cases $\boldsymbol\beta$ does not change.

*Line L8.* The camera control points are $\beta_1\mathbf{v}_1 = s\,\mathbf{x}^\ast$, so $\mathbf{p}_i = s(R\mathbf{X}_i + \mathbf{t})$ by Lemma 2. All true depths are positive, so the sum of the depths has the sign of $s$, and the sign test gives $\mathbf{p}_i = R\mathbf{X}_i + \mathbf{t}$ exactly.

*Line L9.* The pairs $(\mathbf{X}_i, \mathbf{p}_i)$ are related exactly by $(R, \mathbf{t})$, and the $\mathbf{X}_i$ are not collinear. The rigid alignment (the [Kabsch algorithm](/kabsch-algorithm/)) has the unique minimizer $(R, \mathbf{t})$ of $\sum_i\|R'\mathbf{X}_i + \mathbf{t}' - \mathbf{p}_i\|^2$ in that case, because the cost is 0 there and a rigid motion that fixes three non-collinear points is the identity. So the candidate of case $N = 1$ is $(R, \mathbf{t})$, and its error in line L10 is 0.

*Line L11.* Errors are nonnegative, so the chosen candidate $(R', \mathbf{t}')$ has error 0. The error is infinite when a depth is not positive, so $(R', \mathbf{t}')$ projects every point exactly with positive depth. By Lemma 3 its control points $\mathbf{x}'$ satisfy $M\mathbf{x}' = \mathbf{0}$, so $\mathbf{x}' = k\,\mathbf{x}^\ast$ for some $k$. Rigid motions keep the distance between $\mathbf{c}_1$ and $\mathbf{c}_2$, so $|k| = 1$; the depths of $\mathbf{p}_i' = k(R\mathbf{X}_i + \mathbf{t})$ are positive, so $k = 1$. Then $R'\mathbf{c}_j + \mathbf{t}' = R\mathbf{c}_j + \mathbf{t}$ for four affinely independent points, which forces $R' = R$ and $\mathbf{t}' = \mathbf{t}$. $\square$

**Remark (the dimension of the null space).** $M$ has $2n$ rows and 12 columns, so for $n = 4$ its null space has dimension at least 4, and for $n = 5$ at least 2. The assumption of the claim can then hold only for $n \ge 6$. For $n \ge 6$ points in general position it is the usual case, but we do not prove it here; this is a heuristic statement. The cases $N = 2$ and $N = 3$ serve the larger null spaces: they solve the distance equations, linearized in the products $\beta_k\beta_l$, and Gauss-Newton refines the result. They are not guaranteed to find the true pose. They usually do for $n = 5$, and this version can fail for $n = 4$, where the original method also uses the case $N = 4$.

**Remark (floating point).** On exact data in floating point, the eigenvalue 0 becomes a value of the order of the rounding error, and the steps above hold up to a relative error that grows with the ratio of the largest eigenvalue of $M^{\mathsf T}M$ to the second smallest one.
