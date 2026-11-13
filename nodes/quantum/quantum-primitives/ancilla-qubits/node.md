---
tag: HZ3JH4
kind: concept
slug: ancilla-qubits
name: Ancilla qubits
aliases:
- ancillas
- work qubits
- clean ancilla
- dirty ancilla
area: quantum/quantum-primitives
level: intro
summary: "Extra qubits that a circuit uses as workspace. A clean ancilla starts and ends in |0>. A dirty ancilla can be in any state, and the circuit must give that state back."
prereqs: [qubit, quantum-circuit-model, toffoli-gate]
see_also: [uncomputation, reversible-computation, quantum-oracle, phase-kickback, hadamard-test, partial-trace, quantum-error-correction, quantum-modular-exponentiation]
sources:
  - paper: doi:10.1103/PhysRevA.52.3457
    title: "Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin and Harald Weinfurter, Elementary gates for quantum computation, Physical Review A 52(5):3457-3467, 1995"
    locator: "Section 7: Lemma 7.2 (C^m X from 4(m - 2) Toffoli gates with m - 2 dirty ancillas) and Corollary 7.4 (one dirty ancilla, 8(n - 5) Toffoli gates on n wires)"
  - paper: doi:10.1109/TCAD.2003.811448
    title: "Vivek V. Shende, Aditya K. Prasad, Igor L. Markov and John P. Hayes, Synthesis of reversible logic circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 22(6):710-722, 2003"
    locator: circuits of NOT, CNOT and Toffoli gates on n >= 4 wires and no ancilla give exactly the even permutations
  - paper: doi:10.1147/rd.176.0525
    title: "Charles H. Bennett, Logical reversibility of computation, IBM Journal of Research and Development 17(6):525-532, 1973"
    locator: work tapes that are erased by running the computation backward, so they can be used again
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 4.3 (controlled operations with work qubits) and Section 4.4 (measurement and the principle of deferred measurement)"
  - paper: arxiv:quant-ph/0410184
    title: "Steven A. Cuccaro, Thomas G. Draper, Samuel A. Kutin and David Petrie Moulton, A new quantum ripple-carry addition circuit, 2004"
    locator: abstract (a linear-depth ripple-carry adder with a single ancillary qubit)
---

An *ancilla* is a qubit that a circuit uses as workspace and that is not part of its input or its output. A *clean* ancilla starts in $|0\rangle$ and must end in $|0\rangle$. A *dirty* (or *borrowed*) ancilla can start in any state, also one entangled with other qubits, and must end in that same state, so that it is free to use again and is not entangled with the result. Ancillas make circuits smaller: with $k - 2$ clean ancillas a $k$-controlled NOT gate takes $2k - 3$ [Toffoli gates](/toffoli-gate/), and some reversible maps cannot be built from Toffoli gates at all without one.

## In plain words

A circuit often needs scratch space, like the paper you use to do a long sum by hand. In a quantum circuit this scratch space is a set of extra qubits, the ancillas. They start blank, the circuit writes partial results on them, and then the circuit must erase those results again.

The erasing is not just tidiness. A scratch qubit that still holds a partial result is linked to the rest of the computation. Anyone who looks at the result alone sees noise, as if part of it were missing. So a good circuit cleans each ancilla before it gives the answer.

Sometimes a circuit can borrow a qubit that holds someone else's data. It may use it as scratch space only if it puts the data back exactly as it was.

## The idea

### Clean and dirty ancillas

Let $V$ be a unitary on $n$ qubits. A circuit $U$ on $n + a$ qubits *computes $V$ with $a$ clean ancillas* when

$$U\bigl(|\psi\rangle \otimes |0^a\rangle\bigr) = \bigl(V|\psi\rangle\bigr) \otimes |0^a\rangle \quad\text{for every state } |\psi\rangle.$$

Nothing is said about the action of $U$ when the ancillas do not start at $0$. The circuit $U$ *computes $V$ with $a$ dirty ancillas* when $U = V \otimes I$, that is

$$U\bigl(|\psi\rangle \otimes |\phi\rangle\bigr) = \bigl(V|\psi\rangle\bigr) \otimes |\phi\rangle \quad\text{for every } |\psi\rangle \text{ and every } |\phi\rangle.$$

By linearity the dirty form also holds when the ancillas are entangled with qubits outside the circuit. The dirty form is stronger. It lets a circuit borrow idle qubits of a larger computation, whatever they hold. For a classical reversible circuit, which permutes basis states, it is enough to check the condition on every basis state: the ancilla bits must come back with their start values, and the other bits must change as $V$ says.

