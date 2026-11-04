---
tag: Q7GMPG
kind: problem
slug: binary-counter-increment
name: Binary counter increment
aliases:
- k-bit binary counter
- incrementing a binary counter
area: foundations/amortized-analysis
level: intro
summary: Increment a k-bit counter; the total bit flips over n increments are O(n), so each increment is amortized O(1).
prereqs: [amortized-cost, bitwise-operations]
see_also: [aggregate-method, accounting-method, potential-method, stack-with-multipop, gray-code, binomial-heap, decomposable-searching-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.1 (incrementing a binary counter), Sections 16.2 and 16.3 (the same example with credits and with a potential)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.4, Factorial factors (the sum of the floors of n over the powers of 2 equals n minus the binary digit sum of n)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)
    locator: Chapter 9, Numerical Representations
---

The binary counter problem asks for the cost of $n$ increments of a $k$-bit counter that starts at 0, when each changed bit costs one unit. One increment can change all $k$ bits, but the total over $n$ increments is exactly $\sum_{i=0}^{k-1} \lfloor n/2^i \rfloor$, which is less than $2n$ and equals $2n - s_2(n)$ when $n < 2^k$. So each increment has [amortized cost](/amortized-cost/) at most 2. With the [stack with multipop](/stack-with-multipop/), it is the standard first example of the [aggregate method](/aggregate-method/), the [accounting method](/accounting-method/) and the [potential method](/potential-method/).

## In plain words

To add one to a binary number, you start at the right end. Each 1 that you meet becomes 0, and the first 0 that you meet becomes 1. Then you stop. If the number ends in many ones, one addition changes many digits. But such numbers are rare. The last digit changes at each step. The digit before it changes at every second step, the next one at every fourth step, and so on. Add these up and the total number of changed digits is less than two times the number of steps. So a long run of additions costs less than two changes for each addition, although one addition can change all digits.

## Definition

The state is an array $A[0 \ldots k-1]$ of bits, with $A[0]$ the lowest bit. It represents the value $x = \sum_{i=0}^{k-1} A[i]\, 2^i$. The start state is all zeros. INCREMENT adds 1 modulo $2^k$.

```pseudo id=main
INCREMENT(A, k)
L1  i ← 0
L2  while i < k and A[i] = 1 do
L3      A[i] ← 0                   ▷ reset a trailing one
L4      i ← i + 1
L5  if i < k then
L6      A[i] ← 1                   ▷ set the lowest zero
```

The cost of one INCREMENT is the number of bits that it writes, which is the number of bits that change. If the value ends in $t$ ones and $t < k$, the cost is $t + 1$. If all $k$ bits are 1, the counter wraps to 0 and the cost is $k$.

**The problem.** For $n \ge 0$, find the total cost $F_k(n)$ of $n$ increments from 0.

**Theorem.** $F_k(n) = \sum_{i=0}^{k-1} \lfloor n / 2^i \rfloor < 2n$ for $n \ge 1$. If $n < 2^k$, then $F_k(n) = 2n - s_2(n)$, where $s_2(n)$ is the number of 1 bits in the binary form of $n$.

*Proof that bit $i$ flips exactly $\lfloor n/2^i \rfloor$ times.* After $j$ increments the value is $j \bmod 2^k$. For $i < k$, the bit $i$ of $j \bmod 2^k$ is the bit $i$ of $j$, which is $\lfloor j/2^i \rfloor \bmod 2$, because $2^i$ divides $2^k$. This bit changes between $j - 1$ and $j$ if and only if $\lfloor j/2^i \rfloor \ne \lfloor (j-1)/2^i \rfloor$, that is, if and only if $2^i$ divides $j$. The number of $j$ in $1, \ldots, n$ that $2^i$ divides is $\lfloor n/2^i \rfloor$. INCREMENT writes only bits that change (lines L3 and L6 write a bit that had the other value), so the cost counts exactly these changes. Add over $i = 0, \ldots, k-1$ to get the formula for $F_k(n)$.

