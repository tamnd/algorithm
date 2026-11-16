---
tag: M7MNKD
kind: definition
slug: bqp
name: BQP
aliases:
- bounded-error quantum polynomial time
area: complexity/complexity-classes
level: advanced
summary: The decision problems that uniform polynomial-size quantum circuits decide with error at most 1/3 on every input. It contains BPP and factoring and lies inside PP.
prereqs: [bpp, quantum-circuit-model]
see_also: [bpp, pp, qma, quantum-turing-machine, factoring-in-bqp, grover-optimality, simon-problem, solovay-kitaev-theorem]
sources:
  - paper: doi:10.1137/S0097539796300921
    title: Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5), 1411 to 1473 (1997)
    locator: the definition of BQP for quantum Turing machines, BPP in BQP in PSPACE, and the recursive Fourier sampling oracle
  - paper: doi:10.1137/S0097539795293639
    title: Leonard M. Adleman, Jonathan DeMarrais and Ming-Deh A. Huang, Quantum computability, SIAM Journal on Computing 26(5), 1524 to 1540 (1997)
    locator: the inclusion of BQP in PP
  - paper: doi:10.1137/S0097539795293172
    title: Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5), 1484 to 1509 (1997)
    locator: the main theorems (factoring and discrete logarithms in quantum polynomial time)
  - paper: doi:10.1137/S0097539796300933
    title: Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1510 to 1523 (1997)
    locator: the random-oracle result that NP is not in quantum time o(2^(n/2))
  - paper: doi:10.1006/jcss.1999.1651
    title: Lance Fortnow and John Rogers, Complexity limitations on quantum computation, Journal of Computer and System Sciences 59(2), 240 to 252 (1999)
    locator: the result that BQP is low for PP and the oracle with P = BQP and an infinite polynomial hierarchy
  - paper: doi:10.1145/3530258
    title: Ran Raz and Avishay Tal, Oracle separation of BQP and PH, Journal of the ACM 69(4), article 30 (2022)
    locator: the main theorem (an oracle relative to which BQP is not in PH)
  - paper: arxiv:quant-ph/0205115
    title: Yaoyun Shi, Both Toffoli and controlled-NOT need little help to do universal quantum computation (2002)
    locator: the theorem that Toffoli and any basis-changing real one-qubit gate are universal
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press (2010)
    locator: Chapter 4, Quantum circuits (universal gate sets and approximation)
  - paper: doi:10.1109/SFCS.1993.366852
    title: Andrew Chi-Chih Yao, Quantum circuit complexity, 34th Annual Symposium on Foundations of Computer Science, 352 to 361 (1993)
    locator: the simulation of quantum Turing machines by polynomial-size quantum circuits
  - paper: doi:10.1098/rspa.2005.1546
    title: Scott Aaronson, Quantum computing, postselection, and probabilistic polynomial-time, Proceedings of the Royal Society A 461(2063), 3473 to 3482 (2005)
    locator: the theorem PostBQP = PP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 10, Quantum computation (the definition of BQP and its relation to classical classes)
---

BQP (bounded-error quantum polynomial time) is the class of decision problems that a uniform family of polynomial-size [quantum circuits](/quantum-circuit-model/) decides with error at most $1/3$ on every input. It is the quantum analogue of [BPP](/bpp/), and it is the usual formal meaning of "the problems that a quantum computer solves efficiently". BQP contains BPP and the decision versions of integer factoring and discrete logarithm, and it lies inside [PP](/pp/) and so inside [PSPACE](/pspace/). Whether $\mathsf{BPP} = \mathsf{BQP}$ and whether $\mathsf{NP} \subseteq \mathsf{BQP}$ are open.

## Definition

**Model.** Fix the gate set $\{H, \mathrm{Toff}\}$, where $H$ is the one-qubit Hadamard gate and $\mathrm{Toff}$ is the three-qubit Toffoli gate, which flips the target bit when both control bits are $1$. A circuit acts on $m$ qubits, starts in a basis state, applies the gates in order, and at the end measures the first qubit in the computational basis. Toffoli and Hadamard together are universal for quantum computation with real amplitudes (Shi 2002), and real amplitudes are enough for BQP.

