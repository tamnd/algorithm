---
tag: HXRPV7
kind: theorem
slug: no-fast-forwarding-theorem
name: No fast-forwarding theorem
aliases:
- Berry-Childs-Kothari no fast-forwarding
area: quantum/quantum-simulation
level: research
summary: "No method simulates every 2-sparse Hamiltonian for time t with o(t) queries: the evolution can compute the parity of N bits, which needs N/2 queries (Berry, Ahokas, Cleve and Sanders 2007)."
prereqs: [hamiltonian-simulation, sparse-hamiltonian-simulation, parity-problem]
see_also: [optimal-hamiltonian-simulation, qubitization, higher-order-trotter-suzuki, truncated-taylor-series-simulation, polynomial-method, quantum-query-complexity, grover-optimality, quantum-signal-processing]
sources:
  - paper: doi:10.1007/s00220-006-0150-x
    title: "Dominic W. Berry, Graeme Ahokas, Richard Cleve and Barry C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270(2), 2007, pages 359 to 371 (arXiv:quant-ph/0508139)"
    locator: "Section IV (linear limit on simulation time): Theorem 3, its proof with the spin N/2 path and Fig. 1, and Corollary 1 (no general integrator)"
  - paper: arxiv:1501.01715
    title: "Dominic W. Berry, Andrew M. Childs and Robin Kothari, Hamiltonian simulation with nearly optimal dependence on all parameters, Proceedings of the 56th IEEE FOCS, 2015, pages 792 to 809"
    locator: "Section 4 (lower bound): Lemma 12 (the 2d-sparse Hamiltonian that needs Omega(td) queries), Theorem 2 and its proof, and the combined bound with e < |sin(td/N)|^N / 2"
  - paper: doi:10.1145/2591796.2591854
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Exponential improvement in precision for simulating sparse Hamiltonians, Proceedings of the 46th ACM STOC, 2014, pages 283 to 292 (arXiv:1312.1414)"
    locator: "Theorem 1.2 and Section 6 (the lower bound in the error from unbounded-error parity)"
  - paper: doi:10.1145/502090.502097
    title: "Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4), 2001, pages 778 to 797"
    locator: "the degree lower bound and its application to parity (N/2 queries)"
  - paper: doi:10.1103/PhysRevLett.81.5442
    title: "Edward Farhi, Jeffrey Goldstone, Sam Gutmann and Michael Sipser, Limit on the speed of quantum computation in determining parity, Physical Review Letters 81(24), 1998, page 5442"
    locator: "the whole paper (N/2 queries for parity with error probability below 1/2)"
  - paper: arxiv:0908.4398
    title: "Andrew M. Childs and Robin Kothari, Limitations on the simulation of non-sparse Hamiltonians, Quantum Information and Computation 10(7-8), 2010, pages 669 to 684"
    locator: "the extension of no fast-forwarding to dense Hamiltonians"
  - paper: doi:10.1038/s41467-017-01637-7
    title: "Yosi Atia and Dorit Aharonov, Fast-forwarding of Hamiltonians and exponentially precise measurements, Nature Communications 8, 2017 (arXiv:1610.09619)"
    locator: "the definition of fast-forwarding, the fast-forwardable classes (commuting local and quadratic fermionic Hamiltonians) and the result that general fast-forwarding would give BQP = PSPACE"
  - paper: doi:10.22331/q-2019-07-12-163
    title: "Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3, 2019, article 163 (arXiv:1610.06546)"
    locator: "Theorem 1, its footnotes on the lower bound, and Corollary 15 (the matching upper bound for sparse Hamiltonians)"
---

The no-fast-forwarding theorem says that there is no general method that simulates sparse Hamiltonians for time $t$ with a number of queries that grows more slowly than $t$. Berry, Ahokas, Cleve and Sanders proved it in 2007: they built a 2-sparse Hamiltonian whose evolution for time $\pi$ computes the parity of $N$ hidden bits, and parity needs $N/2$ quantum queries. So the cost of [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/) is at least linear in the time, and the algorithms whose cost is $O(\tau)$ plus a term in the error are optimal. The alias "Berry-Childs-Kothari no fast-forwarding" refers to the 2015 strengthening by Berry, Childs and Kothari, who added the sparsity $d$ and, with an earlier result of Berry, Childs, Cleve, Kothari and Somma, the error; the original theorem is the one of Berry, Ahokas, Cleve and Sanders.

