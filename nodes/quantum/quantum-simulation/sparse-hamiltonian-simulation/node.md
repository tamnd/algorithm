---
tag: 2K4RMK
kind: problem
slug: sparse-hamiltonian-simulation
name: Sparse Hamiltonian simulation
aliases:
- row-sparse Hamiltonian simulation
area: quantum/quantum-simulation
level: advanced
summary: Given oracles for the positions and values of the nonzero entries of a d-sparse Hamiltonian H, build a circuit within e of e^(-iHt). The cost is the number of queries.
prereqs: [hamiltonian-simulation, sparse-matrix]
see_also: [optimal-hamiltonian-simulation, no-fast-forwarding-theorem, block-encoding, qubitization, truncated-taylor-series-simulation, edge-coloring, quantum-query-model, linear-system-solving]
sources:
  - paper: doi:10.1007/s00220-006-0150-x
    title: "Dominic W. Berry, Graeme Ahokas, Richard Cleve and Barry C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270(2), 2007, pages 359 to 371 (arXiv:quant-ph/0508139)"
    locator: "Problem 2 (the column-sparse form of the problem), Lemma 2 (6d^2 one-sparse parts, each with O(log* n) queries), Theorem 2 (the query count of the product formulas) and Theorem 3 (the lower bound linear in the time)"
  - paper: arxiv:quant-ph/0301023
    title: "Dorit Aharonov and Amnon Ta-Shma, Adiabatic quantum state generation and statistical zero knowledge, Proceedings of the 35th ACM STOC, 2003"
    locator: "the section on the simulation of sparse Hamiltonians (decomposition by coloring and the product formula), the first efficient algorithm"
  - paper: doi:10.1145/2591796.2591854
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Exponential improvement in precision for simulating sparse Hamiltonians, Proceedings of the 46th ACM STOC, 2014, pages 283 to 292 (arXiv:1312.1414)"
    locator: "Theorem 1.1 (queries with tau = d^2 max|H| t), Theorem 1.2 (the lower bound in the error) and Lemma 4.4 (d^2 one-sparse parts, each with O(1) queries, by the bipartite trick)"
  - paper: arxiv:1501.01715
    title: "Dominic W. Berry, Andrew M. Childs and Robin Kothari, Hamiltonian simulation with nearly optimal dependence on all parameters, Proceedings of the 56th IEEE FOCS, 2015, pages 792 to 809"
    locator: "equations (1) and (2) (the oracles), Theorem 1 (queries and gates with tau = d max|H| t), Theorem 2 and Lemma 12 (the lower bound in tau and e) and Theorem 3 (the trade-off)"
  - paper: doi:10.22331/q-2019-07-12-163
    title: "Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3, 2019, article 163 (arXiv:1610.06546)"
    locator: "Section 3.2: equation (11) (the oracles), Lemma 6 (the block encoding of a d-sparse Hamiltonian with O(1) queries) and Corollary 15 (the query count for sparse Hamiltonians)"
  - paper: arxiv:0908.4398
    title: "Andrew M. Childs and Robin Kothari, Limitations on the simulation of non-sparse Hamiltonians, Quantum Information and Computation 10(7-8), 2010, pages 669 to 684"
    locator: "the lower bounds for non-sparse Hamiltonians (no generic simulation in time poly(||H t||, log N))"
---

Sparse Hamiltonian simulation is the [Hamiltonian simulation](/hamiltonian-simulation/) problem in the sparse oracle model. The Hamiltonian $H$ is a Hermitian $N \times N$ matrix, $N = 2^n$, with at most $d$ nonzero entries in each row. It is too large to write down, so it is given by two oracles: one gives the positions of the nonzero entries of a row, and one gives the value of an entry. The task is to build a circuit within $\epsilon$ of $e^{-iHt}$, and the cost is the number of queries to the oracles, plus the number of other gates. This model is the one in which most lower bounds for simulation are proved, and in which the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/) holds. This page defines the problem; the algorithms are on their own pages, listed under Known algorithms.

## In plain words

Some quantum systems have a huge number of states, but each state connects directly to only a few others. A table of all the connections would be far too large to store. Instead you get two small programs. You give the first one a state and a number, and it tells you which state that connection goes to. You give the second one two states, and it tells you how strong the connection between them is.

The task is to make a quantum computer move its qubits as the real system would move in a given time, with a small allowed error. The cost is how many times you must call the two programs. The answer depends on the time, on the number of connections of each state, on the strongest connection and on the allowed error. It does not depend on the total number of states.

## Definition