**Uniformity.** A family $\{C_n\}$ of circuits is polynomial-time uniform if a deterministic [multitape Turing machine](/multitape-turing-machine/) outputs the description of $C_n$ on input $1^n$ in time polynomial in $n$. So $C_n$ has polynomial size. Without uniformity, the family could contain an undecidable language in its wiring.

**Definition.** A language $L$ is in $\mathsf{BQP}$ if there is a polynomial-time uniform family $\{C_n\}$ of circuits over $\{H, \mathrm{Toff}\}$ such that for every input $x$ of length $n$, when $C_n$ runs on $|x\rangle|0 \cdots 0\rangle$ and the first qubit is measured:

$$x \in L \Rightarrow \Pr[\text{outcome } 1] \ge 2/3, \qquad x \notin L \Rightarrow \Pr[\text{outcome } 1] \le 1/3.$$

**Robustness.**

- *The constant $1/3$.* As for BPP, run the circuit $k$ times on fresh qubits and take the majority. The error falls exponentially in $k$, so any constant in $(0, 1/2)$, and even $1/2 - 1/q(n)$ for a polynomial $q$, gives the same class.
- *The gate set.* Any finite universal gate set whose gates have efficiently computable entries gives the same class. By the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/), each gate of one set is approximated within $\varepsilon$ by $O(\log^c(1/\varepsilon))$ gates of the other, for a constant $c$. Errors of approximation add up at most linearly over the gates (a [hybrid argument](/hybrid-argument/)): for a circuit of $T$ gates the final states differ in norm by at most $T\varepsilon$, and each output probability by at most $2T\varepsilon$. So $\varepsilon = 1/(20T)$ changes the probabilities by at most $1/10$.
- *The machine model.* Bernstein and Vazirani (1997) defined BQP with [quantum Turing machines](/quantum-turing-machine/). Yao (1993) showed that a function computed in polynomial time by a quantum Turing machine has polynomial-size quantum circuits. With the converse simulation of uniform circuits by a machine, the two definitions give the same class.

## Examples and non-examples

**Every problem in BPP.** A Toffoli gate with its target set to $1$ computes NAND, so Toffoli gates simulate any classical circuit reversibly, with extra work bits. A Hadamard gate on $|0\rangle$ followed by measurement gives a fair coin, and the deferred-measurement principle moves every measurement to the end. So $\mathsf{BPP} \subseteq \mathsf{BQP}$, and $\mathsf{P} \subseteq \mathsf{BQP}$ in particular.

