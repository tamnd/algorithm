---
tag: P7XCAZ
kind: algorithm
slug: swap-test
name: Swap test
aliases:
- Buhrman-Cleve-Watrous-de Wolf test
area: quantum/quantum-primitives
level: intro
summary: "A Hadamard gate on an ancilla, controlled swaps of two registers, and a second Hadamard gate. The ancilla reads 0 with probability (1 + |<psi|phi>|^2)/2, so repeated runs estimate the overlap."
model: quantum-circuit-model
complexity:
  vars: {n: the number of qubits of each state, e: the additive error epsilon of the overlap estimate, p: the failure probability delta}
  time: {gates: Θ(n), depth: Θ(n), copies: O(log(1/p)/e^2)}
  space: {qubits: 2n + 1, ancillas: 1}
properties: {deterministic: false, exact: false, quantum: true, destructive: true, one_sided: true}
history:
  year: 1997
  people: [Adriano Barenco, André Berthiaume, David Deutsch, Artur Ekert, Richard Jozsa, Chiara Macchiavello]
  note: Barenco, Berthiaume, Deutsch, Ekert, Jozsa and Macchiavello used the circuit in 1997 to project onto the symmetric subspace. Buhrman, Cleve, Watrous and de Wolf used it in 2001 for quantum fingerprinting, and their paper made it known as the swap test.
prereqs: [hadamard-gate, quantum-measurement, tensor-product]
see_also: [hadamard-test, fidelity, density-matrix, hoeffding-inequality, chernoff-bound, quantum-state-tomography, toffoli-gate, quantum-communication-complexity]
sources:
  - paper: doi:10.1103/PhysRevLett.87.167902
    title: Harry Buhrman, Richard Cleve, John Watrous and Ronald de Wolf, Quantum fingerprinting, Physical Review Letters 87(16), 167902, 2001
    locator: the swap test circuit, its acceptance probability and its use to compare two fingerprints (general locator)
  - paper: doi:10.1137/S0097539796302452
    title: Adriano Barenco, André Berthiaume, David Deutsch, Artur Ekert, Richard Jozsa and Chiara Macchiavello, Stabilization of quantum computations by symmetrization, SIAM Journal on Computing 26(5), 1997
    locator: pp. 1541 to 1557 (the projection onto the symmetric subspace with one ancilla and controlled swaps; general locator)
  - paper: doi:10.1103/PhysRevA.87.052330
    title: Juan Carlos García-Escartín and Pedro Chamorro-Posada, Swap test and Hong-Ou-Mandel effect are equivalent, Physical Review A 87, 052330, 2013
    locator: the destructive swap test without an ancilla, and its optical form at a beam splitter
---

The swap test is a small quantum circuit that compares two unknown [quantum states](/quantum-state/) $|\psi\rangle$ and $|\phi\rangle$ of $n$ qubits each. It uses one ancilla qubit, two [Hadamard gates](/hadamard-gate/) and $n$ controlled swaps. When the ancilla is [measured](/quantum-measurement/), it reads 0 with probability $\frac12(1 + |\langle\psi|\phi\rangle|^2)$. So equal states always give 0, orthogonal states give 0 or 1 with equal probability, and the frequency of 0 over many runs estimates the overlap $|\langle\psi|\phi\rangle|^2$. For [density matrices](/density-matrix/) $\rho$ and $\sigma$ the probability is $\frac12(1 + \operatorname{Tr}(\rho\sigma))$. The test needs no description of the states, only copies of them, and its cost does not depend on the dimension $2^n$ beyond the $n$ gates.

## In plain words

Two boxes each make a quantum state. You want to know how alike the two states are, but you cannot read a quantum state. The swap test puts one copy from each box side by side with one helper qubit. The helper first goes into an even blend of "swap" and "do not swap". In one branch the two states change places and in the other they stay. Then the helper is mixed again and measured.

If the two states are the same, swapping them changes nothing, so the two branches add up and the helper always reads 0. If the states are very different, the branches do not add up, and the helper reads 0 or 1 like a fair coin. In between, the helper reads 0 more often the more alike the states are. Repeat the test with fresh copies and count.

## The problem

**Input.** Copies of two unknown states of $n$ qubits: pure states $|\psi\rangle$ and $|\phi\rangle$, or density matrices $\rho$ and $\sigma$. An error $\varepsilon > 0$ and a failure probability $\delta$.