## Statement

**Model.** The model is the sparse oracle model of [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/). A query to $H$ returns the positions and values of the nonzero entries of one row (or column). A Hamiltonian is **row-computable** if a classical procedure computes these entries efficiently. Here $H$ depends on a hidden string $x \in \{0, 1\}^N$, and a query to $H$ is built from queries to the bits of $x$. The precision is the trace distance between the output state and the ideal state $e^{-iHt}|\psi_0\rangle$ for a fixed start state $|\psi_0\rangle$. An error $\|V - e^{-iHt}\| \le \epsilon$ in the spectral norm gives trace distance at most $\epsilon$, so the theorem holds also for that error measure.

**Theorem (Berry, Ahokas, Cleve and Sanders 2007, Theorem 3).** For every positive integer $N$ there is a row-computable 2-sparse Hamiltonian $H$ on $2(N + 1)$ basis states such that simulating the evolution of $H$ for the scaled time $\tau = \|H\|t = \pi N/2$ within trace distance $1/4$ needs at least $\tau/(2\pi) = N/4$ queries to $H$.

The Hamiltonian has $\|H\| = N/2$ and evolves for $t = \pi$. Dividing it by $N/2$ gives the same statement in a form with a fixed norm:

**Corollary (norm 1).** For every positive integer $N$ there is a 2-sparse $H$ with $\|H\| = 1$ and $\|H\|_{\max} < 1$ (for $N \ge 2$) such that simulating it for time $t = \pi N/2$ within $1/4$ needs at least $t/(2\pi)$ queries. So no method simulates all 2-sparse Hamiltonians of norm at most 1 for time $t$ with $o(t)$ queries.

Two hypotheses matter. First, the number of basis states grows with $\tau$: the instance has about $\log_2 N + 2$ qubits with $N = 2\tau/\pi$. With a fixed dimension, a method could read the whole matrix with a fixed number of queries and then compute $e^{-iHt}$ exactly for any $t$, so the theorem says nothing there. Second, the bound is on queries for a method that must work for every $H$ of the class, not on gates for one explicit $H$.

**Example.** The core of the construction is the path Hamiltonian on $|0\rangle, \ldots, |N\rangle$ with
$$\langle j + 1|H|j\rangle = \langle j|H|j + 1\rangle = \tfrac{1}{2}\sqrt{(N - j)(j + 1)}.$$
Starting from $|0\rangle$, the probability of $|j\rangle$ at time $t$ is the binomial $\binom{N}{j}\sin^{2j}(t/2)\cos^{2(N-j)}(t/2)$ (proved below). For $N = 4$:

| $t$ | $P(0)$ | $P(1)$ | $P(2)$ | $P(3)$ | $P(4)$ |
|---|---|---|---|---|---|
| $\pi/4$ | 0.5308 | 0.3643 | 0.0937 | 0.0107 | 0.0005 |
| $\pi/2$ | 0.0625 | 0.25 | 0.375 | 0.25 | 0.0625 |
| $\pi$ | 0 | 0 | 0 | 0 | 1 |

At $t = \pi$ the whole state has moved to the far end. The amplitude of $|4\rangle$ is $|\sin(t/2)|^4$ in absolute value: $0.0528$ at $t = 1$ and $0.5014$ at $t = 2$. For the bits $x = (1, 0, 1, 1)$, with parity 1, the augmented Hamiltonian of the proof moves $|0, 0\rangle$ along $|1, 1\rangle, |1, 2\rangle, |0, 3\rangle$ to $|1, 4\rangle$, and at $t = \pi$ the whole weight is on $|1, 4\rangle$, so the first register holds the parity.

## In plain words

Imagine a chain of $N + 1$ stations and a quantum particle that starts at the first one. The links between the stations have strengths chosen so that, after a fixed time, the particle arrives at the last station exactly. Now make two copies of the chain, and at each link keep the copies apart or let them cross, as a hidden bit says. The particle then ends in the first or the second copy of the last station, and which copy it is tells whether the number of crossings is odd or even.

