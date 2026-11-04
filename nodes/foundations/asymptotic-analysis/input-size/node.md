---
tag: AE8FW3
kind: definition
slug: input-size
name: Input size
aliases:
- problem size
- size of the input
area: foundations/asymptotic-analysis
level: intro
summary: The measure n of an instance, such as the number of items or bits, against which running time is expressed.
prereqs: []
see_also: [time-complexity, worst-case-analysis, pseudo-polynomial-time, unary-encoding, word-ram, logarithmic-cost-model, multivariate-asymptotic-notation, trial-division]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (input size) and Chapter 31 (Number-Theoretic Algorithms, size of integer inputs)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 7 (Time Complexity, encodings of the input)
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 6.4 (Subset Sums and Knapsacks, pseudo-polynomial running time)
---

The size of an input is the number that an analysis uses as the argument $n$ of a cost function such as the [time complexity](/time-complexity/) $T(n)$. Formally it is the length of the encoding of the instance in bits. In practice it is a simpler measure that is polynomially related to that length, such as the number of items in an array or the number of vertices and edges of a graph. When each item fits in a machine word, it is within a constant factor of the length in words.

## Definition

Fix a finite alphabet $\Sigma$ and an encoding $e$ that maps each instance $x$ of a problem to a string $e(x) \in \Sigma^*$. The size of $x$ is the length $|e(x)|$ of this string. With $\Sigma = \{0,1\}$, the size is a number of bits. The set $I_n$ of instances of size $n$ is then finite, because there are at most $2^n$ strings of length $n$. So the maximum over $I_n$ in a [worst-case analysis](/worst-case-analysis/) always exists.

A change of the alphabet changes the size by a constant factor only. A symbol of an alphabet with $k \ge 2$ symbols fits in $\lceil \lg k \rceil$ bits, so the length in bits is at most $\lceil \lg k \rceil$ times the length in symbols. Conversely, a symbol can carry $\lfloor \lg k \rfloor \ge 1$ bits, so the length in symbols is at most the length in bits divided by $\lfloor \lg k \rfloor$, rounded up. The usual rule is to accept any encoding in which the lengths are polynomially related to the binary length and in which one can convert between encodings in polynomial time. Under this rule, the class of problems solvable in polynomial time does not depend on the choice. This rule does not allow the unary encoding of numbers, as the next section shows.

### Integers: bits, not value

A positive integer $N$ has $\lfloor \lg N \rfloor + 1$ bits in binary, and $N$ symbols in [unary](/unary-encoding/). If $b$ is the number of bits, then $2^{b-1} \le N < 2^b$. So the unary size is exponential in the binary size. For $N = 1000$, the binary size is 10 and the unary size is 1000. The base of a positional system matters only by a constant factor: the number of digits of $N$ in base $k$ is $\lfloor \log_k N \rfloor + 1$, and $\log_k N = \lg N / \lg k$.

### Conventions in practice

The following measures are in common use. Each is justified when the items fit in a constant number of machine words, as in the [word RAM](/word-ram/).

- An array, list or set of items: the number of items $n$.
- A graph with vertex set $V$ and edge set $E$: the two numbers $n = |V|$ and $m = |E|$. An [adjacency list](/adjacency-list/) has $n + m$ entries (or $n + 2m$ for an undirected graph), and an adjacency matrix has $n^2$ entries. The bit length of an adjacency list is larger by a factor of about $\lg n$, because each vertex name in it needs $\lceil \lg n \rceil$ bits. An adjacency matrix has exactly $n^2$ bits. See [multivariate asymptotic notation](/multivariate-asymptotic-notation/).
- A string: its length. A matrix: its dimensions, or the number of entries.
- A single integer, as in primality testing or factoring: its number of bits, $\lfloor \lg N \rfloor + 1$, and not its value $N$.
- A set of numbers whose values are not bounded by a machine word: the total number of bits, or the number of items $n$ together with the bit length $b$ of the largest. In the [logarithmic cost model](/logarithmic-cost-model/) each operation costs in proportion to the bits of its operands.

## Examples and non-examples

- **Trial division.** To factor $N$, [trial division](/trial-division/) divides $N$ by $2, 3, \ldots$ up to $\lfloor \sqrt{N} \rfloor$. It makes at most $\lfloor \sqrt{N} \rfloor - 1$ divisions. In terms of the value, this is $O(\sqrt{N})$, which looks small. In terms of the size $b = \lfloor \lg N \rfloor + 1$, it is up to $2^{b/2}$ divisions, which is exponential. For the prime $N = 2^{61} - 1$, the size is $b = 61$ bits, and the test makes $1518500248$ divisions (the divisors $2$ to $1518500249$). If the number were written in unary, the same algorithm would take a time polynomial in the size.
- **Pseudo-polynomial time.** The dynamic program for [subset sum](/subset-sum-problem/) fills a table with $n + 1$ rows and $W + 1$ columns, where $W$ is the target and $n$ is the number of items. Its time is $O(nW)$. The input has about $n \lceil \lg(W+1) \rceil$ bits or more, and $W$ can be as large as $2^{b} - 1$ for $b$ bits. So the time is polynomial in $n$ and in the value $W$, and exponential in the size. Such a bound is called [pseudo-polynomial](/pseudo-polynomial-time/). For $n = 100$ and $W = 2^{64}$ the table has more than $1.8 \times 10^{21}$ cells, although the input has fewer than $7000$ bits (for 100 items of 64 bits each plus the target).
- **Counting loops over a value.** A routine that computes the $n$th [Fibonacci number](/fibonacci-numbers/) with a loop of $n - 1$ additions makes a number of additions that is linear in the value $n$. Its input $n$ has only $\lfloor \lg n \rfloor + 1$ bits, so it makes a number of additions exponential in the size of the input. Since $F_n$ has $\Theta(n)$ bits, the loop also costs $\Theta(n^2)$ bit operations in the logarithmic cost model.
- **Items that are not of constant size.** Sorting $n$ strings of length $L$ with a comparison sort makes $\Theta(n \log n)$ comparisons, but one comparison of two equal strings reads $L$ characters. The input has $nL$ characters, and the cost of [merge sort](/merge-sort/) on strings can be $\Theta(L n \log n)$ character comparisons. The measure "$n$ items" hides $L$.
- **Not a size.** The value of a number input is a magnitude, not a size. The number of vertices alone is not the size of a graph input, since a graph on $n$ vertices can have between $0$ and $n(n-1)/2$ edges. The size must grow with the amount of data that the algorithm may read.

## Related definitions

- [Time complexity](/time-complexity/) and [space complexity](/space-complexity/) are functions of the input size.
- [Worst-case analysis](/worst-case-analysis/) and [best-case analysis](/best-case-analysis/) take the maximum or minimum over all inputs of one size.
- [Pseudo-polynomial time](/pseudo-polynomial-time/) is a bound that is polynomial in the values of the numbers of the input and in the size, and so it is exponential in the bit length in general.
- [Unary encoding](/unary-encoding/) writes the integer $N$ as $N$ symbols. A problem that is hard with binary numbers can be easy with unary numbers, and strongly hard problems stay hard in unary.
- [Multivariate asymptotic notation](/multivariate-asymptotic-notation/) handles inputs with several size parameters, such as $n$ and $m$.
- The [word RAM](/word-ram/) and the [logarithmic cost model](/logarithmic-cost-model/) set the cost of an operation on numbers, and so they decide when "number of items" is a fair measure.

## References
