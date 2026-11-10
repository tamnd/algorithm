---
tag: DC4W3C
kind: definition
slug: oblivious-adversary
name: Oblivious adversary
aliases:
- oblivious adversary model
- oblivious input model
area: online-and-streaming/competitive-analysis
level: intro
summary: An adversary that fixes the whole input in advance, without seeing the random choices of the algorithm.
prereqs: [randomized-online-algorithm]
see_also: [adaptive-adversary, adaptive-offline-adversary, request-answer-game, yao-minimax-principle, randomized-marking, ski-rental-problem, competitive-ratio, average-case-analysis]
sources:
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the oblivious adversary and its place among the three adversaries
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 2 (the oblivious adversary) and Chapter 7 (the adversary models for request-answer games)
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the marking algorithm, 2H_k-competitive against an oblivious adversary, and the H_k lower bound
---

An oblivious adversary chooses the whole request sequence $\sigma$ before a [randomized online algorithm](/randomized-online-algorithm/) starts, without seeing the algorithm's coins, and pays the [offline optimum](/offline-optimum/) $\mathrm{OPT}(\sigma)$. It knows the algorithm, including the probability distribution of its random choices. It is the weakest of the three adversaries of Ben-David, Borodin, Karp, Tardos and Wigderson (1994), and the standard model for randomized [competitive ratios](/competitive-ratio/).

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

Let ALG be a randomized online algorithm in a [request-answer game](/request-answer-game/). An **oblivious adversary** is a finite request sequence $\sigma$, chosen with knowledge of the code of ALG but not of its random bits. The adversary's cost is $\mathrm{OPT}(\sigma)$. ALG is **$c$-competitive against oblivious adversaries** if there is a constant $b$ such that

$$\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b \quad \text{for every } \sigma,$$

where the expectation is over the coins of ALG. With $b = 0$, ALG is strictly $c$-competitive.

The adversary gains nothing by choosing $\sigma$ at random: the left side is linear in a distribution on $\sigma$, so a worst single $\sigma$ is as bad as any mix. So the oblivious adversary is the same as a worst-case fixed input. For a deterministic algorithm, the adversary can predict every answer, and the definition is the ordinary deterministic competitive ratio.

## Examples and non-examples

- **Ski rental.** Against an oblivious adversary, the rule that buys on a random day with the right distribution has expected ratio $1/(1 - (1 - 1/B)^B)$, which tends to $e/(e-1) \approx 1.582$. The best deterministic ratio is $2 - 1/B$. See [ski rental](/ski-rental-problem/).
- **Paging.** [Randomized marking](/randomized-marking/) is $2H_k$-competitive against an oblivious adversary, and every randomized algorithm has ratio at least $H_k$ (Fiat et al. 1991), where $H_k$ is the $k$-th [harmonic number](/harmonic-series/). Every deterministic algorithm has ratio at least $k$. Since $H_k \approx \ln k$, randomization lowers the ratio from $k$ to $\Theta(\log k)$.
- **Why it can not exploit the coins.** In paging with $k + 1$ pages, an adversary that sees the cache would always request the one page that is missing and force a fault on every request. The oblivious adversary does not know which page is missing. It can hit the missing page only with some probability, and the analysis of marking bounds that probability.
- **Non-example: the adaptive online adversary.** An adversary that picks each request after it sees the past answers, and serves the requests online, is the [adaptive online adversary](/adaptive-adversary/). Against it, every randomized paging algorithm has ratio at least $k$.
- **Non-example: the adaptive offline adversary.** An adversary that picks the requests after it sees the past answers and then pays $\mathrm{OPT}$ of the final sequence is the [adaptive offline adversary](/adaptive-offline-adversary/). Against it, randomization does not help at all.
- **Non-example: a random input.** A fixed distribution on inputs, with the algorithm free to depend on it, is an [average-case analysis](/average-case-analysis/). The oblivious adversary may choose the worst input for the algorithm. The two meet in the [Yao minimax principle](/yao-minimax-principle/), which proves lower bounds against oblivious adversaries with a hard input distribution.

When the oblivious model fits: when the requests come from a process that does not react to the algorithm's random choices. When a later request depends on an earlier answer (for example, a user who sees which page was evicted, or a scheduler whose timing depends on the faults), an adaptive model is safer.

## Related definitions

- **[Adaptive online adversary](/adaptive-adversary/).** Chooses each request after seeing the answers and serves the requests online. Stronger than oblivious.
- **[Adaptive offline adversary](/adaptive-offline-adversary/).** Chooses each request after seeing the answers and pays the offline optimum. The strongest of the three.
- **The hierarchy.** For a fixed algorithm, $c$-competitive against adaptive offline adversaries implies $c$-competitive against adaptive online adversaries, which implies $c$-competitive against oblivious adversaries.
- **[Randomized online algorithm](/randomized-online-algorithm/).** The algorithms this adversary is used for.
- **[Request-answer game](/request-answer-game/).** The general framework of the three adversaries.

## References
