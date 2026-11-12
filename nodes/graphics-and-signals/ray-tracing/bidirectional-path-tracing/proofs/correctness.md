---
title: Unbiasedness of bidirectional path tracing
proves: [correctness]
status: full
---

**Setting.** A full path of $k \ge 1$ edges is $\bar x = x_0 x_1 \cdots x_k$ with $x_0, \dots, x_{k-1}$ on the surfaces and $x_k = c$, the pinhole. Write $\Omega_k$ for the set of such paths, with the product area measure $\mu_k = dA(x_0) \cdots dA(x_{k-1})$. The value of pixel $j$ restricted to the paths of at most $K$ edges is

$$I_j^{(K)} = \sum_{k=1}^{K} \int_{\Omega_k} f_j(\bar x)\, d\mu_k(\bar x),$$

with $f_j \ge 0$ the measurement contribution of the path integral form. It contains the visibility $V(x_i, x_{i+1})$ of every edge.

**Strategies.** For $0 \le s \le k$ and $t = k + 1 - s$, strategy $s$ makes a path of $k$ edges from the first $s$ vertices $y_0 \cdots y_{s-1}$ of the light subpath and the first $t$ vertices $z_0 = c, \dots, z_{t-1}$ of the camera subpath, as $\bar x = y_0 \cdots y_{s-1} z_{t-1} \cdots z_0$. Let $p_s(\bar x)$ be the density of this path with respect to $\mu_k$ on the event that both subpaths are long enough: the product of $p_A(x_0)$ and of the area densities of $x_1, \dots, x_{s-1}$, each made from the previous one, times the area densities of $x_{k-1}, \dots, x_s$, each made from the next one. A vertex made by a ray from $x'$ is visible from $x'$, so $p_s(\bar x) > 0$ only where the edges inside the two subpaths have $V = 1$. The joining edge from $x_{s-1}$ to $x_s$ is not sampled; line L5 tests it. For $s = 0$ there is no joining edge, and for $t = 1$ the joining edge goes to the camera.

**Weights.** For each $k$, let $w_0, \dots, w_k$ be functions on $\Omega_k$ with

1. $w_s(\bar x) \ge 0$, and $w_s(\bar x) = 0$ wherever $p_s(\bar x) = 0$;
2. $\sum_{s=0}^{k} w_s(\bar x) = 1$ wherever $f_j(\bar x) > 0$.

The balance heuristic $w_s = p_s / \sum_r p_r$ and the power heuristic $w_s = p_s^2 / \sum_r p_r^2$ satisfy both, with $w_s = 0$ when all $p_r$ are $0$, provided that

3. for every $\bar x$ with $f_j(\bar x) > 0$ there is at least one $s$ with $p_s(\bar x) > 0$.

**Claim.** Under 1, 2 and 3, let $S_j$ be the sum that one pass of lines L2 to L9 adds to pixel $j$. Then $E[S_j] = I_j^{(K)}$, and the estimate of line L10 is the mean of $N$ independent copies of $S_j$, so it is unbiased.

**Proof.** One pass adds, for each $k \le K$ and each $s \le k$, the value

$$X_{k,s} = \mathbf 1[\text{the subpaths have } s \text{ and } t \text{ vertices}]\; V(x_{s-1}, x_s)\; w_s(\bar x)\, \frac{f_j(\bar x)}{p_s(\bar x)},$$

where $\bar x$ is the joined path and the factor $V$ is $1$ for $s = 0$. Line L5 makes the factor $V$, and lines L6 to L9 add the rest when it is positive. The value of $f_j$ contains $V(x_{s-1}, x_s)$ already, so the extra factor changes nothing on the support of $f_j$. Line L6 skips the paths with $f_j = 0$, and the terms with $p_s = 0$ have $w_s = 0$ by 1.

By the definition of $p_s$, the joined path has the density $p_s$ with respect to $\mu_k$ on the event of the indicator. So

$$E[X_{k,s}] = \int_{\{p_s > 0\}} w_s\, \frac{f_j}{p_s}\, p_s\, d\mu_k = \int_{\Omega_k} w_s\, f_j\, d\mu_k,$$

where the last step uses $w_s = 0$ on $\{p_s = 0\}$. The values are not negative, so the sum and the expectation can be swapped:

$$E[S_j] = \sum_{k=1}^{K} \sum_{s=0}^{k} \int_{\Omega_k} w_s f_j\, d\mu_k = \sum_{k=1}^{K} \int_{\Omega_k} \Big(\sum_{s=0}^{k} w_s\Big) f_j\, d\mu_k = \sum_{k=1}^{K} \int_{\Omega_k} f_j\, d\mu_k = I_j^{(K)},$$

by 2. $\square$

**The weights are well defined.** Condition 3 holds for scenes without point masses in the BSDF: if $f_j(\bar x) > 0$, then $L_e(x_0 \to x_1) > 0$, which with $p_A > 0$ on the emitters makes the light density of $x_0$ positive, and each BSDF factor and cosine of $f_j$ is positive, which with direction densities that are positive where $f_r \cos\theta$ is makes all area densities positive, and the camera samples each direction of the pixel with a positive density. So every $p_s(\bar x) > 0$ with $s \le k$. Then the sum $\sum_r p_r$ is positive and the heuristics satisfy 1 and 2.

**Leaving out a strategy.** The strategy $t = 0$, a light subpath that hits the camera, has density $0$ for a pinhole, so it is not in the sum, and the proof does not need it. In the same way, a join at a vertex with an ideal specular BSDF has $f_j = 0$ almost surely and adds nothing; its strategy must then be removed from the sum of every path that it could make, so that 2 still holds with the other strategies. If no strategy is left for some paths, condition 3 fails and those paths are missed, which is the bias of bidirectional path tracing for paths of the form light, specular, diffuse, specular, camera.

**Without the limit $K$.** If Russian roulette ends both subpaths, the survival probabilities enter $p_s$ as factors, the indicator becomes the event that both subpaths survive long enough, and the same computation holds for every $k$. Monotone convergence then gives $E[S_j] = I_j$.
