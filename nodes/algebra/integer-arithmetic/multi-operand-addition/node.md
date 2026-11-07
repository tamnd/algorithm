---
tag: 0T1Z4G
kind: problem
slug: multi-operand-addition
name: Multi-operand addition
aliases:
- summing many integers
- multioperand addition
- addition of many operands
area: algebra/integer-arithmetic
level: advanced
summary: Sum k integers at once while avoiding repeated carry propagation.
model: boolean-circuit
complexity:
  vars: {k: the number of operands, n: the number of binary digits of each operand}
  time: {worst: Θ(n k)}
  depth: {worst: Θ(log (n k))}
prereqs: [integer-addition, carry-save-addition, ripple-carry-adder]
see_also: [wallace-tree-multiplier, dadda-multiplier, carry-save-addition, array-multiplier, redundant-number-system, kogge-stone-adder, schoolbook-multiplication, carry-propagation]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 8, Multioperand addition (two-operand adders in sequence, carry-save adders, Wallace and Dadda trees, parallel counters and compressors, signed operands)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 3, Multioperand addition (carry-save adder arrays and trees, counters and compressors)
  - paper: C. S. Wallace, A suggestion for a fast multiplier, IEEE Transactions on Electronic Computers EC-13(1), 1964
    title: Christopher S. Wallace, A suggestion for a fast multiplier
    locator: pp. 14 to 17 (reduction of many operands to two by a tree of carry-save adders)
---

Multi-operand addition is the problem of adding $k \ge 3$ integers at once. Done as $k - 1$ ordinary additions, it pays for carry propagation $k - 1$ times. The better way is to keep the running sum in a [redundant](/redundant-number-system/) carry-save form, as two numbers whose sum is the value. A row of full adders turns three numbers into two with no carry chain, in constant depth. A tree of such rows reduces $k$ operands to two in about $\log_{3/2}(k/2)$ levels, and a single fast adder finishes. So $k$ numbers of $n$ bits can be added by a circuit of size $\Theta(nk)$ and depth $\Theta(\log(nk))$, both optimal up to constants. Multi-operand addition is the core of every fast multiplier, whose partial products are $n$ operands, and of multiply-accumulate units, dot products and bit counting.

## In plain words

To add a long column of numbers by hand, you do not add the first two, then add the third to the result, and so on, carrying each time. You add each digit column all at once and carry the column totals to the left.

A circuit can do something similar. It takes the numbers three at a time and turns every three into two: one number of column sums and one of carries, without waiting for any carry to travel. After a few rounds of this, only two numbers are left, and one ordinary addition gives the answer. The number of rounds grows very slowly with the number of operands: 64 numbers need only 10 rounds.

## Definition

**Input.** Integers $x_1, \ldots, x_k$ with $0 \le x_j < 2^n$, each as $n$ binary digits; in software, as arrays of $n$ limbs in radix $\beta = 2^w$.

**Output.** The sum $S = \sum_{j=1}^{k} x_j$, which has at most $n + \lceil \log_2 k \rceil$ binary digits, since $S \le k(2^n - 1) < 2^{n + \lceil \log_2 k \rceil}$.

**Cost model.** For circuits, the [Boolean circuit](/boolean-circuit/) model with gates of fan-in at most 3, a full adder counting as one cell of constant size and depth. The size, in the field `time`, counts gates; the depth is the longest path. For software, the [word RAM](/word-ram/) with $w$-bit words, counting limb operations. The bounds below are proved; the choice between tree shapes in a given technology is observed.

## Variants

- **Signed operands.** Two's complement operands are sign-extended to the width of the sum, or, more cheaply, their sign bits are complemented and a constant is added once; Parhami describes the trick.
- **Partial products of a multiplier.** The operands are $a \cdot b_i 2^i$, shifted copies, so the input is a parallelogram of bits, not a rectangle; see [Wallace tree multiplier](/wallace-tree-multiplier/).
- **Accumulation.** One new operand per clock cycle, added into a carry-save accumulator, with one carry-propagate addition at the end, as in multiply-accumulate units.
- **Counting.** The sum of $k$ single bits, the population count, is the case $n = 1$; parallel counters such as the $(7, 3)$ counter count the bits of one column.
- **Modular sums.** The sum modulo $2^n$, or modulo $2^n - 1$ with end-around carries, as in checksums.
- **Software sums of big integers.** Summing $k$ multiprecision numbers, where the carries of many additions can be delayed by accumulating limbs in double-width words.

## Examples

All examples were checked by script.

