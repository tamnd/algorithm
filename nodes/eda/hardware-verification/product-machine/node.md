---
tag: 0MGAEA
kind: definition
slug: product-machine
name: Product machine
aliases:
- product FSM
area: eda/hardware-verification
level: core
summary: The machine that runs two FSMs side by side on the same inputs and flags a mismatch of outputs; two designs are equivalent if no mismatch state is reachable.
prereqs: [mealy-machine, miter-circuit, reachability-problem]
see_also: [sequential-equivalence-checking, equivalence-checking, product-construction, dfa-equivalence, invariant-checking, state-explosion-problem, signal-correspondence, transition-function-image-computation]
sources:
  - paper: "Olivier Coudert, Christian Berthet and Jean Christophe Madre, Verification of synchronous sequential machines based on symbolic execution, Automatic Verification Methods for Finite State Systems, Lecture Notes in Computer Science 407, 1989"
    title: O. Coudert, C. Berthet and J. C. Madre, Verification of synchronous sequential machines based on symbolic execution, LNCS 407, Springer, 1989
    locator: the comparison of two machines by a symbolic traversal of the states of the machine that runs both
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the section on sequential equivalence checking, the product machine and its reachable states
---

The product machine of two finite state machines with the same inputs and outputs runs both machines in lockstep on one input stream. Its state is a pair of states, one of each machine, and its only output is 1 when the two machines give different outputs. Two designs that start in their initial states are sequentially equivalent exactly when no state with a possible output 1 is reachable in the product. So the product turns [sequential equivalence checking](/sequential-equivalence-checking/) into a [reachability problem](/reachability-problem/), or an [invariant check](/invariant-checking/), on one machine. For circuits, the product is the [miter](/miter-circuit/) of the two circuits with both sets of latches kept.

## Definition

A deterministic [Mealy machine](/mealy-machine/) is $M = (X, Y, S, s^0, \delta, \lambda)$ with input alphabet $X$, output alphabet $Y$, finite state set $S$, initial state $s^0$, next-state function $\delta : S \times X \to S$ and output function $\lambda : S \times X \to Y$. For a circuit, $S = \{0, 1\}^L$ for $L$ latches, $X = \{0, 1\}^n$ and $Y = \{0, 1\}^m$. Here "transition" means one step of $\delta$ on one input, a clock cycle.

Let $M_1$ and $M_2$ be such machines with the same $X$ and $Y$. Their *product machine* is

$$M_1 \times M_2 = \big(X,\ \{0, 1\},\ S_1 \times S_2,\ (s_1^0, s_2^0),\ \delta,\ \lambda\big),$$

$$\delta((p, q), x) = (\delta_1(p, x), \delta_2(q, x)), \qquad \lambda((p, q), x) = [\lambda_1(p, x) \ne \lambda_2(q, x)].$$

A state $(p, q)$ is *bad* if $\lambda((p, q), x) = 1$ for some input $x$. For Moore machines the outputs do not depend on $x$, and a bad state is one with $\lambda_1(p) \ne \lambda_2(q)$.

$M_1$ and $M_2$ are *sequentially equivalent* if, for every input sequence $x^0 x^1 \cdots x^t$, the two machines started in $s_1^0$ and $s_2^0$ give the same output sequence.

**Proposition (the product reduces equivalence to reachability).** $M_1$ and $M_2$ are sequentially equivalent if and only if no bad state is reachable from $(s_1^0, s_2^0)$ in $M_1 \times M_2$.

*Proof.* For an input sequence $w = x^0 \cdots x^t$, let $p^i$ and $q^i$ be the states of $M_1$ and $M_2$ before step $i$. By the definition of $\delta$, $(p^i, q^i)$ is the state of the product after the prefix $x^0 \cdots x^{i-1}$, so it is reachable. Every reachable state arises in this way.

(If) Suppose the outputs differ on $w$, first at step $i$. Then $\lambda_1(p^i, x^i) \ne \lambda_2(q^i, x^i)$, so the reachable state $(p^i, q^i)$ is bad.

(Only if) Suppose $(p, q)$ is bad with witness $x$ and is reached by $x^0 \cdots x^{i-1}$. Then on the input sequence $x^0 \cdots x^{i-1} x$, the machines give different outputs at the last step. $\square$

The product of circuits with $L_1$ and $L_2$ latches has $L_1 + L_2$ latches and is built in linear size, but its state space has $2^{L_1 + L_2}$ states, the [state explosion problem](/state-explosion-problem/) in its plainest form.

## Examples and non-examples

**Two encodings of a parity bit.** $M_1$ has one latch $p$, initial value 0, next state $p \oplus x$ and output $p$. $M_2$ has two latches $q_1 q_2$ with initial value $10$, swaps them when $x = 1$, keeps them when $x = 0$, and outputs $q_2$. So $M_2$ is a one-hot encoding of the same bit. The product has 8 states $(p, q_1 q_2)$.

| state | reachable | bad |
|---|---|---|
| $(0, 10)$ | yes, initial | no |
| $(1, 01)$ | yes, after $x = 1$ | no |
| $(0, 01)$, $(1, 10)$ | no | yes |
| $(1, 00)$, $(0, 11)$ | no | yes |
| $(0, 00)$, $(1, 11)$ | no | no |

The reachable states are $(0, 10)$ and $(1, 01)$, and neither is bad, so the machines are equivalent. Four bad states exist, but none is reachable. A check of the miter of the combinational parts alone, with latch values as free inputs, would report a difference at $(0, 01)$.

**A difference.** Give $M_2$ the initial value $01$. Then the initial state $(0, 01)$ is bad, and the empty prefix with any input $x$ separates the machines.

**Non-example: different input sets.** If one design has an input that the other lacks, the product is not defined until the inputs are matched or the extra input is fixed. The product compares behaviour for one shared input stream.

**Non-example: no initial state.** The proposition uses the pair of initial states. For designs without a reset, the question is about all power-up states, and reachability from one pair does not answer it; see [safe replaceability](/safe-replaceability/).

## Related definitions

- [Equivalence checking](/equivalence-checking/) for labelled transition systems compares possibly nondeterministic systems by bisimulation, trace equivalence and other behavioural relations, with no inputs and outputs in the sense above. For deterministic machines with inputs and outputs, as here, these notions agree, and the product reduces the question to reachability.
- The [product construction](/product-construction/) of finite automata is the same pairing of states, and [DFA equivalence](/dfa-equivalence/) uses it with "accepting in exactly one automaton" as the bad states.
- The [miter](/miter-circuit/) is the product with no latches; reachability is then trivial, and the question is satisfiability.
- [Signal correspondence](/signal-correspondence/) proves that no bad state is reachable by an inductive invariant of the product, and [image computation](/transition-function-image-computation/) computes its reachable states with BDDs.

## References
