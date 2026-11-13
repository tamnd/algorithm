---
tag: DHF67Z
kind: theorem
slug: grover-optimality
name: Optimality of Grover's search
aliases:
- BBBV theorem
- Bennett-Bernstein-Brassard-Vazirani lower bound
area: quantum/quantum-search
level: advanced
summary: Each quantum algorithm that finds one marked item among N with bounded error needs Ω(√N) oracle queries, so Grover's algorithm is optimal up to a constant factor.
prereqs: [unstructured-search, grover-search, quantum-query-model, hybrid-argument]
see_also: [quantum-query-complexity, polynomial-method, quantum-adversary-method, approximate-degree, search-lower-bound, bqp, relativization, yao-minimax-principle]
sources:
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1997, pages 1510-1523"
    locator: the hybrid argument for search, and the theorem that relative to a random oracle, with probability 1, NP is not in quantum time o(2^(n/2))
  - paper: doi:10.1103/PhysRevA.60.2746
    title: "Christof Zalka, Grover's quantum searching algorithm is optimal, Physical Review A 60(4), 1999, pages 2746-2751"
    locator: the whole paper (no algorithm with T queries beats the success probability of T Grover iterations)
  - paper: arxiv:0810.3647
    title: "Catalin Dohotaru and Peter Høyer, Exact quantum lower bound for Grover's problem, Quantum Information and Computation 9(5-6), 2009, pages 533-540"
    locator: Theorem 9 (a success probability sin^2(Theta_T) needs at least (Theta_T - Theta)/(2 Theta) queries, with sin(Theta) = 1/sqrt(N))
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 7, Theorem 7 (floor(sin(pi/8) sqrt N) expected queries for success 1/2) and Theorem 8 (the same with sqrt(N/t) for t solutions)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.6 (optimality of the search algorithm) and Section 6.7 (black box algorithm limits)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6
    locator: Chapter 11 (quantum query lower bounds; Section 11.2 the polynomial method and Section 11.3 the quantum adversary method, each applied to search)
  - paper: doi:10.1145/502090.502097
    title: "Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4), 2001, pages 778-797"
    locator: Section 2, Table 1 (OR needs Theta(sqrt N) queries with bounded error and N queries exactly)
  - paper: doi:10.1006/jcss.2002.1826
    title: "Andris Ambainis, Quantum lower bounds by quantum arguments, Journal of Computer and System Sciences 64(4), 2002, pages 750-767"
    locator: the adversary method and its Omega(sqrt N) bound for search
---

The optimality theorem for Grover's search says that each quantum algorithm that finds the marked item among $N$ items, with bounded error, makes $\Omega(\sqrt{N})$ queries to the oracle. [Grover's search algorithm](/grover-search/) makes about $(\pi/4)\sqrt{N}$ queries, so it is optimal up to a constant factor, and Zalka showed that it is optimal exactly. The bound is a statement about [unstructured search](/unstructured-search/) in the [quantum query model](/quantum-query-model/). It does not show that NP is outside [BQP](/bqp/).

## Statement

The model is the [quantum query model](/quantum-query-model/). For $x \in \{0, \ldots, N-1\}$, let $O_x$ be the oracle of the function that is 1 only at $x$. It may be the phase oracle $|i\rangle \mapsto (-1)^{[i = x]}|i\rangle$ or the bit oracle $|i\rangle|b\rangle \mapsto |i\rangle|b \oplus [i = x]\rangle$, and it acts as the identity on the other registers. Let $O_\varnothing = I$ be the oracle of the function that is 0 everywhere. An algorithm with $T$ queries is a sequence of fixed unitaries $U_0, \ldots, U_T$ that do not depend on $x$, and it ends with a measurement.

**Theorem (Bennett, Bernstein, Brassard and Vazirani).**

1. *Search.* If, for each $x$, the algorithm with oracle $O_x$ outputs $x$ with probability at least $p$, then $T \ge \frac{1}{2}(\sqrt{pN} - 1)$. For $p = 2/3$ this is $T \ge 0.408\sqrt{N} - 0.5$.
2. *Decision.* If the algorithm accepts $O_\varnothing$ with probability at most $1/3$ and accepts each $O_x$ with probability at least $2/3$, then $T \ge \frac{1}{2}(\sqrt{2/3} - \sqrt{1/3})\sqrt{N} \ge 0.119\sqrt{N}$.

So the bounded-error [quantum query complexity](/quantum-query-complexity/) of search and of $\mathrm{OR}_N$ is $\Omega(\sqrt{N})$, and with Grover's algorithm it is $\Theta(\sqrt{N})$.

**Exact form (Zalka 1999).** For each $T$, no algorithm with $T$ queries has a smaller failure probability for search with one marked item than $T$ iterations of Grover's algorithm. In the form of Dohotaru and Høyer: success probability $\sin^2\Theta_T$ needs $T \ge (\Theta_T - \Theta)/(2\Theta)$ queries, where $\sin\Theta = 1/\sqrt{N}$. Grover's algorithm with $T$ queries reaches $\sin^2((2T+1)\Theta)$, which is this bound with equality.

