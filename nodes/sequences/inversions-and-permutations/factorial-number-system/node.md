---
tag: J2RCN6
kind: concept
slug: factorial-number-system
name: Factorial number system
aliases:
- factoradic
- factorial base
area: sequences/inversions-and-permutations
level: core
summary: Mixed-radix number system with bases 2, 3, ..., n; it indexes permutations.
prereqs: [positional-number-system]
see_also: [lehmer-code, permutation-rank-unrank, inversion-table, lexicographic-successor, combinatorial-number-system, radix-conversion, binary-counter-increment, random-permutation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.1 (positional number systems and mixed-radix notation, including the factorial number system)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (permutations generated from mixed-radix numbers)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversion tables as the digits of a mixed-radix number)
---

The factorial number system writes a nonnegative integer as $N = d_{n-1}(n-1)! + \cdots + d_2 \cdot 2! + d_1 \cdot 1!$, where the digit $d_k$ of weight $k!$ lies between $0$ and $k$. It is the [positional number system](/positional-number-system/) with mixed radices $2, 3, 4, \ldots$, read from the right. Every integer from $0$ to $n! - 1$ has exactly one such representation, with $n - 1$ digits, and the digits are the [Lehmer code](/lehmer-code/) of the permutation of [rank](/permutation-rank-unrank/) $N$. So the system is the bridge between the integers below $n!$ and the permutations of $n$ items.

## In plain words

In ordinary decimal, every digit runs from 0 to 9, and each place is worth ten times the place to its right. In the factorial system, the places have different sizes. The rightmost place is worth 1 and holds 0 or 1. The next is worth 2 and holds 0, 1 or 2. The next is worth 6 and holds 0 to 3, then 24 with 0 to 4, and so on: the place worth $k$ factorial holds 0 up to $k$.

When a place is full and you add one more, it goes back to 0 and the place to its left goes up, exactly as 9 rolls over to 0 in decimal. Counting from 0 in this system lists the digit strings in order, and each string names one arrangement of a set of items.

## The idea

**Definition.** A factorial-base representation of $N \ge 0$ is a digit sequence $d_{m} \cdots d_2 d_1$ with
$$N = \sum_{k=1}^{m} d_k \, k!, \qquad 0 \le d_k \le k.$$
This is the mixed-radix system in which the place of weight $k!$ has radix $k + 1$, since $(k+1) \cdot k! = (k+1)!$ is the weight of the next place. A digit $d_0$ of weight $0! = 1$ with radix 1 is often added at the right, always 0, so that a permutation of $n$ items gets exactly $n$ digits.

**The largest value.** With digits $d_1, \ldots, d_{n-1}$ all at their maxima,
$$\sum_{k=1}^{n-1} k \cdot k! = \sum_{k=1}^{n-1} \big((k+1)! - k!\big) = n! - 1,$$
by telescoping.

**Theorem.** Every integer $0 \le N < n!$ has exactly one representation with digits $d_1, \ldots, d_{n-1}$.

*Proof.* There are $2 \cdot 3 \cdots n = n!$ digit sequences, and each gives a value between $0$ and $n! - 1$ by the bound above. So it is enough to show that two different sequences give different values. Let $k$ be the highest place where $d$ and $d'$ differ, say $d_k > d'_k$. The places above $k$ agree, place $k$ contributes at least $k!$ more to the first value, and the places below $k$ can make up at most $\sum_{i<k} i \cdot i! = k! - 1$. So the first value is larger. $\square$

**Conversion.** Like any positional system, the digits come from repeated division, here by $2, 3, 4, \ldots$ in turn:

```pseudo
TO-FACTORIAL-BASE(N)
1  k ← 1
2  while N > 0 do
3      d[k] ← N mod (k + 1)
4      N ← ⌊N / (k + 1)⌋
5      k ← k + 1
6  return d[1 .. k − 1]
```

At step $k$, $N$ holds $\lfloor N_0 / k! \rfloor$, and its remainder modulo $k + 1$ is the digit of weight $k!$. The reverse conversion is Horner's rule: start with $x = d_{n-1}$ and, for $k = n - 2$ down to $1$, set $x \leftarrow (k + 1)\,x + d_k$. Both take $O(n)$ arithmetic operations on numbers up to $n!$, which have about $n \lg n$ bits, so they are [big-integer](/big-integer/) operations for $n$ above 20 on a 64-bit machine. See [radix conversion](/radix-conversion/).

