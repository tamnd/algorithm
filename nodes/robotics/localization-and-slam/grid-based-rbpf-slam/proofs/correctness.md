---
title: Why the improved proposal and its weight are right, and what is approximated
proves: [correctness]
status: full
---

**Setting.** Particle $i$ holds a pose $x^i_{t-1}$, a grid map $m^i_{t-1}$ built from its own path and the scans so far, and a weight $w^i_{t-1}$. The motion model is $p(x_t \mid x_{t-1}, u_t)$ and the scan model is $p(z_t \mid m, x_t)$. The target of the filter is the path posterior $p(x_{1:t} \mid z_{1:t}, u_{1:t})$. Given a path, the map is the result of [occupancy grid mapping](/occupancy-grid-mapping/) on that path, $p(m \mid x_{1:t}, z_{1:t})$.

**Claims.** (1) The method is a Rao-Blackwellized particle filter over paths. (2) If line L6 draws from $p(x_t \mid m^i_{t-1}, x^i_{t-1}, z_t, u_t)$, then the correct weight factor is $p(z_t \mid m^i_{t-1}, x^i_{t-1}, u_t)$, which does not depend on the drawn pose. (3) Lines L5 and L6 approximate this draw by a Gaussian and this factor by a Monte Carlo sum, and line L4 falls back to the motion model, whose weight estimates the same factor. (4) Resampling and the copies of the grids keep the represented distribution. (5) The scan matcher of line L3 stops and never lowers the score.

## (1) The factorization

By the chain rule, $p(x_{1:t}, m \mid z_{1:t}, u_{1:t}) = p(m \mid x_{1:t}, z_{1:t}) \, p(x_{1:t} \mid z_{1:t}, u_{1:t})$. The controls drop from the first factor because, given the path, they carry no information about the map. So it is enough to sample paths and to compute, for each path, the map posterior. Line L7 does this incrementally for each particle, with the log-odds update. The grid update is itself an approximation: it treats the cells as independent and uses an inverse sensor model. So, unlike the landmark filters of FastSLAM in the linear Gaussian case, the "closed form" part here is not exact. This is a known property of occupancy grids, not of the particle filter.

## (2) The optimal proposal and its weight

Write $m = m^i_{t-1}$, $x' = x^i_{t-1}$ and $q(x_t) = p(x_t \mid m, x', z_t, u_t)$. By Bayes' rule,

$$q(x_t) = \frac{p(z_t \mid m, x_t) \, p(x_t \mid x', u_t)}{p(z_t \mid m, x', u_t)}, \qquad p(z_t \mid m, x', u_t) = \int p(z_t \mid m, x) \, p(x \mid x', u_t) \, dx.$$

The scan model needs only the map built from the earlier scans, because the map is a function of the path so far and the scans so far. The path target changes from step $t-1$ to step $t$ by the factor $p(z_t \mid m, x_t) \, p(x_t \mid x', u_t) / p(z_t \mid z_{1:t-1}, u_{1:t})$, where the denominator is the same for all particles. The importance weight is the target over the proposal, so the weight factor of a particle that draws $x_t$ from $q$ is

$$\frac{p(z_t \mid m, x_t) \, p(x_t \mid x', u_t)}{q(x_t)} = p(z_t \mid m, x', u_t),$$

up to the common constant. It does not depend on $x_t$. This is the proposal that Grisetti, Stachniss and Burgard (2007) approximate.

## (3) The approximation of lines L4 to L6

The scan model of a laser is very peaked, so $q$ is concentrated near the poses where the scan fits the map. Line L3 finds such a pose $\hat x$ by scan matching. Line L5 draws $K$ points $x_j$ uniformly in a box $B$ of volume $V$ around $\hat x$ and computes $\tau_j = p(z_t \mid m, x_j) \, p(x_j \mid x', u_t)$.

- **The weight.** $\frac{V}{K} \sum_j \tau_j$ is a Monte Carlo estimate of $\int_B p(z_t \mid m, x) \, p(x \mid x', u_t) \, dx$: each term has the expected value $\frac{1}{V} \int_B \tau(x) \, dx$, so the estimate is unbiased for the integral over $B$. The integral over $B$ is below the integral of claim (2) by the mass outside $B$, which is small when $q$ is concentrated in $B$. The tests compare the estimate with $K = 3000$ against a midpoint rule over the same box. In the code the scan model drops a factor that is the same for every pose and every particle, so it cancels at normalization.
- **The draw.** Line L6 fits a Gaussian to the points with the weights $\tau_j / \sum_k \tau_k$: the weighted mean and the weighted covariance, with a small floor on the diagonal. If $q$ is Gaussian and $K$ is large, the fit tends to the moments of $q$ restricted to $B$. If $q$ has several modes or is cut by the box, the draw is from a different density than the weight assumes, and the weights are then only approximate. This is a known error of the method, not a bug of the code.
- **The fallback.** If the scan matcher fails, line L4 draws $x_t$ from the motion model and multiplies the weight by $p(z_t \mid m, x_t)$. The expected value of this factor over the draw is $\int p(z_t \mid m, x) \, p(x \mid x', u_t) \, dx$, the same integral as above. So both branches estimate the same weight factor, and particles that took different branches can be compared.

## (4) Resampling

Lines L8 and L9 compute $N_\text{eff} = 1 / \sum_i (\tilde w^i)^2$ from the normalized weights and resample only when it is below $N/2$. Resampling draws $N$ particles with probabilities $\tilde w^i$, which keeps the represented distribution in expectation, and sets all weights to $1/N$. If it does not resample, the particles and their weights are left as they are, which is also correct. Each copy gets its own copy of the grid. The tests check that a change to one copy does not change another; if two copies shared one mutable grid, the next update of line L7 would write the scan of one path into the map of the other.

## (5) The scan matcher

The matcher accepts a move only when it raises the score, so the score never goes down and the result is at least as good as the odometry guess. It stops: at each step size the candidate poses lie on a lattice, a pose whose score is above the score of the start must have at least one beam endpoint near an occupied cell of the finite grid, so such poses lie in a bounded region with finitely many lattice points, and a strictly increasing sequence cannot repeat a point. The result is a local maximum at the smallest step size, not always the global one: the tests show a start 6 cm from the truth from which it stops 5 cm off.
