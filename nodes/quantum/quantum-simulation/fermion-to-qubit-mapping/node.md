---
tag: 390342
kind: concept
slug: fermion-to-qubit-mapping
name: Fermion-to-qubit mapping
aliases:
- fermionic encoding
- qubit encoding of fermions
area: quantum/quantum-simulation
level: advanced
summary: "A unitary that stores the 2^n fermionic occupation states of n modes in qubits and turns each a_j into a Pauli sum that keeps the anticommutation relations. The Pauli weight sets the cost."
prereqs: [second-quantization, pauli-gates]
see_also: [jordan-wigner-transformation, bravyi-kitaev-transformation, pauli-string-decomposition, quantum-chemistry-simulation, quantum-many-body-simulation, fenwick-tree, linear-system-modulo-2, digital-quantum-simulation]
sources:
  - paper: doi:10.1007/BF01331938
    title: "Pascual Jordan and Eugene Wigner, Über das Paulische Äquivalenzverbot, Zeitschrift für Physik 47(9), 1928, pages 631 to 651"
    locator: the representation of anticommuting operators by matrices with a string of signs, the first fermion-to-qubit mapping
  - paper: doi:10.1006/aphy.2002.6254
    title: Sergey B. Bravyi and Alexei Yu. Kitaev, Fermionic quantum computation, Annals of Physics 298(1), 2002, pages 210 to 226 (arXiv:quant-ph/0003137)
    locator: the simulation of fermions by qubits with O(log n) overhead per operator, and the local encoding of fermions on a graph
  - paper: doi:10.1063/1.4768229
    title: Jacob T. Seeley, Martin J. Richard and Peter J. Love, The Bravyi-Kitaev transformation for quantum computation of electronic structure, Journal of Chemical Physics 137(22), 2012, article 224109 (arXiv:1208.5986)
    locator: the occupation number, parity and Bravyi-Kitaev bases as linear maps over GF(2), and the update, parity and flip sets
  - paper: doi:10.1103/PhysRevA.95.032332
    title: Vojtěch Havlíček, Matthias Troyer and James D. Whitfield, Operator locality in the quantum simulation of fermionic models, Physical Review A 95(3), 2017, article 032332 (arXiv:1701.07072)
    locator: the Fenwick tree form of the Bravyi-Kitaev mapping for any number of modes
  - paper: doi:10.22331/q-2020-06-04-276
    title: Zhang Jiang, Amir Kalev, Wojciech Mruczkiewicz and Hartmut Neven, Optimal fermion-to-qubit mapping via ternary trees with applications to reduced quantum states learning, Quantum 4, 2020, article 276
    locator: the ternary tree mapping with Majorana weight ceil(log_3(2n + 1)), and the lower bound log_3(2n) on the average Majorana weight
  - paper: doi:10.1103/RevModPhys.92.015003
    title: Sam McArdle, Suguru Endo, Alán Aspuru-Guzik, Simon C. Benjamin and Xiao Yuan, Quantum computational chemistry, Reviews of Modern Physics 92(1), 2020, article 015003
    locator: the section on fermion-to-qubit mappings (Jordan-Wigner, parity and Bravyi-Kitaev) and their Pauli weights
---

A *fermion-to-qubit mapping* stores the states of $n$ fermionic modes in qubits and rewrites every fermionic operator as a sum of Pauli strings. The fermionic operators of [second quantization](/second-quantization/) anticommute on different modes, and the [Pauli gates](/pauli-gates/) on different qubits commute, so the mapping cannot send $a_j$ to an operator on qubit $j$ alone. Each mapping solves this with strings of extra Pauli factors, and the mappings differ in how long the strings are. The [Jordan-Wigner transformation](/jordan-wigner-transformation/) keeps the occupation numbers in the qubits and needs strings of length up to $n$. The [Bravyi-Kitaev transformation](/bravyi-kitaev-transformation/) keeps partial sums of occupation numbers in a tree and needs only $O(\log n)$. Both are cases of one construction, the linear encodings, on this page. The mapping turns a fermionic Hamiltonian into the Pauli list that [Hamiltonian simulation](/hamiltonian-simulation/) takes as input.

## In plain words

A quantum computer has qubits, and a qubit already looks like a fermionic mode: empty or full. The trouble is the sign. When a fermion moves past other fermions, the state picks up a factor $-1$ for each one it passes. Qubits do not do this on their own. So the mapping adds the sign by hand: the operator for mode $j$ also looks at some other qubits and reads off how many fermions it must pass. Where the occupation numbers are stored decides which qubits it must read. Store them plainly and the sign needs many qubits. Store running totals and the change needs many qubits. A tree of partial totals needs only a few qubits for both.

## The idea

