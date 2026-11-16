---
tag: A6A0K6
kind: model
slug: quantum-query-model
name: Quantum query model
aliases:
- quantum oracle model
area: complexity/communication-and-query-complexity
level: research
summary: "A quantum algorithm reads its input only through a unitary oracle that it can call on a superposition of indices. The cost is the number of oracle calls, and all other gates are free."
prereqs: [query-model, quantum-oracle, quantum-circuit-model]
see_also: [quantum-query-complexity, grover-search, grover-optimality, polynomial-method, quantum-adversary-method, hybrid-argument, ambainis-element-distinctness, triangle-finding]
sources:
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 2 (the quantum query model, bit and phase oracles, Q_E and Q_2)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (the model, the bounds for OR, PARITY and MAJORITY, D(f) = O(Q(f)^6) for total f)
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1997, pages 1510-1523"
    locator: the Omega(sqrt N) bound for search and the oracle result for NP
  - paper: doi:10.1145/3406325.3451047
    title: Scott Aaronson, Shalev Ben-David, Robin Kothari, Shravas Rao and Avishay Tal, Degree vs. approximate degree and quantum implications of Huang's sensitivity theorem, 53rd ACM Symposium on Theory of Computing (STOC 2021)
    locator: pp. 1330 to 1342 (D(f) = O(Q(f)^4) for total f)
  - paper: doi:10.1137/S0097539705447311
    title: Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1) (2007)
    locator: the O(n^(2/3)) algorithm for element distinctness
  - paper: doi:10.1145/1008731.1008735
    title: Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4) (2004)
    locator: pp. 595 to 605 (Omega(n^(2/3)) for element distinctness)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415
    locator: Chapter 11 (quantum query lower bounds)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6 (quantum search, the oracle and the black box limits)
---

The quantum query model is the [query model](/query-model/) for quantum algorithms. The input $x \in \{0,1\}^n$ is held by an oracle, as in the classical model, but the oracle is a unitary map, so the algorithm can ask for many indices at once in superposition. The cost is the number of oracle calls. All other quantum gates are free, and so are the number of qubits and the final measurement. The model is the setting of [quantum query complexity](/quantum-query-complexity/), of [Grover search](/grover-search/), and of the three main lower-bound methods: the [hybrid argument](/hybrid-argument/), the [polynomial method](/polynomial-method/) and the [quantum adversary method](/quantum-adversary-method/).

## The machine

The input is a string $x = x_1 \cdots x_n$ with $x_i \in \{0,1\}$, and the task is a function $f$ of $x$. As on the [query model](/query-model/) page, $f$ is total unless the text says that it is partial, that is, defined only on a promise set $P \subseteq \{0,1\}^n$.

The algorithm works on a register of three parts: an index $i \in \{1, \ldots, n\}$, one answer qubit $b$, and a workspace $w$ of any size. The oracle $O_x$ is the [quantum oracle](/quantum-oracle/) of the string $x$. In the **bit form** it acts on basis states as

$$O_x \, |i, b, w\rangle = |i, b \oplus x_i, w\rangle .$$

In the **phase form** it acts as $O_x^{\pm} |i, b, w\rangle = (-1)^{b \cdot x_i} |i, b, w\rangle$. One form is the other with a [Hadamard gate](/hadamard-gate/) on the answer qubit before and after the call, so the two forms give the same count. The answer qubit $b$ in the phase form acts as a control: on $b = 0$ the call does nothing. Without a control of this kind an algorithm cannot tell $x$ from its complement $\bar x$ in the phase form, which is a loss that has nothing to do with the problem.

An algorithm with $T$ queries is a list of unitary maps $U_0, U_1, \ldots, U_T$ that do not depend on $x$. On input $x$ it starts in the all-zero state and produces

$$|\psi_x^T\rangle = U_T \, O_x \, U_{T-1} \, O_x \cdots U_1 \, O_x \, U_0 \, |0\rangle .$$

Then it measures a fixed output qubit and outputs the result. The algorithm computes $f$ **exactly** if the output is $f(x)$ with probability $1$ on every input in the domain, and with **bounded error** if the probability is at least $2/3$ on every input in the domain. For inputs over a larger alphabet, with $x_i \in \{0, \ldots, m-1\}$, the oracle adds $x_i$ modulo $m$ to an answer register, and the rest of the definition does not change.

A small example shows the gain. Let $f(x_1, x_2) = x_1 \oplus x_2$. Start with the index in the state $(|1\rangle + |2\rangle)/\sqrt 2$ and the control at $b = 1$. One phase query gives $((-1)^{x_1}|1\rangle + (-1)^{x_2}|2\rangle)/\sqrt 2$. A Hadamard gate on the index maps this state to $|1\rangle$ up to sign when $x_1 = x_2$, and to $|2\rangle$ up to sign when $x_1 \neq x_2$. So the measurement gives $f(x)$ with probability $1$ after one query, while every classical algorithm must read both bits. This is Deutsch's problem, the case $n = 2$ of the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/). Applied to the $n/2$ pairs of bits of $x$, it gives an exact algorithm for the parity of $n$ bits with $\lceil n/2 \rceil$ queries.

