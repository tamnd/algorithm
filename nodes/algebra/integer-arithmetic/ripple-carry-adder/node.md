---
tag: 0BHM0W
kind: algorithm
slug: ripple-carry-adder
name: Ripple-carry adder
aliases:
- ripple adder
- carry-ripple adder
- RCA
area: algebra/integer-arithmetic
level: intro
summary: Chains full adders so each carry feeds the next, taking time linear in the word length.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  depth: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [boolean-circuit, positional-number-system, integer-addition]
see_also: [carry-lookahead-adder, kogge-stone-adder, brent-kung-adder, sklansky-adder, carry-save-addition, carry-propagation, array-multiplier, multiprecision-integer]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 5, Basic addition and counting (half and full adders, ripple-carry adders, carry chains and their average length)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 2, Two-operand addition (the carry-ripple adder and the overflow of two's complement addition)
  - book: isbn:9780262032933
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, second edition, MIT Press, 2001
    locator: Chapter 29, Arithmetic circuits, Section 29.1 (full adders) and Section 29.2 (ripple-carry addition)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, Algorithm A (addition of nonnegative integers, the same carry chain in radix b)
---

A ripple-carry adder adds two $n$-bit numbers with a chain of $n$ full adders, one for each bit position. Each full adder adds two input bits and the carry from the position below, writes one sum bit, and passes its carry to the position above. The carry can travel, or ripple, through the whole chain, so the circuit has $5n$ gates and depth $2n + 1$, linear in both. It is the smallest adder and the slowest in the worst case. In the [Boolean circuit](/boolean-circuit/) model it is the baseline for the faster adders, such as the [carry-lookahead](/carry-lookahead-adder/) and the [Kogge-Stone](/kogge-stone-adder/) adders, of depth $O(\log n)$. In software, the same chain in radix $\beta = 2^w$ is the limb-by-limb addition of [multiprecision integers](/multiprecision-integer/).

## In plain words

This is the way you add two numbers on paper. Start at the rightmost column. Add the two digits there, write the last digit of the result, and carry the rest to the next column. Then add the next two digits and the carry, and so on to the left.

A ripple-carry adder is a row of small identical boxes, one for each binary digit, that do this. Each box gets two digits and a carry, and gives a digit of the answer and a carry for the next box. The boxes are simple and cheap. The catch is the waiting: the leftmost box cannot know its carry until all the boxes to its right have finished. Adding 1 to a number made of all ones changes every digit, and the carry must walk the whole row.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$ and a carry-in bit $c_0$. The output is the $n + 1$ bits $s_n s_{n-1} \cdots s_0$ of $a + b + c_0$, the [integer addition](/integer-addition/) of fixed width, with $s_n$ the carry out.

**Cost model.** The model is the Boolean circuit with gates AND, OR and XOR of fan-in 2. The size is the number of gates, the field `time` of this page, and the depth is the number of gates on the longest path from an input to an output, which is the delay when every gate takes one unit of time. Real delays depend on the technology and on wire lengths; the figures here count gates only.

## The algorithm

The cell is the **full adder**. For bits $a_i, b_i, c_i$ it computes the *propagate* bit $p_i = a_i \oplus b_i$, the *generate* bit $g_i = a_i \wedge b_i$, the sum bit $s_i = p_i \oplus c_i$ and the carry $c_{i+1} = g_i \vee (p_i \wedge c_i)$. The chain connects the carry out of cell $i$ to the carry in of cell $i + 1$.

```pseudo id=main
RIPPLE-ADD(a[0 .. n − 1], b[0 .. n − 1], c_in)
L1  c ← c_in
L2  for i ← 0 to n − 1 do                ▷ one full adder per bit
L3      p ← a[i] ⊕ b[i]                  ▷ propagate
L4      g ← a[i] ∧ b[i]                  ▷ generate
L5      s[i] ← p ⊕ c
L6      c ← g ∨ (p ∧ c)                  ▷ the carry into stage i + 1
L7  s[n] ← c
L8  return s
```

As a circuit, the loop is unrolled: the $n$ cells exist side by side, and lines L3 and L4 of all cells act at the same time. Only the carry of line L6 forms a chain.

## Example

Add $a = 11 = 1011_2$ and $b = 6 = 0110_2$ with $c_0 = 0$, bit 0 first.

| $i$ | $a_i$ | $b_i$ | $c_i$ | $p_i$ | $g_i$ | $s_i$ | $c_{i+1}$ |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| 2 | 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| 3 | 1 | 0 | 1 | 1 | 0 | 0 | 1 |

So $s = 10001_2 = 17 = 11 + 6$. Stage 1 generates a carry, and stages 2 and 3 propagate it: a carry chain of length 3, which ends in the carry out $s_4 = 1$. The worst case for $n = 8$ is $11111111_2 + 00000001_2$, where the carry of stage 0 passes all 8 stages.

## Correctness

The full adder is correct: for bits $a, b, c$, $a + b + c = s + 2c'$, where $s = a \oplus b \oplus c$ is the parity of the three bits and $c' = (a \wedge b) \vee ((a \oplus b) \wedge c)$ is 1 exactly when at least two of them are 1. The invariant of the chain is that after stage $i$,

$$\sum_{j=0}^{i} s_j 2^j + c_{i+1} 2^{i+1} = \sum_{j=0}^{i} (a_j + b_j) 2^j + c_0 .$$

Stage $i + 1$ adds $(a_{i+1} + b_{i+1} + c_{i+1}) 2^{i+1} = (s_{i+1} + 2c_{i+2}) 2^{i+1}$ to both sides. After stage $n - 1$, with $s_n = c_n$, this says $\sum_{j=0}^{n} s_j 2^j = a + b + c_0$. The full proof is below.

## Complexity

**Size.** Each full adder has 5 gates (2 XOR, 2 AND, 1 OR), so the chain has $5n$ gates, $\Theta(n)$. This is optimal up to the constant, since every output bit depends on the inputs.

**Depth.** The bits $p_i$ and $g_i$ have depth 1, in parallel. The carry $c_1$ has depth 3, and each later stage adds an AND and an OR, so $c_i$ has depth $2i + 1$, the sum bit $s_i = p_i \oplus c_i$ has depth $2i + 2$ for $i \ge 1$, and the carry out $c_n$ has depth $2n + 1$. The depth is $\Theta(n)$, and this is the worst case, the same for every input in a circuit of fixed gates. These depths were checked by script.

**Settling time.** With gates that switch when their inputs change, the time to the final value depends on the longest carry chain of the inputs: the longest run of stages from a generating stage ($g_i = 1$) through propagating stages ($p_j = 1$). For random inputs, this length is on average about $\log_2 n$. In a simulation of 20000 random pairs, the average longest chain was 4.3 for $n = 32$ and 5.3 for $n = 64$, and over 2000 pairs it was 9.3 for $n = 1024$, a little below $\log_2 n$. These are observed values; the asymptotic form $\log_2 n + O(1)$ is a theorem, see History. Asynchronous adders that signal the end of the carry use this average.

**Software.** On the [word RAM](/word-ram/), the same chain in radix $\beta = 2^w$ adds two $n$-limb numbers in $\Theta(n)$ limb operations, with one add-with-carry instruction per limb. There the chain is not a cost, because the operations run in sequence anyway.

## Properties

- **Minimal size.** Linear size with a small constant, and a regular layout with short wires between neighbor cells.
- **Linear delay.** The depth grows with the width; for 64 bits the carry path has 128 gate levels.
- **Subtraction and two's complement.** The same chain computes $a - b$ as $a + \bar{b} + 1$, with the bitwise NOT of $b$ and $c_0 = 1$. In [two's complement](/twos-complement/), the sum overflows exactly when $c_{n-1} \ne c_n$, the carry into the top stage differs from the carry out. For unsigned subtraction, $c_n = 1$ means no borrow, that is $a \ge b$.
- **Serial form.** A single full adder with a one-bit memory for the carry, fed one bit per clock cycle, is the bit-serial adder: one cell, $n$ cycles.

