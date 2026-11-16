---
tag: RNV41Q
kind: definition
slug: qma
name: QMA
aliases:
- quantum Merlin-Arthur
area: complexity/complexity-classes
level: research
summary: "Quantum Merlin-Arthur: a polynomial-time quantum verifier checks a quantum proof state with bounded error. Contains NP, MA and BQP, lies in PP, and the local Hamiltonian problem is complete."
prereqs: [merlin-arthur, bqp, quantum-circuit-model, quantum-state]
see_also: [merlin-arthur, bqp, pp, ground-state-energy-estimation, quantum-measurement, entanglement, no-cloning-theorem, interactive-proofs]
sources:
  - book: isbn:9780821832295
    title: Alexei Kitaev, Alexander Shen and Mikhail Vyalyi, Classical and Quantum Computation, American Mathematical Society, Graduate Studies in Mathematics 47 (2002)
    locator: Chapter 14, the class BQNP (QMA), amplification and the completeness of the 5-local Hamiltonian problem
  - paper: arxiv:quant-ph/0302079
    title: Julia Kempe and Oded Regev, 3-local Hamiltonian is QMA-complete, Quantum Information and Computation 3(3), 258 to 264 (2003)
    locator: the main theorem
  - paper: doi:10.1137/S0097539704445226
    title: Julia Kempe, Alexei Kitaev and Oded Regev, The complexity of the local Hamiltonian problem, SIAM Journal on Computing 35(5), 1070 to 1097 (2006)
    locator: the QMA-completeness of the 2-local Hamiltonian problem
  - paper: doi:10.1007/s00037-005-0194-x
    title: Chris Marriott and John Watrous, Quantum Arthur-Merlin games, Computational Complexity 14(2), 122 to 152 (2005)
    locator: error reduction without a longer proof, and a short proof that QMA is a subset of PP
---

QMA (quantum Merlin-Arthur) is the class of problems whose yes-instances have a *quantum proof*: a state of polynomially many [qubits](/qubit/) that a polynomial-time quantum verifier accepts with probability at least $2/3$, while on no-instances every state is accepted with probability at most $1/3$. It is the quantum analogue of [MA](/merlin-arthur/) and of [NP](/np/). Kitaev defined it under the name BQNP and proved that the 5-local Hamiltonian problem is complete for it, which is the quantum analogue of the Cook-Levin theorem. QMA contains NP, MA and [BQP](/bqp/), and it is a subset of [PP](/pp/).

## Definition

**Verifier.** A *verifier* is a family of quantum circuits $\{V_x\}$ over a fixed finite universal gate set ([quantum circuit model](/quantum-circuit-model/)), generated from $x$ by a deterministic polynomial-time [multitape Turing machine](/multitape-turing-machine/). The circuit $V_x$ acts on $q(|x|)$ proof qubits and $s(|x|)$ work qubits, for polynomials $q$ and $s$. The work qubits start in the state $|0\cdots0\rangle$. After the circuit runs, one output qubit is measured in the standard basis ([quantum measurement](/quantum-measurement/)), and the outcome $1$ means accept. For a proof state $|\psi\rangle$ on $q$ qubits, write $\Pr[V_x \text{ accepts } |\psi\rangle]$.

**Definition.** A promise problem $(A_{\text{yes}}, A_{\text{no}})$ is in $\mathsf{QMA}$ if there is a verifier with

$$x \in A_{\text{yes}} \Rightarrow \exists |\psi\rangle : \Pr[V_x \text{ accepts } |\psi\rangle] \ge \tfrac23, \qquad x \in A_{\text{no}} \Rightarrow \forall |\psi\rangle : \Pr[V_x \text{ accepts } |\psi\rangle] \le \tfrac13.$$

QMA is defined for promise problems because its natural complete problem has a promise. Mixed proofs ([density matrices](/density-matrix/)) do not help a cheating prover, since the acceptance probability of a mixture is an average of the acceptance probabilities of [pure states](/quantum-state/).

**Amplification.** The constants $2/3$ and $1/3$ can be replaced by $1 - 2^{-t}$ and $2^{-t}$ for any polynomial $t$, but the proof differs from MA.

- *Many copies.* A quantum proof cannot be copied ([no-cloning theorem](/no-cloning-theorem/)), and a measurement can disturb it, so Arthur cannot reuse one proof. Instead, Merlin sends $k$ registers, the honest prover sends $|\psi\rangle^{\otimes k}$, and Arthur runs $V_x$ on each register and takes the majority. A cheating Merlin may entangle the registers ([entanglement](/entanglement/)), but conditioned on the outcomes for the other registers, each register is in some state and is accepted with probability at most $1/3$. So the Chernoff bound still applies, as Kitaev showed. The proof grows by the factor $k$.
- *One copy.* Marriott and Watrous (2005) reduced the error without making the proof longer. Arthur alternates the verifier measurement and the projection onto the initial work state, and accepts by the statistics of the outcomes.

