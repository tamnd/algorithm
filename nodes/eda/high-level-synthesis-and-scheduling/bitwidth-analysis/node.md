---
tag: 39ZVKP
kind: technique
slug: bitwidth-analysis
name: Bitwidth analysis
aliases:
- bit-width analysis
- value range analysis for hardware
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Propagates value ranges forward and backward through a program to find the fewest bits each variable needs, so the synthesized datapath is narrower.
prereqs: [abstract-interpretation, interval-arithmetic, twos-complement]
see_also: [interval-domain, widening-operator, dataflow-analysis, kleene-fixed-point-theorem, sparse-conditional-constant-propagation, operation-chaining, module-selection, resource-binding]
sources:
  - paper: doi:10.1145/358438.349317
    title: Mark Stephenson, Jonathan Babb and Saman Amarasinghe, Bitwidth analysis with application to silicon compilation, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2000), ACM SIGPLAN Notices 35(5), 108 to 120, 2000
    locator: the Bitwise compiler, the forward and backward propagation of data ranges, the use of array bounds, type casts and loop trip counts, and the results for silicon compilation
  - paper: doi:10.1145/512950.512973
    title: Patrick Cousot and Radhia Cousot, Abstract interpretation, a unified lattice model for static analysis of programs by construction or approximation of fixpoints, Proceedings of the 4th ACM Symposium on Principles of Programming Languages, 238 to 252, 1977
    locator: the abstract interpretation framework, the interval example and the widening operator
---

Bitwidth analysis finds, for each variable and operation of a program, a range of integers that contains every value it can take, and from that range the fewest bits that hold it. In software a 32-bit add costs the same as an 8-bit one, but in hardware made by [high-level synthesis](/high-level-synthesis/) the width sets the size and delay of each adder, multiplier, register and wire. C code declares most variables as `int`, so a compiler that trusts the declared types builds a datapath far wider than the values need. Stephenson, Babb and Amarasinghe (2000) built the Bitwise compiler for this: it runs an [abstract interpretation](/abstract-interpretation/) over [intervals](/interval-arithmetic/), with forward rules that compute the range of a result from the ranges of its operands, and backward rules that narrow the operands from what the uses of a result need. They measured the savings in the area and power of the hardware that their silicon compiler made from the narrowed programs. The analysis is sound: the computed width never cuts off a value that the program can produce. It is not exact: the true range can be smaller.

## In plain words

A variable declared as a 32-bit number often holds only small values, for example a pixel from 0 to 255. If the tool can prove that, the hardware for that variable needs only 8 wires instead of 32. The tool walks through the program and keeps, for each value, the smallest and largest number it can be. Adding two pixels gives at most 510, so 9 bits. It also walks backward: if a result is cut to its low 8 bits at the end, the steps that feed it only need their low 8 bits too. Fewer bits give smaller, faster and cooler circuits.

## When it applies

It applies when a program written for a processor is turned into hardware: HLS from C or C++, compilation to FPGAs, and custom accelerators. It also helps in software for packing values into narrow registers and SIMD lanes. It needs ranges for the inputs, which come from the declared types of the inputs, from interface specifications such as an 8-bit pixel or a 12-bit sensor, or from assertions in the code. It does most for code with small inputs, masks, shifts and array indices, and least for code whose values really fill their types, such as hash functions.

## The template

Each variable gets an interval $[l, h]$ of integers. The analysis computes intervals by rules that are sound: if every operand lies in its interval, the result lies in the result interval.

1. **Seed.** Inputs get the range of their type or of their specification. A constant $k$ gets $[k, k]$.
2. **Forward rules.** For $x \in [a, b]$ and $y \in [c, d]$:
   - $x + y \in [a + c,\ b + d]$ and $x - y \in [a - d,\ b - c]$;
   - $x \cdot y \in [\min P,\ \max P]$ with $P = \{ac, ad, bc, bd\}$;
   - $x \mathbin{\&} y \in [0,\ d]$ if $c \ge 0$, and $x \mathbin{\&} y \in [0,\ \min(b, d)]$ if also $a \ge 0$;
   - $x \ll k \in [a 2^k,\ b 2^k]$ and $x \gg k \in [\lfloor a / 2^k \rfloor,\ \lfloor b / 2^k \rfloor]$ for a constant $k \ge 0$, where $\gg$ is the arithmetic shift;
   - at a join of control flow, such as a [phi function](/phi-function/), the hull $[\min l_i, \max h_i]$ of the incoming intervals;
   - after a test such as `if (x < k)`, the interval $[a, \min(b, k - 1)]$ on the true branch.