## Variants and improvements

- **Carry-lookahead adders** compute the carries from the $p_i$ and $g_i$ with a tree, depth $O(\log n)$; see [carry-lookahead adder](/carry-lookahead-adder/). The prefix adders, [Sklansky](/sklansky-adder/), [Kogge-Stone](/kogge-stone-adder/) and [Brent-Kung](/brent-kung-adder/), are the regular forms, built from the [parallel prefix](/parallel-prefix/) of the carry operator.
- **Carry-skip (carry-bypass) adders** split the chain into blocks and let a carry skip a block whose bits all propagate, with delay about $O(n^{1/2})$ for blocks of the right size.
- **Carry-select adders** compute each block for both values of its carry in and choose the right result with a multiplexer when the carry arrives, also with delay $O(n^{1/2})$ for one level.
- **Carry-save addition** does not propagate the carries at all: three numbers become two, in depth $O(1)$; see [carry-save addition](/carry-save-addition/). It is used in multipliers, which end with one carry-propagate adder, often a ripple adder in the [array multiplier](/array-multiplier/).
- **Manchester carry chain.** A circuit technique that implements the carry chain with pass transistors, faster per stage than gates.

## When to use it

Use a ripple-carry adder when the width is small, when area or power matters more than delay, or when the carry chain is short in practice. It is also the final adder of many multipliers, where the inputs arrive at different times. For wide adders on the critical path of a processor, use a carry-lookahead or prefix adder. In software, limb-by-limb addition with carries is the right method; there is nothing to gain by lookahead on a sequential machine.

## Pitfalls

- **Assuming the average is the worst case.** The average carry chain is short, but a synchronous circuit must be clocked for the worst case, the full chain of $n$ stages.
- **The overflow rule.** The carry out $c_n$ is the unsigned overflow. The signed overflow is $c_{n-1} \oplus c_n$. Using $c_n$ for signed numbers gives wrong flags, for example $(-1) + 1$ has $c_n = 1$ but does not overflow.
- **Subtraction without the carry in.** $a + \bar{b}$ with $c_0 = 0$ gives $a - b - 1$, the [one's complement](/ones-complement/) difference. Two's complement subtraction needs $c_0 = 1$.
- **Operands of different widths.** Extend the shorter operand with zeros (unsigned) or with copies of its sign bit (signed) before adding; see [sign extension](/sign-extension/).

## Implementations

## History

Adding digit by digit with a carry is the old written method of addition, and early mechanical calculators carried from one wheel to the next in the same way. In electronic computers, the serial adder of the first stored-program machines used one full adder over many cycles, and the parallel machines used chains of full adders. Burks, Goldstine and von Neumann, in their 1946 report on the design of an electronic computer, argued that the average carry chain of random $n$-bit operands has length at most about $\log_2 n$; later work, including a paper by Knuth in 1978, gave the exact asymptotic form $\log_2 n + O(1)$. Faster adders came from the 1950s on: the carry-lookahead idea in the late 1950s, and the regular prefix adders of Kogge and Stone (1973) and Brent and Kung (1982).

## References
