---
tag: 82JHVM
kind: definition
slug: fsm-coverage
name: FSM coverage
aliases:
- state coverage
- transition coverage
area: eda/hardware-verification
level: core
summary: The fraction of the states and transitions of the extracted controller FSMs of a design that a test suite visits, a coverage metric for control logic.
prereqs: [mealy-machine, code-coverage-metrics]
see_also: [functional-coverage, state-assignment, reachability-problem, symbolic-reachability, product-machine, chinese-postman-problem, finite-state-machine-with-datapath, observability-based-coverage]
sources:
  - paper: doi:10.1109/ICCAD.1996.569537
    title: Richard C. Ho and Mark A. Horowitz, Validation coverage analysis for complex digital designs, ICCAD 1996, 146 to 151
    locator: the extraction of the control state machines of a design and coverage of their states and transitions as a validation metric
  - paper: doi:10.1109/54.936247
    title: Serdar Tasiran and Kurt Keutzer, Coverage metrics for functional validation of hardware designs, IEEE Design and Test of Computers 18(4), 36 to 45, 2001
    locator: the section on state-machine based metrics (state, transition and path coverage of FSMs) and their limits
  - book: isbn:9781402080258
    title: Andrew Piziali, Functional Verification Coverage Measurement and Analysis, Kluwer, 2004
    locator: the discussion of FSM coverage as a structural metric next to code coverage (general locator)
---

FSM coverage is a structural coverage metric for the control logic of a hardware design. A tool finds the registers that hold the state of a controller, extracts the finite state machine that their next-state logic defines, and reports which states the simulation runs visited (state coverage) and which arcs between states they traversed (transition coverage). It differs from [code coverage](/code-coverage-metrics/), which counts lines, decisions, conditions and toggles of the source text, and from [functional coverage](/functional-coverage/), which counts events that the verification engineer chose.

## Definition

**The extracted FSM.** A *state register* is a register $q$ whose next value is given by a case analysis on its own current value, with constant values in each arm, as in `case (state) IDLE: if (req) next = BUSY; ...`. Tools find such registers by this pattern or from a declared enumerated type. The extracted FSM is

$$ M = (S, s_0, X, \delta), $$

where $S$ is the set of state values that the code names, $s_0 \in S$ is the reset value, $X$ is the set of values of the other signals that the next-state logic reads, and $\delta : S \times X \to S$ is the next-state function. Its *arcs* are the pairs

