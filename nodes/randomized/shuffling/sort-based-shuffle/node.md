---
tag: JTAPRN
kind: algorithm
slug: sort-based-shuffle
name: Sort-based shuffle
aliases:
- shuffle by random keys
- random-key sort shuffle
- random comparator shuffle
- sort with a random comparator
area: randomized/shuffling
level: intro
summary: Shuffling with a sort routine. Random keys without ties give a uniform order (see permute-by-sorting); a comparator that flips a coin is biased for n ≥ 3 with every sort.
solves: [random-permutation]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n^2), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 2010
  people: [Rob Weir]
  note: The random-comparator idiom is old folklore. A widely read case is the browser choice screen of 2010, whose random order came from a sort with a random comparator and was biased (analysis by Rob Weir, to be checked).
prereqs: [comparison-model, insertion-sort, random-permutation]
see_also: [permute-by-sorting, fisher-yates-shuffle, naive-shuffle, merge-sort, shuffling-a-linked-list, merge-shuffle, total-variation-distance, quicksort]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, 2009
    locator: Section 5.3 (PERMUTE-BY-SORTING, the correct form with random keys)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2 (Algorithm P, the shuffle to use instead)
  - paper: "Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in Algorithms and Complexity, New Directions and Recent Results, J. F. Traub (editor), Academic Press, 1976, pages 357 to 428"
    locator: the model of a procedure driven by fair coin flips, whose output probabilities are dyadic when the number of flips is bounded
---

A sort-based shuffle puts items in random order by calling a sort routine. There are two forms, and they behave very differently. **With random keys**, each item gets an independent random key and the items are sorted by key; this is correct when the keys are distinct, and it is the subject of [permute by sorting](/permute-by-sorting/). **With a random comparator**, the sort is called with a comparison function that ignores the items and returns a coin flip, as in `sort(() => Math.random() - 0.5)`. This page is mainly about the second form. It is biased for every $n \ge 3$ and every sort that makes a bounded number of comparisons, because each output then has a probability with a power of two below it, and $1/n!$ is not such a number. With insertion sort the identity has probability $2^{-(n-1)}$, and the [total variation distance](/total-variation-distance/) to uniform is $0.66$ already for $n = 7$.

## In plain words

There are two ways to shuffle with a sorting routine. The good way gives each card a random number and sorts by the numbers. The bad way asks the sorting routine to sort, but answers each of its "which card comes first?" questions by a coin toss.

The bad way looks harmless, but a sorting routine asks few questions, and it often leaves a card near where it was. With a simple sort a card moves left only while the coin keeps saying so, so most cards move one or two places at most. The order at the end is far from random.

There is also a counting reason. All chances from coin tosses are halves, quarters, eighths, and so on. With three cards, each order needs a chance of one in six, and no sum of halves, quarters and eighths can give that.

## The problem

The intent is to solve the [random permutation](/random-permutation/) problem: output the items of $A[0 \ldots n-1]$ in an order that is uniform on all $n!$ orders. The tool is a sort routine in the [comparison model](/comparison-model/), with a comparison LESS$(x, y)$ supplied by the caller. The random-comparator form sets LESS$(x, y)$ to RANDOM$(0, 1) = 0$, a fair coin that is independent at each call. It fails the intent for $n \ge 3$. The random-key form, which succeeds, is analyzed on [permute by sorting](/permute-by-sorting/).

## The algorithm

The random comparator inside [insertion sort](/insertion-sort/):

```pseudo id=main
COIN-INSERTION-SHUFFLE(A)                  ▷ A[0 .. n − 1]; this is BIASED
L1  for i ← 1 to n − 1 do
L2      x ← A[i]; j ← i − 1
L3      while j ≥ 0 and RANDOM(0, 1) = 0 do    ▷ the test "x < A[j]" is a coin
L4          A[j + 1] ← A[j]; j ← j − 1
L5      A[j + 1] ← x
```

The same comparator inside [merge sort](/merge-sort/) takes the head of the right run when the coin is 0 and the head of the left run when it is 1. The Python file has both forms and the correct form with random keys.

## Example

Run COIN-INSERTION-SHUFFLE on $[a, b, c, d]$ with the coins $1;\ 0, 1;\ 0, 0, 1$.

| $i$ | coins | moves of $x$ | $A$ after line L5 |
|---|---|---|---|
| 1 | 1 | $b$ stays | $a\ b\ c\ d$ |
| 2 | 0, 1 | $c$ moves one place left | $a\ c\ b\ d$ |
| 3 | 0, 0, 1 | $d$ moves two places left | $a\ d\ c\ b$ |

**All runs for $n = 3$.** Exact enumeration of all coin sequences gives these probabilities, starting from $[0, 1, 2]$:

| output | insertion sort | merge sort | uniform |
|---|---|---|---|
| $[0, 1, 2]$ | $1/4$ | $1/4$ | $1/6$ |
| $[0, 2, 1]$ | $1/8$ | $1/4$ | $1/6$ |
| $[1, 0, 2]$ | $1/4$ | $1/8$ | $1/6$ |
| $[1, 2, 0]$ | $1/8$ | $1/8$ | $1/6$ |
| $[2, 0, 1]$ | $1/8$ | $1/8$ | $1/6$ |
| $[2, 1, 0]$ | $1/8$ | $1/8$ | $1/6$ |

Both have total variation distance $1/6$ to uniform. The two sorts favor different orders, so the bias depends on the sort routine, and a library that changes its sort changes the bias.

