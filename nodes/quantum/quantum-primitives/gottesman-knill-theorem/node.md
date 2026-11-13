---
tag: V5TKK8
kind: theorem
slug: gottesman-knill-theorem
name: Gottesman-Knill theorem
aliases:
- Gottesman-Knill theorem for Clifford circuits
area: quantum/quantum-primitives
level: advanced
summary: "A circuit of H, S and CNOT gates on a basis-state input, with computational-basis measurements, can be simulated exactly on a classical computer in polynomial time."
prereqs: [stabilizer-formalism, clifford-group]
see_also: [universal-gate-set, phase-and-t-gates, quantum-error-correction, steane-code, entanglement, bqp, logspace, linear-system-modulo-2]
sources:
  - url: https://arxiv.org/abs/quant-ph/9807006
    title: Daniel Gottesman, The Heisenberg representation of quantum computers, Group22, Proceedings of the XXII International Colloquium on Group Theoretical Methods in Physics, International Press, 1999, pages 32 to 43, arXiv:quant-ph/9807006
    locator: the theorem called Knill's theorem there, and the update rules for Clifford gates and Pauli measurements
  - paper: doi:10.1103/PhysRevA.70.052328
    title: Scott Aaronson and Daniel Gottesman, Improved simulation of stabilizer circuits, Physical Review A 70, 2004, article 052328, arXiv:quant-ph/0406196
    locator: the tableau algorithm with destabilizers (the CHP program) and the theorem that stabilizer circuit simulation is parity-L complete
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 10.5.4 (the Gottesman-Knill theorem), with Sections 10.5.1 to 10.5.3 for the stabilizer updates
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 20.3 (the Gottesman-Knill theorem), Section 20.4 (T gates and magic states) and Section 20.5 (simulation with few T gates)
  - paper: doi:10.1103/PhysRevA.71.022316
    title: Sergey Bravyi and Alexei Kitaev, Universal quantum computation with ideal Clifford gates and noisy ancillas, Physical Review A 71, 2005, article 022316
    locator: magic states make Clifford circuits universal
  - paper: doi:10.1103/PhysRevLett.116.250501
    title: Sergey Bravyi and David Gosset, Improved classical simulation of quantum circuits dominated by Clifford gates, Physical Review Letters 116, 2016, article 250501
    locator: the abstract and main theorems, times poly(n, m) + 2^(0.5t) t^3 for a probability and poly(n, m) + 2^(0.23t) t^3 w^3 for sampling
---

The *Gottesman-Knill theorem* says that a quantum circuit built only from [Clifford gates](/clifford-group/) (Hadamard, phase and CNOT), started on a computational basis state and measured in the computational basis, can be simulated exactly by a classical computer in polynomial time. The proof keeps the $n$ Pauli operators that fix the state ([stabilizer formalism](/stabilizer-formalism/)) in place of the $2^n$ amplitudes, and the Aaronson-Gottesman tableau updates them in $O(n)$ time per gate and $O(n^2)$ per measurement. The theorem is the reason that [entanglement](/entanglement/) alone does not make a quantum computer powerful: Clifford circuits make highly entangled states and still give no speedup. One non-Clifford gate, such as $T$, removes the theorem and gives a [universal gate set](/universal-gate-set/).

## Statement

**Theorem (Gottesman-Knill).** Consider a quantum circuit on $n$ qubits with these parts:

1. the input is a computational basis state $|x\rangle$ (more generally, any stabilizer state given by its generators);
2. the gates are $H$, $S$ and CNOT on any qubits, so every gate is in the [Clifford group](/clifford-group/); the Pauli gates are allowed, since $Z = S^2$ and $X = HZH$;
3. there are $m$ measurements, each of one qubit in the computational basis (more generally, of any Pauli string), at any point in the circuit;
4. the choice of later gates may depend on earlier outcomes (classical control).

Then a classical computer that is given the circuit can, for a circuit of $g$ gates:

- sample the outcomes with exactly the distribution of the quantum circuit, using one fair random bit for each random outcome, in $O(gn + mn^2)$ time and $O(n^2)$ bits of memory;
- compute the probability of any given sequence of outcomes exactly in the same time. Each probability is $0$ or $2^{-r}$, where $r$ is the number of outcomes in the sequence that are random.

The Pauli-string measurements of part 3 reduce to part 3 with one qubit, since a Clifford circuit maps any Pauli string to $Z_0$. The time bound is for the tableau with destabilizers of Aaronson and Gottesman; Gottesman's original method keeps only the stabilizer generators and uses $O(n^3)$ time per measurement for [Gaussian elimination modulo 2](/linear-system-modulo-2/).

## In plain words

