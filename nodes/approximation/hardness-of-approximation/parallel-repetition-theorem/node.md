---
tag: 6R8CMX
kind: theorem
slug: parallel-repetition-theorem
name: Parallel repetition theorem
aliases:
- Raz's parallel repetition theorem
- parallel repetition
area: approximation/hardness-of-approximation
level: research
summary: Playing a two-prover one-round game of value below 1 many times in parallel drives the value down exponentially in the number of rounds, with a rate that depends on the answer size.
prereqs: [two-prover-one-round-game, label-cover, gap-problem]
see_also: [gap-amplification, hastad-3bit-pcp, unique-games-conjecture, set-cover-inapproximability, pcp-theorem, multi-prover-interactive-proofs, gap-preserving-reduction]
sources:
  - paper: "Ran Raz, A parallel repetition theorem, SIAM Journal on Computing 27(3), 763 to 803, 1998 (STOC 1995)"
    locator: the main theorem, the bound (1 - epsilon^32) to the power Omega(k / log s)
  - paper: doi:10.4086/toc.2009.v005a008
    title: Thomas Holenstein, Parallel repetition, simplifications and the no-signaling case, Theory of Computing 5, 141 to 172, 2009 (STOC 2007)
    locator: the main theorem with exponent 3 and its proof by correlated sampling
  - paper: "Anup Rao, Parallel repetition in projection games and a concentration bound, SIAM Journal on Computing 40(6), 1871 to 1891, 2011 (STOC 2008)"
    locator: the bound for projection games with no dependence on the answer size
  - paper: "Ran Raz, A counterexample to strong parallel repetition, Proceedings of the 49th IEEE Symposium on Foundations of Computer Science (FOCS), 2008"
    locator: the lower bound for the repeated odd cycle game
  - paper: "Uriel Feige and Oleg Verbitsky, Error reduction by parallel repetition, a negative result, Combinatorica 22(4), 2002"
    locator: games where the number of repetitions needed depends on the answer size
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, Proceedings of the 46th ACM Symposium on Theory of Computing (STOC), 2014
    locator: the bound for projection games with explicit constants
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 22, Section 22.3 (parallel repetition and the hardness of 2CSP over large alphabets)
---

The parallel repetition theorem says that if a [two-prover one-round game](/two-prover-one-round-game/) $G$ has value at most $1 - \varepsilon$, then the game $G^{\otimes k}$, which asks $k$ independent question pairs at once and accepts only if all $k$ checks pass, has value at most $(1 - \varepsilon^{c})^{\Omega(k / \log s)}$, where $s$ is the number of possible answers and $c$ is an absolute constant. Ran Raz proved it in 1995. The value does not fall like $\operatorname{val}(G)^k$ in general, because the provers can correlate their answers across the coordinates, and the dependence on the answer size cannot be dropped for general games. The theorem turns the constant gap of the [PCP theorem](/pcp-theorem/) into the arbitrarily small soundness of [label cover](/label-cover/), which is the start of most tight [hardness of approximation](/hastad-3bit-pcp/) results.

## Statement

Let $G = (X, Y, A, B, \mu, V)$ be a two-prover one-round game and $s = |A| \cdot |B|$. The $k$-fold parallel repetition $G^{\otimes k}$ has questions $\bar x \in X^k$ and $\bar y \in Y^k$, where the pairs $(x_j, y_j)$ are drawn independently from $\mu$, answers $\bar a \in A^k$ and $\bar b \in B^k$, and accepts when $V(x_j, y_j, a_j, b_j) = 1$ for every $j \in [k]$.

**Easy bounds.** For every game and every $k \ge 1$,

$$\operatorname{val}(G)^k \le \operatorname{val}(G^{\otimes k}) \le \operatorname{val}(G).$$

**Theorem (Raz 1998; Holenstein 2009).** There is an absolute constant $c' > 0$ such that for every $\varepsilon \in (0, 1]$, every game $G$ with $\operatorname{val}(G) \le 1 - \varepsilon$ and every $k \ge 1$,