*Proof of $< 2n$.* $\sum_{i=0}^{k-1} \lfloor n/2^i \rfloor \le \sum_{i=0}^{k-1} n/2^i = 2n(1 - 2^{-k}) < 2n$.

*Proof of the identity.* Write $n = \sum_{j \ge 0} b_j 2^j$ with bits $b_j$. Then $\lfloor n/2^i \rfloor = \sum_{j \ge i} b_j 2^{j-i}$. Add over all $i \ge 0$ and change the order of the sums:

$$\sum_{i \ge 0} \Big\lfloor \frac{n}{2^i} \Big\rfloor = \sum_{j \ge 0} b_j \sum_{i=0}^{j} 2^{j-i} = \sum_{j \ge 0} b_j (2^{j+1} - 1) = 2n - s_2(n).$$

If $n < 2^k$, the terms with $i \ge k$ are 0, so the sum up to $k - 1$ is the full sum. $\square$

### The same bound by the three methods

The theorem is the [aggregate method](/aggregate-method/): a count per bit position, added over the positions. The other two methods give the bound "at most $2n$" without the exact value.

*Accounting method.* Charge 2 for each INCREMENT. Invariant: each bit that is 1 holds 1 coin. Each reset in line L3 is paid by the coin on that bit. The set in line L6 costs 1, and the second coin goes on the new 1 bit. In the wrap case there is no set, and the 2 coins are lost. The invariant holds after each increment and the coins are never negative, so $n$ increments cost at most $2n$.

*Potential method.* Let $\Phi$ be the number of 1 bits; $\Phi = 0$ at the start and $\Phi \ge 0$ always. An increment that resets $t < k$ ones costs $t + 1$ and changes $\Phi$ by $1 - t$, so $\hat c = 2$. The wrap costs $k$ and changes $\Phi$ by $-k$, so $\hat c = 0$. So $F_k(n) \le 2n$, and the identity of the potential method gives more: $F_k(n) = \sum \hat c_i - \Phi(D_n) \le 2n - (\text{number of ones at the end})$, which is $2n - s_2(n)$ when $n < 2^k$, the exact value.

## Variants

- **A counter that does not start at 0.** If the counter starts with $b_0$ ones and ends with $b_n$ ones, the potential argument gives a total of at most $2n - b_n + b_0$ flips. So the bound is $O(n)$ once $n \ge k$.
- **Increment and decrement.** With both operations there is no amortized bound $O(1)$. From $2^{k-1} - 1 = 011\cdots1$, an increment gives $100\cdots0$, which flips $k$ bits, and a decrement goes back, which flips $k$ bits. For $k = 8$, 1000 alternating operations flip 8000 bits, which is $\Theta(nk)$.
- **Reset.** An operation that sets the counter to 0 has $O(1)$ amortized cost if the counter keeps the index of its highest 1 bit: charge 1 more coin for each set bit, and the reset uses the coins of the ones (an exercise of CLRS).
- **Cost $2^i$ for bit $i$.** If a flip of bit $i$ costs $2^i$ (as when bit $i$ stands for a block of $2^i$ items, as in the [logarithmic method](/decomposable-searching-problem/)), bit $i$ costs $2^i \lfloor n/2^i \rfloor \le n$ in total, and $n$ increments cost $O(n \log n)$, so $O(\log n)$ amortized for each.
- **Worst-case $O(1)$ representations.** A [Gray code](/gray-code/) changes exactly one bit at each step, but finding that bit takes work. Redundant number systems, such as skew binary numbers, change $O(1)$ digits per increment in the worst case. Okasaki, Chapter 9, builds data structures on them, such as the [skew binary random access list](/skew-binary-random-access-list/).

## Examples

The first 8 increments of a 4-bit counter:

