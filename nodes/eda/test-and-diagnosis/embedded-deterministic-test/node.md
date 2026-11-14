---
tag: 8YKT6S
kind: technique
slug: embedded-deterministic-test
name: Embedded deterministic test
aliases:
- EDT
- ring generator decompression
area: eda/test-and-diagnosis
level: advanced
summary: Rajski and coauthors' scan compression that feeds a continuous-flow ring generator and phase shifter from a few tester channels, with variables solved per test cube.
prereqs: [lfsr-reseeding, scan-design, linear-system-modulo-2]
see_also: [broadcast-scan, x-compact, multiple-input-signature-register, xor-gaussian-elimination, rank, linear-feedback-shift-register, gf2-polynomial-arithmetic, automatic-test-pattern-generation]
sources:
  - paper: doi:10.1109/TCAD.2004.826558
    title: Janusz Rajski, Jerzy Tyszer, Mark Kassab and Nilanjan Mukherjee, Embedded deterministic test, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 23(5), 776 to 792, 2004
    locator: the continuous-flow decompressor of a ring generator and a phase shifter, the linear equations solved per test cube, the initialization cycles, the compactor with masking, and the dynamic compaction of cubes during test generation
  - paper: doi:10.1109/TCAD.2004.831584
    title: Grzegorz Mrugalski, Janusz Rajski and Jerzy Tyszer, Ring generators, new devices for embedded test applications, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 23(9), 1306 to 1320, 2004
    locator: the ring generator as a transformed LFSR with the same characteristic polynomial, fewer XOR levels, short feedback wires and small fan-out
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter Test Compression (linear decompressors and continuous-flow decompression)
---

Embedded deterministic test (EDT) loads scan chains through an on-chip linear decompressor that receives new tester bits on every shift cycle. Rajski, Tyszer, Kassab and Mukherjee (2004) feed $c$ tester channels into a ring generator, a compact form of a [linear feedback shift register](/linear-feedback-shift-register/), and a phase shifter of XOR gates spreads its stages over many more scan chains than there are channels. Every scan cell then holds a fixed XOR of the injected tester bits. A test cube from [test generation](/automatic-test-pattern-generation/) can be loaded exactly when the linear system "mask of the cell times variables equals care bit" is consistent over GF(2), the same condition as in [LFSR reseeding](/lfsr-reseeding/), and the tester bits are found by solving it. Unlike reseeding, the variables arrive during the whole shift, so long chains get more variables and there is no pause to load a seed. On the output side, the responses of the many chains are compacted by XOR trees with masking for unknown values.

## In plain words

A chip has hundreds of short test chains, but the tester has only a few wires into it. EDT puts a small scrambler on the chip. On every clock step the tester pushes a few fresh bits into the scrambler, and the scrambler sends a mixture of all the bits it has seen so far into every chain.

Each bit that lands in a chain is an XOR of some of the tester bits, and which ones is known in advance. A test only cares about a few bits. So a computer solves a puzzle of XOR equations, one per bit that matters, to find what the tester should push. If the puzzle has no answer, the test is split in two. The free bits come out scrambled, which also helps catch extra faults.

## When it applies

- The design has [scan design](/scan-design/) with many short chains, and the tester has few channels, so the scan data volume and test time are what the compression must reduce.
- Test cubes have few care bits compared with the number of cells, typically a few percent, and the care bits of one cube spread over the shift cycles rather than piling up in a few.
- The test generator can call the solver while it builds cubes, so that it merges cubes only while the merged cube still encodes.
- The responses can be compacted, and unknown values in the responses are known or can be masked.

## The template

Let the decompressor have a ring generator of $R$ stages, $c$ injection channels, a phase shifter onto $k$ chains of length $\ell$, and $d$ initialization cycles in which the ring is filled before the chains start shifting. The tester supplies $V = c(\ell + d)$ variables per pattern.

```pseudo id=main
EDT-ENCODE(the cube, the decompressor)
L1  for each cell (i, t) compute its mask f_(i,t), the set of variables XORed into it, by simulating the decompressor on symbols
L2  for each care bit (i, t) with value v do
L3      add the row f_(i,t) · x = v and reduce it by the stored rows
L4      if the row becomes 0 = 1 then return FAIL
L5  set the free variables and solve the stored rows by back substitution
L6  return x, as c bits per cycle for ℓ + d cycles
```

The holes are the ring generator (its polynomial and the injection points), the phase shifter (which stages each chain XORs), the number $d$ of initialization cycles, the fill of the free variables in line L5, and what to do on FAIL: drop the last merged cube, or split the cube. Lines L2 to L4 are incremental [Gaussian elimination over GF(2)](/xor-gaussian-elimination/), so the test generator can add care bits one at a time and stop when the next one would make the system inconsistent. Line L1 depends only on the decompressor, so it runs once for all cubes.

**When a cube is encodable.** The decompressor is linear over GF(2): the ring starts at zero, each clock is a linear map of the state plus the injected bits, and each phase shifter output is an XOR of stages. So each cell value is $f_{(i,t)} \cdot x$ for the variable vector $x \in \mathrm{GF}(2)^V$, and a vector $x$ loads the cube exactly when $f_{(i,t)} \cdot x = v_{(i,t)}$ for every care bit. The encodings are the solutions of this [linear system modulo 2](/linear-system-modulo-2/). Elimination finds one when the system is consistent and reaches $0 = 1$ exactly when it is not, so `EDT-ENCODE` returns FAIL exactly when no tester input loads the cube. $\blacksquare$

