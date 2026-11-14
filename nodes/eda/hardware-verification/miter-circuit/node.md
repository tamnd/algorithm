---
tag: HDNMPN
kind: definition
slug: miter-circuit
name: Miter
aliases:
- miter circuit
area: eda/hardware-verification
level: intro
summary: A circuit that feeds the same inputs to two designs and XORs matching outputs into one OR output, which can be 1 only if the designs differ.
prereqs: [boolean-circuit, circuit-sat]
see_also: [boolean-equivalence-checking, product-machine, cutpoint-equivalence-checking, sat-sweeping, automatic-test-pattern-generation, tseitin-transformation, and-inverter-graph, co-np-complete]
sources:
  - paper: "Daniel Brand, Verification of large synthesized designs, Proceedings of the International Conference on Computer-Aided Design, 534 to 537, 1993"
    title: D. Brand, Verification of large synthesized designs, ICCAD 1993, 534 to 537
    locator: the joined circuit of the two designs with an XOR on the outputs, and the use of test generation to show that its output cannot be 1
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the section on combinational equivalence checking and the miter structure
---

A miter is a circuit built from two circuits $C_1$ and $C_2$ with the same inputs and the same number of outputs. It connects each input of $C_1$ to the matching input of $C_2$, puts an XOR gate on each pair of matching outputs, and joins the XOR gates with one OR gate. Its single output is 1 on an input exactly when the two circuits give different outputs on it. So $C_1$ and $C_2$ are equivalent if and only if the miter is unsatisfiable, and any input that satisfies it is a counterexample. Brand (1993) named the construction. This page is about the construction; the problem it serves, its algorithms and its bounds are on the [Boolean equivalence checking](/boolean-equivalence-checking/) page.

## Definition

Let $C_1$ and $C_2$ be [Boolean circuits](/boolean-circuit/) over the inputs $x = (x_1, \ldots, x_n)$, each with outputs $o_1, \ldots, o_m$, and let output $j$ of $C_1$ compute $f_j$ and output $j$ of $C_2$ compute $g_j$. The outputs are matched by position or by name. The *miter* $M(C_1, C_2)$ is the circuit that contains both circuits on the shared inputs $x$ and the extra gates

$$d_j = f_j \oplus g_j \quad (j = 1, \ldots, m), \qquad M(x) = d_1 \vee \cdots \vee d_m.$$

$C_1$ and $C_2$ are *equivalent* when $f_j(a) = g_j(a)$ for every $j$ and every $a \in \{0, 1\}^n$.

**Proposition 1 (the miter reduces equivalence to unsatisfiability).** $C_1$ and $C_2$ are equivalent if and only if $M(a) = 0$ for every $a$, that is, the miter is unsatisfiable. An $a$ with $M(a) = 1$ is an input on which the circuits differ.

*Proof.* For a fixed $a$, $M(a) = 1$ if and only if $d_j(a) = 1$ for some $j$, if and only if $f_j(a) \ne g_j(a)$ for some $j$. So $M$ has a satisfying input exactly when some input separates the circuits, and that input separates them. $\square$

The miter has $|C_1| + |C_2| + 2m - 1$ gates, counting the OR as $m - 1$ two-input gates and each XOR as one gate, so it is built in linear time. A SAT solver gets it through the [Tseitin transformation](/tseitin-transformation/).

**Proposition 2 (combinational equivalence is coNP-complete).** The problem "are $C_1$ and $C_2$ equivalent?" for circuits is [coNP-complete](/co-np-complete/).

*Proof.* *Membership.* The complement, "the circuits differ", is in NP: by Proposition 1, an input $a$ with $M(a) = 1$ is a certificate, and evaluating $M$ on $a$ takes time linear in the size of the miter. *Hardness.* [Circuit satisfiability](/circuit-sat/) is NP-complete, so its complement, circuit unsatisfiability, is coNP-complete. Map a circuit $C$ with one output to the pair ($C$, the circuit with the constant 0 as output). This takes polynomial time, and $C$ is equivalent to the constant 0 exactly when $C$ is unsatisfiable. $\square$

## Examples and non-examples

**A half adder.** $C_1$ has the outputs $s = a \oplus b$ and $c = a \wedge b$. $C_2$ has $s' = (a \vee b) \wedge \neg(a \wedge b)$ and $c' = \neg(\neg a \vee \neg b)$. The miter is $M = (s \oplus s') \vee (c \oplus c')$.

| $a$ | $b$ | $s$ | $s'$ | $c$ | $c'$ | $M$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 1 | 1 | 0 |

The miter is unsatisfiable, so the circuits are equivalent.

**A bug.** Replace $c'$ by $a \vee b$. Then $M(1, 0) = 0 \vee (0 \oplus 1) = 1$, and the input $a = 1, b = 0$ is a counterexample: the carry is 0 in $C_1$ and 1 in $C_2$.

**Non-example: wrong output matching.** If $s$ is paired with $c'$ and $c$ with $s'$, the miter is satisfiable although the circuits are equivalent. The miter checks equivalence under the given matching of inputs and outputs only. Finding the matching when the names do not give it is [Boolean matching](/boolean-matching/).

**Non-example: circuits with registers.** If $C_1$ and $C_2$ have latches, the XOR-OR structure on their outputs is not a miter in the sense above. With the latch outputs read as free inputs, a satisfying input can be a state that no input sequence reaches, so a satisfiable output does not show that the designs differ. The sequential form is the [product machine](/product-machine/), where the question is whether a state with output 1 is reachable. If the latches of the two designs are paired one to one, the miter of the next-state and output functions decides equivalence for that pairing; see [latch mapping](/latch-mapping/).

## Related definitions

- [Boolean equivalence checking](/boolean-equivalence-checking/) is the decision problem. The miter turns it into the satisfiability of one circuit, which BDDs, SAT solvers, [SAT sweeping](/sat-sweeping/) and [cutpoint equivalence checking](/cutpoint-equivalence-checking/) then decide.
- Brand used [automatic test pattern generation](/automatic-test-pattern-generation/) on the miter: the output stuck at 0 is a redundant fault exactly when no input sets the output to 1, so a proof that the fault is untestable is a proof of equivalence.
- The dual form joins XNOR gates with an AND gate. Its output is 1 everywhere exactly when the circuits are equivalent, so it turns equivalence into a tautology check.
- The [product machine](/product-machine/) is the miter of two sequential circuits, with both sets of latches kept.

## References