## What it counts

The only cost is the number $T$ of calls to $O_x$. The maps $U_t$ can be any unitary maps on any number of qubits, and their gate count is not counted. This is the reason that lower bounds in this model are proofs with no assumption: they hold for every quantum algorithm, whatever its gate count. The price is that a query lower bound says nothing about time beyond the number of calls. The gate count of a query algorithm is a separate measure, often called its time complexity.

The measures of a function $f$ in this model are:

| Measure | Correctness | Notes |
|---|---|---|
| $Q_E(f)$ | output $f(x)$ with probability $1$ | the exact quantum query complexity |
| $Q(f)$, also $Q_2(f)$ | output $f(x)$ with probability at least $2/3$ | the bounded-error measure; the default |
| $Q_\varepsilon(f)$ | output $f(x)$ with probability at least $1 - \varepsilon$ | $Q(f) = Q_{1/3}(f)$ |

For each constant $\varepsilon < 1/2$, the measures $Q_\varepsilon(f)$ are within a constant factor of each other: repeat the algorithm $O(\log(1/\varepsilon))$ times and output the majority answer. So $Q(f)$ is the measure that most results use, and the [quantum query complexity](/quantum-query-complexity/) page studies it in detail.

## Relation to other models

**Classical queries.** A classical query is a quantum query on one basis state, and a quantum algorithm can simulate any classical decision tree with the same number of calls. So $Q_E(f) \le D^{dt}(f)$ and $Q(f) \le R(f)$ for every $f$. For total $f$ the gap is at most polynomial: Beals, Buhrman, Cleve, Mosca and de Wolf proved $D^{dt}(f) = O(Q(f)^6)$, and Aaronson, Ben-David, Kothari, Rao and Tal improved this to $D^{dt}(f) = O(Q(f)^4)$ with Huang's [sensitivity theorem](/sensitivity-theorem/). For partial $f$ the gap can be exponential. The [Simon problem](/simon-problem/) has a quantum algorithm with $O(n)$ queries on inputs of size $2^n$, and every classical randomized algorithm needs a number of queries exponential in $n$.

**Circuits and oracles.** A quantum query algorithm with $T$ queries and $G$ other gates is a [quantum circuit](/quantum-circuit-model/) with $G$ gates and $T$ oracle gates. A query lower bound for a function of an oracle therefore gives an oracle result about classes such as [BQP](/bqp/). Bennett, Bernstein, Brassard and Vazirani used the hybrid argument to show that relative to a random oracle, with probability $1$, $\mathsf{NP}$ is not contained in quantum time $o(2^{n/2})$. Results of this kind are [relativized](/relativization/), so they do not settle the unrelativized question.

**Communication.** A quantum query algorithm for $f(x \wedge y)$ or a similar function can be run by two parties who hold $x$ and $y$: each query becomes a short exchange of qubits. This simulation is the link to [quantum communication complexity](/quantum-communication-complexity/).

## Known results in the model

The table gives the bounded-error and exact quantum costs of some standard functions, next to the deterministic and randomized costs. The bounds for OR, PARITY and MAJORITY are from Beals et al.; the bound for element distinctness is from Ambainis (upper) and Aaronson and Shi (lower).

| Function | $D^{dt}$ | $R$ | $Q$ | $Q_E$ |
|---|---|---|---|---|
| OR of $n$ bits | $n$ | $\Theta(n)$ | $\Theta(\sqrt n)$ | $n$ |
| PARITY of $n$ bits | $n$ | $n$ | $\lceil n/2 \rceil$ | $\lceil n/2 \rceil$ |
| MAJORITY of $n$ bits | $n$ | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ |
| [Element distinctness](/element-distinctness-lower-bound/), $n$ items | $n$ | $\Theta(n)$ | $\Theta(n^{2/3})$ | |

The upper bound for OR is [Grover search](/grover-search/). With $N = 64$ and one marked item, $\lfloor (\pi/4)\sqrt{64} \rfloor = 6$ Grover iterations find the item with probability $0.9966$. The matching lower bound is the theorem on [optimality of Grover search](/grover-optimality/). Other algorithms in the model are the [quantum walk algorithm for element distinctness](/ambainis-element-distinctness/), [quantum walk search](/quantum-walk-search/) and the algorithms for [triangle finding](/triangle-finding/).

Three methods give lower bounds in the model:

- The [hybrid argument](/hybrid-argument/) of Bennett, Bernstein, Brassard and Vazirani follows how much the state can change at one query. It gives $\Omega(\sqrt n)$ for search.
- The [polynomial method](/polynomial-method/) of Beals et al. shows that the acceptance probability after $T$ queries is a polynomial of degree at most $2T$ in $x$. So $Q(f)$ is at least half the [approximate degree](/approximate-degree/) of $f$.
- The [quantum adversary method](/quantum-adversary-method/) of Ambainis bounds the progress on pairs of inputs with different values. Its general form with negative weights is tight up to a constant factor for every Boolean function.

## References