**Counting.** Adding 1 changes the trailing digits that are at their maxima, $d_k = k$, to 0 and raises the next digit. Over the count from $0$ to $n! - 1$, a digit $d_k$ rolls over once every $(k+1)!$ steps, so the average number of carries per step is less than $\sum_{k \ge 2} 1/k! = e - 2 \approx 0.718$. As with the [binary counter](/binary-counter-increment/), the increment takes $O(1)$ amortized time.

**Permutations.** For a permutation $a$ of $[n]$ with Lehmer code $c_1, \ldots, c_n$, where $c_i$ is the number of smaller items to the right of position $i$ and $0 \le c_i \le n - i$, set $d_{n-i} = c_i$. Then
$$N = \sum_{i=1}^{n} c_i\,(n-i)!$$
is the position of $a$ in lexicographic order, counted from 0. So the factorial-base digits of $N$, read from the left, are the Lehmer code of the $N$-th permutation, and incrementing $N$ is taking the [lexicographic successor](/lexicographic-successor/). The [inversion table](/inversion-table/) gives another such numbering, indexed by values.

**Fractions.** A real number in $[0, 1)$ can be written as $\sum_{k \ge 2} e_k / k!$ with $0 \le e_k \le k - 1$. Every rational number $p/q$ has a finite expansion of this kind, because $p/q = p\,(q-1)!/q!$ and the numerator can be expanded in the system above. The number $e - 2 = \sum_{k \ge 2} 1/k!$ has all digits equal to 1. That expansion is infinite and its digits are not eventually maximal, so it is not the expansion of a rational number, and $e$ is irrational.

## Examples

**Converting 51.** $51 = 25 \cdot 2 + 1$, $25 = 8 \cdot 3 + 1$, $8 = 2 \cdot 4 + 0$, $2 = 0 \cdot 5 + 2$, so the digits are $d_4 d_3 d_2 d_1 = 2\,0\,1\,1$:
$$51 = 2 \cdot 4! + 0 \cdot 3! + 1 \cdot 2! + 1 \cdot 1! = 48 + 0 + 2 + 1.$$
With the trailing digit $d_0 = 0$ this is $2\,0\,1\,1\,0$, the Lehmer code of $3\,1\,4\,5\,2$, the permutation of rank 51 among the 120 permutations of $[5]$.

**Converting 1000.** Dividing by $2, 3, 4, 5, 6, 7$ leaves the remainders $0, 2, 2, 1, 2, 1$, so $1000 = 1\,2\,1\,2\,2\,0$ in the factorial base: $720 + 240 + 24 + 12 + 4 + 0$.

**The largest numbers.** $719 = 6! - 1$ is $5\,4\,3\,2\,1$, and $5039 = 7! - 1$ is $6\,5\,4\,3\,2\,1$. These are the codes of the reversals $6\,5\,4\,3\,2\,1$ and $7\,6 \cdots 1$.

**Counting to 5.** The integers $0, \ldots, 5$ are $00, 01, 10, 11, 20, 21$, with digits $d_2 d_1$. Each is the Lehmer code, without its final 0, of $123, 132, 213, 231, 312, 321$.

## Where it is used

- **[Ranking and unranking permutations](/permutation-rank-unrank/).** The conversion between $N$ and its digits, together with the Lehmer code, maps the integers below $n!$ to permutations and back.
- **Random permutations.** One uniform integer below $n!$, converted to the factorial base and decoded, gives a uniform [random permutation](/random-permutation/). The digit $d_k$ is uniform on $\{0, \ldots, k\}$, which is the choice that the Fisher-Yates shuffle makes at each step.
- **Storing a permutation as a number.** A permutation of $n$ items fits in $\lceil \lg n! \rceil$ bits as its rank, the information-theoretic minimum, against $n \lceil \lg n \rceil$ bits for the plain list.
- **Indexing tables by permutations.** Puzzle solvers and pattern databases store one entry per permutation in an array indexed by the rank.
- **A sister system for subsets.** The [combinatorial number system](/combinatorial-number-system/) plays the same role for $k$-subsets, with binomial coefficients in place of factorials.

## References
