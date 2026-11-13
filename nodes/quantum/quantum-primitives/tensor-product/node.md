---
tag: XDTSZS
kind: definition
slug: tensor-product
name: Tensor product
area: quantum/quantum-primitives
level: intro
summary: "The tensor product combines the state spaces of quantum systems: n qubits live in the 2^n-dimensional space C^2 (x) ... (x) C^2, and the matrices are Kronecker products."
prereqs: [quantum-state, kronecker-product]
see_also: [entanglement, bell-states, partial-trace, density-matrix, quantum-gate, cnot-gate, tensor-rank, walsh-hadamard-transform]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.1.7 (tensor products) and Section 2.2.8 (composite systems)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.3 (qubits and quantum memory) and Appendix A.6 (tensor products)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 2 (linear algebra and the Dirac notation, tensor products) and Chapter 3 (composite systems)
---

The *tensor product* $V \otimes W$ of two vector spaces is the space of the joint system: if one system has the state space $V$ and another has $W$, the pair has the state space $V \otimes W$, of dimension $\dim V \cdot \dim W$. For $n$ qubits it gives $(\mathbb{C}^2)^{\otimes n}$, of dimension $2^n$. In coordinates the tensor product of vectors and of matrices is the [Kronecker product](/kronecker-product/), and the order of the factors fixes which qubit is which. Most vectors of $V \otimes W$ are not of the form $|v\rangle \otimes |w\rangle$; those that are not describe [entangled](/entanglement/) states.

## Definition

**Vectors.** Let $V = \mathbb{C}^m$ and $W = \mathbb{C}^p$, with standard bases $|i\rangle$ and $|k\rangle$. The tensor product $V \otimes W$ is $\mathbb{C}^{mp}$ with the basis vectors $|i\rangle \otimes |k\rangle$, and the tensor product of $|v\rangle = \sum_i v_i |i\rangle$ and $|w\rangle = \sum_k w_k |k\rangle$ is

$$|v\rangle \otimes |w\rangle = \sum_{i,k} v_i w_k \, |i\rangle \otimes |k\rangle.$$

As a column, $|v\rangle \otimes |w\rangle$ has the entry $v_i w_k$ at position $i p + k$. Short forms of $|v\rangle \otimes |w\rangle$ are $|v\rangle|w\rangle$ and $|v, w\rangle$, and for basis states $|i\rangle|k\rangle = |ik\rangle$. The map $(v, w) \mapsto v \otimes w$ is linear in each argument: $(a|v\rangle + b|v'\rangle) \otimes |w\rangle = a\,|v\rangle \otimes |w\rangle + b\,|v'\rangle \otimes |w\rangle$, and the same holds in the second argument. The inner product is $(\langle v| \otimes \langle w|)(|v'\rangle \otimes |w'\rangle) = \langle v|v'\rangle \langle w|w'\rangle$, so the product of two unit vectors is a unit vector.

**Matrices.** For an $m \times n$ matrix $A$ and a $p \times q$ matrix $B$, the tensor product $A \otimes B$ is the $mp \times nq$ Kronecker product with the entries $(A \otimes B)_{ip+k,\, jq+l} = A_{ij} B_{kl}$. It is the unique linear map with $(A \otimes B)(|v\rangle \otimes |w\rangle) = A|v\rangle \otimes B|w\rangle$. It obeys the mixed-product rule $(A \otimes B)(C \otimes D) = AC \otimes BD$ and $(A \otimes B)^\dagger = A^\dagger \otimes B^\dagger$. So the tensor product of two unitary matrices is unitary, and the tensor product of two Hermitian matrices is Hermitian.

**Composite systems.** The state space of a system made of parts with state spaces $\mathcal{H}_1, \dots, \mathcal{H}_k$ is $\mathcal{H}_1 \otimes \cdots \otimes \mathcal{H}_k$. If part $i$ is prepared in the state $|\psi_i\rangle$, independently of the others, the joint state is $|\psi_1\rangle \otimes \cdots \otimes |\psi_k\rangle$. This is postulate 4 of Nielsen and Chuang.

**Product and entangled states.** A pure state of $V \otimes W$ is a *product state* if it equals $|v\rangle \otimes |w\rangle$ for some $|v\rangle \in V$ and $|w\rangle \in W$, and it is *entangled* otherwise. A two-qubit state $\sum_{a,b} \alpha_{ab}|ab\rangle$ is a product state if and only if $\alpha_{00}\alpha_{11} = \alpha_{01}\alpha_{10}$, because this says that the $2 \times 2$ matrix $(\alpha_{ab})$ has rank one ([determinant](/determinant/) zero). A product of $n$ one-qubit pure states has $2n$ real parameters, but a general pure state of $n$ qubits has $2^{n+1} - 2$. So for $n \ge 2$ the product states are a set of measure zero, and most states are entangled.

### The qubit order of the tensor factors

The quantum pages of this encyclopedia use the order that the [quantum state](/quantum-state/) page fixes. In short:

- On $n$ qubits numbered $0$ to $n-1$, $|b_{n-1} \cdots b_1 b_0\rangle = |b_{n-1}\rangle \otimes \cdots \otimes |b_1\rangle \otimes |b_0\rangle = |x\rangle$ with $x = \sum_j b_j 2^j$. Qubit $n-1$ is the leftmost factor and the most significant bit. Qubit $0$ is the rightmost factor and the least significant bit.
- This agrees with the Kronecker index rule above: the left factor sets the high-order part $i$ of the index $ip + k$.
- A gate $U$ on qubit $j$ is $I^{\otimes(n-1-j)} \otimes U \otimes I^{\otimes j}$. So $U \otimes V$ on two qubits applies $V$ to qubit $0$ and $U$ to qubit $1$, and $U \otimes V = (U \otimes I)(I \otimes V)$.
- Nielsen and Chuang number the factors $1$ to $n$ from the left; their qubit $k$ is qubit $n-k$ here. The matrices are the same.

The tensor product is not commutative. $X \otimes I$ flips qubit $1$ and $I \otimes X$ flips qubit $0$, and they are different matrices. The two orders are related by the SWAP matrix $S$, with $S|a b\rangle = |b a\rangle$: $S(A \otimes B)S = B \otimes A$ for $2 \times 2$ matrices $A$ and $B$.

## Examples and non-examples

**Two basis states.** $|1\rangle \otimes |0\rangle = (0, 1)^T \otimes (1, 0)^T = (0, 0, 1, 0)^T = |10\rangle = |2\rangle$. Here qubit $1$ is $1$ and qubit $0$ is $0$.

**A product state with no zero amplitude.** With $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$,

$$|+\rangle \otimes |+\rangle = \tfrac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle).$$

