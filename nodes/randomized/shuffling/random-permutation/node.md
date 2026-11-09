---
tag: 823S59
kind: problem
slug: random-permutation
name: Random permutation generation
aliases:
- uniform random permutation
- random shuffling
- shuffling problem
area: randomized/shuffling
level: intro
summary: Produce a permutation of n items so that each of the n! orders is equally likely, from a source of random numbers.
prereqs: [permutation, uniform-distribution]
see_also: [fisher-yates-shuffle, naive-shuffle, permute-by-sorting, merge-shuffle, sattolo-algorithm, random-cyclic-permutation, card-shuffling, permutation-unranking]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Random sampling and shuffling (Algorithm P and the discussion of shuffling)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 5.3, Randomized algorithms (uniform random permutations and RANDOMLY-PERMUTE)
  - paper: doi:10.1145/364520.364540
    title: Richard Durstenfeld, Algorithm 235, Random permutation, Communications of the ACM 7(7), 1964
    locator: p. 420
  - paper: "Axel Bacher, Olivier Bodini, Alexandros Hollender and Jérémie Lumbroso, MergeShuffle, a very fast, parallel random permutation algorithm, arXiv:1508.03167, 2015"
    locator: Section 1 (the survey of Fisher-Yates, Rao-Sandelius and the splitting methods) and Section 2 (MergeShuffle and its number of random bits)
  - paper: "Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in Algorithms and Complexity, New Directions and Recent Results, J. F. Traub (editor), Academic Press, 1976, pages 357 to 428"
    locator: the lower bound of the entropy on the expected number of random bits
---

The random permutation problem asks for a [permutation](/permutation/) of $n$ items such that each of the $n!$ orders has probability exactly $1/n!$, whatever the input order was. The [Fisher-Yates shuffle](/fisher-yates-shuffle/) solves it in $\Theta(n)$ time with $n - 1$ uniform random integers, and no exact method can use fewer than $\log_2 n!$ random bits on average. This page is about the problem: what counts as a solution, its variants, its bounds and its traps. The algorithms have their own pages.

## In plain words

You have a list of things, for example a deck of cards or the names of people in an experiment. You want to put them in a random order, and "random" has a strict meaning here: every possible order must have exactly the same chance. For three cards there are six orders, so each must come out one time in six on average.

This is harder to get right than it looks. Many simple methods give some orders more often than others, and the error does not show in a quick test. The correct methods are short. They place the items one at a time, and each item comes from the ones that are still free, with equal chances. The question also has a cost side: how many random coin flips you need, and how much time and memory.

## Definition

**Input.** An integer $n \ge 0$, or an array $A[0 \ldots n-1]$ of items. Equal items are allowed, and they count as different by their positions.

**Source of randomness.** One of these models, which the algorithm must state:

- *uniform integers*: RANDOM$(a, b)$ is uniform on $\{a, \ldots, b\}$, and the calls are independent;
- *fair bits*: each call gives one independent bit, 0 or 1 with probability $1/2$ each;
- *uniform reals*: each call gives a uniform real in $[0, 1)$. This is a model of exact arithmetic; a floating point number has only finitely many values.

**Output.** A random permutation $\sigma$ of $\{0, \ldots, n-1\}$, or the array $A[\sigma(0)], \ldots, A[\sigma(n-1)]$, such that
$$\Pr[\sigma = \tau] = \frac{1}{n!} \quad \text{for each permutation } \tau \text{ of } \{0, \ldots, n-1\}.$$
So $\sigma$ has the [uniform distribution](/uniform-distribution/) on the [symmetric group](/symmetric-group/) $S_n$. An algorithm is *exact* if this holds, and *$\varepsilon$-close* if the [total variation distance](/total-variation-distance/) $\frac12 \sum_\tau |\Pr[\sigma = \tau] - 1/n!|$ is at most $\varepsilon$.