A Hermitian matrix $H \in \mathbb{C}^{N \times N}$ is **$d$-sparse** if every row has at most $d$ nonzero entries (see [sparse matrix](/sparse-matrix/)). Since $H$ is Hermitian, every column then has at most $d$ nonzero entries too. The **max norm** is $\|H\|_{\max} = \max_{j,k}|H_{jk}|$. The **graph of $H$** has a vertex for each basis state $|j\rangle$ and an edge $\{j, k\}$ when $H_{jk} \ne 0$; it has maximum degree at most $d$, plus self-loops for the diagonal.

**Input.**

- An oracle $O_F$ for the positions. For each row $j$ there is a list $f(j, 0), \ldots, f(j, d-1)$ of $d$ distinct column indices that contains every $k$ with $H_{jk} \ne 0$ (when a row has fewer than $d$ nonzero entries, the list is filled with columns where $H_{jk} = 0$). The oracle acts in place,
$$O_F|j\rangle|\ell\rangle = |j\rangle|f(j, \ell)\rangle, \qquad \ell \in \{0, \ldots, d-1\}.$$
- An oracle $O_H$ for the values,
$$O_H|j\rangle|k\rangle|z\rangle = |j\rangle|k\rangle|z \oplus H_{jk}\rangle,$$
where $H_{jk}$ is written in a fixed binary format with enough bits.
- The numbers $d$ and $\Lambda \ge \|H\|_{\max}$, a time $t > 0$ and an error $\epsilon > 0$.

Both oracles are unitary, so the algorithm can call them on superpositions and call their inverses. These are the oracles of Berry, Childs and Kothari (2015, equations (1) and (2)) and of Low and Chuang (2019, equation (11)).

**Output.** A quantum circuit $V$ on the $n$ system qubits and some ancilla qubits that start and end in $|0\rangle$, with calls to $O_F$, $O_H$ and their inverses, such that
$$\|V - e^{-iHt}\| \le \epsilon$$
in the spectral norm on the system (or, for a circuit with measurements, in the diamond norm of the channel, as Berry, Childs and Kothari state it).

**Cost.** The **query complexity** is the number of calls to $O_F$, $O_H$ and their inverses. The **gate complexity** is the number of other one- and two-qubit gates. Both are functions of $n$, $d$, $\Lambda$, $t$ and $\epsilon$. The rescaling $e^{-i(sH)(t/s)} = e^{-iHt}$ shows that the cost depends on $\Lambda$ and $t$ only through $\Lambda t$, and the natural size of the instance is the dimensionless time
$$\tau = d\,\|H\|_{\max}\,t.$$

**Three norms.** They satisfy
$$\|H\|_{\max} \le \|H\| \le d\,\|H\|_{\max}.$$
The first holds because $|H_{jk}| = |\langle j|H|k\rangle| \le \|H\|$. For the second, $\|H\| \le \sqrt{\|H\|_1\|H\|_\infty}$ with the largest column sum $\|H\|_1$ and the largest row sum $\|H\|_\infty$ (see [matrix norms](/matrix-norms/)); for Hermitian $H$ both are equal and at most $d\,\|H\|_{\max}$. So $\tau \ge \|H\|t$, and the two can differ by a factor up to $d$. Older bounds are in terms of $\|H\|t$ or $d^2\|H\|_{\max}t$; the modern bounds use $\tau$. When you compare two results, check which of the three quantities each one uses.

## Variants

- **The column form.** Berry, Ahokas, Cleve and Sanders (2007, Problem 2) use one oracle: on a column index $x$ and a number $i$ it returns the row index $y_i$ of the $i$-th nonzero entry and the value $H_{x, y_i}$. This is the same information as $O_F$ and $O_H$ together. They call a Hamiltonian with an efficient classical procedure for this oracle **row-computable**.
- **In place and out of place.** An out-of-place oracle maps $|j, \ell, z\rangle$ to $|j, \ell, z \oplus f(j, \ell)\rangle$. The in-place $O_F$ above also needs the inverse map from $(j, k)$ back to $\ell$. If the list of each row is sorted, the inverse comes from a [binary search](/binary-search/) with $O(\log d)$ out-of-place queries, so the two models differ by at most this factor.
- **The state version.** Given a circuit that prepares $|\psi\rangle$, output a state within $\epsilon$ of $e^{-iHt}|\psi\rangle$. The lower bounds below hold for this version too, since they use one fixed start state.
- **Time-dependent sparse Hamiltonians.** The oracles also take a time $s$, and the target is the time-ordered exponential. Berry, Childs, Cleve, Kothari and Somma (2014) replace $\|H\|_{\max}$ by $\max_s\|H(s)\|_{\max}$ in the query count. See [time-dependent Hamiltonian simulation](/time-dependent-hamiltonian-simulation/).
- **Local Hamiltonians and Pauli lists.** A term that acts on $k$ qubits is $2^k$-sparse, so a sum of $M$ such terms is $2^kM$-sparse (BCCKS 2014). A Pauli string is 1-sparse, so a [Pauli list](/pauli-string-decomposition/) of $L$ terms is $L$-sparse. Both models are special cases, but the sparse bounds for them are often weaker than the bounds that use their structure, because $d\|H\|_{\max}$ can be much larger than the 1-norm $\lambda = \sum_j|c_j|$.
- **Non-sparse Hamiltonians.** With $d$ close to $N$ the model still makes sense, but Childs and Kothari (2010) show that no generic method runs in time polynomial in $\|Ht\|$ and $\log N$.

