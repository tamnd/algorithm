---
tag: G9JK72
kind: problem
slug: automatic-test-pattern-generation
name: Automatic test pattern generation
aliases:
- ATPG
area: eda/timing-and-verification
level: core
summary: For a fault in a circuit, find an input vector that excites the fault and propagates its effect to an output, or prove the fault untestable.
prereqs: [stuck-at-fault-model, boolean-circuit]
see_also: [d-algorithm, podem, sat-based-atpg, fault-simulation, scoap, scan-design, circuit-sat, boolean-equivalence-checking]
sources:
  - paper: "Oscar H. Ibarra and Sartaj K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975"
    title: O. H. Ibarra and S. K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975
    locator: deciding whether a single stuck-at fault of a combinational circuit is detectable is NP-complete
  - paper: "Hideo Fujiwara and Shunichi Toida, The complexity of fault detection problems for combinational logic circuits, IEEE Transactions on Computers C-31(6), 555 to 560, 1982"
    title: H. Fujiwara and S. Toida, The complexity of fault detection problems for combinational logic circuits, IEEE Transactions on Computers C-31(6), 555 to 560, 1982
    locator: NP-completeness for monotone circuits of three or more levels, and polynomial time for two levels
  - paper: doi:10.1147/rd.104.0278
    title: J. P. Roth, Diagnosis of automata failures, a calculus and a method, IBM Journal of Research and Development 10(4), 278 to 291, 1966
    locator: the first complete test generation method, with the D-calculus
  - paper: doi:10.1109/43.108614
    title: T. Larrabee, Test pattern generation using Boolean satisfiability, IEEE Transactions on Computer-Aided Design 11(1), 4 to 15, 1992
    locator: the reduction of test generation for one fault to satisfiability of a formula
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Combinational Circuit Test Generation (the problem, redundancy, and the D-algorithm, PODEM and FAN), and the chapter on sequential circuit test generation
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapters on test generation for combinational and for sequential circuits
---

Automatic test pattern generation, or ATPG, is the problem of finding, for one fault of a circuit, an input vector on which the good and the faulty circuit give different outputs, or of proving that no such vector exists. For the [single stuck-at fault model](/stuck-at-fault-model/) and a combinational circuit, the vector must give the faulty line the value opposite to its stuck value and carry that difference to a primary output. The decision version is NP-complete, so every complete method is exponential in the worst case, but industrial circuits with millions of gates are tested with it every day. With [scan design](/scan-design/), the circuit seen by ATPG is combinational.

## In plain words

A chip comes off the line, and you want to know if one wire inside it is stuck at 0. You cannot look at the wire. You can only set the input pins and read the output pins.

So you look for one input that does two things. It makes the good wire carry a 1, so that the stuck wire is wrong. And it makes the outputs depend on that wire, so that the wrong value shows on some pin. Such an input is a test for the fault.

Sometimes no input works. Then the fault does not change what the circuit computes, and the logic around the wire is redundant. ATPG must find a test, or prove that there is none.

## Definition

**Instance.** A combinational [Boolean circuit](/boolean-circuit/) $C$ with primary inputs $x_1, \ldots, x_n$, primary outputs $z_1, \ldots, z_m$ and $L$ lines, and one fault $f$, here a single stuck-at fault $\ell/v$. The faulty circuit $C_f$ is $C$ with the line $\ell$ fixed to $v$.

**Output.** A vector $t \in \{0, 1\}^n$ with

$$C(t) \ne C_f(t),$$

or the answer that no such $t$ exists, in which case $f$ is **undetectable**, or **redundant**. For a single output $z$, the condition is $\ell(t) = \lnot v$ and $\partial z / \partial \ell\,(t) = 1$, where $\partial z / \partial \ell = z|_{\ell = 0} \oplus z|_{\ell = 1}$ is the Boolean difference of $z$ with respect to the line.

**Decision version.** Given $C$ and $f$, is $f$ detectable?

A partial answer is often given as a **test cube**, a vector over $\{0, 1, X\}$ such that every way of filling the $X$ entries gives a test. In practice the cubes of many faults are merged before the $X$ entries are filled.

## Variants

- **Test set generation.** Given $C$ and a fault list $\Phi$, find a set of vectors that detects every detectable fault of $\Phi$, and classify the rest as redundant. A small set is wanted, since tester time grows with it.
- **Redundancy identification.** Prove that a fault is undetectable. This is the complement of the decision version, and it is used in logic synthesis to remove logic.
- **Sequential ATPG.** The circuit has flip-flops, and a test is a sequence of vectors from a known or unknown state. The usual model unrolls the circuit into $k$ copies, one per clock cycle, and solves a combinational problem with the fault in every copy.
- **Other fault models.** Transition faults and path delay faults need a pair of vectors, one to set the line and one to launch a change. Bridging faults need values on two lines. Cell-aware faults are given by tables inside each cell.
- **$n$-detect tests.** Each fault must be detected by at least $n$ different vectors, which tends to catch more real defects.

