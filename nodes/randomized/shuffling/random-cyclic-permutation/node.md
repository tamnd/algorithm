---
tag: CN6YSC
kind: problem
slug: random-cyclic-permutation
name: Random cyclic permutation generation
aliases:
- random single-cycle permutation
- random n-cycle
- random cyclic permutation
area: randomized/shuffling
level: core
summary: Produce a permutation of n elements that is one cycle through all n elements, with each of the (n − 1)! such cycles equally likely.
prereqs: [permutation-cycles, random-permutation]
see_also: [sattolo-algorithm, fisher-yates-shuffle, derangement, permutation-cycle-decomposition, stirling-numbers, symmetric-group, naive-shuffle]
sources:
  - paper: doi:10.1016/0020-0190(86)90073-6
    title: Sandra Sattolo, An algorithm to generate a random cyclic permutation, Information Processing Letters 22(6), 1986
    locator: pp. 315 to 317
  - paper: doi:10.1007/BF01941134
    title: David Gries and Jinyun Xue, Generating a random cyclic permutation, BIT 28, 1988
    locator: the whole note
  - paper: doi:10.1007/s00026-009-0003-3
    title: Mark C. Wilson, Random and exhaustive generation of permutations and cycles, Annals of Combinatorics 13, 2009
    locator: the treatment of Sattolo's algorithm next to Fisher-Yates
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Algorithm P (the shuffle used by the shuffle-then-link method)
  - paper: "Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in Algorithms and Complexity, New Directions and Recent Results, J. F. Traub (editor), Academic Press, 1976, pages 357 to 428"
    locator: the entropy lower bound on the expected number of random bits
---

