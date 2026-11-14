---
tag: V7JQ6Q
kind: technique
slug: built-in-self-test
name: Built-in self-test
aliases:
- BIST
- logic BIST
area: cad/timing-and-verification
level: core
summary: Puts a pattern generator, usually an LFSR, and a response compactor such as a MISR on the chip, so the circuit tests itself at speed.
prereqs: [stuck-at-fault-model, linear-feedback-shift-register]
see_also: [scan-design, fault-simulation, fault-collapsing, scoap, lfsr, cyclic-redundancy-check, gf2-polynomial-arithmetic, de-bruijn-sequence]
sources:
  - paper: "B. Könemann, J. Mucha and G. Zwiehoff, Built-in logic block observation techniques, Digest of Papers, 1979 Test Conference, 37 to 41, 1979"
    title: B. Könemann, J. Mucha and G. Zwiehoff, Built-in logic block observation techniques, Digest of Papers, 1979 Test Conference, 37 to 41, 1979
    locator: the BILBO register, which works as a normal register, a shift register, a pattern generator or a signature register
  - paper: doi:10.1109/TC.1980.1675610
    title: J. E. Smith, Measures of the effectiveness of fault signature analysis, IEEE Transactions on Computers C-29(6), 510 to 514, 1980
    locator: the probability that a signature register misses an error when all error streams are equally likely
  - paper: doi:10.1109/43.3132
    title: T. W. Williams, W. Daehn, M. Gruetzner and C. W. Starke, Bounds and analysis of aliasing errors in linear feedback shift registers, IEEE Transactions on Computer-Aided Design 7(1), 75 to 83, 1988
    locator: aliasing under independent bit errors, and the comparison of primitive and non-primitive feedback polynomials
  - book: isbn:9780471624639
    title: Paul H. Bardell, William H. McAnney and Jacob Savir, Built-In Test for VLSI, Pseudorandom Techniques, Wiley-Interscience, 1987
    locator: the chapters Pseudorandom Sequence Generators, Test Response Compression Techniques, Shift-Register Polynomial Division and Random Pattern Built-In Test
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Built-In Self-Test (pattern generators, response compaction, aliasing, BIST architectures)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapters Compression Techniques and Built-In Self-Test
---

Built-in self-test, or BIST, puts the test equipment for a digital circuit on the chip itself. A test pattern generator, usually a [linear feedback shift register](/linear-feedback-shift-register/) (LFSR), feeds the circuit under test with a long pseudorandom sequence, and a response compactor, usually a multiple-input signature register (MISR), folds all the outputs into a short signature. At the end, the chip compares the signature with the one computed for the good circuit and reports pass or fail. The test runs at the clock rate of the chip, needs no stored vectors, and can run again in the field. It has two costs that a designer must measure: random patterns miss some faults, and compaction can alias, so that a faulty circuit ends with the good signature. For a $k$-bit signature and the model in which every error stream is equally likely, the aliasing probability is just under $2^{-k}$. This is an EDA page. The LFSR here only needs a long period and good spread of patterns. Its weakness as a cipher, on the [cryptographic LFSR](/lfsr/) page, does not matter for test.

## In plain words

A tester is an expensive machine that stores test inputs and the right outputs. BIST puts a small tester inside the chip.

A shift register with XOR feedback makes a long stream of patterns that look random. The circuit runs on them at full speed. Its outputs go into a second shift register, which mixes them into a short code, the signature. At the end, the chip checks the signature against the right one and gives one bit: pass or fail.

Two things can go wrong. Some faults are hard to hit with random patterns. And a bad circuit can, by chance, end with the right signature. With a 32-bit signature and a simple model of errors, that chance is about one in four billion.

## When it applies

- The chip must be tested at its own clock rate, or many times in its life, for example at each power-on in a safety system, or there are many cores and few tester pins.
- The circuit under test is combinational, or it has full [scan design](/scan-design/), so that each pattern is independent of the ones before it.
- No line of the circuit can take an unknown value $X$ in test mode. An $X$ that enters the signature register makes the final signature unknown.
- Random patterns reach a high enough fault coverage, or the faults that they miss get test points, special seeds or stored patterns from [ATPG](/automatic-test-pattern-generation/).

## The template

```pseudo id=main
BIST(CUT, the LFSR polynomial p and seed s, the MISR polynomial q, N, the good signature S*)
L1  state ← s; r ← 0
L2  for t ← 1 to N do
L3      x ← the bits of state, or of a phase shifter fed by state
L4      w ← CUT(x)
L5      r ← (x · r + w) mod q
L6      state ← the next state of the LFSR by p
L7  if r = S* then return pass else return fail
```

The holes are the pattern generator in lines L1, L3 and L6, the compactor in line L5, the number of patterns $N$, and the polynomials. The good signature $S^*$ comes from a simulation of the good circuit with the same seed and the same $N$, before the chip is made.

