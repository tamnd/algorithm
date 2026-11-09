---
tag: 6ZVXYP
kind: definition
slug: balanced-gray-code
name: Balanced Gray code
aliases:
- Bhat-Savage balanced Gray code
- uniform Gray code
- balanced transition counts
area: combinatorics/gray-codes
level: advanced
summary: A cyclic Gray code in which every bit position changes as close to equally often as possible.
prereqs: [cyclic-gray-code, ruler-sequence]
see_also: [binary-reflected-gray-code, hypercube-hamiltonian-cycle, gray-code, gray-code-generation, hamming-distance, minimal-change-ordering]
sources:
  - paper: doi:10.37236/1249
    title: Girish S. Bhat and Carla D. Savage, Balanced Gray codes, Electronic Journal of Combinatorics 3(1), Research Paper 25, 1996
    locator: the definition by transition counts and the construction of balanced codes for every n
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 3.2 (transition counts, the history from Bakos and Tootill to Wagner and West and Bhat and Savage, exponentially balanced codes, and prescribed transition counts)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (balanced Gray cycles and a short general construction)
---

A balanced Gray code is a [cyclic Gray code](/cyclic-gray-code/) on $n$ bits in which each bit position changes as nearly the same number of times as possible, about $2^n / n$ times around the cycle. The [binary reflected Gray code](/binary-reflected-gray-code/) is far from balanced: bit 0 changes $2^{n-1}$ times and the top bit only twice. Balanced codes exist for every $n$, by Bhat and Savage (1996) after earlier work for powers of 2. They matter when each bit drives a physical part, because no part then takes most of the switching.

## Definition

Let $n \ge 1$ and $N = 2^n$, and let $v_0, v_1, \ldots, v_{N-1}$ be a cyclic Gray code of $\{0,1\}^n$. Bits are numbered $0$ to $n - 1$ from the right. The *cyclic delta sequence* $\delta_1, \ldots, \delta_N$ gives the bit changed at each of the $N$ steps, the wrap step from $v_{N-1}$ to $v_0$ included. The *transition count* of bit $j$ is

$$c_j = \bigl|\{\, i : \delta_i = j \,\}\bigr|, \qquad 0 \le j < n.$$

Each $c_j$ is even, because the cycle returns to its start and so flips each bit an even number of times. The counts add up to $N$, one per step.

The code is *balanced* when

$$\left| c_j - \frac{2^n}{n} \right| < 2 \quad \text{for every } j.$$

Since each $c_j$ is even, this says that each $c_j$ is $2\lfloor 2^{n-1}/n \rfloor$ or $2\lceil 2^{n-1}/n \rceil$, so any two counts differ by at most 2. When $n$ is a power of 2, $2^n / n$ is an even integer, and a balanced code has $c_0 = \cdots = c_{n-1} = 2^n / n$. Some authors call that case *uniform* or *totally balanced*.

**Necessary conditions for any counts.** Sort the counts so that $c'_1 \le c'_2 \le \cdots \le c'_n$. Then each count is even, they sum to $2^n$, and

$$c'_1 + \cdots + c'_k \ge 2^k \quad \text{for } 1 \le k \le n.$$

*Proof of the last condition.* Let $K$ be the set of $k$ bit positions with the smallest counts. Keep only the bits in $K$ of each $v_i$. The result is a closed walk in $Q_k$ in which a step either stays put, when the changed bit is outside $K$, or moves along an edge, when it is in $K$. Every string of $\{0,1\}^k$ appears in the walk, since every string of $\{0,1\}^n$ appears in the code. A closed walk that visits $2^k$ distinct vertices makes at least $2^k$ moves, and the number of moves is $\sum_{j \in K} c_j$. $\square$

Whether every list of counts that meets these conditions is the count list of some cyclic Gray code is open in general (Mütze, Section 3.2). For the balanced counts the answer is yes.

**Existence.** For every $n \ge 1$ a balanced Gray code exists. Wagner and West (1991) proved this when $n$ is a power of 2, and Bhat and Savage (1996) proved it for all $n$. Mütze reports that Tibor Bakos had a construction about 1955, published in a book by Ádám in 1968, which was later forgotten. Knuth gives a short general construction in Section 7.2.1.1.

## Examples and non-examples

- **The reflected code is not balanced for $n \ge 4$.** Its counts are $c_j = 2^{n-1-j}$ for $j < n - 1$ and $c_{n-1} = 2$. A script gave $(8, 4, 2, 2)$ for $n = 4$ and $(16, 8, 4, 2, 2)$ for $n = 5$, listed from bit 0. For $n = 4$ a balanced code needs all counts equal to 4.
- **Small $n$.** For $n = 1, 2, 3$ the reflected code is balanced. Its counts are $(2)$, $(2, 2)$ and $(4, 2, 2)$, and for $n = 3$ the allowed counts are $2$ and $4$, since $8/3 \approx 2.67$.
- **A balanced code for $n = 4$.** 0000, 0001, 0011, 0010, 0110, 0111, 1111, 1011, 1001, 1101, 0101, 0100, 1100, 1110, 1010, 1000, then back to 0000. Its cyclic delta sequence is 0, 1, 0, 2, 0, 3, 2, 1, 2, 3, 0, 3, 1, 2, 1, 3, and each bit appears 4 times.
- **A balanced code for $n = 5$.** Here $32/5 = 6.4$, so each count must be 6 or 8, and the sum 32 forces four 6s and one 8. A backtracking search with a cap on each count found the cycle with delta sequence 0, 1, 0, 2, 0, 1, 0, 3, 0, 4, 1, 4, 2, 4, 3, 2, 1, 2, 3, 4, 0, 4, 2, 3, 1, 3, 4, 2, 4, 3, 1, 4, which starts at 00000 and has counts $(6, 6, 6, 6, 8)$.
- **Non-example: the wrap step left out.** An open list such as the first 15 strings of the $n = 4$ example above has no wrap step, and its counts $(4, 4, 4, 3)$ are not all even. Balance is defined on the cycle, so an open Gray code is neither balanced nor unbalanced under this definition.
- **Non-example: possible but unbalanced counts.** A search found the cyclic 4-bit code 0000, 0001, 0011, 0010, 0110, 0111, 0101, 0100, 1100, 1110, 1111, 1101, 1001, 1011, 1010, 1000 with counts $(6, 6, 2, 2)$. These counts meet the necessary conditions, but the code is not balanced, since 6 and 2 are both 2 or more away from $16/4 = 4$.

## Related definitions

- **[Ruler sequence](/ruler-sequence/).** The delta sequence of the reflected code, the most unbalanced natural case.
- **Exponentially balanced Gray code.** Each $c_j$ is one of two consecutive powers of 2. For $n$ a power of 2 this is the same as balanced. Van Zanten and Suparta (2004) constructed such codes for all $n$ (Mütze, Section 3.2).
- **Prescribed transition counts.** The general question: given even $c_0, \ldots, c_{n-1}$ that meet the conditions above, find a cyclic code with exactly these counts.
- **[Hamiltonian cycle in the hypercube](/hypercube-hamiltonian-cycle/).** A balanced Gray code is a Hamiltonian cycle of $Q_n$ that uses about the same number of edges in each of the $n$ directions.
- **[Minimal change ordering](/minimal-change-ordering/).** Balance makes sense for other Gray codes too, for example a list of $k$-subsets in which each transposition is used about equally often.

## References
