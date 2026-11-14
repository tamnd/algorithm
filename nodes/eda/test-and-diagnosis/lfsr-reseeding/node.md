---
tag: NQ6987
kind: technique
slug: lfsr-reseeding
name: LFSR reseeding
aliases:
- Koenemann reseeding
area: eda/test-and-diagnosis
level: advanced
summary: Koenemann's test compression that stores a seed per test cube and expands it with an LFSR, the seed found by solving linear equations over GF(2) for the care bits.
prereqs: [linear-feedback-shift-register, built-in-self-test, linear-system-modulo-2]
see_also: [embedded-deterministic-test, broadcast-scan, xor-gaussian-elimination, rank, scan-design, automatic-test-pattern-generation, multiple-input-signature-register, berlekamp-massey]
sources:
  - paper: "B. Koenemann, LFSR-coded test patterns for scan designs, Proceedings of the European Test Conference, Munich, 237 to 242, 1991"
    title: B. Koenemann, LFSR-coded test patterns for scan designs, Proceedings of the European Test Conference, Munich, 237 to 242, 1991
    locator: the coding of a test cube as an LFSR seed found from linear equations in the care bits, and the rule that an LFSR of s_max + 20 stages fails with probability about 10^-6
  - paper: "S. Hellebrand, J. Rajski, S. Tarnick, S. Venkataraman and B. Courtois, Built-in test for circuits with scan based on reseeding of multiple-polynomial linear feedback shift registers, IEEE Transactions on Computers 44(2), 223 to 233, February 1995"
    title: S. Hellebrand, J. Rajski, S. Tarnick, S. Venkataraman and B. Courtois, Built-in test for circuits with scan based on reseeding of multiple-polynomial linear feedback shift registers, IEEE Transactions on Computers 44(2), 223 to 233, February 1995
    locator: the multiple-polynomial LFSR, where a code selects one of several feedback polynomials for each seed, so that about s_max + 4 stages suffice
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter Test Compression (linear decompressors, reseeding and the solution of the linear equations)
---

LFSR reseeding is a way to store a test pattern in fewer bits than it has. A test pattern from [automatic test pattern generation](/automatic-test-pattern-generation/) is a test cube: most of its bits are don't-cares, and only a few, the care bits, must have given values. Koenemann (1991) stores, for each cube, only a seed for an on-chip [linear feedback shift register](/linear-feedback-shift-register/), chosen so that the LFSR output matches the cube at every care bit. Each LFSR output bit is a fixed XOR of seed bits, so the seed is a solution of a linear system over GF(2) with one equation per care bit, and the cube can be stored this way exactly when that system is consistent. An LFSR a little longer than the largest number of care bits makes almost every cube encodable.

## In plain words

A test for one fault fixes a few input bits and leaves the rest free. Storing the whole pattern wastes space on the free bits.

A shift register with XOR feedback can make long streams from a short start value, the seed. Each bit it makes is the XOR of some bits of the seed, and which ones is known in advance. So asking "which seed gives these few fixed bits?" is a small puzzle of XOR equations, one equation per fixed bit. A computer solves it before the test. The tester then stores only the seed, and the chip grows the full pattern from it.

The puzzle has no answer when the fixed bits conflict with the way the register mixes bits. A register a bit longer than the number of fixed bits almost always gives an answer.

## When it applies

- The circuit has [scan design](/scan-design/), so a test is one load of the scan cells, and the scan cells can be filled from an on-chip generator instead of the tester.
- The test cubes have few care bits. For a single fault, a cube often fixes a few percent of the cells, and the largest count $s_{\max}$ over all cubes decides the size of the LFSR.
- The design can afford an LFSR of $n \approx s_{\max} + 20$ stages, and the tester can load $n$ bits of seed per pattern. A plain [built-in self-test](/built-in-self-test/) LFSR can be reused, which is how reseeding tops up the coverage of random patterns.

## The template

The LFSR has $n$ stages and a tap set $T \subseteq \{1, \ldots, n\}$. Its output stream starts with the seed bits and then follows the recurrence

$$a_t = s_t \ (0 \le t < n), \qquad a_t = \bigoplus_{i \in T} a_{t-i} \ (t \ge n).$$

The tap set $T$ belongs to the feedback polynomial $x^n + \sum_{i \in T} x^{n-i}$. A test cube $c_0 c_1 \ldots c_{L-1}$ over $\{0, 1, X\}$ is written in the order in which its bits leave the LFSR. With one scan chain of length $L$ fed straight from the output, the bit $a_t$ ends in cell $L - 1 - t$, since the first bit out is shifted deepest.

