---
tag: J6XJBV
kind: concept
slug: independence-of-events
name: Independence of events
aliases:
- Compound events and independence
area: foundations/probabilistic-analysis
level: intro
summary: Two events are independent when the occurrence of one does not change the probability of the other, so the joint probability is the product.
prereqs: [probability-space, conditional-probability, independent-events]
see_also: [independent-events, independent-random-variables, conditional-probability, monte-carlo-algorithm, birthday-paradox, simple-uniform-hashing, pairwise-independence]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2, Probability (independent events, pairwise and mutual independence, conditional probability)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.2, Axioms of Probability (independence, the principle of deferred decisions), Section 1.3 (matrix product verification) and Section 1.5 (randomized min-cut)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter V, Conditional Probability. Stochastic Independence
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (Las Vegas and Monte Carlo algorithms, the min-cut algorithm)
---

Independence of events is the property that the occurrence of one event gives no information about another, so that the probability that both occur is the product of their probabilities. This page explains the idea and how analyses use it: compound events, the product rule, the gap between pairwise and mutual independence, and the difference from disjointness and from conditional independence. The formal definition, with its exact conditions for families of events, is on the page [independent events](/independent-events/). In the analysis of [randomized algorithms](/randomized-algorithm/), independence is what turns the error of one run into the much smaller error of many runs.

## In plain words

Flip a coin and roll a die. Whatever the coin shows, the die is still fair. Knowing one result does not help you guess the other. That is independence. Because of it, the chance of "heads and a six" is the chance of heads times the chance of a six.

Many results are not like this. If you draw two cards from one deck without putting the first back, the first card changes what the second card can be.

Programs use independence all the time. A random test that is wrong half of the time is still useful: run it twenty times with fresh random choices, and the chance that all twenty runs are wrong is about one in a million. That multiplication is only correct because the runs do not affect each other.

## The idea

Fix a [probability space](/probability-space/) with sample space $S$ and probability $\Pr$. A compound event is an event built from other events with "and", "or" and "not", that is, with $\cap$, $\cup$ and complement $\overline{A} = S \setminus A$. In general the probability of a compound event depends on how the parts overlap, and the parts alone do not fix it. Independence is the case where the parts do fix it.

### The product rule and the conditional view

Events $A$ and $B$ are independent when
$$ \Pr[A \cap B] = \Pr[A]\,\Pr[B]. $$
When $\Pr[B] > 0$, this is the same as $\Pr[A \mid B] = \Pr[A]$, because $\Pr[A \mid B] = \Pr[A \cap B]/\Pr[B]$ by the definition of [conditional probability](/conditional-probability/). So "learning that $B$ occurred does not change the probability of $A$". The product form is the one used as the definition, because it is symmetric in $A$ and $B$ and it also makes sense when $\Pr[B] = 0$. An event of probability 0 or 1 is independent of each event.

### Independence survives complements

If $A$ and $B$ are independent, then so are $A$ and $\overline{B}$, $\overline{A}$ and $B$, and $\overline{A}$ and $\overline{B}$.

*Proof.* The event $A$ is the disjoint union of $A \cap B$ and $A \cap \overline{B}$, so
$$ \Pr[A \cap \overline{B}] = \Pr[A] - \Pr[A \cap B] = \Pr[A] - \Pr[A]\Pr[B] = \Pr[A]\,(1 - \Pr[B]) = \Pr[A]\,\Pr[\overline{B}]. $$
So $A$ and $\overline{B}$ are independent. The case of $\overline{A}$ and $B$ is the same with the names exchanged. Apply the first case to the independent pair $\overline{A}, B$ to get the pair $\overline{A}, \overline{B}$. $\square$

The same argument, applied to one event at a time, shows that in a mutually independent family you can replace any of the events by their complements and the family stays mutually independent. This gives the rule for "at least one": if $A_1, \ldots, A_k$ are mutually independent, then
$$ \Pr[A_1 \cup \cdots \cup A_k] = 1 - \Pr[\overline{A_1} \cap \cdots \cap \overline{A_k}] = 1 - \prod_{i=1}^{k} (1 - \Pr[A_i]). $$
Without independence, only the [union bound](/union-bound/) $\Pr[A_1 \cup \cdots \cup A_k] \le \sum_i \Pr[A_i]$ is available.