**What a mapping must do.** A mapping is a unitary $W$ from the Fock space $\mathcal F_n$ to the space of $m \ge n$ qubits, or to a subspace of it. The image of an operator $A$ is $W A W^\dagger$. Because $W$ is unitary, the images satisfy the canonical anticommutation relations (CAR) $\{a_i, a_j^\dagger\} = \delta_{ij}$ and $\{a_i, a_j\} = 0$ automatically, and they have the same spectrum. Conversely, any $n$ operators on $n$ qubits that satisfy the CAR come from such a $W$ (the uniqueness on the [second quantization](/second-quantization/) page). So a mapping with $m = n$ is the same thing as a choice of $n$ Pauli sums that satisfy the CAR.

**Why the cost is the weight.** Simulation applies $e^{-i\theta P}$ for each Pauli string $P$ of the Hamiltonian. For a string of weight $w$ (the number of letters that are not $I$) this takes $2(w - 1)$ CNOT gates and one rotation (see [digital quantum simulation](/digital-quantum-simulation/)). So the weight of the images sets the gate count, and the number of strings sets the number of rotations. A mapping is good when the images of the Hamiltonian terms have low weight.

**Linear encodings.** Let $f \in \{0, 1\}^n$ be the occupation vector, $f_k = n_k$. A *linear encoding* stores it as $b = \beta f \bmod 2$ for an $n \times n$ matrix $\beta$ that is invertible over GF(2): the basis state $|f\rangle$ of $\mathcal F_n$ becomes the qubit basis state $|b\rangle$. Read off three sets from $\beta$ for each mode $j$:

- $c_j$, the qubits $i$ with $\beta_{ij} = 1$: the qubits that change when $f_j$ changes;
- $r_j$, the qubits in row $j$ of $\beta^{-1}$: the qubits whose sum mod 2 is $f_j$;
- $p_j$, the qubits in the sum mod 2 of rows $0, \dots, j-1$ of $\beta^{-1}$: the qubits whose sum is the sign parity $f_0 + \cdots + f_{j-1}$.

Then, with $X(s)$ and $Z(s)$ the products of $X$ or $Z$ over a set $s$ of qubits,
$$a_j^\dagger = X(c_j)\, Z(p_j)\, \frac{I + Z(r_j)}{2}, \qquad a_j = \frac{I + Z(r_j)}{2}\, Z(p_j)\, X(c_j).$$
*Proof.* Apply the right side to $|b\rangle$ with $b = \beta f$. The factor $(I + Z(r_j))/2$ is the projector onto $f_j = 0$, since $Z(r_j)|b\rangle = (-1)^{f_j}|b\rangle$. The factor $Z(p_j)$ gives $(-1)^{f_0 + \cdots + f_{j-1}}$. The factor $X(c_j)$ maps $b$ to $b \oplus \beta e_j = \beta(f \oplus e_j)$, the encoding of $f$ with mode $j$ filled. This is the definition of $a_j^\dagger$, with its sign. $\square$

Each image is a sum of 2 Pauli strings with coefficients $\pm\frac12$ and $\pm\frac i2$. The three standard encodings are:

| encoding | $\beta$ | qubit $i$ stores | image of $a_j$ | weight |
|---|---|---|---|---|
| Jordan-Wigner | $I$ | $f_i$ | $Z$ on $0, \dots, j-1$; $X, Y$ on $j$ | $j + 1$, up to $n$ |
| parity | lower triangle of ones | $f_0 + \cdots + f_i$ | $Z$ on $j - 1$; $X, Y$ on $j$; $X$ on $j+1, \dots, n-1$ | $n - j + 1$, up to $n$ |
| Bravyi-Kitaev | Fenwick tree | $f$ summed over a block of modes | $O(\log n)$ qubits | $\lfloor \log_2 n \rfloor + 1$ at most |

In the Jordan-Wigner encoding the parity is spread out and the occupation is local. In the parity encoding it is the other way round. The Bravyi-Kitaev encoding stores the sum of $f$ over the blocks of a [Fenwick tree](/fenwick-tree/), so both the update set $c_j$ and the parity set $p_j$ have $O(\log n)$ elements. The tree is on its own page. The last column is the largest weight of the two strings in the image of $a_j$. For Bravyi-Kitaev, $\lfloor \log_2 n\rfloor + 1$ is measured, not proved, on every $n$ from 1 to 129 and on $n = 1000$. The bound $O(\log n)$ is proved by Bravyi and Kitaev (2002).

**Majorana weight and a lower bound.** Each Majorana operator $\gamma_{2j} = a_j + a_j^\dagger$ and $\gamma_{2j+1} = i(a_j^\dagger - a_j)$ maps to a single Pauli string, and the $2n$ strings must pairwise anticommute. Jiang, Kalev, Mruczkiewicz and Neven (2020) build the strings from a ternary tree, with weight $\lceil \log_3(2n + 1) \rceil$ for every Majorana operator. They prove that every mapping of $n$ modes into $n$ qubits has average Majorana weight at least $\log_3(2n)$, so the ternary tree is optimal up to rounding. It is not a linear encoding in the sense above. Logarithmic weight is thus the best possible for an arbitrary operator on $n$ qubits.