So a cheap run of the particle would give the parity of the hidden bits cheaply. But a quantum computer must look at half of the bits to learn their parity. Since the chain is about as long as the time, the cost of the simulation must grow at least as fast as the time.

## Proof

**Step 1: the path is a spin.** Let $\bar X = \sum_{i=1}^{N}X_i$ on $N$ qubits and let $|w_k\rangle = \binom{N}{k}^{-1/2}\sum_{|y| = k}|y\rangle$ be the normalized uniform superposition of the strings of Hamming weight $k$. Each string of weight $k$ goes under $\bar X$ to $k$ strings of weight $k - 1$ and $N - k$ strings of weight $k + 1$. A string of weight $k + 1$ is reached from $k + 1$ strings of weight $k$, so
$$\bar X\sum_{|y| = k}|y\rangle = (k + 1)\sum_{|y| = k+1}|y\rangle + (N - k + 1)\sum_{|y| = k-1}|y\rangle.$$
With $\binom{N}{k+1}/\binom{N}{k} = (N - k)/(k + 1)$ and $\binom{N}{k-1}/\binom{N}{k} = k/(N - k + 1)$ this becomes
$$\tfrac{1}{2}\bar X|w_k\rangle = \tfrac{1}{2}\sqrt{(N - k)(k + 1)}\,|w_{k+1}\rangle + \tfrac{1}{2}\sqrt{k(N - k + 1)}\,|w_{k-1}\rangle.$$
So the span of the $|w_k\rangle$ is invariant under $\bar X/2$, and the map $|k\rangle \mapsto |w_k\rangle$ carries the path Hamiltonian $H$ of the example to $\bar X/2$ on that span. Since $e^{-iX\theta} = \cos\theta\,I - i\sin\theta\,X$, the product
$$e^{-i\bar Xt/2}|0\cdots 0\rangle = \big(\cos(t/2)|0\rangle - i\sin(t/2)|1\rangle\big)^{\otimes N}$$
has amplitude $\binom{N}{k}^{1/2}\cos^{N-k}(t/2)\,(-i\sin(t/2))^k$ on $|w_k\rangle$, which gives the binomial law of the example. At $t = \pi$ every factor is $-i|1\rangle$, so
$$e^{-i\pi H}|0\rangle = (-i)^N|N\rangle.$$
The eigenvalues of $\bar X/2$ on the symmetric span are $N/2, N/2 - 1, \ldots, -N/2$ (the span is the spin $N/2$ representation, and $H$ is its $J_x$), so $\|H\| = N/2$.

**Step 2: the parity graph.** Let $x = (x_1, \ldots, x_N)$ be the hidden bits. The augmented Hamiltonian acts on $|k, j\rangle$ with $k \in \{0, 1\}$ and $j \in \{0, \ldots, N\}$, and its nonzero entries are
$$\langle k', j + 1|H_x|k, j\rangle = \langle k, j|H_x|k', j + 1\rangle = \tfrac{1}{2}\sqrt{(N - j)(j + 1)} \quad\text{for } k \oplus k' = x_{j+1}.$$
If $x_{j+1} = 0$ the step from $j$ to $j + 1$ stays in the same copy; if $x_{j+1} = 1$ it crosses. The graph is two disjoint paths. Let $k_0 = 0$ and $k_{j+1} = k_j \oplus x_{j+1}$, so $k_j = x_1 \oplus \cdots \oplus x_j$. The states $|k_j, j\rangle$ form the path that contains $|0, 0\rangle$, and on their span $H_x$ acts as the path Hamiltonian of Step 1 acts on $|j\rangle$. This span is invariant, so Step 1 gives
$$e^{-i\pi H_x}|0, 0\rangle = (-i)^N|k_N, N\rangle, \qquad k_N = x_1 \oplus \cdots \oplus x_N.$$
Berry, Ahokas, Cleve and Sanders write this as $|k_N, N\rangle$, without the phase $(-i)^N$. The phase is global and changes nothing in the argument.

