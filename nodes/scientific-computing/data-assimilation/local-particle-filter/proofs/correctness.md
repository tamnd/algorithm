---
title: The local particle filter analysis resamples each local weighted marginal, and it is the global bootstrap step when the taper is 1
proves: [correctness, termination]
status: full
---

**Setting.** The particles $x_1, \ldots, x_N \in \mathbb R^n$ are given, and the observations are $(\mathrm{pos}_o, y_o, r_o)$ for $o = 1, \ldots, p$. Line L2 computes, at each grid point $j$, the weights

$$w_i(j) = \frac{\exp(\ell_i(j))}{\sum_m \exp(\ell_m(j))}, \qquad \ell_i(j) = -\tfrac12\sum_{o=1}^p \rho_{jo}\,\frac{(y_o - x_{i,\mathrm{pos}_o})^2}{r_o},$$

with the taper values $\rho_{jo} \in [0, 1]$. Lines L4 to L7 apply systematic resampling with one offset $u \in [0, 1)$ at every grid point: grid point $j$ picks, for $i = 0, \ldots, N - 1$, the particle $a_j(i)$ whose interval of cumulative weight $(c_{k-1}(j), c_k(j)]$ holds $t_i = (i + u)/N$, and the new particle $i$ has the components $\tilde x_{i,j} = x_{a_j(i),j}$.

**Lemma 1 (systematic resampling).** For fixed weights $w$, the number of copies $n_k$ of particle $k$ satisfies $\lfloor Nw_k\rfloor \le n_k \le \lceil Nw_k\rceil$, and if $u$ is uniform on $[0, 1)$ then $\mathbb E[n_k] = Nw_k$.

*Proof.* $n_k$ is the number of points $t_i = (i + u)/N$ in the interval $(c_{k-1}, c_k]$ of length $w_k$. The points are spaced $1/N$ apart, so an interval of length $w_k$ holds $\lfloor Nw_k\rfloor$ or $\lceil Nw_k\rceil$ of them. As $u$ runs over $[0, 1)$, the point set $\{t_i\}$ is a uniform random shift of the grid $\{i/N\}$, so each point of $(0, 1]$ is covered by exactly one $t_i$ with density $N$, and $\mathbb E[n_k] = N\,\mathrm{length}(c_{k-1}, c_k] = Nw_k$. $\square$

**Theorem 2 (local marginals).** At every grid point $j$, the values $\tilde x_{1,j}, \ldots, \tilde x_{N,j}$ are a systematic resample of the weighted sample $\{(x_{i,j}, w_i(j))\}$, so for any function $f$ and $u$ uniform,

$$\mathbb E\Big[\frac1N\sum_{i=1}^N f(\tilde x_{i,j})\Big] = \sum_{i=1}^N w_i(j) f(x_{i,j}) .$$

*Proof.* By line L7, $\tilde x_{i,j} = x_{a_j(i),j}$, so $\frac1N\sum_i f(\tilde x_{i,j}) = \frac1N\sum_k n_k(j) f(x_{k,j})$, and Lemma 1 gives the expectation. $\square$

**Theorem 3 (no taper).** If $\rho_{jo} = 1$ for all $j$ and $o$ (radius None), the step is the analysis step of the bootstrap particle filter with systematic resampling.

*Proof.* Then $\ell_i(j) = -\tfrac12\sum_o (y_o - x_{i,\mathrm{pos}_o})^2/r_o$ for every $j$, which is the log likelihood of particle $i$ under independent Gaussian observation errors, up to a constant. All grid points have the same weights, so with the same $u$ they pick the same indices $a_j(i) = a(i)$, and $\tilde x_i = x_{a(i)}$ is the whole particle $a(i)$. This is weighting by the likelihood and systematic resampling of whole particles. $\square$

**Theorem 4 (exact local weights).** Let the prior have independent components, so that the particles have independent components with these marginals, let each observation measure one component, and let $\rho_{jo} = 1$ if $\mathrm{pos}_o = j$ and 0 otherwise (radius 0). Then $w_i(j)$ is the self-normalized importance weight of $x_{i,j}$ for the marginal posterior $p(x_j \mid y) \propto p(x_j)\prod_{o:\,\mathrm{pos}_o = j} p(y_o \mid x_j)$, which depends only on the observations of point $j$.

*Proof.* Under these assumptions the posterior factorizes over the components, so the marginal posterior of $x_j$ is the prior marginal times the likelihood of the observations at $j$. The local log weight $\ell_i(j)$ is exactly the log of that likelihood at $x_{i,j}$, up to a constant. $\square$

So in this case the variance of the local log weights at point $j$ depends on the number of observations at $j$, not on $n$, and the local weights do not collapse as $n$ grows, while the global weights of Theorem 3 do (see [particle filter collapse in high dimensions](/particle-filter-weight-collapse/)). With correlated components, a taper of positive radius is a heuristic: it ignores the information that far observations carry through the correlations, and the new particles mix components of different old particles, which can break balances between neighboring grid points. Rebeschini and van Handel (2015) prove dimension-free error bounds for a block particle filter under a decay of correlations condition, with a bias that comes from the localization.

**Termination.** Line L2 takes $\Theta(Np)$ steps for the misfits and $\Theta(nNq)$ steps for the local sums, where $q$ is the largest number of observations with $\rho_{jo} > 0$ at one grid point. Each systematic resampling in line L5 makes one pass over the $N$ points and the $N$ cumulative weights, since both indices only increase, so lines L4 to L7 take $\Theta(nN)$ steps. Every loop is bounded, and the step ends.

**Summary.** The local analysis is a systematic resample of the local weighted marginal at each grid point (Theorem 2). It is the global bootstrap step when the taper is 1 (Theorem 3), and for independent components with radius 0 its weights are the exact marginal importance weights (Theorem 4). The tests check Lemma 1 against a brute force inverse of the cumulative weights, Theorem 3 by equality with a separate global bootstrap step, Theorem 4 by the weighted mean against the Kalman filter mean, and the page example. $\blacksquare$
