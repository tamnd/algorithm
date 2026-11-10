---
tag: 1PQE8H
kind: definition
slug: randomized-online-algorithm
name: Randomized online algorithm
aliases:
- randomised online algorithm
area: online-and-streaming/competitive-analysis
level: intro
summary: An online algorithm that makes random choices, analysed against oblivious adversaries.
prereqs: [competitive-ratio, randomized-algorithm, expected-value]
see_also: [yao-minimax-principle, oblivious-adversary, adaptive-adversary, adaptive-offline-adversary, ski-rental-problem, randomized-marking, request-answer-game, minimax-theorem]
sources:
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the definition of randomized on-line algorithms and of the oblivious, adaptive online and adaptive offline adversaries
  - paper: doi:10.1007/BF01189993
    title: "Anna R. Karlin, Mark S. Manasse, Lyle A. McGeoch and Susan Owicki, Competitive randomized algorithms for nonuniform problems, Algorithmica 11(6) (1994), 542-571"
    locator: the randomized rent-or-buy rule with ratio tending to e/(e-1) against an oblivious adversary
  - paper: doi:10.1109/SFCS.1977.24
    title: "Andrew Chi-Chih Yao, Probabilistic computations: toward a unified measure of complexity, 18th Annual Symposium on Foundations of Computer Science (1977), 222-227"
    locator: the minimax principle for lower bounds on randomized algorithms
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the marking algorithm and the lower bound H_k for randomized paging
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 2 (randomized online algorithms), Chapter 4 (randomized paging) and Chapter 8 (Yao's principle)
---

A randomized online algorithm is an [online algorithm](/online-algorithm/) that may flip coins when it chooses its answers. Its cost on a fixed request sequence is a random variable, and its [competitive ratio](/competitive-ratio/) compares the expected cost with the [offline optimum](/offline-optimum/). Against the usual [oblivious adversary](/oblivious-adversary/), randomization can lower the best ratio a lot: from $2 - 1/B$ to about $e/(e-1) \approx 1.582$ for ski rental, and from $k$ to $\Theta(\log k)$ for paging.

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

In the [request-answer game](/request-answer-game/) model, a **randomized online algorithm** is one of the two equivalent objects:

- **A distribution over deterministic algorithms.** A probability distribution $\mu$ on the set of deterministic online algorithms $D = (g_1, g_2, \ldots)$. The algorithm draws $D \sim \mu$ once, before the first request, and then runs $D$. In game terms, this is a mixed strategy.
- **Coin flips during the run.** Before it answers $r_i$, the algorithm draws a random value $s_i$, and $a_i$ is a function of $r_1, \ldots, r_i$ and $s_1, \ldots, s_i$. In game terms, this is a behavioural strategy.

Each coin-flip algorithm defines a distribution over deterministic algorithms (fix all the coins in advance), and each distribution can be sampled with coins, so the two views give the same algorithms.

The cost $\mathrm{ALG}(\sigma)$ is a random variable over the coins. ALG is **$c$-competitive against an oblivious adversary** if there is a constant $b$ such that

$$\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b \quad \text{for every request sequence } \sigma.$$

The expectation is over the coins of ALG only. The sequence $\sigma$ is fixed before the coins are flipped. With $b = 0$ the algorithm is strictly $c$-competitive. The randomized competitive ratio of a problem is the infimum of $c$ over all randomized algorithms. When the adversary may see the coins, the definition changes: see [adaptive online adversary](/adaptive-adversary/) and [adaptive offline adversary](/adaptive-offline-adversary/). A claim about a randomized ratio is incomplete until it names the adversary.

**Yao's principle for lower bounds.** Let $\mathcal{D}$ be a probability distribution on request sequences. If every deterministic online algorithm $D$ satisfies $\mathbb{E}_{\sigma \sim \mathcal{D}}[D(\sigma)] \ge c \cdot \mathbb{E}_{\sigma \sim \mathcal{D}}[\mathrm{OPT}(\sigma)]$, then no randomized online algorithm is strictly $c'$-competitive against an oblivious adversary for any $c' < c$. Proof: if ALG $= \mu$ satisfied $\mathbb{E}_\mu[D(\sigma)] \le c' \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$, then averaging over $\sigma \sim \mathcal{D}$ and exchanging the two expectations gives some $D$ with $\mathbb{E}_{\mathcal{D}}[D(\sigma)] \le c' \cdot \mathbb{E}_{\mathcal{D}}[\mathrm{OPT}]$, a contradiction. This is the easy half of the [Yao minimax principle](/yao-minimax-principle/). For a bound on the ratio with an additive constant, the distribution must make $\mathbb{E}[\mathrm{OPT}]$ as large as needed, for example by scaling the costs.

## Examples and non-examples

**Worked example: randomized ski rental with $B = 4$.** Renting costs 1 per day, buying costs $B = 4$, and $\mathrm{OPT}(n) = \min(n, 4)$ for a season of $n$ days. The best deterministic rule has ratio $2 - 1/4 = 7/4$. The randomized rule draws the buy day $j \in \{1, 2, 3, 4\}$ with

$$\Pr[j = 1, 2, 3, 4] = \tfrac{27}{175}, \tfrac{36}{175}, \tfrac{48}{175}, \tfrac{64}{175},$$

that is $p_j \propto (3/4)^{4 - j}$. For a season of one day it pays 4 if $j = 1$ and 1 otherwise, so $\mathbb{E}[\mathrm{ALG}(1)] = (27 \cdot 4 + 148)/175 = 256/175$. The same computation for each $n$ gives $\mathbb{E}[\mathrm{ALG}(n)] = \tfrac{256}{175} \min(n, 4)$ for every $n \ge 1$. So the rule is strictly $256/175 \approx 1.463$-competitive against an oblivious adversary.

**Yao's lower bound for the same game.** Let the season length $n$ be 1, 2 or 3 with probabilities $1/4, 3/16, 9/64$, and 7 with probability $27/64$. Then $\mathbb{E}[\mathrm{OPT}] = (16 + 24 + 27 + 4 \cdot 27)/64 = 175/64$. A deterministic rule that buys on day $j \le 4$, or never buys before day 8, has expected cost exactly 4. A rule that buys on day 5, 6 or 7 pays more. So every deterministic rule has $\mathbb{E}[D] / \mathbb{E}[\mathrm{OPT}] \ge 4 \cdot 64/175 = 256/175$, and by Yao's principle no randomized rule is strictly better than $256/175$-competitive. The randomized rule above is optimal.

For general $B$ the same two constructions give the optimal strict ratio $c_B = 1/(1 - (1 - 1/B)^B)$, which increases to $e/(e-1)$ as $B \to \infty$ (Karlin, Manasse, McGeoch and Owicki 1994). The [ski rental problem](/ski-rental-problem/) derives the optimal distribution of the continuous version.

**Paging.** [Randomized marking](/randomized-marking/) evicts a uniformly random unmarked page on each fault. It is $2H_k$-competitive against an oblivious adversary, where $H_k$ is the $k$-th [harmonic number](/harmonic-series/), and no randomized algorithm beats $H_k$ (Fiat et al. 1991). Every deterministic paging algorithm has ratio at least $k$.

**Non-example: a deterministic algorithm on a random input.** An [average-case analysis](/average-case-analysis/) fixes a distribution on inputs and runs a deterministic algorithm. A randomized online algorithm must do well on every input, with only its own coins random.

**Non-example: coins that the adversary can see.** If the adversary sees each answer before it chooses the next request, then for paging the expected ratio of any randomized algorithm is at least $k$, the same as for deterministic algorithms. Against the [adaptive offline adversary](/adaptive-offline-adversary/), randomization never helps.

## Related definitions

- **[Randomized algorithm](/randomized-algorithm/).** The general notion. A randomized online algorithm is usually of the [Las Vegas](/las-vegas-algorithm/) kind: its answers are always valid, and only the cost is random.
- **[Oblivious adversary](/oblivious-adversary/).** Fixes $\sigma$ before the coins are flipped. The standard model.
- **[Adaptive online adversary](/adaptive-adversary/) and [adaptive offline adversary](/adaptive-offline-adversary/).** Stronger adversaries that see the coins through the answers.
- **[Yao minimax principle](/yao-minimax-principle/).** The tool for randomized lower bounds, from the [minimax theorem](/minimax-theorem/) for [zero-sum games](/zero-sum-game/).
- **[Advice model](/advice-model/).** Advice of $b$ bits chooses among $2^b$ deterministic algorithms; a randomized algorithm chooses among them at random.

## References
