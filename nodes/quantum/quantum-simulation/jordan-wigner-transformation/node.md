---
tag: HV0RT2
kind: technique
slug: jordan-wigner-transformation
name: Jordan-Wigner transformation
aliases:
- Jordan-Wigner mapping
area: quantum/quantum-simulation
level: advanced
summary: "Store occupation n_j in qubit j and map a_j to Z_0...Z_(j-1)(X_j + iY_j)/2. The Z string gives the fermionic sign, so the images obey the anticommutation relations exactly."
prereqs: [second-quantization, fermion-to-qubit-mapping, pauli-gates]
see_also: [bravyi-kitaev-transformation, pauli-string-decomposition, quantum-chemistry-simulation, quantum-many-body-simulation, lieb-robinson-bound, ising-model, trotter-suzuki-product-formulas, digital-quantum-simulation]
sources:
  - paper: doi:10.1007/BF01331938
    title: "Pascual Jordan and Eugene Wigner, Über das Paulische Äquivalenzverbot, Zeitschrift für Physik 47(9), 1928, pages 631 to 651"
    locator: the matrices for anticommuting operators built from a product of sign matrices on the earlier modes
  - paper: doi:10.1063/1.4768229
    title: Jacob T. Seeley, Martin J. Richard and Peter J. Love, The Bravyi-Kitaev transformation for quantum computation of electronic structure, Journal of Chemical Physics 137(22), 2012, article 224109 (arXiv:1208.5986)
    locator: the section on the Jordan-Wigner transformation, the images of the ladder operators and their linear Pauli weight
  - paper: doi:10.1080/00268976.2011.552441
    title: James D. Whitfield, Jacob Biamonte and Alán Aspuru-Guzik, Simulation of electronic structure Hamiltonians using quantum computers, Molecular Physics 109(5), 2011, pages 735 to 750
    locator: the Jordan-Wigner form of the hydrogen molecule Hamiltonian in a minimal basis, and its integrals (Table 2)
  - paper: doi:10.1103/RevModPhys.92.015003
    title: Sam McArdle, Suguru Endo, Alán Aspuru-Guzik, Simon C. Benjamin and Xiao Yuan, Quantum computational chemistry, Reviews of Modern Physics 92(1), 2020, article 015003
    locator: the section on fermion-to-qubit mappings, with the Jordan-Wigner images and the hydrogen example
  - paper: doi:10.1103/PhysRevA.95.032332
    title: Vojtěch Havlíček, Matthias Troyer and James D. Whitfield, Operator locality in the quantum simulation of fermionic models, Physical Review A 95(3), 2017, article 032332 (arXiv:1701.07072)
    locator: the locality of Jordan-Wigner strings for lattice models and the comparison with the Bravyi-Kitaev mapping
---

The *Jordan-Wigner transformation* is the [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) that keeps the occupation number $n_j$ of mode $j$ in qubit $j$. It sends the annihilation operator to
$$a_j \;\mapsto\; Z_0 Z_1 \cdots Z_{j-1}\, \frac{X_j + i Y_j}{2}, \qquad a_j^\dagger \;\mapsto\; Z_0 Z_1 \cdots Z_{j-1}\, \frac{X_j - i Y_j}{2}.$$
The factor $(X_j + iY_j)/2 = |0\rangle\langle 1|$ on qubit $j$ empties the mode. The string of $Z$ gates gives the sign $(-1)^{n_0 + \cdots + n_{j-1}}$ that [second quantization](/second-quantization/) puts on $a_j$. With the Fock index $x = \sum_k n_k 2^k$ of the second quantization page, the transformation is the identity on basis states, so the qubit matrices equal the Fock matrices entry by entry. The image of $a_j$ has Pauli weight $j + 1$, so the strings grow to length $n$. The [Bravyi-Kitaev transformation](/bravyi-kitaev-transformation/) brings this down to $O(\log n)$. Jordan and Wigner (1928) introduced it.

## In plain words