**Two facts used on all the shuffling pages.** If $\sigma$ is uniform on $S_n$ and $\rho$ is a fixed permutation, then $\sigma \circ \rho$, $\rho \circ \sigma$ and $\sigma^{-1}$ are uniform too, because each of these maps is a bijection of $S_n$. So a uniform shuffle of an input in any order is uniform, and a uniform shuffle of a shuffled input is still uniform. Second, an algorithm that uses at most $B$ fair bits on every run gives each output with a probability of the form $m/2^B$. For $n \ge 3$, $1/n!$ is not of this form, because $3$ divides $n!$. So **no exact algorithm on fair bits has a worst-case bound on its number of bits**, for $n \ge 3$. Exact methods on fair bits must use rejection, which has a bounded expected cost and an unbounded worst case.

## Variants

- **Random $k$-permutation.** An ordered sample of $k$ distinct items out of $n$, each with probability $(n-k)!/n!$. The first $k$ steps of Fisher-Yates give it in $\Theta(k)$ time. The unordered version is a [uniform random subset](/uniform-random-subset/); see also [Floyd's sampling](/floyd-sampling/) and [reservoir sampling](/reservoir-sampling/).
- **Random cyclic permutation.** A uniform permutation with one cycle of length $n$. See [random cyclic permutation](/random-cyclic-permutation/) and [Sattolo's algorithm](/sattolo-algorithm/).
- **Random derangement, involution or permutation of a given cycle type.** Uniform on a subset of $S_n$. Rejection from a uniform permutation works when the subset is not too small: a uniform permutation is a [derangement](/derangement/) with probability $D_n/n! \to 1/e$.
- **Approximately uniform shuffles.** A card-shuffling [Markov chain](/markov-chain/) never reaches the exact uniform distribution in a fixed number of steps, but it gets $\varepsilon$-close. The question there is how many steps; see [card shuffling](/card-shuffling/).
- **Shuffling in other memory models.** A linked list ([shuffling a linked list](/shuffling-a-linked-list/)), a stream of unknown length, data on disk ([external permuting](/external-permuting/)), and a parallel machine ([merge shuffle](/merge-shuffle/)).
- **Pseudorandom permutations.** A keyed family of permutations that no efficient test can tell from a uniform one. This is a different, cryptographic problem; see [pseudorandom permutation](/pseudorandom-permutation/).

## Examples

- For $n = 3$ the six orders $[0,1,2]$, $[0,2,1]$, $[1,0,2]$, $[1,2,0]$, $[2,0,1]$, $[2,1,0]$ each have probability $1/6$.
- **Non-example.** The [naive shuffle](/naive-shuffle/), which swaps each position with a uniform position of the whole array, gives these six orders with probabilities $4/27, 5/27, 5/27, 5/27, 4/27, 4/27$. It has $3^3 = 27$ equally likely runs, and 27 is not a multiple of 6.
- **Non-example.** Sorting with a comparator that returns a fair coin flip, with [insertion sort](/insertion-sort/) on $n = 3$, gives $[0,1,2]$ and $[1,0,2]$ with probability $1/4$ each and the other four orders with probability $1/8$ each. See [sort-based shuffle](/sort-based-shuffle/).
- **The size of the problem.** A deck of 52 cards has $52! \approx 8.0658 \cdot 10^{67}$ orders, and $\log_2 52! \approx 225.58$. So an exact shuffle of the deck needs at least 225.58 random bits on average, and a generator with less than 226 bits of state cannot reach all orders.
- **Statistics of a uniform permutation.** By [linearity of expectation](/linearity-of-expectation/), a uniform $\sigma \in S_n$ has 1 fixed point on average for each $n \ge 1$, $n(n-1)/4$ [inversions](/inversion/) on average, and $H_n$ [cycles](/permutation-cycles/) on average. For $n = 52$ these are 1, 663 and $H_{52} \approx 4.538$. Such values give simple checks of a shuffle, but they are not proofs of uniformity.

## Known algorithms

| Algorithm | Exact? | Time | Random input | Notes |
|---|---|---|---|---|
| [Fisher-Yates shuffle](/fisher-yates-shuffle/) | yes | $\Theta(n)$ | $n-1$ uniform integers | in place; the standard method |
| inside-out Fisher-Yates | yes | $\Theta(n)$ | $n-1$ uniform integers | one pass over a stream into a new array |
| [Permute by sorting](/permute-by-sorting/) | yes when the keys are distinct | $\Theta(n \log n)$ | $n$ random keys | needs a key range of about $n^3$ or redraws on a tie |
| [Merge shuffle](/merge-shuffle/) | yes | $\Theta(n \log n)$ | $n \log_2 n + \Theta(n)$ expected bits | divide and conquer, parallel |
| [Permutation unranking](/permutation-unranking/) | yes | $O(n)$ to $O(n \log n)$ | one uniform integer in $[0, n!)$ | needs big integers for large $n$ |
| [Sattolo's algorithm](/sattolo-algorithm/) | uniform on the $n$-cycles only | $\Theta(n)$ | $n-1$ uniform integers | not a solution of this problem |
| [Naive shuffle](/naive-shuffle/) | no, for $n \ge 3$ | $\Theta(n)$ | $n$ uniform integers | a common bug |
| [Sort with a random comparator](/sort-based-shuffle/) | no, for $n \ge 3$ | that of the sort | coin flips | a common bug |
| [Riffle shuffles](/gilbert-shannon-reeds-model/), [top-to-random](/top-to-random-shuffle/), [random transpositions](/random-transposition-shuffle/) | no; $\varepsilon$-close after enough steps | depends on the steps | depends on the chain | models of shuffling a real deck |

Rao (1961) and Sandelius (1962) gave a divide and conquer method: give each item a random bit, put the 0 items before the 1 items, and shuffle each group the same way. It is exact and uses about $n \log_2 n$ bits, and its parts can run in parallel.

## Bounds

- **Time.** Writing the output takes $\Omega(n)$ time, so Fisher-Yates is optimal up to a constant factor on a word RAM with an $O(1)$ random integer.
- **Random bits.** An exact algorithm on fair bits outputs one of $n!$ equally likely values, so its expected number of bits is at least $\log_2 n! = n \log_2 n - n \log_2 e + O(\log n)$. This is the entropy bound of Knuth and Yao. Fisher-Yates with rejection at each step uses $O(n \log n)$ expected bits; the [Fisher-Yates page](/fisher-yates-shuffle/) gives the exact sum, for example 355.91 bits against the bound 225.58 for $n = 52$. Methods that keep the unused randomness, such as Lumbroso's Fast Dice Roller or one uniform draw from $[0, n!)$, come within $O(1)$ or $O(n)$ bits of the bound.
- **Worst case on fair bits.** For $n \ge 3$ no exact method has a worst-case bound on its bits, as proved in the definition.
- **Comparison model.** Permute by sorting needs $\Theta(n \log n)$ comparisons, the cost of the sort. Fisher-Yates makes no comparisons of items.
- **External memory.** On disk, the known exact methods cost about as much as sorting, for example random keys and an external sort. The [permuting problem](/permuting-problem/) page gives the lower bound for moving items to given positions, in block transfers.

## Reductions

- **To sorting.** Give each item an independent random key and sort by key. If the keys are distinct, the order is uniform. This is [permute by sorting](/permute-by-sorting/). It costs one sort and $n$ keys.
- **From a uniform integer.** A uniform integer $r$ in $[0, n!)$, written in the [factorial number system](/factorial-number-system/), is a [Lehmer code](/lehmer-code/), and decoding it gives a uniform permutation. This is [permutation unranking](/permutation-unranking/). Fisher-Yates is the same map, read one digit at a time.
- **To a random subset.** The first $k$ items of a uniform permutation form a uniform $k$-subset, in a uniform order.
- **To a random cyclic permutation.** Write a uniform order $(x_0, \ldots, x_{n-1})$ as the cycle $x_0 \to x_1 \to \cdots \to x_{n-1} \to x_0$. Each $n$-cycle comes from exactly $n$ orders, so the cycle is uniform.

## Applications

- **Randomized algorithms.** Shuffle the input first so that the expected cost holds on every input: [randomized quicksort](/randomized-quicksort/), the [hiring problem](/hiring-problem/), [randomized incremental construction](/randomized-incremental-construction/), and the [random binary search tree](/random-binary-search-tree/).
- **Statistics.** Random assignment of treatments in an experiment, permutation tests, and the bootstrap of orders. This is the use that Fisher and Yates had in mind.
- **Games and simulation.** Card games and lotteries, where a biased shuffle or a small seed is a security hole.
- **Testing.** Random test orders, and random inputs for the average case of an algorithm, as in [average-case analysis](/average-case-analysis/).

## References
