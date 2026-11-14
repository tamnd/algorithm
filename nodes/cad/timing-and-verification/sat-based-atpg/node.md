---
tag: PFQN6B
kind: algorithm
slug: sat-based-atpg
name: SAT-based ATPG
aliases:
- Larrabee ATPG
area: cad/timing-and-verification
level: advanced
summary: Test generation that writes the good circuit and the faulty cone as one CNF formula with a miter on the outputs, so a model of the formula is a test and unsatisfiable means redundant.
solves: [automatic-test-pattern-generation]
model: word-ram
complexity:
  vars: {n: the number of primary inputs, L: the number of lines, P: the number of gate input pins}
  time: {worst: "O(2^n (L + P))", best: "O(L + P)"}
  space: {extra: O(L + P)}
properties: {deterministic: true, exact: true, complete: true, recursive: false}
history:
  year: 1992
  people: [Tracy Larrabee]
  note: Larrabee wrote test generation as Boolean satisfiability, with the Boolean difference of the good and the faulty circuit and the active clauses, in 1989 and in the journal paper of 1992.
prereqs: [automatic-test-pattern-generation, tseitin-transformation, sat]
see_also: [cdcl, dpll, unit-propagation, podem, d-algorithm, equivalence-checking, circuit-sat, conjunctive-normal-form]
sources:
  - paper: doi:10.1109/43.108614
    title: T. Larrabee, Test pattern generation using Boolean satisfiability, IEEE Transactions on Computer-Aided Design 11(1), 4 to 15, 1992
    locator: the formula of the good and the faulty circuit, the Boolean difference at the outputs and the active clauses for the paths of the fault effect
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Combinational Circuit Test Generation (test generation as Boolean satisfiability)
  - paper: "Oscar H. Ibarra and Sartaj K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975"
    title: O. H. Ibarra and S. K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975
    locator: the NP-completeness of fault detection, which the reduction to SAT matches
---

SAT-based ATPG solves [automatic test pattern generation](/automatic-test-pattern-generation/) for one [single stuck-at fault](/stuck-at-fault-model/) by a reduction to [SAT](/sat/). It writes the good circuit and a faulty copy of the part that the fault can reach as one formula in [conjunctive normal form](/conjunctive-normal-form/), with the [Tseitin transformation](/tseitin-transformation/). Extra clauses fix the stuck value at the fault site and ask that some output differs, which is a miter of the two circuits. A model of the formula is a test, and a proof that the formula is unsatisfiable is a proof that the fault is redundant.

## In plain words

Write the circuit as a set of small rules, one group per gate: "this wire is the AND of those two wires", in the form that a SAT solver reads. Then write a second copy for the broken circuit. The copy only needs the gates that the broken wire can reach, since all other gates behave the same in both.

Add three more rules: in the copy the broken wire has its stuck value, in the good circuit it has the other value, and at least one output is different in the two circuits.

Give all the rules to a SAT solver. If it finds values that make every rule true, the input values are a test. If it proves that no such values exist, no test exists, and the fault can never be seen.

## The problem

The input is a combinational circuit $C$ with $n$ primary inputs and $L$ lines in topological order, a fault $(\ell, s)$, and a flag for the optional active clauses. The lines are the primary inputs, the gate outputs and the fanout branches. Any gate type with a Tseitin encoding is allowed, XOR included. The output is a two-valued input vector that detects the fault, or "untestable".

The variables are $G_k$, the good value of line $k$, and $F_k$, the faulty value, for each line $k$ of the cone $K$ of $\ell$, that is, $\ell$ and every line reachable from it. Outside $K$ the faulty value equals the good value, so it needs no variable of its own.

## The algorithm

```pseudo id=main
SAT-ATPG(C, (ℓ, s), active)
L1  for each line k: a variable G_k, and the Tseitin clauses of the good gate of k
L2  K ← ℓ and every line reachable from ℓ
L3  for each k ∈ K: a variable F_k; if k ≠ ℓ, the Tseitin clauses of the gate of k, with F_j for its inputs j ∈ K and G_j for the others
L4  add the units F_ℓ = s and G_ℓ = ¬s
L5  for each primary output o ∈ K: a variable D_o and the clauses of D_o ↔ (G_o xor F_o)
L6  add the clause D_o1 ∨ D_o2 ∨ ... over these outputs (empty if K holds no output)
L7  if active then for each k ∈ K: a variable A_k with A_k → (G_k ≠ F_k), and A_k → ∨ A_w over the fanouts w of k if k is not an output; add the unit A_ℓ
L8  run a SAT solver on the clauses
L9  if the clauses are unsatisfiable then return "untestable"
L10 return the values of G at the primary inputs in the model
```