3. **Loops.** Iterate the rules until the intervals stop changing. Since an interval can grow one step per pass, apply a [widening operator](/widening-operator/) that jumps an unstable bound to the end of the type, or use the trip count when it is known. Bitwise uses known trip counts, array bounds and type casts to get tighter ranges than widening gives.
4. **Backward rules.** A use can narrow its operands. If a value is used only through its low $k$ bits, for example in `r & 0xFF` or a store to an 8-bit array, then for $+$, $-$, $\times$, $\&$, $|$, $\oplus$ and $\ll$, only the low $k$ bits of the operands matter, and the operation can be built $k$ bits wide. A use as an array index also bounds the index by the array size, for a program that does not access out of bounds.
5. **Overflow.** The rules compute in the integers. If an interval leaves the range of the declared type, the program wraps around, and the true values are no longer in the interval. Then set the interval to the full range of the type, unless the wrap is what the program means, in which case keep the low bits as in step 4.
6. **Width.** An interval $[l, h]$ with $l \ge 0$ needs the unsigned width $w = \max(1, \lceil \log_2(h + 1) \rceil)$, the bit length of $h$. An interval with $l < 0$ needs the signed [two's complement](/twos-complement/) width $w = 1 + \max(\lceil \log_2(-l) \rceil, \lceil \log_2(h + 1) \rceil)$, that is, one sign bit plus the larger of the bit lengths of $-l - 1$ and $h$.

**Soundness of the forward rules.** Take $x \in [a, b]$ and $y \in [c, d]$.

- *Add and subtract.* From $a \le x \le b$ and $c \le y \le d$, adding gives $a + c \le x + y \le b + d$, and since $-d \le -y \le -c$, also $a - d \le x - y \le b - c$.
- *Multiply.* For a fixed $y$, the map $x \mapsto x y$ is linear, so on $[a, b]$ it lies between its values at $a$ and $b$. So $x y$ lies between the least and largest of $a y$ and $b y$. Each of these is linear in $y$, so on $[c, d]$ it lies between its values at $c$ and $d$. Together, $x y$ lies between the least and largest of $ac, ad, bc, bd$.
- *And.* Read integers in two's complement with infinitely many bits, as in the [two's complement](/twos-complement/) page, so a nonnegative number has only finitely many 1 bits and a negative one has infinitely many. If $y \ge 0$, then $x \mathbin{\&} y$ has a 1 bit only where $y$ has one. So it has finitely many 1 bits and is nonnegative, and it is a sum of a subset of the powers of 2 that make up $y$, so it is at most $y \le d$. If also $x \ge 0$, the same holds with $x$, so $x \mathbin{\&} y \le \min(x, y) \le \min(b, d)$.
- *Shifts.* $x \ll k = 2^k x$ and $x \gg k = \lfloor x / 2^k \rfloor$ are nondecreasing functions of $x$, so they map $[a, b]$ into the interval between their values at $a$ and $b$.
- *Joins and tests.* A value that reaches a join comes from one of the incoming edges, so it lies in one of the incoming intervals and so in their hull. On the true branch of `x < k`, the value also satisfies $x \le k - 1$.

By induction over the operations in the order of the program, every computed interval of straight-line code contains every value that the variable takes, as long as no value wraps, which step 5 guards. For loops, the result of step 3 is an interval for each variable that the rules map into itself and that contains the values on entry. Such a post-fixed point contains the values of every iteration, by induction on the number of iterations; this is the soundness theorem of abstract interpretation (Cousot and Cousot, 1977), and widening only makes the intervals larger.

**Soundness of the backward rule for low bits.** Taking the low $k$ bits is the map $x \mapsto x \bmod 2^k$, and it respects $+$, $-$ and $\times$: $(x + y) \bmod 2^k = ((x \bmod 2^k) + (y \bmod 2^k)) \bmod 2^k$, and the same for $-$ and $\times$, since $2^k$ divides the difference of the two sides. Bit $i$ of $x \mathbin{\&} y$, $x \mid y$ and $x \oplus y$ depends only on bit $i$ of $x$ and $y$. And $(x \ll j) \bmod 2^k = ((x \bmod 2^k) \ll j) \bmod 2^k$. So if only the low $k$ bits of a result are used, operands that agree in their low $k$ bits give the same used value, and a $k$-bit datapath computes it. The rule does not hold for right shifts, division, remainder or compares, whose low bits depend on high bits of the operands.

**Soundness of the width.** For $l \ge 0$, $w$ bits hold every integer in $[0, 2^w - 1]$, and $h < 2^w$ when $w$ is the bit length of $h$. For $l < 0$, $w$ bits in two's complement hold every integer in $[-2^{w-1}, 2^{w-1} - 1]$. With $w - 1 \ge$ the bit length of $-l - 1$, we have $-l - 1 \le 2^{w-1} - 1$, so $l \ge -2^{w-1}$; and with $w - 1 \ge$ the bit length of $h$, we have $h \le 2^{w-1} - 1$. So every value in $[l, h]$ fits. One bit less fails for one of the two ends, so the formula gives the fewest bits for the interval, though not always for the true set of values.

