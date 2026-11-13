---
tag: 5SF402
kind: technique
slug: block-encoding
name: Block encoding
aliases:
- unitary block encoding
area: quantum/quantum-simulation
level: advanced
summary: "Put A/alpha in the top-left block of a unitary U on a + n qubits. Running U on |0^a>|psi> and seeing the ancillas in 0^a applies A/alpha to |psi>."
prereqs: [unitary-operator, ancilla-qubits, linear-combination-of-unitaries]
see_also: [qubitization, quantum-signal-processing, quantum-eigenvalue-transformation, optimal-hamiltonian-simulation, sparse-hamiltonian-simulation, amplitude-amplification, linear-system-solving, condition-number]
sources:
  - paper: doi:10.1145/3313276.3316366
    title: "András Gilyén, Yuan Su, Guang Hao Low and Nathan Wiebe, Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics, Proceedings of the 51st ACM Symposium on Theory of Computing (STOC), 2019, pages 193 to 204 (arXiv:1806.01838)"
    locator: "numbering of arXiv v1: Definition 43 (the (alpha, a, epsilon) block encoding), Definition 44 (a unitary encodes itself), Lemma 45 (density operators), Lemma 47 (Gram matrices of two state preparations), Lemma 48 (sparse-access matrices), Lemma 52 (linear combinations), Lemma 53 (products) and Corollary 69 (the polynomial for 1/x)"
  - paper: doi:10.22331/q-2019-07-12-163
    title: "Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3, 2019, article 163 (arXiv:1610.06546)"
    locator: "the standard form of a Hamiltonian as a projection of a unitary oracle, and the construction from a linear combination of unitaries"
  - paper: doi:10.1145/2591796.2591854
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Exponential improvement in precision for simulating sparse Hamiltonians, Proceedings of the 46th ACM STOC, 2014, pages 283 to 292 (arXiv:1312.1414)"
    locator: "Section 3 (the PREPARE, SELECT, PREPARE^dagger form of a linear combination of unitaries)"
  - paper: doi:10.1103/PhysRevLett.103.150502
    title: "Aram W. Harrow, Avinatan Hassidim and Seth Lloyd, Quantum algorithm for linear systems of equations, Physical Review Letters 103(15), 2009, article 150502 (arXiv:0811.3171)"
    locator: "the whole paper: the algorithm and its cost in the sparsity, the condition number and the error"
  - paper: doi:10.1137/16M1087072
    title: "Andrew M. Childs, Robin Kothari and Rolando D. Somma, Quantum algorithm for systems of linear equations with exponentially improved dependence on precision, SIAM Journal on Computing 46(6), 2017, pages 1920 to 1950 (arXiv:1511.02306)"
    locator: "the main results: linear systems through a linear combination of unitaries, with cost polylogarithmic in 1/epsilon"
  - paper: doi:10.1038/nphys3272
    title: "Scott Aaronson, Read the fine print, Nature Physics 11, 2015, pages 291 to 293"
    locator: "the whole commentary: the four caveats of the linear systems algorithm"
---

A *block encoding* of a matrix $A$ is a unitary $U$ on $a$ ancilla qubits and $n$ system qubits whose top-left block is $A/\alpha$:
$$U = \begin{pmatrix} A/\alpha & \ast \\ \ast & \ast \end{pmatrix}, \qquad (\langle 0^a| \otimes I)\, U\, (|0^a\rangle \otimes I) = A/\alpha.$$
The number $\alpha \ge \|A\|$ is the *normalization*. More generally, $U$ is an $(\alpha, a, \epsilon)$-block-encoding of $A$ when $\|A - \alpha(\langle 0^a| \otimes I)U(|0^a\rangle \otimes I)\| \le \epsilon$ (Gilyén, Su, Low and Wiebe, Definition 43). A block encoding is the input format of [qubitization](/qubitization/), [quantum signal processing](/quantum-signal-processing/) and the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/): it lets a quantum circuit use a matrix that is not unitary, such as a Hamiltonian, as one of its gates. Each call to $U$ is one query, and the cost of an algorithm is a number of queries and the normalization $\alpha$.

## In plain words

A quantum computer can apply only reversible, length-keeping operations. Most matrices of interest are not of this kind: a Hamiltonian stretches some directions and shrinks others. The trick is to add helper qubits and to build a larger reversible operation that does the wanted action on one small corner. The helpers start in a fixed blank state. After the operation we look at the helpers. If they are still blank, the main qubits carry the result of the wanted matrix, scaled down by a known factor. If they are not blank, the attempt failed. The scale factor sets the price: a larger factor gives a smaller chance of success, and the later algorithms that use the encoding need more calls. A good block encoding has a factor close to the size of the matrix itself.

## When it applies