Give each fermionic mode its own qubit: $|0\rangle$ for empty and $|1\rangle$ for full. To remove a fermion from mode $j$, flip qubit $j$ from $|1\rangle$ to $|0\rangle$. Fermions also need a sign: the result gets a factor $-1$ for each full mode with a lower number. A $Z$ gate on a qubit gives exactly $-1$ when that qubit is $|1\rangle$. So put a $Z$ gate on every qubit below $j$, and their product is the sign. The cost is that an operator on mode $j$ touches $j + 1$ qubits.

## When it applies

- The input is an operator on $n$ fermionic modes, written as a sum of products of $a_j$ and $a_j^\dagger$, for example a molecular or lattice Hamiltonian from [second quantization](/second-quantization/).
- The modes have a fixed order $0, 1, \ldots, n-1$. The order changes nothing in the spectrum but sets the length of the strings.
- The output is to be a sum of Pauli strings on $n$ qubits, the input of a [Pauli string decomposition](/pauli-string-decomposition/) based method such as the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/).
- It works best when the terms couple modes that are close in the order: in one dimension, or for operators that conserve the number of particles in a short range of modes.

## The template

A Pauli string is written with qubit $n-1$ first and qubit 0 last, as on the [Pauli string decomposition](/pauli-string-decomposition/) page.

```pseudo id=main
JORDAN-WIGNER(terms, n)
L1  for each term c · a_{j1}^(†) ⋯ a_{jk}^(†)       ▷ hole: the modes in a fixed order 0..n-1
L2    for each factor a_j or a_j†: Z on qubits 0..j-1
L3      on qubit j: (X + iY)/2 for a_j, (X - iY)/2 for a_j†
L4    multiply the factors as Pauli sums            ▷ XY = iZ, YZ = iX, ZX = iY
L5    add c times the product to the result
L6  drop the strings with coefficient 0            ▷ hole: the tolerance
L7  return the Pauli sum                            ▷ hole: the input of a simulation method
```

**Why it works.** Write $S_j = Z_0 \cdots Z_{j-1}$ and $\sigma_j = (X_j + iY_j)/2 = |0\rangle\langle1|_j$, so the image of $a_j$ is $S_j\sigma_j$.

- *Same mode.* $S_j$ commutes with $\sigma_j$ and $S_j^2 = I$. So $\{S_j\sigma_j, (S_j\sigma_j)^\dagger\} = \sigma_j\sigma_j^\dagger + \sigma_j^\dagger\sigma_j = |0\rangle\langle0| + |1\rangle\langle1| = I$, and $(S_j\sigma_j)^2 = \sigma_j^2 = 0$.
- *Two modes $i < j$.* $S_j$ contains $Z_i$, which anticommutes with $\sigma_i$ and $\sigma_i^\dagger$. Every other factor of one image commutes with every factor of the other. So the images of $a_i$ and $a_j^{(\dagger)}$ anticommute.

These are the canonical anticommutation relations. On a basis state, $S_j\sigma_j|x\rangle = (-1)^{n_0 + \cdots + n_{j-1}}|x - 2^j\rangle$ when $n_j = 1$ and 0 otherwise, which is the definition of $a_j$ on $|n\rangle$. So the map is the identity on the Fock basis, and products and sums of images are images of products and sums. In particular the Hamiltonian and its image have the same spectrum.

**Useful images.** For $i < j$, with the strings $S$ cancelled where they overlap:
$$\hat n_j = a_j^\dagger a_j \mapsto \frac{I - Z_j}{2}, \qquad a_i^\dagger a_j + a_j^\dagger a_i \mapsto \frac12\big(X_i X_j + Y_i Y_j\big) Z_{i+1} \cdots Z_{j-1},$$
$$i\big(a_i^\dagger a_j - a_j^\dagger a_i\big) \mapsto \frac12\big(Y_i X_j - X_i Y_j\big) Z_{i+1} \cdots Z_{j-1}.$$
A number operator has weight 1, a number-conserving term between modes $i$ and $j$ has weight $j - i + 1$, and a general term on modes up to $j$ has weight at most $j + 1$.

