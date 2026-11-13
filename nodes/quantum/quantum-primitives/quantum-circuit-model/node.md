---
tag: 98B9XZ
kind: model
slug: quantum-circuit-model
name: Quantum circuit model
aliases:
- gate model
- quantum circuit
- quantum circuits
area: quantum/quantum-primitives
level: intro
summary: "A computation is a sequence of gates from a fixed finite set on qubits that start in |0...0>, then a measurement. An algorithm is a uniform family of circuits, one per input length."
prereqs: [qubit, quantum-gate, quantum-measurement, boolean-circuit]
see_also: [quantum-turing-machine, bqp, universal-gate-set, solovay-kitaev-theorem, circuit-complexity, quantum-query-model, quantum-threshold-theorem, gottesman-knill-theorem]
sources:
  - paper: doi:10.1098/rspa.1989.0099
    title: "David Deutsch, Quantum computational networks, Proceedings of the Royal Society of London A 425(1868):73-90, 1989"
    locator: "quantum gates connected by wires into networks, and a universal gate on three qubits (general locator)"
  - paper: doi:10.1109/SFCS.1993.366852
    title: "Andrew Chi-Chih Yao, Quantum circuit complexity, Proceedings of the 34th Annual IEEE Symposium on Foundations of Computer Science, pages 352-361, 1993"
    locator: the polynomial equivalence of quantum Turing machines and uniformly generated families of quantum circuits
  - paper: doi:10.1103/PhysRevA.52.3457
    title: "Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin and Harald Weinfurter, Elementary gates for quantum computation, Physical Review A 52(5):3457-3467, 1995"
    locator: the CNOT gate and all one-qubit gates are exactly universal
  - paper: doi:10.1145/276698.276708
    title: "Dorit Aharonov, Alexei Kitaev and Noam Nisan, Quantum circuits with mixed states, Proceedings of the 30th Annual ACM Symposium on Theory of Computing, pages 20-30, 1998"
    locator: "circuits of general quantum operations, and their simulation by unitary circuits with ancillas (general locator)"
  - paper: arxiv:0804.3401
    title: John Watrous, Quantum computational complexity, Encyclopedia of Complexity and Systems Science, Springer, 2009
    locator: "Sections III.1 to III.3 (general and unitary circuits, the universality theorem, unitary purification), Section IV.1 (Definition 2, polynomial-time generated families, and BQP), Section IV.3 (BPP ⊆ BQP) and Section IV.5 (BQP ⊆ PP and PP^BQP = PP)"
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Section 2.1.2 (quantum circuits), Section 2.2 (universal gate sets), Section 13.1 (most functions need exponentially many gates) and Section 13.3 (BQP ⊆ PSPACE)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 4.4 (the principle of deferred measurement), Section 4.5 (universal quantum gates) and Section 4.6 (summary of the quantum circuit model of computation)"
---

The *quantum circuit model* describes a quantum computation as a sequence of [quantum gates](/quantum-gate/) from a fixed finite set, each acting on one, two or three of $n$ [qubits](/qubit/) that start in $|0 \cdots 0\rangle$, followed by a [measurement](/quantum-measurement/) in the computational basis. As for a [Boolean circuit](/boolean-circuit/), one circuit handles one input length, so an algorithm is a *uniform* family of circuits $\{C_n\}$ that a classical polynomial-time machine can write down. The costs are the number of gates, the depth and the number of qubits, and [BQP](/bqp/) is defined in this model. Yao (1993) showed that it is equivalent to the [quantum Turing machine](/quantum-turing-machine/) up to polynomial overhead.

## The machine

**Wires and gates.** A circuit has $n$ wires, one per qubit, numbered $0$ to $n - 1$ as on the [quantum state](/quantum-state/) page: qubit $0$ is the least significant bit. The input $x$ is the initial basis state $|x\rangle|0^a\rangle$, with $a$ [ancilla qubits](/ancilla-qubits/) in $|0\rangle$. Each gate is a [unitary](/unitary-operator/) $G$ from a fixed gate set $\mathcal G$, applied to $k \le 3$ chosen wires and acting as the identity on the others. A circuit $G_1, \ldots, G_T$ applies the unitary $C = G_T \cdots G_1$, so the first gate is the rightmost factor.

**The output.** At the end some qubits are measured in the computational basis, and the outcome is a sample from the [Born rule](/born-rule/) distribution. For a decision problem one output qubit is measured, and the circuit accepts $x$ if it reads $1$.

**Gate sets.** An exact gate set such as the [CNOT gate](/cnot-gate/) together with all one-qubit gates writes every unitary exactly (Barenco et al., 1995). A finite set such as $\{H, T, \mathrm{CNOT}\}$ ([Hadamard](/hadamard-gate/), [T](/phase-and-t-gates/) and CNOT) writes every unitary only approximately, and a cost stated in it must say so. The [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) turns each exact one- or two-qubit gate into $O(\log^c(1/\varepsilon))$ gates of the finite set, with error $\varepsilon$ in operator norm and a small constant $c$; see the [universal gate set](/universal-gate-set/) page.

**Intermediate measurements.** A circuit may also measure in the middle and choose later gates from the result. The *principle of deferred measurement* says that this adds no power: replace each classically controlled gate by the same gate controlled by the qubit, and move all measurements to the end (Nielsen and Chuang, Section 4.4). Circuits of general quantum operations, with fresh ancillas and discarded qubits, are equivalent to unitary circuits with extra ancillas whose output is ignored (Aharonov, Kitaev and Nisan, 1998).