### Pairwise is weaker than mutual

For more than two events there are two notions. The events $A_1, \ldots, A_n$ are pairwise independent when each pair satisfies the product rule. They are mutually independent when the product rule holds for each subfamily: for each $T \subseteq \{1, \ldots, n\}$ with $|T| \ge 2$,
$$ \Pr\Big[\bigcap_{i \in T} A_i\Big] = \prod_{i \in T} \Pr[A_i]. $$
That is $2^n - n - 1$ equations: 1 for two events, 4 for three, 11 for four, and 1013 for ten. Pairwise independence checks only the $\binom{n}{2}$ equations with $|T| = 2$.

The standard example shows that the other equations matter. Flip two fair coins independently, and write the outcomes as bits $b_1, b_2$. Let $A = \{b_1 = 1\}$, $B = \{b_2 = 1\}$ and $C = \{b_1 \oplus b_2 = 1\}$, where $\oplus$ is exclusive or. Each event has probability $\frac12$. Each pair meets in one of the four outcomes, so each pair has probability $\frac14 = \frac12 \cdot \frac12$, and the three events are pairwise independent. But $A \cap B$ forces $b_1 \oplus b_2 = 0$, so $\Pr[A \cap B \cap C] = 0 \ne \frac18$. Any two of the events determine the third. Constructions of [pairwise independence](/pairwise-independence/) from few random bits are built on exactly this example, see [independent random variables](/independent-random-variables/).

### Independent is not disjoint

Disjoint events with positive probability are never independent. If $A \cap B = \emptyset$ and $\Pr[A], \Pr[B] > 0$, then $\Pr[A \cap B] = 0 < \Pr[A]\Pr[B]$. Disjointness is the strongest dependence: if $A$ occurs, $B$ surely does not. Disjointness makes probabilities add ($\Pr[A \cup B] = \Pr[A] + \Pr[B]$). Independence makes probabilities of intersections multiply.

### Conditional independence is a different property

$A$ and $B$ are conditionally independent given $C$, with $\Pr[C] > 0$, when $\Pr[A \cap B \mid C] = \Pr[A \mid C]\,\Pr[B \mid C]$. Neither property implies the other.

- *Conditionally independent, but not independent.* A bag holds a fair coin and a coin with two heads. Pick one coin uniformly at random and flip it twice. Given the coin, the two flips are independent. Without the coin, let $H_1$ and $H_2$ be "heads on flip 1" and "heads on flip 2". Then $\Pr[H_1] = \frac12 \cdot \frac12 + \frac12 \cdot 1 = \frac34$, and $\Pr[H_1 \cap H_2] = \frac12 \cdot \frac14 + \frac12 \cdot 1 = \frac58$, which is not $\left(\frac34\right)^2 = \frac{9}{16}$. Heads on the first flip makes the two-headed coin more likely, and so makes heads on the second flip more likely.
- *Independent, but not conditionally independent.* In the two-bit example, $A$ and $B$ are independent. Given $C$, exactly one of the bits is 1, so $\Pr[A \cap B \mid C] = 0$ while $\Pr[A \mid C] = \Pr[B \mid C] = \frac12$.

### Pitfalls

- **Assuming independence from a story.** Independence is an equation about $\Pr$, not a statement that two parts of a program "do not talk to each other". Two calls that read the same random seed, the same [pseudorandom generator](/pseudorandom-number-generator/) state or the same random hash function are dependent, even when the code paths are separate.
- **Multiplying three or more probabilities after checking pairs.** Pairwise independence does not justify $\Pr[A \cap B \cap C] = \Pr[A]\Pr[B]\Pr[C]$, as the two-bit example shows.
- **Confusing independent with disjoint.** For disjoint events add, for independent events multiply. Using the sum for independent events gives $\Pr[A \cup B] = 1.0$ for two independent events of probability $\frac12$; the correct value is $1 - \frac12 \cdot \frac12 = \frac34$.
- **Forgetting the condition.** A product of conditional probabilities $\Pr[A \mid C]\Pr[B \mid C]$ needs conditional independence given $C$, which independence does not give.

