---
tag: 65V2ET
kind: technique
slug: bit-blasting
name: Bit-blasting
aliases:
- bit-blast
- flattening of bit-vector formulas
area: logic-and-constraints/smt
level: advanced
summary: Encode bit-vector operations as Boolean circuits so a SAT solver can decide them.
prereqs: [bit-vector-satisfiability, tseitin-transformation, boolean-circuit]
see_also: [ripple-carry-adder, array-multiplier, eager-smt-encoding, sat, cdcl, bounded-model-checking, multiplier-bdd-lower-bound, ackermannization]
sources:
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 6, Bit Vectors (the flattening of each operator into a circuit, and incremental flattening)
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 33, Satisfiability Modulo Theories (Barrett, Sebastiani, Seshia and Tinelli), the section on bit-vectors
  - paper: doi:10.1007/s00224-015-9653-1
    title: Gergely Kovásznai, Andreas Fröhlich and Armin Biere, Complexity of fixed-size bit-vector logics, Theory of Computing Systems 59(2), 2016, 323 to 376
    locator: the discussion of why bit-blasting is exponential when the bit-widths are written in binary
  - paper: "Robert Brummayer and Armin Biere, Boolector, an efficient SMT solver for bit-vectors and arrays, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2009), Lecture Notes in Computer Science 5505, Springer, 2009"
    locator: word-level rewriting before bit-blasting, and lemmas on demand for arrays
  - paper: "Randal E. Bryant, Daniel Kroening, Joël Ouaknine, Sanjit A. Seshia, Ofer Strichman and Bryan Brady, Deciding bit-vector arithmetic with abstraction, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2007), Lecture Notes in Computer Science 4424, Springer, 2007"
    locator: under- and over-approximation of the bit-blasted formula, to avoid blasting wide multipliers
---

Bit-blasting decides a formula over fixed-width bit-vectors by replacing each bit-vector variable of width $w$ with $w$ Boolean variables and each operation with a Boolean circuit that computes it bit by bit: an adder for $+$, a multiplier for $\times$, a comparator for $<$. The circuits are turned into clauses with the [Tseitin transformation](/tseitin-transformation/), and a [SAT](/sat/) solver decides the result. A model of the clauses gives the value $\sum_i 2^i b_i$ of each variable. It is the main method of the solvers for [bit-vector satisfiability](/bit-vector-satisfiability/); that page is the decision problem and its complexity, and this page is the encoding.

## In plain words

A computer word is a row of bits, and the machine adds, multiplies and compares words with small circuits built from AND, OR and XOR gates. Bit-blasting writes these same circuits down as logic. Each bit of each unknown becomes a true or false variable, and each gate becomes a few short clauses that say "this output equals that gate of those inputs".

The result is one large formula in plain logic, with no numbers left in it. A SAT solver searches it. If the solver finds an answer, read the bits of each unknown as a binary number. If it finds none, no values of the original words work. Addition costs a few gates for each bit, but multiplication costs many more, so wide multiplications make large formulas.

## When it applies

Use bit-blasting when the variables have fixed and known widths and the semantics is arithmetic modulo $2^w$, as for machine integers:

- [bit-vector](/bit-vector-satisfiability/) formulas from program verification, [symbolic execution](/symbolic-execution/) and [bounded model checking](/bounded-model-checking/) of hardware and software;
- [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/) with known bounds on each variable, after choosing a width that cannot overflow;
- floating-point constraints, after each operation is written as a circuit on the sign, exponent and significand bits ([floating-point satisfiability](/floating-point-satisfiability/));
- any finite-domain constraint that has a compact binary circuit.

It is a poor fit when the widths are very large or are given as parameters, and when the formula has many wide multiplications or divisions: the circuits are then large and hard for SAT solvers.

## The template

```pseudo id=main
BITBLAST(φ, w)
L1  for each subterm t of φ, children first do
L2      if t is a variable: bits(t) ← w fresh Boolean variables
L3      else if t is a constant k: bits(t) ← the w binary digits of k, as true or false
L4      else bits(t) ← CIRCUIT(op(t), bits of the children)      ▷ Tseitin clauses for each gate
L5  replace each atom s ⋈ t by the output literal of a comparator on bits(s) and bits(t)
L6  F ← all gate clauses, the clauses of the Boolean structure of φ, and the unit clause (output)
L7  run a SAT solver on F; from a model, set each variable to Σ 2^i · bit_i

ADD(a, b, c)                      ▷ ripple carry, bit 0 is the least significant
L8  for i ← 0 to w − 1:  s_i ← a_i ⊕ b_i ⊕ c
L9                        c ← (a_i ∧ b_i) ∨ ((a_i ⊕ b_i) ∧ c)
MUL(a, b)
L10 acc ← 0; for i ← 0 to w − 1:  acc ← ADD(acc, (a shifted left by i) ∧ b_i, false)
ULT(a, b)
L11 lt ← false; for i ← 0 to w − 1:  lt ← (¬a_i ∧ b_i) ∨ (¬(a_i ⊕ b_i) ∧ lt)
```

