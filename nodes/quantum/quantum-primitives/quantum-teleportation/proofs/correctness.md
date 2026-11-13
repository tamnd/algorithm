---
title: Teleportation delivers the input state to Bob for every measurement outcome
proves: [correctness]
status: full
---

We use the pseudocode of the page. Qubit $2$ holds the input $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ with $|\alpha|^2 + |\beta|^2 = 1$, qubits $1$ and $0$ hold $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$, and a ket $|q_2 q_1 q_0\rangle$ lists qubit $2$ first.

**Claim.** For each pair of outcomes $(m_z, m_x) \in \{0, 1\}^2$ of line L4: (a) the pair occurs with probability exactly $\tfrac{1}{4}$, whatever $|\psi\rangle$ is; (b) after line L4, qubit $0$ is in the state $X^{m_x} Z^{m_z}|\psi\rangle$; (c) after lines L6 and L7, qubit $0$ is in the state $|\psi\rangle$.

*Proof.* After line L1 the state is

$$\tfrac{1}{\sqrt{2}}\big(\alpha|0\rangle(|00\rangle + |11\rangle) + \beta|1\rangle(|00\rangle + |11\rangle)\big).$$

Line L2 applies CNOT with control qubit $2$ and target qubit $1$. It changes only the terms with qubit $2$ equal to $1$, where it flips qubit $1$:

$$\tfrac{1}{\sqrt{2}}\big(\alpha|0\rangle(|00\rangle + |11\rangle) + \beta|1\rangle(|10\rangle + |01\rangle)\big).$$

Line L3 applies $H$ to qubit $2$, with $H|0\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$ and $H|1\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$:

$$\tfrac{1}{2}\big(\alpha(|0\rangle + |1\rangle)(|00\rangle + |11\rangle) + \beta(|0\rangle - |1\rangle)(|10\rangle + |01\rangle)\big).$$

Expand the products and collect the terms by the values of qubits $2$ and $1$:

$$\tfrac{1}{2}\Big(|00\rangle(\alpha|0\rangle + \beta|1\rangle) + |01\rangle(\alpha|1\rangle + \beta|0\rangle) + |10\rangle(\alpha|0\rangle - \beta|1\rangle) + |11\rangle(\alpha|1\rangle - \beta|0\rangle)\Big).$$

In the term with $(m_z, m_x)$ on qubits $2$ and $1$, the state of qubit $0$ is $\phi_{m_z m_x} = X^{m_x} Z^{m_z}|\psi\rangle$: $Z$ maps $\alpha|0\rangle + \beta|1\rangle$ to $\alpha|0\rangle - \beta|1\rangle$, and $X$ swaps the two amplitudes, which gives the four vectors above in order. Each $\phi_{m_z m_x}$ is a unit vector, because $X$ and $Z$ are unitary.

(a) and (b). Line L4 measures qubits $2$ and $1$ in the computational basis. By the Born rule, the outcome $(m_z, m_x)$ has probability equal to the squared norm of its term, $\lVert \tfrac{1}{2}\phi_{m_z m_x} \rVert^2 = \tfrac{1}{4}$, and the state after the measurement is $|m_z m_x\rangle \otimes \phi_{m_z m_x}$. This proves (a) and (b).

(c). Line L5 gives Bob the bits $m_z$ and $m_x$. Line L6 applies $X^{m_x}$ and line L7 applies $Z^{m_z}$, so qubit $0$ ends in

$$Z^{m_z} X^{m_x} \cdot X^{m_x} Z^{m_z} |\psi\rangle = Z^{m_z} Z^{m_z} |\psi\rangle = |\psi\rangle,$$

because $X^2 = Z^2 = I$. $\square$

**Bob's qubit before the bits arrive.** Before line L5, Bob does not know the outcome, so his qubit is described by the average over the four outcomes of (b):

$$\rho_{\mathrm{Bob}} = \tfrac{1}{4} \sum_{m_z, m_x} X^{m_x} Z^{m_z} |\psi\rangle\langle\psi| Z^{m_z} X^{m_x} = \tfrac{I}{2}.$$

The last equality holds for every $2 \times 2$ matrix $\rho$ in place of $|\psi\rangle\langle\psi|$: write $\rho = \tfrac{1}{2}(\mathrm{Tr}\rho\, I + r_x X + r_y Y + r_z Z)$. Conjugation by $Z$ changes the signs of $r_x$ and $r_y$, and conjugation by $X$ changes the signs of $r_y$ and $r_z$; the average over the four products removes all three. So $\rho_{\mathrm{Bob}} = \tfrac{1}{2}\mathrm{Tr}\rho\, I = I/2$. The same follows from the no-communication theorem, as lines L2 to L4 act only on Alice's qubits. $\square$

**Linearity and entangled inputs.** The circuit of lines L1 to L7 with the corrections controlled by the outcomes is a fixed sequence of operations, so the claim extends by linearity: if qubit $2$ is entangled with a reference system $R$, in the state $\sum_j c_j |r_j\rangle|\psi_j\rangle$, then each outcome occurs with probability $\tfrac{1}{4}$ and, after the corrections, $R$ and qubit $0$ are in $\sum_j c_j |r_j\rangle|\psi_j\rangle$. Indeed, in each branch the operator applied to qubit $0$ is the same operator $X^{m_x} Z^{m_z}$ for every $j$, and the correction undoes it. With $R$ and qubit $2$ in a Bell state, this is entanglement swapping.

**Cost.** Alice applies two gates and measures two qubits; Bob applies at most two one-qubit gates. One Bell pair and two classical bits are used up. $\square$