The Tseitin clauses of $z = \mathrm{AND}(a, b)$ are $(\lnot z \lor a)$, $(\lnot z \lor b)$ and $(z \lor \lnot a \lor \lnot b)$. NAND, NOR and NOT use the clauses of AND, OR and BUF with $z$ negated. An XOR of $k$ inputs is a chain of $k - 1$ two-input XORs with 4 clauses each. The variable $A_k$ of line L7 says "line $k$ is on a path of differences to an output". These clauses are implied in the sense that they keep satisfiability, but they let the solver see at once that the effect needs a path.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$. The fault is $h$ stuck at 0.

Line L1 gives the variables 1 to 8 for $G_a, G_b, G_{b_g}, G_{b_h}, G_c, G_g, G_h, G_z$. The cone is $K = \{h, z\}$, so line L3 adds $F_h = 9$ and $F_z = 10$, and line L5 adds $D_z = 11$.

| line | clauses (DIMACS numbering) | meaning |
|---|---|---|
| L1 | (-3 2) (3 -2) (-4 2) (4 -2) | the branches copy $b$ |
| L1 | (6 1) (6 3) (-6 -1 -3) | $G_g = \mathrm{NAND}(G_a, G_{b_g})$ |
| L1 | (7 4) (7 5) (-7 -4 -5) | $G_h = \mathrm{NAND}(G_{b_h}, G_c)$ |
| L1 | (8 6) (8 7) (-8 -6 -7) | $G_z = \mathrm{NAND}(G_g, G_h)$ |
| L3 | (10 6) (10 9) (-10 -6 -9) | $F_z = \mathrm{NAND}(G_g, F_h)$ |
| L4 | (-9) (7) | $F_h = 0$, $G_h = 1$ |
| L5 | (-11 8 10) (-11 -8 -10) (11 -8 10) (11 8 -10) | $D_z \leftrightarrow G_z \oplus F_z$ |
| L6 | (11) | the output differs |

That is 11 variables and 23 clauses. The active clauses of line L7 add 2 variables and 6 clauses. [Unit propagation](/unit-propagation/) alone gives $F_h = 0$, $G_h = 1$, $D_z = 1$, then $F_z = 1$ from (10 9), $G_z = 0$ from $D_z$, and $G_g = 1$ from (8 6). The solver then decides $a = 0$, $b = 0$ and $c = 0$ with no conflict, so the test is 000. Every vector with $b = 0$, or 010, would also do.

For a redundant fault, take $na = \mathrm{NOT}(a)$, $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(na, c)$, $r = \mathrm{AND}(b, c)$ and $z = \mathrm{OR}(p, q, r)$, with $r$ stuck at 0. The formula has 17 variables and 38 clauses, and unit propagation refutes it with no decision. $G_r = 1$ forces $b = c = 1$, and then $G_z = 1$. The differing output needs $F_z = 0$, so $G_p = G_q = 0$. With $b = 1$, $G_p = 0$ forces $a = 0$, so $na = 1$ and $G_q = 1$, a conflict. So the fault is redundant.

## Correctness

The Tseitin clauses of a gate have, for each value of its inputs, exactly one satisfying value of its output. So once the input variables and $F_\ell$ are fixed, the clauses of lines L1 and L3 have exactly one solution, and it is the list of the true line values in the good and the faulty circuit. Lines outside the cone have the same value in both circuits, so outputs outside the cone never differ, and the clause of line L6 asks exactly that some output differs. A model therefore gives a test, and a test, which must put $\lnot s$ on the good site, gives a model. For the active clauses, set $A_k$ true when a path of differing lines leads from $k$ to an output. A test has such a path from $\ell$, so the extended formula is satisfiable whenever the plain one is. The [full proof](proofs/correctness.md) gives the details.

## Complexity

