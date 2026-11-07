---
tag: FWJCMW
kind: algorithm
slug: carry-skip-adder
name: Carry-skip adder
aliases:
- carry-bypass adder
- CSKA
area: algebra/integer-arithmetic
level: advanced
summary: Skips propagation across a block when all its bits propagate the incoming carry.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  depth: {worst: Θ(n)}
  delay: {worst: Θ(n^(1/2))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Lehman and Burla analysed skip techniques for carry propagation in 1961; the scheme was used in the fast adders of the early transistor computers.
prereqs: [ripple-carry-adder, carry-propagation, boolean-circuit]
see_also: [carry-select-adder, carry-lookahead-adder, ripple-carry-adder, brent-kung-adder, kogge-stone-adder, carry-propagation, integer-addition]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 7, Variations in fast adders, Sections 7.1 and 7.2 (simple carry-skip adders with the optimal uniform block width, and multilevel carry-skip adders)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 2, Two-operand addition (carry-skip adders and the choice of block sizes)
  - book: isbn:9780321547743
    title: Neil H. E. Weste and David Money Harris, CMOS VLSI Design, A Circuits and Systems Perspective, fourth edition, Addison-Wesley, 2011
    locator: Section 11.2.2, Carry-propagate addition (carry-skip adders and their critical path)
---

A carry-skip adder is a [ripple-carry adder](/ripple-carry-adder/) cut into blocks, with a shortcut around each block. For every block, an AND of the propagate signals $p_i = a_i \oplus b_i$ tells whether the whole block would pass on an incoming carry. If it would, a multiplexer sends the carry into the block straight to the carry out, without waiting for it to ripple through. If it would not, the carry out of the block does not depend on the carry in, and the block's own ripple produces it early. Either way a carry crosses each block in two gate delays, and only the first and the last block need a full ripple. With blocks of about $\sqrt{n/2}$ bits, the worst delay is about $4\sqrt{2n}$ gate delays, at a cost of a few gates per block. There is a catch that every analysis of this adder has to face: the long ripple path through all blocks still exists in the circuit. It is a *false path*, one that no input can make slow, so the speed-up shows in the delay, which depends on the data, and not in the depth of the circuit.

## In plain words

In a plain adder, a carry walks from position to position, and the slowest case is a carry that has to walk the whole way. That happens only when the positions it passes all say "pass it on".

A carry-skip adder cuts the number into blocks and checks each block in advance: does every position in this block say "pass it on"? That check uses only the inputs, so it is ready early. If the answer is yes, the carry jumps over the block in one step. If the answer is no, some position inside the block makes or stops a carry by itself, so the block's carry out was settled early, without the incoming carry. The carry still walks inside the first and the last block, but it jumps over the middle ones.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$, with $n \ge 1$, a carry-in bit $c_0$, and block sizes $k_0, \ldots, k_{t-1} \ge 1$ with sum $n$, low block first. The output is the $n + 1$ bits of $a + b + c_0$, the fixed-width [integer addition](/integer-addition/).

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR, XOR and NOT gates, at most two inputs each and unit delay. Three measures are used. The *size*, the field `time`, is the number of gates. The *depth* is the longest path in the circuit, counted without looking at the data. The *delay*, the custom field `delay`, is the time at which all outputs have settled, maximized over the inputs, where a gate settles one unit after a *controlling* input settles (a 0 for AND, a 1 for OR) or else one unit after its last input: this is the usual floating-mode timing of logic. The delay bound below is proved for all block sizes; that it is attained was checked by exhaustive search for $n \le 7$ and by an explicit input for larger $n$. The depth formula is proved.

## The algorithm

Each position has $g_i = a_i \wedge b_i$ and $p_i = a_i \oplus b_i$, and the ripple step is $s_i = p_i \oplus c_i$, $c_{i+1} = g_i \vee (p_i \wedge c_i)$. For a block $j$, $P_j$ is the AND of its $p_i$.

```pseudo id=main
CARRY-SKIP-ADD(a, b, c_in, k[0..t − 1])          ▷ n bits, low first; blocks of sizes k[j]
L1  for all i in parallel: g[i] ← a[i] ∧ b[i];  p[i] ← a[i] ⊕ b[i]
L2  for each block j ≥ 1, in parallel: P[j] ← the AND of p[i] over the block, by a tree of two-input gates
L3  c ← c_in
L4  for j ← 0 to t − 1 do
L5      x ← c                                    ▷ the carry into block j
L6      for each position i of block j, low first: s[i] ← p[i] ⊕ c;  c ← g[i] ∨ (p[i] ∧ c)
L7      if j ≥ 1 then c ← (P[j] ∧ x) ∨ (¬P[j] ∧ c)   ▷ the skip multiplexer
L8  return s[0 .. n − 1] and the carry out c
```

Block 0 has no skip, since its carry-in is an input and arrives at time 0. Line L7 is a full multiplexer, not the simpler $c \vee (P_j \wedge x)$ of some textbook figures. With the OR form, a block whose carry-in is 0 and whose positions all propagate would have to wait for the 0 to ripple through it before its output settles, and the delay would grow back to order $n$ on inputs like $0111 \cdots 1 + 0$ with carry-in 1. The term $\neg P_j \wedge c$ is 0 as soon as $P_j = 1$ is known, so the multiplexer settles from $x$ alone.

## Example

Add $a = \texttt{9A3C}_{16}$ and $b = \texttt{65C4}_{16}$ with $c_0 = 0$, $n = 16$ and four blocks of 4 bits. The nibbles are written high bit first.

| block $j$ | $a$ nibble | $b$ nibble | $g$ (L1) | $P_j$ (L2) | carry in $x$ (L5) | sum (L6) | carry out (L7) |
|---|---|---|---|---|---|---|---|
| 0 | 1100 | 0100 | 0100 | | 0 | 0000 | 1, by ripple |
| 1 | 0011 | 1100 | 0000 | 1 | 1 | 0000 | 1, skipped |
| 2 | 1010 | 0101 | 0000 | 1 | 1 | 0000 | 1, skipped |
| 3 | 1001 | 0110 | 0000 | 1 | 1 | 0000 | 1, skipped |

Position 2 generates a carry; it ripples through position 3 to the end of block 0, and then every later block passes it on. The result is $1\,0000\,0000\,0000\,0000_2 = 2^{16} = \texttt{9A3C}_{16} + \texttt{65C4}_{16}$. On this input the outputs settle at time 15. The same circuit without the skips, a 16-bit ripple-carry adder, settles at time 28 on it, because the carry has to pass 13 positions. The worst delay of this 4-by-4 adder over all inputs is 20, and its depth is 39, the length of the false path through all 16 ripple steps and three multiplexers.

## Correctness

The skip changes the timing but not the values. If $P_j = 0$, line L7 keeps the ripple carry $c$. If $P_j = 1$, every position of block $j$ has $p_i = 1$ and $g_i = 0$, so each ripple step gives $c_{i+1} = c_i$ and the ripple carry out of the block equals its carry in $x$; line L7 outputs $x$. In both cases line L7 outputs the ripple carry out, so the whole circuit computes the same values as a ripple-carry adder with carry-in $c_0$, which are the bits of $a + b + c_0$. The full proof is below.

## Complexity

**Size, proved.** Line L1 has $2n$ gates, the ripple steps $3n$, each AND tree $k_j - 1$ gates, and each multiplexer 4 gates (two ANDs, a NOT and an OR). The size is at most $6n + 4t = \Theta(n)$. For $n = 16$ with four blocks it is 101 gates; for $n = 1024$ with blocks of 32 it is 6205.

**Depth, proved.** The path from $c_0$ through every ripple step and every multiplexer has $2n + 1 + 2(t - 1) = 2n + 2t - 1$ gates, counting the last sum XOR, and no path is longer. So the depth is $\Theta(n)$, larger than that of a plain ripple-carry adder. A static timing tool that only looks at the graph reports this path; designers mark it as a false path.

**Delay, proved bound.** Write $T_j$ for a time by which the carry into block $j$ has settled, on every input. The bounds are:

- In block 0, $c_i$ settles by $2i + 1$, so the sums settle by $2k_0$ and $T_1 = 2k_0 + 1$.
- In a block $j \ge 1$, the internal carry $m$ places above its start settles by $T_j + 2m$, so its sums settle by $T_j + 2k_j - 1$.
- The carry out of block $j \ge 1$ settles by $T_{j+1} = \max(T_j + 2, 2k_j + 3)$. If $P_j = 1$, the term $\neg P_j \wedge c$ settles to 0 by time $3 + \lceil \log_2 k_j \rceil$, the term $P_j \wedge x$ by $\max(T_j, 1 + \lceil \log_2 k_j \rceil) + 1$, and the OR one unit later. If $P_j = 0$, let $q$ be the highest position of the block with $p_q = 0$; the ripple carry out of $q$ settles by time 3 whatever the carry in, and the $k_j - 1$ or fewer steps above it by $2k_j + 1$, which with the multiplexer gives $2k_j + 3$.

The delay is at most the largest of these sum times and $T_t$. For $t$ uniform blocks of size $k \ge 2$, this is $T_j = 2k + 2j - 1$ and a delay of at most $4k + 2t - 4$. With $k \approx \sqrt{n/2}$ and $t \approx \sqrt{2n}$ it is about $4\sqrt{2n} \approx 5.66\sqrt{n}$: for $n = 64$ the best uniform size is $k = 5$ with delay 40, for $n = 256$ it is $k = 10$ with 86, and for $n = 1024$ it is $k = 21$ with 176, against $2n + 1 = 2049$ for ripple. So the delay is $O(\sqrt{n})$.

**Delay, observed.** The test script computes the largest settle time over all inputs for every $n \le 6$ and several block schedules, and it equals the bound each time. The input $a = 2^n - 2$, $b = 0$, $c_0 = 1$ reaches the bound for $n = 8, 16, 64, 256$ and all uniform blocks up to 19 bits: the carry-in 1 is killed at position 0, and the 0 that leaves position 0 ripples through block 0 and the last block, since every other position propagates. The lower bound $\Omega(\sqrt{n})$ for one-level skip with uniform blocks follows from the formula: the first block costs $2k$ and the chain $2t$, and $2k + 2n/k \ge 4\sqrt{n}$.

**Simulation.** Evaluating the circuit sequentially costs time proportional to its size, $\Theta(n)$.

## Properties

- **Almost no extra hardware.** Per block, an AND tree and a multiplexer: about $6n$ gates against $5n$ for ripple, far less than the doubled blocks of a [carry-select adder](/carry-select-adder/).
- **Delay depends on the data.** The adder is fast because no input can make the long path slow, not because the path is absent. Its speed is a property of the delay model, so it suits technologies where a settled controlling input really ends the switching, such as static CMOS with a multiplexer per block or Manchester carry chains.
- **Order $\sqrt{n}$, like carry select.** One level of skipping gives $\Theta(\sqrt{n})$ delay for uniform blocks; better block schedules improve the constant, and more levels improve the exponent.
- **Hard for timing tools.** Because the depth is larger than the delay, a design that uses carry skip must declare the false paths to static timing analysis, or the tool reports the adder as slower than a ripple adder.

## Variants and improvements

- **Variable block sizes.** Blocks that grow from both ends toward the middle balance the ripple at the two ends against the skips in the middle and lower the delay constant; Oklobdzija and Barnes gave optimal schedules in 1985.
- **Multilevel skip.** Groups of blocks get their own propagate signal and skip, as in a tree; with enough levels the delay approaches $O(\log n)$, and the structure approaches a [carry-lookahead adder](/carry-lookahead-adder/).
- **OR form with reset.** The cheaper form $c \vee (P_j \wedge x)$ is correct and is fast for carries of value 1; in dynamic logic, where all carries start at 0 in each cycle, a 0 never has to propagate, and the OR form suffices.
- **Carry skip with carry select.** Hybrid adders use skip logic between blocks and selection or lookahead inside them.

## When to use it

Use a carry-skip adder when area and power are tight and a ripple-carry adder is too slow: medium widths in low-power circuits, and FPGA designs with fast built-in carry chains. It gives most of the speed of a [carry-select adder](/carry-select-adder/) with a fraction of the extra hardware. When the delay must be logarithmic, or when the design flow cannot handle false paths, use a [Brent-Kung](/brent-kung-adder/) or [Kogge-Stone](/kogge-stone-adder/) adder instead. In software, none of this applies: the processor's add instruction already adds a whole word.

## Pitfalls

- **The OR form of the skip.** Writing line L7 as $c \leftarrow c \vee (P_j \wedge x)$ computes the right value, but when $x = 0$ and $P_j = 1$ the output is 0 only after the 0 has rippled through the block, so the delay is of order $n$ on inputs such as $a = 2^n - 2$, $b = 0$, $c_0 = 1$. The multiplexer $(P_j \wedge x) \vee (\neg P_j \wedge c)$ of line L7 settles from $x$ alone when $P_j = 1$.
- **Skipping block 0.** A skip around block 0 is useless, since its carry-in arrives at time 0 and its delay is set by its own ripple. Line L7 starts at $j = 1$.
- **Reading the depth as the delay.** The depth $2n + 2t - 1$ is larger than ripple's $2n + 1$. Claims of $O(\sqrt{n})$ refer to the delay, the settle time over inputs, and depend on controlling values; a model that charges every gate its latest input (the depth) shows no gain at all.
- **Blocks too large or too small.** With uniform blocks the delay $4k + 2t - 4$ is minimized near $k = \sqrt{n/2}$. Blocks of 1 bit give $2n + 1$, the same as ripple, and one block of $n$ bits is ripple.

## Implementations

## History

Skip techniques appear in the fast adders of the first transistor computers. Lehman and Burla analysed them in 1961, together with the choice of block sizes, and the Manchester carry chain of the late 1950s made a block-level bypass cheap to build. Majerski (1967) and later Oklobdzija and Barnes (1985) studied optimal block sizes for one and several levels. The false-path problem, that the static depth of the circuit hides its real speed, became a standard example in the timing-analysis literature of the 1980s and 1990s, and it is why modern designs use the multiplexer form.

## References
