---
tag: W33VWJ
kind: technique
slug: probabilistic-method
name: Probabilistic method
aliases:
- Erdos's probabilistic method
- existence by random choice
- probabilistic existence proof
area: techniques/randomization-techniques
level: advanced
summary: Proves that an object with a property exists by showing a random choice has it with positive probability.
prereqs: [probability-space, union-bound, linearity-of-expectation]
see_also: [lovasz-local-lemma, method-of-conditional-expectations, ramsey-theorem, maximum-cut, max-sat, independent-set, erdos-renyi-model, randomized-algorithm]
sources:
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition
    locator: Chapter 1 (the basic method and Ramsey numbers), Chapter 2 (linearity of expectation, large cuts and derandomization) and Chapter 3 (alterations)
  - paper: doi:10.1090/S0002-9904-1947-08785-1
    title: Paul Erdős, Some remarks on the theory of graphs, Bulletin of the American Mathematical Society 53(4) (1947)
    locator: pp. 292 to 294 (the lower bound 2^{k/2} for the diagonal Ramsey numbers by counting colourings)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 6, The Probabilistic Method (the basic counting argument, the expectation argument, derandomization by conditional expectations, sample and modify, and the Lovász local lemma)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 5, The Probabilistic Method
---

The probabilistic method proves that an object with a given property exists by choosing an object at random from a suitable distribution and showing that it has the property with positive probability. Since a probability space with a positive chance of an event must contain an outcome in that event, the object exists, although the proof does not say which one it is. Erdős made the method famous in 1947 with a lower bound on Ramsey numbers. Its two basic tools are the [union bound](/union-bound/), to show that the probability of a bad event is below 1, and [linearity of expectation](/linearity-of-expectation/), to show that some outcome is at least the mean.

## In plain words

Suppose you want to show that a good thing exists, such as a way to colour a network with no bad pattern. Building one by hand can be very hard. Instead, imagine that you pick one at random, for example by tossing a coin for each part.

Now count the chance that the random pick is bad. If that chance is less than one, then some picks are not bad, so a good thing exists. In the same way, if a random pick is good by ten points on average, then some pick is good by at least ten points, because an average cannot be larger than every value.

The proof gives no recipe for the good object. Sometimes the coin tosses can be replaced by careful choices, one at a time, and then the proof becomes a fast algorithm.

## When it applies

- You want to show that some object in a large finite family has a property, or that some object reaches a value.
- A natural random object exists: each edge coloured by a coin, each vertex kept with probability $p$, each variable set by a coin.
- The bad events are many but each is unlikely, so that their probabilities add up to less than 1. Or the quantity to make large is a sum of simple parts whose expectations are easy.
- An explicit construction is unknown or much weaker. For the diagonal Ramsey numbers, no explicit colouring is known that matches the exponential bound of the random one.

## The template

```pseudo id=main
PROBABILISTIC-EXISTENCE(family Ω of objects, property P)
L1  choose a distribution on Ω                              ▷ hole: the random object
L2  either (union bound)
L3      list bad events B_1, ..., B_m such that "no B_j" implies P     ▷ hole: the bad events
L4      show Σ_j Pr[B_j] < 1
L5      conclude Pr[P] ≥ 1 − Σ_j Pr[B_j] > 0, so an object with P exists
L6  or (expectation)
L7      write the value as X = Σ_j X_j                            ▷ hole: the decomposition
L8      compute E[X] = Σ_j E[X_j]
L9      conclude that some object has X ≥ E[X], and some has X ≤ E[X]
L10 optionally alter the random object to remove the few bad parts     ▷ hole: the alteration
L11 optionally replace each random choice by the choice that keeps the conditional expectation   ▷ derandomization
```

The holes are the distribution of line L1, the bad events of line L3 or the decomposition of line L7, and the alteration of line L10. Line L5 is the union bound $\Pr[\bigcup_j B_j] \le \sum_j \Pr[B_j]$, which needs no independence. Line L9 holds because a random variable that is less than $\mathbb{E}[X]$ on every outcome would have a mean less than $\mathbb{E}[X]$. Both conclusions are for finite spaces, or for any space in the form "the event has positive probability".

## Classic examples

