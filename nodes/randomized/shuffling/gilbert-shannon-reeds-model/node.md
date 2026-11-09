---
tag: WYX8N8
kind: model
slug: gilbert-shannon-reeds-model
name: Gilbert-Shannon-Reeds model
aliases:
- riffle shuffle model
- dovetail shuffle model
- GSR model
- GSR shuffle
area: randomized/shuffling
level: advanced
summary: The standard model of a riffle shuffle. Cut the deck binomially, then interleave the two packets uniformly. After k shuffles a deck with r rising sequences has probability C(2^k + n − r, n)/2^(kn).
prereqs: [markov-chain, total-variation-distance, binomial-distribution, permutation]
see_also: [bayer-diaconis-theorem, card-shuffling, strong-uniform-time, faro-shuffle, eulerian-numbers, top-to-random-shuffle, overhand-shuffle-model, shuffling-a-linked-list]
sources:
  - paper: "Dave Bayer and Persi Diaconis, Trailing the dovetail shuffle to its lair, Annals of Applied Probability 2(2), 1992"
    locator: pp. 294 to 313; the equivalent descriptions of an a-shuffle, the composition rule, and the formula for the probability of a permutation with r rising sequences (theorem numbers to be checked)
  - paper: "E. N. Gilbert, Theory of shuffling, technical memorandum, Bell Laboratories, 1955"
    locator: the model of the riffle shuffle (unpublished memorandum; locator to be checked)
  - paper: "Jim Reeds, unpublished manuscript on riffle shuffles, 1981"
    locator: the inverse shuffle and the bound of about 2 log2 n shuffles (cited by Diaconis 1988 and Bayer-Diaconis 1992; to be checked)
  - paper: "David Aldous and Persi Diaconis, Shuffling cards and stopping times, American Mathematical Monthly 93(5), 1986"
    locator: pp. 333 to 348; the riffle shuffle and the strong uniform time from the inverse shuffle (section to be checked)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapter 4 (the riffle shuffle and its fit to real shuffles) (to be checked)
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, Markov Chains and Mixing Times, second edition, 2017
    locator: Section 8.3 (riffle shuffles and the inverse shuffle) (section number to be checked)
---

The Gilbert-Shannon-Reeds model, or GSR model, is the standard probability model of a riffle shuffle, the shuffle in which a person cuts a deck into two packets and lets the cards drop from both thumbs so that the packets interleave. In the model the cut has the [binomial](/binomial-distribution/) law with parameters $n$ and $\frac12$, and the cards drop one at a time, each from a packet with probability proportional to the number of cards left in it. That makes every interleaving of the two packets equally likely. Gilbert and Shannon proposed the model in 1955 and Reeds studied it in 1981. It is the setting of the [Bayer-Diaconis theorem](/bayer-diaconis-theorem/): the law after $k$ shuffles has a closed form in terms of the rising sequences of the deck, and about $\frac32 \log_2 n$ shuffles, 7 for 52 cards, are needed to make the deck close to uniform.

## The machine

The state is an order of a deck of $n$ cards, written as a list with the top card first. One GSR shuffle is the following random step.

```pseudo id=main
GSR-SHUFFLE(A)                             ▷ A[0 .. n − 1]; A[0] is the top card
L1  k ← the number of heads in n fair coin flips   ▷ the cut is Binomial(n, 1/2)
L2  P ← A[0 .. k − 1]; Q ← A[k .. n − 1]; B ← an empty list
L3  while P and Q are both non-empty do
L4      if RANDOM(0, |P| + |Q| − 1) < |P| then move the top card of P to the bottom of B
L5      else move the top card of Q to the bottom of B
L6  put the rest of P, then the rest of Q, at the bottom of B; return B
```

Lines L3 to L5 build the new deck from the top. The physical description drops cards from the bottoms of the packets with the same proportional rule; both give each of the $\binom nk$ interleavings with probability $1 / \binom nk$, by the product argument on the [linked list](/shuffling-a-linked-list/) page.

**Four equivalent descriptions.** Each of them gives the same law on orders.

