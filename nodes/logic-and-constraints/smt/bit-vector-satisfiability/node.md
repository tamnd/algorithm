---
tag: CHRZF1
kind: problem
slug: bit-vector-satisfiability
name: Bit-vector satisfiability
aliases:
- bit-vector theory
- BV
- QF_BV
- fixed-size bit-vector logic
area: logic-and-constraints/smt
level: core
summary: Decide constraints over fixed-width machine integers with bitwise and arithmetic operations.
prereqs: [sat, smt-problem, twos-complement]
see_also: [bit-blasting, floating-point-satisfiability, linear-integer-arithmetic-satisfiability, eager-smt-encoding, array-theory-satisfiability, symbolic-execution, bounded-model-checking, nexptime]
sources:
  - paper: doi:10.1007/s00224-015-9653-1
    title: Gergely Kovásznai, Andreas Fröhlich and Armin Biere, Complexity of fixed-size bit-vector logics, Theory of Computing Systems 59(2), 2016, 323 to 376
    locator: the complexity of QF_BV and quantified BV with unary and with binary encoded bit-widths (NP, PSPACE and NEXPTIME completeness results)
  - paper: "Martin Jonáš and Jan Strejček, On the complexity of the quantified bit-vector arithmetic with binary encoded bit-widths, Information Processing Letters 135 (2018)"
    locator: quantified bit-vector logic with binary widths is complete for AEXP(poly)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 6, Bit Vectors (syntax, semantics, flattening and incremental flattening)
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 33, Satisfiability Modulo Theories (Barrett, Sebastiani, Seshia and Tinelli), the section on bit-vectors
  - paper: "Clark Barrett, Pascal Fontaine and Cesare Tinelli, The SMT-LIB Standard, Version 2.6, 2017, www.smt-lib.org"
    locator: the theory FixedSizeBitVectors and the logic QF_BV, including the values of division by zero
  - paper: "Robert Brummayer and Armin Biere, Boolector, an efficient SMT solver for bit-vectors and arrays, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2009), Lecture Notes in Computer Science 5505, Springer, 2009"
    locator: word-level rewriting and bit-blasting in a solver for QF_BV and QF_ABV
---

