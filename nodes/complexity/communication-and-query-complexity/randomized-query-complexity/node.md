---
tag: 04WGR8
kind: concept
slug: randomized-query-complexity
name: Randomized query complexity
aliases:
- R(f)
area: complexity/communication-and-query-complexity
level: advanced
summary: "R(f) is the fewest worst-case queries of a randomized algorithm that computes f with error at most 1/3 on every input. For total f, bs(f) is at most 3 R(f) and D^dt(f) is at most 27 R(f)^3."
prereqs: [decision-tree-complexity, block-sensitivity, randomized-algorithm]
see_also: [decision-tree-complexity, block-sensitivity, yao-minimax-principle, game-tree-evaluation, quantum-query-complexity, randomized-communication-complexity, las-vegas-algorithm, monte-carlo-algorithm]
sources:
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (bs(f) at most 3 R(f) and D(f) at most 27 R(f)^3 for total f); conference version in STOC 1989, pp. 327 to 335
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 2 (randomized decision trees, R_0, R_1 and R_2), Section 5.2 (randomized complexity and its relations)
  - paper: doi:10.1109/SFCS.1986.44
    title: Michael Saks and Avi Wigderson, Probabilistic Boolean decision trees and the complexity of evaluating game trees, 27th IEEE Symposium on Foundations of Computer Science (FOCS 1986)
    locator: pp. 29 to 38 (zero-error complexity of the NAND tree, with exponent log2((1 + sqrt 33)/4))
  - paper: doi:10.1109/SFCS.1977.24
    title: Andrew Chi-Chih Yao, Probabilistic computations, toward a unified measure of complexity, 18th IEEE Symposium on Foundations of Computer Science (FOCS 1977)
    locator: pp. 222 to 227 (the minimax principle)
  - paper: doi:10.1145/3106234
    title: Andris Ambainis, Kaspars Balodis, Aleksandrs Belovs, Troy Lee, Miklos Santha and Juris Smotrovs, Separations in query complexity based on pointer functions, Journal of the ACM 64(5) (2017)
    locator: Article 32 (total functions with D = Omega(n) and R_0 = O~(sqrt n), and with R_0 = Omega(n / log n) and R = O~(sqrt n)); conference version in STOC 2016
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees (randomized decision trees and Yao's principle)
---

Randomized query complexity measures how many input bits an algorithm must read when it may flip coins. A randomized query algorithm is a probability distribution over deterministic decision trees, and $R(f)$ is the least worst-case number of queries of such an algorithm that outputs $f(x)$ with probability at least $2/3$ on every input $x$. Zero-error and one-sided variants give $R_0(f)$ and $R_1(f)$. For total functions the randomized measures are polynomially related to the deterministic one, $D^{dt}(f) \le 27 R(f)^3$, but randomness can still save a polynomial factor, as for the NAND tree.

## In plain words

You must answer a yes or no question about a hidden row of bits, and each look at a bit costs one coin. Now you may also toss coins to choose where to look. You must be right with a good chance, say two times out of three, on every row, not just on most rows. Randomized query complexity is the fewest looks that such a plan needs in its worst case. Coins help when a smart random order often finds the answer early, as in a game tree where one good move is enough. They help much less for questions where any single hidden bit could matter: then the plan must look at a fair share of the bits.

## The idea

**Definitions.** Let $f : \{0,1\}^n \to \{0,1\}$. A **randomized decision tree** is a probability distribution $\mu$ over deterministic decision trees. On input $x$ it picks a tree $T \sim \mu$ and outputs $T(x)$. Its cost is the largest depth of a tree in the support of $\mu$, a worst-case bound.

- $R(f)$, also written $R_2(f)$: the least cost of a randomized tree with $\Pr[T(x) = f(x)] \ge 2/3$ for every $x$. This is **two-sided bounded error**.
- $R_1(f)$: the least cost when the algorithm never errs on 0-inputs and errs with probability at most $1/2$ on 1-inputs. This is **one-sided error**; some sources use a different constant, which changes $R_1$ by at most a constant factor.
- $R_0(f)$: the least, over trees that are always correct, of the largest expected number of queries $\max_x \mathbb{E}_T[\text{queries of } T \text{ on } x]$. This is **zero error**; such an algorithm is a [Las Vegas algorithm](/las-vegas-algorithm/), and the others are [Monte Carlo algorithms](/monte-carlo-algorithm/).

The constant $1/3$ does not matter. Run the algorithm $k$ times and take the majority answer: by a Chernoff bound the error falls exponentially in $k$, so any constant error below $1/2$ changes $R$ by at most a constant factor. Zero error with expected cost converts to bounded error with worst-case cost: stop after $3 R_0(f)$ queries and output 0; by Markov's inequality this fails with probability at most $1/3$, so $R(f) \le 3 R_0(f)$.

**Easy relations.** $R_0(f) \le D^{dt}(f) \le n$, and $R(f) \le 3 R_0(f)$ as above. Also $C(f) \le R_0(f)$: on input $x$, every tree in the support queries a certificate for $x$ on its path, because it is always correct, so it makes at least $C(f, x)$ queries. With $D^{dt}(f) \le C_0(f) \, C_1(f)$ this gives $D^{dt}(f) \le R_0(f)^2$ for total $f$.

**Theorem (Nisan 1991).** For every total $f$, $\mathrm{bs}(f) \le 3 R(f)$. So $D^{dt}(f) \le \mathrm{bs}(f)^3 \le 27 R(f)^3$.

*Proof.* Let $A$ be a randomized algorithm with at most $T$ queries and error at most $1/3$. Let $x$ have disjoint sensitive blocks $B_1, \ldots, B_b$. Fix the coins $r$ of $A$. The run of $A$ on $x$ and the run on $x^{B_j}$ are the same until the first query into $B_j$. Let $E_j$ be the event, over $r$, that the run on $x$ queries some bit of $B_j$. Without $E_j$, the two runs are the same and give the same output.

Since $f(x) \ne f(x^{B_j})$, the outputs on $x$ and on $x^{B_j}$ must differ whenever both runs are correct. Each run is correct with probability at least $2/3$, so both are correct with probability at least $1/3$. So $\Pr[E_j] \ge 1/3$ for each $j$.

Each query of the run on $x$ lies in at most one block, because the blocks are disjoint. So $\sum_j \Pr[E_j] \le \mathbb{E}[\text{queries on } x] \le T$. Then $b/3 \le T$, and $\mathrm{bs}(f) \le 3 R(f)$. The bound on $D^{dt}$ follows with $D^{dt}(f) \le \mathrm{bs}(f)^3$ from the [decision tree complexity](/decision-tree-complexity/) page. $\square$

**Lower bounds by distributions.** [Yao's minimax principle](/yao-minimax-principle/) says that $R(f)$ is at least the least cost of a deterministic tree that errs with probability at most $1/3$ on a random input from any fixed distribution. For PARITY, take the uniform distribution. A deterministic tree whose paths all have fewer than $n$ queries leaves a free bit at each leaf, so its output is right on exactly half of the inputs that reach the leaf. Its error is $1/2$, so $R(\mathrm{PARITY}) = n$.

**Upper bounds.** Randomness helps when there are many short certificates and a random order finds one soon.

- **OR.** Query a uniformly random set of $\lceil 2n/3 \rceil$ positions and output 1 if a 1 is seen. If $x$ has a 1 at some position, the set misses that position with probability at most $1/3$. So $R(\mathrm{OR}) \le \lceil 2n/3 \rceil$, with one-sided error, and $R(\mathrm{OR}) \ge \mathrm{bs}(\mathrm{OR})/3 = n/3$. With zero error, the all-zero input forces every run to read all $n$ bits, so $R_0(\mathrm{OR}) = n$.
- **NAND trees.** Take the complete binary tree of depth $d$ with NAND gates and $n = 2^d$ leaves; this is [game tree evaluation](/game-tree-evaluation/). Every deterministic tree needs all $n$ leaves. The randomized algorithm evaluates the two children of each gate in random order and skips the second child when the first one has value 0. Its worst-case expected cost $W_d$ satisfies $W_d(0) = 2 W_{d-1}(1)$ and $W_d(1) = W_{d-1}(0) + W_{d-1}(1)/2$, so it grows as $\lambda^d = n^{\log_2 \lambda}$ with $\lambda = (1 + \sqrt{33})/4$, that is, $n^{0.7537}$. Saks and Wigderson proved that this is optimal for zero error.

## Examples

**NAND tree, exact expected costs.** The recursion above gives these worst-case expected numbers of queries. A brute-force pass over all inputs confirms the values for $d \le 4$.

| depth $d$ | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|---|
| leaves $n$ | 2 | 4 | 8 | 16 | 32 | 64 | 256 | 1024 |
| worst expected queries | 2 | 3 | 5.5 | 8.75 | 15.375 | 25.19 | 72.05 | 205.45 |
| $n^{0.7537}$ | 1.69 | 2.84 | 4.79 | 8.08 | 13.63 | 22.98 | 65.34 | 185.75 |

At $n = 1024$, the randomized algorithm reads about 205 leaves on its worst input, while every deterministic algorithm reads all 1024. The ratio to $n^{0.7537}$ stays near $1.1$, as the eigenvalue analysis predicts.

**The usual functions.**

| function | $D^{dt}$ | $R_0$ | $R$ |
|---|---|---|---|
| OR on $n$ bits | $n$ | $n$ | between $n/3$ and $\lceil 2n/3 \rceil$ |
| PARITY on $n$ bits | $n$ | $n$ | $n$ |
| MAJORITY on $n$ bits | $n$ | $\Theta(n)$ | $\Theta(n)$ |
| NAND tree, $n$ leaves | $n$ | $\Theta(n^{0.7537})$ | $O(n^{0.7537})$ |

For MAJORITY, $\mathrm{bs} = \lceil (n+1)/2 \rceil$ already gives $R \ge (n + 1)/6$.

**Separations for total functions.** How far can $R_0$ and $R$ be below $D^{dt}$? The bound $D^{dt} \le R_0^2$ says at most quadratic for zero error. The pointer functions of Ambainis, Balodis, Belovs, Lee, Santha and Smotrovs (2017) reach this up to log factors: a total function with $D^{dt} = \Omega(n)$ and $R_0 = \tilde O(\sqrt n)$. A second pointer function has $R_0 = \Omega(n / \log n)$ and $R = \tilde O(\sqrt n)$, so zero error and bounded error also differ almost quadratically. Between $D^{dt}$ and $R$, the best known upper bound is the cubic one of Nisan.

## Where it is used

- **Lower bounds for randomized algorithms.** Any algorithm that reads its input through queries, such as a sublinear-time algorithm, inherits a lower bound from $R(f)$. The two standard methods are the block argument of Nisan and [Yao's minimax principle](/yao-minimax-principle/).
- **Game tree search.** The NAND tree result explains why random move ordering helps alpha-beta search on worst-case trees; see [game tree evaluation](/game-tree-evaluation/).
- **Communication complexity.** A randomized query algorithm gives a randomized protocol for composed functions, and lifting results go the other way; see [randomized communication complexity](/randomized-communication-complexity/).
- **Quantum comparison.** $Q(f) \le R(f)$, and for total $f$ the gap is at most polynomial; see [quantum query complexity](/quantum-query-complexity/). For OR, $R = \Theta(n)$ but $Q = \Theta(\sqrt n)$.

## References
