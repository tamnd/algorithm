---
tag: MKRGVR
kind: definition
slug: second-quantization
name: Second quantization
aliases:
- occupation number representation
- creation and annihilation operators
area: quantum/quantum-simulation
level: advanced
summary: "Describe identical particles by the occupation numbers of n modes and by the operators a_j^dagger and a_j. For fermions, {a_i, a_j^dagger} = delta_ij and {a_i, a_j} = 0."
prereqs: [quantum-state, tensor-product]
see_also: [fermion-to-qubit-mapping, jordan-wigner-transformation, bravyi-kitaev-transformation, quantum-chemistry-simulation, quantum-many-body-simulation, quantum-field-theory-simulation, pauli-gates, pauli-string-decomposition]
sources:
  - paper: doi:10.1007/BF01331938
    title: "Pascual Jordan and Eugene Wigner, Über das Paulische Äquivalenzverbot, Zeitschrift für Physik 47(9), 1928, pages 631 to 651"
    locator: the anticommuting creation and annihilation operators of fermions and their matrices in the occupation number basis
  - book: isbn:9780471967552
    title: Trygve Helgaker, Poul Jørgensen and Jeppe Olsen, Molecular Electronic-Structure Theory, Wiley, 2000
    locator: Chapter 1 (second quantization), the occupation number vectors, the anticommutation relations and the one- and two-electron operators
  - book: isbn:9780486691862
    title: Attila Szabo and Neil S. Ostlund, Modern Quantum Chemistry, Introduction to Advanced Electronic Structure Theory, Dover, 1996
    locator: Chapter 2 (many-electron wave functions and operators), the section on second quantization
  - paper: doi:10.1063/1.4768229
    title: Jacob T. Seeley, Martin J. Richard and Peter J. Love, The Bravyi-Kitaev transformation for quantum computation of electronic structure, Journal of Chemical Physics 137(22), 2012, article 224109 (arXiv:1208.5986)
    locator: the review of second quantization and the occupation number basis at the start of the paper
  - paper: doi:10.1103/RevModPhys.92.015003
    title: Sam McArdle, Suguru Endo, Alán Aspuru-Guzik, Simon C. Benjamin and Xiao Yuan, Quantum computational chemistry, Reviews of Modern Physics 92(1), 2020, article 015003
    locator: the section on the electronic structure Hamiltonian in second quantization
---

*Second quantization* describes a system of identical particles by the occupation numbers of a fixed list of single-particle states, called *modes* or *orbitals*, and by operators that add a particle to a mode or remove one. For fermions, such as electrons, each mode holds 0 or 1 particles, and the creation operators $a_j^\dagger$ and annihilation operators $a_j$ satisfy the canonical anticommutation relations $\{a_i, a_j^\dagger\} = \delta_{ij}$ and $\{a_i, a_j\} = 0$. The antisymmetry of the many-particle wave function is then built into the operators, and a state is a vector in a space of dimension $2^n$ for $n$ modes. This is the input format of [quantum chemistry simulation](/quantum-chemistry-simulation/) and of fermionic models in [quantum many-body simulation](/quantum-many-body-simulation/). A quantum computer has qubits, not fermions, so these operators must first be rewritten as Pauli sums by a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/). This page is the definition. The mappings are on their own pages.

## Definition

**Modes.** Fix $n$ orthonormal single-particle states $\phi_0, \dots, \phi_{n-1}$. In chemistry they are spin orbitals: a spatial orbital times a spin state, so $K$ spatial orbitals give $n = 2K$ modes. The order of the modes is a choice, and it matters for the signs below.

**Fock space.** For fermions, the *Fock space* $\mathcal F_n$ has the orthonormal basis of *occupation number states*
$$|n_{n-1} \cdots n_1 n_0\rangle, \qquad n_k \in \{0, 1\},$$
where $n_k$ is the number of particles in mode $k$. So $\dim \mathcal F_n = 2^n$. This encyclopedia writes mode 0 at the right end and gives the state the index $x = \sum_k n_k 2^k$, the same convention as for qubits on the [quantum state](/quantum-state/) page. The state with all $n_k = 0$ is the *vacuum* $|\mathrm{vac}\rangle$. The states with $N = \sum_k n_k$ particles span the $N$-particle sector, of dimension $\binom{n}{N}$.

**Annihilation and creation operators.** For each mode $j$, the annihilation operator $a_j$ is the linear map with
$$a_j\, |n_{n-1} \cdots n_0\rangle = \begin{cases} (-1)^{n_0 + n_1 + \cdots + n_{j-1}}\, |n_{n-1} \cdots 0_j \cdots n_0\rangle & \text{if } n_j = 1, \\ 0 & \text{if } n_j = 0. \end{cases}$$
The creation operator $a_j^\dagger$ is its adjoint. It sets $n_j$ from 0 to 1 with the same sign $(-1)^{n_0 + \cdots + n_{j-1}}$, and it maps a state with $n_j = 1$ to 0. The sign counts the occupied modes below $j$. It is the sign that makes the operators anticommute. With these signs,
$$|n_{n-1} \cdots n_0\rangle = (a_0^\dagger)^{n_0} (a_1^\dagger)^{n_1} \cdots (a_{n-1}^\dagger)^{n_{n-1}}\, |\mathrm{vac}\rangle,$$
so a basis state is a product of creation operators in the order of the modes, applied to the vacuum.