**Factoring and discrete logarithm.** The language $\{(N, k) : N$ has a prime factor at most $k\}$ is in BQP by [Shor's algorithm](/shor-algorithm/) (Shor 1997), and so is the decision version of the [discrete logarithm problem](/discrete-logarithm-problem/). See [factoring in BQP](/factoring-in-bqp/) and [discrete logarithm in BQP](/discrete-logarithm-in-bqp/). Both problems are in $\mathsf{NP} \cap \mathsf{coNP}$, and neither is known to be in BPP.

**Oracle problems.** Relative to oracles, quantum circuits do more than classical ones. [Simon's problem](/simon-problem/) gives an oracle relative to which BQP has a language outside BPP, with an exponential gap in queries. Bernstein and Vazirani (1997) gave an earlier superpolynomial separation by recursive Fourier sampling. Raz and Tal (2019) gave an oracle relative to which BQP is not contained in the [polynomial hierarchy](/polynomial-hierarchy/).

**BQP is in PP: a sum over paths.** In a circuit over $\{H, \mathrm{Toff}\}$, a Toffoli gate maps basis states to basis states, and a Hadamard gate maps $|b\rangle$ to $(|0\rangle + (-1)^b|1\rangle)/\sqrt{2}$. A path is a choice of the output bit at each of the $h$ Hadamard gates; it has sign $-1$ to the power of the number of Hadamard gates with input $1$ and output $1$. If $P_y$ paths with sign $+1$ and $M_y$ paths with sign $-1$ end in the basis state $y$, the final amplitude of $y$ is $(P_y - M_y)/2^{h/2}$, and

$$\Pr[\text{outcome } 1] = \frac{1}{2^h} \sum_{y : y_1 = 1} (P_y - M_y)^2.$$

The sum counts pairs of paths that end in the same $y$ with $y_1 = 1$, with $+1$ for pairs of equal sign and $-1$ for pairs of opposite sign. A nondeterministic polynomial-time machine can guess a pair of paths and compute their signs, so $2^h \Pr[\text{outcome } 1] - 2^{h-1}$ is the difference of two numbers of accepting paths. Asking whether such a difference is positive is a PP question. So $\mathsf{BQP} \subseteq \mathsf{PP}$ (Adleman, DeMarrais and Huang 1997). The same sum can be computed path by path in polynomial space, which gives $\mathsf{BQP} \subseteq \mathsf{PSPACE}$ (Bernstein and Vazirani 1997).

For example, take three qubits $a, b, c$ in state $|000\rangle$ and apply $H(a)$, $H(b)$, $\mathrm{Toff}(a, b \to c)$, $H(a)$, $H(b)$. There are $h = 4$ Hadamard gates and $16$ paths:

| final $abc$ | $000$ | $001$ | $010$ | $011$ | $100$ | $101$ | $110$ | $111$ |
|---|---|---|---|---|---|---|---|---|
| paths with sign $+1$ | 3 | 1 | 2 | 0 | 2 | 0 | 1 | 1 |
| paths with sign $-1$ | 0 | 0 | 1 | 1 | 1 | 1 | 2 | 0 |
| amplitude | $3/4$ | $1/4$ | $1/4$ | $-1/4$ | $1/4$ | $-1/4$ | $-1/4$ | $1/4$ |

Paths cancel in $010$, $100$ and $110$. The probability that $c = 1$ is $(1 + 1 + 1 + 1)/16 = 1/4$, the probability that the first two Hadamard gates produced $a = b = 1$. The direct computation of the state vector gives the same amplitudes.

**Non-examples and open cases.**

- *NP-complete problems.* No NP-complete problem is known to be in BQP. Relative to a random oracle, NP is not contained in quantum time $o(2^{n/2})$ with probability $1$ (Bennett, Bernstein, Brassard and Vazirani 1997). So a quantum algorithm for SAT that treats the formula as a black box can gain at most the square-root speedup of [Grover's search](/grover-search/), which is optimal ([Grover optimality](/grover-optimality/)).
- *A wrong picture.* A quantum computer does not try all certificates in parallel and read off the good one. A measurement gives one outcome, with the probability given by the squared amplitude; the useful algorithms arrange interference so that wrong answers cancel.
- *Graph isomorphism.* The [graph isomorphism problem](/graph-isomorphism-problem/) is not known to be in BQP. It reduces to a hidden subgroup problem over a non-abelian group, while Shor's algorithm solves the case of abelian groups.
- *Undecidable problems.* $\mathsf{BQP} \subseteq \mathsf{PSPACE}$, so quantum computers decide no more languages than classical ones; they may only decide some faster.
- *Limits relative to oracles.* Fortnow and Rogers (1999) showed that BQP is low for PP, that is, $\mathsf{PP}^{\mathsf{BQP}} = \mathsf{PP}$, and gave an oracle relative to which $\mathsf{P} = \mathsf{BQP}$ while the polynomial hierarchy is infinite.

## Related definitions

- [BPP](/bpp/): the classical analogue, and a subset of BQP.
- [PP](/pp/): contains BQP. With postselection, quantum polynomial time equals PP (Aaronson 2005).
- [QMA](/qma/): the quantum analogue of NP and MA, with a quantum proof and a BQP verifier.
- [Quantum Turing machine](/quantum-turing-machine/) and [quantum circuit model](/quantum-circuit-model/): the two equivalent models.
- [Quantum query model](/quantum-query-model/): the model of the oracle results above.

## References
