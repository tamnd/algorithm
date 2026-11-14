---
tag: EMH87K
kind: problem
slug: qubit-mapping
name: Qubit mapping
aliases:
- qubit routing
- quantum layout synthesis
- qubit allocation
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Put the logical qubits of a circuit on the physical qubits of a device and add SWAP gates so every two-qubit gate acts on coupled qubits, with few SWAPs.
prereqs: [quantum-circuit-model, cnot-gate, subgraph-isomorphism]
see_also: [sabre-qubit-mapping, a-star-search, sorting-by-adjacent-swaps, permutation-routing, np-complete, universal-gate-set, reversible-logic-synthesis, fermion-to-qubit-mapping]
sources:
  - paper: doi:10.1145/3168822
    title: "Marcos Yukio Siraichi, Vinícius Fernandes dos Santos, Sylvain Collange and Fernando Magno Quintão Pereira, Qubit allocation, Proceedings of the 2018 International Symposium on Code Generation and Optimization (CGO 2018), pages 113 to 125"
    locator: Definition 2.2 (coupling graph), Definition 2.4 (Qubit Assignment), Theorem 3.1 (Qubit Assignment is NP-complete, by a reduction from subgraph isomorphism), Definitions 3.2 and 3.3 (Swap Minimization and Qubit Allocation), Section 4.1 (an exact dynamic program)
  - paper: doi:10.1609/socs.v9i1.18463
    title: "Adi Botea, Akihiro Kishimoto and Radu Marinescu, On the complexity of quantum circuit compilation, Proceedings of the 11th International Symposium on Combinatorial Search (SoCS 2018), pages 138 to 142"
    locator: Theorem 1 (the makespan version of compilation with SWAPs is NP-complete)
  - paper: doi:10.4230/LIPIcs.ESA.2016.66
    title: "Tillmann Miltzow, Lothar Narins, Yoshio Okamoto, Günter Rote, Antonis Thomas and Takeaki Uno, Approximation and hardness of token swapping, Proceedings of the 24th European Symposium on Algorithms (ESA 2016), LIPIcs 57, article 66"
    locator: token swapping is NP-complete and APX-hard, and has a polynomial-time 4-approximation (general locator)
  - paper: doi:10.1109/TCAD.2018.2846658
    title: "Alwin Zulehner, Alexandru Paler and Robert Wille, An efficient methodology for mapping quantum circuits to the IBM QX architectures, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 38(7), 2019, pages 1226 to 1236"
    locator: the division of the circuit into layers and the A* search for the SWAPs of each layer (general locator)
  - paper: doi:10.1145/3297858.3304023
    title: "Gushu Li, Yufei Ding and Yuan Xie, Tackling the qubit mapping problem for NISQ-era quantum devices, Proceedings of ASPLOS 2019, pages 1001 to 1014"
    locator: Section III.A (the problem, the coupling graph and the SWAP as three CNOTs, Figure 3)
  - paper: doi:10.1145/3316781.3317859
    title: "Robert Wille, Lukas Burgholzer and Alwin Zulehner, Mapping quantum circuits to IBM QX architectures using the minimal number of SWAP and H operations, Proceedings of the 56th Design Automation Conference (DAC 2019)"
    locator: the exact mapping by a reduction to satisfiability (general locator)
  - paper: doi:10.1145/3400302.3415620
    title: "Bochen Tan and Jason Cong, Optimal layout synthesis for quantum computing, Proceedings of the 39th International Conference on Computer-Aided Design (ICCAD 2020)"
    locator: OLSQ, the exact layout synthesis by satisfiability modulo theories for depth or SWAP count (general locator)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A, problem [GT48] Subgraph Isomorphism
---

Qubit mapping is the step of a quantum compiler that fits a circuit onto real hardware. A device has a fixed set of physical qubits, and a two-qubit gate such as a [CNOT](/cnot-gate/) works only between pairs that the hardware couples. The coupled pairs form the *coupling graph*. A circuit in the [circuit model](/quantum-circuit-model/) uses logical qubits and may apply a two-qubit gate to any pair. Qubit mapping picks an initial place for each logical qubit and inserts SWAP gates, which exchange the states of two coupled physical qubits, so that every two-qubit gate of the circuit acts on a coupled pair when it runs. Each SWAP is three CNOTs and adds error and time, so the goal is few SWAPs, or a low depth, or a high expected fidelity. The problem is NP-complete even in its simplest form.

## In plain words

Think of people at a long table where each person can only talk to the people next to them. A script says which pairs must talk, in order. First you choose the seating. When the script needs two people who are not next to each other, you make neighbors exchange seats until they are. You want a seating and a series of exchanges that follow the script with as few exchanges as you can.