- The matrix $A$ has a structure that a circuit can read: a short list of Pauli strings with weights, a sparse pattern with an oracle for the entries, a density matrix with a preparation circuit, or a product or sum of matrices that already have block encodings.
- The algorithm only needs to apply $A$ (or a function of $A$) to a quantum state, not to write the entries of $A$ or of the result.
- The cost of interest is the number of calls to $U$, times the gates per call, as a function of $\alpha$. For [Hamiltonian simulation](/hamiltonian-simulation/) the query count is $\Theta(\alpha t + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/(\alpha t)))$ (Gilyén, Su, Low and Wiebe, Corollary 60), so $\alpha$ plays the role of the norm of $H$.

## The template

The basic construction is for a Hamiltonian given as a [Pauli string decomposition](/pauli-string-decomposition/) $H = \sum_{j=0}^{L-1} c_j P_j$ with real $c_j$. It is the [linear combination of unitaries](/linear-combination-of-unitaries/) in the PREPARE, SELECT, PREPARE$^\dagger$ form. The ancilla register holds an index $j$ in binary on $a = \lceil \log_2 L \rceil$ qubits (at least one), and it sits on the high qubits, so $\langle 0^a| U |0^a\rangle$ is the top-left block of the matrix of $U$.

```pseudo id=main
BLOCK-ENCODE(((c_0, P_0), ..., (c_{L-1}, P_{L-1})))
L1  λ ← |c_0| + ... + |c_{L-1}|;  a ← max(1, ⌈log2 L⌉)
L2  PREP ← a unitary on a qubits with PREP|0^a> = Σ_j sqrt(|c_j|/λ) |j>
L3  SELECT ← Σ_j |j><j| ⊗ sign(c_j) P_j    ▷ the identity for the unused j ≥ L
L4  U ← (PREP^† ⊗ I) · SELECT · (PREP ⊗ I)
L5  return (U, α = λ, a)
```

**Why it works.** Write $|w\rangle = \mathrm{PREP}|0^a\rangle = \sum_j w_j|j\rangle$ with $w_j = \sqrt{|c_j|/\lambda}$. For system states $|\phi\rangle, |\psi\rangle$,
$$\langle 0^a|\langle\phi|\, U\, |0^a\rangle|\psi\rangle = \langle w|\langle\phi|\, \mathrm{SELECT}\, |w\rangle|\psi\rangle = \sum_j w_j^2\, \mathrm{sign}(c_j) \langle\phi|P_j|\psi\rangle = \frac{1}{\lambda}\sum_j c_j \langle\phi|P_j|\psi\rangle,$$
because SELECT keeps the index $j$, so only the diagonal terms $\langle j|\,\cdot\,|j\rangle$ survive. So the top-left block is exactly $H/\lambda$. $U$ is unitary as a product of unitaries.

**How it is used.** Run $U$ on $|0^a\rangle|\psi\rangle$ and measure the ancillas. The state is
$$U|0^a\rangle|\psi\rangle = |0^a\rangle \frac{A}{\alpha}|\psi\rangle + |\perp\rangle, \qquad (\langle 0^a| \otimes I)|\perp\rangle = 0,$$
so the outcome $0^a$ has probability $\|A\psi\|^2/\alpha^2$, and then the system holds $A|\psi\rangle/\|A\psi\|$. Algorithms do not repeat this until success. They interleave $U$, $U^\dagger$ and reflections about $|0^a\rangle$ so that the good part grows, as in [amplitude amplification](/amplitude-amplification/), or so that the block becomes a polynomial in $A/\alpha$, as in [qubitization](/qubitization/) and [quantum signal processing](/quantum-signal-processing/).

**Cost.** PREP prepares a state of $L$ amplitudes, which takes $O(L)$ gates in general. SELECT is $L$ multi-controlled Pauli strings, $O(L \log L)$ gates with the usual unary iteration over the index, or $O(L)$ with more ancillas. One call to $U$ is one call to SELECT and one each to PREP and PREP$^\dagger$. The normalization is $\lambda = \sum_j |c_j|$, the 1-norm of the coefficients, which is at least $\|H\|$ by the triangle inequality. For the Pauli decomposition of $H$ each $|c_j| = |\mathrm{Tr}(P_jH)|/2^n \le \|H\|$, so $\lambda \le L\|H\|$, and both ends occur.

