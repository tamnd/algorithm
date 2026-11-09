---
tag: XAGRT8
kind: concept
slug: strong-uniform-time
name: Strong uniform time
aliases:
- strong stationary time
- Aldous-Diaconis strong uniform time
- SUT
area: randomized/shuffling
level: advanced
summary: A stopping time at which a Markov chain's state is exactly uniform and independent of the stopping time. Its tail bounds the distance to uniform, d(t) ≤ Pr(T > t), which bounds mixing times.
prereqs: [markov-chain, total-variation-distance, stationary-distribution]
see_also: [top-to-random-shuffle, random-transposition-shuffle, gilbert-shannon-reeds-model, mixing-time, coupling-method, card-shuffling, coupon-collector-problem, bayer-diaconis-theorem]
sources:
  - paper: "David Aldous and Persi Diaconis, Shuffling cards and stopping times, American Mathematical Monthly 93(5), 1986"
    locator: pp. 333 to 348; the definition of a strong uniform time and the bound by Pr(T > k) (section numbers to be checked)
  - paper: "David Aldous and Persi Diaconis, Strong uniform times and finite random walks, Advances in Applied Mathematics 8(1), 1987"
    locator: pp. 69 to 97; separation distance, and the existence of a strong uniform time with Pr(T > k) equal to the separation (to be checked)
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, Markov Chains and Mixing Times, second edition, 2017
    locator: Chapter 6 (strong stationary times, separation distance, the bound d(t) ≤ s(t) ≤ Pr(τ > t)) (chapter number to be checked)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapter 4 (strong uniform times for random walks on groups) (to be checked)
---

A strong uniform time for a [Markov chain](/markov-chain/) $X_0, X_1, \ldots$ is a random time $T$ such that the state $X_T$ has the uniform law, or more generally the [stationary distribution](/stationary-distribution/) $\pi$, and is independent of $T$. Aldous and Diaconis introduced the idea in 1986 to bound how fast card shuffles mix. The key fact is short: if $T$ is a strong uniform time, then the [total variation distance](/total-variation-distance/) to $\pi$ after $t$ steps is at most $\Pr[T > t]$. So an upper bound on the [mixing time](/mixing-time/) reduces to the tail of one random time, often a [coupon collector](/coupon-collector-problem/) time. Levin and Peres call the same object a strong stationary time.

## In plain words

You shuffle a deck again and again, and you watch for a moment after which you can be sure the deck is perfectly mixed. The rule for spotting that moment may look at the shuffles done so far, but not at future ones. A strong uniform time is such a moment, with one more demand: the deck at that moment must be perfectly mixed no matter when the moment came, early or late.

If such a moment usually comes soon, the deck is close to mixed soon. The chance that the deck is still badly mixed after some number of shuffles is at most the chance that the moment has not come yet. So to show that a shuffle works fast, find a good moment to watch for and show that it seldom comes late.

## The idea

**Definition.** Let $(X_t)$ be a Markov chain on a finite set $\Omega$ with stationary law $\pi$, driven by independent random choices. A *randomized stopping time* is a random time $T$ such that whether $T = t$ depends only on $X_0, \ldots, X_t$, the choices of the first $t$ steps, and maybe extra randomness that the later steps do not use. $T$ is a *strong uniform time* (or strong stationary time) if for every $t$ and every state $y$,
$$\Pr[T = t, X_T = y] = \Pr[T = t] \, \pi(y).$$
In words, $X_T$ has law $\pi$ and is independent of $T$. When $\pi$ is uniform, as for shuffles, the name "uniform" fits exactly.

**The same property at later times.** If $T$ is a strong uniform time, then for all $t$ and $y$,
$$\Pr[T \le t, X_t = y] = \Pr[T \le t] \, \pi(y).$$
*Proof.* Fix $s \le t$. By the strong Markov property, given $T = s$ and $X_s = x$, the state $X_t$ has law $P^{t-s}(x, \cdot)$. So
$$\Pr[T = s, X_t = y] = \sum_x \Pr[T = s, X_s = x] \, P^{t-s}(x, y) = \Pr[T = s] \sum_x \pi(x) P^{t-s}(x, y) = \Pr[T = s] \, \pi(y),$$
because $\pi$ is stationary. Sum over $s \le t$. ∎

**The bound.** Let $d(t) = \max_{x} \|P^t(x, \cdot) - \pi\|_{TV}$ and let $T$ be a strong uniform time for the chain started at $x$, for each $x$. Then
$$d(t) \le \max_x \Pr_x[T > t].$$
*Proof.* For a start $x$ and a set $A$ of states, by the property above,
$$P^t(x, A) \ge \Pr_x[T \le t, X_t \in A] = \Pr_x[T \le t] \, \pi(A).$$
So $\pi(A) - P^t(x, A) \le \pi(A) \Pr_x[T > t] \le \Pr_x[T > t]$. The total variation distance is the largest value of $\pi(A) - P^t(x, A)$ over $A$. ∎