| $j$ | value before | value after | bits flipped | ones after $\Phi$ | $\hat c$ |
|---|---|---|---|---|---|
| 1 | 0000 | 0001 | 1 | 1 | 2 |
| 2 | 0001 | 0010 | 2 | 1 | 2 |
| 3 | 0010 | 0011 | 1 | 2 | 2 |
| 4 | 0011 | 0100 | 3 | 1 | 2 |
| 5 | 0100 | 0101 | 1 | 2 | 2 |
| 6 | 0101 | 0110 | 2 | 2 | 2 |
| 7 | 0110 | 0111 | 1 | 3 | 2 |
| 8 | 0111 | 1000 | 4 | 1 | 2 |

The total is 15, which is $2 \cdot 8 - s_2(8) = 16 - 1$. The costs of the first 16 increments form the ruler sequence 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 5, with total $31 = 32 - 1$: the cost of increment $j$ is one more than the number of times 2 divides $j$.

More totals, for a counter with enough bits:

| $n$ | $s_2(n)$ | $F(n) = 2n - s_2(n)$ |
|---|---|---|
| 10 | 2 | 18 |
| 100 | 3 | 197 |
| 1000 | 6 | 1994 |
| 1023 | 10 | 2036 |
| 1024 | 1 | 2047 |
| 100000 | 6 | 199994 |

**With wrap-around.** A 3-bit counter has costs 1, 2, 1, 3, 1, 2, 1, 3 for its first 8 increments: the eighth goes from 111 to 000 and flips 3 bits. The total is $14 = 8 + 4 + 2$, the sum of $\lfloor 8/2^i \rfloor$ for $i = 0, 1, 2$. After 16 increments it is $28 = 16 + 8 + 4$.

**Average case, for comparison.** If the counter holds a uniformly random $k$-bit value, one increment flips $2 - 2^{1-k}$ bits in expectation: for $k = 4$ that is $15/8$. This is an [average-case](/average-case-analysis/) statement about one increment, not an amortized one; see [amortized versus expected cost](/amortized-vs-expected-cost/).

## Known algorithms

- **The loop INCREMENT above.** $O(1)$ amortized and $O(k)$ worst-case time in a model that reads and writes one bit per step.
- **A machine word.** On the [word RAM](/word-ram/) with $k$ at most the word length, an increment is one addition, which takes $O(1)$ time. The bit-flip count still matters when bits stand for expensive objects, as in a [binomial heap](/binomial-heap/), or when each write wears out memory.

## Bounds

For a counter with $k \ge \lg(n+1)$ bits, $n$ increments flip exactly $2n - s_2(n)$ bits, between $2n - \lceil \lg(n+1) \rceil$ and $2n - 1$. So the amortized cost of an increment tends to 2. The constant 2 is the best possible: for $n = 2^j$ the total is $2^{j+1} - 1$, and $(2^{j+1}-1)/2^j$ exceeds each constant below 2 for large $j$. The worst-case cost of one increment is $k$ (or $\lfloor \lg n \rfloor + 1$ among the first $n$ increments).

## Reductions

- **To the stack with multipop.** The trailing ones behave like a stack: an increment pops all of them and pushes one bit. The potential "number of ones" is the potential "number of items".
- **Binomial heap insertion.** Inserting into a [binomial heap](/binomial-heap/) with $n$ items is an increment of $n$ in binary: each carry links two trees of the same order. So $n$ inserts into an empty heap take $O(n)$ time, $O(1)$ amortized.
- **The logarithmic method.** The static-to-dynamic transform of Bentley and Saxe for a [decomposable searching problem](/decomposable-searching-problem/) keeps one static structure of size $2^i$ for each 1 bit $i$ of the number of items. An insertion is an increment in which a carry rebuilds a block.

## Applications

The counter is the model for each structure that merges blocks of sizes that are powers of 2: binomial heaps, the logarithmic method, the merges of a bottom-up merge sort run online, and log-structured merge trees. It is also the standard warm-up for the three methods of amortized analysis.

## References
