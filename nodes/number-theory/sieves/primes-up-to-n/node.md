---
tag: GG1WB7
kind: problem
slug: primes-up-to-n
name: Listing primes up to n
aliases:
- prime enumeration
- prime sieve problem
- generating primes up to a bound
area: number-theory/sieves
level: intro
summary: Given n, output all primes less than or equal to n. Sieves solve it in O(n log log n) or O(n) word operations, and the output alone has about n / ln n numbers.
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Ω(n / log n)}
prereqs: [prime-number]
see_also: [sieve-of-eratosthenes, linear-sieve, segmented-sieve, sieve-of-atkin, sieve-of-sundaram, primes-in-range, prime-counting-function, smallest-prime-factor-table]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.2, Sieving (the sieve of Eratosthenes, its cost, and the segmented form)
  - paper: doi:10.1090/S0025-5718-03-01501-1
    title: A. O. L. Atkin and D. J. Bernstein, Prime sieves using binary quadratic forms, Mathematics of Computation 73(246), 2004
    locator: Section 1 (the operation and memory bounds of the earlier sieves, including Pritchard's), and Section 5, Asymptotic performance
  - paper: doi:10.1145/358527.358540
    title: Paul Pritchard, A sublinear additive sieve for finding prime numbers, Communications of the ACM 24(1), 1981
    locator: pages 18 to 23 (the wheel sieve with O(n / log log n) additions)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Chapter 1 (the sieve of Eratosthenes and Theorem 7, the order of magnitude of pi(x)) and Chapter 22 (the proof of Theorem 7)
  - url: https://arxiv.org/abs/2606.22851
    title: David Harvey, Faster enumeration of primes, arXiv preprint 2606.22851, 2026
    locator: Abstract (the bit-operation bounds in the multitape Turing model)
---

Listing the primes up to $n$ is the problem of writing out every [prime number](/prime-number/) $p \le n$, usually in increasing order. It is the job that the classic sieves do: the [sieve of Eratosthenes](/sieve-of-eratosthenes/) solves it in $O(n \log \log n)$ word operations and the [linear sieve](/linear-sieve/) in $O(n)$. The answer has $\pi(n) \sim n / \ln n$ numbers, so no method can be faster than that. Prime lists feed [trial division](/trial-division/), factor tables, and the many number theory programs that need all small primes at once.

## In plain words

You get one whole number, the bound. You must list every prime from two up to the bound. A prime is a number larger than one whose only divisors are one and itself.

Testing each number on its own works, but it repeats a lot of work. A sieve does better: it writes down all the numbers, then crosses out the multiples of each prime it finds. What is never crossed out is prime. The work then grows only a little faster than the bound itself.

The list is long. Up to one million there are 78498 primes, so about one number in thirteen is prime, and the share falls slowly as the bound grows.

## Definition

**Input.** An integer $n \ge 0$.

**Output.** The sequence $p_1 < p_2 < \cdots < p_k$ of all primes $p \le n$. So $k = \pi(n)$, the value of the [prime-counting function](/prime-counting-function/) at $n$. For $n \le 1$ the output is empty.

**Table form.** Some programs want the characteristic table instead: an array $T[0 \ldots n]$ with $T[m] = 1$ when $m$ is prime and $T[m] = 0$ otherwise. One pass over $T$ turns it into the list, and the list turns into $T$ in $O(n)$ time, so the two forms differ by $O(n)$ work.

**Cost model.** The usual model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ binary digits: addition, comparison, multiplication, division and array access on numbers up to $n$ cost one step each. Memory is counted in words, or in single-digit cells for a table of flags. The output list is not counted as working memory.

## Variants

- **Primes in an interval.** List the primes in $[L, R]$ for a large $L$. This is [listing primes in an interval](/primes-in-range/), solved by the [segmented sieve](/segmented-sieve/).
- **Counting only.** Return $\pi(n)$ and not the list. This is the [prime-counting function](/prime-counting-function/), which methods such as the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) compute far faster than any listing.
- **Factor information.** Return the smallest prime factor of every $m \le n$, which is the [smallest prime factor table](/smallest-prime-factor-table/). It contains the prime list as the fixed points $\mathrm{spf}(m) = m$.
- **Unbounded generation.** Produce the primes one at a time, with no bound given in advance. Incremental sieves keep a priority queue of the next multiple of each prime found so far; O'Neill's paper on the "genuine" sieve describes this form.
- **Small memory.** List the primes up to $n$ with $o(n)$ working memory. A segmented sieve needs $O(\sqrt n)$ words.

