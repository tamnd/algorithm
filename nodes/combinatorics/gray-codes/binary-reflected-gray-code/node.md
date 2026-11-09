---
tag: 73K11Q
kind: algorithm
slug: binary-reflected-gray-code
name: Binary reflected Gray code
aliases:
- BRGC
- reflected Gray code construction
area: combinatorics/gray-codes
level: intro
summary: 'Recursive construction: prefix the list with 0, then append the reversed list prefixed with 1.'
solves: [gray-code-generation]
model: word-ram
complexity:
  vars: {n: the length of the strings, N: the number of strings (2^n)}
  time: {worst: Θ(2^n), amortized: Θ(1)}
  space: {extra: Θ(2^n)}
properties: {in_place: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1953
  people: [Frank Gray]
  note: Gray's patent of 1953 (filed in 1947) used the reflected code for pulse code communication. Stibitz patented a use of it in 1943, and Gros linked the Chinese rings puzzle to it in 1872.
prereqs: [gray-code, bitwise-operations, induction]
see_also: [binary-to-gray-conversion, gray-to-binary-conversion, loopless-gray-code-generation, ruler-sequence, cyclic-gray-code, k-ary-gray-code, revolving-door-ordering, power-set-enumeration]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (the recursive definition of the Gray binary code, the formula g(k) = k XOR floor(k/2), its inverse, Algorithm G and the history of the code)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 5, Section 5.2 (the binary reflected Gray code and its applications)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Section 2 (the binary reflected Gray code)
  - url: https://patents.google.com/patent/US2632058A
    title: Frank Gray, Pulse code communication, US Patent 2,632,058, issued 17 March 1953
    locator: the reflected binary code
---

The binary reflected Gray code (BRGC) is the list $\Gamma_n$ of all $N = 2^n$ binary strings of length $n$ given by $\Gamma_0 = \varepsilon$ and $\Gamma_{n+1} = 0\Gamma_n,\ 1\Gamma_n^R$: the old list with a 0 in front, then the old list in reverse order with a 1 in front. Each two neighbors differ in one bit, and so do the last and the first string, so it is a [cyclic Gray code](/cyclic-gray-code/). The string of rank $k$ is $k \oplus \lfloor k/2 \rfloor$, and step $k$ changes bit $\rho(k)$ of the [ruler sequence](/ruler-sequence/). The construction below builds the whole list in $\Theta(N)$ word operations, which is optimal.

## In plain words

Start with a list that holds one empty string. To make the strings one character longer, copy the list, put a 0 in front of each string, and keep it as the first half. Then read the old list from the end back to the start, put a 1 in front of each string, and append it as the second half.

In the first half, each step is an old step, so it changes one character. At the join, the two strings are the same old string, one with a 0 in front and one with a 1 in front. In the second half, each step is an old step read backwards. So each step of the new list changes exactly one character. The last string and the first string also differ only in the front character.

## The problem

Given $n \ge 0$, list each of the $2^n$ strings of $\{0,1\}^n$ once, so that each two neighbors in the list differ in exactly one bit. This is [Gray code generation](/gray-code-generation/). Here $n$ is the length of the strings and $N = 2^n$. We store a string $a_{n-1} \ldots a_1 a_0$ as the integer $\sum_j a_j 2^j$, so bit $a_j$ has weight $2^j$ and the leftmost character is bit $n-1$.

## The algorithm

Prefixing a bit to an $i$-bit string is the same as adding $0$ or $2^i$ to its integer. So $0\Gamma_i$ is the list $\Gamma_i$ itself, and $1\Gamma_i^R$ is $\Gamma_i$ read backwards with $2^i$ added to each entry.

```pseudo id=main
BRGC(n)                                   ▷ returns Γ_n as a list of n-bit integers
L1  G ← [0]                               ▷ Γ_0: one empty string
L2  for i ← 0 to n − 1 do                 ▷ G holds Γ_i
L3      for j ← |G| − 1 downto 0 do       ▷ |G| = 2^i, read once before the loop
L4          append G[j] + 2^i to G        ▷ the string 1 G[j]
L5  return G
```

After the pass with index $i$, the list $G$ has $2^{i+1}$ entries and equals $\Gamma_{i+1}$. The loop of line L3 reads the old entries in reverse order, which makes the reflection.

## Example

For $n = 3$ the list grows in three passes.

| after pass | $G$ as integers | $G$ as strings |
|---|---|---|
| start | 0 | (empty) |
| $i = 0$ | 0, 1 | 0, 1 |
| $i = 1$ | 0, 1, 3, 2 | 00, 01, 11, 10 |
| $i = 2$ | 0, 1, 3, 2, 6, 7, 5, 4 | 000, 001, 011, 010, 110, 111, 101, 100 |

In pass $i = 2$, line L3 reads 2, 3, 1, 0 and line L4 appends $2 + 4 = 6$, $3 + 4 = 7$, $1 + 4 = 5$ and $0 + 4 = 4$. The changed bits from one string to the next are 0, 1, 0, 2, 0, 1, 0, and the wrap from 100 to 000 changes bit 2. For $n = 4$ the list is 0000, 0001, 0011, 0010, 0110, 0111, 0101, 0100, 1100, 1101, 1111, 1110, 1010, 1011, 1001, 1000.

## Correctness

Write $g(k) = k \oplus \lfloor k/2 \rfloor$ and let $\rho(k)$ be the exponent of the largest power of 2 that divides $k \ge 1$. The full proof is in `proofs/correctness.md`. It shows by induction on $i$ that after pass $i$ the list is $\Gamma_{i+1}$ and that $G[k] = g(k)$ for each $k < 2^{i+1}$. The key step uses that $g$ is linear over $\oplus$: for $j < 2^i$, the entry at position $2^{i+1} - 1 - j = j \oplus (2^{i+1} - 1)$ is $g(j) \oplus g(2^{i+1} - 1) = g(j) \oplus 2^i$, which is what line L4 appends. From $G[k] = g(k)$ the page gets the three properties of a Gray cycle:

- **Each string once.** If $g(x) = g(y)$ then $z = x \oplus y$ satisfies $z = \lfloor z/2 \rfloor$, so $z = 0$. So $g$ is one-to-one on $[0, 2^n)$, and it maps into $[0, 2^n)$.
- **One bit per step.** $g(k) \oplus g(k-1) = g(k \oplus (k-1)) = g(2^{\rho(k)+1} - 1) = 2^{\rho(k)}$.
- **Cyclic.** $g(2^n - 1) = 2^{n-1}$ differs from $g(0) = 0$ in bit $n - 1$, for $n \ge 1$.

## Complexity

Pass $i$ appends $2^i$ entries, so the passes append $2^n - 1$ entries in total. Each append is $O(1)$ word operations on the [word RAM](/word-ram/) when $n$ is at most the word size.

- **Time.** $\Theta(N)$ in total, so $\Theta(1)$ amortized per string. Any method that writes all $N$ strings needs $\Omega(N)$ time, so this is optimal.
- **Space.** The output list has $N$ words. If each string must be a separate array of $n$ bits, the output alone takes $\Theta(nN)$ time and space.
- **Without the list.** When the caller needs only one string at a time, a generator keeps one array of $n$ bits and changes one bit per step. [Loopless Gray code generation](/loopless-gray-code-generation/) does this in $O(1)$ worst-case time per string and $O(n)$ space.

## Properties

- **Transition counts.** In the cycle $\Gamma_n$ for $n \ge 2$, bit $j$ changes $2^{n-1-j}$ times for $0 \le j \le n-2$, and bit $n-1$ changes 2 times. For $n = 4$ the counts are 8, 4, 2, 2. A [balanced Gray code](/balanced-gray-code/) evens these out.
- **Reflection symmetry.** $g(2^n - 1 - k) = g(k) \oplus 2^{n-1}$, because $2^n - 1 - k = k \oplus (2^n - 1)$. So the list read backwards is the list with the first bit flipped.
- **Prefix structure.** For each $m \le n$, the strings that share the same first $n - m$ bits form a block of $2^m$ consecutive entries, and the block is $\Gamma_m$ or $\Gamma_m^R$. This is the genlex property.
- **Fixed weight.** The strings of $\Gamma_n$ with exactly $k$ ones, in the order of $\Gamma_n$, form the [revolving door order](/revolving-door-ordering/): each two neighbors differ by moving one 1 (Tang and Liu, 1973).
- **Distances.** Two strings that differ in $t > 0$ bits are at least $\lceil 2t/3 \rceil$ steps apart in $\Gamma_n$ (Yuen 1974, Cavior 1975; see Mütze's survey, Section 3.1).

## Variants and improvements

- **Direct formula.** The string of rank $k$ is $k \oplus \lfloor k/2 \rfloor$: see [binary to Gray conversion](/binary-to-gray-conversion/). The rank of a string is its prefix exclusive or: see [Gray to binary conversion](/gray-to-binary-conversion/).
- **Counting with parity (Knuth, Algorithm G).** Keep the parity of the number of 1s. When the parity is even, flip bit 0. When it is odd, flip the bit to the left of the rightmost 1. This gives $\Gamma_n$ one string at a time in $O(1)$ amortized time.
- **Focus pointers (Knuth, Algorithm L).** A small array of pointers gives the next bit to flip in $O(1)$ worst-case time: see [loopless Gray code generation](/loopless-gray-code-generation/).
- **Larger alphabets.** The same reflection works for digits $0$ to $k - 1$: see [k-ary Gray code](/k-ary-gray-code/).

## When to use it

Use the reflected code when you need any Gray code of $\{0,1\}^n$ and do not care which one: it has the simplest rank and unrank functions of all Gray codes. Build the whole list as above only when you need random access to it. To walk the strings once, use a loopless or a parity based generator, which needs only $O(n)$ space. If the bits must change about equally often, for example to spread wear over the tracks of an encoder, use a [balanced Gray code](/balanced-gray-code/) instead.

## Pitfalls

- **No reversal.** Line L3 with "for $j \leftarrow 0$ to $|G| - 1$" appends $1\Gamma_i$ instead of $1\Gamma_i^R$. For $n = 2$ this gives 00, 01, 10, 11, and the step from 01 to 10 changes two bits. Line L3 must count down.
- **A moving bound.** In line L3, $|G|$ must be read once, before the loop. A loop that tests the current length of $G$ after each append never stops.
- **Copies.** Storing each string as a new array of $n$ bits makes the time $\Theta(nN)$, not $\Theta(N)$.

## Implementations

## History

Frank Gray of Bell Labs filed a patent in 1947 for a pulse code tube that used the reflected binary code, and the patent was issued in 1953; the name "Gray code" comes from it. Knuth, in Section 7.2.1.1, traces the code further back. George Stibitz used it in a patent of 1943, and Émile Baudot used the 5-bit code in a telegraph machine that he showed in 1878. Louis Gros, in a book on the Chinese rings puzzle published in Lyon in 1872, linked the moves of the puzzle to binary numbers, and Knuth calls him the true inventor of the code.

## References