**Canonical anticommutation relations (CAR).** With $\{A, B\} = AB + BA$, for all $i$ and $j$,
$$\{a_i, a_j^\dagger\} = \delta_{ij}\, I, \qquad \{a_i, a_j\} = 0, \qquad \{a_i^\dagger, a_j^\dagger\} = 0.$$
These follow from the definition. For $i < j$, the operator $a_j$ sees the occupation of mode $i$ in its sign, and $a_i$ does not see mode $j$. So $a_i a_j$ and $a_j a_i$ differ by exactly one factor $-1$.

**Consequences.**

- *Exclusion.* $(a_j^\dagger)^2 = 0$: a mode cannot hold two fermions. This is the Pauli exclusion principle.
- *Number operators.* $\hat n_j = a_j^\dagger a_j$ is the diagonal projector onto $n_j = 1$, and $a_j a_j^\dagger = I - \hat n_j$. The $\hat n_j$ commute with each other. The total number $\hat N = \sum_j \hat n_j$ counts the particles.
- *Uniqueness.* Up to a unitary change of basis, these are the only operators on a space of dimension $2^n$ that satisfy the CAR. *Proof.* Let $b_0, \dots, b_{n-1}$ satisfy the CAR on a space $V$ of dimension $2^n$. Then $m_j = b_j^\dagger b_j$ are commuting projectors, since $m_j^2 = b_j^\dagger (I - b_j^\dagger b_j) b_j = m_j$. Take a common eigenvector $v$. If $m_j v = v$, then $b_j v$ is again a common eigenvector, with $m_j$ now 0 and the other $m_k$ unchanged, and $\|b_j v\|^2 = \langle v, m_j v\rangle = 1$. After at most $n$ steps this gives a unit vector $\Omega$ with $b_j \Omega = 0$ for all $j$. The $2^n$ vectors $(b_0^\dagger)^{x_0} \cdots (b_{n-1}^\dagger)^{x_{n-1}} \Omega$ have norm 1 and are eigenvectors of the $m_k$ for different eigenvalue patterns, so they are orthonormal. They span $V$ by the count of dimensions. In this basis the $b_j$ act by the formula above. $\square$
- *Parity.* Every operator that is a sum of products of an even number of $a$ and $a^\dagger$ commutes with the parity $(-1)^{\hat N}$. Physical Hamiltonians are of this kind.

**Majorana operators.** The $2n$ Hermitian operators
$$\gamma_{2j} = a_j + a_j^\dagger, \qquad \gamma_{2j+1} = i\,(a_j^\dagger - a_j)$$
satisfy $\{\gamma_k, \gamma_l\} = 2\delta_{kl} I$, and $a_j = (\gamma_{2j} + i\gamma_{2j+1})/2$. Every fermionic operator is a polynomial in the $\gamma_k$. The mappings to qubits are often stated for Majorana operators, because each $\gamma_k$ maps to a single Pauli string.

**Operators in second quantization.** A one-body operator, such as the kinetic energy plus the attraction of the nuclei, and a two-body operator, such as the Coulomb repulsion of the electrons, are
$$\hat h = \sum_{p,q} h_{pq}\, a_p^\dagger a_q, \qquad \hat v = \frac12 \sum_{p,q,r,s} (pq|rs)\, a_p^\dagger a_r^\dagger a_s a_q,$$
where $h_{pq} = \langle \phi_p | h | \phi_q\rangle$ and $(pq|rs)$ is the two-electron integral in the chemists' notation, which is zero unless $p, q$ have the same spin and $r, s$ have the same spin. Their sum is the electronic structure Hamiltonian of [quantum chemistry simulation](/quantum-chemistry-simulation/). It conserves $\hat N$. It has up to $n^2$ one-body and $n^4$ two-body coefficients. For real orbitals the symmetries $(pq|rs) = (qp|rs) = (pq|sr) = (rs|pq)$ leave about $n^4/8$ distinct two-body values.

**Bosons.** For bosons, such as photons or the modes of a scalar field, the operators satisfy the commutation relations $[b_i, b_j^\dagger] = \delta_{ij}$ and $[b_i, b_j] = 0$, with $b|m\rangle = \sqrt m\, |m - 1\rangle$ and no sign. A mode can hold any number $m \ge 0$ of particles, so the Fock space of one mode has infinite dimension. A simulation must cut the occupation off at some $m \le K$. See [quantum field theory simulation](/quantum-field-theory-simulation/).