### Why an ancilla must come back clean

Suppose a circuit ends in the state $\sum_x \alpha_x |r(x)\rangle|g(x)\rangle$, where $r(x)$ is the result and $g(x)$ is a value left on the ancillas. If $g$ is a constant $g_0$, the result register holds the pure state $\sum_x \alpha_x |r(x)\rangle$. If $g(x)$ depends on $x$, the ancillas are entangled with the result. The state of the result register alone is then the [partial trace](/partial-trace/) over the ancillas, a [mixed state](/mixed-state/). Terms with different $g(x)$ can no longer interfere, and a later step that needs [interference](/quantum-interference/) fails. The standard way to clean an ancilla is [uncomputation](/uncomputation/): run the part of the circuit that wrote on it backward.

### Why reversible circuits need ancillas

On $n$ wires, the NOT gate swaps $2^{n-1}$ pairs of basis states, the CNOT gate swaps $2^{n-2}$ pairs and the Toffoli gate swaps $2^{n-3}$ pairs. For $n \ge 4$ each of these numbers is even, so each gate is an even permutation, and so is every circuit made of them. The gate $C^{n-1}X$ on $n$ wires swaps only the two strings $1^{n-1}0$ and $1^n$. It is odd, so no circuit of NOT, CNOT and Toffoli gates on $n \ge 4$ wires computes it. Shende, Prasad, Markov and Hayes (2003) proved that on $n \ge 4$ wires these gates give exactly the even permutations. With one more wire, $C^{n-1}X \otimes I$ swaps $2$ pairs, so it is even, and the circuits below build it. Quantum gates do not have this limit: Barenco et al. (1995) build $C^{n-1}X$ on $n$ wires with no ancilla from $O(n^2)$ two-qubit gates.

### Multi-controlled NOT gates

The gate $C^kX$ flips the target $t$ when all $k$ controls $c_1, \ldots, c_k$ are $1$. Three circuits of Toffoli gates show how the kind of ancilla changes the cost.

- **The V-chain, $k - 2$ clean ancillas, $2k - 3$ Toffoli gates.** Write $a_1 = c_1c_2$, then $a_i = a_{i-1}c_{i+1}$ for $i = 2, \ldots, k-2$. Then $a_{k-2} = c_1 \cdots c_{k-1}$, so one Toffoli gate from $c_k$ and $a_{k-2}$ to $t$ flips $t$ when all controls are $1$. Then undo the $k - 2$ gates of the chain in reverse order. If an ancilla does not start at $0$, the result is wrong.
- **Dirty ancillas, $k - 2$ of them, $4(k - 2)$ Toffoli gates** (Barenco et al., Lemma 7.2). Let $T_i$ be the Toffoli gate onto $a_i$ from $c_{i+1}$ and $a_{i-1}$, with $T_1$ the gate onto $a_1$ from $c_1$ and $c_2$. Let $D$ be the sweep $T_{k-2} \cdots T_2\, T_1\, T_2 \cdots T_{k-2}$ of $2k - 5$ gates, and let $T_t$ be the Toffoli gate onto $t$ from $c_k$ and $a_{k-2}$. The circuit is $T_t\, D\, T_t\, D$. If $a_i$ starts with the value $\beta_i$, one sweep adds $c_1 \cdots c_{i+1}$ to each $a_i$. So the two copies of $T_t$ add $c_k\beta_{k-2}$ and $c_k(\beta_{k-2} \oplus c_1 \cdots c_{k-1})$ to $t$, which sum to $c_1 \cdots c_k$. The second sweep gives each $a_i$ its value $\beta_i$ back.
- **One dirty ancilla, $8(k - 3)$ Toffoli gates for $k \ge 5$** (Barenco et al., Corollary 7.4). Split the controls into a set $A$ of $\lceil k/2 \rceil$ controls and a set $B$ of the others. Apply $C^AX$ onto the ancilla $a$, then $C^{B \cup \{a\}}X$ onto $t$, then both again. The target gets $c_B\,\beta \oplus c_B(\beta \oplus c_A) = c_Ac_B$, and $a$ is flipped twice. Each of the four gates uses the wires it does not touch as dirty ancillas, so it can use the previous circuit.

So there is a trade: more ancillas give fewer gates, and clean ancillas give fewer gates than dirty ones.

### Ancillas and measurement