## Classic examples

**An average of 16 pixels.** Take `x[16]` with 8-bit unsigned pixels, so each $x_i \in [0, 255]$, and

```
acc = 0
for (i = 0; i < 16; i++) acc = acc + x[i]
y = acc >> 4
z = (y * 3) & 0x3FF
d = x[0] - y
```

where every variable is declared `int`, 32 bits.

| Variable | Interval | Bits |
| --- | --- | --- |
| `acc` after the loop | $[0, 4080]$ | 12 |
| `y` | $[0, 255]$ | 8 |
| `y * 3` | $[0, 765]$ | 10 |
| `z` | $[0, 765]$ | 10 |
| `d` | $[-255, 255]$ | 9, signed |
| `i` | $[0, 16]$ | 5 |

The loop runs 16 times, and after $j$ passes $\mathrm{acc} \in [0, 255 j]$, so the trip count gives $[0, 16 \cdot 255] = [0, 4080]$, which is 12 bits. Plain widening would see the upper bound grow at each pass and move it to the top of the type, which keeps `acc` at 32 bits, so the trip count matters here. The shift gives $[\lfloor 0/16 \rfloor, \lfloor 4080/16 \rfloor] = [0, 255]$. The mask $\mathtt{0x3FF} = 1023$ gives $[0, \min(765, 1023)]$, and it does not narrow `z` further. For `d`, the subtract rule gives $[0 - 255, 255 - 0]$, and the width formula gives $1 + \max(8, 8) = 9$ bits. In place of 32 bits each, the variables `acc`, `y`, `z`, `d` and `i` need 12, 8, 10, 9 and 5 bits, and the loop needs a 12-bit adder.

**Low bits only.** In `w = (a * b + c) & 0xFF` with 32-bit `a`, `b` and `c`, the forward rules give no gain, since the product of two full 32-bit ranges is wide. The backward rule shows that only the low 8 bits of `a`, `b` and `c` matter, so an 8-bit multiplier that keeps the low 8 bits of the product and an 8-bit adder compute `w`. A 32 by 32 multiplier is replaced by an 8 by 8 one.

**Loop counters.** A counter `for (i = 0; i < n; i++)` with `n` known to be at most 100 has $i \in [0, 100]$, 7 bits, and the compare `i < n` needs only 7 bits.

## Variations

- **Value range propagation in compilers.** The same intervals drive the removal of bound checks and of dead branches. Constant propagation, such as [sparse conditional constant propagation](/sparse-conditional-constant-propagation/), is the case of intervals of one value.
- **Bit-level analysis.** Instead of intervals, track for each bit whether it is known to be 0, known to be 1, or unknown. This catches masks and alignments that intervals miss, such as a value that is always a multiple of 8, and the two analyses can run together.
- **Fixed-point formats.** For signal processing code in real numbers, the same propagation finds the integer bits of a fixed-point format, and an error analysis finds the fraction bits.
- **Profiling.** Run the program on test data and record the ranges. This gives narrower widths, but it is not sound: an input outside the tests can overflow. Use it only with a run-time check or a proof.
- **Better domains.** Intervals lose the relations between variables. Relational domains, such as octagons or polyhedra, keep relations like $x \le y$ and give tighter ranges, at a higher cost.

## Pitfalls

- **Wrap-around.** The interval rules hold in the integers. Code that relies on wrap-around, such as hash functions and checksums, leaves the range of its type, and the analysis must fall back to the full width or to the low-bits rule.
- **Too wide after widening.** Widening jumps to the end of the type, so loops without known trip counts often keep their full width. Use loop bounds, assertions or the low-bits rule.
- **Signed and unsigned.** A negative lower bound costs a sign bit. Mixing signed and unsigned operands in C converts the signed one to unsigned, which changes the range of a negative value to a large positive one.
- **Undefined behavior.** The backward rule from array bounds assumes that the program never indexes out of bounds. If it can, narrowing the index hides the bug in hardware.
- **Interfaces.** The widths of the ports of a module are part of its interface. Narrow the internal signals freely, but change the ports only together with the code that drives them.
- **Not exact.** The interval of `x - x` is $[a - b, b - a]$, not $[0, 0]$, since intervals forget that the two operands are equal. The computed widths are upper bounds.

## Exercises

1. Compute the intervals and widths of `s = a * b + c` for 10-bit unsigned `a` and `b` and a 12-bit signed `c`.
2. Show that for $x \in [-4, 3]$ and $y \in [-4, 3]$, the interval rule for $x \mathbin{\&} y$ cannot use $[0, \min(b, d)]$, and give a sound interval.
3. Give a loop for which widening returns the full width but a known trip count gives a small one, and compute both.
4. Prove that $(x \gg 1) \bmod 2^k$ is not determined by $x \bmod 2^k$, and explain what this means for the backward rule.

## References
