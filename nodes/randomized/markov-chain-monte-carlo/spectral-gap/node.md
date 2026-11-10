---
tag: 762CAY
kind: concept
slug: spectral-gap
name: Spectral gap
aliases:
- eigenvalue gap
- eigenvalue gap of a gossip matrix
area: randomized/markov-chain-monte-carlo
level: advanced
summary: For a reversible chain the spectral gap is 1 − λ2. The absolute gap 1 − max|λ| gives the relaxation time t_rel, which bounds the mixing time from above and below.
prereqs: [detailed-balance, eigenvalue, spectral-theorem, mixing-time]
see_also: [conductance, cheeger-inequality, canonical-paths, mixing-time, rayleigh-quotient, averaging-convergence-spectral-gap, power-iteration, expander-walk-sampler]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 12.1 (Lemma 12.2, the spectral representation); Section 12.2, The Relaxation Time (Theorem 12.4, equations (12.10) and (12.11); Theorem 12.5, equation (12.14)); Section 12.3 (eigenvalues of the cycle and the hypercube); Section 13.2 (Lemma 13.7, Remark 13.8)
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Birkhäuser, 2003
    locator: Chapter 5, Canonical paths and applications (spectral gap and mixing time)
---

The spectral gap of a reversible [Markov chain](/markov-chain/) is $\gamma = 1 - \lambda_2$, the distance from the top [eigenvalue](/eigenvalue/) 1 of its [transition matrix](/transition-matrix/) to the second largest eigenvalue. The *absolute* spectral gap $\gamma_* = 1 - \max\{|\lambda| : \lambda \ne 1\}$ also accounts for eigenvalues near $-1$, and its inverse $t_{rel} = 1/\gamma_*$ is the *relaxation time*. The relaxation time bounds the [mixing time](/mixing-time/) from above and from below, with a gap of a factor $\log(1/\pi_{min})$ between the two bounds. The page [conductance](/conductance/) gives a combinatorial view of the same quantity, and the [Cheeger inequality](/cheeger-inequality/) links the two.

## In plain words

Any starting distribution is the stationary one plus a sum of "modes". Each step of the chain multiplies each mode by its own fixed number, smaller than one in size. The stationary part never shrinks. The mode whose number is closest to one in size dies the slowest, so it decides how fast the chain forgets its start. The spectral gap measures how far that slowest number is from one. A large gap means every mode fades fast and the chain mixes in few steps. A tiny gap means some pattern in the start survives for a long time. The gap does not tell the whole story: the number of states also enters, because a start at one state is a mix of many modes, and they all have to fade.

## The idea

### Setting

Let $P$ be irreducible and reversible with respect to $\pi$ on a finite set $\mathcal X$ (see [detailed balance](/detailed-balance/)). Use the inner product $\langle f, g\rangle_\pi = \sum_x\pi(x)f(x)g(x)$ and $\|f\|_2^2 = \langle f, f\rangle_\pi$. Reversibility makes $P$ self-adjoint for this inner product, so by the [spectral theorem](/spectral-theorem/) its eigenvalues are real:
$$
1 = \lambda_1 > \lambda_2 \ge \cdots \ge \lambda_{|\mathcal X|} \ge -1.
$$
The top eigenvalue 1 is simple because $P$ is irreducible, and $\lambda_{|\mathcal X|} = -1$ exactly when the chain has period 2. Define
$$
\gamma = 1 - \lambda_2, \qquad \lambda_* = \max_{j \ge 2}|\lambda_j|, \qquad \gamma_* = 1 - \lambda_*, \qquad t_{rel} = 1/\gamma_*.
$$
For a lazy chain $\tfrac12(I + P)$ all eigenvalues are in $[0, 1]$, so $\gamma_* = \gamma$. The notation for mixing is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$, $t_{mix} = t_{mix}(1/4)$, and $\pi_{min} = \min_x\pi(x)$.

### The spectral representation (LPW Lemma 12.2)

Let $D = \operatorname{diag}(\pi)$. The matrix $A = D^{1/2}PD^{-1/2}$ has entries $\sqrt{\pi(x)}P(x, y)/\sqrt{\pi(y)}$, which is symmetric by detailed balance. Take an orthonormal basis $\varphi_j$ of [eigenvectors](/eigenvector/) of $A$, and let $f_j = D^{-1/2}\varphi_j$. Then the $f_j$ are eigenfunctions of $P$, orthonormal in $\langle\cdot, \cdot\rangle_\pi$, with $f_1 = 1$, and
$$
\frac{P^t(x, y)}{\pi(y)} = \sum_{j=1}^{|\mathcal X|}f_j(x)f_j(y)\lambda_j^t. \qquad (1)
$$
At $t = 0$, (1) gives $\sum_j f_j(x)f_j(y) = 1_{x = y}/\pi(y)$, so $\sum_{j \ge 2}f_j(x)^2 = 1/\pi(x) - 1$.