**The pattern generator.** An LFSR with $n$ stages and a primitive feedback polynomial of degree $n$ goes through all $2^n - 1$ nonzero states and then repeats, as shown on the [LFSR](/linear-feedback-shift-register/) page. So within one period it applies each nonzero vector once, in a fixed order that looks random. It never gives the all-zero vector.

**The compactor.** Line L5 reads the register $r$ as a polynomial over GF(2) of degree less than $k = \deg q$. For one output bit $w$ per clock, this is a single-input signature register, and the step $r \leftarrow (x r + w) \bmod q$ is one step of long division by shift and XOR, as in [GF(2) polynomial arithmetic](/gf2-polynomial-arithmetic/). By induction on $t$, after the bits $b_0, b_1, \ldots, b_{m-1}$ the register holds

$$r = R(x) \bmod q(x), \qquad R(x) = \sum_{i=0}^{m-1} b_i\, x^{m-1-i},$$

since $r_{t+1} = x r_t + b_t \bmod q$. So the signature is the remainder of the response stream divided by $q$, the same computation as a [cyclic redundancy check](/cyclic-redundancy-check/). With $k$ outputs, $w$ is a vector of $k$ bits that is added into the $k$ stages at each step, and the register is a MISR.

**Aliasing.** Let the faulty stream be $R + E$ with an error polynomial $E \ne 0$ of degree less than $m$. The map from streams to signatures is linear, so the faulty signature is the good one exactly when $E \bmod q = 0$, that is, when $q$ divides $E$. The multiples of $q$ with degree less than $m$ are $q u$ with $\deg u < m - k$, so there are $2^{m-k} - 1$ nonzero ones. If all $2^m - 1$ nonzero error streams are equally likely, as in Smith (1980), the aliasing probability is

$$P_{\text{alias}} = \frac{2^{m-k} - 1}{2^m - 1} < 2^{-k},$$

and it tends to $2^{-k}$ as $m$ grows. The same count works for a MISR. Over $m$ clocks with $k$ inputs, the map from the $mk$ error bits to the $k$ signature bits is linear and onto, since the last input word is added straight into the register, so $2^{mk - k} - 1$ nonzero errors alias. The result holds for every $q$ of degree $k$, primitive or not. Two more facts follow from the division. If $q$ has the term 1 and $k \ge 1$, then $q$ has no common factor with $x^j$, so $q$ divides $x^j B(x)$ only when $q$ divides $B(x)$. A burst of errors no longer than $k$ bits is $E = x^j B(x)$ with $B \ne 0$ of degree less than $k$, which $q$ cannot divide. So every single-bit error and every burst of at most $k$ bits is detected.

**Example.** Take the circuit $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$, with 8 lines and 16 single stuck-at faults. The pattern generator is the LFSR with the recurrence $s_{t+3} = s_{t+1} \oplus s_t$, whose polynomial $x^3 + x + 1$ is primitive, and the seed $s_0 s_1 s_2 = 100$. The pattern at time $t$ is $(a, b, c) = (s_t, s_{t+1}, s_{t+2})$. The compactor is a single-input signature register with $q = x^3 + x + 1$.

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $abc$ | 100 | 001 | 010 | 101 | 011 | 111 | 110 |
| $z$ | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| $r$ after the step | 000 | 000 | 000 | 000 | 001 | 011 | 111 |

The 7 patterns are all the nonzero vectors, and the good signature is $S^* = 111$. Each of the 16 faults changes the output stream, and none of them ends with 111, so all 16 are detected. Some faults share a signature: $b$/0 and $z$/0 give the stream 0000000, and $g$/0, $h$/0 and $z$/1 give 1111111. Both streams give the signature 000. For the second one, the stream is $x^6 + x^5 + \cdots + 1 = (x^7 + 1)/(x + 1)$, and $x^3 + x + 1$ divides it, since it divides $x^7 + 1$ and has no common factor with $x + 1$. This does not change pass or fail, but it means that the signature cannot tell these faults apart in diagnosis.

Aliasing shows up with other error streams. The stream 0001100 differs from the good stream 0000111 in the bits 3, 5 and 6, so $E = x^3 + x + 1 = q$, and its signature is 111, the good one. Of the 127 nonzero error streams of length 7, exactly $2^4 - 1 = 15$ alias, a fraction of $15/127 \approx 0.118$, just under $2^{-3} = 0.125$.

## Classic examples

