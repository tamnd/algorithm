---
tag: 3CVTD1
kind: model
slug: request-answer-game
name: Request-answer game
aliases:
- request-answer model
area: online-and-streaming/competitive-analysis
level: advanced
summary: A two-player formulation of online problems where the adversary issues requests and the algorithm answers each one.
prereqs: [online-algorithm, competitive-ratio]
see_also: [oblivious-adversary, adaptive-adversary, adaptive-offline-adversary, randomized-online-algorithm, yao-minimax-principle, zero-sum-game, offline-optimum, paging-problem]
sources:
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the definition of request-answer games, the three adversaries and the theorems that relate them
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 7 (request-answer games) and Chapter 8 (competitive analysis and zero-sum games)
---

A request-answer game is the general model of an online problem defined by Ben-David, Borodin, Karp, Tardos and Wigderson (1994). An adversary issues requests one at a time, the online algorithm answers each request before the next one comes, and a cost function prices the whole play. Paging, ski rental, list update, $k$-server and most other online problems are special cases, so theorems proved for request-answer games hold for all of them.

## The machine

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

A request-answer game (for a minimization problem) is a triple $(R, A, \{f_n\})$:

- $R$ is the set of possible **requests**;
- $A$ is the set of possible **answers**;
- for each $n \ge 0$, $f_n : R^n \times A^n \to \mathbb{R}_{\ge 0} \cup \{\infty\}$ is the **cost function**. The value $f_n(r_1 \cdots r_n, a_1 \cdots a_n)$ is the cost of answering the requests $r_1, \ldots, r_n$ with $a_1, \ldots, a_n$. The value $\infty$ marks an answer sequence that is not allowed.

The play has rounds $i = 1, 2, \ldots$. In round $i$ the adversary issues $r_i \in R$ or ends the game. If it issues $r_i$, the algorithm then chooses $a_i \in A$. The answer is final. If the game ends after $n$ rounds, the algorithm pays $f_n(r_1 \cdots r_n, a_1 \cdots a_n)$.

- A **deterministic online algorithm** is a sequence of functions $g_i : R^i \to A$, with $a_i = g_i(r_1, \ldots, r_i)$. The past answers are functions of the past requests, so they add no information.
- A **randomized online algorithm** is a probability distribution over deterministic online algorithms. Equivalently, it flips coins and lets $a_i$ depend on $r_1, \ldots, r_i$ and on the coins so far. See [randomized online algorithm](/randomized-online-algorithm/).
- The **offline optimum** of $\sigma \in R^n$ is $\mathrm{OPT}(\sigma) = \inf_{a \in A^n} f_n(\sigma, a)$, as on the [offline optimum](/offline-optimum/) page.

For a maximization problem, $f_n$ is a profit and $\mathrm{OPT}$ is a supremum.

**Two encodings.** In [paging](/paging-problem/) with a cache of size $k$, a request is a page, an answer is the new cache content, and $f_n$ counts the rounds where the requested page is not in the old content. The new content must have at most $k$ pages, must contain the requested page and must be a subset of the old content plus the requested page; if some answer breaks these rules, $f_n = \infty$. In [ski rental](/ski-rental-problem/), each request is "one more ski day", an answer is "rent" or "buy", and $f_n$ is $n$ if the answers never say "buy", and $(j - 1) + B$ if the first "buy" is in round $j$.

## What it counts

The model counts the cost $f_n$ of the answers. It does not count time or memory: the functions $g_i$ need not be computable. So a lower bound in the model says that the information about the future is missing, and not that the computation is too hard.

An algorithm ALG is $c$-competitive if there is a constant $b$ such that, for every $\sigma$, $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ (see [competitive ratio](/competitive-ratio/)). For a randomized algorithm the definition depends on how the adversary may react to the coins. Ben-David et al. define three adversaries:

| adversary | chooses $r_i$ | the adversary's cost | ALG is $c$-competitive if |
|---|---|---|---|
| [oblivious](/oblivious-adversary/) | in advance, without seeing the coins | $\mathrm{OPT}(\sigma)$ | $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$ |
| [adaptive online](/adaptive-adversary/) | after seeing $a_1, \ldots, a_{i-1}$ | its own online answers | $\mathbb{E}[\mathrm{ALG} - c \cdot \mathrm{ADV}] \le b$ |
| [adaptive offline](/adaptive-offline-adversary/) | after seeing $a_1, \ldots, a_{i-1}$ | $\mathrm{OPT}$ of the final sequence | $\mathbb{E}[\mathrm{ALG} - c \cdot \mathrm{OPT}] \le b$ |

For a deterministic algorithm the three definitions agree, because the adversary can compute every answer in advance.

## Relation to other models

- **Zero-sum games.** For a fixed length bound, a request-answer game with finite $R$ and $A$ is a finite [zero-sum game](/zero-sum-game/) between the algorithm and the adversary. The [minimax theorem](/minimax-theorem/) then gives the [Yao principle](/yao-minimax-principle/): a lower bound for every deterministic algorithm on one distribution of inputs is also a lower bound for every randomized algorithm against an oblivious adversary. Borodin and El-Yaniv, Chapter 8, treat the details for infinite games.
- **Metrical task systems.** A [metrical task system](/metrical-task-systems/) is a request-answer game where the answers are the states of a metric space and the cost is movement plus a task cost. Paging and $k$-server are special cases of both.
- **Advice.** In the [advice model](/advice-model/), the algorithm also reads bits written by an oracle that knows $\sigma$. With no advice, it is the request-answer game.
- **Offline algorithms.** An [offline algorithm](/offline-algorithm/) is a map from $\sigma$ to a whole answer sequence. It is the same game where the adversary must reveal $\sigma$ first.

## Known results in the model

The first three results are from Ben-David, Borodin, Karp, Tardos and Wigderson (1994). They hold for every request-answer game.

1. **Adaptive offline adversaries.** If a randomized algorithm is $c$-competitive against every adaptive offline adversary, then some deterministic online algorithm is $c$-competitive. So randomization does not help against this adversary. The proof is on the [adaptive offline adversary](/adaptive-offline-adversary/) page.
2. **Adaptive online against oblivious.** If $G$ is $c$-competitive against every adaptive online adversary and some randomized algorithm is $d$-competitive against every oblivious adversary, then $G$ is $c \cdot d$-competitive against every adaptive offline adversary. See the [adaptive online adversary](/adaptive-adversary/) page.
3. **Adaptive online.** Combining 1 and 2 with $H = G$: if a randomized algorithm is $c$-competitive against every adaptive online adversary, then some deterministic algorithm is $c^2$-competitive.
4. **The hierarchy.** For a fixed algorithm, $c$-competitive against adaptive offline adversaries implies $c$-competitive against adaptive online adversaries, which implies $c$-competitive against oblivious adversaries. The gaps can be large: for paging with $k$ pages in the cache, the best deterministic ratio is $k$, and so is the best ratio against adaptive online adversaries, while [randomized marking](/randomized-marking/) is $2H_k$-competitive against an oblivious adversary, where $H_k$ is the $k$-th [harmonic number](/harmonic-series/).

## References
