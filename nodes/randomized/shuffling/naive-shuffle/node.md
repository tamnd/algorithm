---
tag: T33CXF
kind: concept
slug: naive-shuffle
name: Naive (biased) shuffle
aliases:
- incorrect shuffle
- sort-by-random-with-wrong-range
- exchange shuffle
- PERMUTE-WITH-ALL
area: randomized/shuffling
level: intro
summary: The common wrong shuffle that swaps each position with a uniform position of the whole array. It has n^n equally likely runs, so for n ≥ 3 it cannot give each of the n! orders with probability 1/n!.
prereqs: [random-permutation, fisher-yates-shuffle]
see_also: [sattolo-algorithm, sort-based-shuffle, permute-by-sorting, modulo-bias, random-transposition-shuffle, card-shuffling]
sources:
  - paper: "David P. Robbins and Ethan D. Bolker, The bias of three pseudo-random shuffles, Aequationes Mathematicae 22 (1981)"
    locator: pp. 268 to 292 (the shuffle that exchanges the card at each position with a card at a random position)
  - paper: "Daniel Goldstein and David Moews, The identity is the most likely exchange shuffle for large n, Aequationes Mathematicae 65 (2003), arXiv:math/0010066"
    locator: pp. 3 to 30; the abstract and the main theorem (the identity is the most likely output for n of 18 or more)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 5.3, exercises (the procedure PERMUTE-WITH-ALL, which swaps A[i] with a random element of the whole array)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Algorithm P (the correct shuffle that the naive one tries to be)
---

The naive shuffle is the common wrong way to shuffle an array: for each position $i$, swap $A[i]$ with $A[j]$ for a $j$ that is uniform on the *whole* array. It looks like the [Fisher-Yates shuffle](/fisher-yates-shuffle/), and it differs in one range. It has $n^n$ equally likely runs, and $n^n$ is not a multiple of $n!$ for $n \ge 3$, so it cannot give a uniform [random permutation](/random-permutation/). For three items it gives the six orders with probabilities $4/27$, $5/27$, $5/27$, $5/27$, $4/27$ and $4/27$.

## In plain words

To shuffle a row of cards, a programmer goes along the row and swaps each card with a card at a random place in the whole row. This feels fair, because every swap is random. It is not fair.

Count the ways the method can run. Each card picks one of all the places, so the number of runs is the number of cards, multiplied by itself once for each card. The number of orders of the cards is a different number, and the first number cannot be split into equal shares for all orders. So some orders must come out more often than others. With three cards there are twenty-seven runs and six orders, and twenty-seven does not split into six equal parts.

The fix is small: at each step, pick only from the cards that are not yet placed. That is the Fisher-Yates shuffle.

## The idea

```pseudo id=main
NAIVE-SHUFFLE(A)                           ▷ A[0 .. n − 1]; this is WRONG
L1  for i ← 0 to n − 1 do
L2      j ← RANDOM(0, n − 1)               ▷ the correct range is RANDOM(i, n − 1)
L3      exchange A[i] and A[j]
```

Here RANDOM$(a, b)$ is uniform on $\{a, \ldots, b\}$, and the calls are independent. A run is fixed by its choice sequence $(j_0, \ldots, j_{n-1}) \in \{0, \ldots, n-1\}^n$, and each of the $n^n$ sequences has probability $n^{-n}$. So each output order $\tau$ has probability $c_\tau / n^n$, where $c_\tau$ is the number of choice sequences that give $\tau$.

**Theorem.** For $n \ge 3$, NAIVE-SHUFFLE does not give each of the $n!$ orders with probability $1/n!$. For $n \le 2$ it does.

*Proof.* If each order had probability $1/n!$, then $c_\tau = n^n / n!$ for each $\tau$, and this must be an integer. So $n!$ must divide $n^n$. Let $n \ge 3$. Then $n - 1 \ge 2$ divides $n!$. But $\gcd(n-1, n) = 1$, so $n - 1$ has a prime factor $p$ that does not divide $n$, and $p$ does not divide $n^n$. So $n!$ does not divide $n^n$, and the distribution is not uniform. For $n = 1$ the one run gives the one order. For $n = 2$ the four choice sequences $00, 01, 10, 11$ give the orders $[1,0], [0,1], [0,1], [1,0]$, two each. $\square$

The same count proves more. Any procedure whose runs are fixed by a bounded number of choices, with $m_1, m_2, \ldots$ values each, is uniform only if $n!$ divides the product $m_1 m_2 \cdots$. Fisher-Yates has the product $n \cdot (n-1) \cdots 2 = n!$, so the count allows it, and its proof shows that it is uniform. The naive shuffle has the product $n^n$, and the count already rules it out.

