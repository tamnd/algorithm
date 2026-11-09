---
tag: RACQ8D
kind: algorithm
slug: pascal-triangle-dp
name: Pascal's triangle dynamic programming
aliases:
- Pascal's triangle recurrence
- Pascal's rule DP
- binomial coefficient table
area: combinatorics/counting-algorithms
level: intro
summary: Fills a table using C(n,k) = C(n-1,k-1) + C(n-1,k).
solves: [binomial-coefficient-computation]
model: word-ram
complexity:
  vars: {n: the upper index, k: the lower index after symmetry, w: the word size in bits}
  time: {worst: Θ(n*k), best: Θ(1)}
  space: {extra: Θ(k)}
properties: {deterministic: true, recursive: false}
prereqs: [binomial-coefficient, memoization]
see_also: [binomial-coefficient-computation, tabulation, dp-on-dag, counting-lattice-paths, lucas-theorem, combinatorial-number-system, hockey-stick-identity, binomial-theorem]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.6, Binomial Coefficients (the table of Pascal's triangle, the addition formula, and historical notes)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 5.1, Basic identities (the table of Pascal's triangle and the addition formula)
  - paper: doi:10.1145/820127.820168
    title: Yannis Manolopoulos, Binomial coefficient computation, recursion or iteration?, ACM SIGCSE Bulletin 34(4), 65 to 67 (2002)
    locator: the comparison of the plain recursion, the table method and the product formula
---

Pascal's triangle dynamic programming computes the [binomial coefficient](/binomial-coefficient/) $\binom{n}{k}$ by filling the rows of Pascal's triangle with Pascal's rule $\binom{i}{j} = \binom{i-1}{j-1} + \binom{i-1}{j}$, from $\binom{0}{0} = 1$. Keeping one row of $k + 1$ entries and updating it from right to left, it uses $nk - k(k-1)/2$ additions and $\Theta(k)$ words of space. It needs only additions, so it works modulo any number $m$, prime or not, where the factorial formula needs inverses. It also gives every $\binom{i}{j}$ with $i \le n$ and $j \le k$ on the way, which is what a table for [ranking](/combinatorial-number-system/) or for a counting [DP](/dp-on-dag/) needs.

## In plain words

Write a one at the top of a triangle. Each new row starts and ends with one, and each number inside a row is the sum of the two numbers just above it. Row ten, position three, of this triangle is the number of ways to choose three things from ten.

The method builds the rows one after another, and only keeps the current row. To compute the next row in the same place, it goes from right to left, so that it still has the old value on the left when it needs it. It only adds, never multiplies or divides, so the numbers can be kept as remainders after division by any fixed number, which keeps them small.

## The problem

Notation: $n \ge 0$ and $k$ are integers, $\binom{n}{k}$ or $C(n, k)$ is the number of $k$-subsets of $[n] = \{1, \ldots, n\}$, with $\binom{n}{k} = 0$ for $k < 0$ or $k > n$, and $m \ge 1$ is a modulus or $m = \infty$ for exact arithmetic, where "$x \bmod \infty$" means $x$. The task is to output $\binom{n}{k} \bmod m$. This is one case of [computing binomial coefficients](/binomial-coefficient-computation/).

Cost model: on the [word RAM](/word-ram/) with $m < 2^{w-1}$, each addition and reduction modulo $m$ costs $O(1)$. In exact arithmetic the entries are big integers: an entry $\binom{i}{j}$ has at most $i$ bits, and adding two numbers of $b$ bits costs $O(b/w + 1)$ word operations.

## The algorithm

```pseudo id=main
PASCAL-TRIANGLE-DP(n, k, m)
L1  if k < 0 or k > n then return 0
L2  k ← min(k, n − k)                      ▷ symmetry
L3  let R[0 .. k] be a new array of zeros
L4  R[0] ← 1 mod m                         ▷ row 0 of the triangle
L5  for i ← 1 to n do
L6      for j ← min(i, k) downto 1 do      ▷ right to left
L7          R[j] ← (R[j] + R[j − 1]) mod m
L8  return R[k]
```

After the iteration for $i$ of line L5, $R[j] = \binom{i}{j} \bmod m$ for $0 \le j \le k$. Line L7 reads $R[j-1]$ before line L7 changes it for $j - 1$, because $j$ goes down, so $R[j-1]$ still holds the value of row $i - 1$. Entries $R[j]$ with $j > i$ stay $0 = \binom{i}{j}$ and are not touched. $R[0] = 1$ for every row and is not touched either.

