---
tag: P93GTR
kind: definition
slug: ruler-sequence
name: Ruler sequence
aliases:
- ruler function
- transition sequence of Gray code
- 2-adic valuation sequence
- binary carry sequence
area: combinatorics/gray-codes
level: intro
summary: The bit flipped at step i of the binary reflected Gray code is the number of trailing zeros of i.
prereqs: [trailing-zero-count, binary-reflected-gray-code]
see_also: [lowest-set-bit, binary-counter-increment, tower-of-hanoi, gray-code, loopless-gray-code-generation, de-bruijn-bit-scan, amortized-cost, cyclic-gray-code]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.1.3 (the ruler function, written rho x) and Section 7.2.1.1 (the delta sequence of the Gray binary code)
  - url: https://oeis.org/A007814
    title: OEIS A007814, Exponent of highest power of 2 dividing n, a.k.a. the binary carry sequence, the ruler sequence, or the 2-adic valuation of n
    locator: the sequence 0, 1, 0, 2, 0, 1, 0, 3, ... starting at n = 1
  - url: https://oeis.org/A001511
    title: OEIS A001511, The ruler function, exponent of the highest power of 2 dividing 2n
    locator: the shifted sequence 1, 2, 1, 3, 1, 2, 1, 4, ...
---

The ruler sequence is the sequence $\rho(1), \rho(2), \rho(3), \ldots = 0, 1, 0, 2, 0, 1, 0, 3, \ldots$, where the ruler function $\rho(k)$ is the exponent of the largest power of 2 that divides the positive integer $k$. Its first $2^n - 1$ terms are the delta sequence of the [binary reflected Gray code](/binary-reflected-gray-code/): step $k$ of the code flips bit $\rho(k)$. Some authors use the shifted values $\rho(k) + 1 = 1, 2, 1, 3, \ldots$, which count the bits that a binary counter changes at step $k$. The name comes from the marks on an inch ruler, whose lengths follow the same pattern.

## Definition

For an integer $k \ge 1$, the *ruler function* is

$$\rho(k) = \max\{\, r \ge 0 : 2^r \text{ divides } k \,\}.$$

It equals the number of trailing zeros of $k$ in binary, which is the [trailing zero count](/trailing-zero-count/) of $k$, and $2^{\rho(k)}$ is the [lowest set bit](/lowest-set-bit/) of $k$, the value $k \mathbin{\&} (-k)$ in two's complement. It is not defined for $k = 0$. In number theory it is the 2-adic valuation $\nu_2(k)$.

The *ruler sequence* is $(\rho(k))_{k \ge 1}$, OEIS A007814. The shifted sequence $(\rho(k) + 1)_{k \ge 1} = (\rho(2k))_{k \ge 1}$ is OEIS A001511; some sources call this one the ruler function. On this page $\rho(k)$ always counts from 0.

**Recursive form.** Let $R_0$ be the empty sequence and $R_{n+1} = R_n,\ n,\ R_n$. Then $R_n$ has $2^n - 1$ terms and equals $\rho(1), \ldots, \rho(2^n - 1)$.

*Proof.* By induction on $n$. For $n = 0$ both sides are empty. Assume it for $n$. For $1 \le k < 2^n$, the term at position $k$ of $R_{n+1}$ is $\rho(k)$. The term at position $2^n$ is $n = \rho(2^n)$. For $1 \le j < 2^n$, the term at position $2^n + j$ is $\rho(j)$, and $\rho(2^n + j) = \rho(j)$ because $2^r$ divides $2^n + j$ exactly when it divides $j$, for each $r \le n$, and $2^{n}$ does not divide $j$. $\square$

**Link to the Gray code.** Let $g(k) = k \oplus \lfloor k/2 \rfloor$. For $k \ge 1$, $k$ and $k - 1$ differ exactly in bits $0$ to $\rho(k)$, so $g(k) \oplus g(k-1) = 2^{\rho(k)}$. The proof is on the page of the [binary reflected Gray code](/binary-reflected-gray-code/). As a cycle, $\Gamma_n$ returns from its last string $10\ldots0$ to $0\ldots0$ by flipping bit $n - 1$, so its cyclic delta sequence is $R_n, n - 1$.

