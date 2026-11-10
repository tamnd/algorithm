---
tag: WVJRD2
kind: problem
slug: sampling-from-stationary-distribution
name: Sampling from a stationary distribution
aliases:
- MCMC sampling problem
area: randomized/markov-chain-monte-carlo
level: intro
summary: Given a target distribution π, often known only up to a constant, output a random state whose law is within ε of π in total variation. MCMC solves it by running a chain with stationary law π.
prereqs: [stationary-distribution, mixing-time, total-variation-distance]
see_also: [metropolis-hastings, gibbs-sampling, glauber-dynamics, exact-sampling-from-stationary-distribution, mixing-time, burn-in, effective-sample-size, rejection-sampling]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Chapter 3, Markov Chain Monte Carlo, Metropolis and Glauber Chains; Section 4.5 (equation (4.34)); Theorem 7.4
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 6, Markov Chains; Chapter 7, The Metropolis-Hastings Algorithm
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng, editors, Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 1, Introduction to Markov chain Monte Carlo
  - paper: "Mark R. Jerrum, Leslie G. Valiant and Vijay V. Vazirani, Random generation of combinatorial structures from a uniform distribution, Theoretical Computer Science 43, 1986"
    locator: the equivalence of almost uniform sampling and approximate counting for self-reducible problems
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Birkhäuser, 2003
    locator: Chapter 3, Sampling and counting
---

Sampling from a stationary distribution is the problem of producing a random state whose law is close to a given target distribution $\pi$ on a large state space, when $\pi$ is known only through weights $w(x)$ with $\pi(x) = w(x)/Z$ and the constant $Z$ is too costly to compute. Markov chain Monte Carlo, for example [Metropolis-Hastings](/metropolis-hastings/), solves it: build a [Markov chain](/markov-chain/) whose [stationary distribution](/stationary-distribution/) is $\pi$, run it for enough steps, and output the last state. The approximation is measured in [total variation distance](/total-variation-distance/), and the cost is governed by the [mixing time](/mixing-time/). This page is about approximate samples; for samples with law exactly $\pi$ see [exact sampling from a stationary distribution](/exact-sampling-from-stationary-distribution/).

## In plain words

Suppose you want a random proper coloring of a big map, with every coloring equally likely. There are far too many colorings to list, so you cannot just pick one from a list. Instead, start from any coloring and change it a little at a time, for example by recoloring one region with a color its neighbors do not use. The rules are chosen so that, in the long run, the process spends equal time on every coloring. After enough changes, the current coloring is almost a fair random pick. The questions are how many changes are enough, and how to tell. Theory can answer the first question for some processes. Watching the process cannot answer it with certainty, because a process that is stuck in one part of the space can look settled.

## Definition

**Input.**

- A finite state space $\mathcal X$, usually given implicitly, such as the proper $q$-colorings of a graph $G$ with $n$ vertices.
- A weight function $w : \mathcal X \to (0, \infty)$ that can be computed for each state. The target is $\pi(x) = w(x)/Z$ with $Z = \sum_xw(x)$.
- An accuracy $\varepsilon \in (0, 1)$.

**Output.** A random state $X$ with $\|\mathcal L(X) - \pi\|_{TV} \le \varepsilon$, where $\mathcal L(X)$ is the law of $X$.

**The MCMC solution.** Choose an irreducible aperiodic transition matrix $P$ with $\pi P = \pi$, usually by [detailed balance](/detailed-balance/). With $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$, run the chain from any $x_0$ for $t \ge t_{mix}(\varepsilon)$ steps and output $X_t$. Its law is $P^t(x_0, \cdot)$, which is within $d(t) \le \varepsilon$ of $\pi$.

A family of instances has a polynomial time *almost uniform sampler* when the running time is polynomial in the input size $n$ and in $\log(1/\varepsilon)$.

## Variants

- **Uniform targets.** $w \equiv 1$ on a combinatorial set, such as matchings, colorings, independent sets or spanning trees.
- **Gibbs distributions.** $w(x) = e^{-\beta H(x)}$ for an energy $H$, as in the [Ising model](/ising-model/) and the [hard-core model](/hard-core-model/).
- **Bayesian posteriors.** $w(\theta) = $ likelihood times prior, on a continuous space. Total variation is then defined with densities, and the chains are [random-walk Metropolis](/random-walk-metropolis/), [Gibbs sampling](/gibbs-sampling/) or [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/).
- **Many samples.** Run independent chains, or take states far apart in one long run. Successive states of one chain are correlated; see [thinning](/thinning/) and [autocorrelation](/mcmc-autocorrelation/).
- **Expectations instead of samples.** Estimate $\mathbb E_\pi f$ by the average of $f(X_s)$ over a run. The [ergodic theorem](/ergodic-theorem/) gives convergence, and the error is measured by the [effective sample size](/effective-sample-size/).
- **Exact samples.** Ask for $\mathcal L(X) = \pi$ exactly, in a random but finite time; see [exact sampling from a stationary distribution](/exact-sampling-from-stationary-distribution/).

