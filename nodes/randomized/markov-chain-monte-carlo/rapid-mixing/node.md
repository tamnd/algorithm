---
tag: 74JBJ7
kind: concept
slug: rapid-mixing
name: Rapid mixing
aliases:
- rapidly mixing Markov chain
area: randomized/markov-chain-monte-carlo
level: advanced
summary: A family of chains mixes rapidly when t_mix is polynomial in log|Ω|, the size of a state, not in |Ω|. Then MCMC gives polynomial time samplers for exponentially large sets.
prereqs: [mixing-time, total-variation-distance, approximate-counting]
see_also: [mixing-time, coupling-method, path-coupling, canonical-paths, cheeger-inequality, conductance, fpras, glauber-dynamics]
sources:
  - paper: doi:10.1016/0890-5401(89)90067-9
    title: Alistair Sinclair and Mark Jerrum, Approximate counting, uniform generation and rapidly mixing Markov chains, Information and Computation 82(1), 1989
    locator: pages 93 to 133
  - paper: doi:10.1137/0218077
    title: Mark Jerrum and Alistair Sinclair, Approximating the permanent, SIAM Journal on Computing 18(6), 1989
    locator: the matching chain and its rapid mixing by canonical paths
  - paper: doi:10.1002/rsa.3240070205
    title: Mark Jerrum, A very simple algorithm for estimating the number of k-colorings of a low-degree graph, Random Structures and Algorithms 7(2), 1995
    locator: pages 157 to 165
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 4.5 (equation (4.34)); Section 14.3, Rapid Mixing for Colorings (Theorem 14.10); Section 18.2 (Theorem 18.3)
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Birkhäuser, 2003
    locator: Chapters 3 to 5 (sampling and counting, coupling, canonical paths)
---

A family of [Markov chains](/markov-chain/) is *rapidly mixing* when its [mixing time](/mixing-time/) grows only polynomially in $\log|\Omega|$, where $\Omega$ is the state space. In applications $\Omega$ is a set of combinatorial objects, such as the colorings or matchings of a graph, and $|\Omega|$ is exponential in the input size $n$, so $\log|\Omega|$ is polynomial in $n$. A rapidly mixing chain therefore gives a sampler that runs in time polynomial in $n$, although it visits only a tiny fraction of $\Omega$. With [self-reducibility](/self-reducibility/), such a sampler gives an [FPRAS](/fpras/) for counting the elements of $\Omega$.

## In plain words

A deck of 52 cards has more orders than there are atoms on Earth, yet seven good riffle shuffles make the order look random. The shuffle never comes close to visiting every order; it only needs to forget where it started. A rapidly mixing chain does the same for other huge sets: the colorings of a map, the matchings of a graph, the states of a magnet. Its number of steps grows with the size of one object, not with the number of objects. That is the difference between a method that is practical and one that is not. A chain that needs as many steps as there are objects is no better than listing them all. Proving that a chain mixes rapidly is the hard part of most results on random sampling and approximate counting.

## The idea

### The definition

Consider a family of ergodic chains, one for each instance $I$ of a problem, with state space $\Omega_I$, stationary distribution $\pi_I$ and mixing time $t_{mix}(I)$. The notation is that of the group: $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$. The family is **rapidly mixing** if
$$
t_{mix}(I) \le \operatorname{poly}(\log|\Omega_I|).
$$
In most uses $\log|\Omega_I|$ is polynomial in the size $n$ of $I$, and the condition is the same as $t_{mix} \le \operatorname{poly}(n)$.

The accuracy costs only a logarithm. By LPW (4.34), proved on [mixing time](/mixing-time/), $t_{mix}(\varepsilon) \le \lceil\log_2(1/\varepsilon)\rceil\,t_{mix}$. So a rapidly mixing chain reaches distance $\varepsilon$ in $\operatorname{poly}(n)\cdot\log(1/\varepsilon)$ steps.

### Why the logarithm

Any irreducible aperiodic chain mixes in some finite time, and many mix in time polynomial in $|\Omega|$. That is useless when $|\Omega|$ is $2^n$ or $n!$: a polynomial in $|\Omega|$ is more than the cost of listing $\Omega$. Rapid mixing asks for something much stronger, that the number of steps be comparable to the size of one state. Each step changes one small part of the state, so a chain cannot mix faster than the time needed to touch most parts. For many single-site chains on $n$ sites this lower bound is of order $n\log n$, by the coupon collector argument, and that order is reached by the best cases below.

### How to prove it