The formula has $O(L)$ variables and $O(L + P)$ clauses of total size $O(L + P)$, where $P$ is the number of gate input pins, and building it takes $O(L + P)$ time. Solving it is exponential in the worst case, since the problem is NP-complete. The solver of the implementation decides the input variables first. Without the active clauses, unit propagation then sets every other variable, because each gate output and each $D_o$ is a function of its inputs. So the search tree has depth at most $n$, at most $2^n - 1$ decisions, and $O(2^n (L + P))$ time. The best case is one pass of unit propagation, as for the redundant fault of the example. The extra space is the formula and the trail, $O(L + P)$.

How fast real [CDCL](/cdcl/) solvers are on these formulas is a measured result, not a theorem. Larrabee reported that the method was robust on the hard faults of benchmark circuits, and later tools use SAT as the engine for the faults that structural methods abort.

## Properties

- **Complete.** The answer "untestable" is a proof of redundancy, and a CDCL solver can output a certificate for it, such as a DRAT proof.
- **Any gate type.** XOR, multiplexers and complex cells need only their clauses. Structural methods need special rules for gates without a controlling value.
- **Two-valued tests.** The model gives a value to every input. Inputs that the test does not need can be found afterwards by trying X on each one with three-valued simulation.
- **Deterministic.** The solver of the implementation has a fixed decision order. Real solvers are deterministic for a fixed seed.
- **Off-the-shelf solver.** All search work is in the solver, so ATPG gains each improvement in SAT solving without a change.

## Variants and improvements

- **Incremental SAT.** The good circuit is the same for every fault. An incremental solver keeps its clauses and learned clauses, and adds the cone of each new fault under assumptions. This removes most of the cost of building and learning again.
- **Structural information.** Circuit-based solvers use the gate graph to choose decisions, for example on inputs and fanout stems only, and add implications found by structural analysis, much like the learning of FAN-type tools.
- **Other fault models.** Transition and path delay faults use two time frames of the circuit, and bridging faults change the faulty copy. The formula changes, and the solver does not.
- **Sequential circuits.** Unroll the circuit over $k$ clock cycles, as in [bounded model checking](/bounded-model-checking/), or use [scan design](/scan-design/) so that the circuit is combinational for test.
- **Other engines.** A [BDD](/binary-decision-diagram/) of the Boolean difference of the outputs with respect to $\ell$, together with the activation condition, gives all tests at once, but its size can be exponential.

## When to use it

Use SAT-based ATPG for faults that structural methods such as [PODEM](/podem/) abort after a backtrack limit, and to prove that faults are redundant. It is also the simplest correct ATPG to write when a good SAT solver is at hand, and the natural choice for circuits with much XOR logic, such as arithmetic and error correcting circuits. For the many easy faults, random patterns with [fault simulation](/fault-simulation/), followed by a structural method, cost less than building a formula for each fault.

## Pitfalls

- **A faulty copy of the whole circuit.** Lines outside the cone are the same in both circuits. Copying them doubles the formula and hides nothing. But the faulty gates in the cone must read $G_j$ for their inputs outside the cone, not a fresh variable, or the copy is not tied to the inputs.
- **Clauses for the fault site.** The faulty copy of $\ell$ must get the unit $F_\ell = s$ and no gate clauses. With its gate clauses, $F_\ell$ is tied to the good inputs of $\ell$, which give $\lnot s$ by the other unit, so the formula is unsatisfiable for every fault.
- **No output in the cone.** If the fault reaches no output, line L6 adds the empty clause. The formula is unsatisfiable, as it should be. Code that drops an empty clause instead finds false tests.
- **Reading the test from the faulty copy.** The test is the good input values. At a fault on a primary input, $F$ and $G$ differ there.
- **Equating "satisfiable" with "easy".** The formula of a redundant fault can be hard for the solver. A time limit and the label "aborted" are needed in practice, as for structural methods.

## Implementations

## History

Larrabee presented test generation as Boolean satisfiability in a conference paper of 1989, and the journal paper of 1992 gave the full method. It wrote the Boolean difference of the good and the faulty circuit as clauses, added the active clauses that tie the fault effect to a path, and solved the result with a simple SAT search. The idea is the same as the miter used in combinational [equivalence checking](/equivalence-checking/). With the CDCL solvers of the late 1990s and 2000s, SAT became a standard engine in commercial ATPG, mainly for the hard and the redundant faults.

## References
