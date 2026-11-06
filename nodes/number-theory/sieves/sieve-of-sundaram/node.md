---
tag: KQBYRB
kind: algorithm
slug: sieve-of-sundaram
name: Sieve of Sundaram
aliases:
- Sundaram sieve
- Sundaram's sieve
area: number-theory/sieves
level: intro
summary: List the primes up to n by crossing out each x = i + j + 2ij with 1 <= i <= j. The numbers 2x + 1 left are the odd primes. It takes Θ(n log n) word operations and about n/2 flags.
solves: [primes-up-to-n]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [sieve-of-eratosthenes]
see_also: [sieve-of-eratosthenes, primes-up-to-n, linear-sieve, sieve-of-atkin, harmonic-series, prime-number]
sources:
  - paper: "V. Ramaswami Aiyar, Sundaram's Sieve for Prime Numbers, The Mathematics Student 2(2), 1934"
    locator: page 73
  - book: isbn:9780486257785
    title: C. Stanley Ogilvy and John T. Anderson, Excursions in Number Theory, Dover, 1988
    locator: pages 98 to 100 (Sundaram's sieve, as a table of arithmetic progressions)
  - url: https://en.wikipedia.org/wiki/Sieve_of_Sundaram
    title: Sieve of Sundaram, Wikipedia
    locator: Sections Algorithm and Correctness
---

The sieve of Sundaram lists the primes up to $n$ by crossing out every number of the form $x = i + j + 2ij$ with $1 \le i \le j$ in the range $1 \ldots k$, where $k = \lfloor (n-1)/2 \rfloor$. The numbers $2x + 1$ that are not crossed out are exactly the odd primes up to $n$, because $2(i + j + 2ij) + 1 = (2i+1)(2j+1)$. It solves [listing primes up to n](/primes-up-to-n/) in $\Theta(n \log n)$ word operations, which is slower than the [sieve of Eratosthenes](/sieve-of-eratosthenes/). Its interest is its short proof and its link to the odd form of that sieve.

## In plain words

Work with half the numbers: each slot stands for one odd number, and slot number five stands for eleven, twice five plus one. A slot is crossed out when its odd number is a product of two odd numbers that are both at least three.

The method never asks which numbers are prime. For each odd number it crosses out the products with that number and all larger odd numbers. At the end, the odd numbers left are the odd primes, and two is added by hand.

The price is wasted work: it also crosses out the products of numbers that are not prime, such as nine times eleven, which the round of three already removed.

## The problem

The input is an integer $n \ge 0$, and the output is the increasing list of all primes $p \le n$: the problem of [listing primes up to n](/primes-up-to-n/). The cost model is the [word RAM](/word-ram/), where arithmetic, comparisons and array access on numbers up to $n$ take one step. Memory is counted in flags.

## The algorithm

The slot $x$ stands for the odd number $2x + 1$. With $k = \lfloor (n-1)/2 \rfloor$, the slots $1 \ldots k$ stand for $3, 5, \ldots$ up to the largest odd number at most $n$.

```pseudo id=main
SUNDARAM(n)                                ▷ returns the primes p ≤ n
L1  if n < 2 then return the empty list
L2  k ← ⌊(n − 1) / 2⌋
L3  M[1 .. k] ← false                      ▷ M[x] true: 2x + 1 is composite
L4  i ← 1
L5  while 2i + 2i · i ≤ k do               ▷ the smallest x for this i, at j = i
L6      j ← i
L7      while i + j + 2i · j ≤ k do
L8          M[i + j + 2i · j] ← true       ▷ 2x + 1 = (2i + 1)(2j + 1)
L9          j ← j + 1
L10     i ← i + 1
L11 return 2, then 2x + 1 for each x in 1 .. k with M[x] = false
```

For a fixed $i$, the slots $i + j + 2ij$ for $j = i, i+1, \ldots$ form an arithmetic progression with step $2i + 1$. They stand for the odd multiples $(2i+1)^2, (2i+1)(2i+3), \ldots$ of $2i + 1$. So the round of $i$ is the round of $p = 2i + 1$ in the odd-only [sieve of Eratosthenes](/sieve-of-eratosthenes/), done for every odd $p$ and not only for the primes.

## Example

Take $n = 30$, so $k = 14$ and the slots $1 \ldots 14$ stand for $3, 5, \ldots, 29$.

| $i$ | slots $x = i + j + 2ij$ for $j \ge i$ | odd numbers $2x + 1$ |
|---|---|---|
| 1 | 4, 7, 10, 13 | 9, 15, 21, 27 |
| 2 | 12 | 25 |
| 3 | none, since $3 + 3 + 18 = 24 > 14$ | none |

At $i = 3$ the test of line L5 fails, since $6 + 18 = 24 > 14$. The slots left are 1, 2, 3, 5, 6, 8, 9, 11 and 14, which stand for 3, 5, 7, 11, 13, 17, 19, 23 and 29. With 2 in front, line L11 returns the ten primes up to 30.

## Correctness

The key identity is $2(i + j + 2ij) + 1 = 4ij + 2i + 2j + 1 = (2i+1)(2j+1)$. An odd number $m \ge 3$ is composite exactly when $m = ab$ with odd $3 \le a \le b$, that is, $a = 2i + 1$ and $b = 2j + 1$ with $1 \le i \le j$. So the slot $x$ is crossed out exactly when $2x + 1$ is an odd composite. Every prime other than 2 is odd, so line L11 returns all primes up to $n$ and nothing else. The loop bounds lose no pair: if $i + j + 2ij \le k$ with $i \le j$, then $2i + 2i^2 \le i + j + 2ij \le k$, so line L5 lets $i$ through. The full proof is below.

## Complexity

The round of $i$ marks the slots for $j = i, \ldots, \lfloor (k - i)/(2i + 1) \rfloor$, and it runs for $i \le I$ with $2I + 2I^2 \le k$, so $I \approx \sqrt{k/2}$. The number of writes is

$$W(n) = \sum_{i = 1}^{I} \left( \left\lfloor \frac{k - i}{2i + 1} \right\rfloor - i + 1 \right) = \frac{k}{2} \ln I + O(k) = \frac{k}{4} \ln k + O(k),$$

by the [harmonic series](/harmonic-series/) $\sum_{i \le I} 1/(2i+1) = \frac12 \ln I + O(1)$ and $\sum_{i \le I} i = O(k)$. With $k \approx n/2$ this is $\Theta(n \log n)$, and both bounds are proved.

- **Time.** $\Theta(n \log n)$ word operations. The sieve of Eratosthenes needs only $\Theta(n \log \log n)$, because it skips the rounds of the composite numbers.
- **Memory.** $k \approx n/2$ flags, so $\Theta(n)$, plus the output.

| $n$ | $k$ | writes of line L8 | $(k/4) \ln k$ |
|---|---|---|---|
| 30 | 14 | 5 | 9 |
| $10^4$ | 4999 | 8463 | 10644 |
| $10^6$ | 499999 | 1419797 | 1640292 |

## Properties

- **No primality test inside.** The marking loops never read the table; only line L11 does. So the two loops can run in any order.
- **Odd numbers only.** The table covers only odd numbers, so it is half the size of a full table.
- **Repeated marks.** A slot is written once for each way to write its odd number as $(2i+1)(2j+1)$ with $i \le j$. So 45 is marked twice, as $3 \cdot 15$ and $5 \cdot 9$.

## Variants and improvements

- **Skip composite rounds.** Run the round of $i$ only when $M[i]$ is false, that is, when $2i + 1$ is prime. The rounds of line L5 go in increasing $i$, and the slot $i$ is settled before its round, since each pair that crosses it out has a smaller first index. This turns the method into the odd-only sieve of Eratosthenes, with $\Theta(n \log \log n)$ time.
- **A two-dimensional table.** Sundaram's own form is a symmetric table whose entry in row $i$ and column $j$ is $i + j + 2ij$, so row $i$ is the progression $3i + 1, 5i + 2, 7i + 3, \ldots$ with step $2i + 1$. Ogilvy and Anderson give it in this form, with all $j \ge 1$, which marks each slot twice as often.
- **Other forms.** Similar sieves exist for numbers in other residue classes, using the factorization of the class. The [sieve of Atkin](/sieve-of-atkin/) is a sieve of a different kind, based on quadratic forms.

## When to use it

Use it to teach why sieving works, or as a short exercise in proving a program. For real prime tables, the [sieve of Eratosthenes](/sieve-of-eratosthenes/) on odd numbers is faster by a factor of about $\log n / \log \log n$ and is just as simple. The [linear sieve](/linear-sieve/) is the choice when factor information is also needed.

## Pitfalls

- **The bound $k$.** Use $k = \lfloor (n-1)/2 \rfloor$, so that $2k + 1 \le n$. The often seen $k = \lfloor n/2 \rfloor$ can return $n + 1$ when $n$ is even and $n + 1$ is prime.
- **Forgetting 2.** The sieve finds only odd primes; the prime 2 must be added for $n \ge 2$.
- **Starting $j$ at 1.** Letting $j$ run from 1 in each round is correct but marks every slot twice, once as $(i, j)$ and once as $(j, i)$.

## Implementations

## History

The sieve is credited to S. P. Sundaram, a student from India, and was published in a note by V. Ramaswami Aiyar in *The Mathematics Student* in 1934. Ogilvy and Anderson brought it to a wider public in their book on number theory.

## References
