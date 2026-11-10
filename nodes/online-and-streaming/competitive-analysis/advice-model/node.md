---
tag: Y0W652
kind: model
slug: advice-model
name: Online algorithms with advice
aliases:
- advice complexity
- online with advice
area: online-and-streaming/competitive-analysis
level: research
summary: An online algorithm that may read a limited number of advice bits computed from the whole input in advance.
prereqs: [online-algorithm, competitive-ratio, offline-optimum]
see_also: [offline-algorithm, randomized-online-algorithm, paging-problem, belady-algorithm, ski-rental-problem, online-knapsack-problem, learning-augmented-algorithms, kolmogorov-complexity]
sources:
  - paper: doi:10.1051/ita/2009012
    title: "Stefan Dobrev, Rastislav Kralovic and Dana Pardubska, Measuring the problem-relevant information in input, RAIRO Theoretical Informatics and Applications 43(3) (2009), 585-613"
    locator: the first model of online computation with advice, and optimal paging with one bit per request
  - paper: doi:10.1007/978-3-642-10631-6_35
    title: "Hans-Joachim Bockenhauer, Dennis Komm, Rastislav Kralovic, Richard Kralovic and Tobias Momke, On the advice complexity of online problems, ISAAC 2009, Lecture Notes in Computer Science 5878, 331-340"
    locator: the advice tape model, where the advice complexity is the number of bits read
  - paper: doi:10.1016/j.tcs.2010.08.007
    title: "Yuval Emek, Pierre Fraigniaud, Amos Korman and Adi Rosen, Online computation with advice, Theoretical Computer Science 412(24) (2011), 2642-2656"
    locator: the model with a fixed number of advice bits per request
  - paper: doi:10.1145/3056461
    title: "Joan Boyar, Lene M. Favrholdt, Christian Kudahl, Kim S. Larsen and Jesper W. Mikkelsen, Online algorithms with advice: a survey, ACM Computing Surveys 50(2) (2017), Article 19"
    locator: Section 2 (the models) and the results for paging, knapsack and string guessing
  - paper: doi:10.1016/j.tcs.2014.01.027
    title: "Hans-Joachim Bockenhauer, Dennis Komm, Richard Kralovic and Peter Rossmanith, The online knapsack problem: advice and randomization, Theoretical Computer Science 527 (2014), 61-72"
    locator: one advice bit gives ratio 2 for the simple knapsack problem, and logarithmic advice is needed to do better
  - paper: doi:10.1016/j.tcs.2014.06.006
    title: "Hans-Joachim Bockenhauer, Juraj Hromkovic, Dennis Komm, Sacha Krug, Jasmin Smula and Andreas Sprock, The string guessing problem as a method to prove lower bounds on the advice complexity, Theoretical Computer Science 554 (2014), 95-108"
    locator: the string guessing problem and its advice complexity
---

In the advice model, an [online algorithm](/online-algorithm/) may read bits written by an oracle that knows the whole request sequence in advance. The advice complexity is the number of bits it reads, as a function of the input length $n$. The model measures how much information about the future an online problem needs: with no advice it is the usual online setting, and with enough advice the algorithm can copy an optimal [offline algorithm](/offline-algorithm/). It was developed by Dobrev, Královič and Pardubská (2008), Böckenhauer, Komm, Královič, Královič and Mömke (2009) and Emek, Fraigniaud, Korman and Rosén (2009).

## The machine

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

**The tape model (Böckenhauer et al. 2009).** Before the first request, an oracle with unlimited power sees all of $\sigma = r_1 \cdots r_n$ and writes an infinite binary string $\varphi$, the advice tape. The algorithm answers each $r_i$ with $a_i = g_i(\varphi, r_1, \ldots, r_i)$, but it may read only a prefix of $\varphi$, and the length of the prefix it reads must be decided online. Let $s(\sigma)$ be the number of bits read on $\sigma$. The **advice complexity** of the algorithm is $s(n) = \max \{ s(\sigma) : |\sigma| = n \}$.

The algorithm ALG with advice is **$c$-competitive with advice complexity $s(n)$** if there is a constant $b$ and an oracle such that $\mathrm{ALG}^{\varphi(\sigma)}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$. It is **optimal** if $\mathrm{ALG}^{\varphi(\sigma)}(\sigma) = \mathrm{OPT}(\sigma)$ for every $\sigma$. For a maximization problem, the inequality is reversed as on the [competitive ratio](/competitive-ratio/) page.

The tape is infinite because the algorithm does not know $n$, so it can not know where a finite advice string ends. If an algorithm needs a number $m$ from the oracle, it must read a self-delimiting code for it, which costs about $2 \log_2 m$ bits (or $\log_2 m + O(\log \log m)$ bits with a better code).

**The per-request model (Emek et al. 2009).** With each request $r_i$ the algorithm receives exactly $u$ advice bits, chosen by the oracle with knowledge of $\sigma$. The advice complexity is $u$ bits per request. This model can not express advice that is sublinear in $n$, since every algorithm reads at least $n$ bits.