**Step 3: the cost of a query.** Each vertex $|k, j\rangle$ has at most two neighbors, $|k \oplus x_j, j - 1\rangle$ and $|k \oplus x_{j+1}, j + 1\rangle$, so $H_x$ is 2-sparse, and the entries are given by a simple formula, so it is row-computable. To answer a query about row $(k, j)$ a circuit needs only $x_j$ and $x_{j+1}$. The entry between two given vertices needs only the one bit of the step between them, and the $\ell$-th neighbor of a given vertex needs only one of $x_j$ and $x_{j+1}$. A reversible query to $H_x$ therefore costs at most two queries to the bits: one query writes the needed bit into an ancilla, the answer is computed from it, and a second query erases the ancilla. Berry, Ahokas, Cleve and Sanders also count at most two bit queries for each query to $H_x$.

**Step 4: parity is hard.** Any quantum algorithm that outputs the parity of $N$ bits with error probability less than $1/2$ on every input makes at least $N/2$ queries (Farhi, Goldstone, Gutmann and Sipser 1998; Beals, Buhrman, Cleve, Mosca and de Wolf 2001). By the [polynomial method](/polynomial-method/), after $q$ queries the probability of output 1 is a real polynomial of degree at most $2q$ in the bits, and $p(x) - 1/2$ has the sign of the parity only if the degree is $N$. See the [parity problem](/parity-problem/).

**Step 5: together.** Suppose a simulation of $H_x$ for time $\pi$ from $|0, 0\rangle$ makes $q$ queries to $H_x$ and outputs a state $\rho$ within trace distance $1/4$ of the ideal state $|k_N, N\rangle\langle k_N, N|$. Measure the first register of $\rho$. The ideal state gives $k_N$ with certainty, and the probability of an event changes by at most the trace distance, so the outcome is wrong with probability at most $1/4 < 1/2$. With Step 3 this is an algorithm for parity with at most $2q$ bit queries, so $2q \ge N/2$ by Step 4, and $q \ge N/4$. Since $\|H_x\| = N/2$ and $t = \pi$, $\tau = \pi N/2$ and $N/4 = \tau/(2\pi)$. $\blacksquare$

For the corollary, $H' = (2/N)H_x$ has $\|H'\| = 1$ and $e^{-iH'\pi N/2} = e^{-i\pi H_x}$, with the same queries. Its largest entry is $\max_j\sqrt{(N - j)(j + 1)}/N \le (N + 1)/(2N)$, which is less than 1 for $N \ge 2$ (for $N = 4$ it is $0.6124$). For a time $t$ that is not of the form $\pi N/2$, take $N = \lfloor 2t/\pi\rfloor$ and scale $H'$ by $\pi N/(2t) \le 1$.

## Consequences

- **Linear time is optimal.** A general method for sparse Hamiltonians needs $\Omega(\|H\|t)$ queries. The methods of [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) and [qubitization](/qubitization/) use $O(\tau)$ queries plus a term in the error, so they are optimal in the time. The product formulas of order $2k$ (see [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/)) use $(\|H\|t)^{1+1/(2k)}$ times other factors, which Berry, Ahokas, Cleve and Sanders note is close to the bound for large $k$.
- **No general integrator.** Write $H_x = H_1 + H_2$, with $H_1$ the edges from even $j$ and $H_2$ the edges from odd $j$. Both are 1-sparse and each is simulated with two bit queries for any time. So no integrator that depends only on $\tau$ and calls exponentials of $H_1$ and $H_2$ reaches trace distance $1/4$ with fewer than $\tau/(2\pi)$ exponentials (Berry, Ahokas, Cleve and Sanders 2007, Corollary 1). This holds for every splitting method, such as the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), however high the order.
- **The quantity that sets the cost.** In the query model the cost is at least linear in $\|H\|t$, and the best upper bounds do not depend on the number of qubits at all. This is why bounds are stated in the dimensionless time $\tau$ (see [Hamiltonian simulation](/hamiltonian-simulation/)).
- **Fast-forwarding is special.** Some classes have $e^{-iHt}$ at a cost that does not grow with $t$: 1-sparse Hamiltonians (two queries, see the [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/) examples), sums of commuting local terms, and quadratic fermionic Hamiltonians (Atia and Aharonov 2017). The theorem says that such shortcuts cannot exist for all sparse Hamiltonians.
- **Gates for explicit Hamiltonians.** The theorem counts queries. For one explicit Hamiltonian it gives no gate lower bound, and such a bound would need a separation of complexity classes. Atia and Aharonov (2017) show that a method that fast-forwards all physically realizable Hamiltonians would give BQP = PSPACE, and they relate fast-forwarding to measurements of energy with a precision better than the time-energy uncertainty allows.
## Tightness