- **Logic BIST of scan designs.** In the STUMPS design of Bardell and McAnney, one LFSR feeds many [scan](/scan-design/) paths at once through a phase shifter, the circuit captures one response per pattern, and a MISR takes the outputs of all paths. This is test-per-scan: each pattern costs a full shift.
- **BILBO.** The register of Könemann, Mucha and Zwiehoff (1979) works as a normal register, as a shift register, as an LFSR pattern generator or as a MISR. Two such registers around a block of logic test it, and then swap roles to test the next block.
- **Fault grading.** [Fault simulation](/fault-simulation/) of the pseudorandom patterns gives the coverage and the list of missed faults. The result depends on the fault list, so state whether it is the full or the [collapsed](/fault-collapsing/) list.
- **Memory BIST.** Embedded memories are tested by on-chip controllers that run deterministic march sequences of writes and reads, not random patterns, since memory faults follow the layout of the cell array.
- **Signature checks outside test.** The same polynomial division checks data on links and disks as a [cyclic redundancy check](/cyclic-redundancy-check/).

## Variations

- **Test points.** A line that random patterns rarely set gets a control point, an extra gate that forces it in test mode with a higher probability. A line that is rarely observed gets an observation point into the compactor. The [SCOAP](/scoap/) measures and their probability forms point to the lines.
- **Weighted random patterns.** Bias each input to 1 with a probability other than 1/2, chosen per input, so that wide AND and OR gates are hit more often.
- **Reseeding.** For each missed fault, ATPG finds a test cube, and the seed that makes the LFSR produce it is the solution of a linear system over GF(2), since each LFSR output bit is a linear function of the seed. The chip stores the seeds, which are much shorter than the patterns.
- **Exhaustive and pseudo-exhaustive test.** If each output depends on at most $w$ inputs, apply all $2^w$ vectors to each cone. A counter does it, or an LFSR with an extra NOR term that adds the all-zero state, which gives a [de Bruijn sequence](/de-bruijn-sequence/) of period $2^w$.
- **Other compactors.** Counting the ones or the transitions in a stream needs less hardware but misses more errors than polynomial division. Space compactors of XOR trees cut the number of outputs before the MISR.
- **Error models.** Williams, Daehn, Gruetzner and Starke (1988) study the model where each bit is wrong with probability $p$, independently. There the aliasing probability depends on $q$ and on $p$, and primitive polynomials alias much less in general than non-primitive ones.

## Pitfalls

- **Faults that random patterns miss.** The output of a 16-input AND gate stuck at 0 needs all 16 inputs at 1, a probability of $2^{-16}$ per uniform random pattern. Then $N$ patterns detect it with probability $1 - (1 - 2^{-16})^N$, which is 0.142 for $N = 10^4$ and 0.783 for $N = 10^5$, and a 95% chance needs about 196 000 patterns. An LFSR that feeds exactly these 16 inputs covers all nonzero vectors in 65 535 patterns. But in a real design the LFSR feeds many inputs and its period is far longer than the test, so the uniform model is the right guide.
- **The missing all-zero vector.** For $z = \mathrm{NOR}(a, b, c)$ fed by the 3-stage LFSR of the example, the faults $z$/0, $a$/1, $b$/1 and $c$/1 all need the vector 000, which the LFSR never gives. So 4 of the 8 faults are missed after the full period.
- **Unknown values.** One $X$ into the MISR makes every later signature bit unknown. Memories, analog blocks, bus contention and uninitialized latches must be blocked or masked in test mode.
- **The aliasing number is a model value.** The bound $2^{-k}$ assumes equally likely error streams. A real fault gives a structured error, often the same error in many cycles. Fault simulation of the actual signature, not the model, decides which faults alias.
- **Correlated scan paths.** Neighbor stages of one LFSR give shifted copies of one sequence. If they feed neighbor scan paths directly, the paths get the same bits one cycle apart, and some patterns can never occur. A phase shifter of XOR gates mixes the stages first.
- **The good signature must match the netlist.** $S^*$ is computed by simulation of the exact gates, seed and pattern count. Any change to the netlist, the seed or $N$ needs a new $S^*$.
- **Faults in the BIST logic.** A fault in the comparator or in the pass flag can pass every chip. Test the BIST hardware through scan, or make the chip output the signature itself.
- **Power.** Random patterns switch far more lines per clock than normal operation, and at full speed this can cause supply droop and false failures.

## Exercises

1. From the seed 100 and the recurrence $s_{t+3} = s_{t+1} \oplus s_t$, list the 7 patterns of the example, and check that the next pattern is 100 again.
2. Prove that a signature register whose polynomial $q$ of degree $k$ has the term 1 detects every burst of errors of length at most $k$.
3. Count the aliasing error streams of length 8 for $q = x^3 + x + 1$, and check that there are $2^5 - 1 = 31$ of the 255 nonzero ones.
4. For $z = \mathrm{NOR}(a, b, c)$, change the 3-stage LFSR so that it also gives the vector 000, and check that it then detects all 8 faults.

## References
