---
tag: 56XJ14
kind: algorithm
slug: random-transposition-shuffle
name: Random transposition shuffle
aliases:
- random transpositions walk
- random transpositions shuffle
- transpose a random pair
area: randomized/shuffling
level: advanced
summary: Repeatedly swaps two uniformly chosen cards; a random walk on the symmetric group whose mixing time has a cutoff at (1/2) n ln n (Diaconis and Shahshahani 1981).
solves: [card-shuffling]
model: word-ram
complexity:
  vars: {n: the number of cards, t: the number of moves}
  time: {worst: Θ(t), best: Θ(t)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 1981
  people: [Persi Diaconis, Mehrdad Shahshahani]
  note: Diaconis and Shahshahani found the cutoff at (1/2) n log n with Fourier analysis on the symmetric group, the first sharp mixing result for a card shuffle.
prereqs: [markov-chain, total-variation-distance, symmetric-group, permutation-cycles]
see_also: [card-shuffling, top-to-random-shuffle, strong-uniform-time, mixing-time, fisher-yates-shuffle, coupon-collector-problem, chebyshev-inequality, gilbert-shannon-reeds-model]
sources:
  - paper: "Persi Diaconis and Mehrdad Shahshahani, Generating a random permutation with random transpositions, Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete 57, 1981"
    locator: pp. 159 to 179; the main theorem (upper bound a e^(−2c) at (1/2) n log n + cn and the lower bound) (theorem number to be checked)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapter 3D (random transpositions, with the Fourier proof) and Chapter 4 (Broder's strong uniform time) (to be checked)
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, Markov Chains and Mixing Times, second edition, 2017
    locator: Chapter 8 (random transpositions, Broder's stopping time, the lower bound by fixed points) (chapter number to be checked)
  - paper: "Peter Matthews, A strong uniform time for random transpositions, Journal of Theoretical Probability 1, 1988"
    locator: pp. 411 to 423 (to be checked)
---

The random transposition shuffle is a [Markov chain](/markov-chain/) on the orders of a deck of $n$ cards. At each move it picks two positions $L$ and $R$, independent and uniform on the $n$ positions, and swaps the two cards there. With probability $1/n$ the two positions are the same and the deck does not change. The chain is the random walk on the [symmetric group](/symmetric-group/) driven by the uniform law on transpositions and the identity. Diaconis and Shahshahani proved in 1981 that it needs $\frac12 n \ln n$ moves to get close to uniform, and that the [total variation distance](/total-variation-distance/) drops from near 1 to near 0 in a window of order $n$ around that point. For 52 cards that is about 103 moves. It is the second classic example of the cutoff phenomenon, next to the [top-to-random shuffle](/top-to-random-shuffle/), and the first one proved with representation theory.

## In plain words

Lay the cards in a row. Pick a random card with your right hand and a random card with your left hand, and swap them. Sometimes both hands pick the same card, and nothing happens. Repeat.

A card that no hand has touched is still in its first place. So the deck cannot be mixed before almost every card has been touched at least once. Each move touches two cards, and touching every card is a collecting problem, like collecting all the stickers of a set. That gives the right number of moves, about half the number of cards times its natural logarithm, which is about 100 swaps for a deck of 52 cards. The hard part, proved with tools from group theory, is that this number is also enough.

## The problem

The input is a deck $A[0 \ldots n-1]$ and a number of moves $t$. The output is the deck after $t$ moves. The question is the [card shuffling](/card-shuffling/) question: how large must $t$ be for the law $P^t$ of the deck to be within $\varepsilon$ of the uniform law $\pi$ in total variation? Let $d(t) = \|P^t - \pi\|_{TV}$; by symmetry it does not depend on the start.

## The algorithm

```pseudo id=main
RANDOM-TRANSPOSITIONS(A, t)                ▷ A[0 .. n − 1]
L1  for s ← 1 to t do
L2      L ← RANDOM(0, n − 1)
L3      R ← RANDOM(0, n − 1)               ▷ independent of L; L = R with probability 1/n
L4      exchange A[L] and A[R]
```

**The exact version (Broder).** Mark cards as follows. At a move, mark the card at position $R$ if it is not marked yet and either the card at position $L$ is marked or $L = R$. Stop at the move $T$ that marks the last card. The deck at time $T$ is exactly uniform, so $T$ is a [strong uniform time](/strong-uniform-time/). With $k$ cards marked, a move marks a new card with probability $(n-k)(k+1)/n^2$, so
$$E[T] = \sum_{k=0}^{n-1} \frac{n^2}{(n-k)(k+1)} = \frac{2 n^2}{n+1} H_n \approx 2 n \ln n.$$
This rule is in the Python file, and the tests check its exact uniformity for $n \le 4$.

## Example

Four cards $a\,b\,c\,d$. Suppose the calls in lines L2 and L3 return $(0, 3)$, $(1, 1)$, $(2, 0)$.

| move | $L$ | $R$ | deck after |
|---|---|---|---|
| start | | | a b c d |
| 1 | 0 | 3 | d b c a |
| 2 | 1 | 1 | d b c a |
| 3 | 2 | 0 | c b d a |

Card $b$ was never touched, so it is still at position 1, a fixed point.

**Exact distances.** The law of the deck is constant on each cycle type, so the distance to uniform can be computed from the law of the cycle type, a Markov chain on the partitions of $n$. The Python file does this and checks it against brute force over all $n!$ orders for $n \le 5$. The values, rounded:

| $n$ | $\frac12 n \ln n$ | $d(t)$ at the listed $t$ |
|---|---|---|
| 4 | 2.8 | $t = 1$ to 4: $17/24 \approx 0.708$, $9/32 \approx 0.281$, $65/384 \approx 0.169$, $39/512 \approx 0.076$ |
| 10 | 11.5 | $t = 4, 8, 12, 16, 20, 24$: 0.9797, 0.5078, 0.2275, 0.0949, 0.0397, 0.0164 |
| 20 | 30.0 | $t = 12, 20, 28, 36, 44, 52, 60$: 0.9935, 0.6487, 0.3420, 0.1557, 0.0678, 0.0295, 0.0128 |

For $n = 20$ the distance is about $1/2$ near $t = 22$ and falls below $0.03$ by $t = 52$, consistent with a cutoff at $\frac12 n \ln n \approx 30$ and a window of order $n$.

## Correctness

The chain makes no claim of exactness at a fixed $t$; the results are about $d(t)$.

**Uniform is stationary and the chain converges.** Each move applies a transposition or the identity, a bijection of the orders, so the uniform law is stationary. Transpositions generate the symmetric group, and the identity has probability $1/n > 0$, so the chain is irreducible and aperiodic and $d(t) \to 0$.

**Theorem (Diaconis and Shahshahani 1981).** There is a constant $a$ such that for $c > 0$ and $t \ge \frac12 n \ln n + cn$,
$$d(t) \le a e^{-2c}.$$
The proof uses the Fourier transform on the symmetric group: the step law is constant on conjugacy classes, so its Fourier transform at each irreducible representation $\rho$ is a scalar, $\frac1n + \frac{n-1}{n} r(\rho)$, where $r(\rho)$ is the character ratio at a transposition. The bound comes from the upper bound lemma $4\,d(t)^2 \le \sum_{\rho \ne 1} d_\rho^2 \, |\hat Q(\rho)|^{2t}$ and estimates of the character ratios. This page does not reproduce that proof.

**Lower bound.** For $c > 0$ and $t \le \frac{n-1}{2} \ln n - c(n-1)$,
$$d(t) \ge 1 - 6 e^{-2c}.$$
A position that neither hand has picked holds its first card. The expected number of such positions is at least $e^{2c}$, and they are spread enough that Chebyshev's inequality shows the deck has at least $e^{2c}/2$ fixed points with high probability, while a uniform deck has on average one fixed point. Together with the upper bound, this gives a cutoff at $\frac12 n \ln n$ with a window of order $n$.

**Broder's time is a strong uniform time.** Given the history of which positions hold marked cards, the matching of marked cards to those positions is uniform. A new mark with $L = R$ or $L$ marked is a step of the Fisher-Yates kind: the new card goes to a uniform one of the $k + 1$ positions. All proofs except the Fourier bound are in the proof file.

## Complexity

Each move is $\Theta(1)$ time, so $t$ moves are $\Theta(t)$ time and $\Theta(1)$ extra space. To be close to uniform the chain needs about $\frac12 n \ln n$ moves, which is $\Theta(n \log n)$ time and $n \log_2 n$ random integers: much more than the $n - 1$ calls of [Fisher-Yates](/fisher-yates-shuffle/), which is exact. Broder's exact version takes about $2 n \ln n$ moves on average, 463 for 52 cards.

## Properties

- **Symmetric.** Each move is its own inverse, so the chain is reversible and its transition matrix is symmetric.
- **Constant on cycle types.** The law after $t$ moves is a class function on the symmetric group, so only the law of the cycle type matters.
- **Never exactly uniform at a fixed time** for $n \ge 3$: all probabilities are multiples of $n^{-2t}$, and $n!$ does not divide $n^{2t}$.
- **Laziness is needed.** The identity move, from $L = R$, breaks the parity: see the pitfalls.

## Variants and improvements

- **Distinct pairs.** Choose $L \ne R$ uniformly among the $\binom n2$ pairs. The chain is then periodic (see the pitfalls). Adding a lazy step with probability $1/n$ gives back the chain on this page.
- **Transpose with the top card, or adjacent transpositions.** Swapping only with the top card mixes in about $n \ln n$ moves (to be checked); swapping only adjacent cards is much slower, of order $n^3 \log n$ moves (Wilson 2004; to be checked). See [card shuffling](/card-shuffling/).
- **Fisher-Yates as a fixed schedule.** If the move at step $s$ swaps position $n - s$ with a uniform position at most $n - s$, then $n - 1$ moves give an exactly uniform deck. This is [Fisher-Yates](/fisher-yates-shuffle/): the randomness is used where it is needed, not spread over all positions.

## When to use it

Use it as the model example for Fourier analysis on groups and for the coupon-collector lower bound. It also models a person who mixes cards by swapping random pairs, a physical process such as random exchanges between particles, and the random-swap step of some Monte Carlo methods. Do not use it to shuffle data.

## Pitfalls

- **Forcing $L \ne R$.** Then every move is an odd permutation, the parity of the deck after $t$ moves is the parity of $t$, and $d(t) \ge \frac12$ for all $t$. The test file checks this for $n = 3$.
- **Too few moves.** About $n$ swaps feel like a lot, but after $n$ moves about $n e^{-2} \approx 0.14 n$ positions are never touched, and the deck is far from uniform. For 52 cards, about 103 moves is the cutoff point, and more are needed for a small distance.
- **Reading Broder's mean $2 n \ln n$ as the mixing time.** It is an upper bound that is off by a factor of 4; the cutoff is at $\frac12 n \ln n$.

## Implementations

## History

Diaconis and Shahshahani published the result in 1981, with a proof by the representation theory of the symmetric group. It was the first card shuffle with a sharp mixing time, and it showed the cutoff phenomenon. Broder found a strong uniform time with mean about $2 n \ln n$, described in Diaconis's 1988 book. Matthews gave in 1988 a strong uniform time that reaches the sharp constant $\frac12$ (to be checked).

## References
