---
tag: KPQ2QF
kind: concept
slug: quantum-query-complexity
name: Quantum query complexity
aliases:
- Q(f)
area: complexity/communication-and-query-complexity
level: research
summary: "Q(f) is the least number of oracle calls of a quantum algorithm that computes f with error at most 1/3. Q_E(f) is the same with no error allowed."
prereqs: [quantum-query-model, query-complexity]
see_also: [quantum-adversary-method, polynomial-method, approximate-degree, grover-optimality, element-distinctness-lower-bound, randomized-query-complexity, sensitivity-theorem, quantum-communication-complexity]
sources:
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 2 (Q_E and Q_2) and Section 5 (relations with D, R, deg and bs)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (Q(f) at least half the approximate degree, Q(f) = Omega(sqrt(bs(f))), the bounds for OR and PARITY, D(f) = O(Q(f)^6) for total f)
  - paper: doi:10.1006/jcss.2002.1826
    title: "Andris Ambainis, Quantum lower bounds by quantum arguments, Journal of Computer and System Sciences 64(4), 2002, pages 750-767"
    locator: the adversary method and the Omega(sqrt N) bound for the AND of ORs
  - paper: doi:10.1137/1.9781611973082.44
    title: Ben W. Reichardt, Reflections for quantum query algorithms, Proceedings of the 22nd ACM-SIAM Symposium on Discrete Algorithms (SODA 2011)
    locator: pp. 560 to 569 (the general adversary bound is tight for every Boolean function)
  - paper: doi:10.1145/3406325.3451047
    title: Scott Aaronson, Shalev Ben-David, Robin Kothari, Shravas Rao and Avishay Tal, Degree vs. approximate degree and quantum implications of Huang's sensitivity theorem, 53rd ACM Symposium on Theory of Computing (STOC 2021)
    locator: pp. 1330 to 1342 (D(f) = O(Q(f)^4) for total f)
  - paper: doi:10.1137/S0097539705447311
    title: Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1) (2007)
    locator: the O(n^(2/3)) algorithm for element distinctness
  - paper: doi:10.1145/1008731.1008735
    title: Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4) (2004)
    locator: pp. 595 to 605 (Omega(n^(1/3)) for collision and Omega(n^(2/3)) for element distinctness)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415
    locator: Chapter 11 (quantum query lower bounds)
---

Quantum query complexity measures how many oracle calls a quantum algorithm needs to compute a function. For $f$ on inputs $x \in \{0,1\}^n$, $Q(f)$ is the least number of calls to the oracle $O_x$ in the [quantum query model](/quantum-query-model/) such that some algorithm outputs $f(x)$ with probability at least $2/3$ on every input in the domain. $Q_E(f)$ is the same count when the algorithm must be correct with probability $1$. The measures sit next to $D^{dt}(f)$ and $R(f)$ in the family of [query complexity](/query-complexity/) measures.

## In plain words

A quantum program gets its input from a black box. It may ask the box about many positions at the same time, in a quantum way, but each question still costs one unit. Thinking between questions is free. Quantum query complexity counts the questions that the best such program needs to give the right answer with high probability. For some tasks the saving over normal programs is large. To find one marked item among a million, a normal program must look at about a million places, but a quantum program needs only about a thousand questions. For other tasks there is almost no saving, for example to decide whether most of the bits are ones. This measure is useful because, for it, strong lower bounds can be proved. Lower bounds on time are much harder.

## The idea

Fix a function $f$, total or partial. A quantum query algorithm with $T$ queries is a product $U_T O_x U_{T-1} \cdots U_1 O_x U_0$ applied to $|0\rangle$, followed by a measurement, where the maps $U_t$ do not depend on $x$. Then:

- $Q_\varepsilon(f)$ is the least $T$ for which some such algorithm outputs $f(x)$ with probability at least $1 - \varepsilon$ on each $x$ in the domain,
- $Q(f) = Q_{1/3}(f)$, the bounded-error measure, and
- $Q_E(f) = Q_0(f)$, the exact measure.

For a constant $\varepsilon < 1/2$, $Q_\varepsilon(f) = \Theta(Q(f))$, because a majority vote over a constant number of runs lowers the error.

A quantum algorithm can simulate a decision tree query by query, so $Q(f) \le R(f) \le D^{dt}(f) \le n$ and $Q_E(f) \le D^{dt}(f)$. The three lower-bound methods give:

- **Polynomial method.** After $T$ queries, the acceptance probability is a real polynomial of degree at most $2T$ in $x_1, \ldots, x_n$. So $Q(f) \ge \widetilde{\deg}(f)/2$ and $Q_E(f) \ge \deg(f)/2$, where $\widetilde{\deg}$ is the [approximate degree](/approximate-degree/). See [polynomial method](/polynomial-method/).
- **Block sensitivity.** Beals et al. show $Q(f) = \Omega(\sqrt{bs(f)})$, where $bs$ is the [block sensitivity](/block-sensitivity/).
- **Adversary method.** $Q(f) = \Omega(\mathrm{ADV}(f))$ for the positive-weight bound, and $Q(f) = \Theta(\mathrm{ADV}^{\pm}(f))$ for the general bound with negative weights when $f$ is Boolean (Reichardt). So the general adversary bound is, up to a constant factor, a formula for $Q(f)$. See [quantum adversary method](/quantum-adversary-method/).

