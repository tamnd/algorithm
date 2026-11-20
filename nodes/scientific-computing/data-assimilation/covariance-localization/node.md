---
tag: HWT5MF
kind: technique
slug: covariance-localization
name: Covariance localization
aliases:
- Schur product localization
area: scientific-computing/data-assimilation
level: core
summary: Multiplies the ensemble covariance elementwise by a compactly supported correlation to remove spurious long-range correlations.
prereqs: [ensemble-kalman-filter, positive-definite-matrix]
see_also: [gaspari-cohn-function, covariance-inflation, local-ensemble-transform-kalman-filter, ensemble-square-root-filter, hybrid-ensemble-variational, local-particle-filter, background-error-covariance, lorenz-96-model]
sources:
  - paper: doi:10.1175/1520-0493(2001)129<0123:ASEKFF>2.0.CO;2
    title: "P. L. Houtekamer and H. L. Mitchell, A sequential ensemble Kalman filter for atmospheric data assimilation, Monthly Weather Review 129(1) (2001) 123-137"
    locator: the localized gain with a compactly supported correlation function
  - paper: doi:10.1175/1520-0493(2001)129<2776:DDFOBE>2.0.CO;2
    title: "T. M. Hamill, J. S. Whitaker and C. Snyder, Distance-dependent filtering of background error covariance estimates in an ensemble Kalman filter, Monthly Weather Review 129(11) (2001) 2776-2790"
    locator: the Schur product of the ensemble covariance with a correlation function and its effect for small ensembles
  - paper: doi:10.1002/qj.49712555417
    title: "G. Gaspari and S. E. Cohn, Construction of correlation functions in two and three dimensions, Quarterly Journal of the Royal Meteorological Society 125(554) (1999) 723-757"
    locator: "eq. (4.10), the compactly supported fifth order function used as the taper"
  - paper: doi:10.1016/j.physd.2006.11.008
    title: "B. R. Hunt, E. J. Kostelich and I. Szunyogh, Efficient data assimilation for spatiotemporal chaos: a local ensemble transform Kalman filter, Physica D 230(1-2) (2007) 112-126"
    locator: the local analysis with the observations near each grid point and their weighting by distance
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation of the data assimilation pages
---

Covariance localization removes the spurious correlations between distant variables from the sample covariance of an ensemble. A forecast ensemble of $N$ members gives a covariance $P^f$ of rank at most $N - 1$, and between two variables that are in fact unrelated it shows a sample correlation of typical size $1/\sqrt{N - 1}$. An observation then changes variables far away from it. Localization multiplies $P^f$ entry by entry (the Schur product) by a correlation matrix $\rho$ that is $1$ on the diagonal, falls with distance and is zero beyond a cutoff, often the [Gaspari-Cohn function](/gaspari-cohn-function/). The Schur product theorem keeps the result a covariance matrix, and makes it full rank. Houtekamer and Mitchell (2001) and Hamill, Whitaker and Snyder (2001) introduced it in the [ensemble Kalman filter](/ensemble-kalman-filter/).

## In plain words

With twenty members, two numbers that have nothing to do with each other will still look a little related, just by chance. The filter takes this chance relation for real, so an observation in one place changes the state in a far place. Localization says: trust the ensemble for nearby pairs of variables, trust it less as the distance grows, and ignore it beyond some distance. It does this by multiplying each covariance by a weight that depends on the distance. The weights are chosen so that the result is still a valid covariance.

## When it applies

- An ensemble filter or smoother whose ensemble is much smaller than the number of variables, so that $P^f$ is rank deficient.
- A system where the true correlations decay with distance, as in the atmosphere, the ocean or the [Lorenz-96 model](/lorenz-96-model/).
- An analysis that changes variables far from all observations, or a filter that needs very large inflation or diverges with a small ensemble.

## The template

