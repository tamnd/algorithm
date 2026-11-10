---
tag: 25P02X
kind: definition
slug: adaptive-offline-adversary
name: Adaptive offline adversary
area: online-and-streaming/competitive-analysis
level: intro
summary: An adversary that sees the algorithm's random choices and also knows the input in advance.
prereqs: [adaptive-adversary]
see_also: [oblivious-adversary, randomized-online-algorithm, request-answer-game, offline-optimum, competitive-ratio, ski-rental-problem, zero-sum-game]
sources:
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the adaptive offline adversary and the theorem that a randomized algorithm c-competitive against it gives a deterministic c-competitive algorithm
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 7 (request-answer games and the relations between the adversaries)
---

An adaptive offline adversary builds the request sequence one request at a time, after it sees each answer of a [randomized online algorithm](/randomized-online-algorithm/), and then pays the [offline optimum](/offline-optimum/) of the sequence it built. So it learns the algorithm's random choices as they happen and is charged as if it had known the whole sequence in advance. It is the strongest of the three adversaries of Ben-David, Borodin, Karp, Tardos and Wigderson (1994), and against it randomization does not help at all.

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

Let $(R, A, \{f_n\})$ be a [request-answer game](/request-answer-game/) in which every finite request sequence has finite $\mathrm{OPT}$. An **adaptive offline adversary** $Q$ is a rule that, given the history $h = (r_1, a_1, \ldots, r_m, a_m)$ of requests and answers so far, either stops or issues a next request $r_{m+1}$. The play must stop after finitely many rounds, whatever the answers are. If it stops with the requests $\sigma = r_1 \cdots r_n$, the adversary pays $\mathrm{OPT}(\sigma)$.

A randomized online algorithm ALG is **$c$-competitive against adaptive offline adversaries** if there is a constant $b$ such that, for every such $Q$,

$$\mathbb{E}[\mathrm{ALG}(\sigma) - c \cdot \mathrm{OPT}(\sigma)] \le b,$$

where $\sigma$ is the random sequence that $Q$ builds against the coins of ALG.

The difference from the [adaptive online adversary](/adaptive-adversary/) is the cost: the online adversary must commit to its own answers as it goes, and this adversary pays the best answers in hindsight. The difference from the [oblivious adversary](/oblivious-adversary/) is the order: the oblivious adversary fixes $\sigma$ before any coin is flipped.

**Theorem (Ben-David et al. 1994).** If a randomized online algorithm ALG is $c$-competitive against adaptive offline adversaries, with constant $b$, then there is a deterministic online algorithm $D$ with $D(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$.

*Proof.* For a history $h$ with requests $r_1 \cdots r_m$ and answers $a_1 \cdots a_m$, let its value be

$$v(h) = f_m(r_1 \cdots r_m, a_1 \cdots a_m) - c \cdot \mathrm{OPT}(r_1 \cdots r_m).$$

Say that the adversary **wins from $h$** if it has a strategy that starts at $h$, stops after finitely many rounds against every sequence of answers, and stops at a history of value greater than $b$. Let $W$ be the set of histories from which the adversary wins.

1. *If $h \notin W$, then $v(h) \le b$.* Otherwise the strategy "stop now" wins from $h$.
2. *If $h \notin W$, then for every request $r$ there is an answer $a$ with $h \cdot (r, a) \notin W$.* Suppose not: for some $r$, every $h \cdot (r, a)$ is in $W$. Choose for each $a$ a winning strategy $S_a$ from $h \cdot (r, a)$. The strategy "issue $r$; if the answer is $a$, follow $S_a$" stops after finitely many rounds and wins from $h$. So $h \in W$, a contradiction.
3. *The empty history is not in $W$.* Suppose it is, and let $S$ be a winning strategy. Let $Q$ be the adaptive offline adversary that plays $S$ against ALG. For every outcome of the coins, ALG gives some sequence of answers, so the play stops at a history of value greater than $b$. So $\mathrm{ALG}(\sigma) - c \cdot \mathrm{OPT}(\sigma) - b$ is strictly positive on every outcome, its expectation is strictly positive, and $\mathbb{E}[\mathrm{ALG}(\sigma) - c \cdot \mathrm{OPT}(\sigma)] > b$. This contradicts the assumption on ALG.

Now define $D$. It keeps the history $h$ of the play so far, which starts empty and so is not in $W$ by 3. On a request $r$, it answers with some $a$ such that $h \cdot (r, a) \notin W$, which exists by 2. The history is a function of the requests so far, so $D$ is a deterministic online algorithm. Every history of $D$ is outside $W$, so by 1 its value is at most $b$: $D(\sigma) - c \cdot \mathrm{OPT}(\sigma) \le b$ for every $\sigma$. $\square$

The proof needs no determinacy theorem for infinite games: it uses only the definition of $W$ and the fact that the adversary's strategies stop in finite time. The algorithm $D$ need not be efficient; the theorem is about information.

**Consequences.**

- The best ratio against adaptive offline adversaries equals the best deterministic ratio, for every request-answer game. A deterministic algorithm is $c$-competitive against all three adversaries at once.
- With the theorem on the [adaptive online adversary](/adaptive-adversary/) page, a randomized algorithm that is $c$-competitive against adaptive online adversaries gives a deterministic algorithm that is $c^2$-competitive.

## Examples and non-examples

- **Ski rental.** Renting costs 1 per day and buying costs $B$. The adaptive offline adversary issues ski days until the algorithm buys, and stops on the day of the purchase (or after day $N$ if it has not bought). If the purchase is on day $j$, the algorithm pays $j - 1 + B$ against $\mathrm{OPT} = \min(j, B)$, a ratio of at least $2 - 1/B$. So no randomized rule has a strict ratio below $2 - 1/B$ against this adversary, while against the oblivious adversary the best strict ratio tends to $e/(e-1)$. See [ski rental](/ski-rental-problem/).
- **Paging.** For a cache of $k$ pages, the best ratio against adaptive offline adversaries is $k$, the deterministic ratio of [LRU](/lru/). Against oblivious adversaries it is $H_k$.
- **Non-example: the adaptive online adversary.** It also sees the answers but pays the cost of its own online answers, which can be larger than $\mathrm{OPT}(\sigma)$.
- **Non-example: an adversary that knows the coins in advance.** An adversary that sees all the random bits before the first request is at least as strong. For each fixed outcome of the coins, ALG is a deterministic algorithm, so against this adversary ALG is no better than its worst deterministic part.

## Related definitions

- **[Oblivious adversary](/oblivious-adversary/).** Fixes $\sigma$ in advance and pays $\mathrm{OPT}(\sigma)$. The weakest adversary.
- **[Adaptive online adversary](/adaptive-adversary/).** Sees the answers and serves the requests online. Between the other two.
- **[Offline optimum](/offline-optimum/).** The cost this adversary pays.
- **[Request-answer game](/request-answer-game/).** The model in which the theorem holds.
- **[Zero-sum game](/zero-sum-game/).** The game between the algorithm and the adversary. Against this adversary its value is reached by a pure (deterministic) strategy of the algorithm.

## References
