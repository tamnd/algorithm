---
tag: 4XX4WG
kind: algorithm
slug: array-multiplier
name: Array multiplier
aliases:
- combinational multiplier
- carry-save array multiplier
area: algebra/integer-arithmetic
level: intro
summary: Hardware multiplier arranged as a grid of adders, the circuit form of schoolbook multiplication.
solves: [integer-multiplication]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  depth: {worst: Θ(n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
history:
  note: An array of adders with one row per multiplier bit is the direct hardware form of long multiplication; Baugh and Wooley gave the two's complement form in 1973.
prereqs: [schoolbook-multiplication, ripple-carry-adder, boolean-circuit]
see_also: [wallace-tree-multiplier, dadda-multiplier, booth-multiplication, carry-save-addition, carry-propagation, integer-multiplication]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Section 11.5, Array multipliers (the carry-save array with a final ripple-carry adder, and its delay), and Section 11.1, Full-tree multipliers, for comparison
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 4, Multiplication (linear arrays of carry-save adders and the final adder)
  - paper: doi:10.1109/T-C.1973.223648
    title: Charles R. Baugh and Bruce A. Wooley, A two's complement parallel array multiplication algorithm, IEEE Transactions on Computers C-22(12), 1973
    locator: pp. 1045 to 1047
---

An array multiplier is a combinational circuit that multiplies two $n$-bit numbers by adding their $n$ partial products in a grid of adder cells, one row per partial product. It is [schoolbook multiplication](/schoolbook-multiplication/) laid out in hardware. The carry-save form, given here, passes the carries of each row down to the next row instead of along it, and resolves them once at the end with a [ripple-carry adder](/ripple-carry-adder/). It uses $n^2$ AND gates, $n^2 - 2n$ full adders and $n$ half adders, and its depth is $2n - 1$ cell delays. Tree multipliers ([Wallace](/wallace-tree-multiplier/), [Dadda](/dadda-multiplier/)) reach depth $O(\log n)$ with the same number of cells, but the array has short wires and a regular layout.

## In plain words

When you multiply two binary numbers by hand, you write one copy of the first number for each 1 in the second number, each copy shifted one place more to the left, and then you add up the rows. With binary digits, each copy is either the first number or all zeros, and a single digit of it is just an AND of two input digits.

The array multiplier builds this picture out of hardware. It has one row of small adders for each row of the picture. Each adder takes one digit of the new row, one digit of the running sum from above, and one carry from above, and passes its outputs down. Carries go down, not sideways, so a row does not wait for a carry to run along it. Only at the bottom, one ordinary adder turns the leftover carries into the final digits.

## The problem

The input is two unsigned integers $a = \sum_{i=0}^{n-1} a_i 2^i$ and $b = \sum_{j=0}^{n-1} b_j 2^j$ given as bits, with $n \ge 1$. The output is the $2n$ bits $p_0, \ldots, p_{2n-1}$ of the product $ab < 2^{2n}$. The cost model is the [Boolean circuit](/boolean-circuit/) built from AND gates, half adders (two inputs, a sum and a carry) and full adders (three inputs), with one unit of delay for each gate or cell on a path. This is the [integer multiplication](/integer-multiplication/) problem for operands of one fixed size.

## The algorithm

The partial product bit $a_i \wedge b_j$ has weight $2^{i+j}$. Row $j$ of the array adds the partial product $a \cdot b_j \cdot 2^j$. Before row $j$, the running sum is kept in carry-save form as two vectors: $s[i]$ of weight $2^{j-1+i}$ and $c[i]$ of weight $2^{j+i}$.

```pseudo id=main
ARRAY-MULTIPLY(a, b)                     ▷ n bits each, low bit first; returns p[0 .. 2n − 1]
L1  for j ← 0 to n − 1 do pp[j][i] ← a[i] ∧ b[j] for each i       ▷ n² AND gates
L2  s ← pp[0], c ← (0, …, 0)               ▷ row 0 is the first partial product
L3  for j ← 1 to n − 1 do                  ▷ row j of n cells, all in parallel
L4      p[j − 1] ← s[0]                    ▷ the lowest sum bit is final
L5      for i ← 0 to n − 1 do (s′[i], c′[i]) ← FA(pp[j][i], s[i + 1], c[i])   ▷ s[n] = 0
L6      s ← s′, c ← c′
L7  p[n − 1] ← s[0]
L8  carry ← 0
L9  for i ← 1 to n − 1 do                  ▷ the final ripple-carry adder
L10     (p[n − 1 + i], carry) ← FA(s[i], c[i − 1], carry)
L11 p[2n − 1] ← carry
```

FA$(x, y, z)$ returns the sum bit $x \oplus y \oplus z$ and the carry bit $\operatorname{maj}(x, y, z)$, so $x + y + z = s + 2c$. A cell whose input is a constant 0 by construction is built as a half adder, and a cell with one live input is a wire. In row 1 the vector $c$ is all zeros, so its cells are half adders. The top cell of each row has no $s[n]$ and, as the proof shows, its carry input is always 0, so it is a wire. The final adder has a constant 0 carry-in, so its first cell is a half adder.

## Example

Multiply $a = 13 = 1101_2$ by $b = 11 = 1011_2$ with $n = 4$. The bits are listed low first, so $a = [1, 0, 1, 1]$ and $b = [1, 1, 0, 1]$, and row $j$ is $a$ if $b_j = 1$ and zeros otherwise.

| step | partial product row | $s$ after the row | $c$ after the row | product bits so far |
|---|---|---|---|---|
| L2, row 0 | $[1, 0, 1, 1]$ | $[1, 0, 1, 1]$ | $[0, 0, 0, 0]$ | none |
| row 1 | $[1, 0, 1, 1]$ | $[1, 1, 0, 1]$ | $[0, 0, 1, 0]$ | $p_0 = 1$ |
| row 2 | $[0, 0, 0, 0]$ | $[1, 0, 0, 0]$ | $[0, 0, 1, 0]$ | $p_1 = 1$ |
| row 3 | $[1, 0, 1, 1]$ | $[1, 0, 0, 1]$ | $[0, 0, 1, 0]$ | $p_2 = 1$ |
| L7 to L11 | | | | $p_3 = 1$, then $p_4 p_5 p_6 p_7 = 0, 0, 0, 1$ |

In row 2 the cell $i = 2$ adds $0 + s[3] + c[2] = 0 + 1 + 1$, which gives sum 0 and carry 1. In the final adder, the position $i = 3$ adds $s[3] + c[2] = 1 + 1$, and its carry is $p_7$. The product is $1000\,1111_2 = 143 = 13 \cdot 11$.

## Correctness

Let $P_j = \sum_{k < j} p_k 2^k$ be the product bits fixed before row $j$, and $V_j = \sum_i s[i]\, 2^{j+i} + \sum_i c[i]\, 2^{j+i+1}$ the value held by $s$ and $c$ after row $j$. The invariant is

$$P_j + V_j = a \cdot (b \bmod 2^{j+1}),$$

and also $c[n - 1] = 0$. Row $j$ adds $a b_j 2^j$ to both sides: each cell keeps the sum of its three inputs, and the bit $s[0]$ that no cell of the row reads moves into $P$. After row $n - 1$ the leftover value is $2^n$ times the sum of two $(n-1)$-bit numbers, which the final ripple-carry adder computes. The full proof is below.

## Complexity

All counts are exact and hold for every input, since a circuit does the same work on each input.

- **AND gates.** $n^2$, one per partial product bit (line L1).
- **Adder cells.** Rows $2, \ldots, n-1$ have $n - 1$ full adders each and a wire at the top; row 1 has $n - 1$ half adders. The final adder has one half adder and $n - 2$ full adders. In total there are $(n-2)(n-1) + (n-2) = n^2 - 2n$ full adders and $n$ half adders, for $n \ge 2$. The test file checks these counts for $n \le 12$.
- **Depth.** The AND gates take one unit. By induction on $j$, the outputs of row $j$ arrive at time $j + 1$, since each cell reads the outputs of row $j - 1$. So $s$ and $c$ are ready at time $n$. The final adder adds one unit per position, and its last carry arrives at time $n + (n - 1) = 2n - 1$. So the depth is $2n - 1$ cell delays, $\Theta(n)$.
- **Simulation.** A sequential program that evaluates the circuit does $\Theta(n^2)$ bit operations, the size of the circuit; this is the time entry of the front matter.

The model counts one unit for each cell. In real circuits the sum output of a full adder is slower than the carry, and the delay of the array is usually quoted as about $2n$ full-adder delays plus the AND delay.

## Properties

- **Regular and local.** Each cell talks only to its neighbors in the row above and below, so the layout is a rectangle of identical cells with short wires. The area is $\Theta(n^2)$.
- **Pipelinable.** Latches between the rows turn the array into a pipeline that accepts a new product every cycle.
- **No carry chain inside a row.** Only the last adder propagates carries. A row that propagated its carries, as in the naive design with a ripple-carry adder in each row, has the same $\Theta(n)$ order of depth but larger constants.
- **Unsigned.** The array as given multiplies unsigned numbers. Signed operands need the Baugh-Wooley modification or Booth recoding.

## Variants and improvements

- **Ripple-row array.** Each row is a ripple-carry adder that adds the next partial product to the shifted running sum. Its depth is also about $2n$, because the critical path runs diagonally, but each row must finish its carries.
- **Baugh-Wooley array.** For [two's complement](/twos-complement/) operands, the partial product bits that involve one sign bit are complemented and constant 1s are added in two positions, so that the same array of positive cells computes the signed product (Baugh and Wooley, 1973).
- **Booth recoding.** [Booth multiplication](/booth-multiplication/) in radix 4 halves the number of rows, with partial products from $\{-2a, -a, 0, a, 2a\}$.
- **Tree reduction.** The [Wallace tree](/wallace-tree-multiplier/) and the [Dadda multiplier](/dadda-multiplier/) reduce the partial products with [carry-save adders](/carry-save-addition/) in a tree of depth $O(\log n)$, followed by a fast final adder.
- **Fast final adder.** Replacing the ripple adder of lines L8 to L11 with a [carry-lookahead adder](/carry-lookahead-adder/) cuts the depth to $n + O(\log n)$, since the rows still take $n$ levels.

## When to use it

Use an array multiplier when area and simplicity matter more than speed, when the operands are small (8 to 16 bits), or when the multiplier is pipelined so that its depth is spread over several cycles. Its regular layout is easy to place and route. For wide fast multipliers, such as the 53-bit significand products of double precision floating point, tree multipliers with Booth recoding are the usual choice, because their depth is logarithmic. In software, the same row-by-row process is [schoolbook multiplication](/schoolbook-multiplication/).

## Pitfalls

- **Sideways carries.** Feeding the carry of cell $i$ into cell $i + 1$ of the same row turns line L5 into a ripple-carry adder per row. The result is still correct, but each row then waits for its carry chain. Line L5 sends $c[i]$ down to the next row at the same position.
- **Losing the low bits.** Line L4 takes $s[0]$ as a final product bit before the row is processed. A program that keeps only $s$ and $c$ of width $n$ and forgets line L4 drops $p_0, \ldots, p_{n-2}$.
- **The final adder's inputs.** Line L10 adds $s[i]$ to $c[i - 1]$, not $c[i]$: the carry $c[i - 1]$ has weight $2^{n + i - 1}$, the same as $s[i]$. Using $c[i]$ shifts every carry by one place.
- **Signed inputs.** Feeding two's complement numbers into the unsigned array gives the wrong high half of the product. Sign-extend the partial products, or use the Baugh-Wooley form.

## Implementations

## History

An array of adders with one row per multiplier bit is the direct hardware form of long multiplication. Wallace in 1964 replaced the rows of carry-save adders by a tree to reach logarithmic depth, and Dadda refined the tree in 1965. Baugh and Wooley published the two's complement array in 1973, and array multipliers became a standard block of VLSI design in the following decade because of their regular layout.

## References