**The first model (Dobrev, Královič and Pardubská).** Their model also lets an oracle send bits with the requests. Because a request may carry an empty advice string, the presence or absence of advice itself carries information. The tape model removes this problem.

## What it counts

The model counts advice bits and the competitive ratio, and the result is a trade-off between the two. Time and memory are not counted, and the oracle and the algorithm may be any functions.

The key fact for lower bounds: an algorithm that reads at most $s$ bits of advice on inputs of length $n$ behaves on these inputs like one of at most $2^s$ deterministic online algorithms, one for each advice string. So an advice lower bound is a counting argument: if every deterministic algorithm is good on only a small part of a set of inputs, then many algorithms, and so many bits, are needed to cover the set.

**A tight example: string guessing.** The input is a string $x_1 \cdots x_n$ over an alphabet of $q$ letters. Before $x_i$ is shown, the algorithm must guess it; then $x_i$ is shown. The cost is the number of wrong guesses, so $\mathrm{OPT} = 0$ for every string.

- *Upper bound.* Before each guess, read $\lceil \log_2 q \rceil$ advice bits that give the next letter. This uses $n \lceil \log_2 q \rceil$ bits and makes no wrong guesses.
- *Lower bound.* A deterministic algorithm $D$ is perfect on exactly one string: its first guess fixes $x_1$, its second guess (after it sees $x_1$) fixes $x_2$, and so on. An optimal algorithm with $s$ bits is a set of at most $2^s$ deterministic algorithms that together are perfect on all $q^n$ strings. So $2^s \ge q^n$, and $s \ge n \log_2 q$.

For $q$ a power of two the two bounds are equal: exactly $n \log_2 q$ bits are needed and enough. With $q = 2$ this is one bit per request. Böckenhauer, Hromkovič, Komm, Krug, Smula and Sprock (2014) also study the trade-off for a given number of wrong guesses, and use string guessing as a source of reductions.

**A small example: ski rental.** In the [ski rental problem](/ski-rental-problem/), one bit is enough for ratio 1: the oracle writes 1 if the season has at least $B$ days, and the algorithm buys on day 1 if the bit is 1 and never buys otherwise. With 0 bits the best ratio is $2 - 1/B$.

## Relation to other models

- **Deterministic online algorithms.** With advice complexity 0, the model is the deterministic online model.
- **Offline algorithms.** With enough advice the algorithm can follow an optimal offline solution: write the optimal answer to each request in $\lceil \log_2 |A| \rceil$ bits, if the set $A$ of possible answers is finite. So the advice complexity of being optimal is at most about $n \log_2 |A|$.
- **Randomized algorithms.** A [randomized online algorithm](/randomized-online-algorithm/) also chooses among deterministic algorithms, but at random. Advice chooses the best one for the input, so it is at least as strong. Böckenhauer, Komm, Královič and Královič (ICALP 2011, in a paper on the $k$-server problem) show that a randomized algorithm can be converted into an algorithm with advice of about the same ratio, with a number of bits logarithmic in $n$ plus a doubly logarithmic term in the number of inputs of length $n$.
- **Kolmogorov complexity.** The advice is a description of the useful part of the input. Its size is related to the [Kolmogorov complexity](/kolmogorov-complexity/) of the optimal answers given the requests.
- **Learning-augmented algorithms.** In [learning-augmented algorithms](/learning-augmented-algorithms/), the algorithm gets predictions that may be wrong. Advice is always correct, so it gives the limit of what perfect predictions can do.

## Known results in the model

- **Paging, optimal.** One bit per request is enough to be optimal (Dobrev et al.). The bit for request $r_i$ says whether an optimal offline algorithm keeps the page $r_i$ in its cache until the next request to it. On a fault, the algorithm evicts a page whose last bit is 0. On $\sigma = 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$ with $k = 3$ and an empty cache, the bits from [Belady's rule](/belady-algorithm/) are $1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0$, and the algorithm makes 7 faults, the optimum. A simpler scheme gives $\lceil \log_2 k \rceil$ bits on each fault to name the page to evict.
- **Paging, near $H_k$.** Constant advice is enough to reach ratio $H_k + \varepsilon$, the best randomized ratio, while a ratio below $H_k$ needs advice linear in $n$ (Mikkelsen 2016, see the survey of Boyar et al.).
- **Simple knapsack.** In the online knapsack problem where each item's profit equals its weight, no deterministic algorithm without advice has a bounded ratio. One bit of advice gives ratio 2, and $\Omega(\log n)$ bits are needed for any ratio below 2 (Böckenhauer, Komm, Královič and Rossmanith 2014). See [online knapsack](/online-knapsack-problem/).
- **Many other problems.** The survey of Boyar, Favrholdt, Kudahl, Larsen and Mikkelsen (2017) lists advice results for bin packing, $k$-server, list update, scheduling, graph coloring, matching and more.

## References
