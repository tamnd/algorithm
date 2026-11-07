---
tag: HGRER8
kind: algorithm
slug: lattice-multiplication
name: Lattice multiplication
aliases:
- gelosia multiplication
- sieve multiplication
- product scanning
area: algebra/integer-arithmetic
level: intro
summary: A grid-based layout of schoolbook multiplication that sums diagonals of partial products.
solves: [integer-multiplication]
model: word-ram
complexity:
  vars: {m: the number of digits of the first operand, n: the number of digits of the second operand}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [schoolbook-multiplication, positional-number-system]
see_also: [schoolbook-multiplication, russian-peasant-multiplication, karatsuba-multiplication, integer-multiplication, multi-operand-addition, convolution]
sources:
  - book: isbn:9783540633693
    title: Jean-Luc Chabert (editor), A History of Algorithms, From the Pebble to the Microchip, Springer, 1999
    locator: Chapter 1, the section on multiplication per gelosia, pp. 21 to 26 (Ibn al-Banna and the spread of the method to Italy)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, Algorithm M (the same digit products, added by rows)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3.1, Naive multiplication
---

Lattice multiplication computes a product of two numbers by writing all the digit products in a grid, each split by a diagonal into its high and its low digit, and then adding the digits along each diagonal with carries. It is [schoolbook multiplication](/schoolbook-multiplication/) in another order: the grid holds the same $mn$ digit products, but the additions run by output position instead of by rows. It costs $\Theta(mn)$ digit operations, and in machine code the same order is called *product scanning*, which computes each output limb in one pass of a small accumulator.

## In plain words

Draw a grid with one column for each digit of the first number and one row for each digit of the second. Cut each cell by a diagonal line. In each cell, write the product of its column digit and its row digit: the tens digit above the line and the units digit below it. The products are all small, from the times table.

Now the diagonal lines form lanes across the grid. Add the digits in each lane, starting from the lane at the corner of the lowest digits. Write the last digit of each lane sum, and carry the rest into the next lane. The digits you write, read in order, are the product. You never have to add long rows of shifted numbers; the grid does the shifting for you.

## The problem

The input is two nonnegative integers in a radix $\beta \ge 2$, as digit arrays $a = [a_0, \ldots, a_{m-1}]$ and $b = [b_0, \ldots, b_{n-1}]$, least significant digit first, with $A = \sum a_i \beta^i$ and $B = \sum b_j \beta^j$. The output is the array $c$ of $m + n$ digits with $\sum_k c_k \beta^k = AB$, the problem of [integer multiplication](/integer-multiplication/). On paper $\beta = 10$. On a machine $\beta = 2^w$, the digits are limbs, and the costs are in limb operations on the [word RAM](/word-ram/) with $w$-bit words.

## The algorithm

```pseudo id=main
LATTICE-MUL(a[0 .. m − 1], b[0 .. n − 1])
L1  for i ← 0 to m − 1, j ← 0 to n − 1 do               ▷ fill the grid
L2      (h[i][j], l[i][j]) ← (⌊a[i] b[j] / β⌋, a[i] b[j] mod β)
L3  s ← an array of m + n zeros                          ▷ the diagonal sums
L4  for i ← 0 to m − 1, j ← 0 to n − 1 do
L5      s[i + j] ← s[i + j] + l[i][j];  s[i + j + 1] ← s[i + j + 1] + h[i][j]
L6  carry ← 0
L7  for k ← 0 to m + n − 1 do                            ▷ one carry pass
L8      t ← s[k] + carry
L9      c[k] ← t mod β;  carry ← ⌊t / β⌋
L10 return c                                             ▷ here carry = 0
```

Cell $(i, j)$ holds $a_i b_j = h_{ij}\beta + l_{ij}$. Its low digit has the weight $\beta^{i+j}$ and its high digit the weight $\beta^{i+j+1}$. In the drawing, all digits of weight $\beta^k$ lie in one diagonal lane, which is why line L5 adds the low digit to lane $i + j$ and the high digit to lane $i + j + 1$. Lines L7 to L9 turn the lane sums, which can be larger than a digit, into digits.

Because $(\beta - 1)^2 = (\beta - 2)\beta + 1$, each high digit is at most $\beta - 2$. Lane $k$ gets at most $\min(m, n)$ low digits and $\min(m, n)$ high digits, so $s_k \le 2\min(m, n)(\beta - 1)$. By induction the carry stays below $2\min(m, n)$, so a lane sum needs only $\lceil \log_2 (2 \min(m, n)) \rceil$ bits more than a digit.

## Example

Multiply $A = 4093$ by $B = 199$ in radix 10. Least significant digit first, $a = [3, 9, 0, 4]$ and $b = [9, 9, 1]$. The grid, with each cell written as high digit / low digit:

| | $a_3 = 4$ | $a_2 = 0$ | $a_1 = 9$ | $a_0 = 3$ |
|---|---|---|---|---|
| $b_0 = 9$ | 3 / 6 | 0 / 0 | 8 / 1 | 2 / 7 |
| $b_1 = 9$ | 3 / 6 | 0 / 0 | 8 / 1 | 2 / 7 |
| $b_2 = 1$ | 0 / 4 | 0 / 0 | 0 / 9 | 0 / 3 |