## Classic examples

- **Three modes.** The images are $a_0 \mapsto \frac12(IIX + i\,IIY)$, $a_1 \mapsto \frac12(IXZ + i\,IYZ)$ and $a_2 \mapsto \frac12(XZZ + i\,YZZ)$. On 3 and 4 modes the Pauli coefficients of every anticommutator come out as exactly $1$ on the identity or exactly 0, and the matrices of the images equal the Fock matrices exactly. The weight of $a_j$ is $j + 1$, checked on 8 and 64 modes. The hopping term $a_0^\dagger a_2 + a_2^\dagger a_0$ on 3 modes is $\frac12(XZX + YZY)$.
- **The XX chain is free fermions.** On a line, $i$ and $j = i + 1$ have no string between them, so $\frac J2(X_iX_{i+1} + Y_iY_{i+1}) = J(a_i^\dagger a_{i+1} + a_{i+1}^\dagger a_i)$. The spin chain is a hopping problem for one fermion at a time, and its time evolution is an $n \times n$ matrix exponential. The [Lieb-Robinson bound](/lieb-robinson-bound/) page uses this to get the exact commutator norm $2|U_{0d}(t)|$ in terms of Bessel functions.
- **The transverse-field Ising chain.** From $a_j^\dagger - a_j \mapsto -iS_jY_j$ and $a_j^\dagger + a_j \mapsto S_jX_j$ one gets $X_jX_{j+1} = (a_j^\dagger - a_j)(a_{j+1}^\dagger + a_{j+1})$ and $Z_j = I - 2\hat n_j$. So $-J\sum X_jX_{j+1} - g\sum Z_j$, which is the [Ising model](/ising-model/) $-J\sum Z_jZ_{j+1} - g\sum X_j$ after a Hadamard gate on every qubit, is quadratic in the fermions. On a ring of $n$ sites the ground energy is $-\sum_k \sqrt{J^2 + g^2 - 2Jg\cos k}$ with $k = \pi(2m - 1)/n$, $m = 1, \ldots, n$. For $n = 6$ and $J = 1$ this gives $-6.384695$, $-7.727407$ and $-12.769389$ at $g = 0.5, 1, 2$, which agree with exact diagonalization of the $64 \times 64$ spin matrix to 6 decimal places.
- **The hydrogen molecule.** In a minimal basis, $H_2$ has 4 spin orbitals. The Jordan-Wigner image of its electronic Hamiltonian, with the integrals of Whitfield, Biamonte and Aspuru-Guzik (2011), is a sum of 15 Pauli strings on 4 qubits: the identity, 4 single $Z$, 6 $ZZ$ pairs and the 4 strings $XXYY$, $YYXX$, $XYYX$, $YXXY$ with coefficients $\mp 0.045322$. Its lowest eigenvalue in the 2-electron singlet sector is $-1.851046$ hartree, or $-1.137270$ with the nuclear repulsion $1/R = 0.713776$ at $R = 1.401$ bohr. See [quantum chemistry simulation](/quantum-chemistry-simulation/).
- **The Hubbard chain.** With spin orbital $2i + s$ for site $i$ and spin $s$, a hop of spin $s$ between sites $i$ and $i+1$ goes from mode $2i + s$ to $2i + 2 + s$ and passes one other mode, so it has weight 3, for example $\frac12(XZX + YZY)$ on qubits $2i+s$ to $2i+s+2$. The interaction $U\hat n_{i\uparrow}\hat n_{i\downarrow}$ becomes $\frac U4(I - Z_{2i})(I - Z_{2i+1})$. For two sites at half filling the spectrum is $\frac12(U - \sqrt{U^2 + 16t^2}), 0, U, \frac12(U + \sqrt{U^2 + 16t^2})$ in the sector $S_z = 0$, and the image reproduces it. See [quantum many-body simulation](/quantum-many-body-simulation/).

## Variations

