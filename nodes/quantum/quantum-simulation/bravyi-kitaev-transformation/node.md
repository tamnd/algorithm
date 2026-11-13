---
tag: P3HDKS
kind: technique
slug: bravyi-kitaev-transformation
name: Bravyi-Kitaev transformation
aliases:
- Bravyi-Kitaev mapping
- binary tree fermion mapping
area: quantum/quantum-simulation
level: advanced
summary: "Store in each qubit the parity of a block of modes from a Fenwick tree. Then a_j touches O(log n) qubits: its ancestors, a prefix of blocks and qubit j, against n for Jordan-Wigner."
prereqs: [jordan-wigner-transformation, fenwick-tree]
see_also: [fermion-to-qubit-mapping, second-quantization, pauli-string-decomposition, quantum-chemistry-simulation, quantum-many-body-simulation, bit-manipulation, segment-tree, digital-quantum-simulation]
sources:
  - paper: doi:10.1006/aphy.2002.6254
    title: Sergey B. Bravyi and Alexei Yu. Kitaev, Fermionic quantum computation, Annals of Physics 298(1), 2002, pages 210 to 226 (arXiv:quant-ph/0003137)
    locator: the encoding of n modes in n qubits with O(log n) qubits per fermionic operator, for n a power of 2
  - paper: doi:10.1063/1.4768229
    title: Jacob T. Seeley, Martin J. Richard and Peter J. Love, The Bravyi-Kitaev transformation for quantum computation of electronic structure, Journal of Chemical Physics 137(22), 2012, article 224109 (arXiv:1208.5986)
    locator: the update, parity and flip sets, the image of a_j with the remainder set, and the hydrogen Hamiltonian in the Bravyi-Kitaev basis
  - paper: doi:10.1103/PhysRevA.95.032332
    title: Vojtěch Havlíček, Matthias Troyer and James D. Whitfield, Operator locality in the quantum simulation of fermionic models, Physical Review A 95(3), 2017, article 032332 (arXiv:1701.07072)
    locator: Section II (the Bravyi-Kitaev transformation as a Fenwick tree, for any number of modes)
  - paper: doi:10.22331/q-2020-06-04-276
    title: Zhang Jiang, Amir Kalev, Wojciech Mruczkiewicz and Hartmut Neven, Optimal fermion-to-qubit mapping via ternary trees with applications to reduced quantum states learning, Quantum 4, 2020, article 276
    locator: the ternary tree mapping and the lower bound log_3(2n) on the average Majorana weight
  - paper: doi:10.1103/RevModPhys.92.015003
    title: Sam McArdle, Suguru Endo, Alán Aspuru-Guzik, Simon C. Benjamin and Xiao Yuan, Quantum computational chemistry, Reviews of Modern Physics 92(1), 2020, article 015003
    locator: the section on fermion-to-qubit mappings, with the Bravyi-Kitaev encoding and its O(log n) weight
---

The *Bravyi-Kitaev transformation* is the [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) whose qubits store partial sums of the occupation numbers, arranged as a [Fenwick tree](/fenwick-tree/). Qubit $i$ holds the parity of the modes $k$ with $i - \mathrm{lowbit}(i + 1) < k \le i$, where $\mathrm{lowbit}(m) = m \mathbin{\&} (-m)$ is the lowest set bit. The fermionic sign of mode $j$ is then a Fenwick prefix query over $O(\log n)$ qubits, and filling mode $j$ is a Fenwick point update of $O(\log n)$ qubits. So each $a_j$ maps to two Pauli strings of weight $O(\log n)$, where the [Jordan-Wigner transformation](/jordan-wigner-transformation/) needs up to $n$. Bravyi and Kitaev (2002) gave the encoding for $n$ a power of 2, Seeley, Richard and Love (2012) gave the sets used here, and Havlíček, Troyer and Whitfield (2017) showed that the Fenwick tree gives it for every $n$.

## In plain words

The Jordan-Wigner encoding writes down which modes are full. Then the sign for mode $j$, which counts the full modes below $j$, needs all those qubits. The opposite choice writes down the running totals. Then the sign is in one qubit, but adding a fermion changes every running total above it. The Bravyi-Kitaev encoding stores totals over blocks of sizes $1, 2, 4, \ldots$, as a Fenwick tree does with sums of an array. A count below $j$ adds up a few blocks, and a change at $j$ touches the few blocks that contain $j$. Both are about $\log_2 n$ qubits.

## When it applies

- The input is a fermionic operator on $n$ modes, given in terms of $a_j$ and $a_j^\dagger$, as for the [Jordan-Wigner transformation](/jordan-wigner-transformation/).
- The terms couple modes far apart in the order, as in a molecule, where the Jordan-Wigner strings would be long.
- Any $n \ge 1$ works. The tree of Bravyi and Kitaev is complete only for $n$ a power of 2. The Fenwick form drops the qubits $\ge n$ and keeps the rest.
- The aim is a Pauli sum with short strings, for example as input for the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), where a string of weight $w$ costs $2(w - 1)$ CNOT gates per rotation.

## The template