Bit-vector satisfiability is the problem of deciding whether a formula over fixed-width words of bits, with the operations of machine integers, has a model. The words behave like the registers of a processor: $+$, $-$ and $\times$ wrap around modulo $2^w$, comparisons come in unsigned and signed ([two's complement](/twos-complement/)) forms, and the bitwise, shift and slicing operations are exact. In SMT-LIB the quantifier-free version is the logic QF_BV. It is [NP-complete](/np-complete/) when the widths are small numbers, and much harder when widths are written in binary. The usual method is [bit-blasting](/bit-blasting/) to SAT: this page is the decision problem, and that page is the encoding.

## In plain words

Computer programs do not compute with true integers. Each number is stored in a fixed number of bits, for example 32, and a sum that is too large wraps around to a small number. Bit-vector constraints describe such stored numbers exactly, including the wrap around, the bit operations AND, OR and XOR, and shifts.

The question is whether some values of the words make all constraints true. Because each word has only finitely many values, the answer can always be found. The common way is to write every bit as a true or false variable and give the result to a SAT solver. This works very well for programs, but some formulas, such as those with many wide multiplications, stay hard.

## Definition

A *bit-vector term* of width $w \ge 1$ denotes an element of $\{0, 1\}^w$, read as the number $\sum_{i < w} 2^i b_i$ in $[0, 2^w)$, or as a signed number in $[-2^{w-1}, 2^{w-1})$. The terms are built from variables of declared widths, constants, and the operations of the SMT-LIB theory FixedSizeBitVectors:

| group | operations | semantics |
|---|---|---|
| structure | concatenation, extract $t[j:i]$, zero and sign extension | rearrange bits; widths add or shrink |
| bitwise | $\neg$, $\wedge$, $\vee$, $\oplus$ | bit by bit |
| arithmetic | $+$, $-$, $\times$, negation | modulo $2^w$ |
| division | unsigned and signed quotient and remainder | $x / 0$ is the all-ones word and $x \bmod 0 = x$ for the unsigned forms |
| shifts | $\ll$, logical and arithmetic $\gg$ | the shift amount is a word; amounts $\ge w$ give $0$ (or the sign fill) |
| predicates | $=$, $<_u$, $\le_u$, $<_s$, $\le_s$ | unsigned and signed order |

A QF_BV formula is a Boolean combination of atoms; the problem asks whether some assignment of words to the variables makes it true. For the complexity, the input size counts the bit-widths either in *unary* (or as fixed constants) or in *binary*, as in SMT-LIB, where `(_ BitVec 1000000)` takes only a few characters.

**How it relates to bit-blasting.** [Bit-blasting](/bit-blasting/) is one method for this problem, the translation of each operation into a Boolean circuit. This page states the problem, its complexity for each encoding of the widths, and the other methods.

## Variants

- **Widths in unary or fixed.** The usual case for proofs of membership in NP.
- **Widths in binary (QF_BV2).** The SMT-LIB encoding; the complexity rises to NEXPTIME (see Bounds).
- **With arrays (QF_ABV) and uninterpreted functions (QF_UFBV).** Memory as an [array](/array-theory-satisfiability/) from address words to byte words, the logic of most tools for software.
- **With quantifiers (BV).** Used for synthesis and for invariants; PSPACE-complete for unary widths.
- **Linear equations only.** A system of linear equations modulo $2^w$ can be solved in polynomial time by a normal form over the integers (as for linear congruences); adding inequalities or bitwise operations brings back NP-hardness.
- **Floating-point.** [Floating-point satisfiability](/floating-point-satisfiability/) is usually reduced to bit-vectors.

## Examples

Each example was checked by a script, with the [bit-blasting](/bit-blasting/) solver and with brute force over all values.

1. **Unsigned overflow.** $x + 1 <_u x$ has, for $w = 8$, the single model $x = 255$, because $255 + 1 = 0$. Over the integers it has no model.
2. **Signed overflow.** $0 <_s x \wedge x + x <_s 0$ has, for $w = 8$, exactly the 64 models $64 \le x \le 127$; the solver returned $x = 127$. This is the bug pattern of a signed overflow check written after the operation.
3. **A valid bit trick.** For $w = 8$, $x \ne 0 \wedge (x \wedge (x - 1)) = 0$ holds exactly for the powers of two $1, 2, 4, \ldots, 128$. A solver proves such an equivalence by showing that its negation is unsatisfiable.
4. **An invalid rewrite.** $(3x) / 3 = x$ is not valid for $w = 4$: it fails for $x = 6, \ldots, 15$; for $x = 6$, $18 \bmod 16 = 2$ and $2 / 3 = 0$. A compiler may not apply this rewrite to machine integers.
5. **Modular inverses.** $3x = 1$ with $w = 4$ has the model $x = 11$, since $33 = 2 \cdot 16 + 1$, while $2x = 1$ has none, because $2x$ is even modulo 16.
6. **Factoring.** $x \cdot y = 15 \wedge 1 <_u x \le_u y$ with $w = 4$ has the models $(3, 5)$, $(7, 9)$ and $(11, 13)$. With large $w$ and a large product, such formulas encode factoring and are hard for every known method.

## Known algorithms

| method | idea | cost |
|---|---|---|
| eager [bit-blasting](/bit-blasting/) | circuits plus [Tseitin](/tseitin-transformation/), then [CDCL](/cdcl/) | CNF of size $O(n w^2)$, then exponential search |
| word-level rewriting, then bit-blasting | simplify at the word level, propagate constants, slice words, then blast (Brummayer and Biere 2009) | as above, with much smaller formulas in practice |
| abstraction refinement | blast cheap operations; over- and under-approximate multiplications and add their circuits on demand (Bryant et al. 2007) | iterative |
| lemmas on demand for arrays | treat array reads as fresh words and add read-over-write lemmas when a model is spurious | iterative |
| word-level local search | change whole words, guided by the operations, for satisfiable instances | incomplete |
| integer encoding ("int-blasting") | write each word as an integer in $[0, 2^w)$ and each wrap-around with an extra integer variable, then use a [LIA](/linear-integer-arithmetic-satisfiability/) or nonlinear integer solver | useful for wide arithmetic with few bitwise operations |
| polynomial-time special cases | linear equations modulo $2^w$; pure bitwise formulas reduce to SAT of the same size | polynomial or SAT |

## Bounds

**Theorem.** With the widths given in unary, or bounded by a constant, QF_BV satisfiability is NP-complete.

*Proof.* *In NP.* A model assigns $w$ bits to each variable, and the total is at most the input size when widths are in unary. Each operation can be evaluated in time polynomial in $w$: addition and comparison in $O(w)$, multiplication and division in $O(w^2)$ bit operations. So a guessed model is checked in polynomial time. (Equivalently, [bit-blasting](/bit-blasting/) gives a CNF of size $O(n w^2)$, which is satisfiable if and only if the formula is.)

*NP-hard.* Reduce [SAT](/sat/). With $w = 1$, the bitwise operations $\neg$, $\wedge$, $\vee$ on words of one bit are the Boolean operations, so read each propositional variable $p$ as a word $x_p$ of width 1, and the formula $\psi$ as a term $t_\psi$ of width 1. The single atom $t_\psi = 1$ is a QF_BV formula of the same size as $\psi$, with the same models. $\square$

**Binary widths (quoted from Kovásznai, Fröhlich and Biere 2016).**

| logic | unary widths | binary widths |
|---|---|---|
| QF_BV | NP-complete | NEXPTIME-complete |
| QF_UFBV | NP-complete | NEXPTIME-complete |
| BV (with quantifiers) | PSPACE-complete | NEXPTIME-hard, in EXPSPACE; complete for AEXP(poly) (Jonáš and Strejček 2018) |
| UFBV | NEXPTIME-complete | 2-NEXPTIME-complete |

The reason for the jump is that a formula of length $n$ with binary widths can declare words of $2^{\Theta(n)}$ bits, so bit-blasting, and each method that looks at all bits, can be exponential in $n$. Kovásznai, Fröhlich and Biere also identify fragments with binary widths that stay in PSPACE or NP, for example when only bitwise operations and equality are used.

## Reductions

- **From SAT.** Width 1, as in the proof above.
- **To SAT.** [Bit-blasting](/bit-blasting/), polynomial for unary widths.
- **From bounded LIA.** A [linear integer](/linear-integer-arithmetic-satisfiability/) formula with known bounds becomes QF_BV with a width large enough to avoid overflow; the small-solution bound for LIA makes this a correct reduction with polynomial widths.
- **To LIA or NIA.** Each word becomes an integer $0 \le x < 2^w$, and $x + y$ becomes $x + y - 2^w o$ with $o \in \{0, 1\}$; multiplication needs nonlinear integer arithmetic, and bitwise operations need one integer per bit or special lemmas.
- **From floating-point.** [Floating-point](/floating-point-satisfiability/) operations are circuits on the sign, exponent and significand fields, so QF_FP reduces to QF_BV.
- **From arrays and uninterpreted functions.** With [Ackermannization](/ackermannization/) and the read-over-write axioms, QF_ABV and QF_UFBV reduce to QF_BV.

## Applications

- [Symbolic execution](/symbolic-execution/) and test generation for binaries and C programs, where path conditions are over machine words.
- [Bounded model checking](/bounded-model-checking/) of hardware designs and software.
- Proving or refuting compiler rewrites and bit tricks (examples 3 and 4), and the verification of hardware arithmetic.
- Analysis of cryptographic code and searches for collisions in small parameters.

## References