## Examples

Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, and the fault $h$/0. A test must set $h = 1$ in the good circuit, so $b = 0$ or $c = 0$. To pass the difference through $z = \mathrm{NAND}(g, h)$, the side input must have the non-controlling value $g = 1$, so $a = 0$ or $b = 0$. The cube $X0X$ does both: on 000, 001, 100 and 101 the good circuit gives $g = h = 1$ and $z = 0$, and the faulty one gives $z = \mathrm{NAND}(1, 0) = 1$. The full set of tests is 000, 001, 010, 100, 101. The [D-algorithm](/d-algorithm/), [PODEM](/podem/) and [SAT-based ATPG](/sat-based-atpg/) pages solve this same instance step by step.

Now take $p = ab$, $q = \bar{a}c$, $r = bc$, $z = p + q + r$, and the fault $r$/0. A test needs $r = 1$, so $b = c = 1$. To see $r$ at the OR gate, the side inputs must be 0: $p = 0$ gives $a = 0$, and then $q = \bar{a}c = 1$. So no vector works, and the fault is redundant. This is the consensus theorem, $ab + \bar{a}c + bc = ab + \bar{a}c$: the gate $r$ can be removed, and the circuit computes the same function.

## Known algorithms

- **Exhaustive fault simulation.** Run [fault simulation](/fault-simulation/) on all $2^n$ vectors. It is the reference method for small $n$.
- **[D-algorithm](/d-algorithm/)** (Roth, 1966). Searches over values of internal lines with five values $0, 1, X, D, \bar{D}$, with a D-frontier and a J-frontier.
- **[PODEM](/podem/)** (Goel, 1981). Decides values only on primary inputs, with a backtrace from each objective. The FAN rules of Fujiwara and Shimono (1983) are described there.
- **[SAT-based ATPG](/sat-based-atpg/)** (Larrabee, 1992). Writes the good and the faulty circuit as a formula and gives it to a [SAT](/sat/) solver.
- **Guides for the search.** The [SCOAP](/scoap/) measures estimate how hard each line is to set and to observe. [Fault collapsing](/fault-collapsing/) reduces the fault list first.

## Bounds

- **NP-complete in general.** In the model of [Boolean circuits](/boolean-circuit/) of AND, OR and NOT gates, the decision version is NP-complete (Ibarra and Sahni, 1975). It is in NP since a test is checked by two circuit evaluations. Fujiwara and Toida (1982) showed that it stays NP-complete for monotone circuits with three or more levels of gates, and that it is polynomial for monotone two-level circuits. So no algorithm solves it in polynomial time unless P = NP, and the complement, redundancy identification, is coNP-complete.
- **Exhaustive upper bound.** Evaluating the good and the faulty circuit on all $2^n$ vectors takes $O(2^n (L + P))$ time on a [word RAM](/word-ram/), with $P$ the number of gate input pins. PODEM keeps this bound with decisions on inputs only.
- **Fanout-free circuits.** If every line feeds at most one gate, every fault of a circuit of AND, OR, NAND, NOR and NOT gates is detectable, and a test is built in $O(L)$ time by setting each side input of the path to its non-controlling value. The proof is on the [stuck-at fault model](/stuck-at-fault-model/) page.
- **Minimum test sets.** Finding a smallest test set for a fault list is NP-hard, since with one fault on the list and the bound $k = 1$ it is the decision version. It is a [set cover](/set-cover/) problem over the detecting sets.
- **What is only measured.** On benchmark and industrial circuits, complete methods find tests for most faults with little backtracking, and a few faults are aborted after a backtrack limit. These are measured results, not bounds, and they depend on the circuit, the method and the limit.

## Reductions

- **From [circuit SAT](/circuit-sat/).** Given a circuit $C$ with one output $z$, take the fault $z$/0. A vector detects it exactly when $z = 1$ in the good circuit, so the fault is detectable exactly when $C$ is satisfiable. This shows NP-hardness for general circuits in one line. The proofs of Ibarra and Sahni and of Fujiwara and Toida work for restricted circuits.
- **To SAT.** Build the **miter**: the good and the faulty circuit share the inputs, and an OR of the XORs of their outputs is the new output. The fault is detectable exactly when the miter output can be 1. The [Tseitin transformation](/tseitin-transformation/) turns the miter into a [CNF](/conjunctive-normal-form/) formula of size $O(L + P)$, which is the start of [SAT-based ATPG](/sat-based-atpg/).
- **Relation to equivalence checking.** A fault is redundant exactly when $C$ and $C_f$ are equivalent, so redundancy identification is a special case of [Boolean equivalence checking](/boolean-equivalence-checking/), and the same miter is used for both.
- **Sequential to combinational.** Full [scan design](/scan-design/) makes every flip-flop an input and an output for test, which turns sequential ATPG into the combinational problem above. Without scan, unrolling $k$ clock cycles gives a combinational instance of size $O(k (L + P))$.

## Applications

- **Manufacturing test.** ATPG with [fault simulation](/fault-simulation/) produces the vectors that a tester applies to each chip through the scan paths.
- **Redundancy removal.** In logic synthesis, a redundant fault $\ell/v$ shows that $\ell$ can be tied to $v$, which removes gates. This uses the [observability don't-cares](/observability-dont-care/) of the line.
- **Equivalence checking.** Early equivalence checkers used ATPG engines on the miter of two circuits, and SAT-based methods now share the same structure.
- **Diagnosis.** Tests that tell two faults apart narrow down the place of a defect in a failing chip.
- **Built-in self-test.** Faults that pseudorandom patterns miss in [built-in self-test](/built-in-self-test/) get stored tests from ATPG, or test points.

## References
