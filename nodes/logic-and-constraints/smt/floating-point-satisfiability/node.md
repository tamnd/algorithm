---
tag: PV4DSM
kind: problem
slug: floating-point-satisfiability
name: Floating-point satisfiability
aliases:
- floating-point SMT
- IEEE 754 constraints
- QF_FP
area: logic-and-constraints/smt
level: research
summary: Decide constraints over IEEE 754 floating-point numbers and their rounding.
prereqs: [ieee-754, bit-vector-satisfiability, rounding-modes]
see_also: [bit-blasting, floating-point-arithmetic, round-to-nearest-even, linear-real-arithmetic-satisfiability, nonlinear-real-arithmetic-satisfiability, interval-arithmetic, rounding-error-analysis, symbolic-execution]
sources:
  - paper: "Philipp Rümmer and Thomas Wahl, An SMT-LIB theory of binary floating-point arithmetic, 8th International Workshop on Satisfiability Modulo Theories (SMT 2010)"
    locator: the first proposal of the SMT-LIB theory FloatingPoint
  - paper: "Martin Brain, Cesare Tinelli, Philipp Rümmer and Thomas Wahl, An automatable formal semantics for IEEE-754 floating-point arithmetic, 22nd IEEE Symposium on Computer Arithmetic (ARITH 2015)"
    locator: the formal semantics of the SMT-LIB theory, including the single NaN and the two kinds of equality
  - paper: "IEEE Standard for Floating-Point Arithmetic, IEEE Std 754-2008 (revised as IEEE Std 754-2019)"
    locator: the formats, the rounding-direction attributes and the correctly rounded operations
  - paper: "Martin Brain, Florian Schanda and Youcheng Sun, Building better bit-blasting for floating-point problems, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2019), Lecture Notes in Computer Science 11427, Springer, 2019"
    locator: the SymFPU library of circuits for floating-point operations, used by cvc4 and later solvers
  - paper: "Martin Brain, Vijay D'Silva, Alberto Griggio, Leopold Haller and Daniel Kroening, Deciding floating-point logic with abstract conflict driven clause learning, Formal Methods in System Design 45 (2014)"
    locator: a CDCL-style search over intervals of floating-point values instead of bits
  - paper: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1), 1991"
    locator: rounding, signed zeros, infinities and NaN, and the failure of the laws of real arithmetic
---

Floating-point satisfiability is the problem of deciding whether a formula over [IEEE 754](/ieee-754/) floating-point numbers has a model, with the exact semantics of the standard: each operation rounds its exact real result to a representable number under a given [rounding mode](/rounding-modes/), and the special values $\pm 0$, $\pm\infty$ and NaN behave as the standard says. In SMT-LIB the quantifier-free logic is QF_FP. It is needed to verify numeric software, because the laws of [real arithmetic](/linear-real-arithmetic-satisfiability/) fail for floats: addition is not associative, and $x + 1 = x$ has models. For fixed formats the problem is NP-complete, and the usual method reduces it to [bit-vectors](/bit-vector-satisfiability/).

## In plain words

Computers store most numbers with fractions as floating-point numbers: a sign, a fixed number of significant binary digits, and an exponent. After each step of a calculation, the exact result is rounded to the nearest number that can be stored. So small errors appear, very large numbers absorb small ones, and special values stand for "infinity" and "not a number".

The question is whether some floating-point values make all constraints true, with the exact rounding rules of the standard. Answers can differ from those over the real numbers. For example, a positive number added to 1 can give exactly 1. Solvers usually describe each rounding step as a circuit on the bits of the numbers and use a SAT solver.

## Definition

A *format* $(e, s)$ has $e$ exponent bits and $s$ significand bits, including the hidden bit; binary32 is $(8, 24)$ and binary64 is $(11, 53)$. Its values are:

- the normal numbers $\pm 1.f \times 2^{k}$ with $s - 1$ fraction bits and $k$ in the exponent range,
- the subnormal numbers $\pm 0.f \times 2^{k_{\min}}$,
- $+0$ and $-0$, $+\infty$ and $-\infty$, and NaN (one NaN in SMT-LIB; IEEE 754 has many bit patterns for it).

The operations take a rounding mode $r \in \{\mathrm{RNE}, \mathrm{RNA}, \mathrm{RTP}, \mathrm{RTN}, \mathrm{RTZ}\}$ (to nearest with ties to even, to nearest with ties away from zero, toward $+\infty$, toward $-\infty$, toward zero). The value of $\mathrm{fp.add}(r, x, y)$ for finite $x$ and $y$ is the exact sum $x + y$ rounded by $r$, and likewise for subtraction, multiplication, division, fused multiply-add, square root, remainder and rounding to an integer. Conversions to and from other formats, integers and bit-vectors are also in the theory.

**Two equalities.** $\mathrm{fp.eq}$ is IEEE equality: NaN is not equal to itself, and $+0$ equals $-0$. The logical equality $=$ of SMT-LIB is identity of values: NaN $=$ NaN, and $+0 \ne -0$. The order predicates are false whenever one argument is NaN.

A QF_FP formula is a Boolean combination of atoms over these terms, possibly mixed with bit-vector terms. The problem asks whether some values of the variables make it true.

**How it relates to its neighbours.** [Bit-vector satisfiability](/bit-vector-satisfiability/) is the target of the main reduction. [Linear](/linear-real-arithmetic-satisfiability/) and [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/) are the idealized versions without rounding, and they give different answers.

## Variants