$$\operatorname{val}(G^{\otimes k}) \le \big(1 - \varepsilon^{3}\big)^{c' k / \log s} .$$

Raz proved this with $\varepsilon^{32}$ in place of $\varepsilon^3$, and Holenstein improved the exponent to $3$. Taking $\log \max(|A|, |B|)$ instead of $\log s$ changes the exponent by at most a factor of $2$.

**Theorem (Rao 2011).** There is an absolute constant $c'' > 0$ such that for every *projection* game $G$ with $\operatorname{val}(G) \le 1 - \varepsilon$,

$$\operatorname{val}(G^{\otimes k}) \le \big(1 - \varepsilon^{2}\big)^{c'' k} ,$$

with no dependence on the answer size. Dinur and Steurer (2014) give an analytic proof for projection games with explicit constants, of the form $(1 - \varepsilon^2/16)^k$.

## In plain words

Two people who cannot talk are each asked one question, and they win if their answers fit together. If they can win at most a fixed fraction of the time, one might expect that asking many independent pairs of questions at once, and requiring all answers to fit, makes winning exponentially unlikely. That is true, but the proof is hard and the speed is slower than the naive guess. The players see all their questions at once, so they can choose answers that win or lose together, and this can keep the chance of winning everything higher than the product of the single chances. The theorem says that the chance still falls exponentially, at a rate that depends on how bad the single game is and on how many different answers the players can give.

## Proof

The two easy bounds are proved in full in [proofs/sketch.md](proofs/sketch.md). The lower bound plays the optimal single-game strategy in each coordinate. The upper bound $\operatorname{val}(G^{\otimes k}) \le \operatorname{val}(G)$ embeds one game into coordinate $1$ and fills the other coordinates with shared random questions.

The main bound is given there as a sketch, not a full proof. It follows Holenstein. Fix a strategy for $G^{\otimes k}$ and grow a set $S$ of coordinates. While the probability of winning on all of $S$ is not yet tiny, conditioning on that event, and on the answers in $S$, changes the question distribution in a typical other coordinate $j$ by a small statistical distance, bounded through the Kullback-Leibler divergence by about $\sqrt{(d + |S| \log s)/k}$ when the event has probability $2^{-d}$. If coordinate $j$ were won with probability more than $\operatorname{val}(G)$ plus that distance, the provers of a single game could embed their question in coordinate $j$, sample the rest of the conditioned questions with Raz's dependency-breaking variables, and agree on them by Holenstein's correlated sampling lemma, which would beat $\operatorname{val}(G)$. So some coordinate is lost with probability at least $\varepsilon/2$, and adding it to $S$ multiplies the winning probability by $1 - \varepsilon/2$. This works for $\Omega(\varepsilon^2 k / \log s)$ steps, which gives the bound. The $\log s$ term pays for conditioning on the answers in $S$, and Rao's argument for projection games avoids it.

## Consequences

On this site a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. The consequences below are gap results for the value of games, read as hardness of approximation within the ratio of soundness to completeness.

- **Label cover with small soundness.** The [clause-variable game](/two-prover-one-round-game/) of a 3CNF formula is a projection game with answers of size $8$ and $2$. By the PCP theorem it is NP-hard to tell value $1$ from value at most $1 - \varepsilon_0$ for a constant $\varepsilon_0 > 0$. Parallel repetition keeps value $1$ (play a satisfying assignment in each coordinate) and drops value $1 - \varepsilon_0$ to at most $\delta$ for $k = O(\log(1/\delta))$. The repeated game is still a projection game, its size is $n^{O(k)}$, and its answer sets have size $8^k$ and $2^k$, polynomial in $1/\delta$. So for every constant $\delta > 0$, [label cover](/label-cover/) with value $1$ versus value at most $\delta$ is NP-hard with alphabet size $\mathrm{poly}(1/\delta)$.
- **Tight constants.** This label cover hardness is the outer layer of [Håstad's 3-bit PCP](/hastad-3bit-pcp/), and so of the $7/8 + \varepsilon$ bound for [Max 3SAT](/max-3sat-inapproximability/) and the $1/2 + \varepsilon$ bound for Max 3LIN.
- **Quasi-polynomial reductions.** Taking $k$ polylogarithmic in $n$ makes the soundness $2^{-\mathrm{polylog}\, n}$ at the price of a reduction of size $n^{\mathrm{polylog}\, n}$. A hardness result proved this way assumes that NP has no algorithm of time $n^{\mathrm{polylog}\, n}$, instead of P $\ne$ NP.
- **Error reduction in proof systems.** For [multi-prover interactive proofs](/multi-prover-interactive-proofs/) with two provers and one round, parallel repetition lowers the soundness error without adding rounds.

## Tightness

**The value need not fall as $\operatorname{val}(G)^k$.** In the following game, the questions $x, y \in \{0, 1\}$ are independent and uniform. Each prover answers a pair $(i, z) \in \{1, 2\} \times \{0, 1\}$. The verifier accepts if both answers are the same pair $(i, z)$ and $z$ is the question of prover $i$. So the two provers must agree on which prover's question is revealed, and the other prover must guess it.

- *$\operatorname{val}(G) = 1/2$, in full.* Let $p = \Pr_y[g(y) \text{ has } i = 1]$ and $q = \Pr_x[f(x) \text{ has } i = 2]$. Acceptance with $i = 1$ needs $g(y) = (1, x)$, which has probability at most $p/2$ because $x$ is uniform and independent of $y$, and needs $f(x)$ to have $i = 1$ and $g(y)$ to have $i = 1$, which has probability $(1 - q) p$. Acceptance with $i = 2$ similarly has probability at most $\min(q/2, q(1 - p))$. If $p \le 1/2$ and $q \le 1/2$ the sum is at most $p/2 + q/2 \le 1/2$. If $q \le 1/2 < p$ it is at most $p/2 + q(1-p) \le p/2 + (1-p)/2 = 1/2$, and the case $p \le 1/2 < q$ is the same. If both exceed $1/2$ it is at most $p(1-q) + q(1-p) = \tfrac12 - 2(p - \tfrac12)(q - \tfrac12) < \tfrac12$. The strategy where both answer $(1, 0)$ wins with probability $1/2$.
- *$\operatorname{val}(G^{\otimes 2}) = 1/2$.* On $(x_1, x_2)$ the first prover answers $((1, x_1), (2, x_1))$, and on $(y_1, y_2)$ the second prover answers $((1, y_2), (2, y_2))$. The answers are equal exactly when $x_1 = y_2$, and then both coordinates pass. So the value is at least $1/2$, and at most $1/2$ by the easy upper bound.

So two repetitions do not lower the value at all, while $\operatorname{val}(G)^2 = 1/4$.

**The exponent of $\varepsilon$.** For odd $m$ the [odd cycle game](/two-prover-one-round-game/) is a projection game, in fact a unique game, of value $1 - \tfrac{1}{2m}$. Raz (2008) shows that its $k$-fold repetition has value at least $1 - O(\sqrt{k}/m)$. With $\varepsilon = \tfrac{1}{2m}$ the value stays above a constant for $k$ up to order $1/\varepsilon^2$, so the bound $(1 - \varepsilon)^{\Omega(k)}$, called strong parallel repetition, is false even for unique games, and the exponent $2$ in Rao's bound is best possible.

**The answer size.** Feige and Verbitsky (2002) give games of value at most a constant below $1$ for which the number of repetitions needed to reach a fixed smaller value grows with the answer size. So some dependence on $s$ is needed for general games, as in the bounds of Raz and Holenstein.

## History

Raz proved the general exponential bound at STOC 1995, and the journal version appeared in 1998. Holenstein simplified the proof and improved the exponent of $\varepsilon$ from $32$ to $3$ at STOC 2007. Rao removed the answer size for projection games at STOC 2008, the same year that Raz gave the odd cycle counterexample to strong repetition. Dinur and Steurer gave an analytic proof for projection games in 2014.

## References