The holes of the template are the circuits. The others follow from these few:

- bitwise $\neg, \wedge, \vee, \oplus$: one gate for each bit, or no gate for $\neg$, which only flips literals;
- subtraction: $a - b = a + \neg b + 1$, that is ADD with the carry-in true; negation is $0 - a$;
- shifts by a constant: rename the bits and fill with false; a shift by a variable amount needs a barrel shifter of $\log_2 w$ layers of multiplexers;
- equality: the AND over $i$ of $\neg(a_i \oplus b_i)$;
- signed less-than: flip the two sign bits, then use ULT;
- division: introduce new words $q$ and $r$ for the quotient and remainder, and add $a = q \cdot b + r \wedge r <_u b$ for $b \ne 0$ (with care for overflow and the value that SMT-LIB fixes for $b = 0$).

### Example

Take $w = 3$ and the term $x + y$ with $x = 5 = (101)_2$ and $y = 3 = (011)_2$. Lines L8 and L9 compute, from bit 0 up:

| $i$ | $a_i$ | $b_i$ | carry in | $s_i = a_i \oplus b_i \oplus c$ | carry out |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 | 1 |
| 2 | 1 | 0 | 1 | 0 | 1 |

The sum bits are $000$, and the last carry is dropped, so $5 + 3 = 0$ in 3 bits, which is $8 \bmod 8$. The overflow is what makes the formula $x + 1 <_u x$ satisfiable: with $w = 4$, bit-blasting and a SAT solver find its only model, $x = 15$. The implementation blasts that formula into 62 clauses over 23 variables. For $x \cdot y = 15 \wedge 1 <_u x \wedge x \le_u y$ with $w = 4$, the models are $(3, 5)$, $(7, 9)$ and $(11, 13)$, since $11 \cdot 13 = 143 = 8 \cdot 16 + 15$; the tests compare the solver with brute force.

### Why it is correct

Fix values for the bits of the variables. Call an assignment to all Boolean variables *consistent* if each gate variable has the value of its gate on its inputs.

**Lemma 1.** The clauses of each gate are satisfied exactly by the consistent values of the gate variable. So for each input there is exactly one consistent assignment, and it satisfies all gate clauses.

*Proof.* The Tseitin clauses of $y \leftrightarrow a \wedge b$ are $(\neg y \vee a)$, $(\neg y \vee b)$, $(y \vee \neg a \vee \neg b)$, which together say $y \leftrightarrow a \wedge b$; the four clauses of XOR exclude the four wrong rows of its truth table. Gates are created after their inputs, so induction along this order gives the unique consistent assignment. $\square$

**Lemma 2.** Under the consistent assignment, the bits of each subterm $t$ encode the value of $t$ modulo $2^w$, and the output literal of each atom has the truth value of the atom.

*Proof.* By induction on $t$; lines L2 and L3 are clear. For ADD, by induction on $i$, after step $i$ the invariant $\sum_{j \le i} s_j 2^j + c\, 2^{i+1} = (a \bmod 2^{i+1}) + (b \bmod 2^{i+1}) + c_0$ holds, because $s_i$ and the new carry are the low and high bits of $a_i + b_i + c$, which is what lines L8 and L9 compute. At $i = w - 1$, dropping the last carry gives the sum modulo $2^w$. For MUL, after row $i$, $acc = a \cdot (b \bmod 2^{i+1}) \bmod 2^w$, since row $i$ adds $a \cdot 2^i$ when $b_i = 1$, truncated to $w$ bits. For ULT, after step $i$, $lt$ says $(a \bmod 2^{i+1}) < (b \bmod 2^{i+1})$: the higher bit $i$ decides if $a_i \ne b_i$, and the lower bits decide otherwise. $\square$

**Theorem.** $F$ is satisfiable if and only if $\varphi$ has a model, and each model of $F$ gives a model of $\varphi$ by line L7.

*Proof.* A model of $\varphi$ gives input bits, and by Lemma 1 a consistent assignment, which by Lemma 2 makes each atom literal true exactly when the atom is true, so the Boolean structure and the unit clause hold. Conversely, a model of $F$ satisfies all gate clauses, so by Lemma 1 it is the consistent assignment for its input bits, and by Lemma 2 the values read by line L7 make $\varphi$ true. $\square$

### Size and time

For width $w$, the counts below are for the implementation, which folds constants:

