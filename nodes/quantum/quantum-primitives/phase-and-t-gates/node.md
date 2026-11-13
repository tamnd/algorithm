---
tag: XQY3VF
kind: definition
slug: phase-and-t-gates
name: Phase and T gates
aliases:
- S gate
- T gate
- pi/8 gate
area: quantum/quantum-primitives
level: intro
summary: "The phase gate S = diag(1, i) and the T gate T = diag(1, e^(i pi/4)), with T^2 = S and S^2 = Z. S is a Clifford gate; T is not, and Clifford gates with T are universal."
prereqs: [pauli-gates, hadamard-gate]
see_also: [clifford-group, universal-gate-set, solovay-kitaev-theorem, gottesman-knill-theorem, quantum-threshold-theorem, quantum-fourier-transform, phase-kickback, bloch-sphere]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.2 (single qubit operations, the phase and pi/8 gates) and Section 4.5.3 (a discrete set of universal operations)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.4 (elementary gates, the phase gate R_phi)
  - paper: doi:10.1016/S0020-0190(00)00084-3
    title: P. Oscar Boykin, Tal Mor, Matthew Pulver, Vwani Roychowdhury and Farrokh Vatan, A new universal and fault-tolerant quantum basis, Information Processing Letters 75(3), 2000, pages 101 to 107
    locator: the basis of H, CNOT and T
---

The *phase gates* are the one-qubit gates $R_\varphi = \operatorname{diag}(1, e^{i\varphi})$, which leave $|0\rangle$ unchanged and multiply $|1\rangle$ by the phase $e^{i\varphi}$. Two of them have their own names: the *phase gate* $S = R_{\pi/2} = \operatorname{diag}(1, i)$ and the *T gate* $T = R_{\pi/4} = \operatorname{diag}(1, e^{i\pi/4})$, with $T^2 = S$ and $S^2 = Z$. $S$ is a Clifford gate. $T$ is not, and the Clifford gates together with $T$ are a universal gate set, which makes $T$ the standard non-Clifford gate of fault-tolerant quantum computing.

## Definition

For a real number $\varphi$, the **phase gate** $R_\varphi$ is the [quantum gate](/quantum-gate/) on one qubit with the matrix

$$R_\varphi = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\varphi} \end{pmatrix}, \qquad R_\varphi|b\rangle = e^{i\varphi b}|b\rangle \text{ for } b \in \{0, 1\}.$$

The gates with names are

$$Z = R_\pi = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \qquad S = R_{\pi/2} = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \qquad T = R_{\pi/4} = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}.$$

$S$ is the **phase gate** (some texts write $P$) and $T$ is the **T gate**, also called the **$\pi/8$ gate**.

**Powers.** $R_\varphi R_\psi = R_{\varphi + \psi}$, so the phase gates commute with each other and with $Z$. In particular

$$T^2 = S, \qquad S^2 = Z, \qquad T^4 = Z, \qquad T^8 = I, \qquad S^\dagger = S^3, \qquad T^\dagger = T^7.$$

**The name $\pi/8$.** Up to a global phase, $T$ is a rotation about the $z$ axis:

$$T = e^{i\pi/8}\begin{pmatrix} e^{-i\pi/8} & 0 \\ 0 & e^{i\pi/8} \end{pmatrix} = e^{i\pi/8}R_z(\pi/4).$$

The diagonal entries of the second matrix are $e^{\mp i\pi/8}$, which gives the name, although the Bloch-sphere rotation angle is $\pi/4$. In general $R_\varphi = e^{i\varphi/2}R_z(\varphi)$ with $R_z(\varphi) = e^{-i\varphi Z/2}$. On the [Bloch sphere](/bloch-sphere/), $R_\varphi$ turns every state by the angle $\varphi$ about the $z$ axis: it adds $\varphi$ to the azimuth and keeps the polar angle.

**Conjugation of the Pauli matrices.**

| $U$ | $UXU^\dagger$ | $UYU^\dagger$ | $UZU^\dagger$ |
|---|---|---|---|
| $S$ | $Y$ | $-X$ | $Z$ |
| $T$ | $(X + Y)/\sqrt 2$ | $(Y - X)/\sqrt 2$ | $Z$ |

$S$ maps every [Pauli matrix](/pauli-gates/) to a Pauli matrix up to sign, so it is in the [Clifford group](/clifford-group/). $T$ maps $X$ to $(X + Y)/\sqrt 2$, which is not a Pauli matrix times a phase, so $T$ is not a Clifford gate.

**The Clifford group and universality.** The gates $H$ and $S$ generate the one-qubit Clifford group; up to global phase it has 24 elements, the rotations of the cube that has the six Pauli eigenstates at the centres of its faces. With CNOT they generate the $n$-qubit Clifford group, whose circuits a classical computer can simulate efficiently ([Gottesman-Knill theorem](/gottesman-knill-theorem/)). Adding $T$ gives a [universal gate set](/universal-gate-set/): $\{H, T, \text{CNOT}\}$ approximates every unitary to any accuracy. On one qubit, $T$ and $HTH$ are rotations by $\pi/4$ about the $z$ and $x$ axes, and their product $T \cdot HTH$ is, up to phase, a rotation by an angle $\theta$ with

$$\cos\frac{\theta}{2} = \cos^2\frac{\pi}{8}.$$