For total $f$ the quantum and classical measures are polynomially related. Beals et al. proved $D^{dt}(f) = O(Q(f)^6)$. Aaronson, Ben-David, Kothari, Rao and Tal used the [sensitivity theorem](/sensitivity-theorem/) to improve this to $D^{dt}(f) = O(Q(f)^4)$. For partial $f$ no relation of this kind holds, because the promise can hide the structure that a quantum algorithm uses.

## Examples

| Function | $Q(f)$ | Lower-bound method | Upper bound |
|---|---|---|---|
| OR of $n$ bits | $\Theta(\sqrt n)$ | hybrid argument, polynomials, adversary | [Grover search](/grover-search/) |
| PARITY of $n$ bits | $\lceil n/2 \rceil$ | polynomials (degree $n$) | pairs of bits, one query each |
| AND of $\sqrt n$ ORs of $\sqrt n$ bits | $\Omega(\sqrt n)$ and $O(\sqrt n \log n)$ | adversary | Grover inside Grover |
| [Element distinctness](/element-distinctness-lower-bound/), $n$ items | $\Theta(n^{2/3})$ | polynomials (Aaronson and Shi) | [quantum walk](/ambainis-element-distinctness/) |
| MAJORITY of $n$ bits | $\Theta(n)$ | polynomials | read all bits |

**OR.** Grover search finds a 1 in $x$ with $O(\sqrt n)$ queries, and the theorem on [optimality of Grover search](/grover-optimality/) shows that $\Omega(\sqrt n)$ queries are necessary. The exact cost is different: $\deg(\mathrm{OR}_n) = n$, so $Q_E(\mathrm{OR}_n) \ge n/2$, and Beals et al. show $Q_E(\mathrm{OR}_n) = n$. With no error allowed, quantum gives no saving for OR.

**PARITY.** One phase query computes $x_1 \oplus x_2$ exactly (Deutsch's problem, worked on the [quantum query model](/quantum-query-model/) page). Do this for each of the $\lceil n/2 \rceil$ pairs and add the results modulo 2. The parity of $n$ bits has approximate degree $n$, so $Q(\mathrm{PARITY}_n) \ge n/2$, and the upper bound is tight. Quantum gives a saving of a factor of 2 and no more.

**AND of ORs.** Let $n = k^2$ and $f(x) = \bigwedge_{b=1}^{k} \bigvee_{j=1}^{k} x_{b,j}$. Run Grover search over the $k$ blocks to find a block with no 1, and in each step run Grover search inside the block to test it. With error reduction inside, this costs $O(\sqrt k \cdot \sqrt k \log k) = O(\sqrt n \log n)$ queries. Ambainis proved the lower bound $\Omega(\sqrt n)$ with his adversary method. When Ambainis wrote his paper, no matching bound from the polynomial method was known for this function.

**Element distinctness and collision.** For $n$ items from a large range, the quantum walk of Ambainis decides if two items are equal with $O(n^{2/3})$ queries, and Aaronson and Shi proved $\Omega(n^{2/3})$ with the polynomial method. For the collision problem, a partial function where the input is promised to be one-to-one or two-to-one, the [Brassard-Hoyer-Tapp algorithm](/brassard-hoyer-tapp-collision/) uses $O(n^{1/3})$ queries and Aaronson and Shi proved $\Omega(n^{1/3})$.

**Partial functions.** In the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/) the input is promised to be constant or balanced. One query decides it exactly, so $Q_E = 1$, while a deterministic algorithm must read more than half the bits. In the [Simon problem](/simon-problem/), $O(n)$ queries suffice on an input of size $2^n$, and each classical randomized algorithm needs a number of queries exponential in $n$.

## Where it is used

- **Lower bounds for quantum algorithms.** Each query is at least one step, so a query lower bound is a lower bound on time. It is the main source of unconditional lower bounds for quantum algorithms, for example for search, element distinctness, [k-distinctness](/k-distinctness/) and [triangle finding](/triangle-finding/).
- **Oracle results.** A query lower bound for a problem about an oracle gives a separation of classes relative to that oracle. The bound for OR gives an oracle relative to which $\mathsf{NP}$ is not in [BQP](/bqp/).
- **Communication complexity.** A query algorithm for $f$ applied to $x \wedge y$ gives a protocol in [quantum communication complexity](/quantum-communication-complexity/). This is how $O(\sqrt n \log n)$ qubits suffice for set disjointness.
- **Cryptography.** The collision lower bound limits generic quantum attacks on hash functions to about $N^{1/3}$ queries for a range of size $N$.

## References