**Example: $H = X + Z$.** Here $L = 2$, $a = 1$, $\lambda = 2$, and $w = (1/\sqrt2, 1/\sqrt2)$, so PREP is the Hadamard gate. With the ancilla as the high qubit, SELECT $= |0\rangle\langle 0| \otimes X + |1\rangle\langle 1| \otimes Z$, and the blocks of $U$ are $(X+Z)/2$, $(X-Z)/2$, $(X-Z)/2$, $(X+Z)/2$:
$$U = \frac12\begin{pmatrix} 1 & 1 & -1 & 1 \\ 1 & -1 & 1 & 1 \\ -1 & 1 & 1 & 1 \\ 1 & 1 & 1 & -1 \end{pmatrix}.$$
The top-left $2 \times 2$ block is $\frac12\begin{pmatrix}1 & 1\\ 1 & -1\end{pmatrix} = H/2$. On $|\psi\rangle = |0\rangle$, $H|0\rangle = |0\rangle + |1\rangle$ has squared norm 2, so the ancilla gives 0 with probability $2/4 = 1/2$, and then the system is in $|{+}\rangle$. Here $\|H\| = \sqrt2 \approx 1.414$, so $\alpha = 2$ wastes a factor $\sqrt2$. The tests in `impl/python` check this matrix entry by entry and check the top-left block against $H/\lambda$ for random Pauli sums on up to 3 qubits.

## Classic examples

- **Pauli sums** (the template): $\alpha = \sum_j |c_j|$, $a = \lceil \log_2 L \rceil$. Since SELECT is Hermitian here, $U$ is Hermitian and $U^2 = I$, which [qubitization](/qubitization/) uses.
- **Sparse matrices with oracle access** (Gilyén, Su, Low and Wiebe, Lemmas 47 and 48). Let $A$ have at most $s$ nonzero entries in each row and column, let $X = \max_{jk}|A_{jk}|$, and let $a_{jk} = A_{jk}/X$. Two state preparations, built from the oracles of [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/), give
$$|L_j\rangle = \frac{1}{\sqrt s}\sum_{k \in \mathrm{row}(j)} |0\rangle|j\rangle|k\rangle, \qquad |R_k\rangle = \frac{1}{\sqrt s}\sum_{j \in \mathrm{col}(k)} \big(a_{jk}|0\rangle + \sqrt{1 - |a_{jk}|^2}\,|1\rangle\big)|j\rangle|k\rangle,$$
on a flag qubit and two registers of $n$ qubits. Then $\langle L_j|R_k\rangle = a_{jk}/s$, so $U = U_L^\dagger U_R$ is a block encoding with $\alpha = sX = s\|A\|_{\max}$ and $a = n + 1$. The construction does not need $A$ to be Hermitian, and negative or complex entries need no shift. For $A = \begin{pmatrix}1 & 0.5\\ 0.5 & -1\end{pmatrix}$, $s = 2$, $X = 1$, $\alpha = 2$, while $\|A\| = \sqrt{1.25} \approx 1.118$.
- **A unitary** is a $(1, 0, 0)$-block-encoding of itself (Definition 44).
- **Density matrices** (Lemma 45). If $G$ prepares a purification of a [density matrix](/density-matrix/) $\rho$, on $a + s$ qubits, then $(G^\dagger \otimes I_s)(I_a \otimes \mathrm{SWAP}_s)(G \otimes I_s)$ is a block encoding of $\rho$ with $\alpha = 1$ and $a + s$ ancillas.
- **Products** (Lemma 53). If $U_A$ encodes $A$ with $(\alpha, a)$ and $U_B$ encodes $B$ with $(\beta, b)$, then $(I_b \otimes U_A)(I_a \otimes U_B)$ on separate ancillas encodes $AB$ with $(\alpha\beta, a + b)$, and errors $\delta$ and $\epsilon$ add to $\alpha\epsilon + \beta\delta$.
- **Linear combinations** (Lemma 52). A PREP on a new index register and a SELECT of the block encodings $U_j$ encode $\sum_j y_j A_j$ with normalization $\sum_j |y_j|\alpha_j$. This is the template again, one level up.
- **Polynomials and functions of $A$.** [Qubitization](/qubitization/), [quantum signal processing](/quantum-signal-processing/) and the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) turn a block encoding of a Hermitian $A$ into a block encoding of $p(A/\alpha)$ for a bounded polynomial $p$, with $\deg p$ calls. This gives $e^{-iHt}$ in [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/).

**Linear systems and the fine print.** The best known use outside simulation is to solve $Ax = b$. The algorithm of Harrow, Hassidim and Lloyd (2009), and its successors by Childs, Kothari and Somma (2017) and by the singular value transformation, apply an approximation of $1/x$ to a block encoding of $A$. An odd polynomial of degree $O(\kappa \log(1/\epsilon))$ approximates $1/x$ on $[-1, -1/\kappa] \cup [1/\kappa, 1]$ (Corollary 69), where $\kappa = \|A\|\,\|A^{-1}\|$ is the [condition number](/condition-number/). Aaronson (2015) lists the conditions under which this is a speedup over classical [linear system solving](/linear-system-solving/):
- $A$ must have a block encoding with small $\alpha$, for example a [sparse matrix](/sparse-matrix/) with an efficient oracle for its nonzero entries. A dense matrix stored as a table has none in general.
- The cost grows linearly with the condition number $\kappa$. Classical methods for well-conditioned sparse systems, such as the [conjugate gradient method](/conjugate-gradient-method/), also improve with small $\kappa$.
- A fast circuit must prepare the state $|b\rangle = \sum_i b_i|i\rangle/\|b\|$. Loading $N$ arbitrary numbers costs about $N$ gates, which removes the speedup.
- The output is the quantum state $|x\rangle \propto A^{-1}|b\rangle$, not the vector $x$. Reading all $N$ entries needs about $N$ repetitions. The method helps only when a few numbers, such as an expectation value $\langle x|M|x\rangle$, are enough.