| Method | Gives | Page |
|---|---|---|
| Coupling, path coupling | $d(t) \le$ probability that two copies have not met | [coupling method](/coupling-method/), [path coupling](/path-coupling/) |
| Canonical paths | $\gamma \ge 1/B$ | [canonical paths](/canonical-paths/) |
| Conductance | $\gamma \ge \Phi_*^2/2$ | [conductance](/conductance/), [Cheeger inequality](/cheeger-inequality/) |
| Strong stationary times | $d(t) \le \Pr[\tau > t]$ | [strong uniform time](/strong-uniform-time/) |

The spectral bounds become mixing bounds through LPW Theorem 12.4: $t_{mix} \le \lceil t_{rel}(\tfrac12\log(1/\pi_{min}) + \log 2)\rceil$. For the uniform distribution on $\Omega$, $\log(1/\pi_{min}) = \log|\Omega|$, so a gap of $1/\operatorname{poly}(n)$ is enough. For a lazy reversible chain, by the Cheeger inequality and the bottleneck bound, rapid mixing holds exactly when $1/\Phi_*$ is polynomial, provided $\log(1/\pi_{min})$ is polynomial.

### How to disprove it

One bad set is enough: $t_{mix} \ge 1/(4\Phi(S))$ for any $S$ with $\pi(S) \le 1/2$ (LPW Theorem 7.4). Chains whose mixing time is exponential in $n$ are sometimes called *torpidly mixing*.

## Examples

| Chain | $\lvert\Omega\rvert$ | $t_{mix}$ | Rapid? |
|---|---|---|---|
| lazy walk on the hypercube $\{0,1\}^n$ | $2^n$ | $\tfrac12 n\log n$ to first order (LPW Theorem 18.3) | yes |
| [random transposition shuffle](/random-transposition-shuffle/) | $n!$ | $\tfrac12 n\log n$ to first order | yes |
| [top-to-random shuffle](/top-to-random-shuffle/) | $n!$ | order $n\log n$ | yes |
| [Glauber dynamics](/glauber-dynamics/) for proper $q$-colorings, $q > 2\Delta$ | up to $q^n$ | $\le \lceil\frac{q - \Delta}{q - 2\Delta}n(\log n + \log 4)\rceil$ (Jerrum 1995; LPW Theorem 14.10) | yes |
| Jerrum-Sinclair chain on matchings | up to exponential | polynomial (Jerrum and Sinclair 1989) | yes |
| lazy walk on a cycle with $n$ vertices | $n$ | order $n^2$ | no |
| two copies of $K_k$ joined by an edge, lazy | $2k$ | at least order $k^2$ | no |
| Glauber dynamics for the [Ising model](/ising-model/) on an $n \times n$ grid at low temperature | $2^{n^2}$ | exponential in $n$ | no |

The cycle and the two cliques are not rapidly mixing in the formal sense, because $n^2$ is not polynomial in $\log n$. This does not matter in practice for such small state spaces: they are the simplest examples of the two reasons for slow mixing, diffusion over a long distance and a bottleneck. For the Ising model at low temperature the bottleneck is exponential, and the [Swendsen-Wang](/swendsen-wang/) dynamics or [parallel tempering](/parallel-tempering/) are used instead of single-site updates.

**The exact numbers for small cases.** For the lazy hypercube, $t_{mix}$ is 1, 3 and 5 for $n = 2, 3, 4$. For Glauber dynamics on 5-colorings of a path with 3 vertices ($\Delta = 2$, 80 colorings), the exact $t_{mix}$ is 6, and the path coupling bound above is 23.

## Where it is used

- **Approximate counting.** By the [Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/), for a [self-reducible](/self-reducibility/) problem, almost uniform sampling in polynomial time and approximate counting in polynomial time are equivalent. A rapidly mixing chain gives the sampler. This is how FPRAS results were proved for [counting graph colorings](/counting-graph-colorings/) with many colors and [counting perfect matchings](/counting-perfect-matchings/) in dense bipartite graphs, and how Jerrum, Sinclair and Vigoda (2004) gave an FPRAS for the [permanent](/permanent-computation/) of a non-negative matrix.
- **Volume estimation.** The volume of a convex body in high dimension can be estimated in polynomial time with rapidly mixing random walks inside the body, while deterministic methods need exponential time.
- **Statistical physics.** Rapid mixing of Glauber dynamics marks the high-temperature phase of many spin systems, and its failure often marks a phase transition.
- **Practice.** In applied MCMC, rapid mixing is rarely proved. Diagnostics such as the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) cannot prove it, so they are no substitute for a bound.

## References
