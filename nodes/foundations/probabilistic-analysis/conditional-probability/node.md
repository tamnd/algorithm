---
tag: QDJPW8
kind: definition
slug: conditional-probability
name: Conditional probability
area: foundations/probabilistic-analysis
level: intro
summary: The probability of an event given that another event has occurred.
prereqs: [probability-space]
see_also: [independent-events, bayes-theorem, conditional-expectation, karger-min-cut, quicksort-expected-running-time, monty-hall-problem, miller-rabin-primality-test, bloom-filter]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2 (conditional probability and independence, Bayes's theorem); Section 7.4.2 (the probability that two keys are compared)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.2, Axioms of Probability (conditional probability, law of total probability, Bayes' law); Section 1.5, Application, A Randomized Min-Cut Algorithm
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (the min-cut algorithm); Appendix C, Basic Probability Theory
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter V, Conditional Probability. Stochastic Independence
---

The conditional probability $\Pr(A \mid B)$ is the probability of an event $A$ given that an event $B$ has occurred, defined as $\Pr(A \cap B) / \Pr(B)$ when $\Pr(B) > 0$. It is the tool for reasoning in stages: the chance that a [randomized algorithm](/randomized-algorithm/) does the right thing at step $i$, given what it did at the steps before. The product of these stage-by-stage chances gives the probability of a whole run, as in the analysis of [Karger's min-cut algorithm](/karger-min-cut/).

## Definition

Let $(\Omega, \mathcal{F}, \Pr)$ be a [probability space](/probability-space/), and let $B$ be an event with $\Pr(B) > 0$. For each event $A$, the **conditional probability of $A$ given $B$** is

$$\Pr(A \mid B) = \frac{\Pr(A \cap B)}{\Pr(B)}.$$

When $\Pr(B) = 0$, this formula does not define $\Pr(A \mid B)$. In a finite space with equally likely outcomes, $\Pr(A \mid B) = |A \cap B| / |B|$: we keep only the outcomes in $B$, and they stay equally likely.

**It is a probability measure.** For fixed $B$ with $\Pr(B) > 0$, the function $Q(A) = \Pr(A \mid B)$ satisfies the three axioms. $Q(A) \ge 0$ since both parts of the fraction are nonnegative and the bottom is positive. $Q(\Omega) = \Pr(B)/\Pr(B) = 1$. For pairwise disjoint $A_1, A_2, \ldots$, the sets $A_i \cap B$ are pairwise disjoint with union $(\bigcup_i A_i) \cap B$, so $Q(\bigcup_i A_i) = \sum_i \Pr(A_i \cap B)/\Pr(B) = \sum_i Q(A_i)$. So each rule of the probability space page holds for $\Pr(\cdot \mid B)$, for example $\Pr(\bar A \mid B) = 1 - \Pr(A \mid B)$ and the [union bound](/union-bound/).

**Multiplication rule.** For events $A_1, \ldots, A_n$ with $\Pr(A_1 \cap \cdots \cap A_{n-1}) > 0$,

$$\Pr(A_1 \cap \cdots \cap A_n) = \Pr(A_1) \, \Pr(A_2 \mid A_1) \, \Pr(A_3 \mid A_1 \cap A_2) \cdots \Pr(A_n \mid A_1 \cap \cdots \cap A_{n-1}).$$

Proof by induction on $n$. For $n = 1$ the product is $\Pr(A_1)$. For $n \ge 2$, let $D = A_1 \cap \cdots \cap A_{n-1}$. Each conditioning event in the product contains $D$, so it has positive probability by monotonicity. The definition gives $\Pr(D \cap A_n) = \Pr(D) \Pr(A_n \mid D)$, and the hypothesis for $n - 1$ expands $\Pr(D)$.

**Law of total probability.** Let $B_1, B_2, \ldots$ be a finite or countable partition of $\Omega$ into events with $\Pr(B_i) > 0$. Then for each event $A$,

$$\Pr(A) = \sum_i \Pr(A \mid B_i) \Pr(B_i).$$

Proof: the events $A \cap B_i$ are pairwise disjoint with union $A$, so $\Pr(A) = \sum_i \Pr(A \cap B_i)$, and each term is $\Pr(A \mid B_i) \Pr(B_i)$ by the definition. The same holds when the $B_i$ cover $\Omega$ up to a null event.

**Bayes' theorem.** If $\Pr(A) > 0$ and $\Pr(B) > 0$, then

$$\Pr(B \mid A) = \frac{\Pr(A \mid B) \Pr(B)}{\Pr(A)}.$$

Both sides equal $\Pr(A \cap B) / \Pr(A)$. With the law of total probability in the bottom, $\Pr(B_j \mid A) = \Pr(A \mid B_j)\Pr(B_j) / \sum_i \Pr(A \mid B_i)\Pr(B_i)$. See [Bayes' theorem](/bayes-theorem/).

## Examples and non-examples

**Karger's min-cut algorithm.** The algorithm contracts a uniformly random edge of a multigraph until two vertices remain. Fix a minimum cut $K$ of size $c$ in a graph with $n$ vertices. Let $E_i$ be the event that the $i$-th contraction does not pick an edge of $K$. Suppose $E_1, \ldots, E_{i-1}$ hold, so $K$ is still a cut of the current graph, which has $k = n - i + 1$ vertices. Each vertex has degree at least $c$, otherwise its edges would form a smaller cut, so the graph has at least $kc/2$ edges. Hence $\Pr(\bar E_i \mid E_1 \cap \cdots \cap E_{i-1}) \le c / (kc/2) = 2/k$. The multiplication rule over the $n - 2$ contractions gives

$$\Pr(\text{the algorithm returns } K) \ge \prod_{k=3}^{n} \left(1 - \frac{2}{k}\right) = \prod_{k=3}^{n} \frac{k-2}{k} = \frac{2}{n(n-1)}.$$

The product telescopes: its top is $(n-2)!$ and its bottom is $n!/2$. For $n = 10$ the bound is $1/45 \approx 0.0222$. Mitzenmacher and Upfal, Section 1.5, and Motwani and Raghavan, Chapter 1, give this analysis.

**Two keys in randomized quicksort.** Let $z_1 < \cdots < z_n$ be the sorted keys, and $Z_{ij} = \{z_i, \ldots, z_j\}$. Until the first pivot from $Z_{ij}$ is chosen, all of $Z_{ij}$ is in one subarray, because a pivot outside $Z_{ij}$ is either below or above all of it. When the pivot is drawn from a subarray of size $s$ that holds $Z_{ij}$, and we condition on the event that it lands in $Z_{ij}$, each key of $Z_{ij}$ has conditional probability $(1/s) / (|Z_{ij}|/s) = 1/(j - i + 1)$. The keys $z_i$ and $z_j$ are compared exactly when this first pivot from $Z_{ij}$ is $z_i$ or $z_j$. By the law of total probability over the step at which this happens, the probability is $2/(j - i + 1)$. CLRS, Section 7.4.2, uses it to get the expected number of comparisons, see [quicksort expected running time](/quicksort-expected-running-time/).

**Bloom filter answers.** A [Bloom filter](/bloom-filter/) has a false positive rate of 1%: a key that is not in the set gets the answer "present" with probability $0.01$. Keys in the set always get "present". Suppose 10% of the queries are for keys in the set. Let $S$ be "the key is in the set" and $P$ be "the answer is present". Then $\Pr(P) = 1 \cdot 0.1 + 0.01 \cdot 0.9 = 0.109$, and Bayes' theorem gives $\Pr(S \mid P) = 0.1 / 0.109 \approx 0.917$. So about 8.3% of the "present" answers are wrong, much more than 1%.

**Miller-Rabin and the base rate.** One round of the [Miller-Rabin test](/miller-rabin-primality-test/) passes an odd composite number with probability at most $1/4$, over the random base. That is $\Pr(\text{pass} \mid \text{composite}) \le 1/4$, not $\Pr(\text{composite} \mid \text{pass})$. Take a random odd number near $2^{1024}$. By the prime number theorem, about $2/\ln(2^{1024}) \approx 0.00282$ of such numbers are prime. With only the bound $1/4$, Bayes' theorem gives $\Pr(\text{composite} \mid \text{one pass}) \le 0.989$. With $t$ rounds and independent bases the bound becomes $4^{-t}$ in place of $1/4$, and the result is about $3.4 \times 10^{-4}$ for $t = 10$ and $2.9 \times 10^{-22}$ for $t = 40$. The bound $1/4$ is a worst case over all odd composites, so the true values for random numbers can be smaller.

**Retries across two servers.** A load balancer sends 70% of the requests to server $A$, which fails 1% of the time, and 30% to server $B$, which fails 5% of the time. The law of total probability gives $\Pr(\text{fail}) = 0.7 \cdot 0.01 + 0.3 \cdot 0.05 = 0.022$. Bayes' theorem gives $\Pr(A \mid \text{fail}) = 0.007 / 0.022 \approx 0.318$: most failures come from $B$, although $B$ gets fewer requests.

**Non-example: conditioning on a null event.** Let $U$ be uniform on $[0, 1]$. The expression $\Pr(U < 1/2 \mid U = 1/3)$ is not defined by the formula, because $\Pr(U = 1/3) = 0$. A value for it needs a limit or the theory of [conditional expectation](/conditional-expectation/), and different limits can give different answers.

### Pitfalls

- **$\Pr(A \mid B)$ is not $\Pr(B \mid A)$.** The Bloom filter and Miller-Rabin examples show how far apart they can be. The link is Bayes' theorem, and it needs the prior $\Pr(B)$.
- **Know what you condition on.** "At least one of two keys hashes to bucket 0" and "the first key hashes to bucket 0" are different events, and they give different conditional probabilities that both keys do. With $m = 2$ buckets the answers are $1/3$ and $1/2$. The [Monty Hall problem](/monty-hall-problem/) is a famous case of this error.
- **The conditioning event must not depend on the answer you want.** In an analysis that "conditions on the algorithm being lucky so far", check that the event is defined before the step you study, as $E_1 \cap \cdots \cap E_{i-1}$ is in Karger's analysis.
- **Conditioning can create or destroy independence.** Two independent fair bits $X$ and $Y$ are not independent given $X + Y = 1$: then $Y = 1 - X$.

## Related definitions

- $A$ and $B$ are [independent events](/independent-events/) when $\Pr(A \cap B) = \Pr(A) \Pr(B)$, that is $\Pr(A \mid B) = \Pr(A)$ when $\Pr(B) > 0$.
- [Conditional expectation](/conditional-expectation/) $\mathbb{E}[X \mid B]$ is the expected value of $X$ under the measure $\Pr(\cdot \mid B)$.
- [Bayes' theorem](/bayes-theorem/) is the rule above, used for inference.
- A [Markov chain](/markov-chain/) is defined by the conditional probabilities of the next state given the present one.

## References
