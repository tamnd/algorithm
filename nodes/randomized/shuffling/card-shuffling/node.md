---
tag: 33YR4Y
kind: problem
slug: card-shuffling
name: Card shuffling (mixing a deck)
aliases:
- deck shuffling
- mixing time of card shuffles
- how many shuffles
area: randomized/shuffling
level: advanced
summary: Determine how many shuffles of a deck are needed before its order is close to uniform, as measured by total variation distance.
prereqs: [markov-chain, total-variation-distance, mixing-time, symmetric-group]
see_also: [gilbert-shannon-reeds-model, bayer-diaconis-theorem, top-to-random-shuffle, random-transposition-shuffle, overhand-shuffle-model, strong-uniform-time, faro-shuffle, random-permutation]
sources:
  - paper: "David Aldous and Persi Diaconis, Shuffling cards and stopping times, American Mathematical Monthly 93(5), 1986"
    locator: pp. 333 to 348 (the question, the variation distance, strong uniform times and the cutoff phenomenon)
  - paper: "Dave Bayer and Persi Diaconis, Trailing the dovetail shuffle to its lair, Annals of Applied Probability 2(2), 1992"
    locator: pp. 294 to 313 (riffle shuffles, 52 cards)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapters 3 and 4 (random walks on groups, the upper bound lemma, many shuffles) (to be checked)
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, Markov Chains and Mixing Times, second edition, 2017
    locator: Chapters 4 to 8 (total variation, coupling, strong stationary times, lower bounds, shuffling) and Chapter 18 (the cutoff phenomenon) (chapter numbers to be checked)
  - paper: "Persi Diaconis, The cutoff phenomenon in finite Markov chains, Proceedings of the National Academy of Sciences of the USA 93(4), 1996"
    locator: pp. 1659 to 1664 (to be checked)
---

The card shuffling problem asks: for a given way of shuffling a deck of $n$ cards, how many shuffles are needed before the order of the deck is close to uniform? A shuffle is modelled as a random permutation with a fixed law, applied again and again, so the deck is a [Markov chain](/markov-chain/) on the $n!$ orders, a random walk on the [symmetric group](/symmetric-group/). The answer is its [mixing time](/mixing-time/), usually measured in [total variation distance](/total-variation-distance/). Different shuffles give very different answers: about $\frac32 \log_2 n$ riffle shuffles, $\frac12 n \ln n$ random transpositions, $n \ln n$ top-to-random moves, and order $n^2 \log n$ overhand shuffles. Many of these chains show a cutoff: the distance stays near 1 and then drops to near 0 in a short window. This is a different problem from [random permutation generation](/random-permutation/), where a computer produces an exactly uniform order in one pass.

## In plain words

People shuffle cards by hand, and each shuffle mixes the deck a little. A game is fair only if the deck is mixed well, so we ask how many shuffles of a given kind are enough.

To answer, we treat each shuffle as a random rearrangement with known chances, and we measure how far the chances of all orders of the deck are from being equal. Often the deck stays clearly unmixed for a while, then becomes well mixed within a few more shuffles. The answer depends a lot on the kind of shuffle. Riffle shuffles, where two halves are interleaved, need only about seven for an ordinary deck. Overhand shuffles, where small packets are slid from one hand to the other, need far more. A computer does not need any of this: it can produce a perfectly mixed order in one pass.

## Definition

**Input.** A deck size $n$ and a *shuffle*, a probability law $Q$ on the permutations of $n$ positions. One shuffle applies a permutation drawn from $Q$, independent of the past.

**The chain.** From a fixed start order, the law of the deck after $t$ shuffles is $P^t = Q^{*t}$, the $t$-fold convolution. Let $\pi$ be the uniform law and
$$d(t) = \|P^t - \pi\|_{TV} = \max_{A} \bigl(\pi(A) - P^t(A)\bigr) = \frac12 \sum_\sigma |P^t(\sigma) - \pi(\sigma)|.$$
By symmetry of the group, $d(t)$ does not depend on the start order.