## In plain words

Imagine that you run a quantum search program twice: once with a box that has no yes item, and once with a box that has its yes item at some place. At first the two runs are the same. They can differ only after a question that touches that place. A question spreads its weight over all places. So, summed over all places, one question can push the two runs apart only a little: about one over the square root of the number of places for each place on average.

To find the yes item, the run for each place must end far from the run with the empty box. Adding the small pushes, this needs about the square root of the number of places in questions. So no quantum program can search faster than Grover's method, except by a constant factor.

## Proof

We prove both parts with the [hybrid argument](/hybrid-argument/) of Bennett, Bernstein, Brassard and Vazirani.

**Notation.** All states are unit vectors in the state space of the algorithm. Let $|\phi_0\rangle = |\phi_0^x\rangle = U_0|0\rangle$ and, for $k = 1, \ldots, T$,

$$|\phi_k\rangle = U_k O_\varnothing |\phi_{k-1}\rangle = U_k|\phi_{k-1}\rangle, \qquad |\phi_k^x\rangle = U_k O_x |\phi_{k-1}^x\rangle.$$

So $|\phi_k^x\rangle$ is the state after $k$ queries to $O_x$, and $|\phi_k\rangle$ the state after $k$ queries to the empty oracle. Let $P_x$ be the projector onto the states whose query register holds $x$. The $P_x$ are orthogonal projectors with $\sum_x P_x = I$, so $\sum_x \|P_x \phi\|^2 = \|\phi\|^2 = 1$ for each state $\phi$. Let $E_k^x = \||\phi_k^x\rangle - |\phi_k\rangle\|$.

**Step 1: one query moves a state only where it queries $x$.** For each state $\phi$, $\|(O_x - I)\phi\| \le 2\|P_x\phi\|$. For the phase oracle, $O_x - I = -2P_x$. For the bit oracle, $O_x - I = (X_b - I)P_x$, where $X_b$ flips the answer qubit, and $\|X_b - I\| = 2$. In both cases $O_x - I = (O_x - I)P_x$ and $\|O_x - I\| \le 2$.

**Step 2: the distance grows slowly.** For $k \ge 1$,

$$|\phi_k^x\rangle - |\phi_k\rangle = U_k\big(O_x(|\phi_{k-1}^x\rangle - |\phi_{k-1}\rangle) + (O_x - I)|\phi_{k-1}\rangle\big).$$

Unitaries keep norms, so with Step 1, $E_k^x \le E_{k-1}^x + 2\|P_x\phi_{k-1}\|$. Since $E_0^x = 0$, induction on $k$ gives

$$E_T^x \le 2\sum_{k=0}^{T-1} \|P_x \phi_k\|.$$

**Step 3: the sum over $x$.** By the Cauchy-Schwarz inequality, for each $k$, $\sum_x \|P_x\phi_k\| \le \sqrt{N}\,\big(\sum_x \|P_x\phi_k\|^2\big)^{1/2} = \sqrt{N}$. So

$$\sum_{x=0}^{N-1} E_T^x \le 2\sum_{k=0}^{T-1}\sum_x \|P_x\phi_k\| \le 2T\sqrt{N}. \qquad (1)$$

**Step 4: part 1 (search).** Let $\Pi_x$ be the projector onto the outcomes of the final measurement that output $x$. The $\Pi_x$ are orthogonal, so $\sum_x \|\Pi_x\phi_T\|^2 \le 1$. By the hypothesis, $\|\Pi_x\phi_T^x\| \ge \sqrt{p}$. Projectors do not increase norms, so

$$\sqrt{p} \le \|\Pi_x\phi_T^x\| \le \|\Pi_x(\phi_T^x - \phi_T)\| + \|\Pi_x\phi_T\| \le E_T^x + \|\Pi_x\phi_T\|.$$

Sum over $x$ and use Cauchy-Schwarz again: $\sum_x \|\Pi_x\phi_T\| \le \sqrt{N}$. So $\sum_x E_T^x \ge N\sqrt{p} - \sqrt{N}$. With (1), $2T\sqrt{N} \ge N\sqrt{p} - \sqrt{N}$, that is, $T \ge \frac{1}{2}(\sqrt{pN} - 1)$.