**The constant.** The theorem gives $\tau/(2\pi)$ queries, and the upper bounds are $O(\tau)$ plus a term in the error, so the bound is tight up to a constant factor for constant precision.

**The sparsity.** Berry, Childs and Kothari (2015, Lemma 12) show that the factor $d$ in $\tau = d\|H\|_{\max}t$ is needed too. They divide the entries by $N$ and replace each vertex $|k, j\rangle$ by $d$ copies $|k, j, \ell\rangle$, with an edge between all copies of neighbors (a complete bipartite graph $K_{d,d}$ for each old edge). The new $H$ is $2d$-sparse with $\|H\|_{\max} = \Theta(1)$. The uniform states $|k, j, *\rangle = d^{-1/2}\sum_\ell|k, j, \ell\rangle$ span an invariant subspace on which the entries are multiplied by $d$, so the parity appears at time $t = N\pi/(2d)$, and $\Omega(N) = \Omega(td)$ queries are needed. For $N = 3$, $x = (1, 0, 1)$ and $d = 2$ the matrix has size 16, rows with 4 nonzero entries, and at $t = 3\pi/4$ the whole weight is on the copies of $|0, 3\rangle$, the parity 0. This is stronger than separate bounds $\Omega(t)$ and $\Omega(d)$, which give only $\Omega(t + d)$.

**The error.** Berry, Childs, Cleve, Kothari and Somma (2014, Theorem 1.2) use the same path for a short time. With the entries divided by $N$, the amplitude of the far end is $|\sin(t/N)|^N$ and the other copy of the far end has amplitude 0, so a simulation with error well below $|\sin(t/N)|^N$ gives an unbounded-error algorithm for parity, which also needs $\Omega(N)$ queries. For constant $t$ this forces $N = \Theta(\log(1/\epsilon)/\log\log(1/\epsilon))$, and so $\Omega(\log(1/\epsilon)/\log\log(1/\epsilon))$ queries for a 2-sparse $H$ with $\|H\|_{\max} < 1$.

**Both together.** Berry, Childs and Kothari (2015, Theorem 2) combine the two: for every $\epsilon, t > 0$, every $d \ge 2$ and every value of $\|H\|_{\max}$ there is a $d$-sparse $H$ that needs
$$\Omega\Big(\tau + \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}\Big)$$
queries. They also give the sharper bound $\Omega(N)$ for every $N$ with $\epsilon < \tfrac{1}{2}|\sin(td/N)|^N$, which can be larger than the sum for intermediate values. Low and Chuang (2019, Theorem 1 and Corollary 15) give an upper bound that matches this sharper bound up to constant factors for all parameters, so the query complexity of sparse Hamiltonian simulation is known up to a constant.

**The hypotheses cannot be dropped.** The sparsity 2 is the smallest possible, since 1-sparse Hamiltonians are fast-forwardable. The growth of the dimension is needed, as explained under Statement. Dense Hamiltonians are harder still: Childs and Kothari (2010) extend the argument and show that no generic method simulates them in time polynomial in $\|Ht\|$ and $\log N$.

## History

Berry, Ahokas, Cleve and Sanders posted the theorem in 2005 (arXiv:quant-ph/0508139), with the product formula algorithms for sparse Hamiltonians, and published it in Communications in Mathematical Physics in 2007. They called the result a linear limit on the simulation time. The parity bound they use is from Farhi, Goldstone, Gutmann and Sipser (1998) and Beals, Buhrman, Cleve, Mosca and de Wolf (2001). Childs and Kothari (2010) extended it to non-sparse Hamiltonians. Berry, Childs, Cleve, Kothari and Somma (2014) turned the same construction into a lower bound in the error. Berry, Childs and Kothari (2015) added the sparsity and stated the combined bound; this is the source of the alias of this page. Low and Chuang (2017, 2019) gave algorithms that reach the bound. Atia and Aharonov (2017) studied which Hamiltonians can be fast-forwarded.

## References