**Output.** The mixing time $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$, often with $\varepsilon = \frac14$, or its asymptotic form as $n \to \infty$. A sequence of chains has a **cutoff** at $t_n$ with window $w_n = o(t_n)$ if $d(t_n - c w_n) \to 1$ and $d(t_n + c w_n) \to 0$ as first $n \to \infty$ and then $c \to \infty$.

**Convergence.** If the support of $Q$ generates the symmetric group and the chain is aperiodic (for example $Q(\text{identity}) > 0$), then $d(t) \to 0$. Otherwise the deck never mixes, as with the deterministic [faro shuffle](/faro-shuffle/) or with random transpositions that always swap two different cards, where the parity of the deck is fixed by $t$.

## Variants

- **Other distances.** The separation $s(t) = 1 - n! \min_\sigma P^t(\sigma)$, measured exactly by [strong uniform times](/strong-uniform-time/); the $\ell^2$ distance, which the Fourier method bounds; and the relative entropy. Each gives its own number of shuffles. For riffles, separation needs about $2 \log_2 n$ shuffles against $\frac32 \log_2 n$ in total variation.
- **Specific features.** A game may depend only on some features of the order, such as the top card, the suits of the first few cards, or the rising sequences. Fewer shuffles may make such features close to uniform.
- **Exact mixing at a random time.** Run the chain until a strong uniform time and stop; the deck is then exactly uniform. See the exact versions on the [top-to-random](/top-to-random-shuffle/) and [random transposition](/random-transposition-shuffle/) pages.
- **Many decks.** Casinos shuffle several decks together; the theory applies with larger $n$.

## Examples

The table lists the standard models. The numbers for 52 cards are computed from the formulas or the exact computations on the linked pages.

| shuffle | mixing time | cutoff | 52 cards |
|---|---|---|---|
| riffle ([GSR](/gilbert-shannon-reeds-model/)) | $\frac32 \log_2 n$ | yes, window $O(1)$ | $d = 0.61, 0.33, 0.17, 0.085$ after 6, 7, 8, 9 shuffles |
| [random transpositions](/random-transposition-shuffle/) | $\frac12 n \ln n$ | yes, window $O(n)$ | about 103 moves |
| [top-to-random](/top-to-random-shuffle/) | $n \ln n$ | yes, window $O(n)$ | about 205 moves; the exact stopping time has mean 236 |
| [overhand](/overhand-shuffle-model/), cut probability $p$ | $\Theta(n^2 \log n)$ | open on this page | with $p = \frac12$, over 100 shuffles for the top card alone |
| adjacent transpositions | $\Theta(n^3 \log n)$ | yes (Lacoin 2016; to be checked) | |
| [perfect faro](/faro-shuffle/) | never | | 8 out-shuffles restore the deck |

**Four cards.** The exact distances for $t = 1, 2, 3$ steps are: riffle $0.5, 0.2812, 0.1445$; random transpositions $0.7083, 0.2812, 0.1693$; top-to-random $0.8333, 0.5, 0.3125$. All were computed with exact fractions over the 24 orders.

**Seven riffles.** For 52 cards, $d(7) \approx 0.334$: seven is the first number of riffles with $d < \frac12$, not a point of exact randomness. See the [Bayer-Diaconis theorem](/bayer-diaconis-theorem/).

## Known algorithms

Here the "algorithms" are methods to compute or bound $d(t)$.

