---
tag: 6D8HV3
kind: model
slug: stuck-at-fault-model
name: Stuck-at fault model
aliases:
- single stuck-at fault
area: cad/timing-and-verification
level: core
summary: A fault model in which one line of a circuit is fixed at 0 or at 1, the standard target of manufacturing test generation.
prereqs: [boolean-circuit]
see_also: [fault-collapsing, fault-simulation, automatic-test-pattern-generation, observability-dont-care, scan-design, built-in-self-test, boolean-network]
sources:
  - paper: "Richard D. Eldred, Test routines based on symbolic logical statements, Journal of the ACM 6(1), 33 to 37, 1959"
    title: R. D. Eldred, Test routines based on symbolic logical statements, Journal of the ACM 6(1), 33 to 37, January 1959
    locator: tests that set a line to the opposite of its fixed value and make it visible at an output, the early form of the stuck-at model
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Fault Modeling (single and multiple stuck-at faults, fault equivalence, dominance and checkpoints)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault modeling (the single stuck-fault model, redundancy and multiple faults)
  - paper: "Oscar H. Ibarra and Sartaj K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975"
    title: O. H. Ibarra and S. K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975
    locator: deciding whether a single stuck-at fault is detectable is NP-complete
  - paper: "Hideo Fujiwara and Shunichi Toida, The complexity of fault detection problems for combinational logic circuits, IEEE Transactions on Computers C-31(6), 555 to 560, 1982"
    title: H. Fujiwara and S. Toida, The complexity of fault detection problems for combinational logic circuits, IEEE Transactions on Computers C-31(6), 555 to 560, 1982
    locator: NP-completeness for monotone circuits of three or more levels, and polynomial time for two levels
---

The stuck-at fault model describes a defect of a digital circuit as one line whose value is fixed at 0 or at 1, whatever the gates that drive it do. Under the single fault assumption, the circuit has exactly one such fault, so a circuit with $L$ lines has $2L$ faults. An input vector detects a fault when the good circuit and the faulty circuit give different values on some primary output. The model is an abstraction for test, not a claim about physics: real defects are shorts, opens and slow transistors, and the model is used because tests for its faults also catch most of them in practice.

## The machine

The circuit is a combinational [Boolean circuit](/boolean-circuit/) $C$ with primary inputs $x_1, \ldots, x_n$, gates, and primary outputs. Its lines are the primary inputs, the gate outputs, and the fanout branches: a line that feeds $k \ge 2$ gates or outputs is a stem with $k$ branches, one per destination, and each branch is a line of its own. A fault on a stem and a fault on one of its branches are different faults, because the branch fault changes one destination only.

A single stuck-at fault is a pair $f = (\ell, v)$ with a line $\ell$ and $v \in \{0, 1\}$, written $\ell/v$. The faulty circuit $C_f$ is $C$ with the value of $\ell$ replaced by the constant $v$. For a vector $t \in \{0, 1\}^n$, let $C(t)$ and $C_f(t)$ be the vectors of output values. Then

$$t \text{ detects } f \iff C(t) \ne C_f(t).$$

A test must do two things: it must **activate** the fault, by giving $\ell$ the value $\lnot v$ in the good circuit, and it must **propagate** the difference along some path to an output. A fault that no vector detects is **undetectable**, or redundant. Then $C_f$ computes the same function as $C$, so the line can be tied to $v$ without any change at the outputs.

For a sequential circuit, the faulty machine has the same fault on every clock cycle, and a test is a sequence of vectors from a known state. [Scan design](/scan-design/) gives direct access to the flip-flops, so that the test problem becomes the combinational one above.

## What it counts

The main measure is **fault coverage**: the fraction of the $2L$ faults that a test set detects. Some reports divide by the number of detectable faults instead, which needs a proof that the other faults are redundant. The second measure is the **number of tests**, which sets the time on the tester. Both are computed by [fault simulation](/fault-simulation/), and [fault collapsing](/fault-collapsing/) reduces the list to one fault per class of equivalent faults first.

Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ and $b_h$. The lines are $a, b, b_g, b_h, c, g, h, z$, so there are 16 faults. The good output is 1 only on 011, 110 and 111.

