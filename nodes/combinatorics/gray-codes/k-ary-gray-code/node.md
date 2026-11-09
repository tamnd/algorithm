---
tag: 71AG12
kind: algorithm
slug: k-ary-gray-code
name: k-ary Gray code
aliases:
- Guan's k-ary Gray code
- radix-k Gray code
- mixed-radix Gray code
- reflected k-ary Gray code
- Algorithm H (loopless reflected mixed-radix Gray generation)
area: combinatorics/gray-codes
level: advanced
summary: Gray-style ordering of base-k digit strings, where consecutive strings differ by 1 in one digit.
solves: [k-ary-gray-code-generation]
model: word-ram
complexity:
  vars: {n: the number of digits, k: the radix, N: the number of strings (k^n)}
  time: {worst: Θ(k^n), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1976
  people: [James R. Bitner, Gideon Ehrlich, Edward M. Reingold, Donald E. Knuth]
  note: The reflected code for larger alphabets appears in work of the 1950s and later. The loopless generator with focus pointers and direction flags is Knuth's Algorithm H, an extension of the binary method of Bitner, Ehrlich and Reingold.
prereqs: [binary-reflected-gray-code, loopless-gray-code-generation, radix]
see_also: [k-ary-gray-code-generation, gray-code-conversion, cyclic-gray-code, ruler-sequence, factorial-number-system, radix-conversion, minimal-change-ordering, loopless-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (reflected and modular Gray codes for mixed-radix n-tuples, and Algorithm H, loopless reflected mixed-radix Gray generation)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 3.19 (larger alphabets, the recursive definition of the b-ary reflected code and its references)
  - paper: doi:10.1145/360336.360343
    title: James R. Bitner, Gideon Ehrlich and Edward M. Reingold, Efficient generation of the binary reflected Gray code and its applications, Communications of the ACM 19(9), 517 to 521, 1976
    locator: the focus pointer technique for loopless Gray code generation
---

The reflected $k$-ary Gray code lists all $N = k^n$ strings of $n$ digits from $\{0, \ldots, k-1\}$ so that each step changes one digit by $+1$ or $-1$. It extends the [binary reflected Gray code](/binary-reflected-gray-code/): write the list for $n - 1$ digits after a leading 0, then the same list reversed after a leading 1, then forward after a 2, and so on. The same idea works when digit $j$ has its own radix $m_j \ge 2$, which gives the reflected mixed-radix code. Knuth's Algorithm H, shown here, generates it with $O(1)$ worst-case time per string, using the focus pointers of [loopless Gray code generation](/loopless-gray-code-generation/) plus one direction flag per digit.

## In plain words

Think of a set of dials. Dial number $j$ has $m_j$ positions, numbered from 0. You want to see every setting of all the dials once, and at each step you may turn one dial by one click.

The plan is like an odometer that never jumps. The first dial sweeps up from 0 to its top, then the next dial clicks once, then the first dial sweeps back down to 0, then the next dial clicks again, and so on. When the second dial reaches its own end, the third dial clicks, and the second dial starts to sweep the other way. Each dial remembers which way it moves. A small list of notes tells the program which dial to turn next, so each step costs the same small amount of work.

## The problem

Given radices $m_0, \ldots, m_{n-1}$, each at least 2, list all $N = m_0 m_1 \cdots m_{n-1}$ digit arrays $a = (a_{n-1}, \ldots, a_0)$ with $0 \le a_j < m_j$, so that two consecutive arrays differ in one digit, by $\pm 1$. This is [k-ary Gray code generation](/k-ary-gray-code-generation/), and the uniform case $m_j = k$ gives $N = k^n$. Here $n$ is the number of digits and $k$ is the radix. The generator keeps one array and visits it in place.

The *reflected code* is the list $G(0), \ldots, G(N-1)$ defined as follows. Write $r$ in the mixed radix as $r = \sum_j b_j P_j$ with $P_j = m_0 \cdots m_{j-1}$ and $0 \le b_j < m_j$, and let $H_j = \lfloor r / P_{j+1} \rfloor$ be the number formed by the digits above $j$. Then digit $j$ of $G(r)$ is

$$a_j = \begin{cases} b_j & \text{if } H_j \text{ is even,} \\ m_j - 1 - b_j & \text{if } H_j \text{ is odd.} \end{cases}$$

For $m_j = 2$ this is $a_j = b_j \oplus b_{j+1}$, the binary reflected code. Recursively, with $\Gamma$ the list for the lower digits, the list for one more digit on top of radix $m$ is $0\Gamma, 1\Gamma^R, 2\Gamma, 3\Gamma^R, \ldots$, ending with $(m-1)\Gamma$ or $(m-1)\Gamma^R$.

## The algorithm

The focus pointers $f_0, \ldots, f_n$ work as in the binary case, with "digit $j$ is at its last value in the sweep" in the role of "bit $j$ is 1". The flag $o_j \in \{+1, -1\}$ is the direction of the next move of digit $j$.

```pseudo id=main
REFLECTED-MIXED-RADIX(m_0, …, m_{n−1})      ▷ every m_j ≥ 2
L1  for j ← 0 to n − 1 do a_j ← 0; f_j ← j; o_j ← +1
L2  f_n ← n
L3  loop
L4      visit a_{n−1} … a_1 a_0
L5      j ← f_0; f_0 ← 0
L6      if j = n then return
L7      a_j ← a_j + o_j
L8      if a_j = 0 or a_j = m_j − 1 then     ▷ digit j reached an end
L9          o_j ← −o_j
L10         f_j ← f_{j+1}; f_{j+1} ← j + 1
```

Lines L9 and L10 both belong to the test of line L8. Each pass through lines L4 to L10 does a bounded number of operations.

## Example

For $n = 2$ and $k = 3$ the table shows the state at line L4. Strings are written $a_1 a_0$.

| $r$ | $a_1 a_0$ | $f_0 f_1 f_2$ | $o_0 o_1$ | next $j$ |
|---|---|---|---|---|
| 0 | 00 | 0 1 2 | $+$ $+$ | 0 |
| 1 | 01 | 0 1 2 | $+$ $+$ | 0 |
| 2 | 02 | 1 1 2 | $-$ $+$ | 1 |
| 3 | 12 | 0 1 2 | $-$ $+$ | 0 |
| 4 | 11 | 0 1 2 | $-$ $+$ | 0 |
| 5 | 10 | 1 1 2 | $+$ $+$ | 1 |
| 6 | 20 | 0 2 2 | $+$ $-$ | 0 |
| 7 | 21 | 0 2 2 | $+$ $-$ | 0 |
| 8 | 22 | 2 1 2 | $-$ $-$ | 2, stop |

At $r = 1$, line L7 moves $a_0$ from 1 to 2, which is its top, so line L9 turns $o_0$ to $-1$ and line L10 sets $f_0 \leftarrow f_1 = 1$. The next pass changes digit 1. At $r = 5$, $a_1$ moves to 2, its top, and line L10 sets $f_1 \leftarrow f_2 = 2$, so after the last sweep of digit 0 the focus reaches $n = 2$ and the generator stops. By the formula, $G(5)$ has $b_0 = 2$, $b_1 = 1$, $H_0 = 1$ odd, so $a_0 = 2 - 2 = 0$, and $a_1 = b_1 = 1$: the string 10, as in the table.

## Correctness

Call digit $j$ of the counter $r$ *full* when $b_j = m_j - 1$. Let $t_j(r)$ be the number of consecutive full digits of $r$ from digit $j$ upward. The proof in `proofs/correctness.md` has two parts.

- **The code is a Gray code.** For $1 \le r < N$, let $i$ be the number of trailing full digits of $r - 1$. Then $G(r)$ and $G(r-1)$ differ only in digit $i$, by $+1$ if $H_i$ is even and by $-1$ if it is odd. The lower digits wrap from $m_j - 1$ to 0 while their $H_j$ grows by one, and the two changes cancel in $a_j$.
- **The algorithm follows the code.** At the $r$-th visit, $a = G(r)$; $f_j = j + t_j(r)$ when $j = 0$ or digit $j - 1$ of $r$ is not full, and $f_j = j$ otherwise; and $o_j = (-1)^{H_j}$ when digit $j$ of $r$ is not full, and $-(-1)^{H_j}$ when it is full. So line L5 reads $j = t_0(r) = i$, and line L7 moves digit $i$ in the right direction. A digit reaches 0 or $m_j - 1$ after a move exactly when its counter digit becomes full, so lines L8 to L10 keep the invariant.

The map $r \mapsto G(r)$ is one-to-one, because $r$ can be read back from $G(r)$ digit by digit from the top. So each array is visited once.

## Complexity

- **Time.** $\Theta(n)$ to initialize, then $O(1)$ worst-case time per visit, which makes the generator loopless. The total is $\Theta(n + N)$, and $\Theta(N)$ when every $m_j \ge 2$, since then $N \ge 2^n$. This meets the $\Omega(N)$ bound for visiting $N$ strings.
- **Space.** The digits, the $n + 1$ pointers and the $n$ flags: $\Theta(n)$ words.
- **Output.** One digit changes per step, in place. Copying each array costs $\Theta(n)$ more per string.
- **Rank and unrank.** The formula above converts between $r$ and $G(r)$ in $O(n)$ arithmetic operations, reading the digits from the top for the rank.

## Properties

- **Unit steps.** Each step changes one digit by exactly 1, so neighbors are at Lee distance 1 and at [Hamming distance](/hamming-distance/) 1.
- **Ends.** The first string is $0 \ldots 0$. For uniform radix $k$, the last string is $(k-1)(k-1) \ldots (k-1)$ when $k$ is odd and $(k-1) 0 \ldots 0$ when $k$ is even, for $n \ge 1$.
- **Not cyclic for $k \ge 3$.** With $\pm 1$ steps and no wrap, the last and first strings are never neighbors for $k \ge 3$ and $n \ge 1$. For odd $k$ no cyclic code with $\pm 1$ steps exists at all: color each string by the parity of its digit sum; each step changes the color, so a closed walk has even length, but $k^n$ is odd. See [cyclic Gray code](/cyclic-gray-code/).
- **Genlex.** The strings with the same top digits form a block of consecutive entries.
- **Number of moves per digit.** Digit $j$ changes $(m_j - 1) \cdot N / (m_0 \cdots m_j)$ times, the same as the number of times digit $j$ of an ordinary counter increments without a carry out.

## Variants and improvements

- **Modular Gray code.** Let digit $j$ be $(b_j - b_{j+1}) \bmod k$, with $b_n = 0$. Each step changes one digit by $+1$ modulo $k$, and the list is cyclic for every $k$. For $n = 2$, $k = 3$: 00, 01, 02, 12, 10, 11, 21, 22, 20. Knuth describes this code next to the reflected one.
- **Binary case.** With all $m_j = 2$ the flags are not needed, since a bit can move only one way, and Algorithm H becomes Algorithm L of [loopless Gray code generation](/loopless-gray-code-generation/).
- **CAT without pointers.** An odometer that keeps the directions and scans for the lowest digit that can still move gives the same list in $O(1)$ amortized time, like the binary parity rule.
- **Other mixed radices.** With $m_j = j + 2$ the arrays are the digit strings of the [factorial number system](/factorial-number-system/), and the code lists them with one unit change per step. Mapping such strings to permutations gives minimal change lists of permutations.

## When to use it

Use it to step through every point of a grid $[0, m_0) \times \cdots \times [0, m_{n-1})$ when the cost of a step grows with the size of the change: one coordinate moves to a neighbor value per step. Examples are a search over the settings of several discrete parameters where a step reuses the previous result, or a test that walks a multi-dimensional table with small moves. If the walk must close into a ring, use the modular code, or the reflected code with $k$ even and wraparound allowed. If you need only one string at a given position, use the rank and unrank formulas.

## Pitfalls

- **Line L10 outside the test.** If line L10 runs after every move, the focus leaves digit 0 after one step. For $n = 2$, $k = 3$ the output is 00, 01, 11, 12, and it stops after four of nine strings. Lines L9 and L10 must both run only when line L8 finds an end.
- **Testing before moving.** If line L8 runs before line L7, the first pass sees $a_0 = 0$, turns $o_0$ to $-1$, and moves $a_0$ to $-1$. The move of line L7 must come first, and the test must look at the new value.
- **A radix of 1.** With $m_j = 1$, the digit starts at its end, and line L7 moves it to 1, out of range. Line L1 needs every $m_j \ge 2$; drop digits with $m_j = 1$ before the call.
- **Wrong parity in unranking.** For odd $k$, the parity of $H_j$ is the parity of the digit sum $b_{j+1} + \cdots + b_{n-1}$, not the parity of $b_{j+1}$. Using $b_{j+1}$ alone gives the right answer only for even radices.

## Implementations

## History

Reflected codes for alphabets larger than two were studied from the 1950s on; Mütze, Section 3.19, lists papers from 1956 to 1995 with the recursive definition. Some sources name the $k$-ary code after Dah-Jyh Guan, who described generalized Gray codes in 1998. The loopless generator here is Knuth's Algorithm H in Section 7.2.1.1. It adds direction flags to the focus pointers that Bitner, Ehrlich and Reingold used in 1976 for the binary code.

## References