| circuit | gates | clauses | measured gates at $w = 8, 16, 32$ |
|---|---|---|---|
| ADD, SUB, NEG | $5w - 3$ for ADD | about $17w$ | 37, 77, 157 |
| MUL (shift and add) | $\Theta(w^2)$ | $\Theta(w^2)$ | 155, 691, 2915 |
| EQ, ULT | $2w$ for EQ, $4w$ for ULT | about $7w$ for EQ, $13w$ for ULT | linear |
| shift by a variable | $\Theta(w \log w)$ | $\Theta(w \log w)$ | not implemented |
| division | $\Theta(w^2)$ | $\Theta(w^2)$ | through MUL |

So the CNF has size $O(|\varphi| \cdot w^2)$, which is polynomial when $w$ is written in unary or is a fixed constant. When the widths are written in binary, as in SMT-LIB, a formula of length $n$ can declare a word of width $2^n$, and the encoding is exponential in $n$; this gap is real, since that logic is NEXPTIME-complete (Kovásznai, Fröhlich and Biere 2016). The encoding takes linear time in its size, and the SAT search is exponential in the worst case.

## Classic examples

- **SMT solvers for QF_BV.** STP, Boolector, Bitwuzla, Z3 and cvc5 simplify the formula at the word level and then bit-blast what is left to a [CDCL](/cdcl/) SAT solver; see [eager SMT encoding](/eager-smt-encoding/).
- **Bounded model checking of C programs.** Tools such as CBMC unroll loops, turn machine integers into bit-vectors, and bit-blast the result.
- **Hardware equivalence.** Two circuits that should compute the same function are blasted into one miter formula that asks for an input where they differ. Multipliers are the hard case: they have no small [binary decision diagrams](/multiplier-bdd-lower-bound/), and they are also hard for CDCL.
- **Bounded integer arithmetic.** With known bounds, [LIA](/linear-integer-arithmetic-satisfiability/) constraints can be blasted with a width that avoids overflow.

## Variations

- **Eager and lazy.** Eager bit-blasting blasts everything at once. Lazy or incremental variants first blast cheap operations, replace multiplications by fresh words, and add their circuits only if the model found is spurious (Bryant et al. 2007; Kroening and Strichman, Chapter 6).
- **Word-level rewriting first.** Rules such as $x + 0 = x$, $x \cdot 2^k = x \ll k$ and the propagation of constants remove most circuits before blasting (Brummayer and Biere 2009).
- **And-inverter graphs.** Represent the circuit with only AND gates and negated edges, hash equal gates, and simplify the graph before Tseitin.
- **Polarity-based encoding.** The [Plaisted-Greenbaum transformation](/plaisted-greenbaum-transformation/) keeps only one direction of each gate definition where the gate occurs with one polarity.
- **Uninterpreted functions and arrays.** These are removed first, by [Ackermannization](/ackermannization/) or by lemmas on demand, and then the rest is blasted.
- **Incremental solving.** With an [incremental SAT](/incremental-sat/) solver, the circuits of earlier queries are kept, and new constraints add clauses.

## Pitfalls

- **Carry.** Wrong: $c \leftarrow a_i \wedge b_i$, which loses the carry chain. Right: line L9, $c \leftarrow (a_i \wedge b_i) \vee ((a_i \oplus b_i) \wedge c)$.
- **Signed order.** Wrong: use ULT for the signed comparison $x <_s y$; then $-1 = (1\ldots1)_2$ looks larger than $0$. Right: flip both sign bits and then use ULT, or compare the sign bits first.
- **Division by zero.** Wrong: leave $x / 0$ unconstrained or treat it as an error. Right: SMT-LIB defines $\mathrm{bvudiv}(x, 0)$ as the all-ones word and $\mathrm{bvurem}(x, 0) = x$, and the circuit must give these values.
- **Large shifts.** Wrong: a shift by $s \ge w$ that reuses only the low bits of $s$. Right: in SMT-LIB, $x \ll s$ and the logical right shift are $0$ when $s \ge w$, so the barrel shifter must test the high bits of $s$.
- **Blasting wide multiplications at once.** Wrong: blast every $64$-bit product eagerly; the result has tens of thousands of clauses for each product and the SAT search is slow. Right: rewrite at the word level first and add multiplier circuits lazily, as in the variations above.
- **Reading the model.** Wrong: read bit $0$ as the most significant bit. Right: line L7 uses $\sum_i 2^i b_i$, with bit $0$ the least significant, and the same order must be used in every circuit.

## Exercises

1. Write the clauses for a full adder cell with inputs $a, b, c$ and outputs $s, c'$, without intermediate variables. How many clauses do you need?
2. Show that the shift-and-add multiplier of line L10 needs only $w - i$ AND gates in row $i$ when the result is truncated to $w$ bits, and count the gates for $w = 8$.
3. Give a bit-vector formula with one variable of width $w$ that is satisfiable for each $w \ge 2$ but only by a value with at least two set bits, and blast it for $w = 3$.

## References