The lane sums are $s = [7, 10, 14, 23, 9, 7, 0]$. For example lane 2 gets the low digits of the cells with $i + j = 2$, which are $l_{2,0} = 0$, $l_{1,1} = 1$ and $l_{0,2} = 3$, and the high digits of the cells with $i + j = 1$, which are $h_{1,0} = 8$ and $h_{0,1} = 2$: in total 14. The carry pass:

| $k$ | $s_k$ | carry in | $t$ | $c_k$ | carry out |
|---|---|---|---|---|---|
| 0 | 7 | 0 | 7 | 7 | 0 |
| 1 | 10 | 0 | 10 | 0 | 1 |
| 2 | 14 | 1 | 15 | 5 | 1 |
| 3 | 23 | 1 | 24 | 4 | 2 |
| 4 | 9 | 2 | 11 | 1 | 1 |
| 5 | 7 | 1 | 8 | 8 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 |

So $c = [7, 0, 5, 4, 1, 8, 0]$, and $4093 \cdot 199 = 814507$. The carry of lane 3 is 2: a lane can carry more than 1.

## Correctness

The lanes regroup the terms of the product. Since $a_i b_j = h_{ij}\beta + l_{ij}$,

$$AB = \sum_{i,j} a_i b_j \beta^{i+j} = \sum_{i,j} \big( l_{ij}\beta^{i+j} + h_{ij}\beta^{i+j+1} \big) = \sum_{k} s_k \beta^k .$$

The carry pass keeps the invariant $\sum_{k' < k} c_{k'}\beta^{k'} + \text{carry}\cdot\beta^k = \sum_{k' < k} s_{k'}\beta^{k'}$, so at the end $\sum c_k \beta^k + \text{carry}\cdot\beta^{m+n} = AB < \beta^{m+n}$, and the final carry is 0. The full proof is below.

## Complexity

All costs are in digit operations (limb operations for $\beta = 2^w$). Lines L1 and L2 do $mn$ digit products. Lines L4 and L5 do $2mn$ additions into the lane sums, and the carry pass does $m + n$ steps. So the time is $\Theta(mn)$ for every input, the same order and the same number of digit products as the schoolbook method. The grid as written takes $\Theta(mn)$ space; a program does not store it, and adds each product into its lanes at once, which leaves $\Theta(m + n)$ extra space for the lane sums.

**Product scanning.** A machine version computes the lanes one at a time: for $k = 0, 1, \ldots$, it adds all $a_i b_j$ with $i + j = k$ into an accumulator of three limbs, writes the low limb as $c_k$, and shifts the accumulator by one limb. Each output limb is then written once. This order is used in multiplication code for cryptography and in hardware, where it avoids reading and writing the partial result many times. Which order is faster on a given machine is observed, not proved.

## Properties

- **Same work as schoolbook.** The same $mn$ digit products; only the order of the additions changes.
- **Additions are short.** On paper, each step adds small digits, and no long rows are written.
- **Carries are delayed.** The lane sums can exceed a digit, and the carries are resolved once at the end. This is a simple case of the [carry-save](/carry-save-addition/) idea.
- **Not in place.** The output needs its own $m + n$ digits.

## Variants and improvements

- **Napier's bones.** Rods that hold the rows of the grid for each digit, so that the grid is laid out by placing rods side by side.
- **Column (Comba) multiplication.** The product scanning order above, with a three-limb accumulator.
- **Squaring by lanes.** In lane $k$, the products $a_i a_j$ and $a_j a_i$ are equal, so each lane needs only half of its products, doubled, plus a square $a_{k/2}^2$ when $k$ is even.
- **The convolution view.** The lane sums before the split into digits, $\sum_{i + j = k} a_i b_j$, are the [convolution](/convolution/) of the two digit sequences. The fast methods compute this convolution with fewer products and then do the same carry pass.

## When to use it

On paper, lattice multiplication is a reliable way to multiply long numbers, because each step is small and the layout prevents errors of alignment. On a machine, use the product-scanning order when the output should be written in one pass, for example in fixed-size cryptographic code; otherwise the row order of the [schoolbook method](/schoolbook-multiplication/) is as good. For long operands, use [Karatsuba](/karatsuba-multiplication/) or a faster method.

## Pitfalls

- **Lane carries larger than one.** Line L9 must use $\lfloor t / \beta \rfloor$, not a carry bit. In the example, lane 3 has $t = 24$ and carries 2. With a carry of 0 or 1 the result is wrong.
- **The high digit in the wrong lane.** The high digit $h_{ij}$ belongs to lane $i + j + 1$ (line L5). Adding it to lane $i + j$ gives a value that is too small.
- **Accumulator width.** In machine code, a lane sum of $\min(m, n)$ products of two limbs can need more than two limbs. Use an accumulator of $2w + \lceil \log_2 \min(m, n) \rceil$ bits, in practice three limbs.
- **Reading the digits in the wrong order.** On paper the result is read along the left and bottom edges, from the top-left lane down to the bottom-right lane. Reading the edges the other way reverses the digits.

## Implementations

## History

The method is old. Chabert's history of algorithms gives its earliest known description in the Maghreb, in the work of Ibn al-Banna in the late thirteenth century, and describes its spread to Italy, where it was called *gelosia*, after the lattice screens of windows. Later it was printed in Italian arithmetic books of the fifteenth century, and the rods of John Napier, known as Napier's bones, mechanize it.

## References
