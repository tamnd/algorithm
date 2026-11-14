---
tag: Z1Y4FS
kind: algorithm
slug: switch-level-simulation
name: Switch-level simulation
aliases:
- MOSSIM switch-level model
- Bryant switch-level simulation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Bryant's simulation of MOS circuits as networks of switch transistors and charged nodes with discrete strengths, between gate-level and circuit simulation.
solves: [logic-simulation]
model: word-ram
complexity:
  vars: {N: the number of storage nodes, T: the number of transistors, R: the number of rounds until the network settles}
  time: {worst: "O(R (N + T) log N)", best: "O((N + T) log N)"}
  space: {extra: "O(N + T)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1981
  people: [Randal E. Bryant]
  note: Bryant described MOSSIM at the Design Automation Conference in 1981 and gave the formal switch-level model with strengths and the algorithm of MOSSIM II in 1984.
prereqs: [channel-connected-component, multi-valued-logic-simulation, widest-path]
see_also: [ternary-simulation, event-driven-logic-simulation, timing-simulation, dijkstra, disjoint-set, circuit-extraction, symbolic-trajectory-evaluation, fault-simulation]
sources:
  - paper: doi:10.1109/TC.1984.1676408
    title: R. E. Bryant, A switch-level model and simulator for MOS digital systems, IEEE Transactions on Computers C-33(2), 160 to 177, 1984
    locator: the switch graph, node sizes and transistor strengths, the steady-state response with definite and potential paths, the partition into components and the simulation algorithm of MOSSIM II
  - paper: "R. E. Bryant, MOSSIM: a switch-level simulator for MOS LSI, Proceedings of the 18th Design Automation Conference, 786 to 790, 1981"
    title: R. E. Bryant, MOSSIM, a switch-level simulator for MOS LSI, Proceedings of the 18th Design Automation Conference, 786 to 790, 1981
    locator: the first switch-level simulator, with node states 0, 1 and X and transistor states open, closed and unknown
  - book: isbn:9780780310629
    title: M. Abramovici, M. A. Breuer and A. D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on logic simulation, the part on switch-level models
---

Switch-level simulation models a MOS circuit as a network of switches. Each transistor is a switch that is open or closed by the value on its gate. Each node holds a charge, and the value of a node comes from the strongest signals that reach it through closed switches. Node sizes and transistor strengths are small integers that order the signals: a supply beats any transistor path, a strong transistor beats a weak one, and any driven path beats a stored charge. With these discrete strengths the model handles what a gate-level model cannot: pass transistors, bidirectional switches, buses with several drivers, ratioed nMOS logic, charge storage and charge sharing. It needs no voltages and no equations. This page is in the logic simulation half of [logic and circuit simulation](/logic-simulation/): the values are 0, 1 and X, and the work is graph search, not numerical analysis. Its delay model is unit delay per [channel-connected component](/channel-connected-component/): in each round every component whose inputs changed goes to its new steady state, computed from the values of the round before. Within a component the response is instantaneous.

## In plain words

Think of the chip as wires joined by switches. A transistor closes or opens depending on the value at its gate. Power and ground push 1 and 0 into the wires through closed switches. A wire that is cut off from both keeps its last value, like a small bucket of charge.

When two pushes meet, the stronger one wins. A wide transistor pushes harder than a narrow one, and a big wire holds more charge than a small one. If two equal pushes disagree, the result is X, unknown.

The simulator splits the circuit into groups of wires joined by switch channels. It solves each group by itself, then wakes up the groups whose switches changed, and repeats until nothing changes.

## The problem

A switch network has input nodes and storage nodes. The input nodes are vdd (value 1), gnd (value 0) and the primary inputs. They have the strength $\omega$, larger than every other strength. Each storage node $n$ has a size $\kappa(n)$ and a stored value $v(n) \in \{0, 1, X\}$. Each transistor has a type (n or p), a gate node, two channel terminals and a strength $\gamma$. All sizes are smaller than all strengths. An n-type transistor is in state 1 (closed) when its gate is 1, a p-type one when its gate is 0, and in state X when its gate is X. Otherwise it is open.

A *signal* on a path through closed transistors has the strength of the weakest element on it: the source ($\omega$ for an input, $\kappa(m)$ for the charge of a storage node $m$) and every transistor. Let $S(n)$ be the largest strength of a signal that reaches $n$. A path to $n$ is *dominant* when, at every node $m$ that it reaches, its strength so far equals $S(m)$. A path that reaches a node with a stronger signal from elsewhere is blocked there. With every transistor in state 0 or 1, the steady-state value of $n$ is the least upper bound, in the order $0 \sqsubseteq X$, $1 \sqsubseteq X$, of the source values of the dominant paths to $n$. Two dominant paths with values 0 and 1 give X, as in a bus fight.

When some transistors are in state X, the exact steady-state value is the least upper bound over all ways to make each of them open or closed. That can take time exponential in the number of X transistors, so the simulator computes a sound approximation.

## The algorithm

The network is split once into channel-connected components: storage nodes joined through transistor channels, with the input nodes left out. A component reads the gates of its transistors and the input nodes on its edge, so it can be solved alone.

```pseudo id=main
SIMULATE(network, inputs, init)
L1  val ← init; set the inputs, vdd ← 1, gnd ← 0
L2  split the storage nodes into channel-connected components
L3  queue ← all components
L4  while queue is not empty               (one round, one unit of delay)
L5      for each component P in queue: new(P) ← STEADY(P, val)
L6      changed ← the nodes whose new value differs; val ← new
L7      queue ← the components with a changed node or a transistor gated by one
L8  return val

STEADY(P, val)
L9  for each transistor of P: state ← 1, 0 or X from the value at its gate
L10 S ← widest-path strengths from all sources, through transistors in state 1
L11 for b in {0, 1}
L12     reach_b ← widest paths from the sources of value b or X, through transistors in
        state 1 or X, keeping a signal at node m only if its strength is at least S(m)
L13 for each node n of P: value ← X if both reach_0 and reach_1 get to n, else the one that does
L14 return the values
```

Line L10 is a [widest-path](/widest-path/) search, run like [Dijkstra's algorithm](/dijkstra/) with the largest strength first: a node starts with its own size, or the strength of a closed transistor to an input node, and a transistor of strength $\gamma$ passes $\min(S(u), \gamma)$ from $u$ to its other side. The strengths $S$ use only the transistors that are certainly closed, so they are the *definite* strengths: no choice for the X transistors can make a node weaker. Line L12 runs the same search over the *potential* paths, which may use X transistors, but drops a signal at any node where it is weaker than the definite strength there. Such a signal is blocked in every choice for the X transistors. If no surviving signal of value 0 reaches $n$, no dominant path of value 0 reaches $n$ in any choice, so $n$ is 1. This is in the spirit of the definite and potential paths of MOSSIM II, though not a copy of its equations.

When all transistors are in state 0 or 1, the two kinds of path are the same, and the floor test of line L12 keeps exactly the dominant paths, so STEADY computes the steady state of the definition. Sources with value X take part in both searches and give X.

## Example

A precharged bus: node bus (size 2) is precharged to 1 through a p transistor gated by $\phi$, and two small nodes c1 and c2 (size 1, value 0) hang on it through n transistors gated by e. All transistors have strength 10. Take $\phi = 1$ (precharge off) and e = 1.

| step | bus | c1 | c2 |
| --- | --- | --- | --- |
| stored values | 1 | 0 | 0 |
| sizes | 2 | 1 | 1 |
| L10, strengths $S$ | 2 | $\min(2, 10) = 2$ | $\min(2, 10, 10) = 2$ |
| L12, value 1 from the charge of bus | 2 | 2 | 2 |
| L12, value 0 from c1 and c2 | dropped: $1 < S = 2$ | dropped | dropped |
| L13, new values | 1 | 1 | 1 |

The large node wins the charge sharing. With all three sizes equal, both searches reach every node and the result is X: the final voltage depends on the capacitances, and the model does not claim to know it.

For the CMOS NAND gate with inputs a and b, where the output out reaches gnd through n transistors in series with an internal node m between them, a = 1 and b = 0 give out = 1 through the p transistor of b, and m joins out through the closed n transistor of a, so m = 1 with strength 10. With a = 0 and b = X, out still gets 1: the definite strength of out is 10 through the p transistor of a, and every 0 signal (the small charges of out and m) is dropped at line L12. With a = 1 and b = X, out = X, which is correct, since b = 0 and b = 1 give different outputs.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following, all exactly.

1. The search of line L10 gives $S(n)$, the largest signal strength at $n$, and following its tree gives a dominant path to every node.
2. With every transistor in state 0 or 1, STEADY returns exactly the least upper bound of the source values of the dominant paths, which is the definition of the steady state.
3. STEADY is monotone: if every value in val is replaced by a value at least as high in the information order, every result goes up or stays. With 2, this gives soundness: each 0 or 1 that STEADY gives is the value for every binary completion of the X values on the gates, inputs and stored charges.
4. STEADY of a component reads only its own nodes, the gates of its transistors and the input nodes. A component that is not queued has none of these changed, so solving only the queued components gives the same rounds as solving all of them in every round. When the queue is empty, the values are a fixed point of one round. The rounds of SIMULATE from a three-valued start bound, round by round, the rounds from every binary completion of the start.

The tests compare STEADY on random networks with a brute force that lists every simple path and applies the definition, check soundness against all completions, check monotonicity and the bound on whole runs, and check hand-worked networks: CMOS inverter, NAND and NOR gates with their internal nodes, a ratioed nMOS inverter, a dynamic latch that keeps its charge, charge sharing by size, a bus fight, a blocked weak path, a latch of two inverters and a ring of three inverters that never settles.

## Complexity

A component with $n$ storage nodes and $t$ transistors costs three widest-path searches with a binary heap, $O((n + t) \log n)$. A round costs at most $O((N + T) \log N)$ for the whole network, and the run costs $O(R (N + T) \log N)$, where $R$ is the number of rounds. On a circuit without feedback, $R$ is at most one more than the number of components on the longest chain of gate connections. With feedback, the run may not settle at all, as in a ring oscillator, and the implementation stops after a fixed number of rounds. The space is $O(N + T)$.

These are proved bounds on the work per round. How much work the queue saves in practice is measured, not proved: on a chain of 20 inverters, settling from all X takes 59 component solves.

## Properties

- **Exact for binary transistor states.** With no X on any transistor gate, the result is the steady state of the definition.
- **Sound with X.** A node that gets 0 or 1 has that value for every completion of the X values. In the tests, 393 of 407 random component nodes got exactly the least upper bound over all completions; the others got X where a completion analysis gives a binary value.
- **X pessimism.** Take an n transistor and a p transistor in parallel from vdd to a node that stores 0, both gated by s. With s = 0 or s = 1, one of them conducts and the node is 1. With s = X, neither is definite, the stored 0 survives the floor test, and the result is X. The model treats the two transistors as independent, as ternary gate simulation treats the two branches of reconvergent fanout.
- **Bidirectional.** Signals flow either way through a transistor channel. No direction is assigned in advance.
- **Unit delay per component.** Delays inside a component are zero, so a race inside one component is not visible.

## Variants and improvements

- **MOSSIM II.** Bryant's simulator of 1984 uses the same sizes and strengths and solves each component by a relaxation over a discrete algebra with definite and potential strengths.
- **Symbolic and fault simulation.** COSMOS compiles each component into Boolean equations and simulates them as code, MOSSIM can run many faulty copies at once (FMOSSIM), and [symbolic trajectory evaluation](/symbolic-trajectory-evaluation/) runs the switch-level model over symbolic values.
- **Delays.** Switch-level timing simulators attach RC delays to the switches, as in [Elmore delay](/elmore-delay/) estimates on [RC trees](/rc-tree/), and move toward [timing simulation](/timing-simulation/).
- **Gate recognition.** A tool can recognize standard gates in the components and simulate them at gate level, keeping the switch model only for pass transistors and buses.

## When to use it

Use switch-level simulation to check a full-custom or transistor-level design, extracted from layout by [circuit extraction](/circuit-extraction/), when it uses pass transistors, dynamic nodes, precharged buses or ratioed logic that a gate model cannot express. It runs much faster than [timing simulation](/timing-simulation/) or a full circuit simulator, since it computes no voltages. Do not use it for analog behavior, timing margins or charge sharing whose result depends on exact capacitances; it gives X there.

## Pitfalls

- **Sizes not below strengths.** The model needs every node size below every transistor strength. Otherwise a charge could beat a driven path.
- **Reading X as a circuit fault.** An X can come from X pessimism, from equal fights that a real circuit would resolve by ratio, or from charge sharing between equal nodes. Check the cause before changing the design.
- **Forgetting the internal nodes.** Internal nodes of series stacks hold charge and take part in charge sharing. Leaving them out hides real bugs.
- **Treating oscillation as an error of the simulator.** A ring of inverters has no steady state. The rounds keep changing, and the limit on rounds stops the run.

## Implementations

## History

Randal Bryant presented MOSSIM at the Design Automation Conference in 1981. His 1984 paper in the IEEE Transactions on Computers gave the formal model with node sizes, transistor strengths and the steady-state response, and the algorithm of MOSSIM II. Switch-level simulators of this type were used in industry in the 1980s to check microprocessors at the transistor level. Bryant and his students later added compiled simulation (COSMOS) and symbolic simulation, which led to symbolic trajectory evaluation with Seger.

## References