- **Majorana form.** With $\gamma_{2j} = a_j + a_j^\dagger$ and $\gamma_{2j+1} = i(a_j^\dagger - a_j)$, the images are the single strings $S_jX_j$ and $S_jY_j$. A quadratic Majorana term $i\gamma_p\gamma_q$ is then one Pauli string, which is convenient for rotations $e^{-i\theta P}$.
- **Other mode orders.** On an $L \times L$ lattice, number the sites along rows in a snake. Hops along a row have weight 2, but hops between rows pass about $L$ modes and have weight about $L + 1 = O(\sqrt n)$. For spin orbitals, ordering all spin-up orbitals before all spin-down orbitals makes the interaction $\hat n_{i\uparrow}\hat n_{i\downarrow}$ a $ZZ$ term between far qubits, which costs nothing extra, and hops never cross the other spin.
- **Other encodings.** The parity and [Bravyi-Kitaev](/bravyi-kitaev-transformation/) encodings are the linear encodings with other matrices $\beta$, as on the [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) page. They trade the long parity string for long update strings, or both for $O(\log n)$ strings. Encodings with extra qubits make lattice hops constant weight.
- **Backward use.** Read from right to left, the transformation turns a spin chain into a fermion problem. This is how the XX and transverse-field Ising chains are solved exactly.

## Pitfalls

- **Dropping the string.** The map $a_j \mapsto (X_j + iY_j)/2$ without the $Z$ string gives operators that commute on different modes: hard-core bosons, not fermions. For $H = -\sum (a_i^\dagger a_k + a_k^\dagger a_i)$ over the three bonds of a 3-site ring, the 2-particle spectrum is $-1, -1, 2$ with the string and $-2, 1, 1$ without. The 1-particle sector agrees, which hides the error in small tests.
- **The boundary bond of a ring.** For the bond from mode $n-1$ to mode $0$, the string covers every other mode. With the parity $P = Z_0 \cdots Z_{n-1} = (-1)^N$, the image is $a_0^\dagger a_{n-1} + a_{n-1}^\dagger a_0 \mapsto -\frac12(X_0X_{n-1} + Y_0Y_{n-1})P$. So a periodic spin chain is a fermion chain whose boundary condition depends on the parity of the number of particles. Exact solutions of the transverse-field Ising ring must use the right $k$ values in each parity sector.
- **The string order is the mode order.** Images computed with $Z$ on the modes above $j$ instead of below are also a valid encoding, but they do not match the sign convention of the Fock basis, and mixing the two in one program gives wrong signs.
- **Hermitian conjugate pairs.** A single term $a_i^\dagger a_j$ is not Hermitian, and its image has imaginary coefficients such as $\frac i4 X_iY_j$. They cancel only after the term $a_j^\dagger a_i$ is added. Drop the imaginary parts before adding the conjugate and the Hamiltonian is wrong.
- **Weight is not locality.** In one dimension a nearest-neighbour fermion hop has weight 2, but a two-dimensional model or a molecule in an arbitrary orbital order has terms of weight up to $n$. The rotation $e^{-i\theta P}$ for a string of weight $w$ takes $2(w-1)$ CNOT gates.

## Exercises

1. Compute the image of $a_1^\dagger a_0$ on 2 modes and check that its matrix in the basis $x = n_0 + 2n_1$ has a single entry $1$, at row $2$ and column $1$.
2. Show that $\hat n_i\hat n_j \mapsto \frac14(I - Z_i)(I - Z_j)$ and that the string of $a_i^\dagger a_j$ cancels to $Z_{i+1}\cdots Z_{j-1}$.
3. Derive the image of the boundary bond of a ring in the Pitfalls, using $XZ = -iY$ and $YZ = iX$.
4. Show that $\frac J2(X_iX_{i+1} + Y_iY_{i+1})$ conserves $\sum_k Z_k$, and find its one-particle spectrum on an open chain of $n$ sites.
5. For the spin orbitals $2i + s$ of a Hubbard chain on $L$ sites, find the largest weight of a hopping term. Then do the same for the order with all spin-up orbitals first.

## References