## Examples

**The Land of Oz.** The weather chain on $\{R, N, S\}$ with
$$
P = \begin{pmatrix}1/2 & 1/4 & 1/4\\ 1/2 & 0 & 1/2\\ 1/4 & 1/4 & 1/2\end{pmatrix}
$$
has $\pi = (2/5, 1/5, 2/5)$ and $d(t) = \tfrac45\cdot4^{-t}$, computed exactly. One step from $R$ already gives distance $3/20$. So $t_{mix} = 1$ and $t_{mix}(1/100) = 4$: four steps from any start give a sample within $1/100$ of $\pi$.

**Colorings.** For the 5-colorings of a path with 3 vertices, $|\mathcal X| = 80$ and $\pi$ is uniform. [Glauber dynamics](/glauber-dynamics/) has exact $t_{mix} = 6$, and the path coupling bound gives 23.

**A slow example.** For the lazy walk on two copies of $K_4$ joined by an edge, $\pi$ is proportional to the degree, the exact $t_{mix}$ is 14 and $t_{mix}(1/100) = 69$, although there are only 8 states. A bottleneck slows the chain, and a run of fewer steps returns states from the starting clique too often.

## Known algorithms

| method | idea | exact? | needs |
|---|---|---|---|
| [inverse transform sampling](/inverse-transform-sampling/) | invert the cumulative distribution | yes | $Z$ and a list of $\mathcal X$ |
| [rejection sampling](/rejection-sampling/) | propose from a simpler law, accept with probability $w/(Mg)$ | yes | a bound $M$ on $w/g$ |
| [Metropolis-Hastings](/metropolis-hastings/) | propose a move, accept with the Hastings ratio | no | ratios $w(y)/w(x)$ |
| [Gibbs sampling](/gibbs-sampling/), [Glauber dynamics](/glauber-dynamics/) | resample one coordinate from its conditional law | no | the conditional laws |
| [random-walk Metropolis](/random-walk-metropolis/), [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) | Metropolis-Hastings with local or gradient-based proposals | no | $w$, and its gradient for HMC |
| [Swendsen-Wang](/swendsen-wang/), [parallel tempering](/parallel-tempering/) | large moves across bottlenecks | no | model structure, or a ladder of temperatures |
| [coupling from the past](/coupling-from-the-past/) | run coupled chains from the past until they coalesce | yes | a grand coupling, often monotone |
| [Wilson's algorithm](/wilson-algorithm/) | loop-erased random walks | yes | for uniform spanning trees |

## Bounds

- **Upper bounds.** With an MCMC method the cost is $t_{mix}(\varepsilon)$ times the cost of a step. By LPW (4.34), $t_{mix}(\varepsilon) \le \lceil\log_2(1/\varepsilon)\rceil\,t_{mix}$, so high accuracy is cheap once $t_{mix}$ is known. Proven bounds on $t_{mix}$ come from [coupling](/coupling-method/), [path coupling](/path-coupling/), the [spectral gap](/spectral-gap/) and [canonical paths](/canonical-paths/).
- **Lower bounds.** Any set $S$ with $\pi(S) \le 1/2$ gives $t_{mix} \ge 1/(4\Phi(S))$ (LPW Theorem 7.4); see [conductance](/conductance/). A chain whose moves change one site needs about $n\log n$ steps on $n$ sites before most sites have been touched.
- **No test can certify convergence.** From the output of finitely many steps alone one cannot prove that $d(t) \le \varepsilon$: a chain trapped behind a bottleneck can look stationary. Diagnostics such as the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) and [burn-in](/burn-in/) rules detect some failures but prove nothing.
- **Hardness.** For some targets no polynomial time almost uniform sampler exists unless $\mathrm{NP} = \mathrm{RP}$. An example is the hard-core model on graphs of maximum degree $\Delta$ with fugacity above the uniqueness threshold (Sly 2010, with later extensions).

## Reductions

- **Counting.** For [self-reducible](/self-reducibility/) problems, polynomial time almost uniform sampling and polynomial time [approximate counting](/approximate-counting/) are equivalent ([Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/)). A [rapidly mixing](/rapid-mixing/) chain thus gives an [FPRAS](/fpras/).
- **Exact sampling is stronger.** An exact sampler solves this problem for every $\varepsilon$. The converse fails in general.
- **Integration.** $\mathbb E_\pi f$ and ratios of normalizing constants reduce to sampling, as in [Monte Carlo integration](/monte-carlo-integration/) and [importance sampling](/importance-sampling/).

## Applications

- Bayesian statistics, where the posterior is known up to its normalizing constant.
- Statistical physics, for the Ising, Potts and hard-core models.
- Approximate counting of [graph colorings](/counting-graph-colorings/), [perfect matchings](/counting-perfect-matchings/) and other combinatorial structures.
- Estimating volumes of convex bodies and integrals in high dimension.
- Ranking on graphs: [PageRank](/pagerank/) is the stationary distribution of a random surfer, and it can be estimated by simulating the walk.

## References