## Examples and non-examples

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| binary | 1 | 10 | 11 | 100 | 101 | 110 | 111 | 1000 | 1001 | 1010 | 1011 | 1100 | 1101 | 1110 | 1111 | 10000 |
| $\rho(k)$ | 0 | 1 | 0 | 2 | 0 | 1 | 0 | 3 | 0 | 1 | 0 | 2 | 0 | 1 | 0 | 4 |

- **Gray code for $n = 3$.** The delta sequence of 000, 001, 011, 010, 110, 111, 101, 100 is $0, 1, 0, 2, 0, 1, 0 = R_3$, and the wrap back to 000 flips bit 2, so the cyclic delta sequence is $0, 1, 0, 2, 0, 1, 0, 2$.
- **Value at $k = 96$.** $96 = 2^5 \cdot 3$, so $\rho(96) = 5$.
- **Sum.** $\sum_{k=1}^{2^n - 1} \rho(k) = 2^n - n - 1$. For each $r \ge 1$, exactly $2^{n-r} - 1$ numbers $k$ in $1, \ldots, 2^n - 1$ are multiples of $2^r$, and $\rho(k) = \sum_{r \ge 1} [2^r \text{ divides } k]$. So the sum is $\sum_{r=1}^{n} (2^{n-r} - 1) = (2^n - 1) - n$. For $n = 3$, $0 + 1 + 0 + 2 + 0 + 1 + 0 = 4 = 8 - 3 - 1$. So the average of $\rho(k)$ over a full block is less than 1, which is why a binary counter changes fewer than 2 bits per increment on average.
- **Non-example: trailing ones.** The number of trailing ones of $k$ is $\rho(k + 1)$, not $\rho(k)$. For $k = 3 = 11_2$ it is 2, but $\rho(3) = 0$.
- **Non-example: the count of changed bits.** Incrementing a binary counter from $k - 1$ to $k$ changes $\rho(k) + 1$ bits, not $\rho(k)$. From 3 to 4 it changes three bits, and $\rho(4) = 2$.
- **Non-example: $k = 0$.** Every power of 2 divides 0, so $\rho(0)$ is not defined. Hardware trailing zero count instructions often return the word size for 0, which is not a value of $\rho$.

## Related definitions

- **[Trailing zero count](/trailing-zero-count/)** and **[lowest set bit](/lowest-set-bit/).** These compute $\rho(k)$ and $2^{\rho(k)}$. A table lookup after a multiplication by a de Bruijn constant also finds $\rho(k)$ in $O(1)$ time: see [de Bruijn bit scan](/de-bruijn-bit-scan/).
- **[Binary counter increment](/binary-counter-increment/).** The increment from $k - 1$ to $k$ clears the $\rho(k)$ trailing ones and sets bit $\rho(k)$. The bound of fewer than 2 changed bits per step on average is the standard first example of [amortized cost](/amortized-cost/).
- **[Tower of Hanoi](/tower-of-hanoi/).** In the optimal solution with $n$ discs, move $k$ moves disc $\rho(k) + 1$, counted from the smallest.
- **[Loopless Gray code generation](/loopless-gray-code-generation/).** Focus pointers produce $\rho(1), \rho(2), \ldots$ in $O(1)$ worst-case time per term, with no word operations beyond assignment.
- **Delta sequence.** For any Gray code $v_0, v_1, \ldots$, the delta sequence lists the bit changed at each step. The ruler sequence is the delta sequence of the reflected code. A [balanced Gray code](/balanced-gray-code/) has a delta sequence in which each bit appears about equally often, unlike $R_n$, in which bit $j$ appears $2^{n-1-j}$ times.

## References