**Output.** One run returns a bit that is 0 with probability $\frac12(1 + |\langle\psi|\phi\rangle|^2)$. Many runs return an estimate $\hat x$ with $|\hat x - |\langle\psi|\phi\rangle|^2| < \varepsilon$ with probability at least $1 - \delta$. For mixed states, $\hat x$ estimates $\operatorname{Tr}(\rho\sigma)$. With pure states, $|\langle\psi|\phi\rangle|$ is the [fidelity](/fidelity/) of the two states, so the test also estimates the fidelity.

**Equality testing.** A second use is to decide whether $|\psi\rangle = |\phi\rangle$. Equal states pass every run, and states with $|\langle\psi|\phi\rangle|^2 \le 1 - \gamma$ fail one run with probability at least $\gamma/2$.

## The algorithm

Register $A$ holds $|\psi\rangle$ on qubits $0, \ldots, n-1$, register $B$ holds $|\phi\rangle$ on qubits $n, \ldots, 2n-1$, and the ancilla $c$ is qubit $2n$. Qubit 0 is the least significant bit of a basis index, as on the [quantum state](/quantum-state/) page.

```pseudo id=main
SWAP-TEST(|ψ⟩, |φ⟩)                     ▷ two states of n qubits each
L1  c ← |0⟩, A ← |ψ⟩, B ← |φ⟩
L2  apply H to c
L3  for j ← 0 to n - 1 do apply the swap of A_j and B_j, controlled by c
L4  apply H to c
L5  measure c and return the outcome

ESTIMATE-OVERLAP(ε, δ)                  ▷ uses N copies of |ψ⟩ and N copies of |φ⟩
L6  N ← ⌈2 ln(2/δ) / ε²⌉
L7  k ← the number of runs of SWAP-TEST, on N fresh pairs of copies, that return 0
L8  return max(0, 2k/N - 1)
```

The swaps of line L3 all have the same control, and together they exchange the whole register $A$ with the whole register $B$. A controlled swap of two qubits is the Fredkin gate. It is a [Toffoli gate](/toffoli-gate/) between two [CNOT gates](/cnot-gate/): CNOT from $B_j$ to $A_j$, Toffoli with controls $c$ and $A_j$ and target $B_j$, and CNOT from $B_j$ to $A_j$ again. Line L8 uses $2k/N - 1$ because $\Pr[0] = (1 + x)/2$ gives $x = 2\Pr[0] - 1$, and it replaces a negative value by 0 because the overlap is never negative.

## Example

Let $|\psi\rangle = |0\rangle$ and $|\phi\rangle = |+\rangle = (|0\rangle + |1\rangle)/\sqrt2$, so $n = 1$ and $|\langle\psi|\phi\rangle|^2 = \frac12$. We write the states as $|c\rangle|B\rangle|A\rangle$, with the ancilla first.

| after line | state |
| --- | --- |
| L1 | $\lvert 0\rangle\lvert +\rangle\lvert 0\rangle$ |
| L2 | $\frac{1}{\sqrt2}\bigl(\lvert 0\rangle\lvert +\rangle\lvert 0\rangle + \lvert 1\rangle\lvert +\rangle\lvert 0\rangle\bigr)$ |
| L3 | $\frac{1}{\sqrt2}\bigl(\lvert 0\rangle\lvert +\rangle\lvert 0\rangle + \lvert 1\rangle\lvert 0\rangle\lvert +\rangle\bigr)$ |
| L4 | $\frac12\lvert 0\rangle\bigl(\lvert +0\rangle + \lvert 0+\rangle\bigr) + \frac12\lvert 1\rangle\bigl(\lvert +0\rangle - \lvert 0+\rangle\bigr)$ |

In the computational basis $|+0\rangle + |0+\rangle = \frac{1}{\sqrt2}(2|00\rangle + |01\rangle + |10\rangle)$ and $|+0\rangle - |0+\rangle = \frac{1}{\sqrt2}(|10\rangle - |01\rangle)$. So line L5 returns 0 with probability $\frac14 \cdot \frac12(4 + 1 + 1) = \frac34$ and 1 with probability $\frac14 \cdot \frac12 \cdot 2 = \frac14$. This agrees with $\frac12(1 + \frac12) = \frac34$.