- **Carry-save, three to two.** $13 + 11 + 7$: the bitwise XOR is $0001$, and the majority of each column, shifted left one place, is $11110$. So the three operands become $1$ and $30$, with sum $31$.
- **Four operands.** Adding $5$ to the pair $(1, 30)$ by one more row of full adders gives $(26, 10)$, and one carry-propagate addition gives $36 = 13 + 11 + 7 + 5$.
- **Levels of a tree.** With $d_0 = 2$ and $d_{j+1} = \lfloor 3d_j/2 \rfloor$, the numbers $2, 3, 4, 6, 9, 13, 19, 28, 42, 63, 94$ are the largest numbers of operands that $0, 1, 2, \ldots, 10$ levels of carry-save adders reduce to two. So 64 operands need 10 levels, and the 53 partial products of a double-precision significand multiplier need 9. A script that reduces greedily, three rows to two at each level, agrees for every $k < 100$.

## Known algorithms

| method | size | depth | notes |
|---|---|---|---|
| $k - 1$ ripple-carry additions in sequence | $\Theta(nk)$ | $\Theta(n + k)$ | the carries of the additions overlap in time, as in an [array multiplier](/array-multiplier/) |
| $k - 1$ fast additions in sequence | $\Theta(kn\log n)$ | $\Theta(k \log n)$ | each a [Kogge-Stone](/kogge-stone-adder/) or similar adder |
| Binary tree of fast adders | $\Theta(kn \log n)$ | $\Theta(\log k \log n)$ | pairwise sums, each level waits for its carries |
| Carry-save array, then one adder | $\Theta(nk)$ | $\Theta(k + \log n)$ | a linear chain of [carry-save](/carry-save-addition/) rows |
| Wallace tree, then one fast adder | $\Theta(nk)$ | $\Theta(\log k + \log n)$ | three rows to two at every level, as early as possible |
| Dadda tree, then one fast adder | $\Theta(nk)$ | $\Theta(\log k + \log n)$ | the same number of levels with fewer adders, by reducing as late as possible; see [Dadda multiplier](/dadda-multiplier/) |
| Trees of 4 to 2 compressors | $\Theta(nk)$ | $\Theta(\log k + \log n)$ | two levels of carry-save in one more regular cell |
| Word RAM, delayed carries | $\Theta(kn)$ limb operations | | accumulate each limb column in a double-width word, then one carry pass |

## Bounds

- **Size.** $\Theta(nk)$. Every input bit must enter the circuit, so $\Omega(nk)$. A carry-save tree uses $(k - 2)n$ full adders, and a final adder of linear size, a ripple-carry adder or, for logarithmic depth as well, a [Brent-Kung adder](/brent-kung-adder/), adds $O(n + \log k)$ gates.
- **Depth.** $\Theta(\log(nk))$. The top output bit depends on all $nk$ input bits, so with fan-in at most 3 the depth is $\Omega(\log(nk))$. A Wallace or Dadda tree reaches two operands in $\lceil \log_{3/2}(k/2) \rceil + O(1)$ levels of constant depth, and a prefix adder of the result width adds $O(\log(n + \log k))$, so $O(\log k + \log n)$ in total.
- **Full adders are optimal for the reduction.** Each full adder removes exactly one bit from the bit matrix, three bits in and two out, so reducing $nk$ input bits to two rows of about $n + \log_2 k$ bits needs about $(k - 2)n$ full adders, whatever the tree shape.
- **Software.** $\Theta(kn)$ limb operations, to read the input.

## Reductions

- **From multiplication.** An $n \times n$ product is the multi-operand sum of $n$ shifted partial products, so a multi-operand adder of depth $O(\log n)$ gives a multiplier of depth $O(\log n)$; this is the Wallace tree multiplier.
- **To counting.** The sum is $\sum_i 2^i C_i$, where $C_i$ is the number of ones in column $i$. Counting the bits of each column with parallel counters, and adding the counts with their shifts, reduces the problem to a smaller multi-operand addition.
- **To two-operand addition**, through carry-save form: after the reduction, one ordinary addition is left, so the problem costs one carry propagation in total, not $k - 1$.

## Applications

- **Multipliers.** Every fast multiplier sums its partial products this way; see the [Wallace tree multiplier](/wallace-tree-multiplier/) and the [Dadda multiplier](/dadda-multiplier/).
- **Multiply-accumulate and dot products.** Digital signal processors and matrix units add many products into one accumulator, keeping it in carry-save form between steps.
- **Fused operations.** A fused multiply-add adds the third operand into the partial product tree, so that only one rounding and one carry propagation occur.
- **Population count.** The number of ones in a word, used in error-correcting codes and bit manipulation, is a multi-operand sum of single bits; see [population count](/population-count/).
- **Software.** Summing many big integers, or the columns of a [schoolbook product](/schoolbook-multiplication/) computed column by column, as in Comba's product scanning method, uses delayed carries in wide accumulators.

## References
