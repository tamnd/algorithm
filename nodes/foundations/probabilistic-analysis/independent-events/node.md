---
tag: FWHF55
kind: definition
slug: independent-events
name: Independent events
area: foundations/probabilistic-analysis
level: intro
summary: Two events are independent when the probability that both occur equals the product of their individual probabilities.
prereqs: [probability-space, conditional-probability]
see_also: [independence-of-events, independent-random-variables, pairwise-independence, k-wise-independent-hashing, universal-hash-family, limited-independence, bernoulli-trials, union-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2 (conditional probability and independence, pairwise and mutual independence)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.2, Axioms of Probability (independence); Section 15.1, Pairwise Independence
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Appendix C, Basic Probability Theory
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter V, Conditional Probability. Stochastic Independence
---

Two events $A$ and $B$ are independent when $\Pr(A \cap B) = \Pr(A) \Pr(B)$: knowing that one occurred does not change the [conditional probability](/conditional-probability/) of the other. For more than two events there are several strengths of independence: pairwise, $k$-wise and mutual. The difference matters in algorithms, because cheap [hash families](/universal-hash-family/) give only pairwise or [$k$-wise independence](/k-wise-independent-hashing/), and some tail bounds need mutual independence.

## Definition

Let $(\Omega, \mathcal{F}, \Pr)$ be a [probability space](/probability-space/).

**Two events.** Events $A$ and $B$ are **independent** when

$$\Pr(A \cap B) = \Pr(A) \Pr(B).$$

If $\Pr(B) > 0$, this is the same as $\Pr(A \mid B) = \Pr(A)$: divide both sides by $\Pr(B)$. The definition by the product is symmetric, and it also covers $\Pr(B) = 0$.

**A family of events.** Events $A_1, \ldots, A_n$ are

- **pairwise independent** when $\Pr(A_i \cap A_j) = \Pr(A_i) \Pr(A_j)$ for all $i \ne j$;
- **$k$-wise independent** when $\Pr\left(\bigcap_{i \in I} A_i\right) = \prod_{i \in I} \Pr(A_i)$ for each index set $I$ with $|I| \le k$;
- **mutually independent** (or just independent) when the product rule holds for every index set $I \subseteq \{1, \ldots, n\}$.

An infinite family is mutually independent when each finite subfamily is. Mutual independence of $n$ events is $2^n - n - 1$ equations, one for each $I$ with $|I| \ge 2$. For three events that is 4 equations: three for the pairs and one for the triple.

### Properties

**(a) Complements.** If $A$ and $B$ are independent, then so are $A$ and $\bar B$. Proof: $A$ is the disjoint union of $A \cap B$ and $A \cap \bar B$, so $\Pr(A \cap \bar B) = \Pr(A) - \Pr(A)\Pr(B) = \Pr(A)(1 - \Pr(B)) = \Pr(A) \Pr(\bar B)$. Applying this twice gives $\bar A$ and $\bar B$.

**(b) Complements in a family.** If $A_1, \ldots, A_n$ are mutually independent, then so are $B_1, \ldots, B_n$ where each $B_i$ is $A_i$ or $\bar A_i$. Proof by induction on the number of complemented events. It suffices to replace one event, say $A_1$, by $\bar A_1$, in a family that is already mutually independent. Take an index set $I$ that contains 1, and let $C = \bigcap_{i \in I \setminus \{1\}} A_i$, with $C = \Omega$ when $I = \{1\}$. Then $\Pr(\bar A_1 \cap C) = \Pr(C) - \Pr(A_1 \cap C) = \prod_{i \in I \setminus\{1\}} \Pr(A_i) \cdot (1 - \Pr(A_1))$. Index sets without 1 are not affected.

**(c) None of them occurs.** If $A_1, \ldots, A_n$ are mutually independent with $\Pr(A_i) = p_i$, then by (b),

$$\Pr\left(\bigcap_i \bar A_i\right) = \prod_{i=1}^n (1 - p_i) \le \exp\left(-\sum_{i=1}^n p_i\right),$$

since $1 - x \le e^{-x}$ for all real $x$. So the probability that at least one occurs is $1 - \prod_i (1 - p_i)$, and it is close to 1 when $\sum_i p_i$ is large. The [union bound](/union-bound/) gives the other side, $\Pr(\bigcup_i A_i) \le \sum_i p_i$, with no independence.

**(d) An event and itself.** $A$ is independent of $A$ exactly when $\Pr(A) = \Pr(A)^2$, that is $\Pr(A) \in \{0, 1\}$. An event with probability 0 or 1 is independent of every event: if $\Pr(A) = 0$, then $\Pr(A \cap B) \le \Pr(A) = 0$, and if $\Pr(A) = 1$, use (a) on $\bar A$.

**(e) Disjoint is not independent.** If $A \cap B = \emptyset$ and both have positive probability, then $\Pr(A \cap B) = 0 < \Pr(A)\Pr(B)$. Disjoint events with positive probability are dependent: if one occurs, the other cannot.

## Examples and non-examples

**Independent retries.** A client tries a request up to 3 times, and each attempt fails with probability $0.1$, independently of the other attempts. By (c), all three fail with probability $0.1^3 = 0.001$, and $t$ attempts all fail with probability $0.1^t$. The number of attempts until success is [geometric](/geometric-distribution/).

**Coin flips in a skip list.** In a [skip list](/skip-list/), each key flips its own coins. The events "key $x$ reaches level 2" and "key $y$ reaches level 2" for $x \ne y$ are independent, each with probability $1/2$, so both reach level 2 with probability $1/4$. The flips are [Bernoulli trials](/bernoulli-trials/).

**Pairwise but not mutually independent.** Flip two fair coins $X_1, X_2 \in \{0, 1\}$ and let $X_3 = X_1 \oplus X_2$. Let $A_i$ be the event $X_i = 1$. Each $A_i$ has probability $1/2$. Each pair has $\Pr(A_i \cap A_j) = 1/4$, so the events are pairwise independent. But $A_1 \cap A_2 \cap A_3 = \emptyset$, because $X_1 = X_2 = 1$ forces $X_3 = 0$. So $\Pr(A_1 \cap A_2 \cap A_3) = 0 \ne 1/8$, and they are not mutually independent. The same XOR idea, applied to all nonempty subsets of $b$ random bits, gives $2^b - 1$ pairwise independent bits (Mitzenmacher and Upfal, Section 15.1.1).

**Pairwise independent hash values.** Let $p$ be prime and choose $a, b$ uniformly and independently from $\{0, \ldots, p-1\}$. Set $h(x) = (ax + b) \bmod p$. For keys $x \ne y$ and any targets $u, v$, the system $ax + b \equiv u$, $ay + b \equiv v \pmod p$ has exactly one solution $(a, b)$, since its determinant $x - y$ is nonzero mod $p$. So $\Pr(h(x) = u, h(y) = v) = 1/p^2$: the values at two distinct keys are uniform and independent. But three values are not independent. For $p = 5$, the events $h(1) = 0$, $h(2) = 0$ and $h(3) = 0$ each have probability $1/5$, each pair has probability $1/25$, and the triple also has probability $1/25$, not $1/125$: the first two force $a = b = 0$, which forces the third. This family is the base of [universal hashing](/universal-hash-family/), see Mitzenmacher and Upfal, Chapter 15.

**A product rule for the triple only.** On 8 equally likely outcomes $\{1, \ldots, 8\}$, let $A = B = \{1, 2, 3, 4\}$ and $C = \{1, 5, 6, 7\}$. Then $\Pr(A \cap B \cap C) = \Pr(\{1\}) = 1/8 = \Pr(A)\Pr(B)\Pr(C)$. But $\Pr(A \cap B) = 1/2 \ne 1/4$. So the triple equation alone does not give independence: all $2^n - n - 1$ equations are needed.

**Non-example: one key, two buckets.** With one key and $m \ge 2$ buckets, the events "the key is in bucket 0" and "the key is in bucket 1" are disjoint with positive probability, so by (e) they are dependent.

### Pitfalls

- **Pairwise independence is not mutual independence.** It is enough for results that use only pairs, such as the additivity of [variance](/variance/) and so [Chebyshev's inequality](/chebyshev-inequality/) for sums. It is not enough for the [Chernoff bound](/chernoff-bound/), which multiplies over all the events. Know which one your hash family gives, see [limited independence](/limited-independence/).
- **Correlated failures.** Retries are often not independent. Suppose that with probability $0.05$ the server is down, so all attempts fail, and otherwise each attempt fails with probability $0.05$, independently. One attempt then fails with probability $0.05 + 0.95 \cdot 0.05 = 0.0975$. The independent model predicts that three attempts all fail with probability $0.0975^3 \approx 0.00093$. The true value is $0.05 + 0.95 \cdot 0.05^3 \approx 0.0501$, more than 50 times larger. This is why retries go to another replica, or wait with [exponential backoff](/exponential-backoff/).
- **Independence is a property of the measure.** Two events can be independent under one distribution and dependent under another, with the same sets. Check the product rule. Do not reason from the story of the events alone.
- **Disjoint and independent are different.** See property (e).

## Related definitions

- **Independence as a modelling choice.** The page [independence of events](/independence-of-events/) covers how independence is used and checked in the analysis of algorithms: when it may be assumed, how to show it, and what breaks when it fails. This page gives the formal definitions and their properties.
- [Independent random variables](/independent-random-variables/): the events $\{X \in B\}$ and $\{Y \in C\}$ are independent for all sets $B$ and $C$.
- [Pairwise independence](/pairwise-independence/) and [$k$-wise independent hashing](/k-wise-independent-hashing/) give limited independence with few random bits.
- [Bernoulli trials](/bernoulli-trials/) are mutually independent trials with the same success probability.
- [Conditional probability](/conditional-probability/): $\Pr(A \mid B) = \Pr(A)$ for independent $A$, $B$ with $\Pr(B) > 0$.
- Conditional independence given $C$: $\Pr(A \cap B \mid C) = \Pr(A \mid C)\Pr(B \mid C)$. It neither implies nor follows from independence.

## References