The people are the logical qubits, the seats are the physical qubits, the table is the coupling graph, and an exchange is a SWAP gate. At the end, people may sit in other seats than at the start, which is fine: you only have to remember who sits where when you read the results.

## Definition

**Input.** A circuit $C$ on $n$ logical qubits: a sequence of gates, each on one or two qubits (larger gates are first decomposed). A connected coupling graph $G = (Q, E)$ with $N = |Q| \ge n$ physical qubits.

**Output.** An initial *mapping*, an injective map $\pi_0$ from logical to physical qubits, and a new circuit $C'$ on the physical qubits. $C'$ holds every gate of $C$ and some SWAP gates, each SWAP on an edge of $G$. Each SWAP on $\{p, q\}$ changes the current mapping by exchanging the logical qubits (if any) at $p$ and $q$. A gate of $C$ on logical qubits $a$ and $b$ is placed in $C'$ on the physical qubits $\pi(a)$ and $\pi(b)$, where $\pi$ is the mapping at that point of $C'$. The output is *valid* if:

1. every two-qubit gate of $C'$, the SWAPs included, acts on an edge of $G$, and
2. the gates of $C$ appear in an order that respects their dependences: two gates that share a qubit keep their order in $C$.

Then $C'$ computes the same operation as $C$, up to the relabeling of the qubits by $\pi_0$ at the input and by the final mapping $\pi_f$ at the output. The final permutation costs nothing: the program reads each logical qubit from the physical qubit where it ends.

**Objective.** The usual cost is the number of SWAPs, or the number of added CNOTs, which is 3 per SWAP. Other costs are the depth of $C'$, or the product of the success rates of its gates on a device whose couplings have different error rates.

**Decision versions.** *Qubit Assignment* (Siraichi et al., Definition 2.4) asks if there is a mapping that needs no SWAP at all. *Swap Minimization* (Definition 3.2) asks if a valid output exists with at most $K$ SWAPs.

**SWAP.** The SWAP gate on qubits $p$ and $q$ maps $|x, y\rangle$ to $|y, x\rangle$. It equals three CNOTs, with the middle one reversed: $\mathrm{CNOT}_{pq} \mathrm{CNOT}_{qp} \mathrm{CNOT}_{pq}$, the same three XORs as the [XOR swap](/xor-swap/). The CNOT page proves it. No device has to support SWAP as a native gate.

## Variants

- **Routing with a fixed layout.** The initial mapping is given, and only the SWAPs are chosen. Changing one given mapping into another with the fewest SWAPs is *token swapping* on $G$.
- **Directed coupling.** On some early devices, a CNOT works on a coupled pair in one direction only. The other direction costs four extra Hadamard gates, and the cost counts them, as in Wille, Burgholzer and Zulehner (DAC 2019).
- **Depth and time.** The cost is the depth of $C'$, since SWAPs on disjoint pairs run at the same time, or the makespan with gate times, as in Botea, Kishimoto and Marinescu (2018).
- **Noise-aware.** Each coupling and each qubit has an error rate, and the cost is the expected fidelity, which favors good qubits for the initial mapping.
- **Other moves.** Some methods also use bridge gates, which do a CNOT across a distance of two with four CNOTs and no change of mapping, or change the order of commuting gates. Trapped-ion and neutral-atom devices move the qubits themselves instead of using SWAPs.
- **Sub-steps.** Many tools split the problem into *layout*, the choice of $\pi_0$, and *routing*, the choice of SWAPs. The name "qubit allocation" is used for the whole problem and also for the layout step alone.

This problem is not [fermion-to-qubit mapping](/fermion-to-qubit-mapping/), which encodes the fermionic modes of a physics problem into qubit operators and has nothing to do with the hardware coupling.

## Examples

**A triangle on a line.** Take three logical qubits $a, b, c$ and the circuit $\mathrm{CNOT}(a, b)$, $\mathrm{CNOT}(b, c)$, $\mathrm{CNOT}(a, c)$. The device is a line $q_0 - q_1 - q_2$.

The three gates use all three pairs of logical qubits, a triangle, and a line has no triangle, so no mapping makes all three pairs adjacent: at least one SWAP is needed. One suffices. Map $a \to q_0$, $b \to q_1$, $c \to q_2$. The first two gates act on $(q_0, q_1)$ and $(q_1, q_2)$, both edges. Then SWAP $(q_0, q_1)$, which puts $a$ on $q_1$ and $b$ on $q_0$, and the last gate acts on $(q_1, q_2)$. The output has 4 two-qubit gates, 6 CNOTs after the SWAP is expanded, and the final mapping is $b \to q_0$, $a \to q_1$, $c \to q_2$.