## Correctness

The random-comparator shuffle is **not correct**. The page states and proves the failure.

**Theorem.** Let a sort routine make at most $B$ calls of the comparator on every input and for every answer sequence. If each answer is a fair coin, each output order has probability $m / 2^B$ for an integer $m$. For $n \ge 3$ this is never $1/n!$, so the output is not uniform.

*Proof sketch.* Pad every run to exactly $B$ coins. A run is fixed by its $B$ coins, each sequence has probability $2^{-B}$, and an output's probability is the number of its sequences over $2^B$. If this equals $1/n!$, then $n! \cdot m = 2^B$, which is false for $n \ge 3$, since 3 divides $n!$. $\square$

Every comparison sort that stops on all comparator answers has such a bound $B$: $\binom{n}{2}$ for insertion sort, about $n \lceil \log_2 n \rceil$ for [merge sort](/merge-sort/). The same holds for [quicksort](/quicksort/), [heapsort](/heapsort/) and any [sorting network](/sorting-network/). So no choice of sort repairs the method. The proof file also gives the exact distribution of COIN-INSERTION-SHUFFLE.

For $n \le 2$ the method is fair: with two items one coin decides the order.

## Complexity

COIN-INSERTION-SHUFFLE makes at most $\binom{n}{2}$ coin flips and shifts, so its time is $O(n^2)$ in the worst case and $\Theta(n)$ in the best case. Item $i$ moves a truncated geometric number of places, with mean less than 1, so the expected time is $\Theta(n)$. With merge sort the time is $\Theta(n \log n)$. The cost does not matter much, since the output is wrong.

The random-key form costs a sort, $\Theta(n \log n)$, plus $n$ random keys; see [permute by sorting](/permute-by-sorting/).

## Properties

**How large the bias is.** Exact enumeration over all coin sequences, with the identity as input:

| $n$ | insertion: TV | insertion: largest / smallest | merge: TV | merge: largest / smallest |
|---|---|---|---|---|
| 3 | 0.1667 | $1/4$ / $1/8$ | 0.1667 | $1/4$ / $1/8$ |
| 4 | 0.2917 | $1/8$ / $1/64$ | 0.1667 | $1/16$ / $1/32$ |
| 5 | 0.4083 | $1/16$ / $1/1024$ | 0.2375 | $1/32$ / $1/256$ |
| 6 | 0.5463 | $1/32$ / $1/32768$ | 0.2917 | $1/128$ / $1/2048$ |
| 7 | 0.6562 | $1/64$ / $1/2097152$ | 0.3224 | $1/512$ / $1/16384$ |

For insertion sort the most likely output is the input order, with probability $2^{-(n-1)}$, which is $78.75$ times the uniform $1/7!$ at $n = 7$. The least likely is the reversed order, with probability $2^{-\binom{n}{2}}$. The TV values are rounded from exact fractions; for $n = 4$ they are $7/24$ and $1/6$.

**Dependence on the input order.** The output is a random function of the input order, close to it for insertion sort. A uniform shuffle has no such memory.

## Variants and improvements

- **Random keys.** Draw one key per item before the sort, and sort by the keys. This is correct when the keys are distinct; see [permute by sorting](/permute-by-sorting/).
- **Weighted coins in a merge.** If the merge takes the head of the left run with probability $\ell / (\ell + r)$, where $\ell$ and $r$ are the numbers of items left in the runs, each interleaving is equally likely and merge sort becomes a correct shuffle. This is not a comparator any more, since the coin depends on the run sizes. See [shuffling a linked list](/shuffling-a-linked-list/) and [MergeShuffle](/merge-shuffle/).
- **A biased comparator with $p \ne 1/2$.** The probabilities become polynomials in $p$. For insertion sort the identity has probability $(1-p)^{n-1}$, and no single $p$ makes all $n!$ orders equal for $n \ge 3$.

## When to use it

Do not use the random-comparator form. Use the [Fisher-Yates shuffle](/fisher-yates-shuffle/) in memory, and use random keys with a sort when only a sort is available, for example `ORDER BY` a random value in a database.

## Pitfalls

- **It passes a quick look.** For $n = 3$ every order appears, and a few runs look random. The bias shows only in counts, and for some sorts it hides in a few orders.
- **It breaks the sort's contract.** A comparator must be consistent: if $x < y$ and $y < z$ then $x < z$, and LESS$(x, y)$ must give the same answer each time. A coin violates this. Some sort routines then give an error (Java's TimSort can report that the comparison method violates its general contract), read past the array or do not stop. The behavior depends on the library.
- **A key function that is called more than once.** In a language whose sort calls the key function at each comparison, a random key function acts as a random comparator. Draw the keys once, store them, then sort.
- **Ties in short random keys.** Even the random-key form is biased if ties are left to a stable sort; see the pitfalls of [permute by sorting](/permute-by-sorting/).

## Implementations

## History

Sorting with a random comparator is folklore and appears in code and answers on the web in many languages. A well-known case is the browser choice screen that Microsoft showed to users in Europe in 2010. Its random order of five browsers came from a sort with a random comparator in JavaScript, and Rob Weir showed that the positions were far from uniform. The fix was a Fisher-Yates shuffle. The counting argument on this page is the same as for the [naive shuffle](/naive-shuffle/) and is in the spirit of the analysis of coin-driven procedures by Knuth and Yao.

## References