- **Fixed formats.** binary16, binary32, binary64 and binary128; the case in practice.
- **Formats as parameters.** With $e$ and $s$ written in binary, a term may denote very wide numbers; this matters for the complexity, as with bit-vector widths.
- **One rounding mode.** Most programs use only RNE, which removes a variable and many cases.
- **Mixed theories.** QF_BVFP and QF_ABVFP add bit-vectors and arrays, for programs that reinterpret the bits of a float or keep floats in memory.
- **Real relaxation with error bounds.** Replace each rounded operation $x \oplus y$ by $(x + y)(1 + \varepsilon)$ with $|\varepsilon| \le u$ (the [standard model](/floating-point-model/) of [rounding error analysis](/rounding-error-analysis/)), which gives sound but incomplete reasoning over the reals.

## Examples

Each example was checked in Python, whose `float` is binary64 with RNE.

1. **Absorption.** $x + 1 = x$ has the models $x = 2^{53}$ and $x = +\infty$, among others: $2^{53} + 1$ lies halfway between $2^{53}$ and $2^{53} + 2$, and the tie goes to the even significand, $2^{53}$. For $x = 2^{52}$ the sum is exact, so it is not a model. Over the reals the formula is unsatisfiable.
2. **A positive number that disappears.** $x > 0 \wedge x + 1 = 1$ holds for $x = 2^{-60}$, and also for $x = 2^{-53}$ (a tie that rounds to even), but not for $x = 2^{-52}$.
3. **No associativity.** With $a = 0.1$, $b = 0.2$, $c = 0.3$ (each rounded to binary64), $(a + b) + c = 0.6000000000000001$ and $a + (b + c) = 0.6$, so $(a + b) + c \ne a + (b + c)$ is satisfiable. A compiler that reassociates sums changes results.
4. **NaN.** $\neg \mathrm{fp.eq}(x, x)$ holds exactly when $x$ is NaN; the formula $x = x$ with logical equality is valid.
5. **Signed zeros.** $\mathrm{fp.eq}(x, y) \wedge \neg (x = y)$ has the model $x = +0$, $y = -0$, and then $1/x = +\infty$ while $1/y = -\infty$, so equal floats need not give equal results.
6. **Unsatisfiable.** $x \cdot x < 0$ is unsatisfiable: a product of a number with itself is never negative, and it is NaN only if $x$ is NaN, where $<$ is false.

## Known algorithms

| method | idea | notes |
|---|---|---|
| [bit-blasting](/bit-blasting/) through bit-vectors | unpack each float into sign, exponent and significand; build circuits that align, add or multiply, normalize and round, with guard and sticky bits | complete; the standard method (for example the SymFPU circuits, Brain, Schanda and Sun 2019); multiplication, division and square root give large circuits |
| abstract CDCL over intervals | a CDCL search whose decisions and conflicts are intervals of floats, not bits (Brain et al. 2014) | complete for fixed formats; strong on problems with wide ranges |
| reduced precision first | solve the formula in a smaller format, then try to lift the model and refine the precision on failure | a heuristic for satisfiable problems |
| real relaxation | reason in [LRA](/linear-real-arithmetic-satisfiability/) or [NRA](/nonlinear-real-arithmetic-satisfiability/) with rounding errors bounded as intervals | sound for unsatisfiability under conditions; incomplete |
| numerical search | treat the formula as a function to minimize over floats, using distances in units in the last place | finds models fast in many cases; cannot prove unsatisfiability |
| [interval arithmetic](/interval-arithmetic/) propagation | propagate float intervals through the operations | a preprocessing step for the methods above |

## Bounds

**Theorem.** For each fixed format, and more generally for formats with $e$ and $s$ written in unary, QF_FP satisfiability is NP-complete.

*Proof.* *In NP.* A model is a bit pattern of $e + s$ bits for each variable (one sign bit, $e$ exponent bits and $s - 1$ fraction bits), polynomial in the input size. Each operation can be evaluated in time polynomial in $e + s$: for addition, align the significands, but keep only $s + 3$ bits, with the guard, round and sticky bits standing for all the shifted-out bits, which is enough to round correctly; multiplication, division and square root need $O(s)$ extra bits. So a guessed model is checked in polynomial time.

*NP-hard.* Reduce [SAT](/sat/). For each propositional variable $p$ take a float variable $x_p$ and the atom $\mathrm{fp.isNegative}(x_p)$. These atoms are independent, since each $x_p$ can be $-1$ or $1$ freely, so a propositional formula is satisfiable if and only if the same formula over these atoms is. $\square$

With bit-vector parts and formats in binary, the reductions to [bit-vectors](/bit-vector-satisfiability/) give upper bounds of the same kind as for bit-vectors with binary widths. Practical difficulty comes from the size of the circuits: a binary64 multiplication blasts into a circuit with a multiplier of $53 \times 53$ bits.

## Reductions

- **To QF_BV.** Each format becomes a bit-vector of width $e + s$, and each operation becomes a circuit; with [bit-blasting](/bit-blasting/), this gives SAT.
- **From SAT.** As in the proof above.
- **From and to real arithmetic, partially.** On ranges where no rounding happens, for example small integers in binary64, float operations agree with the real ones and a real model is a float model. In general, neither satisfiability implies the other (examples 1 and 2).
- **To the analysis of programs.** A path through numeric code becomes a QF_FP formula in [symbolic execution](/symbolic-execution/).

## Applications

- Test generation and [symbolic execution](/symbolic-execution/) of numeric C code, for example to reach a branch that depends on a float comparison.
- Proving the absence of overflow to infinity, of NaN, and of division by zero in control software.
- Checking compiler optimizations such as reassociation, fused multiply-add contraction and the replacement of $x / c$ by $x \cdot (1/c)$.
- Validating hardware floating-point units against the standard.

## References