For the estimate, $\varepsilon = 0.1$ and $\delta = 0.01$ give $N = \lceil 2\ln 200/0.01 \rceil = 1060$ runs, and $\varepsilon = 0.05$ gives $N = 4239$. If 795 of 1060 runs return 0, the estimate is $2 \cdot 795/1060 - 1 = 0.5$.

For two copies of the maximally mixed qubit $I/2$, $\operatorname{Tr}(\rho\sigma) = \operatorname{Tr}(I/4) = \frac12$, so the test returns 0 with probability $\frac34$ as well. One run cannot tell this pair from the pair $|0\rangle, |+\rangle$.

## Correctness

The loop of line L3 is one swap $S$ of the two registers, controlled by $c$. For an input $|\chi\rangle$ of the two registers, the state after line L4 is $|0\rangle P_+|\chi\rangle + |1\rangle P_-|\chi\rangle$ with $P_\pm = \frac12(I \pm S)$, the projectors onto the symmetric and the antisymmetric subspaces. So outcome 0 has probability $\operatorname{Tr}(P_+(\rho\otimes\sigma)) = \frac12 + \frac12\operatorname{Tr}(S(\rho\otimes\sigma))$, and $\operatorname{Tr}(S(\rho\otimes\sigma)) = \operatorname{Tr}(\rho\sigma)$. For the estimate, the runs are independent, and the [Hoeffding inequality](/hoeffding-inequality/) bounds the error of the frequency of 0 by $\varepsilon/2$, except with probability $\delta$. The full proof is below.

## Complexity

- **Gates.** Two Hadamard gates and $n$ controlled swaps. A Toffoli gate takes 6 CNOT gates and a few one-qubit gates from $\{H, T, T^\dagger\}$, so each controlled swap takes 8 CNOT gates and $O(1)$ one-qubit gates. The circuit has $\Theta(n)$ gates from the Clifford plus $T$ set, exactly, with no approximation. All controlled swaps share the ancilla, so the depth is $\Theta(n)$ in this order. The depth falls to $O(\log n)$ if the control is first copied to $n - 1$ more ancillas by a tree of CNOT gates, and the copies are removed at the end.
- **Qubits.** $2n$ data qubits and one ancilla. The ancilla is measured, so it is not returned clean, and the data registers are changed by the measurement: after outcome 0 they are in the symmetric subspace.
- **Copies.** Each run uses one copy of each state. The estimate uses $N = \lceil 2\ln(2/\delta)/\varepsilon^2\rceil = O(\log(1/\delta)/\varepsilon^2)$ pairs, and the number does not depend on $n$.
- **A lower bound.** Order $1/\varepsilon^2$ copies are necessary for any method. Let $|\psi_\theta\rangle = \cos\theta|0\rangle + \sin\theta|1\rangle$ and $|\phi\rangle = |0\rangle$, so the overlap is $\cos^2\theta$. Near $\theta = \pi/4$, an overlap change of $\varepsilon$ is an angle change of about $\varepsilon$, and $N$ copies of the two states $|\psi_\theta\rangle$ have the inner product $\cos^N\varepsilon \approx e^{-N\varepsilon^2/2}$. Two states with an inner product close to 1 cannot be told apart reliably, so $N\varepsilon^2$ must be at least a constant.

## Properties

- **One-sided error for equality.** Equal pure states pass every run. Only unequal states can fail.
- **A run cannot fail often.** The probability of outcome 1 is $\frac12(1 - |\langle\psi|\phi\rangle|^2) \le \frac12$. So one run never decides equality with confidence, and $k$ runs miss a pair with overlap $1 - \gamma$ with probability $(1 - \gamma/2)^k$.
- **Symmetric and phase blind.** The result does not change when $|\psi\rangle$ and $|\phi\rangle$ change places, or when either one gets a global phase. The test sees $|\langle\psi|\phi\rangle|$, not the phase of $\langle\psi|\phi\rangle$.
- **Destructive.** The measurement changes both states, so every run needs fresh copies.
- **Dimension free.** The number of runs for error $\varepsilon$ is the same for all $n$. Only the gate count grows with $n$.

## Variants and improvements