N&C (Section 4.5.3) show that $\theta/\pi$ is irrational, so the powers of this rotation are dense in the rotations about its axis, and they build every one-qubit gate from $H$ and $T$ to any accuracy. The [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) makes this efficient: accuracy $\epsilon$ needs $O(\log^c(1/\epsilon))$ gates.

**On $n$ qubits.** With the qubit order convention of [quantum state](/quantum-state/), $R_\varphi$ on qubit $j$ multiplies the amplitude of $|x\rangle$ by $e^{i\varphi x_j}$, where $x_j$ is bit $j$ of $x$. A phase gate is diagonal in the computational basis, so it does not change the probabilities of a measurement in that basis.

## Examples and non-examples

**On the equator.** $S|+\rangle = (|0\rangle + i|1\rangle)/\sqrt 2 = |{+i}\rangle$, the $+1$ eigenvector of $Y$. $T|+\rangle = (|0\rangle + e^{i\pi/4}|1\rangle)/\sqrt 2$ is the point of the equator at azimuth $\pi/4$, halfway between $|+\rangle$ and $|{+i}\rangle$.

**A phase that matters later.** $T$ does not change the measurement probabilities of $|+\rangle$ in the computational basis: they stay $\tfrac12$ and $\tfrac12$. After a Hadamard gate they differ: $HTH|0\rangle$ gives $1$ with probability $\sin^2(\pi/8) \approx 0.146$ by the [Born rule](/born-rule/), because the two paths to $|1\rangle$ have the amplitudes $\tfrac12$ and $-\tfrac12 e^{i\pi/4}$ and cancel only in part. [Phase kickback](/phase-kickback/) and the [quantum Fourier transform](/quantum-fourier-transform/) use this: they write information into relative phases and then turn the phases into probabilities.

**A square root of $X$.** $HSH = \tfrac12\begin{pmatrix} 1 + i & 1 - i \\ 1 - i & 1 + i \end{pmatrix}$ squares to $HZH = X$.

**Non-example: a global phase.** $e^{i\pi/4}I$ multiplies every amplitude by the same number, so it is the identity gate up to global phase. $T$ multiplies only the amplitude of $|1\rangle$; this relative phase is observable.

**Non-example: square roots are not unique.** $S$ and $S^\dagger = \operatorname{diag}(1, -i)$ both square to $Z$, and so do $-S$ and $-S^\dagger$: the four diagonal matrices $\operatorname{diag}(\pm 1, \pm i)$. "$\sqrt Z$" means $S$ only by convention.

### Common errors

- Writing $T = \operatorname{diag}(1, e^{i\pi/8})$. The name comes from the symmetric form $e^{i\pi/8}\operatorname{diag}(e^{-i\pi/8}, e^{i\pi/8})$; the entry of $T$ is $e^{i\pi/4}$.
- Treating $R_\varphi$ and $R_z(\varphi)$ as the same gate in a controlled gate. They differ by the global phase $e^{i\varphi/2}$, but a controlled-$R_\varphi$ and a controlled-$R_z(\varphi)$ differ by the gate $R_{\varphi/2}$ on the control qubit. A global phase of $U$ becomes a relative phase of controlled-$U$.
- Giving all one-qubit gates the same cost. In a fault-tolerant code the Clifford gates $H$, $S$ and CNOT are usually inexpensive and $T$ is the expensive gate ([quantum threshold theorem](/quantum-threshold-theorem/)), so circuits are measured by their number of $T$ gates.

### Implementation

The file `impl/python/phase_and_t_gates.py` has $R_\varphi$, $S$, $T$, $R_z$, the phase gate on qubit $j$ of a register, a key for a matrix up to global phase, a breadth-first search for the group that a set of one-qubit gates generates up to phase, and the rotation angle of a $2 \times 2$ unitary. The tests check $T^2 = S$, $S^2 = Z$, $T^4 = Z$, $T^8 = I$, the $\pi/8$ form of $T$, $R_\varphi = e^{i\varphi/2}R_z(\varphi)$ for 20 random angles with seed 5, the conjugation table, that $TXT^\dagger$ is not a Pauli matrix up to phase, that $H$ and $S$ generate 24 elements up to phase and that each maps Pauli matrices to Pauli matrices up to sign, that $T$ is not among them, the angle $\cos(\theta/2) = \cos^2(\pi/8)$ of $T \cdot HTH$, and that phase gates keep the computational-basis probabilities of a random 4-qubit state with seed 17.

## Related definitions

- [Pauli gates](/pauli-gates/): $Z = R_\pi$ is the phase gate with the angle $\pi$.
- [Clifford group](/clifford-group/): generated by $H$, $S$ and CNOT.
- [Universal gate set](/universal-gate-set/) and [Solovay-Kitaev theorem](/solovay-kitaev-theorem/): why Clifford gates and $T$ are enough, and how many gates are needed.
- [Gottesman-Knill theorem](/gottesman-knill-theorem/): circuits without $T$ gates are classically simulable.
- [Quantum Fourier transform](/quantum-fourier-transform/): uses controlled $R_{2\pi/2^k}$ gates.

### History

Boykin, Mor, Pulver, Roychowdhury and Vatan showed in 2000 that $H$, CNOT and $T$ form a universal set whose gates can be applied fault-tolerantly. N&C call $T$ the $\pi/8$ gate.

## References