**How many cubes are encodable.** Fix the care positions and let $r$ be the [rank](/rank/) of their masks. The map $x \mapsto (f_{(i,t)} \cdot x)$ over the $s$ care positions is linear with an image of dimension $r$, so exactly $2^r$ of the $2^s$ value patterns are encodable. Since $r \le \min(s, V)$:

- if the masks are independent, every value pattern on those positions is encodable;
- if $s > V$, at most a fraction $2^{V - s}$ of value patterns is encodable, so cubes with more care bits than variables almost never encode;
- locally, the cells shifted in $j$ consecutive cycles depend only on the ring state at the start of the window, at most $R$ independent forms, and on the $c j$ variables injected during it. So their masks have rank at most $R + c j$, and a cube with more than $R + c j$ care bits in $j$ consecutive cycles fails for most value patterns, however many variables the whole pattern has. $\blacksquare$

The last point is why the size $R$ of the ring matters even though the variables keep coming, and why the first cycles need the $d$ initialization cycles: without them, the cells of the first shift cycle depend on only $c$ variables.

**A measurement.** A toy decompressor shows the effect of $d$. It uses a 16-stage LFSR with the primitive polynomial $x^{16} + x^{12} + x^3 + x + 1$ in place of a ring generator, 2 channels injected at stages 0 and 8, and a phase shifter of 3-input XORs onto 16 chains of 40 cells. Cubes with $s$ care bits at random cells and random values, 1000 per entry, gave these encoding rates.

| care bits $s$ | 10 | 20 | 40 | 60 | 70 | 80 |
|---|---|---|---|---|---|---|
| $d = 0$ (80 variables) | 0.865 | 0.687 | 0.46 | 0.193 | 0.065 | 0.01 |
| $d = 4$ (88 variables) | 1.0 | 1.0 | 0.989 | 0.914 | 0.70 | 0.261 |
| $d = 8$ (96 variables) | 1.0 | 1.0 | 0.998 | 0.961 | 0.808 | 0.454 |

With $d = 0$ even small cubes often fail, from care bits in the first cycles. With a few initialization cycles, more than 90% of the cubes encode up to about 60% as many care bits as variables, and the rate falls quickly beyond that. With $d = 8$, five different phase shifters gave rates from 0.648 to 0.882 at 70 care bits, so the phase shifter matters too. These are measurements of one toy design, not bounds.

## Classic examples

- **EDT (2004).** Rajski, Tyszer, Kassab and Mukherjee combine a ring generator, a phase shifter, injection on every shift cycle, and dynamic compaction in test generation, with an XOR-tree compactor and masking on the output side. Compression ratios grow with the ratio of chains to channels until the care bits per cube approach the variables per pattern.
- **Ring generators.** Mrugalski, Rajski and Tyszer (2004) transform an LFSR into a ring with the same characteristic polynomial but at most one XOR gate between stages, short feedback wires and small fan-out, which keeps the decompressor fast and small. A primitive characteristic polynomial over GF(2) gives the longest period, $2^R - 1$.
- **Static reseeding as a special case.** With all variables injected before the shift starts and none during it, EDT becomes [LFSR reseeding](/lfsr-reseeding/), with the limit that the seed size bounds the care bits of every cube.
- **Broadcast as the simplest case.** If each chain is wired straight to one channel, every cell gets one variable, and EDT becomes [broadcast scan](/broadcast-scan/), where two care bits conflict whenever they share a variable.

## Variations

- **Response compaction.** The $k$ chain outputs are XORed down to a few outputs. Unknown values are blocked by masking chains per pattern, or tolerated by an XOR code as in [X-compact](/x-compact/), or a [MISR](/multiple-input-signature-register/) is used when no X can occur.
- **Low-power fill.** The free variables of line L5 can be chosen so that the decompressor repeats values for long runs, which lowers the switching during shift, at the cost of fewer extra faults detected by chance.
- **Hold and control bits.** Some decompressors let a few control bits per pattern hold the ring or change the injection points, which adds variables where the care bits cluster.
- **Several decompressors.** Large designs use one decompressor per block, each with its own channels, so the equations are solved per block.

## Pitfalls

- **Too few initialization cycles.** With $d$ small, the cells of the first shift cycles depend on very few variables, and cubes with care bits there fail, as the row $d = 0$ above shows. A rule of thumb is $d \approx R / c$, the number of cycles in which $c$ channels can inject $R$ variables, so the ring is filled before the first cell is loaded.
- **Shifted copies in the chains.** If two chains take neighbor stages of the ring with no phase shifter, one gets a delayed copy of the other, and their masks are equal at shifted positions. Care bits at those positions conflict as in broadcast scan. The phase shifter must be built so that the chains get sequences far apart.
- **Counting only total care bits.** A cube with fewer care bits than variables can still fail when its care bits cluster in a few cycles, by the window bound above. Test generators must check encodability, not only the count.
- **The X problem on the output side.** One unknown value in an XOR tree hides all errors in that output and cycle. Plan masking with the decompressor, since the masking bits also use tester data.
- **Comparing with the wrong baseline.** The data per pattern is $c(\ell + d)$ bits, so a compression ratio must count the initialization cycles and the masking data, and the test time grows with $\ell + d$, not with $\ell$.

## Exercises

1. Show that the decompressor with an LFSR, injection points and a phase shifter is linear over GF(2), and write the mask recurrence used in line L1.
2. Prove that if the masks of the care positions are independent, every value pattern on them is encodable, and count the encodings.
3. For the toy decompressor above with $d = 0$, show that the 16 cells of the first shift cycle have masks of rank at most 2, so that at most 4 of the $2^{16}$ value patterns of that cycle can be loaded.
4. Prove the window bound: the cells of $j$ consecutive shift cycles have masks of rank at most $R + c j$.

## References