### The upper bound (LPW Theorem 12.4)

**Theorem.** For $P$ reversible and irreducible,
$$
t_{mix}(\varepsilon) \le \Big\lceil t_{rel}\Big(\tfrac12\log\frac1{\pi_{min}} + \log\frac1{2\varepsilon}\Big)\Big\rceil \le t_{rel}\log\frac1{\varepsilon\,\pi_{min}}.
$$
*Proof.* By (1) and the orthonormality of the $f_j$,
$$
\Big\|\frac{P^t(x, \cdot)}{\pi} - 1\Big\|_2^2 = \sum_{j \ge 2}\lambda_j^{2t}f_j(x)^2 \le \lambda_*^{2t}\Big(\frac1{\pi(x)} - 1\Big) \le \frac{\lambda_*^{2t}}{\pi_{min}}.
$$
By the $\ell^2$ bound on the page [total variation distance](/total-variation-distance/), $\|P^t(x, \cdot) - \pi\|_{TV}$ is at most half the left side's square root, so
$$
d(t) \le \frac{\lambda_*^t}{2\sqrt{\pi_{min}}} = \frac{(1 - \gamma_*)^t}{2\sqrt{\pi_{min}}} \le \frac{e^{-\gamma_* t}}{2\sqrt{\pi_{min}}}.
$$
The right side is at most $\varepsilon$ once $t \ge t_{rel}(\tfrac12\log(1/\pi_{min}) + \log(1/(2\varepsilon)))$. The second inequality of the theorem holds because $\tfrac12\log(1/\pi_{min}) + \log(1/(2\varepsilon)) \le \log(1/\pi_{min}) + \log(1/\varepsilon) - \log 2$, and the ceiling adds less than 1. $\square$

LPW also proves the same bound with $\log(1/(\varepsilon\pi_{min}))$ for the stronger $\ell^\infty$ mixing time, equation (12.11).

### The lower bound (LPW Theorem 12.5)

**Theorem.** Let $P$ be irreducible and aperiodic, and let $\lambda \ne 1$ be an eigenvalue of $P$. Then
$$
t_{mix}(\varepsilon) \ge \Big(\frac1{1 - |\lambda|} - 1\Big)\log\frac1{2\varepsilon}.
$$
For a reversible chain, with $|\lambda| = \lambda_*$, this is $t_{mix}(\varepsilon) \ge (t_{rel} - 1)\log\frac1{2\varepsilon}$.

*Proof.* Let $Pf = \lambda f$ with $f \ne 0$, complex if needed. Since $\pi P = \pi$, $\lambda\sum_y\pi(y)f(y) = \sum_y\pi(y)f(y)$, and $\lambda \ne 1$ gives $\sum_y\pi(y)f(y) = 0$. So for each $x$,
$$
|\lambda|^t|f(x)| = |P^tf(x)| = \Big|\sum_y\big(P^t(x, y) - \pi(y)\big)f(y)\Big| \le \|f\|_\infty\cdot 2d(t).
$$
Take $x$ with $|f(x)| = \|f\|_\infty$: $|\lambda|^t \le 2d(t)$. At $t = t_{mix}(\varepsilon)$ this gives $t\log(1/|\lambda|) \ge \log(1/(2\varepsilon))$. If $\lambda = 0$ the claim is trivial. Otherwise use $\log(1/|\lambda|) \le 1/|\lambda| - 1 = (1 - |\lambda|)/|\lambda|$, so $t \ge \frac{|\lambda|}{1 - |\lambda|}\log\frac1{2\varepsilon} = \big(\frac1{1 - |\lambda|} - 1\big)\log\frac1{2\varepsilon}$. $\square$

Together, with $\varepsilon = 1/4$: $(t_{rel} - 1)\log 2 \le t_{mix} \le \lceil t_{rel}(\tfrac12\log(1/\pi_{min}) + \log 2)\rceil$.

### The variational form (LPW Lemma 13.7 and Remark 13.8)

Let $Q(x, y) = \pi(x)P(x, y)$ and define the *Dirichlet form* $\mathcal E(f, f) = \langle(I - P)f, f\rangle_\pi = \frac12\sum_{x, y}Q(x, y)(f(x) - f(y))^2$. Then
$$
\gamma = \min\Big\{\frac{\mathcal E(f, f)}{\operatorname{Var}_\pi(f)} : f \text{ not constant}\Big\}.
$$
*Proof.* Write $f - \mathbb E_\pi f = \sum_{j \ge 2}a_jf_j$. Then $\mathcal E(f, f) = \sum_{j \ge 2}(1 - \lambda_j)a_j^2 \ge (1 - \lambda_2)\sum_{j \ge 2}a_j^2 = \gamma\operatorname{Var}_\pi(f)$, with equality at $f = f_2$. $\square$