$$ A = \{ (s, s') \in S \times S : \delta(s, x) = s' \text{ for some } x \in X \}. $$

Whether self-loops $(s, s)$ count as arcs is a tool option.

**Visited states and traversed arcs.** A run $\tau$ samples $q$ at each clock edge and gives a sequence $q_0 q_1 \ldots q_{\ell}$. For a suite $T$ of runs,

$$ V(T) = \{ q_t : \text{some run in } T \text{ has } q_t \}, \qquad E(T) = \{ (q_t, q_{t+1}) : \text{some run in } T \text{ has these values at } t \text{ and } t + 1 \}. $$

A reset between two runs does not create an arc.

**The two metrics.** For a denominator $S^\ast \subseteq S$ and $A^\ast \subseteq A$,

$$ \text{state coverage} = \frac{|V(T) \cap S^\ast|}{|S^\ast|}, \qquad \text{transition coverage} = \frac{|E(T) \cap A^\ast|}{|A^\ast|}. $$

Two choices of denominator are common, and a reported number must say which one it uses:

- the *declared* sets, $S^\ast = S$ and $A^\ast = A$, read from the code alone;
- the *reachable* sets $S_R$ and $A_R$: the states and arcs that some input sequence from reset reaches in the whole design, where the rest of the design may forbid some values of $X$ in some states. Computing them is a [reachability](/reachability-problem/) problem, usually solved by [symbolic reachability](/symbolic-reachability/).

**Fact (arcs cover states).** If every run starts at $s_0$ and $E(T) \supseteq A_R$, then $V(T) \supseteq S_R$. A reachable state $s \ne s_0$ is the end of the last arc of some path from $s_0$, and that arc is in $A_R$ and so is traversed; $s_0$ is visited at the start of every run. The converse fails, as the second example shows.

**What it guarantees.** Full coverage says that each state was entered and each arc was taken at least once, in the implementation. It does not say:

- *under which input the arc fired.* An arc with the guard `req && !abort` and the same arc with the guard `req` look the same;
- *that the arc is right.* The metric counts the arcs of the code, so a wrong arc is covered like a right one, and an arc that the specification needs but the code lacks is not in $A$ at all;
- *anything about sequences.* Each arc alone was taken, not each path of two or more arcs. Some tools offer coverage of arc pairs or of paths up to a length $k$, which are stronger and grow fast with $k$;
- *anything about the datapath* that the controller drives, or about whether a wrong state value was ever observed at an output.

## Examples and non-examples

**Full coverage that misses a bug.** The specification of a small controller says: in IDLE, go to BUSY on `req && !abort`, else stay; in BUSY, go to DONE on `fin`, else stay; from DONE, go to IDLE. The code forgets `abort`:

```
case (state)
  IDLE: next = req ? BUSY : IDLE;   // bug: the specification says req && !abort
  BUSY: next = fin ? DONE : BUSY;
  DONE: next = IDLE;
endcase
```

The extracted FSM has 3 states and 5 arcs: IDLE to IDLE, IDLE to BUSY, BUSY to BUSY, BUSY to DONE and DONE to IDLE. One run from reset with the inputs $(\mathit{req}, \mathit{abort}, \mathit{fin}) = (0,0,0), (1,0,0), (0,0,0), (0,0,1), (0,0,0)$ takes the arcs in that order. State coverage is 3 of 3 and transition coverage is 5 of 5. The bug needs `req` and `abort` both 1 in IDLE, which this run never applies, and the arc IDLE to BUSY is covered under the wrong guard. Since `abort` does not occur in the code, no [code coverage](/code-coverage-metrics/) item mentions it either.

**All states, not all arcs.** On the same code, the run $(1,0,0), (0,0,1), (0,0,0)$ goes IDLE, BUSY, DONE, IDLE. State coverage is 3 of 3, and transition coverage is 3 of 5, since the self-loops at IDLE and BUSY are never taken. A bug in the "stay in BUSY" arm stays hidden.

**The denominator matters.** Encode the three states in 2 bits as 00, 01 and 10, and add a recovery arm `default: next = IDLE`. Counted over all four encodings, the value 11 is a declared state, and the arc from 11 to IDLE is a declared arc. Neither is reachable from reset, so the best possible score is 3 of 4 states and 5 of 6 arcs against the declared sets, and 3 of 3 and 5 of 5 against the reachable sets.

**Non-example: a counter.** A 4-bit counter `q <= q + 1` is not extracted as a controller: its next value is arithmetic on $q$, not a case analysis with constant arms. If it were treated as an FSM, it would have 16 states and 16 arcs, and transition coverage would need 16 cycles, while its one statement, which has no decision, is covered after a single cycle. This shows that FSM coverage and code coverage count different things on the same code.

**Non-example: one-hot without a case.** A controller written as separate flip-flops with ad hoc next-state equations has the same behavior as an encoded one, but a tool that looks for the case pattern may not extract it. Then no FSM coverage is reported for it, which says nothing about how well it was exercised.

## Related definitions

- **[Code coverage metrics](/code-coverage-metrics/).** Line, decision, condition and toggle counts of the source text. When the code writes each arc as its own arm, as in the controller above, full decision coverage of the `case` and of the choices inside it takes every arc, and the two metrics agree. They part when the code does not spell out the arcs: an arm such as `BUSY: next = table[op];` is one decision outcome that can lead to several states, and the counter above is the extreme case.
- **[Functional coverage](/functional-coverage/).** Coverage items that the engineer writes, for example a cross of the state with the inputs, which would have exposed the missing `abort` above: the bin "IDLE with `req` and `abort`" stays empty.
- **[Mealy machine](/mealy-machine/) and [Moore machine](/moore-machine/).** The extracted FSM is the next-state part of one of these, with outputs ignored.
- **[State assignment](/state-assignment/).** The encoding of the states in bits decides the declared denominator: unused codes appear as declared states.
- **[Product machine](/product-machine/).** The reachable sets $S_R$ and $A_R$ are computed on the product of the controller with the rest of the design, not on the controller alone.
- **Transition tours.** When every guard can be met at will and the FSM is strongly connected, a shortest input sequence that takes every arc is a directed [Chinese postman](/chinese-postman-problem/) tour. A stimulus generator that aims at full transition coverage can follow such a tour, when it can steer the inputs that the guards read.
- **[Observability-based coverage](/observability-based-coverage/).** Counts an item only when an error at it would reach an output, which neither state nor transition coverage checks.

## References