- **Mixed states and purity.** For density matrices the test estimates $\operatorname{Tr}(\rho\sigma)$. With two copies of the same $\rho$, it estimates the purity $\operatorname{Tr}(\rho^2)$, which is 1 exactly for pure states (see [mixed state](/mixed-state/)).
- **Hadamard test with the swap.** The swap test is the [Hadamard test](/hadamard-test/) for the unitary $S$ on the state $\rho \otimes \sigma$, since $\operatorname{Tr}(S(\rho\otimes\sigma)) = \operatorname{Tr}(\rho\sigma)$ is the real number that the Hadamard test estimates.
- **Destructive swap test.** Measure each pair $A_j, B_j$ in the Bell basis, with a CNOT from $A_j$ to $B_j$ and then $H$ on $A_j$, and count the pairs that give the outcome 11, which is the singlet. An even count means "symmetric", with the same probability $\frac12(1 + \operatorname{Tr}(\rho\sigma))$. This needs no ancilla and no three-qubit gate. With photons, it is the Hong-Ou-Mandel effect at a beam splitter (García-Escartín and Chamorro-Posada, 2013).
- **Cyclic shift test.** With $k$ copies and a controlled cyclic shift of the $k$ registers in place of the swap, the same circuit estimates $\operatorname{Tr}(\rho^k)$, the moments of the spectrum.
- **With preparation circuits.** If unitaries $U_\psi$ and $U_\phi$ that prepare the states are given, [amplitude amplification](/amplitude-amplification/) in the form of amplitude estimation reduces the number of uses from order $1/\varepsilon^2$ to order $1/\varepsilon$.
- **Quantum fingerprinting.** Buhrman, Cleve, Watrous and de Wolf map each $m$-bit string to a state of $O(\log m)$ qubits so that different strings give states with a small inner product. Two parties send their fingerprints to a referee, who runs the swap test. This gives an exponential gap over classical simultaneous message protocols for equality in [quantum communication complexity](/quantum-communication-complexity/).

## When to use it

Use the swap test when the two states are available only as copies, for example as outputs of two devices or two circuits that you cannot invert, and you need their overlap, their pure-state fidelity, or the purity of a state. It costs $O(\log(1/\delta)/\varepsilon^2)$ copies for every $n$, while [quantum state tomography](/quantum-state-tomography/) of the two states costs a number of copies that grows as $4^n$. If the preparation circuits are known and can be inverted, apply $U_\phi^\dagger U_\psi$ to $|0\ldots0\rangle$ and measure all qubits: the outcome $0\ldots0$ has probability $|\langle\phi|\psi\rangle|^2$, with half the qubits and no controlled swaps. If classical descriptions of the states are known, compute the overlap directly.

## Pitfalls

- **Overlap, not amplitude.** The test estimates $|\langle\psi|\phi\rangle|^2$. To get the fidelity $|\langle\psi|\phi\rangle|$, take the square root, and note that the error grows near 0.
- **The factor 2.** An error $\varepsilon/2$ in the frequency of 0 is an error $\varepsilon$ in the overlap. A count of runs from a bound for the frequency alone is too small by a factor of 4.
- **Reused copies.** After a run the registers are projected onto the symmetric or antisymmetric subspace. A second run on the same registers does not give a fresh sample, and it biases the estimate towards 0.
- **Pairing of qubits.** Line L3 must swap qubit $j$ of $A$ with qubit $j$ of $B$ for each $j$. Any other pairing compares $|\psi\rangle$ with a permuted $|\phi\rangle$.
- **Mixed states.** For mixed states the result is $\operatorname{Tr}(\rho\sigma)$, which is not the fidelity. Two copies of $I/2$ give $\frac12$, the same as two pure states at overlap $\frac12$.

## Implementations

## History

Barenco, Berthiaume, Deutsch, Ekert, Jozsa and Macchiavello (1997) introduced the circuit as a way to project the state of several copies of a computation onto the symmetric subspace, which removes part of the errors. Buhrman, Cleve, Watrous and de Wolf (2001) used it to compare two quantum fingerprints, and since that paper it is known as the swap test. It is now a standard step in tests of state equality, in estimates of purity and overlap, and in quantum machine learning methods that compare encoded data. García-Escartín and Chamorro-Posada (2013) showed that the version without an ancilla is the Hong-Ou-Mandel effect.

## References
