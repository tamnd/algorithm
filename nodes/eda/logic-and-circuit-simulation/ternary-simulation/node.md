---
tag: 9Z1Y7X
kind: algorithm
slug: ternary-simulation
name: Ternary simulation
aliases:
- Eichelberger hazard detection
- three-valued simulation
area: eda/logic-and-circuit-simulation
level: advanced
summary: "Eichelberger's two-phase simulation with X for signals that may change: it finds static hazards and critical races, and each 0 or 1 it reports holds for all gate and wire delays."
solves: [logic-simulation]
model: word-ram
complexity:
  vars: {n: the number of gates (state variables), P: the number of gate input pins}
  time: {worst: "O(n (n + P))", best: "O(n + P)"}
  space: {extra: "O(n + P)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1965
  people: [Edward B. Eichelberger]
  note: Eichelberger gave the two procedures with the value X for hazards and races in 1965. Brzozowski and Yoeli (1979) and Brzozowski and Seger (1987) gave the exact meaning of the result in terms of gate and wire delays.
prereqs: [multi-valued-logic-simulation, logic-simulation, fixed-point]
see_also: [event-driven-logic-simulation, kleene-fixed-point-theorem, knaster-tarski-theorem, abstract-interpretation, prime-implicant, symbolic-trajectory-evaluation, switch-level-simulation, inertial-and-transport-delay]
sources:
  - paper: doi:10.1147/rd.92.0090
    title: E. B. Eichelberger, Hazard detection in combinational and sequential switching circuits, IBM Journal of Research and Development 9(2), 90 to 99, 1965
    locator: the two procedures with the third value for changing signals, the detection of static hazards in combinational circuits and of critical races in sequential circuits
  - book: doi:10.1007/978-1-4612-4210-9
    title: Janusz A. Brzozowski and Carl-Johan H. Seger, Asynchronous Circuits, Springer, New York, 1995, ISBN 0-387-94420-6
    locator: Chapter 7, Ternary Simulation, pages 113 to 141 (Algorithms A and B, and their relation to the binary race analysis)
  - paper: "Janusz A. Brzozowski and Carl-Johan Seger, A characterization of ternary simulation of gate networks, IEEE Transactions on Computers C-36(11), 1318 to 1327, 1987"
    title: J. A. Brzozowski and C.-J. Seger, A characterization of ternary simulation of gate networks, IEEE Transactions on Computers C-36(11), 1318 to 1327, 1987
    locator: the results of ternary simulation equal the results of binary race analysis when every gate and every wire has a delay
  - paper: "Janusz A. Brzozowski and Michael Yoeli, On a ternary model of gate networks, IEEE Transactions on Computers C-28(3), 178 to 184, 1979"
    title: J. A. Brzozowski and M. Yoeli, On a ternary model of gate networks, IEEE Transactions on Computers C-28(3), 178 to 184, 1979
    locator: the ternary model and its relation to the multiple-winner race model
---

Ternary simulation evaluates a gate circuit with the three values 0, 1 and X, where X means "this signal may be 0 or 1, or may be changing". Eichelberger (1965) used it to find hazards and races caused by an input change. Phase A sets every input that changes to X and lets the X spread through the circuit until nothing more changes. Phase B then sets the inputs to their new values and lets the circuit settle again. A signal that is 0 or 1 after phase A cannot change at all, whatever the gate and wire delays are, so it has no glitch. A signal that has the same value before and after the change but is X after phase A may have a static hazard. A signal that is X after phase B may end in either value or never settle: a critical race. This page is in the logic simulation half of [logic and circuit simulation](/logic-simulation/). Its delay model is the weakest one: every gate and every wire may have any delay, and each 0 or 1 that ternary simulation gives holds for all of them. The price is pessimism: X can appear where a careful analysis would find a known value.

## In plain words

Suppose an input switches from 1 to 0. While it switches, nobody knows which value the gates see, so call it X, for "unknown".

Phase A pushes this X forward. Each gate gives 0 or 1 if its known inputs already fix the answer, as 0 does for an AND, and X otherwise. The X can only spread, never shrink, so after at most one round per gate nothing changes. Every wire that is still 0 or 1 is safe: it cannot flicker, however slow or fast the gates are.

Phase B gives the input its new value and lets the circuit settle again. A wire that is still X after that has no final value that you can rely on.

A wire that starts at 1, ends at 1, but was X in phase A may show a short wrong pulse. That is a hazard.

## The problem

The input is a gate circuit with primary inputs and $n$ gates, possibly with loops, as in latches and other asynchronous circuits. Each gate output is a state variable. For an input vector $u$ and a state $s$, let $F(u, s)$ be the state obtained by evaluating every gate once on these values. A state $s_0$ is stable under the input $a$ when $F(a, s_0) = s_0$. The input then changes from $a$ to $b$.

The question is what can happen during and after this change: which signals may change for a short time, and which end in a value that depends on the delays. The values are ordered by information: $0 \sqsubseteq X$ and $1 \sqsubseteq X$, and vectors are ordered position by position. The least upper bound of 0 and 1 is X. The gates use Kleene's three-valued tables, which give each gate the exact three-valued extension of its Boolean function: the output is 0 or 1 when all binary completions of the inputs agree, and X otherwise. See [multi-valued logic simulation](/multi-valued-logic-simulation/).

## The algorithm

```pseudo id=main
TERNARY-SIM(C, a, b, s0)                  (s0 is stable under the input a)
L1  â ← lub(a, b): each input that differs between a and b becomes X
L2  s ← s0
L3  repeat                                         (phase A)
L4      s' ← F(â, s), every gate evaluated with the three-valued tables
L5      done ← (s' = s); s ← s'
L6  until done
L7  t ← s                                          (phase B)
L8  repeat
L9      t' ← F(b, t); done ← (t' = t); t ← t'
L10 until done
L11 return s_A = s and t_B = t
```

Read the results net by net, with $s_0$ the value before the change:

- $s_A = s_0$ (binary): the net does not change during the transition, for any delays.
- $s_0 = t_B$ (binary) and $s_A = X$: the net may have a static hazard, a short pulse to the other value.
- $s_0 \ne t_B$, both binary: the net changes to its new value. Ternary simulation cannot tell whether it does so once or with extra pulses, a dynamic hazard, because both cases give $s_A = X$.
- $t_B = X$: the final value is not determined by the circuit alone. In a sequential circuit this is a critical race or an oscillation.

Ternary simulation is sometimes said to detect dynamic hazards. It does not, for the reason in the third case above. Finding dynamic hazards needs more values, as in the hazard algebras of Brzozowski and Ésik.

For a combinational circuit with some inputs at X and no change at all, the same iteration from the all-X state gives the plain three-valued evaluation of the circuit, which is how X handling works in gate-level simulation, test generation and [symbolic trajectory evaluation](/symbolic-trajectory-evaluation/).

## Example

Take $y = ab + a'c$ built from $\bar a = \mathrm{NOT}(a)$, $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(\bar a, c)$ and $y = \mathrm{OR}(p, q)$. Let $b = c = 1$ and let $a$ fall from 1 to 0. The stable start is $s_0 = (\bar a, p, q, y) = (0, 1, 0, 1)$. Phase A uses $\hat a = (X, 1, 1)$, and phase B uses $b = (0, 1, 1)$.

| step | $\bar a$ | $p$ | $q$ | $y$ |
| --- | --- | --- | --- | --- |
| $s_0$ | 0 | 1 | 0 | 1 |
| A1 | X | X | 0 | 1 |
| A2 | X | X | X | X |
| A3 | X | X | X | X (no change, $s_A$ found) |
| B1 | 1 | 0 | X | X |
| B2 | 1 | 0 | 1 | X |
| B3 | 1 | 0 | 1 | 1 |
| B4 | 1 | 0 | 1 | 1 (no change, $t_B$ found) |

So $y$ is 1 before and after but X after phase A: a static 1-hazard. A unit-delay simulation shows it as a pulse to 0 two time units after the change, as on the [event-driven page](/event-driven-logic-simulation/). Adding the consensus term $r = \mathrm{AND}(b, c)$, so $y = ab + a'c + bc$, removes it: in phase A, $r = 1$ keeps $y = 1$ at every step. This is an instance of a theorem of Eichelberger: a sum of products in which no term holds a variable together with its complement is free of hazards in the ternary sense exactly when it contains all [prime implicants](/prime-implicant/) of its function.

For a sequential example, take a latch of two NAND gates, $q = \mathrm{NAND}(\bar S, \bar q)$ and $\bar q = \mathrm{NAND}(\bar R, q)$, at rest with $\bar S = \bar R = 0$, so $q = \bar q = 1$. Let both inputs rise to 1 at once. Phase A gives $q = \bar q = X$, and phase B keeps them at X, because $\mathrm{NAND}(1, X) = X$. The final state depends on which gate is faster: a critical race. A normal set, with $\bar S$ falling from 1 to 0 while $q = 0$ and $\bar q = 1$, gives $s_A = (X, X)$ and $t_B = (1, 0)$, so the latch ends in a known state.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following, all exactly.

1. Every gate table is monotone in the information order and exact on binary inputs, so $F$ is monotone. So ternary evaluation is sound: if a net gets 0 or 1 under a vector with some X inputs, every binary completion of the vector gives the same value. On fanout-free circuits it is also exact.
2. Phase A climbs: $s_0 \sqsubseteq F(\hat a, s_0) \sqsubseteq \cdots$, so it stops after at most $n$ changing steps, at the least fixed point of $F(\hat a, \cdot)$ above $s_0$. Phase B descends from $s_A$ and stops after at most $n$ changing steps at the greatest fixed point of $F(b, \cdot)$ below $s_A$.
3. In any run with any gate and wire delays, as long as every new value of a gate output is its gate function applied to values its inputs held earlier, every value of every net is below $s_A$. So a net that is binary in $s_A$ never changes. Every stable state that such a run reaches is below $t_B$.

So the 0 and 1 results are sound for every delay assignment. The converse, that every X found by phase A is a real change under some gate and wire delays and that phase B finds exactly the final behaviors, is a theorem of Brzozowski and Seger (1987) that this page cites and does not prove. With delays only on gates and none on wires, the converse can fail.

The tests check the gate tables against all completions, soundness on random circuits against all completions, exactness on random fanout-free circuits, the step bounds and the bounds on every reachable state by an exhaustive search over the multiple-winner race model on random circuits with loops, and the absence of glitches on binary nets under random integer gate delays.

## Complexity

Each application of $F$ evaluates every gate once and costs $O(n + P)$. Phase A changes at least one variable from binary to X at each step that is not the last, and phase B changes at least one from X to binary, so each phase makes at most $n + 1$ applications. The total is $O(n(n + P))$, and the space is $O(n + P)$. An event-driven version that evaluates only the fanout of the variables that changed brings the cost down to $O(P k)$, with $k$ the largest fan-in, since each variable changes at most once per phase. A binary race analysis that tries every order of gate changes can need time exponential in $n$.

## Properties

- **Sound, not complete.** Each 0 or 1 is right for every delay assignment and every binary completion. An X may hide a known value.
- **X pessimism on reconvergent fanout.** In the multiplexer $y = s a + s' b$ with $a = b = 1$ and $s = X$, the circuit gives $y = X$, although both completions give 1. The X reaches the OR gate along two paths, and the tables do not remember that the two copies are the same signal and opposite. On circuits without reconvergent fanout, ternary evaluation is exact.
- **Monotone.** Replacing a binary input by X can only replace binary outputs by X, never change a 0 into 1.
- **Cheap.** The cost is polynomial, while the exact analysis of all delay orders is exponential.

## Variants and improvements

- **Plain X simulation.** With no input change, evaluating from the all-X state gives the three-valued value of every net under inputs with X. Simulators use it for unknown initial states, and test tools for unknown values in scan cells.
- **More values.** Five-valued and eight-valued algebras keep more history, such as "changed from 0 to 1", and the hazard algebras of Brzozowski and Ésik detect dynamic hazards.
- **Symbolic trajectory evaluation.** STE runs ternary simulation over symbolic values and uses the information order to check properties of a circuit with a small number of symbolic variables.
- **Event-driven ternary simulation.** Evaluate only the gates whose inputs changed in the last step, as in [event-driven simulation](/event-driven-logic-simulation/).
- **Switch-level circuits.** The same X value and the same monotone arguments work for transistor networks in [switch-level simulation](/switch-level-simulation/).

## When to use it

Use ternary simulation to check an asynchronous circuit or a latch design for hazards and races after each input change, to screen a combinational circuit for static hazards, and to simulate designs whose initial state is unknown. It needs no delay values, which makes it a good first check before any timing is known. When it reports X, follow up with an exact method: a race analysis over the possible orders, or timed simulation with real delays.

## Pitfalls

- **Reading every X as a real problem.** X is a warning, not a proof. Reconvergent fanout gives X on safe nets.
- **Expecting dynamic hazards.** A net that changes from 0 to 1 always gets X in phase A, with or without extra pulses.
- **Starting from an unstable state.** The theorems need $F(a, s_0) = s_0$. From an unstable start, phase A need not climb.
- **Changing inputs one at a time.** Setting the changing inputs to X one after another can miss a race between them. Set them all to X together, as line L1 does.
- **Gate delays without wire delays.** A model that puts delays only on gates can call a circuit hazard-free when a wire delay would show a hazard. Ternary simulation is sound for the wider model, which is the safe side.

## Implementations

## History

Edward Eichelberger at IBM presented ternary hazard detection at the Symposium on Switching Circuit Theory and Logical Design in 1964 and in the IBM Journal of Research and Development in 1965. He gave the two procedures, called A and B in later work, and used them for static hazards in combinational circuits and critical races in sequential circuits. Brzozowski and Yoeli (1979) related the ternary model to binary race analysis. Brzozowski and Seger (1987) proved that ternary simulation gives exactly the results of the binary analysis when every gate and every wire may have a delay, and their 1995 book gives the full theory. Bryant carried the X value into switch-level simulation in the 1980s, and Seger and Bryant built symbolic trajectory evaluation on it.

## References