The random cyclic permutation problem asks for a [permutation](/permutation/) $\sigma$ of $\{0, \ldots, n-1\}$ that is one [cycle](/permutation-cycles/) of length $n$, with each of the $(n-1)!$ such cycles equally likely. It is a restricted form of the [random permutation](/random-permutation/) problem: the output is uniform on a subset of the [symmetric group](/symmetric-group/), not on all of it. [Sattolo's algorithm](/sattolo-algorithm/) solves it in place in $\Theta(n)$ time. This page is about the problem; the algorithm and its proof are on the Sattolo page.

## In plain words

Some people stand in a circle, and each one must give a present to exactly one other person and get one from exactly one other person. If the gifts must form one big loop, so that following them from any person visits everyone before it comes back, the loop is a cyclic permutation. The task is to pick such a loop at random so that every possible loop has the same chance.

A random order of the people is not the same thing. A random order often splits into several small loops, and some people even give to themselves. The fix is to put the people in a random order and close the line into a ring, or to use Sattolo's small change to the usual shuffle.

## Definition

**Input.** An integer $n \ge 1$, or an array $A[0 \ldots n-1]$. A source of randomness, in one of the models of the [random permutation](/random-permutation/) page.

**Output.** A random permutation $\sigma$ of $\{0, \ldots, n-1\}$ with $\Pr[\sigma = \tau] = 1/(n-1)!$ for each $\tau$ in
$$C_n = \{\tau \in S_n : \tau \text{ is one cycle of length } n\}.$$
For an array input, the output is $A[\sigma(0)], \ldots, A[\sigma(n-1)]$, and the cycle is read on positions.

**Size of $C_n$.** $|C_n| = (n-1)!$. Each $n$-cycle has exactly one cycle notation $(0\ x_1\ \cdots\ x_{n-1})$ that starts with 0, and $(x_1, \ldots, x_{n-1})$ can be any of the $(n-1)!$ orders of $\{1, \ldots, n-1\}$. The [Stirling number](/stirling-numbers/) of the first kind $\left[{n \atop 1}\right]$ counts the same set.

**Two representations.** An $n$-cycle can be given as the map $p \mapsto \sigma(p)$ (an array of "next" pointers) or as the cyclic order $(x_0, x_1, \ldots, x_{n-1})$ with $\sigma(x_k) = x_{k+1}$ and $x_n = x_0$. The cyclic order is defined up to rotation: each $n$-cycle has exactly $n$ such orders.

## Variants

- **Undirected cycle.** A uniform Hamiltonian cycle of the complete graph on $n \ge 3$ vertices, with no direction. There are $(n-1)!/2$ of them. Draw a uniform $n$-cycle and forget the direction: each undirected cycle comes from exactly two directed ones, so the result is uniform.
- **Uniform derangement.** A permutation with no fixed point, uniform on all $D_n$ [derangements](/derangement/). This is a larger set: for $n = 4$ there are 9 derangements, of which 6 are 4-cycles and 3 are products of two 2-cycles. An $n$-cycle is a derangement for $n \ge 2$, but a uniform $n$-cycle is not a uniform derangement for $n \ge 4$.
- **Given cycle type.** A uniform permutation with a given list of cycle lengths. Draw a uniform order and cut it into blocks of the given lengths, then close each block into a cycle. The $n$-cycle is the case of one block.
- **Random $k$-cycle.** A uniform cycle of length $k$ on $k$ chosen points among $n$, with the other points fixed. Choose a uniform ordered sample $(x_0, \ldots, x_{k-1})$ of $k$ points and close it into a cycle; each $k$-cycle comes from $k$ samples.

## Examples

- **$n = 3$.** $C_3$ has the two cycles $(0\ 1\ 2)$ and $(0\ 2\ 1)$. As arrays $p \mapsto \sigma(p)$ they are $[1, 2, 0]$ and $[2, 0, 1]$. Each must have probability $1/2$, so one fair bit is enough.
- **$n = 4$.** $C_4$ has 6 cycles: $(0\ 1\ 2\ 3)$, $(0\ 1\ 3\ 2)$, $(0\ 2\ 1\ 3)$, $(0\ 2\ 3\ 1)$, $(0\ 3\ 1\ 2)$ and $(0\ 3\ 2\ 1)$. Of the 24 permutations of 4 elements, these 6 are the ones with one cycle, so a uniform permutation is a 4-cycle with probability $1/4$.
- **In general,** a uniform permutation of $n$ elements is an $n$-cycle with probability $(n-1)!/n! = 1/n$. The expected number of cycles of a uniform permutation is the [harmonic number](/harmonic-series/) $H_n \approx \ln n$, so a random order has about $\ln n$ loops, not one.
- **$n = 52$.** $|C_{52}| = 51! \approx 1.551 \times 10^{66}$, and $\log_2 51! \approx 219.88$ bits.

## Known algorithms

| method | time | extra space | randomness | exact |
|---|---|---|---|---|
| [Sattolo's algorithm](/sattolo-algorithm/) | $\Theta(n)$ | $O(1)$ | $n - 1$ uniform integers, ranges $n-1, \ldots, 1$ | yes |
| shuffle, then link | $\Theta(n)$ | $\Theta(n)$ | $n - 1$ uniform integers, ranges $n, \ldots, 2$ | yes |
| shuffle $\{1, \ldots, n-1\}$, then put 0 first | $\Theta(n)$ | $\Theta(n)$ | $n - 2$ uniform integers | yes |
| rejection from uniform permutations | $\Theta(n^2)$ expected | $\Theta(n)$ | $n$ shuffles expected | yes |

- **Sattolo's algorithm** is the [Fisher-Yates shuffle](/fisher-yates-shuffle/) with the random index taken from $\{0, \ldots, i-1\}$. The proof on its page shows a bijection between the $(n-1)!$ choice sequences and $C_n$.
- **Shuffle, then link.** Draw a uniform order $(x_0, \ldots, x_{n-1})$ and set $\sigma(x_k) = x_{k+1 \bmod n}$. Each $n$-cycle comes from exactly its $n$ rotations, so each has probability $n / n! = 1/(n-1)!$.
- **Fix the start.** Draw a uniform order $(x_1, \ldots, x_{n-1})$ of $\{1, \ldots, n-1\}$ and output the cycle $(0\ x_1\ \cdots\ x_{n-1})$. This is the bijection that proves $|C_n| = (n-1)!$, and it needs the fewest random integers among the simple methods.
- **Rejection.** Draw uniform permutations until one is an $n$-cycle. Each try succeeds with probability $1/n$, so the expected number of tries is $n$ (a [geometric distribution](/geometric-distribution/)). It is correct and slow.

## Bounds

- **Time.** $\Omega(n)$, since the output has $n$ entries. Sattolo's algorithm meets it.
- **Random bits.** An exact method needs at least $\log_2 (n-1)!$ fair bits on average, the entropy of the uniform distribution on $C_n$ (Knuth and Yao). This is $\log_2 n$ bits less than for a uniform permutation.
- **No bounded worst case on fair bits for $n \ge 4$.** With at most $B$ fair bits per run, each probability has the form $m/2^B$. For $n \ge 4$, 3 divides $(n-1)!$, so $1/(n-1)!$ has no such form. For $n \le 3$, $(n-1)!$ is 1 or 2, and at most one bit is enough.

## Reductions

- **Random permutation of $n - 1$ elements gives a random $n$-cycle.** The "fix the start" map above is a bijection from the orders of $\{1, \ldots, n-1\}$ to $C_n$. It sends the uniform distribution to the uniform distribution.
- **Random $n$-cycle gives a random permutation of $n - 1$ elements.** Read a uniform $n$-cycle from position $n - 1$: the order $\sigma(n-1), \sigma^2(n-1), \ldots, \sigma^{n-1}(n-1)$ lists $\{0, \ldots, n-2\}$, and it is uniform because the map is the inverse of the bijection above. So the two problems are equivalent, with the size changed by one, and with $O(n)$ extra work.
- **To a cycle decomposition.** Any method that writes a permutation as cycles can check the output; see [cycle decomposition](/permutation-cycle-decomposition/).

## Applications

- **Pointer-chasing tests.** An array `next` that is one random cycle visits every slot before it repeats, and each load depends on the one before it. Such loops are used to measure memory latency without help from the hardware prefetcher. Several cycles would visit only a part of the array.
- **Random tours.** A random first tour for a local search on the traveling salesman problem, or a random order of visits that must return to the start.
- **Gift exchanges in one loop.** A draw in which each person gives to the next person on one random loop. If any derangement is allowed, the draw must be a uniform [derangement](/derangement/) instead.
- **Tests of cycle algorithms.** Single-cycle permutations are the worst case for algorithms that follow cycles, for example [cycle-leader permutation](/cycle-leader-permutation/) in place.

## References