## Examples

| $n$ | output | $\pi(n)$ |
|---|---|---|
| 0 | empty | 0 |
| 1 | empty | 0 |
| 2 | 2 | 1 |
| 10 | 2, 3, 5, 7 | 4 |
| 30 | 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 | 10 |
| 100 | 2, 3, 5, ..., 89, 97 | 25 |

**Non-examples.** The output 1, 2, 3, 5, 7 for $n = 10$ is wrong, because 1 is not prime. The output 2, 3, 5, 7, 9 is wrong, because $9 = 3 \cdot 3$.

**The size of the output.** The table gives $\pi(10^k)$ and the estimate $10^k / \ln 10^k$ of the prime number theorem.

| $n$ | $\pi(n)$ | $n / \ln n$ |
|---|---|---|
| $10^2$ | 25 | 21.7 |
| $10^4$ | 1229 | 1085.7 |
| $10^6$ | 78498 | 72382.4 |
| $10^8$ | 5761455 | 5428681.0 |

## Known algorithms

| algorithm | time (word operations) | working memory |
|---|---|---|
| test each $m \le n$ by [trial division](/trial-division/) | $O(n^{3/2})$ | $O(1)$ words |
| [sieve of Eratosthenes](/sieve-of-eratosthenes/) | $\Theta(n \log \log n)$ | $n + 1$ flags |
| [sieve of Sundaram](/sieve-of-sundaram/) | $\Theta(n \log n)$ | about $n/2$ flags |
| [linear sieve](/linear-sieve/) | $\Theta(n)$ | $n + 1$ words |
| [segmented sieve](/segmented-sieve/) | $O(n \log \log n)$ | $O(\sqrt n)$ words |
| [sieve of Atkin](/sieve-of-atkin/), basic form | $O(n)$ | $n + 1$ flags |
| Atkin and Bernstein, with a growing wheel | $O(n / \log \log n)$ | $n^{1/2 + o(1)}$ |
| Pritchard's wheel sieve | $O(n / \log \log n)$ additions | $n^{1 + o(1)}$ |

All bounds in the table are proved, and none depends on a conjecture. The bound for trial division takes at most $\sqrt m$ trial divisors for each $m$, and $\sum_{m \le n} \sqrt m = O(n^{3/2})$.

## Bounds

**Lower bound.** An algorithm that outputs the list writes $\pi(n)$ numbers, so it takes $\Omega(\pi(n))$ steps. Chebyshev proved that $\pi(n)$ has order $n / \log n$ (Hardy and Wright, Theorem 7), so the lower bound is $\Omega(n / \log n)$, with no conjecture needed. The prime number theorem sharpens this to $\pi(n) \sim n / \ln n$.

**Upper bound.** The best word-RAM bounds in the literature are $O(n / \log \log n)$ operations: Pritchard's wheel sieve reaches it with memory $n^{1 + o(1)}$, and the sieve of Atkin and Bernstein reaches it with memory $n^{1/2 + o(1)}$. So a factor of about $\log n / \log \log n$ separates the two bounds.

**Bit complexity.** In a model that charges every operation on single binary digits, such as the multitape Turing machine, the bounds above change. A 2026 preprint by Harvey describes algorithms in that model; the fastest uses $n (\log \log n)^{1 + o(1)}$ bit operations but is not fully rigorous, and there are slower rigorous randomized and deterministic versions. The preprint is not yet refereed.

## Reductions

- **To the table form and back** in $O(n)$ time, as in the definition.
- **From counting.** Each listing algorithm gives $\pi(n)$ by counting its output. The converse fails: $\pi(n)$ can be computed in $O(n^{2/3})$ time, which is less than the size of the list.
- **To an interval.** Listing the primes up to $n$ is the case $L = 2$, $R = n$ of [listing primes in an interval](/primes-in-range/).

## Applications

- A list of the primes up to $\sqrt N$ makes [trial division](/trial-division/) of $N$ divide only by primes.
- The factor bases of the [quadratic sieve](/quadratic-sieve/) and of other factoring methods are lists of small primes.
- Prime lists are the first step of the [segmented sieve](/segmented-sieve/), of the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) and of the computation of [multiplicative functions up to n](/multiplicative-functions-up-to-n/).
- Tables of primes let one check conjectures numerically, for example on [prime gaps](/prime-gaps/).

## References
