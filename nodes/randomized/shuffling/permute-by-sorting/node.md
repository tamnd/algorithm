---
tag: E5K3WT
kind: algorithm
slug: permute-by-sorting
name: Permute by sorting
aliases:
- PERMUTE-BY-SORTING
- random priorities shuffle
- shuffle by sorting random keys
area: randomized/shuffling
level: core
summary: Give each item an independent random key from a range of size n^3, draw again if two keys are equal, and sort the items by key. With distinct keys each of the n! orders has probability exactly 1/n!.
solves: [random-permutation]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {expected: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {in_place: false, online: false, deterministic: false, recursive: false}
history:
  year: 2001
  people: [Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein]
  note: The method is folklore. The name PERMUTE-BY-SORTING and the lemma on distinct priorities are from the chapter on randomized algorithms of the textbook by Cormen, Leiserson, Rivest and Stein, which first appeared in the second edition (to be checked).
prereqs: [random-permutation, sorting-problem, birthday-paradox]
see_also: [fisher-yates-shuffle, sort-based-shuffle, merge-shuffle, union-bound, stable-sort, sorting-network, treap, naive-shuffle]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, 2009
    locator: Section 5.3, the procedure PERMUTE-BY-SORTING and Lemma 5.4 (uniform if all priorities are distinct); Exercise 5.3-5 (the priorities are distinct with probability at least 1 − 1/n) (lemma and exercise numbers to be checked)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2 (Algorithm P, the linear-time method that is usually better)
  - paper: "Axel Bacher, Olivier Bodini, Alexandros Hollender and Jérémie Lumbroso, MergeShuffle, a very fast, parallel random permutation algorithm, arXiv:1508.03167, 2015"
    locator: Section 1 (the splitting methods, which use random bits as keys one bit at a time)
---

Permute by sorting produces a uniform [random permutation](/random-permutation/) by attaching an independent random key, or priority, to each item and sorting the items by key. If the keys are distinct, the sorted order is uniform on all $n!$ orders. With keys from a range of size $n^3$, a tie has probability at most $1/(2n)$, and the algorithm draws all keys again when one occurs. It costs $\Theta(n \log n)$ time with a comparison sort and uses about three times more random bits than needed. Its value is that it needs only a sort, which makes it the standard shuffle in databases, in parallel and external-memory settings, and in a proof that random priorities give random orders.

## In plain words

Give every card a lottery ticket with a random number on it. Then sort the cards by their ticket numbers. Since the tickets were handed out at random, no card has a better chance than another to get the smallest number, or the second smallest, and so on. So the sorted order is a fair random order.

There is one catch. If two tickets show the same number, the sort must decide which card goes first, and it usually keeps the old order. That gives a small advantage to the old order. The fix is to use numbers from a big range, so that equal tickets are rare, and to hand out new tickets if two are equal.

This page is about random keys. The different and wrong idea of a sort with a coin flip as the comparison is on the sort-based shuffle page.

## The problem

The input is an array $A[0 \ldots n-1]$. The output is $A[\sigma(0)], \ldots, A[\sigma(n-1)]$ for a random permutation $\sigma$ with $\Pr[\sigma = \tau] = 1/n!$ for each $\tau$. The source of randomness is RANDOM$(a, b)$, uniform on $\{a, \ldots, b\}$ with independent calls. This is the [random permutation](/random-permutation/) problem.

## The algorithm

```pseudo id=main
PERMUTE-BY-SORTING(A)                      ▷ A[0 .. n − 1]
L1  n ← A.length; M ← n³
L2  repeat
L3      for i ← 0 to n − 1 do P[i] ← RANDOM(0, M − 1)
L4  until the keys P[0], …, P[n − 1] are distinct
L5  sort A, using P as the sort keys
L6  return A
```

Line L5 can use any correct sort: the keys are distinct, so the sorted order is the same for all sorts, and stability does not matter. The test of line L4 is a hash set in expected $O(n)$ time, or a check of adjacent keys after the sort. Any range $M \ge n$ gives a correct algorithm. The choice $M = n^3$ keeps the number of rounds near 1 and the keys within $3 \log_2 n$ bits.

## Example

Let $A = [a, b, c, d]$, so $n = 4$ and $M = 64$. Suppose that line L3 draws the keys $P = [37, 5, 51, 12]$. They are distinct, so line L4 accepts them.

| item | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| key | 37 | 5 | 51 | 12 |
| rank of the key | 2 | 0 | 3 | 1 |

Sorted by key, the output is $[b, d, a, c]$. If line L3 had drawn $[37, 5, 37, 12]$, the tie between $a$ and $c$ would send the algorithm back to line L3 for four new keys.

## Correctness

**Theorem.** Let the $n$ keys be independent and uniform on $\{0, \ldots, M-1\}$ with $M \ge n$. Given that the keys are distinct, the sorted order is uniform on all $n!$ orders. So PERMUTE-BY-SORTING returns a uniform random permutation, and it stops with probability 1.

*Counting proof.* A key vector with distinct entries is fixed by two things: the set $S$ of its $n$ values, and the order $\tau$ in which the items get the values of $S$ from smallest to largest. Each pair $(S, \tau)$ gives exactly one key vector. So each order $\tau$ comes from exactly $\binom{M}{n}$ key vectors, all of the same probability $M^{-n}$. Given distinct keys, each order has probability $\binom{M}{n} / (n! \binom{M}{n}) = 1/n!$.

*Symmetry proof.* For a fixed permutation $\pi$ of the items, the key vector $(P_{\pi(0)}, \ldots, P_{\pi(n-1)})$ has the same distribution as $(P_0, \ldots, P_{n-1})$, because the keys are i.i.d. The event "distinct" does not change under $\pi$. Relabeling by $\pi$ maps the event "the output is $\tau$" onto the event "the output is $\tau'$" for an order $\tau'$ that depends on $\pi$, and every $\tau'$ is reached by some $\pi$. So all orders have the same conditional probability. This proof works for any i.i.d. keys with a continuous distribution too, where ties have probability 0.

Each round is independent and succeeds with probability $q > 0$, so the number of rounds is geometric, and the rounds after a rejection do not depend on the rejected keys. The details are in the proof file.

## Complexity

**Probability of a tie.** By the [union bound](/union-bound/) over the $\binom{n}{2}$ pairs of items,
$$\Pr[\text{some tie}] \le \binom{n}{2} \frac{1}{M} = \frac{n(n-1)}{2n^3} < \frac{1}{2n}.$$
This is the [birthday problem](/birthday-paradox/) with $M$ days. The exact probability of distinct keys is $q = \prod_{i=0}^{n-1} (1 - i/M)$.

| $n$ | $M = n^3$ | $q$ | expected rounds $1/q$ | key bits per round $n \log_2 M$ | $\log_2 n!$ |
|---|---|---|---|---|---|
| 3 | 27 | 0.89163 | 1.1215 | 14.3 | 2.6 |
| 4 | 64 | 0.90891 | 1.1002 | 24.0 | 4.6 |
| 10 | 1000 | 0.95586 | 1.0462 | 99.7 | 21.8 |
| 52 | 140608 | 0.99061 | 1.0095 | 889.3 | 225.6 |
| 1000 | $10^9$ | 0.99950 | 1.0005 | 29897.4 | 8529.4 |

**Time.** Each round draws $n$ keys and checks them in expected $O(n)$ time. The sort costs $\Theta(n \log n)$ comparisons. On the [word RAM](/word-ram/), the keys have $3 \log_2 n$ bits, so a radix sort with base $n$ sorts them in three passes and $\Theta(n)$ time. The expected number of rounds is $1/q < 1 + 1/(2n - 1)$.

**Randomness.** About $3 n \log_2 n$ bits per round, three times the $\log_2 n! \approx n \log_2 n$ of the [Fisher-Yates shuffle](/fisher-yates-shuffle/).

**Space.** $\Theta(n)$ extra for the keys and the index array. The worst case is unbounded, as for every exact method on fair bits.

## Properties

- **Exact** when the keys are uniform integers and ties cause a new draw.
- **Not in place.** It needs the array of keys.
- **Order of the input does not matter.** The keys do not depend on the items, so the output is uniform for each input order.
- **Parallel and oblivious.** All keys can be drawn at once, and any parallel sort or [sorting network](/sorting-network/) finishes the job.

## Variants and improvements

- **Real keys.** Keys uniform in $[0, 1)$ have no ties with probability 1, in exact arithmetic. With floating point numbers of 53 random bits, a tie among $10^6$ keys has probability about $5.6 \times 10^{-5}$, which is not negligible for a test that runs many times.
- **Break ties with more random bits.** Instead of a new draw for all keys, draw more bits only for the keys in a tied group, and sort the group by them. This is the idea of the bitwise splitting methods (Rao and Sandelius) and of [MergeShuffle](/merge-shuffle/), which reveal one random bit of each key at a time.
- **Random keys in a data structure.** A [treap](/treap/) gives each node a random priority, so its shape is that of a [random binary search tree](/random-binary-search-tree/). The proof that a random order of insertions is uniform is the same as here.
- **External memory.** Attach keys and sort with an external merge sort; this costs a sort in the I/O model, which is optimal for [permuting](/permuting-problem/) on disk in most cases. See [external permuting](/external-permuting/).

## When to use it

Use it when a sort is available and a shuffle is not, for example `ORDER BY` a random column in SQL, or in a parallel or distributed system where a sort is the basic step. Use it to shuffle data that do not fit in memory. In ordinary code in memory, use the [Fisher-Yates shuffle](/fisher-yates-shuffle/): it is linear, in place and uses fewer random bits.

## Pitfalls

- **Small key ranges and a stable sort.** Without the check of line L4, ties are left to the sort. A stable sort keeps tied items in input order, so the input order gets extra weight. For $n = 3$ with keys from 2 values, the orders have probabilities $4/8, 1/8, 1/8, 1/8, 1/8, 0$, and the reversed order never appears. With 3 values the counts are $10, 4, 4, 4, 4, 1$ out of 27, and with 4 values $20, 10, 10, 10, 10, 4$ out of 64 (exact enumeration, in the test file).
- **Short keys.** With 32-bit keys and $n = 52$, a tie has probability about $3.1 \times 10^{-7}$; with $n = 10^5$ it is about $0.69$. The key length must grow with $n$.
- **A random comparator is not a random key.** A sort called with a comparison that flips a coin, or a key function that is called again at each comparison, does not give random keys. It is biased; see [sort-based shuffle](/sort-based-shuffle/).
- **Quadratic sorts on large inputs.** The sort is the whole cost; an $O(n^2)$ sort removes the reason to use the method.

## Implementations

## History

The idea of sorting random numbers to get a random order is old and has no clear first source. Cormen, Leiserson, Rivest and Stein gave it the name PERMUTE-BY-SORTING in their textbook, with a proof that distinct priorities give a uniform order and an exercise that bounds the probability of a tie for keys from $\{1, \ldots, n^3\}$. The same idea underlies random priorities in treaps (Aragon and Seidel, 1989) and the splitting methods of Rao (1961) and Sandelius (1962).

## References