A measurement in the middle of a circuit, followed by a gate that depends on its outcome, gives the same statistics as a controlled gate followed by a measurement at the end. This is the *principle of deferred measurement* (Nielsen and Chuang, Section 4.4). If the circuit needs the measured qubit again as a fresh qubit, a new clean ancilla takes its place, so all measurements can move to the end at the cost of more qubits. In the same way, each general measurement and each [quantum channel](/quantum-channel/) is a unitary on the system and some ancillas, followed by discarding or measuring the ancillas. In this use the ancillas are not cleaned. They carry away the information that the measurement or the noise takes out.

## Examples

**The V-chain for $k = 3$.** Wires $c_1, c_2, c_3$, target $t$, one clean ancilla $a$. The circuit is three Toffoli gates: onto $a$ from $c_1, c_2$; onto $t$ from $c_3, a$; onto $a$ from $c_1, c_2$. On the input $c = 111$, $t = 0$, $a = 0$, the first gate sets $a = 1$, the second sets $t = 1$, and the third sets $a = 0$. On $c_1 = c_2 = 1$, $c_3 = 0$ the ancilla goes to $1$ and back, and $t$ does not change. This is $2k - 3 = 3$ gates.

**The same gate with a dirty ancilla.** Now $a$ starts with an unknown value $\beta$. The circuit of Lemma 7.2 is four Toffoli gates: onto $t$ from $c_3, a$; onto $a$ from $c_1, c_2$; onto $t$ from $c_3, a$; onto $a$ from $c_1, c_2$. The target gets $c_3\beta \oplus c_3(\beta \oplus c_1c_2) = c_1c_2c_3$, and $a$ ends at $\beta$. The V-chain fails here: with $c_3 = 1$, $c_1 = c_2 = 0$ and $\beta = 1$ its middle gate flips $t$. So a clean ancilla saves one gate in this case.

**A dirty ancilla that holds a quantum state.** Use the four-gate circuit above, and let the ancilla $a$ share the Bell state $\frac{1}{\sqrt2}(|00\rangle + |11\rangle)$ with a qubit $e$ outside the circuit. Take $c_1 = c_2 = c_3 = 1$ and $t = 0$. On the branch with $\beta = 0$ and on the branch with $\beta = 1$ the circuit sets $t = 1$ and gives $a$ its value back. By linearity the final state is $|111\rangle|1\rangle \otimes \frac{1}{\sqrt2}(|00\rangle + |11\rangle)$, so the entanglement of $a$ with $e$ is not touched.

**An ancilla left dirty.** Put the controls of the $k = 3$ V-chain in the state $|{+}{+}{+}\rangle$ and run only the first two gates. The state is $\frac{1}{\sqrt 8}\sum_c |c\rangle|t = c_1c_2c_3\rangle|a = c_1c_2\rangle$. The ancilla is $1$ on $2$ of the $8$ terms. Its two values split the controls and the target into two orthogonal pure states with weights $\frac34$ and $\frac14$, so the state of controls and target has purity $\mathrm{Tr}\,\rho^2 = \frac{9}{16} + \frac{1}{16} = \frac58$. After the third gate the purity is $1$.

## Where it is used

- **Oracles.** The bit form of a [quantum oracle](/quantum-oracle/) writes $f(x)$ into an output register, and its classical circuit uses work qubits that [uncomputation](/uncomputation/) cleans. [Phase kickback](/phase-kickback/) uses one ancilla in the state $|{-}\rangle$, which the oracle leaves unchanged.
- **Reversible arithmetic.** Adders and multipliers in [quantum modular exponentiation](/quantum-modular-exponentiation/) trade ancillas for gates. The adder of Cuccaro, Draper, Kutin and Moulton (2004) adds two $n$-bit numbers with one ancilla. Earlier reversible forms of the [ripple-carry adder](/ripple-carry-adder/) kept the carries on a number of ancillas that grows linearly with $n$. Dirty-ancilla circuits let an arithmetic step borrow qubits that hold other numbers.
- **Measuring a property of a state.** The [Hadamard test](/hadamard-test/), the [swap test](/swap-test/) and [quantum phase estimation](/quantum-phase-estimation/) use ancillas as control qubits and then measure them.
- **Error correction.** A code such as the [Shor code](/shor-code/) or the [Steane code](/steane-code/) measures its syndrome on ancillas, so that the data qubits are not measured; see [quantum error correction](/quantum-error-correction/).
- **Classical reversible computing.** Bennett (1973) used work tapes that the machine erases by running backward, and these are the clean ancillas of a [reversible computation](/reversible-computation/).

## References
