---
tag: FEMWRD
kind: problem
slug: sequential-equivalence-checking
name: Sequential equivalence checking
aliases:
- sequential equivalence
area: eda/hardware-verification
level: core
summary: Decide whether two sequential circuits with possibly different state encodings produce the same outputs for every input sequence from their initial states.
prereqs: [product-machine, reachability-problem, pspace]
see_also: [signal-correspondence, latch-mapping, safe-replaceability, boolean-equivalence-checking, bounded-model-checking, k-induction, ic3-pdr, dfa-equivalence]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage Learning, 2013
    locator: Chapter 8, Section 8.1 (Savitch's theorem, NPSPACE = PSPACE) and Section 8.3 (PSPACE-completeness and the encoding of configurations of a space-bounded machine)
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the definition of sequential equivalence, the product machine, and the survey of methods based on reachability, register correspondence and induction
  - paper: "Carl Pixley, A theory and implementation of sequential hardware equivalence, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 11(12), 1469 to 1478, 1992"
    title: C. Pixley, A theory and implementation of sequential hardware equivalence, IEEE TCAD 11(12), 1469 to 1478, 1992
    locator: equivalence of designs without a known initial state, aligning sequences, and the BDD-based decision procedure
  - paper: "C. A. J. van Eijk, Sequential equivalence checking based on structural similarities, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 19(7), 814 to 819, 2000"
    title: C. A. J. van Eijk, Sequential equivalence checking based on structural similarities, IEEE TCAD 19(7), 814 to 819, 2000
    locator: the inductive proof of equal signals of the product machine without computing its reachable states
---

Sequential equivalence checking asks whether two circuits with registers, each started in its initial state, give the same output sequence for every input sequence. The circuits can have different numbers of latches and different state encodings, so their states cannot be compared bit by bit. The [product machine](/product-machine/) reduces the problem to the [reachability](/reachability-problem/) of a state where the outputs can differ. For circuits given as netlists the problem is [PSPACE](/pspace/)-complete, against coNP-complete for [combinational equivalence](/boolean-equivalence-checking/). This page is the problem and its complexity. [Signal correspondence](/signal-correspondence/) is one algorithm for it, sound but not complete.

## In plain words

Two chips have the same pins. Each has memory inside, and each starts from a fixed reset value. You feed both chips the same stream of inputs, one value per clock tick, and watch the outputs. The chips are equivalent if their outputs agree on every tick for every stream you could feed them. The memories can be organized in different ways, for example a counter in binary in one chip and in a one-hot code in the other. So you cannot just compare memory bits. You must show that no stream of inputs ever leads the two chips to a point where they disagree.

## Definition

**Input.** Two synchronous circuits $C_1$ and $C_2$ with the same primary inputs $x \in \{0, 1\}^n$ and the same outputs, matched by name. Circuit $C_i$ has $L_i$ latches with initial values $s_i^0$, a next-state function $\delta_i(s, x)$ and an output function $\lambda_i(s, x)$, all given as gates. Here a transition is one clock cycle: one step of $\delta_i$ on one input vector.

**Output.** *Yes* if for every input sequence $x^0 x^1 \cdots x^t$ the two output sequences from $s_1^0$ and $s_2^0$ are equal, and *no* otherwise. A useful checker gives a *counterexample* for *no*: an input sequence after which the outputs differ.

By the proposition on the [product machine](/product-machine/) page, the answer is *yes* exactly when no state $(p, q)$ with $\lambda_1(p, x) \ne \lambda_2(q, x)$ for some $x$ is reachable from $(s_1^0, s_2^0)$.

## Variants

- **Bounded equivalence.** Equal outputs for all sequences of length at most $k$. With $k$ given in unary this is coNP-complete: unroll both circuits $k$ times into one combinational [miter](/miter-circuit/), and the case $k = 1$ with no latches is combinational equivalence. [Bounded model checking](/bounded-model-checking/) solves it.
- **Equivalence with a register correspondence.** If the latches are paired one to one and paired latches always hold equal values, a combinational check of the next-state and output functions is enough. Finding the pairing is [latch mapping](/latch-mapping/).
- **No known initial state.** Designs without a reset power up in any state. Pixley (1992) asks for equivalence after an aligning input sequence; Singhal and Pixley ask that every state of the new design behave like some state of the old one, which is [safe replaceability](/safe-replaceability/). Neither is a reachability question from one state pair.
- **Sets of initial states, and don't care outputs.** The question can be asked for a set of initial states, or with outputs that need to agree only when a valid signal is 1.
- **Explicit machines.** For machines given by state tables, the question is [DFA equivalence](/dfa-equivalence/) in disguise, with output symbols in place of acceptance.

## Examples

**Different encodings.** A parity bit kept in one latch and the same bit kept as a one-hot pair of latches are equivalent. The [product machine](/product-machine/) page lists the 8 product states: 4 of them are bad, and none of the bad ones is reachable.

**A retimed register.** $C_1$ has one latch $r$ with initial value 0, next value $a \wedge b$ and output $r$. $C_2$ has two latches $u, v$ with initial values $0, 0$, next values $a$ and $b$, and output $u \wedge v$. At clock 0 both outputs are 0, and at clock $t \ge 1$ both are $a^{t-1} \wedge b^{t-1}$. The circuits are equivalent, but they have 1 and 2 latches, so no one-to-one latch pairing exists, and the check needs more than combinational equivalence. [Retiming](/retiming/) produces such pairs.

**A wrong initial value.** Give $u$ and $v$ the initial values $1, 1$. The outputs at clock 0 are 0 and 1, so the empty prefix already separates the circuits. The combinational parts are the same as before, so only the initial states differ.

## Known algorithms

All exact methods work on the product machine. They differ in how they prove that no bad state is reachable.

| method | answer | note |
|---|---|---|
| explicit search of the product | exact | only for small state spaces; see [explicit-state model checking](/explicit-state-model-checking/) |
| BDD reachability of the product | exact, with a shortest counterexample | [symbolic reachability](/symbolic-reachability/), with [image computation](/transition-function-image-computation/) or a [partitioned transition relation](/partitioned-transition-relation/) |
| latch mapping, then a combinational check | sound; complete only when the mapping is right | [latch mapping](/latch-mapping/), [cutpoint equivalence checking](/cutpoint-equivalence-checking/) |
| [signal correspondence](/signal-correspondence/) | sound, not complete | an inductive proof of equal signals, no reachable states |
| [bounded model checking](/bounded-model-checking/) | counterexamples up to a bound | bug finding |
| [k-induction](/k-induction/) | exact for a large enough $k$ when made complete with simple paths | often with signal correspondence as a strengthening |
| [IC3](/ic3-pdr/) | exact | builds an inductive invariant of the product |

In practice, checkers first merge equal signals with simulation and [SAT sweeping](/sat-sweeping/), prove what they can by induction, and give the rest to a model checker.

## Bounds

**Theorem.** Sequential equivalence of circuits given as netlists is PSPACE-complete.

*Proof.* Let $N$ be the total size of the two circuits and $L = L_1 + L_2$.

*In PSPACE.* We show that non-equivalence is in NPSPACE. A nondeterministic machine keeps the product state $(p, q)$ in $L$ bits and a counter $c$ in $L$ bits, starting from $(s_1^0, s_2^0)$ and $c = 0$. At each step it guesses an input $x$ and evaluates both circuits on $(p, x)$ and $(q, x)$ in space $O(N)$. If the outputs differ, it accepts. Otherwise it sets $(p, q) \leftarrow (\delta_1(p, x), \delta_2(q, x))$ and $c \leftarrow c + 1$, and it rejects when $c$ reaches $2^L$. If the circuits differ, a bad product state is reachable, and a shortest path to it visits no state twice, so it has fewer than $2^L$ steps; some run accepts. If they are equivalent, no run accepts. The space is $O(N + L)$, so non-equivalence is in NPSPACE, which is PSPACE by [Savitch's theorem](/savitch-theorem/) (Sipser, Section 8.1). PSPACE is a deterministic class, so it is closed under complement, and equivalence is in PSPACE too.

*PSPACE-hard.* Let $L'$ be any language in PSPACE. Its complement is also in PSPACE, so it is decided by a deterministic Turing machine $D$ in space $p(m)$ on inputs of length $m$. Change $D$ so that its accepting and rejecting states loop on themselves. For an input $w$, build a circuit $C_w$ with no primary inputs. Its latches hold a configuration of $D$: $p(m)$ cells, each with a tape symbol and a marker for the head and the control state. Their initial values are the initial configuration on $w$, and the next-state logic makes one step of $D$, cell by cell from the cells $j - 1$, $j$ and $j + 1$. This is the circuit of the PSPACE-hardness proof on the [reachability problem](/reachability-problem/) page, of size $O(p(m))$. The output of $C_w$ is 1 when the control state is accepting. Compare $C_w$ with $C_0$, a circuit with no latches and the constant 0 as output. The output sequence of $C_w$ is all 0 exactly when $D$ never accepts $w$, so $C_w$ and $C_0$ are equivalent exactly when $w \notin \overline{L'}$, that is, $w \in L'$. The map $w \mapsto (C_w, C_0)$ is computed in polynomial time, so it is a [polynomial-time reduction](/polynomial-time-reduction/) from $L'$. $\blacksquare$

The hard instances have no inputs at all, so the hardness comes from the state encoded in latches, not from the inputs. The combinational case, with no latches, is coNP-complete, as the [miter](/miter-circuit/) page proves. For machines given by explicit state tables, a search of the product takes time linear in its size, and [Hopcroft and Karp's method](/hopcroft-karp-equivalence/) is near-linear in the sum of the sizes. We know of no single primary paper for the theorem; the proof above uses the standard tools in Sipser, Chapter 8.

## Reductions

- **To reachability and invariant checking.** The product machine reduces non-equivalence to the reachability of a bad state in linear time, and equivalence to [invariant checking](/invariant-checking/) of "the outputs agree".
- **From combinational equivalence.** Circuits with no latches are a special case.
- **From reachability.** The hardness proof turns a space-bounded machine into a circuit; in the same way, reachability of a target in a circuit reduces to equivalence with a circuit whose output is constant 0.
- **To combinational equivalence, under a latch mapping.** If the latches are paired and the pairing is an invariant, equivalence of the next-state and output functions as combinational circuits implies sequential equivalence. The converse fails, because the combinational check also looks at unreachable states.

## Applications

- **Retiming and sequential synthesis.** [Retiming](/retiming/), re-encoding of states by [state assignment](/state-assignment/), and the removal of redundant latches change the latches, so a combinational check cannot verify them.
- **RTL against a netlist.** When synthesis changes the register structure, for example by pipelining or by clock gating, the RTL model and the gate netlist are compared sequentially.
- **Engineering change orders.** A late change to a netlist is checked against the version before the change.

## References