**More qubits for local models.** On a lattice, a Hamiltonian has hopping terms only between neighbouring modes. A mapping with more than $n$ qubits can make the image of every such term have constant weight. The second construction of Bravyi and Kitaev (2002) puts one qubit on each edge of the interaction graph. The extra qubits must stay in a subspace fixed by stabilizer constraints. These encodings trade qubits for locality.

## Examples

**Four modes, three encodings.** These are the exact images on 4 qubits. A string is written with qubit 3 first and qubit 0 last.

| | $a_0^\dagger$ | $a_2^\dagger$ | $\hat n_3$ |
|---|---|---|---|
| Jordan-Wigner | $\frac12(IIIX - i\, IIIY)$ | $\frac12(IXZZ - i\, IYZZ)$ | $\frac12(IIII - ZIII)$ |
| parity | $\frac12(XXXX - i\, XXXY)$ | $\frac12(XXZI - i\, XYII)$ | $\frac12(IIII - ZZII)$ |
| Bravyi-Kitaev | $\frac12(XIXX - i\, XIXY)$ | $\frac12(XXZI - i\, XYZI)$ | $\frac12(IIII - ZZZI)$ |

Check the parity row by hand. In the parity encoding, $f_0 = b_0$ and $f_j = b_j + b_{j-1}$. So $a_0^\dagger$ flips $f_0$, which changes every $b_i$: the factor is $XXXX$. Its projector onto $f_0 = 0$ is $(I + Z_0)/2$, and $X_0 Z_0 = -iY_0$ gives the second string. The number operator $\hat n_3 = (I - Z_3 Z_2)/2$ has weight 2, since $f_3 = b_3 + b_2$. In the Bravyi-Kitaev row, qubit 3 stores $f_0 + f_1 + f_2 + f_3$ and qubit 1 stores $f_0 + f_1$, so $\hat n_3$ reads qubits 3, 2 and 1.

**The same spectrum.** Take a random number-conserving Hamiltonian on 4 modes, with hopping $h_{pq}$ and interactions $u_{pq} \hat n_p \hat n_q$ drawn with seed 3. Its 16 eigenvalues agree to $10^{-9}$ under the Jordan-Wigner, parity and Bravyi-Kitaev encodings, under a random invertible $\beta$, and with the matrix built from the definition in the Fock space. The CAR hold exactly for all four encodings on 3 and 4 modes: the Pauli coefficients of every anticommutator are exactly $1$ on the identity or exactly zero.

**The weights grow differently.** The largest weight of the image of $a_j$, over all $j$, computed from the formula above:

| $n$ | Jordan-Wigner | parity | Bravyi-Kitaev |
|---|---|---|---|
| 8 | 8 | 8 | 4 |
| 16 | 16 | 16 | 5 |

The averages over $j$ are $4.5$, $5.375$ and $4$ for $n = 8$, and $8.5$, $9.44$ and $5$ for $n = 16$. The [Bravyi-Kitaev transformation](/bravyi-kitaev-transformation/) page extends the table to $n = 1000$.

**A free qubit from a symmetry.** In the parity encoding, qubit $n-1$ stores $f_0 + \cdots + f_{n-1}$, the parity of the particle number. Every physical Hamiltonian commutes with this parity, so the Hamiltonian acts on qubit $n-1$ only through $Z_{n-1}$, and $Z_{n-1}$ has a fixed value $\pm1$ in each sector. Replace $Z_{n-1}$ by that value and the qubit is gone. The same works for every conserved parity that is stored in one qubit.

## Where it is used

- [Quantum chemistry simulation](/quantum-chemistry-simulation/): the electronic Hamiltonian in a basis of $n$ spin orbitals becomes a Pauli list with $O(n^4)$ terms. Hydrogen in a minimal basis gives 15 Pauli strings on 4 qubits under Jordan-Wigner.
- [Quantum many-body simulation](/quantum-many-body-simulation/): the Hubbard model and other lattice fermion models. In one dimension with nearest-neighbour hopping the Jordan-Wigner strings are short, and in two dimensions they are long unless the mapping adds qubits.
- [Quantum field theory simulation](/quantum-field-theory-simulation/): lattice fermion fields, for example the staggered fermions of the Schwinger model.
- [Pauli string decomposition](/pauli-string-decomposition/): the output of a mapping is a Pauli sum, and all Pauli-based methods, such as the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), [qDRIFT](/qdrift/) and [linear combination of unitaries](/linear-combination-of-unitaries/), take it as input.
- Solving for $\beta^{-1}$ in a linear encoding is a [linear system modulo 2](/linear-system-modulo-2/).

## References