## Examples

**Amplifying a one-sided error.** A [Monte Carlo algorithm](/monte-carlo-algorithm/) with one-sided error answers "yes" correctly each time, and on a "no" instance answers wrongly with probability at most $p < 1$. Run it $k$ times with fresh random bits and answer "no" if any run says "no". The runs use disjoint random bits, so the events "run $i$ errs" are mutually independent, and the result is wrong only if all $k$ runs err:
$$ \Pr[\text{all } k \text{ runs err}] = \prod_{i=1}^{k} \Pr[\text{run } i \text{ errs}] \le p^k. $$
[Freivalds' algorithm](/freivalds-algorithm/) checks a matrix product $AB = C$ with one random 0 or 1 vector, and it errs with probability at most $\frac12$. Twenty independent runs bring the error down to at most $2^{-20} = 9.54 \times 10^{-7}$, and each run costs three matrix-vector products, $\Theta(n^2)$ time for $n \times n$ matrices.

**Repeating Karger's contraction.** One run of [Karger's min-cut algorithm](/karger-min-cut/) on a graph with $n$ vertices finds a given minimum cut with probability at least $2/(n(n-1))$. For $n = 50$ this is $1/1225$. The algorithm fails after $t$ independent runs only if every run misses, which has probability at most $(1 - 1/1225)^t$. For $t = 1225$ the bound is $0.3677$, close to $e^{-1} = 0.3679$. For $t = 12250$ it is $4.52 \times 10^{-5}$, close to $e^{-10}$. In general $(1 - q)^t \le e^{-qt}$, so $t = \lceil \ln(1/\delta)/q \rceil$ runs bring the failure probability below $\delta$.

**A product of conditional probabilities.** In the [birthday paradox](/birthday-paradox/), 23 people have birthdays that are independent and uniform over 365 days. The probability that all are distinct is the product, over $i = 1, \ldots, 22$, of the probability that person $i+1$ avoids the $i$ earlier birthdays given that those are distinct, which is $(365 - i)/365$ by independence. The product is $0.4927$, so a shared birthday has probability $0.5073$. Here the events "person $i+1$ avoids the earlier birthdays" are not independent of each other; independence of the birthdays is what fixes each conditional factor.

**A non-example from sampling without replacement.** Draw two cards from a deck of 52 without replacement. Let $A$ be "the first card is an ace" and $B$ "the second card is an ace". Then $\Pr[A] = \Pr[B] = \frac{4}{52}$, but $\Pr[B \mid A] = \frac{3}{51} \ne \frac{4}{52}$, so the events are dependent. With replacement they are independent.

## Where it is used

- **Error reduction.** Amplification of Monte Carlo algorithms ([Freivalds' algorithm](/freivalds-algorithm/), [Miller-Rabin](/miller-rabin/)) and of Las Vegas algorithms with a time limit ([Las Vegas algorithm](/las-vegas-algorithm/)) rests on the product rule for independent runs.
- **Hashing.** The [simple uniform hashing](/simple-uniform-hashing/) assumption says that keys hash to independent uniform slots, so two given keys collide with probability $1/m$ for $m$ slots. [Universal hash families](/universal-hash-family/) give this pairwise bound without full independence.
- **Repeated trials.** [Bernoulli trials](/bernoulli-trials/), and with them the [binomial](/binomial-distribution/) and [geometric distributions](/geometric-distribution/), are defined by mutually independent events of equal probability.
- **Tail bounds.** The [Chernoff bound](/chernoff-bound/) needs mutual independence of the events it counts. Pairwise independence is enough for the [Chebyshev inequality](/chebyshev-inequality/) on a count, see [independent random variables](/independent-random-variables/).
- **Random variables.** Independence of random variables, on the page [independent random variables](/independent-random-variables/), is independence of all the events $\{X \in A\}$ and $\{Y \in B\}$ that they define.

## References
