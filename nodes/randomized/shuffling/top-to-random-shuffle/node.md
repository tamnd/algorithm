---
tag: 8HFMHV
kind: algorithm
slug: top-to-random-shuffle
name: Top-to-random shuffle
aliases:
- random insertion shuffle
- top-in-at-random shuffle
area: randomized/shuffling
level: core
summary: The card-shuffling chain that moves the top card to a uniformly random place. It has a simple strong uniform time with mean n H_n, and its mixing time has a cutoff at n ln n (Aldous, Diaconis 1986).
solves: [card-shuffling]
model: word-ram
complexity:
  vars: {n: the number of cards, t: the number of moves}
  time: {worst: O(t·n), best: O(t)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 1986
  people: [David Aldous, Persi Diaconis]
  note: Aldous and Diaconis used this shuffle in 1986 as the first example of a strong uniform time and of the cutoff phenomenon.
prereqs: [markov-chain, total-variation-distance, coupon-collector-problem]
see_also: [strong-uniform-time, card-shuffling, mixing-time, random-transposition-shuffle, gilbert-shannon-reeds-model, bayer-diaconis-theorem, fisher-yates-shuffle, chebyshev-inequality]
sources:
  - paper: "David Aldous and Persi Diaconis, Shuffling cards and stopping times, American Mathematical Monthly 93(5), 1986"
    locator: pp. 333 to 348; Section 1 (the top-in-at-random shuffle, the stopping time and the bound n log n + cn) and the lower bound argument
  - paper: "David Aldous and Persi Diaconis, Strong uniform times and finite random walks, Advances in Applied Mathematics 8(1), 1987"
    locator: pp. 69 to 97 (strong uniform times in general)
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, Markov Chains and Mixing Times, second edition, 2017
    locator: Chapter 6 (strong stationary times, with the top-to-random shuffle as the first example) and Chapter 7 (the lower bound) (chapter numbers to be checked)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapter 4 (random walks on groups and the top-in-at-random shuffle) (to be checked)
---

The top-to-random shuffle is a [Markov chain](/markov-chain/) on the orders of a deck of $n$ cards. At each move it takes the top card and puts it back at one of the $n$ places in the deck, chosen uniformly: on top, between two cards, or at the bottom. It is a model of a slow, simple shuffle. It does not give a uniform deck after any fixed number of moves, but it gets close. Aldous and Diaconis showed in 1986 that about $n \ln n$ moves are necessary and sufficient: the [total variation distance](/total-variation-distance/) to uniform drops from near 1 to near 0 in a window of order $n$ around $n \ln n$, the cutoff phenomenon. The proof uses a [strong uniform time](/strong-uniform-time/): one move after the card that started at the bottom reaches the top, the deck is exactly uniform. That time has mean $n H_n$, about 236 moves for 52 cards.

## In plain words

Take the top card of a deck and push it into the deck at a random place, any place with the same chance, including the top and the bottom. Do this again and again. How many times until the deck is well mixed?

Watch the card that started at the bottom. Cards pushed in below it end up in a random order, because each goes to a random place among the cards already there. This card rises as more cards go under it. When it reaches the top, every other card is under it in a random order. Push it in once more at a random place, and the whole deck is perfectly random.

The card rises slowly at first, since a card rarely lands at the very bottom. The wait is like collecting all the stickers of a set.

## The problem

The input is a deck $A[0 \ldots n-1]$, with $A[0]$ the top card, and a number of moves $t$. The output is the deck after $t$ moves. The question is the [card shuffling](/card-shuffling/) question: for which $t$ is the law of the deck within $\varepsilon$ of the uniform distribution in total variation? Let $P^t$ be the law after $t$ moves from a fixed start and $\pi$ the uniform law on the $n!$ orders. The distance is $d(t) = \max_A \|P^t - \pi\|_{TV}$, and the [mixing time](/mixing-time/) is $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$.

## The algorithm

```pseudo id=main
TOP-TO-RANDOM(A, t)                        ▷ A[0 .. n − 1]; A[0] is the top card
L1  for s ← 1 to t do
L2      x ← A[0]; remove A[0] from the deck
L3      p ← RANDOM(0, n − 1)               ▷ n places: 0 is the top, n − 1 the bottom
L4      insert x at position p
```

Each move is one of $n$ permutations, the cycles that move the top card down by $p$ places, each with probability $1/n$. The inverse move, which takes a uniform random card and puts it on top, is the Tsetlin library or random-to-top chain; it has the same distance to uniform after $t$ moves, because the inverse of a uniform permutation is uniform.

**The exact version.** Stop at the first move in which the card that started at the bottom is the card $x$ of line L2. The deck is then exactly uniform. This is a correct Las Vegas shuffle with an expected $n H_n$ moves, much slower than [Fisher-Yates](/fisher-yates-shuffle/), and it is in the Python file to test the theory.

## Example

Four cards $a\,b\,c\,d$, with $d$ at the bottom. Suppose line L3 returns $3, 2, 1, 2$.

| move | card moved | place $p$ | deck after | cards below $d$ |
|---|---|---|---|---|
| start | | | a b c d | 0 |
| 1 | $a$ | 3 | b c d a | 1 |
| 2 | $b$ | 2 | c d b a | 2 |
| 3 | $c$ | 1 | d c b a | 3 |
| 4 | $d$ | 2 | c b d a | |

After move 3 the card $d$ is on top, and the three cards below it are in an order that was uniform on the $3!$ orders. Move 4 inserts $d$ at a uniform place, so the deck after move 4 is uniform on all $4!$ orders, and $T = 4$ here.

**Exact distances.** The exact law of the deck after $t$ moves from $a\,b\,c\,d\ldots$ was computed with exact fractions over all $n!$ orders. The table gives $d(t)$ and the bound $\Pr[T > t]$, rounded.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| $n = 4$: $d(t)$ | 0.8333 | 0.5 | 0.3125 | 0.1719 | 0.0898 | 0.0459 | 0.0232 | 0.0117 | 0.0029 | 0.0007 |
| $n = 4$: $\Pr[T > t]$ | 1 | 1 | 1 | 0.9062 | 0.7656 | 0.6191 | 0.4873 | 0.3771 | 0.2194 | 0.1252 |
| $n = 6$: $d(t)$ | 0.9917 | 0.9583 | 0.8333 | 0.6481 | 0.4537 | 0.3765 | 0.2930 | 0.2179 | 0.1109 | 0.0530 |
| $n = 6$: $\Pr[T > t]$ | 1 | 1 | 1 | 1 | 1 | 0.9846 | 0.9460 | 0.8860 | 0.7282 | 0.5622 |

The bound holds, as it must, and it is far from tight for small $n$.

## Correctness

The chain does not claim exactness at a fixed $t$; it claims convergence to uniform with a rate. The results are these.

**Uniform is stationary.** Each move applies one of $n$ fixed permutations, so it maps the uniform law to the uniform law. The chain is irreducible and aperiodic for $n \ge 2$ (the move $p = 0$ does nothing), so $P^t \to \pi$.

**A strong uniform time.** Let $b$ be the card at the bottom at the start, and let $T$ be the first move in which $b$ is the card taken from the top. Then for each $t$ and each order $\sigma$, $\Pr[X_t = \sigma, T \le t] = \Pr[T \le t] / n!$. The reason: at each moment, the cards below $b$ are in a uniform order given their set, since each card enters that part at a uniform place among the cards already there. When $b$ is on top, all other cards are below it in a uniform order, and move $T$ puts $b$ at a uniform place.

**The bound.** $d(t) \le \Pr[T > t]$ for every strong uniform time (see [strong uniform time](/strong-uniform-time/)). Here $T = \sum_{i=1}^{n} G_i$ with independent $G_i$ geometric with success probability $i/n$: with $k$ cards below $b$, the moved card lands below $b$ with probability $(k+1)/n$. This is the law of the [coupon collector](/coupon-collector-problem/) time, so $E[T] = n H_n$ and
$$\Pr[T > n \ln n + cn] \le e^{-c}.$$

**Theorem (Aldous and Diaconis 1986).** For $c \ge 0$ and $n \ge 2$, $d(n \ln n + cn) \le e^{-c}$. For $c > 0$ and $t = n \ln n - cn$, $d(t) \ge 1 - 1/j! - 4/((j-1)c^2)$ with $j = \lfloor e^{c/2} \rfloor \ge 2$. So $d(n \ln n - c_n n) \to 1$ when $c_n \to \infty$: the chain has a cutoff at $n \ln n$ with window $O(n)$.

The lower bound watches the bottom $j$ cards. They stay in their first relative order until the highest of them reaches the top, which takes about $n \ln(n/j)$ moves, while a uniform deck has them in that order with probability only $1/j!$. The proofs are in the proof file.

## Complexity

Each move is $O(n)$ time on an array, because of the removal and the insertion, and $O(\log n)$ with a balanced tree with sizes. To get within a small distance of uniform the chain needs about $n \ln n$ moves, so $\Theta(n^2 \log n)$ time on an array. As a way to shuffle data this is far worse than [Fisher-Yates](/fisher-yates-shuffle/), which is exact in $\Theta(n)$ time. The chain is studied as a model, not used as an algorithm.

For $n = 52$: $n \ln n \approx 205.5$, $E[T] = 52 H_{52} \approx 236.0$, and the exact tail of $T$ gives $\Pr[T > 258] \approx 0.30$ and $\Pr[T > 362] \approx 0.046$ (computed by the recurrence for $T$), close to the bounds $e^{-1} \approx 0.37$ and $e^{-3} \approx 0.05$.

## Properties

- **Never exactly uniform at a fixed time** for $n \ge 3$: all probabilities after $t$ moves have the denominator $n^t$, and $n!$ does not divide $n^t$ for $n \ge 3$.
- **Cutoff.** The distance falls from near 1 to near 0 between $n \ln n - cn$ and $n \ln n + cn$ moves.
- **Lazy.** The move $p = 0$ leaves the deck unchanged.
- **Same mixing as its inverse.** The random-to-top chain (the Tsetlin library with uniform weights) has the same $d(t)$.

## Variants and improvements

- **Random-to-top and random-to-random.** Random-to-top moves a uniform card to the top; random-to-random moves a uniform card to a uniform place, with a cutoff at $\frac34 n \ln n$ (Bernstein and Nestoridi, 2019; to be checked).
- **Top-$k$ to random.** Insert several top cards at once.
- **Inverse riffle view.** The top-to-random chain and the riffle shuffle both have strong uniform times built from "cards in uniform relative order"; see [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/).

## When to use it

Use it as the first example of mixing-time analysis: the strong uniform time is short and complete, and the lower bound needs only [Chebyshev's inequality](/chebyshev-inequality/). It also models a real "insert a card at random" shuffle and the move-to-front heuristic of self-organizing lists. Do not use it to shuffle data.

## Pitfalls

- **Inserting only between cards.** If the card can go only to the $n - 1$ places below the top, the chain loses its lazy step and the bookkeeping changes. The analysis above needs all $n$ places.
- **Stopping too early.** The exact version must stop *after* the original bottom card is moved, not when it reaches the top.
- **Reading $n H_n$ as the mixing time.** $E[T] = n H_n$ is an upper-bound tool; the cutoff is at $n \ln n$, and $n H_n - n \ln n \approx 0.577 n$ is inside the window.

## Implementations

## History

Aldous and Diaconis introduced strong uniform times in their 1986 paper "Shuffling cards and stopping times", with the top-in-at-random shuffle as the first example, and they described the cutoff phenomenon. They developed the general theory in 1987. The shuffle is also treated in the book of Levin and Peres.

## References