By induction on $t$, every $a_t$ is the XOR of a fixed set of seed bits, written as an $n$-bit mask $f_t$: $f_t$ is the unit vector $e_t$ for $t < n$, and $f_t = \bigoplus_{i \in T} f_{t-i}$ after that. So $a_t = f_t \cdot s$, the dot product over GF(2).

```pseudo id=main
RESEED(n, T, the cube c_0 ... c_(L-1))
L1  f_0, ..., f_(L-1) ← the output masks: f_t = e_t for t < n, else XOR of f_(t-i) over i in T
L2  for each t with c_t ≠ X do
L3      (m, v) ← (f_t, c_t), reduced by the stored rows whose leading bit is set in m
L4      if m = 0 and v = 1 then return FAIL
L5      if m ≠ 0 then store (m, v) as the row with leading bit the top bit of m
L6  s ← 0
L7  for the stored rows in increasing order of leading bit do set that bit of s so that m · s = v
L8  return s
```

The holes are the generator (the size $n$, the taps $T$, and a phase shifter when one LFSR feeds many chains), the map from output times to scan cells, and the fill of the free seed bits in line L6. Lines L2 to L5 are [Gaussian elimination over GF(2)](/xor-gaussian-elimination/), one row at a time, and line L7 is back substitution: every other bit of a stored row is below its leading bit, so it is already fixed when the row is reached.

**Why the answer is exact.** A seed $s$ makes the LFSR produce the cube exactly when $f_t \cdot s = c_t$ for every care position $t$, since $a_t = f_t \cdot s$. So the encoding seeds are the solutions of a [linear system modulo 2](/linear-system-modulo-2/). Elimination finds a solution when one exists, and it reaches a row $0 = 1$ exactly when the rows are dependent in a way that their values contradict. So `RESEED` fails exactly when no seed encodes the cube. When the system is consistent and its [rank](/rank/) is $r$, exactly $2^{n-r}$ seeds encode the cube.

**What is always encodable.** If $n \in T$, then any $n$ consecutive output bits $a_j, \ldots, a_{j+n-1}$ can take any values. The window at $j$ fixes the window at $j - 1$, since the recurrence for $a_{j+n-1}$ contains $a_{j-1}$ with coefficient 1 and the other terms are in the window. So by induction the window at $j$ fixes the seed, the map from seeds to windows is one to one, and as both sets have $2^n$ elements it is onto. So a cube whose care bits fit in $n$ consecutive positions always has a seed.

**What is not.** Having at most $n$ care bits is not enough. For $x^3 + x + 1$, the tap set is $\{2, 3\}$, so $a_{t+3} = a_{t+1} \oplus a_t$ for every $t$. A cube with $c_t = 1$, $c_{t+1} = 0$ and $c_{t+3} = 0$ has only 3 care bits, but it asks for $0 = 1 \oplus 0$, and no seed of the 3-stage LFSR gives it.

**How large an LFSR.** Suppose, as a model, that the $s$ masks of the care bits behave like independent uniform vectors of $\mathrm{GF}(2)^n$. Row $i + 1$ falls in the span of the first $i$ with probability at most $2^{i-n}$, so all $s$ are independent, and the cube is encodable, with probability at least $1 - \sum_{i<s} 2^{i-n} > 1 - 2^{s-n}$. For $n = s + 20$ the failure chance is below $2^{-20} \approx 10^{-6}$, which is Koenemann's rule of $s_{\max} + 20$ stages. This is a model of the masks, not a theorem about a given LFSR: real masks are not random, and the "what is not" case above is a set of 3 dependent masks out of 3. A measurement shows how close the model is. For the 24-stage LFSR with the primitive polynomial $x^{24} + x^7 + x^2 + x + 1$, cubes of length 400 with $s$ care bits at random positions and random values, 2000 cubes per row (seed 2026), gave these rates.

| care bits $s$ | 16 | 20 | 22 | 24 |
|---|---|---|---|---|
| encodable, measured | 0.9985 | 0.9655 | 0.8675 | 0.6000 |
| encodable, random-mask model | 0.9980 | 0.9692 | 0.8826 | 0.6103 |

The model value counts that a dependent row is still consistent with probability $1/2$, so it is above the bound $1 - 2^{s-n}$.