- **Ramsey numbers, Erdős 1947.** The [Ramsey number](/ramsey-theorem/) $R(k, k)$ is the least $n$ such that each colouring of the edges of the complete graph $K_n$ with two colours has a $k$-clique of one colour. *Claim:* $R(k, k) > 2^{k/2}$ for $k \ge 3$. Colour each edge of $K_n$ red or blue with a fair coin, independently. A fixed set of $k$ vertices has one colour on all $\binom{k}{2}$ edges with probability $2^{1 - \binom{k}{2}}$. By the union bound, some $k$-set has one colour with probability at most $\binom{n}{k} 2^{1 - \binom{k}{2}}$. For $n = \lfloor 2^{k/2} \rfloor$, $\binom{n}{k} < n^k/k! \le 2^{k^2/2}/k!$, so the bound is less than $2^{1 + k/2}/k!$, which is less than 1 for $k \ge 3$. So some colouring of $K_n$ has no one-coloured $k$-clique. For $k = 10$ and $n = 32$, the bound is about $3.67 \times 10^{-6}$. The same union bound stays below 1 up to $n = 100$ for $k = 10$, so $R(10, 10) > 100$.
- **Large cuts.** Every graph with $m$ edges has a cut with at least $m/2$ edges. Put each vertex on one of two sides with a fair coin. Each edge crosses with probability $1/2$, so the expected size of the cut is $m/2$, and some cut is at least as large. The Petersen graph has 15 edges, so it has a cut of at least 8 edges; its [maximum cut](/maximum-cut/) has 12. The [method of conditional expectations](/method-of-conditional-expectations/) turns this proof into the greedy algorithm that puts each vertex opposite most of its placed neighbours, which always reaches $m/2$ and finds a cut of 12 on the Petersen graph, with the outer cycle numbered 0 to 4, the inner vertices 5 to 9, and the vertices taken in this order.
- **Satisfiable formulas.** In a 3-CNF formula in which each clause has 3 distinct variables, a random assignment satisfies each clause with probability $7/8$. So some assignment satisfies at least $7/8$ of the clauses, and each such formula with at most 7 clauses is satisfiable. This is the base of the $7/8$ approximation for [MAX-SAT](/max-sat/) with clauses of length 3.
- **Independent sets by alteration.** A graph with $n$ vertices and average degree $d \ge 1$ has an [independent set](/independent-set/) of at least $n/(2d)$ vertices. Keep each vertex with probability $p = 1/d$, then delete one end of each edge that survives. The kept vertices number $np$ in expectation and the surviving edges $(nd/2)p^2$, so the expected size of the result is at least $np - (nd/2)p^2 = n/(2d)$. For the Petersen graph this guarantees 2 vertices; the true maximum is 4.
- **The [Lovász local lemma](/lovasz-local-lemma/).** When the bad events are many but each depends on only a few others, their probabilities can add up to more than 1, and the union bound fails. The local lemma still gives a positive probability that none occurs, for example a 2-colouring of a hypergraph with no one-coloured edge when each edge of size $k$ meets at most $2^{k-1}/e - 1$ others.
- **Random graphs.** In the [Erdős-Rényi model](/erdos-renyi-model/), the expected number of copies of a small graph and the second moment show that most graphs have a property, which proves that graphs with that property exist.

## Variations

- **Counting form.** In a finite uniform space, "the probability is positive" is "the number of good objects is positive". Erdős's proof is a count of colourings.
- **First moment.** If $X \ge 0$ is an integer and $\mathbb{E}[X] < 1$, then $\Pr[X = 0] > 0$. The union bound is the case where $X$ counts the bad events.
- **Second moment.** To show that a count $X$ is positive with positive probability, show $\mathrm{Var}[X] < \mathbb{E}[X]^2$, and use [Chebyshev's inequality](/chebyshev-inequality/): $\Pr[X = 0] \le \mathrm{Var}[X]/\mathbb{E}[X]^2$.
- **Alteration, or sample and modify.** Take a random object that has few bad parts and repair them. For Ramsey numbers it gives $R(k, k) > (1 - o(1))\,(k/e)\,2^{k/2}$, a factor $\sqrt{2}$ better than the best form of the plain union bound.
- **Derandomization.** Fix the random choices one at a time, each time to the value that keeps the conditional expectation of the value at least its mean, or the conditional probability of failure below 1. This is the [method of conditional expectations](/method-of-conditional-expectations/), and it gives a deterministic algorithm when the conditional expectations can be computed.
- **From existence to algorithms.** If the good event has probability at least $q$, sampling until a good object is found is a [randomized algorithm](/randomized-algorithm/) with $1/q$ expected trials, provided a good object can be recognized. The algorithm of Moser and Tardos does this for the local lemma.

## Pitfalls

- **A probability equal to 1 is not enough.** The union bound must be strictly below 1. A bound of exactly 1 proves nothing.
- **Existence is not construction.** The Ramsey proof shows that good colourings exist, and in fact most colourings are good, but checking one colouring takes time exponential in $k$. A good object can exist without a known efficient way to find or check it.
- **Independence where none is given.** The union bound and linearity of expectation need no independence. A product of probabilities does. Check which one a step of the proof uses.
- **Some, not most.** The expectation argument gives one object at least the mean. It does not show that a typical object is near the mean; for that, a tail bound is needed.
- **The wrong distribution.** A uniform choice is not always best. In the alteration example the choice $p = 1/d$ is what makes the bound work, and $p = 1/2$ gives a negative bound on dense graphs.

## Exercises

1. Show that $\binom{n}{k} 2^{1 - \binom{k}{2}} < 1$ for $k = 10$ and $n = 100$, and that it fails for $n = 101$.
2. Prove that every graph with $m$ edges has a bipartite subgraph with at least $m/2$ edges, and that the greedy algorithm from conditional expectations finds one in $O(n + m)$ time.
3. Prove that every 3-CNF formula with clauses of 3 distinct variables and at most 7 clauses is satisfiable, and give an unsatisfiable formula with 8 such clauses.
4. Show that some tournament on $n$ vertices has at least $n!/2^{n-1}$ Hamiltonian paths, by computing the expected number of Hamiltonian paths in a random tournament. This is the first example of Alon and Spencer, a result of Szele.

5. Use alteration with $p = 1/d$ to prove the bound $n/(2d)$ on independent sets in detail, and compare it with the bound $n/(d + 1)$ of Turán's theorem for the Petersen graph.

## References