## Examples

**A two-qubit instance.** Take $H = X \otimes I + \tfrac{1}{2}\,Z \otimes Z$ on two qubits. Qubit 0 is the least significant bit, the rightmost symbol, so $X$ acts on qubit 1 and flips the index bit of value 2. In the basis $|00\rangle, |01\rangle, |10\rangle, |11\rangle$,
$$H = \begin{pmatrix} 0.5 & 0 & 1 & 0 \\ 0 & -0.5 & 0 & 1 \\ 1 & 0 & -0.5 & 0 \\ 0 & 1 & 0 & 0.5 \end{pmatrix}.$$
Each row has two nonzero entries, so $d = 2$, with $f(j, 0) = j$ (the diagonal) and $f(j, 1) = j \oplus 2$. The max norm is $\|H\|_{\max} = 1$. The two terms anticommute, so $H^2 = (1 + 0.25)I = 1.25\,I$ and $\|H\| = \sqrt{1.25} \approx 1.118$, between $\|H\|_{\max} = 1$ and $d\|H\|_{\max} = 2$. From $H^2 = 1.25\,I$,
$$e^{-iHt} = \cos(\sqrt{1.25}\,t)\,I - i\,\frac{\sin(\sqrt{1.25}\,t)}{\sqrt{1.25}}\,H.$$
At $t = 1$ the state $|00\rangle$ goes to $(0.4375 - 0.4022i)|00\rangle - 0.8043i\,|10\rangle$, with probabilities $0.3531$ and $0.6469$; at $t = 2$ the probabilities are $0.5048$ and $0.4952$. Here $\tau = 2t$, while the older parameter $d^2\|H\|_{\max}t$ is $4t$.

**One-sparse Hamiltonians.** If $d = 1$, the graph of $H$ is a set of isolated vertices (with self-loops) and isolated edges, so $H$ is a direct sum of $1 \times 1$ and $2 \times 2$ blocks. For example
$$H = \begin{pmatrix} 0.7 & 0 & 0 & 0 \\ 0 & 0 & w & 0 \\ 0 & \bar w & 0 & 0 \\ 0 & 0 & 0 & -0.2 \end{pmatrix}, \qquad w = 0.6 + 0.8i,\ |w| = 1,$$
gives, at $t = 1$, the phases $e^{-0.7i} = 0.7648 - 0.6442i$ on $|0\rangle$ and $e^{0.2i} = 0.9801 + 0.1987i$ on $|3\rangle$, and on $\{|1\rangle, |2\rangle\}$ the block
$$\cos 1\,I - i\sin 1\begin{pmatrix} 0 & w \\ \bar w & 0 \end{pmatrix} = \begin{pmatrix} 0.5403 & 0.6732 - 0.5049i \\ -0.6732 - 0.5049i & 0.5403 \end{pmatrix}.$$
A circuit finds the partner $f(j, 0)$ and the value with a constant number of queries, applies the $2 \times 2$ rotation, and uncomputes. The number of queries does not grow with $t$, so 1-sparse Hamiltonians can be fast-forwarded. Every sparse method reduces to this case (see Reductions).

**The hypercube.** $H = \sum_{i=0}^{n-1} X_i$ is $n$-sparse with $\|H\|_{\max} = 1$, and its graph is the $n$-dimensional hypercube. Here $\|H\| = n = d\|H\|_{\max}$, so the upper bound on the norm is reached. The terms commute and $e^{-iHt} = \bigotimes_i e^{-iX_it}$, so $n$ one-qubit rotations simulate it for any $t$. At $t = \pi/2$, $|0\cdots 0\rangle$ goes to $(-i)^n|1\cdots 1\rangle$; for $n = 3$ and $t = \pi/4$ all 8 basis states have probability $0.125$. Structure such as this makes some sparse Hamiltonians easy; the problem asks for a method that works without it.