$X$ and $Y$ are the unscaled perturbations of the state and of the predicted observations, so $P^fH^\top \approx XY^\top/(N - 1)$ and $HP^fH^\top \approx YY^\top/(N - 1)$. $\circ$ is the Schur (entrywise) product. The holes are the taper $\phi$ (a correlation function) and the length scale $c$. In the notation of Ide, Courtier, Ghil and Lorenc (1997), $f$ marks the forecast.

```pseudo id=main
LOCALIZED-GAIN(X, Y, R, positions, phi, c)
L1  rho^xy_jk <- phi(dist(grid j, obs k) / c)          ▷ hole: phi and c
L2  rho^yy_kl <- phi(dist(obs k, obs l) / c)
L3  PH^T <- rho^xy o (X Y^T / (N - 1))
L4  HPH^T <- rho^yy o (Y Y^T / (N - 1))
L5  K <- PH^T (HPH^T + R)^-1
L6  return K                                             ▷ use in any ensemble analysis
```

Lines L1 and L2 compute the weights from the distances. Lines L3 and L4 localize the two covariances that the gain needs, which is the form of Houtekamer and Mitchell (2001). For a linear $H$ that only picks grid values, they are $(\rho \circ P^f)H^\top$ and $H(\rho\circ P^f)H^\top$ for the correlation matrix $\rho$ on the grid. A serial filter that takes one observation at a time, like the serial [EnSRF](/ensemble-square-root-filter/), only needs line L3 for one column: it multiplies the regression coefficients of the state on the observation by $\phi(\text{dist}/c)$.

**Localization in observation space.** The [LETKF](/local-ensemble-transform-kalman-filter/) has no gain matrix of the full state. It computes a separate analysis for each grid point with the nearby observations, and divides the error variance of observation $k$ by the weight $w_k = \phi(\text{dist}/c)$. This acts on $R$ instead of $P^f$. The two forms agree for observations at the grid point and differ elsewhere.

**Why the matrix stays a covariance.** The Schur product theorem: if $A$ and $B$ are symmetric positive semidefinite, so is $A \circ B$. Proof: write $B = \sum_k b_kb_k^\top$. Then $x^\top(A \circ B)x = \sum_k (x \circ b_k)^\top A(x \circ b_k) \ge 0$. If $A$ is positive definite and $B$ has a positive diagonal, the sum is zero only if $x \circ b_k = 0$ for all $k$. Each $i$ has some $k$ with $b_{k,i} \ne 0$, because $B_{ii} = \sum_k b_{k,i}^2 > 0$, so $x = 0$. Hence a positive definite $\rho$ with unit diagonal turns any sample covariance with positive variances into a positive definite matrix of full rank, with the same variances. This is why $\phi$ must be a correlation function in the dimension of the grid, not just any function that falls to zero.

**How large the spurious correlations are.** Let $u$ and $v$ be independent, with $v$ Gaussian, and let $r$ be the sample correlation of $N$ independent draws. Then $\mathbb E[r^2] = 1/(N - 1)$. Proof: given the draws of $u$, $r = a^\top v_c/|v_c|$, where $a$ is a fixed unit vector in the space of dimension $N - 1$ of vectors with zero sum and $v_c$ is the centred vector of the draws of $v$. $v_c$ is a standard Gaussian vector in that space times the standard deviation of $v$, so $v_c/|v_c|$ is uniform on its unit sphere. Each of the $N - 1$ coordinates of a uniform unit vector has the same mean square, and the squares add to $1$. With $N = 20$ the root mean square of a spurious correlation is $1/\sqrt{19} \approx 0.23$.