**Step 5: part 2 (decision).** Let $\Pi$ be the projector onto the accepting outcomes. By the hypothesis, $\|\Pi\phi_T^x\| \ge \sqrt{2/3}$ and $\|\Pi\phi_T\| \le \sqrt{1/3}$. So $E_T^x \ge \|\Pi(\phi_T^x - \phi_T)\| \ge \sqrt{2/3} - \sqrt{1/3}$ for each $x$, and $\sum_x E_T^x \ge N(\sqrt{2/3} - \sqrt{1/3})$. With (1), $T \ge \frac{1}{2}(\sqrt{2/3} - \sqrt{1/3})\sqrt{N}$. Since $\sqrt{2/3} - \sqrt{1/3} > 0.239$, this is at least $0.119\sqrt{N}$. $\blacksquare$

The proof uses no property of the unitaries $U_k$. So it holds for each algorithm, with any number of ancillas and any gates between the queries. The exact form of Zalka needs a finer argument, which we do not repeat here; Dohotaru and Høyer give a short proof.

**A check by hand.** Part 1 says that the success probability after $T$ queries is at most $(2T+1)^2/N$ for every algorithm. For $N = 64$:

| $T$ | bound $(2T+1)^2/64$ | Grover, $\sin^2((2T+1)\Theta)$ |
|---|---|---|
| 0 | 0.0156 | 0.0156 |
| 1 | 0.1406 | 0.1348 |
| 2 | 0.3906 | 0.3439 |
| 3 | 0.7656 | 0.5914 |
| 4 | 1 | 0.8164 |

For small $T$ the simple bound is close to the exact optimum, which Grover's algorithm reaches by Zalka's theorem.

## Consequences

- **Grover's algorithm is optimal.** Its $\lfloor (\pi/4)\sqrt{N} \rfloor$ queries meet the bound up to a constant factor, and by Zalka's theorem exactly.
- **Many marked items.** With $M$ marked items the bound becomes $\Omega(\sqrt{N/M})$ (Boyer, Brassard, Høyer and Tapp, Theorem 8). A simple reduction shows why: copy each of $N/M$ items $M$ times. One marked item among $N/M$ becomes $M$ marked items among $N$, and each query to the large oracle costs one query to the small one. So $T$ queries for the large problem give $T$ queries for search on $N/M$ items. With an unknown $M$, [BBHT search](/bbht-search/) meets this bound.
- **Other problems.** Each problem that contains $\mathrm{OR}_N$ needs $\Omega(\sqrt{N})$ queries: [minimum finding](/minimum-finding/), and the decision version of [counting](/counting-marked-items/) (is the count 0 or not).
- **Relative to an oracle.** Bennett, Bernstein, Brassard and Vazirani conclude that, relative to a random oracle, with probability 1, NP is not contained in quantum time $o(2^{n/2})$. A brute-force quantum search over $2^n$ certificates cannot beat $2^{n/2}$ in this setting.
- **No proof that NP is outside BQP.** The theorem is about black-box algorithms. A real NP problem such as [SAT](/sat/) has a formula, not an oracle, and an algorithm may use its structure. Since statements relative to an oracle can go either way (see [relativization](/relativization/)), the theorem does not separate NP from [BQP](/bqp/).

## Tightness

- **The constant.** Part 1 with $p \to 1$ gives about $\sqrt{N}/2$ queries. Grover's algorithm uses about $(\pi/4)\sqrt{N} \approx 0.785\sqrt{N}$. The exact bound of Zalka closes this gap: the optimum is $\lceil (\Theta_T - \Theta)/(2\Theta) \rceil$ queries for success $\sin^2\Theta_T$, which Grover's algorithm meets.
- **Success probability 1/2.** Boyer, Brassard, Høyer and Tapp (Theorem 7) show that success $1/2$ needs at least $\lfloor \sin(\pi/8)\sqrt{N} \rfloor \approx 0.383\sqrt{N}$ expected queries. Grover's algorithm uses about $(\pi/8)\sqrt{N} \approx 0.393\sqrt{N}$ iterations for this, which is a few percent more.
- **Exact algorithms.** For the decision version with no error, the bound jumps to $N$ queries (Beals, Buhrman, Cleve, Mosca and de Wolf). The $\sqrt{N}$ speedup needs some error, or a promise such as "exactly one marked item".
- **Other proofs.** The [polynomial method](/polynomial-method/) gives the same $\Omega(\sqrt{N})$, because $\mathrm{OR}_N$ has [approximate degree](/approximate-degree/) $\Theta(\sqrt{N})$. The [quantum adversary method](/quantum-adversary-method/) of Ambainis gives it too, and extends to many other functions.

## History

Bennett, Bernstein, Brassard and Vazirani circulated the hybrid argument in 1994, before Grover's algorithm existed, and published it in SIAM Journal on Computing in 1997. Grover's 1996 paper pointed out that this bound makes his algorithm optimal up to a constant. Boyer, Brassard, Høyer and Tapp sharpened the constant in 1996, and Zalka proved in 1999 that Grover's algorithm is optimal exactly, for each number of queries. Beals and others (1998) and Ambainis (2000) gave the polynomial and the adversary proofs. Dohotaru and Høyer gave a short exact proof in 2009.

## References