**Full table.** To get the whole triangle up to row $n$, keep all rows: $T[i][0] = T[i][i] = 1$ and $T[i][j] = T[i-1][j-1] + T[i-1][j]$ for $0 < j < i$. This takes $\Theta(n^2)$ additions and space and answers each later query $\binom{i}{j}$ with $i \le n$ in $O(1)$.

## Example

Compute $\binom{6}{3}$ exactly. Line L2 keeps $k = 3$. The row $R[0 \ldots 3]$ after each iteration of line L5:

| $i$ | $j$ updated (in order) | $R[0]$ | $R[1]$ | $R[2]$ | $R[3]$ |
|---|---|---|---|---|---|
| 0 (start) | none | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 |
| 2 | 2, 1 | 1 | 2 | 1 | 0 |
| 3 | 3, 2, 1 | 1 | 3 | 3 | 1 |
| 4 | 3, 2, 1 | 1 | 4 | 6 | 4 |
| 5 | 3, 2, 1 | 1 | 5 | 10 | 10 |
| 6 | 3, 2, 1 | 1 | 6 | 15 | 20 |

The answer is $R[3] = 20$, after $1 + 2 + 3 + 3 + 3 + 3 = 15$ additions. In row 4 the order matters: $R[3] \leftarrow 1 + 3 = 4$ uses the old $R[2] = 3$, and only then $R[2] \leftarrow 3 + 3 = 6$. Left to right, $R[2]$ would become 6 first and $R[3]$ would get $1 + 6 = 7$, which is wrong.

With $m = 7$, the same steps give $20 \bmod 7 = 6$. With $m = 10^9$, which is not prime, $\binom{100}{50} \bmod 10^9 = 812497256$, the last nine digits of $100891344545564193334812497256$, after $3775$ additions of residues.

## Correctness

Line L1 returns the right value 0 outside $0 \le k \le n$. Line L2 is right by the symmetry $\binom{n}{k} = \binom{n}{n-k}$. The loop of line L5 keeps the invariant: before the iteration for $i$, $R[j] = \binom{i-1}{j} \bmod m$ for all $0 \le j \le k$. Line L4 makes it true for $i = 1$. The inner loop of line L6 keeps a second invariant: when it is about to process $j$, the entries $R[j+1 \ldots]$ hold row $i$ and $R[0 \ldots j]$ still hold row $i - 1$. So line L7 computes $\binom{i-1}{j} + \binom{i-1}{j-1} = \binom{i}{j}$ modulo $m$ by Pascal's rule, and reduction modulo $m$ commutes with addition. At the end $R[k] = \binom{n}{k} \bmod m$. The full proof is in the correctness proof below.

## Complexity

- **Additions.** Line L7 runs $\sum_{i=1}^{n} \min(i, k)$ times. For $0 \le k \le n$ this is $nk - k(k-1)/2$, which is between $nk/2$ and $nk$. With $k \le n/2$ after line L2, the time is $\Theta(nk)$ when $k \ge 1$, and $\Theta(1)$ beyond the loop overhead when $k = 0$. For $\binom{100}{50}$ it is $3775$ additions.
- **Modular cost.** With $m < 2^{w-1}$, each addition and reduction costs $O(1)$, so the time is $\Theta(nk)$ and the space is $k + 1$ words.
- **Exact cost.** The entries of row $i$ have at most $i$ bits, and by the [binomial coefficient bounds](/binomial-coefficient-bounds/) the middle ones have $\Theta(i)$ bits. So the exact version costs $O(n^2 k / w)$ word operations, which is $\Theta(n^3/w)$ for $k = n/2$. The product formula of [computing binomial coefficients](/binomial-coefficient-computation/) costs $O(kL/w)$ with $L$ the number of bits of the answer, which is $O(n^2/w)$; so for one exact value the table method is slower by a factor of about $n$. For $n = 100$ and $k = 50$, the entries of the full table up to column 50 have $168008$ bits in total.
- **Space.** $\Theta(k)$ entries for one row, $\Theta(n^2)$ for the full triangle.
- **Plain recursion.** Without a table, the recursion $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ with base cases $\binom{n}{0} = \binom{n}{n} = 1$ makes $2\binom{n}{k} - 1$ calls, because its leaves each return 1 and it is a binary tree. For $\binom{30}{15}$ that is $310235039$ calls. [Memoization](/memoization/) or the [tabulation](/tabulation/) of this page reduces it to $O(nk)$.