The proof gives more. It shows $P^t(x, y) \ge (1 - \Pr_x[T > t]) \, \pi(y)$ for every single state $y$. The *separation distance* $s(t) = \max_{x, y} (1 - P^t(x, y)/\pi(y))$ is therefore also at most $\max_x \Pr_x[T > t]$, and $d(t) \le s(t)$ always. Aldous and Diaconis showed that some strong uniform time meets this bound with equality, so separation is exactly what strong uniform times measure (1987; to be checked).

**Contrast with coupling.** A [coupling](/coupling-method/) of two copies of the chain bounds $d(t)$ by the tail of the meeting time. A strong uniform time is a one-chain argument, and it bounds the stronger separation distance. Both methods give exact upper bounds; neither gives lower bounds, which need a test set $A$ with $P^t(A)$ far from $\pi(A)$.

**An exact sampler.** Running the chain until $T$ and returning $X_T$ gives an exactly uniform sample. This is a [Las Vegas algorithm](/las-vegas-algorithm/), and the tests of the shuffle pages use it to check the theory.

## Examples

**Top-to-random.** In the [top-to-random shuffle](/top-to-random-shuffle/), let $T$ be one move after the card that started at the bottom first reaches the top. The cards below it are always in a uniform order, so the deck at $T$ is uniform. $T$ is a sum of independent geometric times with success probabilities $1/n, 2/n, \ldots, 1$, so $E[T] = n H_n$ and $\Pr[T > n \ln n + cn] \le e^{-c}$.

**Random transpositions.** In the [random transposition shuffle](/random-transposition-shuffle/), Broder's rule marks the card at the right hand's position when it is unmarked and the left hand's card is marked or is the same card. The time when all cards are marked is a strong uniform time with mean $\frac{2n^2}{n+1} H_n \approx 2 n \ln n$, four times the true mixing time $\frac12 n \ln n$.

**Inverse riffles.** In the inverse of the [Gilbert-Shannon-Reeds](/gilbert-shannon-reeds-model/) riffle, each card gets a fair bit at each shuffle, and the cards are sorted stably by bit. After $k$ inverse shuffles each card has a $k$-bit label, and the deck is sorted by label with ties kept in the first order. Let $T$ be the first $k$ at which all labels are distinct. Given that the labels are distinct, the order is the order of $n$ distinct i.i.d. labels, which is uniform. By the [birthday paradox](/birthday-paradox/) count,
$$\Pr[T > k] = 1 - \prod_{i=1}^{n-1} \left(1 - \frac{i}{2^k}\right).$$
Since the riffle and its inverse have the same distance to uniform, this also bounds riffle shuffles.

| shuffles $k$ | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| $\Pr[T > k]$, $n = 52$ | 0.9962 | 0.9315 | 0.7321 | 0.4795 | 0.2775 | 0.1497 | 0.0778 | 0.0397 |
| exact $d(k)$, $n = 52$ | 0.1672 | 0.0854 | 0.0429 | 0.0215 | 0.0108 | | | |

The exact distances were recomputed with the formula of Bayer and Diaconis (see [Bayer-Diaconis theorem](/bayer-diaconis-theorem/)). The bound needs about $2 \log_2 n$ shuffles, 11 or 12 for 52 cards, while the truth is about $\frac32 \log_2 n$. For $n = 4$ and $k = 1$ to 4 the bound is $1, 0.9062, 0.5898, 0.3335$ and the exact distance is $0.5, 0.2812, 0.1445, 0.0728$.

**The lazy walk on the hypercube.** At each step pick a coordinate of a word of $n$ bits and set it to a fresh fair bit. Once every coordinate has been picked, the word is uniform and independent of when that happened. This is the coupon collector time again, and $d(t) \le n e^{-t/n}$.

**Fisher-Yates.** The [Fisher-Yates shuffle](/fisher-yates-shuffle/) is the extreme case: the deterministic time $T = n - 1$ is a strong uniform time.

**Times that are not strong uniform.**

- In the top-to-random shuffle, the first time the bottom card *reaches* the top is not one: at that time the deck has that card on top for sure. The extra move is needed.
- In random transpositions with two cards, let $T$ be the first move after which both positions have been picked by a hand. If the first move swaps the cards, $T = 1$ and the deck is reversed. A short count gives $\Pr[X_T = \text{start order}] = 1/6$, not $1/2$. "Every card was touched" is not enough.
- A time that looks at the deck and stops when it "looks mixed", for example when no card is in its first place, is never a strong uniform time, because $X_T$ avoids some states.

## Where it is used

- **Upper bounds on mixing times** of card shuffles and random walks on groups: top-to-random, riffles, random transpositions, walks on the hypercube. See [card shuffling](/card-shuffling/).
- **Separation distance**, which strong uniform times measure exactly, and the comparison $d(t) \le s(t)$.
- **Exact sampling** by running a chain to a stopping time, the idea behind the exact versions on the shuffle pages.
- **Teaching.** The top-to-random argument is the standard first proof of a mixing time and of the cutoff phenomenon.

## References