1. **Cut and interleave.** As above: a binomial cut, then a uniform interleaving. Each pair (cut $k$, interleaving) has probability $\binom nk 2^{-n} \cdot \binom nk^{-1} = 2^{-n}$.
2. **Sequences of packet labels.** Pick $w \in \{0, 1\}^n$ uniformly. Packet 0 is the top $k$ cards, where $k$ is the number of zeros in $w$. Position $p$ of the new deck gets the next card of packet $w_p$. Each of the $2^n$ sequences has probability $2^{-n}$, and it gives exactly the pair (cut, interleaving) of description 1.
3. **The inverse shuffle.** Give each card a fair bit and move the cards with bit 0 to the top, keeping their order, with the cards with bit 1 below them in their order. This step has the law of the *inverse* of a GSR shuffle. It is the reverse of description 2: the bit of a card is the packet it came from.
4. **The doubling map.** Put $n$ independent uniform points in $[0, 1)$ in increasing order, and label them as the deck. Apply $x \mapsto 2x \bmod 1$. The new order of the labels is a GSR shuffle of the old one: the points in $[0, \frac12)$ form the top packet, and the doubled points interleave uniformly.

**The $a$-shuffle.** Description 2 with $w \in \{0, \ldots, a-1\}^n$ uniform is an $a$-shuffle: cut into $a$ packets with multinomial sizes and interleave uniformly. A GSR shuffle is a 2-shuffle. Description 4 with $x \mapsto ax \bmod 1$ is the same $a$-shuffle.

## What it counts

The model counts **shuffles**: the number $k$ of GSR steps from a fixed start order. The quality of the deck after $k$ shuffles is measured by the [total variation distance](/total-variation-distance/) $d(k) = \|P^k - \pi\|_{TV}$ to the uniform law $\pi$ on the $n!$ orders. A second measure is the separation $s(k) = 1 - n! \min_\sigma P^k(\sigma)$, which is at least $d(k)$. Other measures appear in the literature, for example the entropy and the success of a guessing game, and they give different numbers of shuffles; see [card shuffling](/card-shuffling/).

The step is the same at every shuffle and does not depend on the state, so the model is a random walk on the [symmetric group](/symmetric-group/), a [Markov chain](/markov-chain/) whose law after $k$ steps is the $k$-fold convolution of the one-step law. The time to perform a shuffle is not counted.

## Relation to other models

- **The [faro shuffle](/faro-shuffle/)** is a perfect riffle: an exact half cut and strict alternation. It is one of the $2^n$ outcomes of description 2, and it is deterministic, so it never mixes: 8 perfect out-shuffles restore a 52-card deck. Expert riffles are closer to faros than amateur ones, and the GSR model fits amateur shuffles better (Diaconis 1988; to be checked).
- **The [top-to-random shuffle](/top-to-random-shuffle/)** is a riffle with a cut of exactly one card: the top card is interleaved with the rest at a uniform place. It needs about $n \ln n$ steps, against about $\frac32 \log_2 n$ for GSR, because a GSR shuffle moves about half the deck at once.
- **The [overhand shuffle model](/overhand-shuffle-model/)** moves packets but never interleaves, and it needs order $n^2 \log n$ steps.
- **The [random transposition shuffle](/random-transposition-shuffle/)** needs $\frac12 n \ln n$ steps.
- **Stable sorting by random keys.** $k$ inverse GSR shuffles sort the deck stably by $k$-bit random labels, the most recent bit first. With $k = \infty$ this is [permute by sorting](/permute-by-sorting/) with infinite random keys, and with recursion it is the split method of the [linked list](/shuffling-a-linked-list/) page.
- **[Strong uniform times](/strong-uniform-time/).** The time at which all labels become distinct is a strong uniform time for the inverse walk.

## Known results in the model

**One shuffle.** A GSR shuffle of the order $0, 1, \ldots, n-1$ gives an order with at most two *rising sequences*. A rising sequence is a maximal run of consecutive card values $v, v+1, \ldots, w$ that appear in increasing positions. The identity has probability $(n+1)/2^n$, since each of the $n + 1$ cuts can interleave back to it, and each of the other $2^n - n - 1$ orders with exactly two rising sequences has probability $2^{-n}$. For 52 cards, the deck stays in order with probability $53 / 2^{52} \approx 1.2 \times 10^{-14}$, and one shuffle can reach only $2^{52} - 52$ of the $52!$ orders.