## Properties

- **Division free.** Only additions are used, so the method works in any commutative ring, in particular modulo a composite $m$ or modulo a small prime $p \le n$, where $k!$ has no inverse.
- **Exact intermediate values.** Every intermediate entry is itself a binomial coefficient, at most the answer when $k \le n/2$, so the exact version never handles a number larger than the answer, and with $m$ fitting in a word nothing overflows.
- **Monotone dependency.** Entry $(i, j)$ depends only on row $i - 1$, so the computation is a [DP on a DAG](/dp-on-dag/) whose sources are $\binom{0}{0}$ and whose paths are the monotone [lattice paths](/counting-lattice-paths/): $\binom{n}{k}$ is the number of paths from the top to entry $(n, k)$.
- **Deterministic and iterative.** No recursion, no randomness.

## Variants and improvements

- **Full triangle for many queries.** Build rows $0$ to $N$ once, in $\Theta(N^2)$ time and space, and answer each query with $n \le N$ in $O(1)$. This is the usual choice for $N$ up to a few thousand and any modulus.
- **Column-limited triangle.** Keep columns $0$ to $K$ only, for $\Theta(NK)$ time and space, when queries have small $k$.
- **Other triangles.** The same row update computes the [Stirling numbers of the second kind](/stirling-numbers-second-kind/) with $S(i, j) = j S(i-1, j) + S(i-1, j-1)$, the Stirling numbers of the first kind, the Delannoy numbers and the number of lattice paths in a grid with forbidden cells.
- **A prime modulus with $p > n$.** For many queries, tables of factorials and inverse factorials take $O(n)$ time and give each query in $O(1)$; see [computing binomial coefficients](/binomial-coefficient-computation/).
- **A small prime.** [Lucas's theorem](/lucas-theorem/) reduces $\binom{n}{k} \bmod p$ to the triangle up to row $p - 1$, which this method fills in $O(p^2)$ time.
- **Parity.** Modulo 2 the triangle is the Sierpinski pattern, and a row can be updated as a bit vector with $R \leftarrow R \oplus (R \ll 1)$, $w$ entries per word operation.

## When to use it

Use it when you need many values $\binom{i}{j}$ for all $i$ up to a bound, or one value modulo a composite number or a small prime, with $nk$ small enough, for example up to about $10^8$. It is also the simplest safe method for exact values with $n \le 67$ in unsigned 64-bit integers, since no intermediate value exceeds the answer. Do not use it for one exact value with large $n$: the product formula is about $n$ times faster. Do not use it for $n$ up to $10^6$ or more modulo a prime $p > n$: factorial tables are faster.

## Pitfalls

- **Wrong direction.** Updating one row from left to right reads the new value of $R[j-1]$ and computes the wrong numbers, as the example shows. With two rows, either direction works.
- **Forgetting symmetry.** Without line L2, $\binom{n}{n-1}$ costs $\Theta(n^2)$ instead of $\Theta(n)$.
- **Overflow in exact mode.** In 64-bit unsigned arithmetic, all entries fit for $n \le 67$ and the central ones overflow from row 68 on. Reduce modulo $m$ in line L7, or use big integers.
- **Modulus 1.** Line L4 must set $R[0] = 1 \bmod m$, which is $0$ for $m = 1$; writing $1$ returns $1$ for $\binom{0}{0} \bmod 1$.
- **Index range.** Line L6 must stop at $\min(i, k)$ and not go below $j = 1$, or it reads $R[-1]$.
- **Exponential recursion.** The recursive form of Pascal's rule without memoization makes $2\binom{n}{k} - 1$ calls.

## Implementations

## History

The triangle of binomial coefficients was known long before Pascal, in Indian, Persian and Chinese mathematics; Knuth (Section 1.2.6) gives its history. Blaise Pascal's treatise on the arithmetic triangle, published in 1665, studied it systematically, and the name comes from that work. The rule that each entry is the sum of the two above it is the addition formula of Knuth's Section 1.2.6, and the table method is the standard first example of replacing an exponential recursion by a table (Manolopoulos, 2002).

## References