This is a [Rayleigh quotient](/rayleigh-quotient/). Each test function $f$ gives an upper bound on $\gamma$; this proves the easy half of the [Cheeger inequality](/cheeger-inequality/). Lower bounds on $\gamma$ need an argument for all $f$, which is what [canonical paths](/canonical-paths/) provide.

### Why the absolute gap

The mixing bounds use $\gamma_*$, not $\gamma$. The simple walk on a 4-cycle has eigenvalues $1, 0, 0, -1$, so $\gamma = 1$, but $\gamma_* = 0$ and the walk never mixes, because it is periodic. The eigenvalue $-1$ is the period. Making the chain lazy moves each eigenvalue $\lambda$ to $(1 + \lambda)/2 \ge 0$, so $\gamma_*$ becomes $\gamma/2$, at the cost of a factor 2 in time.

## Examples

All values below were computed exactly from the matrices; the irrational ones are rounded.

| Chain | Eigenvalues | $\gamma$ | $\gamma_*$ | $t_{rel}$ | $t_{mix}$ |
|---|---|---|---|---|---|
| Land of Oz | $1, \tfrac14, -\tfrac14$ | $3/4$ | $3/4$ | $4/3$ | 1 |
| two states, $P(0,1) = a$, $P(1,0) = b$ | $1, 1 - a - b$ | $a + b$ | $1 - \lvert 1 - a - b\rvert$ | | |
| lazy hypercube $\{0,1\}^n$ | $1 - k/n$, multiplicity $\binom nk$ | $1/n$ | $1/n$ | $n$ | 3 for $n = 3$, 5 for $n = 4$ |
| lazy cycle, $n$ vertices | $\frac{1 + \cos(2\pi k/n)}{2}$ | $\frac{1 - \cos(2\pi/n)}{2}$ | same | about $n^2/\pi^2$ | 6 for $n = 8$ |
| simple walk on a 4-cycle | $1, 0, 0, -1$ | 1 | 0 | infinite | never |
| two triangles joined by an edge, lazy | | 0.1023 | 0.1023 | 9.77 | 8 |

For the lazy hypercube with $n = 3$ the upper bound of Theorem 12.4 is $\lceil 3(\tfrac12\log 8 + \log 2)\rceil = 6$ and the lower bound of Theorem 12.5 is $2\log 2 \approx 1.39$; the true value is 3. For the Land of Oz the bounds are $\lceil\tfrac43(\tfrac12\log 5 + \log 2)\rceil = 2$ and $\tfrac13\log 2 \approx 0.23$; the true value is 1. More rows are on the page [mixing time](/mixing-time/).

**The hypercube in detail.** The functions $\chi_S(x) = \prod_{i \in S}(-1)^{x_i}$ for $S \subseteq \{1, \ldots, n\}$ are eigenfunctions of the lazy walk. A step picks coordinate $i$ and sets it to a fair bit; if $i \in S$ the new value of $\chi_S$ has mean 0, and otherwise $\chi_S$ does not change. So $P\chi_S = (1 - |S|/n)\chi_S$.

**Cycles are slow.** On the lazy cycle with $n$ vertices, $\gamma \approx \pi^2/n^2$, so $t_{rel}$ grows like $n^2$. The walk needs order $n^2$ steps to cross a distance $n$, as for a diffusion.

## Where it is used

- **Mixing time bounds.** Theorem 12.4 is the standard way to turn a bound on $\gamma$ into a bound on $t_{mix}$. With $\log(1/\pi_{min})$ polynomial in the input size, a gap of $1/\text{poly}$ gives [rapid mixing](/rapid-mixing/).
- **Bounding the gap.** Lower bounds on $\gamma$ come from [conductance](/conductance/) through the [Cheeger inequality](/cheeger-inequality/), from [canonical paths](/canonical-paths/), and from comparison with a chain whose gap is known.
- **Variance of MCMC estimates.** For a reversible chain started in $\pi$, the asymptotic variance in the central limit theorem of the [ergodic theorem](/ergodic-theorem/) page is at most $\frac{2}{\gamma}\operatorname{Var}_\pi(f)$, because each eigenfunction $f_j$ contributes $\frac{1 + \lambda_j}{1 - \lambda_j}$ times its share of the variance.
- **Expanders.** A random walk on a graph with a large gap mixes in $O(\log n)$ steps. This is the basis of the [expander walk sampler](/expander-walk-sampler/).
- **Gossip and averaging.** Repeated averaging $x \leftarrow Wx$ with a symmetric doubly stochastic matrix $W$ converges to the mean at the rate $\lambda_*(W)^t$; see [averaging convergence and the spectral gap](/averaging-convergence-spectral-gap/).
- **Computation.** [Power iteration](/power-iteration/) for $\pi$, and for the [PageRank](/pagerank/) vector, converges at the rate $\lambda_*^t$.

## References