## Examples and non-examples

**One mode.** In the basis $(|0\rangle, |1\rangle)$, $a = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ and $a^\dagger = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$. Then $a a^\dagger = \mathrm{diag}(1, 0)$, $a^\dagger a = \mathrm{diag}(0, 1)$, and the sum is $I$. Also $a^2 = 0$. The Majorana operators are $\gamma_0 = X$ and $\gamma_1 = Y$, two of the [Pauli gates](/pauli-gates/).

**Two modes and the sign.** In the basis $|00\rangle, |01\rangle, |10\rangle, |11\rangle$ (indices 0 to 3, mode 0 on the right),
$$a_0 = \begin{pmatrix} 0&1&0&0 \\ 0&0&0&0 \\ 0&0&0&1 \\ 0&0&0&0 \end{pmatrix}, \qquad a_1 = \begin{pmatrix} 0&0&1&0 \\ 0&0&0&-1 \\ 0&0&0&0 \\ 0&0&0&0 \end{pmatrix}.$$
The entry $-1$ is the sign: $a_1|11\rangle = (-1)^{n_0}|01\rangle = -|01\rangle$. Check the anticommutator on $|11\rangle$: $a_0 a_1|11\rangle = -a_0|01\rangle = -|00\rangle$ and $a_1 a_0|11\rangle = a_1|10\rangle = |00\rangle$, so $\{a_0, a_1\}|11\rangle = 0$. On the other three basis states both products are 0. As Kronecker products, $a_0 = I \otimes \sigma^-$ and $a_1 = \sigma^- \otimes Z$ with $\sigma^- = |0\rangle\langle 1|$. The factor $Z$ is the start of the [Jordan-Wigner transformation](/jordan-wigner-transformation/).

**Hopping.** $\hat H = -t(a_0^\dagger a_1 + a_1^\dagger a_0)$ moves a particle between two modes. On the one-particle states $(|01\rangle, |10\rangle)$ it is $-t\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, with energies $\pm t$. On $|00\rangle$ and $|11\rangle$ it is 0: in $|11\rangle$ both modes are full, so no particle can move.

**Hydrogen in a minimal basis.** H$_2$ with one bonding and one antibonding spatial orbital has $n = 4$ spin orbitals and 2 electrons. The two-electron sector has $\binom42 = 6$ states, and 4 of them have total spin projection 0. The Hartree-Fock state is $a_{0}^\dagger a_{1}^\dagger|\mathrm{vac}\rangle = |0011\rangle$, the bonding orbital with spin up and spin down. The [quantum chemistry simulation](/quantum-chemistry-simulation/) page solves this Hamiltonian exactly.

**Non-example: operators that commute.** On two qubits, $\sigma^-_0 = I \otimes \sigma^-$ and $\sigma^-_1 = \sigma^- \otimes I$ satisfy $\{\sigma^-_j, (\sigma^-_j)^\dagger\} = I$ on each site, but $\sigma^-_0$ and $\sigma^-_1$ commute instead of anticommuting. They describe hard-core bosons, not fermions. The difference is visible in energies. On a ring of 3 modes with hopping $-1$ between neighbours and 2 particles, fermions have the energies $-1, -1, 2$ and hard-core bosons have $-2, 1, 1$ (exact diagonalization on the [Jordan-Wigner transformation](/jordan-wigner-transformation/) page).

**Non-example: a truncated boson.** Cut one bosonic mode at $m \le 1$. Then $b = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ and $[b, b^\dagger] = \mathrm{diag}(1, -1)$, not $I$. A truncation keeps the commutation relation only on the states well below the cutoff.

## Related definitions

- **[Fermion-to-qubit mapping](/fermion-to-qubit-mapping/).** A unitary from $\mathcal F_n$ to $n$ or more qubits that turns each $a_j$ into a Pauli sum. The [Jordan-Wigner transformation](/jordan-wigner-transformation/) and the [Bravyi-Kitaev transformation](/bravyi-kitaev-transformation/) are the two standard cases.
- **[Tensor product](/tensor-product/).** As a vector space, $\mathcal F_n$ is isomorphic to $(\mathbb C^2)^{\otimes n}$. The operators $a_j$ are not local in this product: by the sign rule, $a_j$ acts on the modes $0, \dots, j$.
- **[Pauli string decomposition](/pauli-string-decomposition/).** After a mapping, a fermionic Hamiltonian is a sum of Pauli strings. The weight of the strings depends on the mapping.
- **First quantization.** The other description writes a state of $N$ particles as an antisymmetric function of $N$ coordinates, for example a Slater determinant. It needs about $N \log_2 n$ qubits for $N$ particles in $n$ modes, against $n$ qubits in second quantization.

## References