Index the Fenwick tree from 1: node $i = j + 1$ belongs to mode $j$ and to qubit $j$. A Pauli string is written with qubit $n-1$ first.

```pseudo id=main
BRAVYI-KITAEV(terms, n)
L1  U(j) ← qubits i-1 for i = j+1 + lowbit(j+1), then i += lowbit(i), while i ≤ n
L2  P(j) ← qubits i-1 for i = j, then i -= lowbit(i), while i > 0
L3  F(j) ← the children of node j+1 in P(j); R(j) ← P(j) \ F(j)
L4  a_j ← ½ X_U(j) (X_j Z_P(j) + i Y_j Z_R(j)),  a_j† ← ½ X_U(j) (X_j Z_P(j) - i Y_j Z_R(j))
L5  for each term c · word: multiply the images of its factors
L6    add c times the product to the result
L7  drop the zero strings and return the Pauli sum      ▷ hole: the input of a simulation method
```

The three sets have plain meanings:

- the *update set* $U(j)$ holds the qubits other than $j$ that store $n_j$: the ancestors of node $j + 1$;
- the *parity set* $P(j)$ holds qubits whose sum is $n_0 + \cdots + n_{j-1}$: the Fenwick prefix query;
- the *flip set* $F(j)$ holds the qubits whose sum with $n_j$ is qubit $j$: the children of node $j+1$, which are $j - 1, j - 2, j - 4, \ldots$ down to a block of size $\mathrm{lowbit}(j+1)/2$.

**Why it works.** The encoding is linear, $b = \beta f \bmod 2$, with $\beta_{ik} = 1$ exactly when $i - \mathrm{lowbit}(i+1) < k \le i$. The general formula of the [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) page is $a_j^\dagger = X(c_j)\,Z(p_j)\,(I + Z(r_j))/2$ with three sets read off $\beta$. Here $c_j = \{j\} \cup U(j)$ is column $j$ of $\beta$, $p_j = P(j)$ gives the sign, and $r_j = \{j\} \cup F(j)$ gives $n_j = b_j + \sum_{F(j)} b$. Expand the projector. Since $F(j) \subseteq P(j)$, the factor $Z(P)\,Z(F)$ is $Z(R)$, and $X_jZ_j = -iY_j$:
$$a_j^\dagger = \tfrac12 X_{U(j)}\big(X_j Z_{P(j)} + X_jZ_j\, Z_{P(j)} Z_{F(j)}\big) = \tfrac12 X_{U(j)}\big(X_j Z_{P(j)} - iY_j Z_{R(j)}\big).$$
The images satisfy the anticommutation relations because the encoding is a unitary on the basis states.

**Why the weight is logarithmic.** Take $n = 2^k$ and $j < n - 1$. Write node $i = j + 1$ as $i = m\,2^{t+1} + 2^t$. Then $|P(j)|$ is the number of ones of $j = m\,2^{t+1} + 2^t - 1$, which is $\mathrm{ones}(m) + t$. Each step $i \mathrel{+}= \mathrm{lowbit}(i)$ moves the lowest set bit to the next zero above it, so $|U(j)|$ is the number of zeros among the $k - t - 1$ bits of $m$, plus one for the root. The sum is $|U(j)| + |P(j)| + 1 = k + 1$. For $j = n - 1$, $U$ is empty and $|P| = k$. So for $n = 2^k$ the first string of every image has weight exactly $k + 1$, and the second has weight $k + 1 - t \le k + 1$. For other $n$, embed the tree in the next power of 2: $P(j)$ does not change and $U(j)$ only loses qubits. This proves the weight bound $\lceil \log_2 n\rceil + 1$. The sharper value $\lfloor \log_2 n\rfloor + 1$ is measured, not proved, on every $n$ from 1 to 129 and on $n = 1000$.

## Classic examples

- **The sets on 8 modes.**

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| qubit $j$ stores modes | 0 | 0..1 | 2 | 0..3 | 4 | 4..5 | 6 | 0..7 |
| $U(j)$ | 1, 3, 7 | 3, 7 | 3, 7 | 7 | 5, 7 | 7 | 7 | none |
| $P(j)$ | none | 0 | 1 | 2, 1 | 3 | 4, 3 | 5, 3 | 6, 5, 3 |
| $F(j)$ | none | 0 | none | 2, 1 | none | 4 | none | 6, 5, 3 |

  For $j = 5$, node 6 is $110_2$. The prefix query from node 5 visits nodes 5 and 4, which are qubits 4 and 3. Qubit 4 stores $n_4$ and qubit 3 stores $n_0 + n_1 + n_2 + n_3$, so their sum is the parity below mode 5.

- **Four modes, exact images.** With $\beta = [[1,0,0,0],[1,1,0,0],[0,0,1,0],[1,1,1,1]]$ (row $i$ is qubit $i$):
$$a_0 = \tfrac12(XIXX + i\,XIXY),\quad a_1 = \tfrac12(XIXZ + i\,XIYI),\quad a_2 = \tfrac12(XXZI + i\,XYZI),\quad a_3 = \tfrac12(XZZI + i\,YIII).$$
  The anticommutation relations hold exactly for $n = 3, 4, 5$: the Pauli coefficients of each anticommutator are exactly 1 on the identity or 0. The matrices equal the Fock matrices after the change of basis $b = \beta f$ for $n = 1$ to $5$. On a random number-conserving Hamiltonian on 4 modes, drawn with seed 7, the spectrum agrees with Jordan-Wigner and with the Fock matrix to $10^{-9}$.