**A worked example.** Take two grid points at positions $0$ and $3$, two members $(-1, -1)$ and $(1, 1)$, and one observation $y^o = 1$ of point $0$ with $R = 1$. The sample covariance is $\begin{pmatrix} 2 & 2\\ 2 & 2\end{pmatrix}$, so without localization the gain is $(2/3, 2/3)$ and the mean of point $3$ moves from $0$ to $2/3$, as far as point $0$. With the Gaspari-Cohn taper and $c = 2$, the distance $3 = 1.5c$ has the weight $19/1152$. The localized cross covariance is $2 \cdot 19/1152 = 19/576$, the gain for point $3$ becomes $(19/576)/3 = 19/1728 \approx 0.011$, and its mean moves only to $0.011$. Point $0$ keeps the gain $2/3$. The LETKF form on the same data moves point $3$ to $19/595 \approx 0.032$ (see its page), because it changes the weight of the observation and not the covariance.

**Measurements on the other pages.** On the Lorenz-96 model with $n = 40$, every other variable observed and $N = 20$, the serial EnSRF with $\rho = 1.02$ had the RMSE $0.373$ with $c = 4$, $0.303$ with $c = 10$ and $4.52$ without localization. The EnKF had $0.347$ with $c = 8$ and $\rho = 1.05$, and above $4.6$ without localization even with large inflation. With localization both filters stayed well below the error $3.7$ of a free ensemble.

## Classic examples

- [Ensemble Kalman filter](/ensemble-kalman-filter/): the localized gain of lines L3 to L5 with perturbed observations.
- [Ensemble square root filter](/ensemble-square-root-filter/): serial processing, where each observation updates the state with localized regression coefficients.
- [Ensemble adjustment Kalman filter](/ensemble-adjustment-kalman-filter/): the same localized regression from observation space to each state variable.
- [Local ensemble transform Kalman filter](/local-ensemble-transform-kalman-filter/): localization in observation space by local analyses and weighted error variances.
- [Hybrid ensemble-variational assimilation](/hybrid-ensemble-variational/): the localized ensemble covariance as part of the background covariance of a variational method.
- [Local particle filter](/local-particle-filter/): the same idea of a local analysis applied to particle weights.

## Variations

- **Choice of taper.** The Gaspari-Cohn function is the usual choice because it looks like a Gaussian and has compact support. Any compactly supported correlation function of the right dimension works.
- **Length scale.** $c$ is tuned. A small $c$ removes more noise but also removes true correlations; a large $c$ keeps more noise. In the EnSRF measurement above the error fell as $c$ grew up to $15$, the largest value tried (with the distance along the ring, for which the taper matrix at $c = 15$ has a negative eigenvalue; see the pitfall on the wrong distance below), and the EnKF did best near $c = 8$ to $10$, so the best value depends on the filter.
- **Several distances.** A separate length scale can be used for each direction, for example for the vertical in a model of the atmosphere.
- **Localization in time.** In a [smoother](/ensemble-kalman-smoother/), the spurious correlations between distant times are not removed by a spatial taper. A shorter lag does this.

## Pitfalls

- **A taper that is not positive definite (line L1).** A function that is $1$ at zero and falls to zero, such as a cut-off step or a triangle in two dimensions, can give a matrix $\rho$ with negative eigenvalues. Then $\rho \circ P^f$ can fail to be a covariance and the analysis can be unstable.
- **The wrong distance (line L1).** A correlation function of $\mathbb R^3$ stays positive definite on a sphere or a circle with the chordal distance, because these lie in $\mathbb R^3$. With the distance along the circle this holds only while the support is at most half the circle. On the Lorenz-96 ring of 40 points the Gaspari-Cohn matrix with the distance along the ring has a negative eigenvalue for $c = 11$ and more; see the [Gaspari-Cohn function](/gaspari-cohn-function/) page.
- **Half-width or support.** With the Gaspari-Cohn function, $c$ is the half-width and the weight is zero beyond $2c$. A stated "localization radius" can mean either of the two. Check which one a value means.
- **Imbalance.** Localization also removes true long-range correlations, for example physical balances between variables, so the analysis can be out of balance.
- **Nonlocal observations.** An observation of an integral over many grid points, such as a satellite radiance, has no single position, so its distance to a grid point is not well defined.

## References