**The parity path.** The Hamiltonian in the proof of the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/) is 2-sparse: it is a path of $N + 1$ vertices whose edges are rerouted by the bits of a hidden string. Its evolution for time $\pi$ writes the parity of the string into one qubit, so any method that simulates all 2-sparse Hamiltonians quickly would compute parity quickly.

## Known algorithms

The algorithms are on their own pages or on the pages of their methods. Query counts for a $d$-sparse $H$ on $n$ qubits, with $\tau = d\|H\|_{\max}t$:

| year | authors | method | queries |
|---|---|---|---|
| 2003 | Aharonov and Ta-Shma | coloring into 1-sparse parts and the [Lie-Trotter product formula](/lie-trotter-product-formula/) | $\mathrm{poly}(n, d)\,(\|H\|t)^2/\epsilon$ |
| 2007 | Berry, Ahokas, Cleve and Sanders | $6d^2$ parts and [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) formulas of order $2k$ | $O\big(5^{2k}d^2\log^*n\,(d^2\|H\|t)^{1+1/(2k)}/\epsilon^{1/(2k)}\big)$ |
| 2010, 2012 | Childs; Berry and Childs | phase estimation on a discrete-time quantum walk | $O(\tau/\sqrt{\epsilon})$ |
| 2014 | Berry, Childs, Cleve, Kothari and Somma | fractional queries, [linear combination of unitaries](/linear-combination-of-unitaries/) | $O\big(\tau_2\log(\tau_2/\epsilon)/\log\log(\tau_2/\epsilon)\big)$ with $\tau_2 = d^2\|H\|_{\max}t$ |
| 2015 | Berry, Childs, Cleve, Kothari and Somma | [truncated Taylor series simulation](/truncated-taylor-series-simulation/) | the same, with $\tau_2$ |
| 2015 | Berry, Childs and Kothari | a linear combination of quantum walk steps | $O\big(\tau\log(\tau/\epsilon)/\log\log(\tau/\epsilon)\big)$ |
| 2017, 2019 | Low and Chuang | [quantum signal processing](/quantum-signal-processing/) and [qubitization](/qubitization/) on the walk; see [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) | $O\big(\tau + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/\tau)\big)$ |

Notes on the table:

- The product formula bounds use $\|H\|t$ and the factor $\log^* n$ (the [iterated logarithm](/iterated-logarithm/)), which comes from the coloring step. Berry, Childs, Cleve, Kothari and Somma (2014, Lemma 4.4) remove that factor.
- Berry, Childs and Kothari (2015, Theorem 1) also count gates: $O\big(\tau\,[n + \log^{5/2}(\tau/\epsilon)]\,\log(\tau/\epsilon)/\log\log(\tau/\epsilon)\big)$. Their Theorem 3 gives the trade-off $O(\tau^{1 + \alpha/2} + \tau^{1 - \alpha/2}\log(1/\epsilon))$ for $\alpha \in (0, 1]$.
- Low and Chuang state the last row as $O(\tau + \log(1/\epsilon)/\log\log(1/\epsilon))$. That form is not correct for all parameters; the form in the table is Corollary 60 of Gilyén, Su, Low and Wiebe (2019) with $\alpha = d\|H\|_{\max}$. The details are on the page of [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/).
- The query counts from 2014 on do not depend on $n$. The gate counts do, through the arithmetic on the indices.

## Bounds