**A permutation on a line.** If the layout is fixed and a step must put the logical qubits on a line in the reverse order, then the fewest SWAPs is the number of inversions, $n(n-1)/2$, because a SWAP on a line is an adjacent transposition: this is [sorting by adjacent swaps](/sorting-by-adjacent-swaps/).

## Known algorithms

- **Exact.** Siraichi et al. (2018) give a dynamic program over mappings, exponential in $N$. Wille, Burgholzer and Zulehner (DAC 2019) find the minimal number of SWAP and H gates by satisfiability, and OLSQ (Tan and Cong, ICCAD 2020) finds an optimal depth or SWAP count by satisfiability modulo theories. These handle small devices and short circuits only.
- **Search per layer.** Zulehner, Paler and Wille (TCAD 2019) split the circuit into layers of gates on disjoint qubits and use [A* search](/a-star-search/) to find the SWAPs that make one layer executable. The result is optimal for each layer, not for the whole circuit.
- **Heuristic search.** [SABRE](/sabre-qubit-mapping/) (Li, Ding and Xie, ASPLOS 2019) chooses one SWAP at a time by a cost over the front layer of gates and a lookahead, and finds the initial mapping by forward and backward passes. It is fast enough for large circuits, and the SabreLayout and SabreSwap passes of Qiskit are based on it.
- **Token swapping.** When the goal mapping of a step is known, a token swapping algorithm finds the SWAPs; on a line this is bubble sort, and on any graph there is a 4-approximation (Miltzow et al., 2016).

## Bounds

**Hardness.** Qubit Assignment is NP-complete (Siraichi et al., Theorem 3.1). Swap Minimization, with the initial mapping free, is NP-complete too, since its case $K = 0$ is Qubit Assignment; both are proved below. The makespan version is NP-complete (Botea, Kishimoto and Marinescu, Theorem 1). With the mapping fixed, a step that must reach a given mapping is token swapping, which is NP-complete and APX-hard (Miltzow et al., 2016).

**Upper bound.** Let $g$ be the number of two-qubit gates. Before each such gate, move one of its qubits along a shortest path of $G$ toward the other. That takes $d - 1$ SWAPs for distance $d$, at most $\mathrm{diam}(G) - 1 \le N - 2$. So $g(N - 2)$ SWAPs always suffice, and the optimum is polynomial in the input.

**Lower bound.** If the *interaction graph*, the graph of the pairs of logical qubits that share a gate, is not a subgraph of $G$, at least one SWAP is needed. Stronger lower bounds come only from exact methods.

## Reductions

**From subgraph isomorphism (Siraichi et al., Theorem 3.1).** [Subgraph isomorphism](/subgraph-isomorphism/) ([GT48] in Garey and Johnson) asks if a graph $H$ is isomorphic to a subgraph of a graph $G$, that is, if there is an injective map $f : V(H) \to V(G)$ with $\{f(u), f(v)\} \in E(G)$ for every edge $\{u, v\}$ of $H$. It is NP-complete. Given $H$ and $G$ with $|V(H)| \le |V(G)|$ (otherwise the answer is no), make one logical qubit for each vertex of $H$, a circuit with one CNOT on $u, v$ for each edge of $H$ in any order, and the coupling graph $G$. A mapping needs no SWAP exactly when every CNOT acts on an edge of $G$, which is exactly a map $f$ as above. So Qubit Assignment answers yes if and only if $H$ is a subgraph of $G$, and the construction is linear. Qubit Assignment is in NP, since a mapping is a certificate checked in linear time. So it is NP-complete. Siraichi et al. state it for a directed coupling graph; the undirected case above is the same with each edge taken in both directions.

**Swap Minimization.** The case $K = 0$ is Qubit Assignment, so Swap Minimization is NP-hard. It is in NP: by the upper bound, an optimal output has at most $g(N-2)$ SWAPs, so for $K$ above that the answer is yes and for smaller $K$ the output is a certificate of polynomial size, checked by replaying the mapping. So it is NP-complete.

**To satisfiability and integer programming.** The exact methods encode the mapping at each step as Boolean or integer variables, with constraints for adjacency and for the change made by each SWAP, and give the encoding to a solver.

## Applications

Every program that runs on superconducting hardware with a sparse coupling graph, such as a heavy-hexagon or square grid, goes through qubit mapping in its compiler, and the added SWAPs are often the largest share of the two-qubit gates of the compiled circuit. Since a two-qubit gate on such devices fails with a probability of the order of 0.1% to 1%, the number of SWAPs decides whether a circuit gives a useful result. The same problem appears, with other moves, for trapped ions and neutral atoms, and in the design of new devices, where the coupling graph is chosen to make mapping cheap for the expected circuits.

## References