- **Exact computation.** For small $n$, multiply out $P^t$ over all $n!$ orders. If $Q$ is constant on conjugacy classes, as for random transpositions, $P^t$ is too, and it suffices to track the cycle type. For riffles, the Bayer-Diaconis formula reduces $d(t)$ to a sum of $n$ terms.
- **[Strong uniform times](/strong-uniform-time/)**: $d(t) \le \Pr[T > t]$. They give the upper bounds for top-to-random ($n \ln n$), riffles ($2 \log_2 n$) and random transpositions (Broder, $2 n \ln n$).
- **[Coupling](/coupling-method/)**: $d(t) \le \Pr[\text{two copies have not met by } t]$.
- **Fourier analysis on the group.** The upper bound lemma $4 d(t)^2 \le \sum_{\rho \ne 1} d_\rho \operatorname{tr}\bigl(\hat Q(\rho)^t \hat Q(\rho)^{t*}\bigr)$ over the irreducible representations; it gave the first sharp result, for random transpositions (Diaconis and Shahshahani 1981).
- **Eigenvalues and the [spectral gap](/spectral-gap/)**, and comparison of one chain with another with known eigenvalues.
- **Lower bounds by test sets.** Choose an event $A$ that the chain reaches slowly: fixed points (random transpositions), the relative order of the bottom cards (top-to-random), the number of rising sequences (riffles). Then $d(t) \ge P^t(A) - \pi(A)$. Wilson's method uses an eigenfunction as the test statistic, as for overhand shuffles and adjacent transpositions.

## Bounds

**A counting lower bound.** If one shuffle can produce at most $m$ different permutations, then
$$d(t) \ge 1 - \frac{m^t}{n!}.$$
*Proof.* $P^t$ is supported on a set $S$ of at most $m^t$ orders. Then $d(t) \ge P^t(S) - \pi(S) \ge 1 - m^t / n!$. ∎ So at least $\log(n!) / \log m$ shuffles are needed for any $\varepsilon < 1$, up to an additive constant. For riffles, $m = 2^n - n$, and since $\log_2 52! \approx 225.6$, four riffles of 52 cards reach at most $2^{208}$ orders and $d(4) \ge 1 - 2^{-17}$. This gives the order $\log_2 n$; the sharp constant $\frac32$ needs more.

**Never exact at a fixed time.** If all probabilities of $Q$ are multiples of $1/N$, then all probabilities of $P^t$ are multiples of $1/N^t$, and $d(t) = 0$ is possible only if $n!$ divides $N^t$. For the top-to-random shuffle ($N = n$) and random transpositions ($N = n^2$) this fails for $n \ge 3$, because $n - 1$ divides $n!$ and is coprime to $n$. For riffles, $N = 2^n$ and $n!$ has odd factors for $n \ge 3$. So these chains get close to uniform but never reach it at a fixed $t$.

**General upper bound.** Every aperiodic irreducible chain on a finite set has $d(t) \le C \alpha^t$ for some $\alpha < 1$; the question is how $t_{mix}$ grows with $n$.

## Reductions

- **To mixing of a random walk on a group.** Every shuffle model is such a walk, so the tools for walks on groups apply directly.
- **A walk and its inverse.** The law of $\sigma^{-1}$ for $\sigma \sim P^t$ is the $t$-step law of the inverse walk, and inversion preserves the uniform law, so a shuffle and its inverse have the same $d(t)$. Riffles are analysed through inverse riffles, and top-to-random through random-to-top.
- **To [random permutation](/random-permutation/) generation.** A computer needs one exact draw, not a chain: [Fisher-Yates](/fisher-yates-shuffle/) is the exact one-step shuffle, and the exact versions of the chains stop at a strong uniform time.

## Applications

- **Card games and casinos.** Too few riffles leave rising sequences that a player can use; the Bayer-Diaconis analysis gives the number of shuffles for a fair game. Shuffling machines and dealer procedures are judged by the same measures.
- **Magic.** Card tricks that work after a few riffles use the surviving rising sequences (Bayer and Diaconis 1992; to be checked).
- **Markov chain Monte Carlo.** Card shuffles are the model examples for the mixing analysis of samplers, including the cutoff phenomenon.
- **Randomized experiments and audits.** Physical randomization, for example of ballots or of lottery balls, raises the same question of how much mixing is enough.

## References