**Composition (Bayer and Diaconis 1992).** An $a$-shuffle followed by a $b$-shuffle has the law of an $ab$-shuffle. In the inverse form this is clear: an inverse $a$-shuffle sorts the cards stably by uniform labels in $\{0, \ldots, a-1\}$, and an inverse $b$-shuffle after it sorts stably by new labels; the result is a stable sort by the pair (new label, old label), which is a uniform label in $\{0, \ldots, ab - 1\}$. So $k$ GSR shuffles are one $2^k$-shuffle.

**The formula (Bayer and Diaconis 1992).** An $a$-shuffle of the deck $0, \ldots, n-1$ gives a fixed order $\sigma$ with $r$ rising sequences with probability
$$P_a(\sigma) = \binom{a + n - r}{n} \Big/ a^n.$$
*Proof.* In description 2, the sequence $w$ fixes packets that are consecutive blocks of the start order, split at $a - 1$ cut points $0 \le c_1 \le \cdots \le c_{a-1} \le n$. Each block appears in $\sigma$ in increasing positions, so $\sigma$ arises from $w$ exactly when the cut points include the $r - 1$ places where one rising sequence of $\sigma$ ends. Given the cut points, $w$ is fixed by $\sigma$. The other $a - r$ cut points form a multiset of the $n + 1$ places, and there are $\binom{n + a - r}{a - r} = \binom{a + n - r}{n}$ such multisets. Each $w$ has probability $a^{-n}$. ∎

The number of orders with $r$ rising sequences is the [Eulerian number](/eulerian-numbers/) $A(n, r)$: $\sigma$ has $r$ rising sequences exactly when its inverse has $r - 1$ [descents](/descents/). So
$$d(k) = \frac12 \sum_{r=1}^{n} A(n, r) \left| \binom{2^k + n - r}{n} 2^{-kn} - \frac{1}{n!} \right|,$$
a sum of $n$ terms instead of $n!$. For $n = 4$ the counts are $1, 11, 11, 1$.

**Exact values, recomputed.** The values below were recomputed with exact rational arithmetic from the formula. The Python file checks the formula against brute force, by composing the one-shuffle law over all $n!$ orders, for $n \le 6$ and $k \le 4$ ($k \le 3$ for $n = 6$).

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $n = 52$ | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9237 | 0.6135 | 0.3341 | 0.1672 | 0.0854 | 0.0429 | 0.0215 | 0.0108 |

The first four values are 1 to six decimal places. Small decks: for $n = 3$, $d = 0.3333, 0.1458, 0.0677, 0.0326$ at $k = 1$ to 4; for $n = 4$, $0.5, 0.2812, 0.1445, 0.0728$; for $n = 5$, $0.775, 0.3629, 0.1657, 0.0781$. Each extra shuffle roughly halves the distance once it is below about $\frac12$.

**Separation and the inverse shuffle.** The least likely order is the reversal, with $r = n$, so
$$s(k) = 1 - n! \binom{2^k}{n} 2^{-kn} = 1 - \prod_{i=1}^{n-1} \left(1 - \frac{i}{2^k}\right).$$
This equals $\Pr[T > k]$ for the strong uniform time "all $k$-bit labels are distinct" of the inverse shuffle, so that time is optimal for separation. For 52 cards $s(k)$ is $0.9962, 0.9315, 0.7321, 0.4795, 0.2775$ at $k = 8$ to 12. It needs about $2 \log_2 n$ shuffles, 11 or 12 for 52 cards, while $d(k)$ needs about $\frac32 \log_2 n$.

**The cutoff.** $d(k)$ has a cutoff at $\frac32 \log_2 n$ shuffles with a window of constant width; see the [Bayer-Diaconis theorem](/bayer-diaconis-theorem/).

**A lower bound by counting.** After $k$ shuffles the deck has at most $2^k$ rising sequences, while a uniform deck has about $n/2$. So $d(k)$ is near 1 while $2^k$ is much smaller than $n/2$, that is, for $k < \log_2 n - 1$. The sharp lower bound at $\frac32 \log_2 n$ needs the finer count of rising sequences in the theorem.

## References