**Why the bias has this shape.** The naive shuffle is a product of $n$ transpositions $(i\ j_i)$, in which the first position of each transposition is fixed and only the second is random. A position can be chosen as $j$ many times, so an item can move several times, forward and back. Fisher-Yates never moves an item that it has placed. In the naive shuffle, the items that are moved early can be moved again later, and the orders that are reached by many such paths get extra weight.

## Examples

**All 27 runs for $n = 3$.** Start from $A = [0, 1, 2]$. Each run is a string $j_0 j_1 j_2$.

| output | runs | count | probability |
|---|---|---|---|
| $[0, 1, 2]$ | 012, 021, 102, 210 | 4 | $4/27 \approx 0.148$ |
| $[0, 2, 1]$ | 011, 022, 101, 120, 200 | 5 | $5/27 \approx 0.185$ |
| $[1, 0, 2]$ | 002, 112, 121, 201, 220 | 5 | $5/27 \approx 0.185$ |
| $[1, 2, 0]$ | 001, 020, 111, 122, 202 | 5 | $5/27 \approx 0.185$ |
| $[2, 0, 1]$ | 000, 110, 211, 222 | 4 | $4/27 \approx 0.148$ |
| $[2, 1, 0]$ | 010, 100, 212, 221 | 4 | $4/27 \approx 0.148$ |

For example, the run 000 swaps position 0 with itself, then positions 1 and 0, which gives $[1, 0, 2]$, then positions 2 and 0, which gives $[2, 0, 1]$. A uniform shuffle would give each order with probability $1/6 \approx 0.167$, which is $4.5/27$. The [total variation distance](/total-variation-distance/) to uniform is $\frac12 \cdot 6 \cdot \frac{0.5}{27} = 1/18 \approx 0.056$.

**Larger $n$.** The bias grows with $n$. Exact counts over all $n^n$ runs give:

| $n$ | runs $n^n$ | uniform share $n^n/n!$ | largest count | smallest count | largest / smallest | total variation |
|---|---|---|---|---|---|---|
| 3 | 27 | 4.5 | 5 | 4 | 1.25 | 0.0556 |
| 4 | 256 | 10.67 | 15 | 8 | 1.88 | 0.0651 |
| 5 | 3125 | 26.04 | 47 | 16 | 2.94 | 0.0842 |
| 6 | 46656 | 64.8 | 159 | 32 | 4.97 | 0.0980 |
| 7 | 823543 | 163.40 | 543 | 64 | 8.48 | 0.1123 |

For $n = 4$ the most likely order is $[1, 0, 3, 2]$, with probability $15/256$, and the least likely are $[3, 0, 1, 2]$ and $[3, 1, 2, 0]$, with $8/256$. For $n$ from 5 to 7 the least likely order is the rotation $[n-1, 0, 1, \ldots, n-2]$, with count $2^{n-1}$. Goldstein and Moews proved that for $n \ge 18$ the identity is the most likely order. A statistical test with enough samples finds the bias. For $n = 4$, a chi-squared test with 24000 samples has a statistic of about 740 on average, while a uniform shuffle stays below 80 with probability more than $1 - 10^{-7}$.

**Other wrong shuffles of the same kind.**

- **Swap with an earlier position only.** RANDOM$(0, i - 1)$ in Durstenfeld's loop gives [Sattolo's algorithm](/sattolo-algorithm/): uniform, but only on the $(n-1)!$ cyclic permutations. It is correct for its own problem, and wrong as a shuffle.
- **Sort with a random comparator.** The run is fixed by a bounded number of coin flips, so each probability is a fraction with a power of two below it. For $n \ge 3$ that cannot be $1/n!$. See [sort-based shuffle](/sort-based-shuffle/).
- **Random keys with many ties.** Random keys from a small range, with a stable sort, favor the input order. See [permute by sorting](/permute-by-sorting/).
- **Modulo of a random word.** The right range with `word mod (i + 1)` is biased; see [modulo bias](/modulo-bias/).
- **A fixed number of random swaps.** Swapping two uniform positions $t$ times is the [random transposition shuffle](/random-transposition-shuffle/). It is never exactly uniform for $n \ge 3$, and it needs about $\frac12 n \ln n$ swaps to be close to uniform. With only $n$ swaps it is far from uniform for large $n$.

## Where it is used

The naive shuffle appears in teaching material and in production code as a bug. It is the standard example of why a [randomized algorithm](/randomized-algorithm/) needs a proof of its output distribution and not only a test. It also shows the counting argument that rules out a class of methods: if the number of equally likely runs is not a multiple of $n!$, the method is not uniform. The same argument shows that the card-shuffling chains of the [card shuffling](/card-shuffling/) page are never exactly uniform after a fixed number of steps.

## References
