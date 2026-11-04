---
tag: X8VFRC
kind: definition
slug: probability-space
name: Probability space
aliases:
- sample space
- probability measure
area: foundations/probabilistic-analysis
level: intro
summary: A sample space with events and a probability measure, the basis of all probabilistic analysis.
prereqs: [binomial-coefficient]
see_also: [probability-distribution, discrete-probability-distribution, random-variable, conditional-probability, independent-events, union-bound, inclusion-exclusion-principle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2 (Probability, the axioms of probability and discrete probability distributions)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.2, Axioms of Probability
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Appendix C, Basic Probability Theory
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter I, The Sample Space, and Chapter IV, Combination of Events
---

A probability space is a triple $(\Omega, \mathcal{F}, \Pr)$: a set $\Omega$ of outcomes, a family $\mathcal{F}$ of subsets of $\Omega$ called events, and a function $\Pr$ that gives each event a number in $[0, 1]$. Every statement of the form "with probability $p$" in the analysis of a [randomized algorithm](/randomized-algorithm/) or of an [average case](/average-case-analysis/) is a statement about one probability space. To read such a statement correctly, you must know what the outcomes are and which choices are random.

## Definition

Let $\Omega$ be a nonempty set, the **sample space**. Its elements are **outcomes** (CLRS calls them elementary events).

A family $\mathcal{F}$ of subsets of $\Omega$ is a **$\sigma$-algebra** when:

1. $\Omega \in \mathcal{F}$.
2. If $A \in \mathcal{F}$, then the complement $\bar A = \Omega \setminus A$ is in $\mathcal{F}$.
3. If $A_1, A_2, \ldots \in \mathcal{F}$, then $\bigcup_{i \ge 1} A_i \in \mathcal{F}$.

The members of $\mathcal{F}$ are the **events**. By rules 2 and 3 and De Morgan's law, $\mathcal{F}$ is also closed under countable intersections, and $\emptyset = \bar\Omega \in \mathcal{F}$.

A **probability measure** on $(\Omega, \mathcal{F})$ is a function $\Pr : \mathcal{F} \to \mathbb{R}$ with these three axioms:

1. **Nonnegativity.** $\Pr(A) \ge 0$ for each event $A$.
2. **Normalization.** $\Pr(\Omega) = 1$.
3. **Countable additivity.** If $A_1, A_2, \ldots$ are events and $A_i \cap A_j = \emptyset$ for all $i \ne j$, then $\Pr\left(\bigcup_{i \ge 1} A_i\right) = \sum_{i \ge 1} \Pr(A_i)$.

The triple $(\Omega, \mathcal{F}, \Pr)$ is a **probability space**. When $\Omega$ is finite or countable, we can take $\mathcal{F}$ to be the set of all subsets of $\Omega$, and $\Pr$ is fixed by the values $\Pr(\{\omega\})$, see [discrete probability distribution](/discrete-probability-distribution/). Almost all spaces in the analysis of algorithms are of this kind. CLRS and Mitzenmacher and Upfal work in this setting, and Feller's first volume works only with discrete sample spaces.

An event $A$ **occurs** in an outcome $\omega$ when $\omega \in A$. An event with probability 1 happens **almost surely**. An event with probability 0 is a **null event**. In a countable space with $\Pr(\{\omega\}) > 0$ for each $\omega$, the only null event is $\emptyset$. In other spaces, a nonempty event can have probability 0.

### Consequences of the axioms

The rules below hold in each probability space, for all events $A$, $B$ and $A_1, A_2, \ldots$.

**(a) $\Pr(\emptyset) = 0$.** The sets $\Omega, \emptyset, \emptyset, \ldots$ are pairwise disjoint and their union is $\Omega$. Axiom 3 gives $\Pr(\Omega) = \Pr(\Omega) + \sum_{i \ge 2} \Pr(\emptyset)$. The sum is finite, and each term is the same nonnegative number, so that number is 0.

**(b) Finite additivity.** If $A_1, \ldots, A_n$ are pairwise disjoint, then $\Pr(A_1 \cup \cdots \cup A_n) = \sum_{i=1}^n \Pr(A_i)$. Apply axiom 3 to $A_1, \ldots, A_n, \emptyset, \emptyset, \ldots$ and use (a).

**(c) Complement.** $\Pr(\bar A) = 1 - \Pr(A)$. The events $A$ and $\bar A$ are disjoint with union $\Omega$, so (b) and axiom 2 give $\Pr(A) + \Pr(\bar A) = 1$.

**(d) Monotonicity.** If $A \subseteq B$, then $\Pr(A) \le \Pr(B)$, and $\Pr(B \setminus A) = \Pr(B) - \Pr(A)$. The events $A$ and $B \setminus A$ are disjoint with union $B$, so $\Pr(B) = \Pr(A) + \Pr(B \setminus A)$, and the last term is at least 0 by axiom 1. With $B = \Omega$ this gives $\Pr(A) \le 1$.

**(e) Two-set inclusion and exclusion.** $\Pr(A \cup B) = \Pr(A) + \Pr(B) - \Pr(A \cap B)$. Write $A \cup B$ as the disjoint union of $A$ and $B \setminus (A \cap B)$, and use (b) and (d). The general form for $n$ events is the [inclusion-exclusion principle](/inclusion-exclusion-principle/).

**(f) Union bound (Boole's inequality).** $\Pr\left(\bigcup_{i \ge 1} A_i\right) \le \sum_{i \ge 1} \Pr(A_i)$. Let $B_1 = A_1$ and $B_i = A_i \setminus (A_1 \cup \cdots \cup A_{i-1})$ for $i \ge 2$. The $B_i$ are pairwise disjoint, $B_i \subseteq A_i$, and they have the same union as the $A_i$. Axiom 3 and (d) give $\Pr(\bigcup_i A_i) = \sum_i \Pr(B_i) \le \sum_i \Pr(A_i)$. This is the [union bound](/union-bound/). It needs no independence.

**(g) Continuity.** If $A_1 \subseteq A_2 \subseteq \cdots$, then $\Pr\left(\bigcup_i A_i\right) = \lim_{n \to \infty} \Pr(A_n)$. With $B_i$ as in (f), $A_n = B_1 \cup \cdots \cup B_n$, so $\Pr(A_n) = \sum_{i \le n} \Pr(B_i)$, and the limit of these partial sums is $\sum_i \Pr(B_i) = \Pr(\bigcup_i A_i)$. By (c), the dual rule holds for a decreasing sequence: if $A_1 \supseteq A_2 \supseteq \cdots$, then $\Pr\left(\bigcap_i A_i\right) = \lim_n \Pr(A_n)$.

## Examples and non-examples

**One hash value.** A [hash function](/hash-function/) that is chosen at random sends one key to a bucket in $\{0, \ldots, m-1\}$. The sample space is $\Omega = \{0, \ldots, m-1\}$, $\mathcal{F}$ is all subsets, and $\Pr(A) = |A| / m$. This is the model of [simple uniform hashing](/simple-uniform-hashing/).

**Two keys and a collision.** For two keys, $\Omega = \{0, \ldots, m-1\}^2$ with $m^2$ equally likely outcomes. The collision event $C = \{(u, v) : u = v\}$ has $m$ outcomes, so $\Pr(C) = 1/m$. For $m = 10$ there are 100 outcomes and $\Pr(C) = 0.1$.

**Many keys, and the union bound.** For $n$ keys, $\Omega = \{0, \ldots, m-1\}^n$ has $m^n$ outcomes. Let $C_{ij}$ be the event that keys $i$ and $j$ collide. By (f), the probability of at least one collision is at most $\sum_{i < j} \Pr(C_{ij}) = \binom{n}{2} / m$. For $n = 100$ and $m = 10^6$ the bound is $0.00495$. The exact value is $1 - \prod_{i=0}^{n-1} (1 - i/m) \approx 0.004938$, so the bound is close here. For $n = 23$ and $m = 365$ the bound is $0.693$ and the exact value is $0.507$: when the probability is not small, the bound is weak. See the [birthday paradox](/birthday-paradox/).

**Randomized quicksort.** The pivot choices of [randomized quicksort](/randomized-quicksort/) on $n$ distinct keys make a finite space. Each outcome is a full record of the pivots chosen, and its probability is the product of $1/s$ over the subarray sizes $s$ at the choices. For $n = 3$ there are 5 outcomes: the middle key as first pivot (probability $1/3$), or an end key as first pivot and then one of the two keys that remain (probability $1/3 \cdot 1/2 = 1/6$ each, four outcomes). The probabilities sum to 1.

**Infinite coin flips.** A loop that flips a fair coin until it sees heads has no bound on the number of flips. One space for it is $\Omega = \{1, 2, 3, \ldots\} \cup \{\infty\}$, where $k$ means "first heads at flip $k$", with $\Pr(\{k\}) = 2^{-k}$ and $\Pr(\{\infty\}) = 0$. The sum $\sum_{k \ge 1} 2^{-k} = 1$, so the loop stops almost surely, but the outcome $\infty$ is in the space. This is the model of [geometric](/geometric-distribution/) waiting times, such as the level of a node in a [skip list](/skip-list/). The full space of infinite flip sequences, $\Omega = \{0, 1\}^{\mathbb{N}}$, is uncountable. On it, each single sequence has probability 0, so $\mathcal{F}$ cannot be fixed by values on single outcomes, and one takes the $\sigma$-algebra made by the events that depend on finitely many flips.

**Non-example: weights that do not sum to 1.** On $\Omega = \{1, 2, 3, \ldots\}$, the weights $\Pr(\{k\}) = 1/k^2$ violate axiom 2, because $\sum_{k \ge 1} 1/k^2 = \pi^2/6$. Divide each weight by $\pi^2/6$ to get a probability measure.

**Non-example: a uniform random natural number.** There is no probability measure on $\mathbb{N}$ that gives the same value $c$ to each single number. If $c = 0$, countable additivity gives $\Pr(\mathbb{N}) = 0$. If $c > 0$, it gives $\Pr(\mathbb{N}) = \infty$. Both violate axiom 2. So "pick a random integer" has no meaning until you give a distribution, for example uniform on $\{0, \ldots, N-1\}$.

**Non-example: finite additivity only.** A function that is additive on finite disjoint unions but not on countable ones is not a probability measure. The rule (g), used to show that a loop stops almost surely, depends on countable additivity.

### Pitfalls

- **Name the space.** "The probability that quicksort makes more than $2n \ln n$ comparisons" is about the pivot choices for a fixed input in randomized quicksort, and about a random input order in deterministic quicksort. These are different spaces, and the statements give different guarantees. See [average-case analysis](/average-case-analysis/).
- **Probability 0 is not impossible.** In the space of infinite flip sequences, each single sequence has probability 0 but can occur.
- **Not every subset can be an event.** On $[0, 1)$ there is no countably additive, shift-invariant measure that is defined on all subsets and gives each interval its length. This is why the definition has $\mathcal{F}$. For a countable $\Omega$, the problem does not appear.

## Related definitions

- A [probability distribution](/probability-distribution/) is the function $\Pr$, or the measure that a [random variable](/random-variable/) induces on its values.
- A [discrete probability distribution](/discrete-probability-distribution/) is a probability measure on a countable $\Omega$, given by its point masses.
- A [random variable](/random-variable/) is a function $X : \Omega \to \mathbb{R}$ such that $\{X \le x\}$ is an event for each $x$.
- [Conditional probability](/conditional-probability/) $\Pr(A \mid B)$ defines a new probability measure on the same $(\Omega, \mathcal{F})$.
- [Independent events](/independent-events/) are events with $\Pr(A \cap B) = \Pr(A) \Pr(B)$.
- A [probabilistic Turing machine](/probabilistic-turing-machine/) defines a probability space on its random bits for each input.

## References