| fault | the vectors $abc$ that detect it |
|---|---|
| a/0, $b_g$/0, g/1 | 110 |
| $b_h$/0, c/0, h/1 | 011 |
| a/1, c/1 | 010 |
| b/0, z/0 | 011, 110, 111 |
| b/1 | 001, 100, 101 |
| $b_g$/1 | 100, 101 |
| $b_h$/1 | 001, 101 |
| g/0, h/0, z/1 | 000, 001, 010, 100, 101 |

The test set {110, 011} detects 8 of the 16 faults, a coverage of 50%. Every fault needs one of the rows, and the rows a/0, $b_h$/0, a/1 and $b_g$/1 have disjoint vector sets, so at least 4 tests are needed. The set {010, 011, 101, 110} detects all 16 faults, and it is the only complete set of size 4. All faults of this circuit are detectable.

## Relation to other models

- **Multiple stuck-at faults.** Any set of lines may be stuck at once, which gives $3^L - 1$ faults. One fault can mask another, so a test set that detects all single faults need not detect all multiple faults. The single fault model is used because its fault list is linear in $L$.
- **Boolean difference and don't-cares.** For one output $z$, the vector $t$ detects $\ell/v$ exactly when $\ell(t) = \lnot v$ and $z$ changes when $\ell$ is flipped at $t$. The vectors where $\ell$ cannot be seen at any output are the [observability don't-cares](/observability-dont-care/) of $\ell$. So $\ell/v$ is undetectable exactly when $\ell = \lnot v$ only inside those don't-cares, which links test to multilevel logic optimization: removing redundant faults simplifies a [Boolean network](/boolean-network/).
- **Delay faults.** The transition fault model says that a line is slow to rise or slow to fall, and needs a pair of vectors: one to set the old value and one to launch the change. The path delay model says that one path is too slow. Both relate to the paths of [static timing analysis](/static-timing-analysis/).
- **Bridging and open faults.** A bridging fault shorts two lines, which then compute a wired AND or OR, or follow the stronger driver. A stuck-open fault in CMOS can turn a gate into a memory element. These models are closer to the defects but have more faults or need sequences.
- **Cell-aware and current-based tests.** Modern flows add faults inside library cells and measure the quiescent supply current. They extend the stuck-at model and do not replace it.

## Known results in the model

- **Detection is NP-complete.** Deciding whether a single stuck-at fault is detectable is NP-complete (Ibarra and Sahni, 1975), by a reduction from [SAT](/sat/). Fujiwara and Toida (1982) showed that it stays NP-complete for monotone circuits with three or more levels, and that it is polynomial for two-level circuits. So [automatic test pattern generation](/automatic-test-pattern-generation/) has no known polynomial algorithm, and its solvers are exponential in the worst case.
- **Fanout-free circuits have no redundant fault.** In a circuit of AND, OR, NAND, NOR and NOT gates with one output, where every line feeds at most one gate, every single stuck-at fault is detectable. Proof: the subcircuit below a line $\ell$ is a tree over its own inputs. A tree of these gates over distinct variables is not constant, so some setting of its inputs gives $\ell = \lnot v$. The path from $\ell$ to the output is unique. Each side input of a gate on it is again the root of a tree over its own inputs, not shared with any other tree, so it can be set to the non-controlling value of that gate. These settings use disjoint inputs, so they hold together, and the difference reaches the output.
- **Redundancy means a constant.** If $\ell/v$ is undetectable, replacing $\ell$ by $v$ gives an equivalent circuit, and the gates that only fed $\ell$, or that the constant now fixes, can go. This is redundancy removal in logic synthesis.
- **Checkpoints.** In a circuit of AND, OR, NAND, NOR, NOT and BUF gates, a test set that detects all single stuck-at faults on the primary inputs and the fanout branches detects all single stuck-at faults. The proof and an XOR circuit where it fails are on the [fault collapsing](/fault-collapsing/) page.
- **Test set size.** A complete test set is a hitting set of the detecting sets of the detectable faults, which is a [set cover](/set-cover/) problem with one element per fault. The size of any family of faults with pairwise disjoint detecting sets is a lower bound on its size, as in the example.

## References