## Variations

- **Approximate encodings.** An $(\alpha, a, \epsilon)$-block-encoding allows the block to be $\epsilon/\alpha$ away from $A/\alpha$. Errors add under products and sums as in Lemmas 52 and 53, and the transformations of the block keep them small.
- **Asymmetric preparation.** With complex $c_j = |c_j|e^{i\theta_j}$, put the phase into SELECT, or use two different preparations $\mathrm{PREP}_L$ and $\mathrm{PREP}_R$ with $\langle 0|\mathrm{PREP}_L^\dagger|j\rangle\langle j|\mathrm{PREP}_R|0\rangle = c_j/\lambda$. This is the Gram matrix form of Lemma 47.
- **Hermitian encodings.** If $A$ is Hermitian but $U$ is not, one more ancilla and a controlled $U$ or $U^\dagger$ give a Hermitian encoding of the same $A$ with the same $\alpha$ (Low and Chuang, qubitization). Some transformations need this.
- **Projected encodings.** In place of $|0^a\rangle$ on both sides, any two projectors $\tilde\Pi$ and $\Pi$ can be used, and the encoded matrix is $\tilde\Pi U \Pi$. This is the general input of the quantum singular value transformation, with the [singular value decomposition](/singular-value-decomposition/) of the block in place of the eigendecomposition.
- **Better normalization.** For sparse matrices, a preamplified encoding (Lemma 49) uses bounds on the norms of the rows and columns of $A$, in place of $s\|A\|_{\max}$, and can give a smaller $\alpha$ for some more queries. For Pauli sums, grouping terms into fewer, larger unitaries can make $\lambda$ smaller.

## Pitfalls

- **The normalization is part of the cost.** Two block encodings of the same $H$ with $\alpha = \|H\|$ and $\alpha = 10\|H\|$ are not equal: every algorithm that uses them pays in proportion to $\alpha$. Report $\alpha$ with every encoding.
- **Which block.** The convention here puts the ancillas on the high qubits, so the encoded matrix is the top-left block. With the ancillas on the low qubits, the same $\langle 0^a|U|0^a\rangle$ is spread over every $2^a$-th row and column of the matrix. Mixing the two conventions gives a wrong matrix with no error message.
- **Signs and phases of the coefficients.** PREP can only make nonnegative amplitudes $\sqrt{|c_j|/\lambda}$. The sign of $c_j$ must go into SELECT, or the encoded matrix is $\sum_j |c_j|P_j$.
- **The ancillas must start in $|0^a\rangle$.** If they start in another state, the block that acts is a different block of $U$. After a failed run the ancillas must be reset before they are used again.
- **Post-selection is expensive.** Applying $A/\alpha$ once succeeds with probability $\|A\psi\|^2/\alpha^2$. For a product of $k$ encodings this falls like $\alpha^{-2k}$. Use amplitude amplification or a polynomial transformation, not repeated tries.
- **The norm of the block is at most 1.** No unitary has a block of norm larger than 1, so $\alpha \ge \|A\|$ is necessary (Definition 43). A claimed encoding with smaller $\alpha$ has a bug.

## Exercises

1. Build the block encoding of $H = 0.5\,X + 0.3\,Z - 0.2\,Y$ on one qubit with $a = 2$, and check that the top-left block is $H/1$.
2. Show that the template gives a Hermitian $U$ with $U^2 = I$ when PREP is a Householder reflection, as in the code. Then give a PREP with the same first column for which $U$ is not Hermitian, and show that the top-left block is still $H/\lambda$.
3. Show that every block encoding has $\alpha \ge \|A\|$. Hint: the top-left block of a unitary is a contraction.
4. For the sparse construction, explain why the flag qubit is needed only in $|R_k\rangle$ and not in $|L_j\rangle$, and what goes wrong if both carry the factor $\sqrt{|a_{jk}|}$ on the flag with the rest on $|1\rangle$.
5. Prove Lemma 53 for exact encodings: $(\langle 0^{a+b}|\otimes I)(I_b \otimes U_A)(I_a \otimes U_B)(|0^{a+b}\rangle \otimes I) = AB/(\alpha\beta)$.

## References