**Inclusions.** $\mathsf{NP} \subseteq \mathsf{MA} \subseteq \mathsf{QMA} \subseteq \mathsf{PP} \subseteq \mathsf{PSPACE}$ and $\mathsf{BQP} \subseteq \mathsf{QMA}$.

- MA is in QMA: a classical proof is a basis state, and a quantum circuit can simulate Arthur's coins with Hadamard gates.
- BQP is in QMA: the verifier ignores the proof.
- QMA is in PP: Kitaev and Watrous proved it, and Marriott and Watrous gave a short proof with their one-copy amplification. Amplify with one copy until the error is below $2^{-q-2}$, where $q$ is the number of proof qubits, and run the verifier on a uniformly random basis state as the proof. Its acceptance probability is $2^{-q}$ times the trace of the acceptance operator. On a yes-instance the trace is at least the largest eigenvalue, which is at least $3/4$. On a no-instance every eigenvalue is at most $2^{-q-2}$, so the trace is at most $1/4$. A PP machine can compare the acceptance probability of a polynomial-time quantum computation with the threshold $2^{-q-1}$.
- QCMA is the class with a classical proof and a quantum verifier. It lies between MA and QMA. Whether QCMA equals QMA is open.

## Examples and non-examples

**Examples.**

- *The $k$-local Hamiltonian problem.* The input is a Hamiltonian $H = \sum_{j=1}^m H_j$ on $n$ qubits, where each $H_j$ is a Hermitian matrix with $0 \le H_j \le I$ that acts on at most $k$ qubits and is given by its $2^k \times 2^k$ entries, and two numbers $a < b$ with $b - a \ge 1/\mathrm{poly}(n)$. The promise is that the smallest eigenvalue $\lambda_{\min}(H)$ is at most $a$ or at least $b$; the question is which. Kitaev proved it QMA-complete for $k = 5$, Kempe and Regev (2003) for $k = 3$, and Kempe, Kitaev and Regev (2006) for $k = 2$. For $k = 1$ it is in P, because each term acts alone and the smallest eigenvalue is the sum of the smallest eigenvalues of the terms. The numerical task is on [ground state energy estimation](/ground-state-energy-estimation/).
- *Why it is in QMA.* Merlin sends a state $|\psi\rangle$ that is claimed to have low energy. Arthur picks $j$ uniformly and measures the two-outcome measurement $\{H_j, I - H_j\}$ on the qubits of $H_j$, and accepts on the outcome $I - H_j$. Then $\Pr[\text{accept}] = 1 - \langle \psi | H | \psi \rangle / m$. The ground state gives $1 - \lambda_{\min}/m$, and every state gives at most this. The gap between yes and no is $(b - a)/m$, which is at least an inverse polynomial, and amplification with many copies makes it a constant.
- *A worked case on three qubits.* Let $P$ be the projector on the singlet $(|01\rangle - |10\rangle)/\sqrt2$ of two qubits, and take $H = \sum_{\{i,j\}} (I - P_{ij})$ over the three pairs of qubits, so $m = 3$ and each term is $2$-local. Exact diagonalization gives the eigenvalues $1.5$ with multiplicity $4$ and $3$ with multiplicity $4$. Every standard basis state has energy $2$ or $3$. For a product state with Bloch vectors $n_1, n_2, n_3$, the energy is $\tfrac94 + \tfrac14 \sum_{i<j} n_i \cdot n_j$, and $\sum_{i<j} n_i \cdot n_j \ge -\tfrac32$ because $|n_1 + n_2 + n_3|^2 \ge 0$. So every product state has energy at least $1.875$, with equality when the three vectors lie in one plane at $120^\circ$ to each other. With the verifier above, the acceptance probabilities are $1 - 1.5/3 = 0.5$ for a ground state, $1 - 1.875/3 = 0.375$ for the best product state and $1 - 2/3 = 1/3$ for the best basis state. With $a = 1.5$ and $b = 1.8$, the instance is a yes-instance, but only an entangled state has energy below $b$.

**Non-examples.**

- *PSPACE-complete problems, unless $\mathsf{PSPACE} = \mathsf{PP}$*, since QMA is a subset of PP.
- *Proofs with two unentangled parts.* The class $\mathsf{QMA}(2)$, where Merlin sends two registers that are promised to be unentangled, is a different definition. It is not known to equal QMA.
- *Quantum interactive proofs with many messages.* These give QIP, which equals PSPACE, not QMA. See [interactive proofs](/interactive-proofs/).

## Related definitions

- [MA](/merlin-arthur/) is QMA with a classical proof and a classical randomized verifier.
- [BQP](/bqp/) is QMA without a proof.
- [PP](/pp/) is an upper bound for QMA.
- The local Hamiltonian problem plays the role of [SAT](/sat/): its terms are local constraints, and the energy counts the violated constraints in a weighted sense. A classical constraint system of $k$-ary constraints is the special case of a diagonal Hamiltonian, so the problem is NP-hard for every $k \ge 2$.
- Classical interactive proofs with several provers that share entanglement give the class $\mathsf{MIP}^*$, which is on [multi-prover interactive proofs](/multi-prover-interactive-proofs/).

## References