- **Number operators.** $\hat n_j \mapsto \frac12(I - Z_jZ_{F(j)})$. On 8 modes the even modes give weight 1, and $\hat n_7 \mapsto \frac12(I - Z_7Z_6Z_5Z_3)$ has weight 4.

- **The hydrogen molecule.** The minimal basis Hamiltonian of $H_2$ on 4 spin orbitals has 15 Pauli strings under both encodings. Under Bravyi-Kitaev the hopping part is $0.045322\,(IXZX + IYZY + ZXZX + ZYZY)$, the other 11 strings are products of $Z$, and the lowest eigenvalue is $-1.851046$ hartree, the same as under Jordan-Wigner. See [quantum chemistry simulation](/quantum-chemistry-simulation/).

- **The weight table.** The largest weight of the image of any $a_j$:

| $n$ | $\log_2 n$ | Jordan-Wigner | Bravyi-Kitaev |
|---|---|---|---|
| 4 | 2 | 4 | 3 |
| 8 | 3 | 8 | 4 |
| 16 | 4 | 16 | 5 |
| 64 | 6 | 64 | 7 |
| 128 | 7 | 128 | 8 |
| 1000 | 9.97 | 1000 | 10 |

  For a hop $a_i^\dagger a_k + a_k^\dagger a_i$ over all pairs, the largest weight is $n$ for Jordan-Wigner and 5, 7, 9 for Bravyi-Kitaev at $n = 8, 16, 32$.

## Variations

- **The parity encoding.** Qubit $i$ stores $n_0 + \cdots + n_i$. The sign is one $Z$, but the update set is every qubit above $j$. Bravyi-Kitaev sits between it and Jordan-Wigner.
- **Ternary trees.** Jiang, Kalev, Mruczkiewicz and Neven (2020) map the $2n$ Majorana operators to strings of weight $\lceil \log_3(2n + 1)\rceil$, using a tree with three children per node. They prove that no mapping of $n$ modes into $n$ qubits does better on average than $\log_3(2n)$.
- **Encodings with extra qubits.** The second construction of Bravyi and Kitaev (2002) puts qubits on the edges of the interaction graph, so that each hop on the graph has constant weight. It uses more qubits than modes and a stabilizer constraint on the extra space.
- **Other trees.** Any rooted tree on the modes, with each qubit storing the parity of its subtree, gives a valid linear encoding with weights set by the depth and the number of children. The Fenwick tree is the one with $O(\log n)$ in both the update and the prefix direction.

## Pitfalls

- **$R$ and not $P$ in the $Y$ term.** The second string has $Z$ on $R(j) = P(j) \setminus F(j)$. Using $Z_{P(j)}$ in both strings gives operators that still satisfy $\{a_j, a_j^\dagger\} = I$ but fail the relations between different modes. On 4 modes, $\{a_0, a_1\}$ is then $\frac12(IIZX + i\,IIZY)$ and not 0.
- **Off-by-one in the tree.** The Fenwick tree is indexed from 1, the qubits from 0. Mode $j$ is node $j+1$, the update set starts at $j + 1 + \mathrm{lowbit}(j+1)$, and the parity query starts at node $j$, not $j + 1$.
- **The basis changes.** The basis state $|f\rangle$ of occupations becomes $|\beta f\rangle$, not $|f\rangle$. A Hartree-Fock state with modes 0 and 1 full on 4 modes is the qubit state with $b = (1, 0, 0, 0)$ for $b_0, \ldots, b_3$, since qubit 1 and qubit 3 store $n_0 + n_1 = 0 \bmod 2$. Preparing $|f\rangle$ directly gives the wrong state.
- **Short in the worst case, not always shorter.** On a line, the Jordan-Wigner image of a nearest-neighbour hop always has weight 2. The Bravyi-Kitaev image does not: on 8 modes the hops $(j, j+1)$ have weights 2, 3, 3, 5, 2, 3, 4. Count the CNOT gates for the actual Hamiltonian before choosing.

## Exercises

1. Compute $U(j)$, $P(j)$ and $F(j)$ for $n = 16$ and $j = 10$, and check that $|U| + |P| + 1 = 5$.
2. Show that $F(j) \subseteq P(j)$ and that $\sum_{F(j)} b + b_j = n_j$.
3. Derive $a_3 = \frac12(XZZI + i\,YIII)$ on 4 modes from the general formula, and explain why the second string has no $Z$ on qubits 1 and 2.
4. For $n = 6$, write $\beta$ and the image of $a_5$. Compare its weight with $\lfloor\log_2 6\rfloor + 1$.
5. Find the Bravyi-Kitaev basis state for the occupation $f = (1, 1, 0, 0, 0, 0, 0, 0)$ on 8 modes.

## References