A list of $n$ qubits normally needs $2^n$ numbers. But the states that these circuits make are special: each one is fixed by $n$ simple "check" operators, and each check is a string of $n$ letters. A gate changes each letter string by a simple rule, and a measurement either gives a known answer or a fair coin flip, which you can find from the strings. So you carry about $2n$ strings of $n$ letters, not $2^n$ numbers, and you can predict what the circuit will do. The theorem fails as soon as one gate is not of this special type.

## Proof

Write $\mathcal{P}_n$ for the Pauli group (see [Clifford group](/clifford-group/)). A *stabilizer state* is a state $|\psi\rangle$ with a set of $n$ Pauli operators $g_1, \ldots, g_n$ (each $\pm$ a Pauli string) that commute in pairs, that are independent (no product of a nonempty subset is $\pm I$), and that satisfy $g_i |\psi\rangle = |\psi\rangle$. The group $\mathcal{G} = \langle g_1, \ldots, g_n \rangle$ has $2^n$ elements and does not contain $-I$.

**Step 1: the generators fix the state.** Each $(I + g_i)/2$ is a projector of rank $2^{n-1}$, the projectors commute, and with independent generators their product $\Pi = \prod_i (I + g_i)/2 = 2^{-n} \sum_{g \in \mathcal{G}} g$ has trace $2^{-n} \cdot 2^n = 1$, since every $g \neq I$ in $\mathcal{G}$ is a traceless Pauli string up to sign. So $\Pi$ is a rank-one projector and $\Pi = |\psi\rangle\langle\psi|$. The list $g_1, \ldots, g_n$ fixes $|\psi\rangle$ up to a global phase. The input $|x\rangle$ has generators $(-1)^{x_j} Z_j$ for $j = 0, \ldots, n-1$.

**Step 2: gates.** If $g|\psi\rangle = |\psi\rangle$ then $(UgU^\dagger)(U|\psi\rangle) = U|\psi\rangle$. So $U|\psi\rangle$ has generators $U g_i U^\dagger$. For $U$ in the Clifford group these are again Pauli operators, they still commute and are still independent. The rules for $H$, $S$ and CNOT on page [Clifford group](/clifford-group/) compute each new generator in $O(1)$ word operations, so a gate costs $O(n)$ for the $n$ generators.

**Step 3: measurement with a random outcome.** Measure $Z_a$. Suppose some generator $g_p$ anticommutes with $Z_a$. Replace each other generator $g_i$ that anticommutes with $Z_a$ by $g_i g_p$; this keeps the group and makes $g_p$ the only generator that anticommutes with $Z_a$. Now $g_p (I + Z_a) g_p = I - Z_a$, and $g_p |\psi\rangle = |\psi\rangle$, so

$$\Pr[+1] = \langle\psi| \tfrac{I + Z_a}{2} |\psi\rangle = \langle\psi| g_p \tfrac{I + Z_a}{2} g_p |\psi\rangle = \langle\psi| \tfrac{I - Z_a}{2} |\psi\rangle = \Pr[-1],$$

and both are $1/2$. After outcome $(-1)^b$ the state $(I + (-1)^b Z_a)|\psi\rangle$, normalized, is fixed by $(-1)^b Z_a$ and by every $g_i$ with $i \neq p$, since these commute with $Z_a$. These $n$ operators are independent, so they are the new generators: replace $g_p$ by $(-1)^b Z_a$.

**Step 4: measurement with a fixed outcome.** Suppose $Z_a$ commutes with every generator. Then $Z_a$ commutes with all of $\mathcal{G}$, and $\mathcal{G}$ is a maximal commuting set of $2^n$ Pauli strings modulo signs, so $Z_a$ or $-Z_a$ is in $\mathcal{G}$. If $(-1)^b Z_a \in \mathcal{G}$ then $(-1)^b Z_a |\psi\rangle = |\psi\rangle$, so the outcome is $(-1)^b$ with probability $1$ and the state does not change. To find $b$, write $(-1)^b Z_a$ as a product of generators. Aaronson and Gottesman keep $n$ more Pauli strings $d_1, \ldots, d_n$, the *destabilizers*, such that $d_i$ anticommutes with $g_i$ and commutes with every other $g_j$ and every other $d_j$. Then $Z_a = \pm \prod_{i \in I} g_i$ where $I$ is the set of $i$ for which $d_i$ anticommutes with $Z_a$, and the sign of the product follows from at most $n$ multiplications of Pauli strings with signs, each of $O(n)$ time. So this case costs $O(n^2)$. The gates act on the destabilizers by the same rule as on the generators, and Step 3 replaces $d_p$ by the old $g_p$, which keeps the pairing.

**Step 5: the totals.** Steps 2 to 4 track the state exactly, up to a global phase, through every gate and measurement, so the simulator reproduces the outcome distribution of the circuit exactly. A random outcome is a fair coin, and a fixed outcome is computed. Classical control only chooses which step to apply next. The sums are $O(gn)$ for the gates and $O(mn^2)$ for the measurements, and the tableau has $2n$ rows of $2n + 1$ bits. For a given sequence of outcomes, follow the same steps with each random outcome forced to the given value; the probability is $0$ if a fixed outcome disagrees and $2^{-r}$ otherwise. $\blacksquare$