**Example.** Take $n = 4$ and $x^4 + x + 1$, so $T = \{3, 4\}$ and $a_t = a_{t-3} \oplus a_{t-4}$. The masks of the first ten outputs are $s_0$, $s_1$, $s_2$, $s_3$, $s_0 + s_1$, $s_1 + s_2$, $s_2 + s_3$, $s_0 + s_1 + s_3$, $s_0 + s_2$ and $s_1 + s_3$. The cube XX1X0XX1X0 has the care bits $c_2 = 1$, $c_4 = 0$, $c_7 = 1$ and $c_9 = 0$. Line L5 stores $s_2 = 1$ (leading bit 2), $s_0 + s_1 = 0$ (leading bit 1) and $s_0 + s_1 + s_3 = 1$ (leading bit 3). The last row $s_1 + s_3 = 0$ has leading bit 3, so line L3 adds the stored row and gets $s_0 = 1$, a new row with leading bit 0. Line L7 then sets $s_0 = 1$, $s_1 = 1$, $s_2 = 1$ and $s_3 = 1 \oplus s_0 \oplus s_1 = 1$. The seed 1111 gives the stream 1111000100, which matches the cube, and a search over all 16 seeds finds no other. Four care bits fix four seed bits here, so one more care bit can only agree or conflict: the cube 0X1X0XX1X0 asks for $s_0 = 0$ and fails.

## Classic examples

- **Koenemann's scheme (1991).** One LFSR of $s_{\max} + 20$ stages feeds the scan chains through a phase shifter, the tester loads one seed per pattern, and the LFSR runs freely during the shift.
- **Multiple-polynomial LFSR.** Hellebrand, Rajski, Tarnick, Venkataraman and Courtois (1995) let a few extra bits per seed choose one of several feedback polynomials. A cube that one polynomial cannot encode often has a seed under another, which brings the size down to about $s_{\max} + 4$ stages with 16 polynomials.
- **Mixed-mode BIST.** A [built-in self-test](/built-in-self-test/) runs pseudorandom patterns first, and the faults they miss are covered by stored seeds for the same LFSR, which is much cheaper than stored patterns.
- **Continuous reseeding in [embedded deterministic test](/embedded-deterministic-test/).** Instead of one seed loaded at the start, new tester bits are injected into the generator on every shift clock, and the same linear algebra solves for all of them at once.

## Variations

- **Many chains.** With a phase shifter, each scan cell gets an XOR of several LFSR stages at some clock. The mask of every cell is still a linear form in the seed, and only line L1 changes.
- **Free bits.** The free seed bits of line L6 can be set to 0, to random values, or to values that also detect other faults, so that one seed covers several cubes.
- **Seed per pattern or per set.** A seed can be expanded into one pattern, or into a run of patterns that are then simulated against the remaining faults.
- **Incremental solving.** Each care bit is one row, so a test generator can ask after each new care bit whether the cube is still encodable, and stop adding care bits to a cube when it is not.
- **Finding a short generator.** The opposite problem, finding the shortest LFSR that outputs a given full stream, is solved by the [Berlekamp-Massey algorithm](/berlekamp-massey/). Reseeding fixes the LFSR and asks only for the seed of a partial stream.

## Pitfalls

- **Counting care bits is not enough.** The 3-bit example above fails with 3 care bits on a 3-stage LFSR. Use the measured failure rate, not $s \le n$, to size the LFSR, and keep a fallback such as a stored pattern.
- **Correlated chains.** Neighbor stages of one LFSR feed shifted copies of one sequence. If two scan chains take neighbor stages without a phase shifter, the masks of their cells repeat with a shift, and cubes with care bits in both chains fail much more often than the model says.
- **Taps without $n$.** If $n \notin T$, the window argument fails and some seed bits never reach later outputs. Then fewer than $n$ seed bits are useful, and the effective size is smaller than it looks.
- **Seed loading time.** The seed has to be loaded before the shift starts, which takes time unless the LFSR has a shadow register. Continuous injection, as in embedded deterministic test, avoids the pause.
- **The pattern is not the cube.** The don't-care bits get pseudorandom values. They can switch many cells during shift and capture, which raises test power, and they change which other faults the pattern detects.

## Exercises

1. For the LFSR $x^4 + x + 1$, compute the masks $f_{10}$ to $f_{14}$ and check that $f_{15} = f_0$.
2. Prove that the solutions of a consistent system with rank $r$ in $n$ unknowns over GF(2) are exactly $2^{n-r}$ seeds, and use it to count the seeds of the cube X1XX0XX1XX for $x^4 + x + 1$ (there are 2).
3. Show that for any tap set that contains $n$, every cube whose care bits lie in $n$ consecutive positions is encodable, and give a tap set without $n$ for which this fails.
4. In the random-mask model, show that the chance that $s$ uniform vectors of $\mathrm{GF}(2)^n$ are independent is $\prod_{i<s} (1 - 2^{i-n})$, and evaluate it for $n = 24$ and $s = 20$.

## References
