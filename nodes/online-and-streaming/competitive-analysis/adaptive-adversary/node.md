---
tag: XFSKPH
kind: definition
slug: adaptive-adversary
name: Adaptive adversary
aliases:
- adaptive online adversary
- adaptive adversary
area: online-and-streaming/competitive-analysis
level: intro
summary: An adversary that chooses each request after seeing the algorithm's past actions, including its random outcomes.
prereqs: [oblivious-adversary, request-answer-game]
see_also: [adaptive-offline-adversary, randomized-online-algorithm, competitive-ratio, paging-problem, randomized-marking, lru, yao-minimax-principle]
sources:
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the adaptive online adversary and the theorem that gives a c times d competitive ratio against adaptive offline adversaries
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 4 (randomized paging against adaptive adversaries) and Chapter 7 (the relations between the adversaries)
---

An adaptive online adversary chooses each request after it sees the answers that a [randomized online algorithm](/randomized-online-algorithm/) has given so far, and it must serve its own requests online, at the same time as the algorithm. So it learns the algorithm's past random choices, but it can not use the future, because its own answers are fixed when it gives them. It is the middle one of the three adversaries of Ben-David, Borodin, Karp, Tardos and Wigderson (1994): stronger than the [oblivious adversary](/oblivious-adversary/) and weaker than the [adaptive offline adversary](/adaptive-offline-adversary/).

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

Let ALG be a randomized online algorithm in a [request-answer game](/request-answer-game/). An **adaptive online adversary** $Q$ plays rounds $i = 1, 2, \ldots$. In round $i$ it either stops or chooses a request $r_i$ as a function of $r_1, a_1, \ldots, r_{i-1}, a_{i-1}$, where $a_j$ are the answers of ALG. It also gives its own answer $a'_i$ to $r_i$, as a function of the same history and $r_i$, before it sees $a_i$. When it stops after $n$ rounds, its cost is $\mathrm{ADV} = f_n(r_1 \cdots r_n, a'_1 \cdots a'_n)$. Both $\sigma$ and $\mathrm{ADV}$ are random variables, because they depend on the coins of ALG.

ALG is **$c$-competitive against adaptive online adversaries** if there is a constant $b$ such that, for every adaptive online adversary $Q$ that stops after finitely many rounds,

$$\mathbb{E}[\mathrm{ALG}(\sigma) - c \cdot \mathrm{ADV}] \le b.$$

The adversary's answers $a'_i$ depend only on the past, so $\mathrm{ADV}$ is the cost of an online algorithm on $\sigma$, and $\mathrm{ADV} \ge \mathrm{OPT}(\sigma)$. If the adversary could pay $\mathrm{OPT}(\sigma)$ instead, it would be the adaptive offline adversary.

**The theorem of Ben-David et al.** Let $G$ be $c$-competitive against adaptive online adversaries, and let some randomized online algorithm $H$ be $d$-competitive against oblivious adversaries. Then $G$ is $c \cdot d$-competitive against adaptive offline adversaries.

*Proof.* Let $Q$ be an adaptive offline adversary against $G$, and let $b, b'$ be the additive constants of $G$ and $H$. Build an adaptive online adversary $Q'$: it issues the same requests as $Q$ (it sees the same answers of $G$), and it serves them by running $H$ with its own independent coins. Fix the coins of $G$. Then the sequence $\sigma$ is fixed, and the coins of $H$ do not depend on it, so $\mathbb{E}_H[H(\sigma)] \le d \cdot \mathrm{OPT}(\sigma) + b'$. Since $G$ is $c$-competitive against $Q'$, $\mathbb{E}[G(\sigma)] \le c \cdot \mathbb{E}[H(\sigma)] + b \le c d \cdot \mathbb{E}[\mathrm{OPT}(\sigma)] + c b' + b$. This is the claim with additive constant $c b' + b$. $\square$

With the theorem on the [adaptive offline adversary](/adaptive-offline-adversary/) page (randomization does not help against that adversary), and with $H = G$ (which is $c$-competitive against oblivious adversaries, so $d = c$), this gives: **if a randomized algorithm is $c$-competitive against adaptive online adversaries, some deterministic online algorithm is $c^2$-competitive.** So against this adversary randomization can at most take the square root of the best deterministic ratio.

## Examples and non-examples

**Paging: randomization does not help.** Take a cache of $k$ pages, $k + 1$ pages in all, and let ALG and the adversary start with the cache $\{1, \ldots, k\}$. The adversary always requests the one page that ALG does not hold. It sees the answers, so it knows that page. ALG faults on every request, and $\mathrm{ALG}(\sigma) = n$ for $n$ requests.

The adversary serves the requests with one of $k$ online rules $A_1, \ldots, A_k$. On the first request, page $k + 1$, rule $A_i$ evicts page $i$. Now the pages missing from the $k$ rules are all different, so exactly one page is held by all of them. On each later request $p$, at most one rule lacks $p$. That rule loads $p$ and evicts the page that all the rules hold, and the missing pages stay all different. So $\sum_i A_i(\sigma) \le k + (n - 1)$.

If ALG were $c$-competitive with constant $b$, then $\mathbb{E}[n - c \cdot A_i(\sigma)] \le b$ for each $i$. The average over $i$ gives $n - c(n + k - 1)/k \le b$ for every $n$, so $c \ge k$. [LRU](/lru/) is deterministic and $k$-competitive, so $k$ is the exact ratio of paging against adaptive online adversaries. Against the [oblivious adversary](/oblivious-adversary/), [randomized marking](/randomized-marking/) reaches $2H_k$.

- **Non-example: the oblivious adversary.** It fixes $\sigma$ before the coins and pays $\mathrm{OPT}(\sigma)$. It can not aim at the missing page.
- **Non-example: the adaptive offline adversary.** It also sees the answers, but it pays $\mathrm{OPT}(\sigma)$ of the final sequence, as if it had known $\sigma$ from the start.
- **Non-example: a deterministic algorithm.** For a deterministic ALG the adaptive online adversary has no advantage over the oblivious one: it can compute all answers in advance.

## Related definitions

- **[Oblivious adversary](/oblivious-adversary/).** The weakest adversary. A ratio against adaptive online adversaries is also a ratio against oblivious ones.
- **[Adaptive offline adversary](/adaptive-offline-adversary/).** The strongest adversary. A ratio against it is also a ratio against adaptive online ones.
- **[Randomized online algorithm](/randomized-online-algorithm/).** The algorithms these adversaries are used for.
- **[Request-answer game](/request-answer-game/).** The general model in which the theorems hold.
- **[Competitive ratio](/competitive-ratio/).** The deterministic definition, which the three adversary models extend.

## References