## Consequences

- **Entanglement is not enough.** Clifford circuits make [Bell states](/bell-states/), GHZ states and the code states of the [Steane code](/steane-code/) and other stabilizer codes, so highly entangled states, and the theorem simulates them in polynomial time. A quantum speedup needs gates outside the Clifford group.
- **Error correction is classically checkable.** Encoding, syndrome measurement and Pauli corrections of stabilizer codes are Clifford circuits with Pauli errors, so simulators of the Aaronson-Gottesman kind can run them on thousands of qubits; this is how threshold estimates under Pauli noise are computed (see [quantum error correction](/quantum-error-correction/) and [quantum threshold theorem](/quantum-threshold-theorem/)).
- **The power of the circuits is ⊕L.** Aaronson and Gottesman show that simulating a stabilizer circuit is complete for $\oplus\mathrm{L}$. This is the class of problems that a nondeterministic [logarithmic-space](/logspace/) machine solves when it accepts on an odd number of paths, and it contains the solution of a [linear system over GF(2)](/linear-system-modulo-2/). So, unless $\oplus\mathrm{L} = \mathrm{P}$, Clifford circuits are not even universal for classical polynomial-time computation, which the [Toffoli gate](/toffoli-gate/) alone gives.
- **The resources of fault tolerance.** In most fault-tolerant schemes the Clifford gates are the inexpensive gates, and the $T$ gate is the expensive one, made from *magic states* (Bravyi and Kitaev). The theorem says that the $T$ gates are where the quantum advantage lives.

## Tightness

Each hypothesis is needed.

- **The gate set.** Add the [T gate](/phase-and-t-gates/): $H$, $S$, CNOT and $T$ form a [universal gate set](/universal-gate-set/), so an efficient classical simulation of these circuits would put $\mathrm{BQP}$ inside $\mathrm{BPP}$ ([bqp](/bqp/), [bpp](/bpp/)), which is not expected. The [Toffoli gate](/toffoli-gate/) with $H$ is also universal.
- **The input.** With the product input $(|0\rangle + e^{i\pi/4}|1\rangle)/\sqrt 2$ on some qubits (a magic state), Clifford gates with measurement and classical control can apply $T$ by gate teleportation, so they become universal (Bravyi and Kitaev).
- **The measurements.** A measurement in a basis that is not a Pauli eigenbasis, such as the eigenbasis of $(X + Y)/\sqrt 2$, is a $T$ conjugate of a Pauli measurement and again gives universality.
- **Few T gates.** The cost grows only with the non-Clifford part. For a circuit with $t$ gates $T$ among $g$ gates, Bravyi and Gosset compute an output probability approximately in time $\mathrm{poly}(n, g) + 2^{0.5 t} t^3$, and sample $w$ output qubits in time $\mathrm{poly}(n, g) + 2^{0.23 t} t^3 w^3$. So the hard part of a quantum circuit can be measured by its $T$ count.
- **The bounds are tight up to the model.** The tableau must hold $\Theta(n^2)$ bits, since there are $2^{\Theta(n^2)}$ stabilizer states on $n$ qubits. A measurement in the worst case changes $\Theta(n)$ rows of $\Theta(n)$ bits each.

### Implementation

The file `impl/python/gottesman_knill_theorem.py` is a tableau simulator in the style of Aaronson and Gottesman. It keeps $n$ destabilizer rows, $n$ stabilizer rows and a scratch row as bit masks with sign bits, and applies $H$, $S$, CNOT and computational-basis measurements, with an optional forced outcome. The tests run random Clifford circuits of 1 to 4 qubits (seeds 7071 to 7073) next to the state-vector simulator `qsim.py`. After every step each stabilizer row fixes the state vector and the rows have the commutation pattern of a tableau. For every measurement the tableau's "fixed or fair coin" answer agrees with the state vector's probability, and the exact output distribution found by branching over the random outcomes equals the squared amplitudes. A 300-qubit GHZ circuit, beyond any state vector, gives equal outcomes on all qubits.

## History

Gottesman stated the theorem in his 1998 Group22 lecture "The Heisenberg representation of quantum computers" under the name "Knill's theorem", citing a private communication from Emanuel Knill, and based it on the stabilizer formalism of his 1997 thesis. Aaronson and Gottesman (2004) added the destabilizers, which bring a measurement from $O(n^3)$ to $O(n^2)$, wrote the CHP program, and proved $\oplus\mathrm{L}$ completeness. Bravyi and Kitaev (2005) showed that magic states restore universality, and Bravyi and Gosset (2016) gave simulations whose cost is exponential only in the number of $T$ gates.

## References