**Uniformity.** A family $\{C_n\}$ is *polynomial-time uniform* if a deterministic Turing machine outputs a description of $C_n$ in time polynomial in $n$. Then a language $L$ is in BQP if a uniform family of circuits of size polynomial in $n$ accepts every $x \in L$ with probability at least $\frac23$ and every $x \notin L$ with probability at most $\frac13$. Running the circuit $k$ times and taking the majority makes the error $e^{-\Omega(k)}$ by the [Chernoff bound](/chernoff-bound/), so the constants $\frac23$ and $\frac13$ do not matter.

**Example: a Bell pair.** On two qubits, apply $H$ to qubit $1$ and then CNOT with control $1$ and target $0$. From $|00\rangle$ the first gate gives $\frac{1}{\sqrt2}(|00\rangle + |10\rangle)$, and the second gives $\frac{1}{\sqrt2}(|00\rangle + |11\rangle)$. The circuit has size $2$, depth $2$ and width $2$, and the two outcomes $00$ and $11$ each have probability $\frac12$.

## What it counts

- **Size**: the number of gates from the stated set. A count of exact gates and a count of Clifford plus T gates after Solovay-Kitaev differ by a factor polylogarithmic in $1/\varepsilon$.
- **Depth**: the number of layers, where the gates in one layer act on disjoint qubits. The Bell circuit has depth $2$, because its CNOT uses the qubit that the $H$ gate acts on.
- **Width**: the number of qubits, with data qubits and ancillas counted apart, and with a note on whether the ancillas are returned to $|0\rangle$.
- **Special counts**: the number of two-qubit gates, or the number of T gates, which dominates the cost in fault-tolerant schemes because Clifford gates are cheap there.
- **Queries**: in circuits with [oracle](/quantum-oracle/) gates, the number of oracle gates, which is the cost in the [quantum query model](/quantum-query-model/).
- **Error**: the success probability of the output, and the distance of the circuit from the ideal one. Errors of gates add: for unitaries, $\|U_2U_1 - V_2V_1\| \le \|U_2 - V_2\| + \|U_1 - V_1\|$, because $U_2U_1 - V_2V_1 = U_2(U_1 - V_1) + (U_2 - V_2)V_1$. So $T$ gates, each within $\varepsilon$, give a circuit within $T\varepsilon$.

## Relation to other models

- **Boolean circuits.** A [reversible](/reversible-computation/) Boolean circuit of NOT, CNOT and [Toffoli](/toffoli-gate/) gates is a quantum circuit whose matrices are permutations. A Boolean circuit of size $s$ becomes a reversible circuit of size $O(s)$ with $O(s)$ ancillas, which are cleaned by [uncomputation](/uncomputation/). With $H$ on fresh qubits as a source of fair coins, this gives $\mathrm{BPP} \subseteq \mathrm{BQP}$ (Watrous, Section IV.3).
- **Quantum Turing machines.** Yao (1993) showed that $t$ steps of a quantum Turing machine are simulated by a uniform family of circuits of size $O(t^2)$, and that a quantum Turing machine simulates a uniform family in polynomial time. So both models define the same BQP. Molina and Watrous (2019) gave circuits of depth $O(t)$ for the first direction.
- **Probabilistic computation.** A randomized circuit applies stochastic matrices to a probability vector; a quantum circuit applies unitary matrices to an amplitude vector. The difference is [interference](/quantum-interference/).
- **Nonuniform families.** Without uniformity a family can hide a hard answer in the choice of $C_n$, as a Boolean family of polynomial size can for [P/poly](/p-poly/). Such families define BQP/poly and not BQP.
- **Circuit complexity.** Size and depth here are the quantum analogues of the measures of [circuit complexity](/circuit-complexity/), and the same counting arguments apply.

## Known results in the model

- **Universality.** The CNOT gate and all one-qubit gates are exactly universal (Barenco et al., 1995). Finite sets such as $\{H, T, \mathrm{CNOT}\}$ approximate every unitary to any accuracy, and the choice of a universal set with efficiently computable entries changes sizes only by polylogarithmic factors.
- **Counting lower bound.** A circuit of $T$ gates from a finite set has at most $(|\mathcal G| \cdot n^3)^T$ choices, so most Boolean functions on $n$ bits need quantum circuits of size exponential in $n$ (de Wolf, Section 13.1).
- **Upper bounds on BQP.** $\mathrm{BPP} \subseteq \mathrm{BQP} \subseteq \mathrm{PP} \subseteq \mathrm{PSPACE}$. The last quantum step uses the sum over paths of [quantum interference](/quantum-interference/). Fortnow and Rogers showed $\mathrm{PP}^{\mathrm{BQP}} = \mathrm{PP}$ (Watrous, Section IV.5).
- **Factoring.** Factoring and discrete logarithms are in BQP ([factoring in BQP](/factoring-in-bqp/)), while no polynomial-time classical algorithm is known.
- **Clifford circuits.** Circuits of $H$, $S$ and CNOT on basis inputs with computational-basis measurements are simulated classically in polynomial time ([Gottesman-Knill theorem](/gottesman-knill-theorem/)). Adding the gate $T$ makes the set universal.
- **Noise.** If each gate fails with probability below a constant threshold, with local and weakly correlated noise, fast classical processing and fresh ancillas, a circuit of size $T$ is simulated with polylogarithmic overhead by an encoded circuit ([threshold theorem](/quantum-threshold-theorem/)).

### Pitfalls

- **Arbitrary gates hide power.** A gate set with a rotation angle that encodes an uncomputable number lets a family answer undecidable questions. The gate set must be finite, or its entries efficiently computable.
- **The order of the matrix product.** The circuit $G_1$ then $G_2$ is the matrix $G_2G_1$. Writing $G_1G_2$ gives a different unitary when the gates do not commute.
- **Ancillas count.** A bound in gates says nothing about width. A circuit with a garbage register that is never cleaned is a different circuit from one that returns its ancillas to $|0\rangle$, and only the second can be used inside an interference step.

## References