Here $\alpha_{00}\alpha_{11} = \alpha_{01}\alpha_{10} = \tfrac{1}{4}$. In the same way $H^{\otimes n}|0\rangle^{\otimes n}$, the [Hadamard gate](/hadamard-gate/) on each qubit, is the uniform superposition over all $2^n$ basis states, and it is a product state.

**A gate on one qubit of two.** $X$ on qubit $0$ is $I \otimes X$, the matrix with the blocks $X$ on the diagonal. It maps $|ab\rangle$ to $|a\,(1-b)\rangle$. $X$ on qubit $1$ is $X \otimes I = \begin{pmatrix} 0 & I \\ I & 0 \end{pmatrix}$.

**Non-example: a Bell state.** $(|00\rangle + |11\rangle)/\sqrt{2}$ has $\alpha_{00}\alpha_{11} = \tfrac{1}{2}$ and $\alpha_{01}\alpha_{10} = 0$, so it is not a product state ([Bell states](/bell-states/)). The [CNOT gate](/cnot-gate/) is also not a tensor product of two one-qubit matrices: it acts on qubit $0$ in a way that depends on qubit $1$.

**Non-example: the direct sum.** The space of a qubit together with a second qubit is not $\mathbb{C}^2 \oplus \mathbb{C}^2 = \mathbb{C}^4$ with the vectors $(a, b, c, d)$ read as two separate pairs. The direct sum has dimension $2 + 2$; the tensor product has dimension $2 \cdot 2$. For $n$ qubits the dimensions are $2n$ and $2^n$, and the gap between them is the reason that $n$ qubits cannot be simulated by $n$ separate two-dimensional vectors in general.

### Common errors

- Reversing the factors. Code that builds $I \otimes U$ for "$U$ on qubit $1$" puts $U$ on qubit $0$ in this convention. Test a new gate routine against the rule $X$ on qubit $j$ maps $|x\rangle$ to $|x \oplus 2^j\rangle$.
- Building the full matrix. $I^{\otimes(n-1-j)} \otimes U \otimes I^{\otimes j}$ has $4^n$ entries. A simulator applies $U$ to each of the $2^{n-1}$ pairs of amplitudes $(\alpha_x, \alpha_{x + 2^j})$ with bit $j$ of $x$ equal to $0$, in $O(2^n)$ time and with no extra matrix.
- Reading an entangled state as a list of qubit states. The state of one qubit of an entangled pair is not a vector but a density matrix, the [partial trace](/partial-trace/) of the joint state.

### Implementation

The file `impl/python/tensor_product.py` has `kron` and `kron_vec` with the index rule above, `on_qubit(n, u, j)` for the matrix of $U$ on qubit $j$, the SWAP matrix, and the two-qubit product test $\lvert \alpha_{00}\alpha_{11} - \alpha_{01}\alpha_{10} \rvert = 0$ with a factorization routine. The tests compare `on_qubit` with the simulator routine that applies a gate to one qubit, check the mixed-product rule and the SWAP relation on random matrices with fixed seeds, and check that $|b_{n-1}\rangle \otimes \cdots \otimes |b_0\rangle = |x\rangle$ for every basis state on 1 to 4 qubits.

## Related definitions

- [Kronecker product](/kronecker-product/): the matrix form, with its algebraic rules and their use in fast algorithms.
- [Quantum state](/quantum-state/): the qubit order convention in full.
- [Entanglement](/entanglement/) and [Bell states](/bell-states/): states that are not tensor products.
- [Partial trace](/partial-trace/): the inverse operation for states, from a joint state to the state of one part.
- [Tensor rank](/tensor-rank/): the least number of product terms in a sum that gives a tensor; for two parts it is the matrix rank, and for pure states it is the Schmidt rank.
- [Walsh-Hadamard transform](/walsh-hadamard-transform/): the $n$-fold tensor power $H^{\otimes n}$ of the Hadamard matrix.

## References