- **Linear in the time.** For every $N$ there is a 2-sparse, row-computable $H$ such that simulation for time $t$ with $\|H\|t = \pi N/2$ to precision $1/4$ needs at least $\|H\|t/(2\pi)$ queries (Berry, Ahokas, Cleve and Sanders 2007, Theorem 3). So no method uses $o(\|H\|t)$ queries for all sparse $H$. This is the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/).
- **Linear in $\tau$.** Berry, Childs and Kothari (2015, Lemma 12) replace each vertex of that Hamiltonian by $d$ copies and get a $2d$-sparse $H$ with $\|H\|_{\max} = \Theta(1)$ that needs $\Omega(dt)$ queries. So the factor $d$ in $\tau$ is needed, not only the factor $t$.
- **In the error.** For every $\epsilon > 0$ there is a 2-sparse $H$ with $\|H\|_{\max} < 1$ whose simulation for a constant time to precision $\epsilon$ needs $\Omega(\log(1/\epsilon)/\log\log(1/\epsilon))$ queries (Berry, Childs, Cleve, Kothari and Somma 2014, Theorem 1.2).
- **Together.** For every $\epsilon, t > 0$, $d \ge 2$ and value of $\|H\|_{\max}$ there is a $d$-sparse $H$ that needs $\Omega(\tau + \log(1/\epsilon)/\log\log(1/\epsilon))$ queries (Berry, Childs and Kothari 2015, Theorem 2). The upper bound of the last row of the table matches the sharper combined lower bound of the same paper up to constant factors, so the query complexity of the problem is known up to a constant for all parameters.
- **Gates.** The lower bounds count queries only. For gate counts with an explicit Hamiltonian there is no unconditional bound of this kind. Atia and Aharonov (2017) show that a method that fast-forwards all physically realizable Hamiltonians would give BQP = PSPACE.
- **Without sparsity.** For dense $H$ with bounded $\|H\|$, no generic method runs in time $\mathrm{poly}(\|Ht\|, \log N)$ (Childs and Kothari 2010).

## Reductions

- **To a block encoding.** With $O(1)$ queries to $O_F$ and $O_H$ one builds a [block encoding](/block-encoding/) of $H/(d\|H\|_{\max})$ (Low and Chuang 2019, Lemma 6; Gilyén, Su, Low and Wiebe 2019, Lemma 48, with the normalization $\sqrt{s_rs_c}$ for $s_r$-row-sparse and $s_c$-column-sparse matrices with entries of size at most 1). So every algorithm for the block encoding model, with $\alpha = d\|H\|_{\max}$, solves the sparse problem, and $\alpha t = \tau$. This is why $\tau$ is the natural parameter.
- **To sums of 1-sparse Hamiltonians.** An [edge coloring](/edge-coloring/) of the graph of $H$ splits $H$ into one 1-sparse part for each color, and each 1-sparse part is simulated in closed form (see Examples). The diagonal is one more 1-sparse part. An edge coloring with $d + 1$ colors exists by [Vizing's theorem](/vizing-theorem/), but the simulation methods do not use it. They need a coloring in which a few local queries give the color of an edge, and they pay with more colors. Berry, Ahokas, Cleve and Sanders (2007, Lemma 2) use a local coloring with $6d^2$ colors and $O(\log^* n)$ queries for each color. Berry, Childs, Cleve, Kothari and Somma (2014, Lemma 4.4) first replace $H$ by the bipartite $X \otimes H$, with $e^{-i(X \otimes H)t}|{+}\rangle|\psi\rangle = |{+}\rangle e^{-iHt}|\psi\rangle$, and color the edge from $u$ on the left to $v$ on the right by the pair (rank of $v$ in the list of $u$, rank of $u$ in the list of $v$). This uses $d^2$ colors and two queries for each color.
- **From parity.** The [parity problem](/parity-problem/) on $N$ bits reduces to the simulation of a 2-sparse Hamiltonian for time $\Theta(N)$, which gives the lower bounds above.
- **From quantum circuits.** Local Hamiltonians are sparse, so the decision form of sparse Hamiltonian simulation is [BQP](/bqp/)-hard by the clock construction of the [Hamiltonian simulation](/hamiltonian-simulation/) page. For a row-computable $H$ with $\tau$ polynomial in $n$, the algorithms above put it in BQP.

## Applications

- **Continuous-time quantum walks.** A walk on a graph with an adjacency oracle is the evolution $e^{-iAt}$ of a sparse adjacency matrix $A$. Algorithms that are defined by such walks, for example on glued trees and for the evaluation of NAND formulas, become circuits by sparse simulation. See also [quantum walk search](/quantum-walk-search/).
- **Linear systems.** Quantum algorithms for [linear system solving](/linear-system-solving/) with a [sparse](/sparse-linear-systems/) matrix $A$ use $e^{-iAt}$ or a block encoding of $A$. Their fine print (the [condition number](/condition-number/), the preparation of the right-hand side, and an output that is a state, not the vector) is on the page of [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/).
- **Physical Hamiltonians.** Chemistry and lattice Hamiltonians in a basis where each state couples to few others are sparse; see [quantum chemistry simulation](/quantum-chemistry-simulation/).
- **Phase estimation.** Controlled-$e^{-iHt}$ for a sparse $H$ inside [quantum phase estimation](/quantum-phase-estimation/) estimates its eigenvalues, the [phase estimation problem](/phase-estimation-problem/) for sparse matrices.

## References
