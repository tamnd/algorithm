---
title: Superdense coding decodes every message with certainty, and two bits per qubit is the most possible
proves: [correctness]
status: full
---

We use the pseudocode of the page. Qubit $1$ is Alice's half of the pair and qubit $0$ is Bob's half, and a ket $|q_1 q_0\rangle$ lists qubit $1$ first. The message is $(x, y) \in \{0, 1\}^2$.

**Claim 1.** For each message $(x, y)$, Bob's measurement in line L7 gives $(x, y)$ with probability $1$.

*Proof.* Line L1 gives $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$. Lines L2 and L3 apply $Z^x X^y$ to qubit $1$. The four results are

- $(0, 0)$: $(|00\rangle + |11\rangle)/\sqrt{2} = |\Phi^+\rangle$;
- $(0, 1)$: $X$ on qubit $1$ gives $(|10\rangle + |01\rangle)/\sqrt{2} = |\Psi^+\rangle$;
- $(1, 0)$: $Z$ on qubit $1$ gives $(|00\rangle - |11\rangle)/\sqrt{2} = |\Phi^-\rangle$;
- $(1, 1)$: $X$, then $Z$, on qubit $1$ gives $(|01\rangle - |10\rangle)/\sqrt{2} = |\Psi^-\rangle$.

Line L4 moves qubit $1$ to Bob and does not change the state. Line L5 applies CNOT with control qubit $1$ and target qubit $0$, which maps $|00\rangle, |01\rangle, |10\rangle, |11\rangle$ to $|00\rangle, |01\rangle, |11\rangle, |10\rangle$. So the four states become

$$\tfrac{|00\rangle + |10\rangle}{\sqrt{2}} = |{+}\rangle|0\rangle,\quad \tfrac{|01\rangle + |11\rangle}{\sqrt{2}} = |{+}\rangle|1\rangle,\quad \tfrac{|00\rangle - |10\rangle}{\sqrt{2}} = |{-}\rangle|0\rangle,\quad \tfrac{|01\rangle - |11\rangle}{\sqrt{2}} = |{-}\rangle|1\rangle,$$

with $|{\pm}\rangle = (|0\rangle \pm |1\rangle)/\sqrt{2}$. Line L6 applies $H$ to qubit $1$, and $H|{+}\rangle = |0\rangle$, $H|{-}\rangle = |1\rangle$. So the message $(x, y)$ ends in the basis state $|x\, y\rangle$, and the measurement of line L7 returns $(x, y)$ with probability $1$. $\square$

The proof also shows that the four states after line L3 are the four Bell states, which are orthonormal, and that lines L5 and L6 are the unitary that maps the Bell basis to the computational basis.

**Claim 2.** Each qubit alone carries no information about the message: for every $(x, y)$, the reduced state of qubit $1$ and the reduced state of qubit $0$ are both $I/2$.

*Proof.* Each of the four Bell states has the form $(|a b\rangle \pm |\bar a \bar b\rangle)/\sqrt{2}$ with $\bar a = 1 - a$. Tracing out one qubit gives $\tfrac{1}{2}(|a\rangle\langle a| + |\bar a\rangle\langle \bar a|) = I/2$, since the cross terms pair orthogonal states of the traced qubit. $\square$

So an eavesdropper who captures the qubit of line L4 alone, or who holds Bob's half alone, learns nothing.

**Claim 3 (optimality).** Suppose Alice sends one qubit $Q$ to Bob, and Bob also holds a system $B$ that may be entangled with Alice's systems in any way before the message is chosen. Then the mutual information between the message and Bob's measurement result is at most $2$ bits.

*Proof.* Alice's encoding of the message $m$ acts only on her systems, so by the no-communication theorem the state $\rho_B$ of $B$ is the same for every $m$. Let $\rho^m_{QB}$ be the state Bob holds for message $m$, sent with probability $p_m$, and let $\bar\rho_{QB} = \sum_m p_m \rho^m_{QB}$. The Holevo bound says the mutual information is at most

$$\chi = S(\bar\rho_{QB}) - \sum_m p_m S(\rho^m_{QB}).$$

By subadditivity, $S(\bar\rho_{QB}) \le S(\bar\rho_Q) + S(\rho_B) \le 1 + S(\rho_B)$. By the triangle inequality of Araki and Lieb, $S(\rho^m_{QB}) \ge S(\rho_B) - S(\rho^m_Q) \ge S(\rho_B) - 1$. Together, $\chi \le 1 + S(\rho_B) - (S(\rho_B) - 1) = 2$. $\square$

**Claim 4 (without entanglement).** If Alice and Bob share no entanglement, that is, the start state of $Q$ and $B$ is a product $\rho_Q \otimes \sigma_B$ or a mixture of products, then for a uniform message of two bits Bob guesses correctly with probability at most $\tfrac{1}{2}$.

*Proof.* First take a product start. Alice's encoding gives $\rho^m_Q \otimes \sigma_B$ for message $m$, with $\sigma_B$ fixed. Let $\{M_m\}$ be Bob's measurement on $QB$, with $M_m \ge 0$ and $\sum_m M_m = I$. Since $\rho^m_Q \le I_Q$, also $\rho^m_Q \otimes \sigma_B \le I_Q \otimes \sigma_B$, so

$$\Pr[\text{correct}] = \tfrac{1}{4}\sum_m \mathrm{Tr}\big(M_m(\rho^m_Q \otimes \sigma_B)\big) \le \tfrac{1}{4}\sum_m \mathrm{Tr}\big(M_m (I_Q \otimes \sigma_B)\big) = \tfrac{1}{4}\mathrm{Tr}(I_Q \otimes \sigma_B) = \tfrac{2}{4}.$$

A mixture of products is a convex combination of such cases, so the bound holds for it too. The bound is reached: start in $|00\rangle$ and run lines L2 to L7. Since $Z|0\rangle = |0\rangle$, the encoding gives $|y\,0\rangle$, line L5 gives $|y\,y\rangle$ and line L6 gives $H|y\rangle \otimes |y\rangle$. Bob reads $y$ with certainty and $x$ only with probability $\tfrac{1}{2}$. $\square$

**Cost.** Alice applies at most two one-qubit gates and sends one qubit. Bob applies one CNOT and one Hadamard and measures two qubits. One Bell pair is used up per two bits. $\square$
