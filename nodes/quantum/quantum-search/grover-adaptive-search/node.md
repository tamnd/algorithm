---
tag: Z3TQD9
kind: algorithm
slug: grover-adaptive-search
name: Grover adaptive search
aliases:
- GAS
area: quantum/quantum-search
level: research
summary: Repeated Grover search for a point below the best cost so far, used to minimize functions of binary variables such as QUBO objectives. It needs O(√N) queries for N points.
solves: [minimum-finding]
model: quantum-query-model
complexity:
  vars: {N: the number of points (2^n for n binary variables), n: the number of binary variables, m: the number of qubits of the value register}
  queries: {expected: O(N^(1/2)), worst: O(N^(1/2))}
  time: {worst: O(N^(1/2) (m n^2 + m^2))}
  space: {extra: O(m)}
properties: {deterministic: false, exact: false, oracle: sign of f(x) - y, success_probability: at least 1/2 with the budget rule, monte_carlo: true}
history:
  year: 2003
  people: [David Bulger, William Baritompa, Graham Wood]
  note: Bulger, Baritompa and Wood used Grover search to implement pure adaptive search in 2003 and studied the framework for global optimization in 2005. Gilliam, Woerner and Gonciulea built the oracles for QUBO problems in 2021.
prereqs: [durr-hoyer-minimum-finding]
see_also: [minimum-finding, bbht-search, maximum-cut, combinatorial-optimization-problem, portfolio-optimization, simulated-annealing, variational-quantum-eigensolver, brute-force-search]
sources:
  - paper: doi:10.22331/q-2021-04-08-428
    title: "Austin Gilliam, Stefan Woerner and Constantin Gonciulea, Grover adaptive search for constrained polynomial binary optimization, Quantum 5, 428, 2021 (arXiv:1912.04088)"
    locator: "Section 2 and Algorithm 1 (the loop with the rotation count from {0, ..., ceil(k - 1)}, the update k = lambda k and the reset k = 1), Section 3 (QUBO objectives x^T Q x + b^T x + c, the operator A from a quantum dictionary, Table 1 with the gate counts, Section 3.2 on the sign qubit as the oracle, Section 3.3 on constraints) and Section 4.1 (the portfolio example of Equation 14, the stop after three iterations without an improvement, Figure 8)"
  - paper: doi:10.1137/040605072
    title: "William P. Baritompa, David W. Bulger and Graham R. Wood, Grover's quantum algorithm applied to global optimization, SIAM Journal on Optimization 15(4), 2005, pages 1170-1184"
    locator: the whole paper (the framework of adaptive global optimization with Grover search, and the comparison of the method of Dürr and Høyer with the method of the authors)
  - paper: doi:10.1023/A:1023061218864
    title: "David W. Bulger, William P. Baritompa and Graham R. Wood, Implementing pure adaptive search with Grover's quantum algorithm, Journal of Optimization Theory and Applications 116(3), 2003, pages 517-529"
    locator: the whole paper
  - paper: arxiv:quant-ph/9607014
    title: Christoph Dürr and Peter Høyer, A quantum algorithm for finding the minimum, arXiv:quant-ph/9607014, 1996
    locator: Section 2 (the loop with a threshold, Theorem 1 and Lemma 1)
---

Grover adaptive search is a quantum method to minimize a cost function $f$ on $N = 2^n$ bit strings, such as a quadratic unconstrained binary optimization (QUBO) objective $f(x) = x^{\mathsf T}Qx + b^{\mathsf T}x + c$. It keeps the best value $y$ found so far, uses [Grover's search](/grover-search/) with a random number of iterations to sample a point with $f(x) < y$, and lowers $y$ at each improvement. With the rotation counts of [BBHT search](/bbht-search/) and a budget of $O(\sqrt N)$ queries it is [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/) on the table of $f$, and it finds a minimum with probability at least $1/2$. In practice it is often run with a patience rule instead, which stops after a number of rounds without an improvement and has no such guarantee.

## In plain words

You want the cheapest of a very large set of choices, and you can compute the cost of any choice. Pick one choice at random and remember its cost as the best so far. Then use a quantum search to find a choice that is cheaper than the best so far. If the search finds one, it becomes the new best. If it does not, try again with a longer search.

The quantum search needs about the square root of the number of choices, and each improvement usually cuts the number of better choices by a large factor. So the whole method needs about the square root of the number of choices in total. You stop after a fixed amount of work, or after some searches in a row find nothing better.

## The problem

The input is a cost function $f : \{0,1\}^n \to \mathbb{R}$, and the output is a point $x$ with $f(x) = \min_z f(z)$. The variable $x_i$ is bit $i - 1$ of the index $x$, and qubit 0 is the least significant bit, as on [quantum state](/quantum-state/). The algorithm uses two operators for a threshold $y$:

- $A_y$ prepares $\frac{1}{\sqrt N}\sum_x |x\rangle_n|f(x) - y\rangle_m$, a uniform superposition of the points with the shifted values in an $m$-qubit value register in two's complement.
- $O$ flips the sign of the states whose value is negative, that is $f(x) < y$. It reads one qubit, the sign bit of the value register.

The Grover iteration is $G_y = A_y D A_y^\dagger O$, where $D$ flips the sign of $|0\rangle$. On the key register, $G_y$ acts as the Grover iteration for the marking $[f(x) < y]$, with the [Grover diffusion operator](/grover-diffusion-operator/) about the uniform state. Each application of $G_y$ counts as one query in the [quantum query model](/quantum-query-model/), and the value of $f$ at a measured point counts as one more. This is the problem of [quantum minimum finding](/minimum-finding/) for the table $T[x] = f(x)$, with a cost function in place of a stored table.

## The algorithm

```pseudo id=main
GROVER-ADAPTIVE-SEARCH(f, N, B, P)     ▷ B: budget of queries; P: patience; either may be ∞
L1  x ← a point chosen uniformly at random; y ← f(x); used ← 1
L2  k ← 1; λ ← 6/5; fails ← 0
L3  while used < B and fails < P
L4      choose r uniformly at random from {0, 1, ..., ⌈k⌉ - 1}
L5      prepare A_y|0⟩, apply G_y^r, measure the key x′ and read f(x′)   ▷ r queries
L6      used ← used + r + 1
L7      if f(x′) < y then x ← x′; y ← f(x′); k ← 1; fails ← 0
L8      else k ← min(λk, √N); fails ← fails + 1
L9  return x, y
```

Gilliam, Woerner and Gonciulea state the loop as their Algorithm 1 with any $\lambda > 1$ and a free termination rule; the set $\{0, \ldots, \lceil k - 1\rceil\}$ of line L4 there has the same $\lceil k\rceil$ elements. This page fixes $\lambda = 6/5$ and the cap $\sqrt N$ of BBHT search, and gives two termination rules. The **budget rule** sets $P = \infty$ and $B = 2Q(N)$ with $Q(N) = 1 + 18\sqrt N + \ln N(\log_{6/5}\sqrt N + 5)$. The **patience rule** sets $B = \infty$ and stops after $P$ rounds in a row without an improvement; Gilliam, Woerner and Gonciulea use $P = 3$ in their test case.

In a real circuit, $A_y$ adds the constant $-y$ to the free term of the polynomial, and line L5 reads $f(x') - y$ from the value register. The simulator of the implementation applies the phase flip $(-1)^{[f(x) < y]}$ to the key register directly, which has the same effect on the key register as $A_y$, $O$ and $A_y^\dagger$.

## Example

Take the portfolio objective of Equation 14 of Gilliam, Woerner and Gonciulea, with $n = 3$ and $N = 8$:

$$f(x) = -2x_1x_3 - x_2x_3 - x_1 + 2x_2 - 3x_3.$$

Its values on the indices $0, 1, \ldots, 7$ are $0, -1, 2, 1, -3, -6, -2, -5$, and the minimum is $f = -6$ at index 5, the point $(x_1, x_2, x_3) = (1, 0, 1)$. A run with the seed 6 of the implementation and the patience rule with $P = 3$ starts in line L1 at index 1 with $y = -1$. Here $t$ is the number of points below $y$, and $\Pr$ is the probability $\sin^2((2r+1)\theta)$, with $\sin^2\theta = t/8$, that line L5 gives one of them:

| round | $y$ | $t$ | $k$ | $r$ | $\Pr$ | $x'$ | $f(x')$ | line L7 | queries so far |
|---|---|---|---|---|---|---|---|---|---|
| 1 | $-1$ | 4 | 1 | 0 | 0.5 | 6 | $-2$ | new threshold | 2 |
| 2 | $-2$ | 3 | 1 | 0 | 0.375 | 0 | 0 | no | 3 |
| 3 | $-2$ | 3 | 1.2 | 1 | 0.8438 | 7 | $-5$ | new threshold | 5 |
| 4 | $-5$ | 1 | 1 | 0 | 0.125 | 2 | 2 | no | 6 |
| 5 | $-5$ | 1 | 1.2 | 0 | 0.125 | 2 | 2 | no | 7 |
| 6 | $-5$ | 1 | 1.44 | 0 | 0.125 | 5 | $-6$ | new threshold | 8 |
| 7 | $-6$ | 0 | 1 | 0 | 0 | 7 | $-5$ | no | 9 |
| 8 | $-6$ | 0 | 1.2 | 0 | 0 | 1 | $-1$ | no | 10 |
| 9 | $-6$ | 0 | 1.44 | 1 | 0 | 5 | $-6$ | no | 12 |

After three rounds in a row without an improvement, the run returns index 5 with $y = -6$, after 12 queries. Over all random choices, this rule finds the minimum with probability $0.7663$ and makes $7.82$ queries on average; an exhaustive scan needs 8 evaluations. With two points below the threshold, one iteration finds one of them with certainty, and with one point, with probability $25/32 = 0.781$; these are the probabilities of Figure 8 of the paper.

## Correctness

Line L7 accepts a measured point only if its value is below $y$, so $y$ never increases, $f(x) = y$ always holds, and $y$ is the least value seen. In a phase between two improvements, `fails` counts the rounds, so a phase has at most $P$ rounds, and the run stops. With the budget rule, the loop is line for line Dürr-Høyer minimum finding on the table $T[x] = f(x)$, so its theorem gives a minimum with probability at least $1/2$. With the patience rule, the Grover state gives every point below the threshold the same amplitude, so each improvement is uniform among those points, and a recursion over the distinct values gives the exact success probability. That probability is at most $\frac{n_1}{N}(1 + P(2c_P - 1)^2\ln N)$, where $n_1$ points have the minimum value and $c_P = \lceil\min(1.2^{P-1}, \sqrt N)\rceil$; so a fixed patience fails for large $N$. The full proof is in proofs/correctness.md.

## Complexity

With the budget rule, a run makes fewer than $B + \sqrt N + 2 = O(\sqrt N)$ queries, and the expected number of queries until the minimum is found is at most $Q(N)$. The patience rule needs a larger $P$ as $N$ grows. The exact values below are for $N$ distinct values, from the recursion of the proof:

| $n$ | $N$ | least $P$ for success $\ge 1/2$ | its mean queries | least $P$ for success $\ge 0.9$ | its mean queries | success with $P = 3$ | budget rule: mean queries until the minimum | budget $2Q(N)$ |
|---|---|---|---|---|---|---|---|---|
| 3 | 8 | 2 | 5.3 | 5 | 12.7 | 0.766 | 5.9 | 149 |
| 4 | 16 | 3 | 8.6 | 6 | 17.4 | 0.578 | 9.1 | 216 |
| 6 | 64 | 6 | 21.4 | 10 | 39.1 | 0.223 | 20.6 | 427 |
| 8 | 256 | 10 | 47.9 | 14 | 80.6 | 0.064 | 44.6 | 803 |
| 10 | 1024 | 14 | 97.8 | 18 | 162.6 | 0.017 | 92.9 | 1487 |

The patience needed grows by about 2 for each extra variable, that is like $\log_{6/5}\sqrt N$, and with it the mean cost stays near $5\sqrt N$ for success $0.9$. These are computed values, not a proved bound. The proved budget is much larger than the mean cost, but a run with the budget rule always spends the whole budget, because it cannot know that it has found the minimum.

The cost of one query depends on the circuit for $f$. For a QUBO with dense $Q$ and $b$, Table 1 of Gilliam, Woerner and Gonciulea gives $m$ Hadamard gates, $m$ phase gates, $mn$ singly controlled and $mn(n-1)/2$ doubly controlled phase gates, and one inverse [quantum Fourier transform](/quantum-fourier-transform/) on $m$ qubits for $A$. So the time is $O(\sqrt N(mn^2 + m^2))$ gates, and the space is $n + m$ qubits, with $m$ large enough to hold every value of $f - y$ and its sign.

## Properties

- **Anytime.** $y$ never increases, and a run stopped at any moment returns the best point it has seen.
- **Bounded error with the budget rule.** The output is always a valid point, and it is a minimum with probability at least $1/2$. Repetition makes the error smaller.
- **No guarantee with a fixed patience.** For a fixed $P$, the success probability tends to 0 as $N$ grows; $P$ must grow with $n$.
- **Ties.** Points with equal values are allowed, and any minimum point can be the output. A strict test in line L7 keeps the threshold from moving among equal values.
- **Quadratic speedup over exhaustive search.** $O(\sqrt N) = O(2^{n/2})$ evaluations of $f$ in superposition, against $2^n$ for [exhaustive search](/brute-force-search/). The [optimality of Grover's search](/grover-optimality/) shows that no quantum algorithm does better for a cost function given only as an oracle.

## Variants and improvements

- **Other rules for the rotation count.** Baritompa, Bulger and Wood compare the rule of Dürr and Høyer with a rule of their own for choosing the number of Grover iterations. Gilliam, Woerner and Gonciulea allow any $\lambda > 1$ and do not cap $k$; without the cap, $k$ grows without bound in a long run of failures, and each round costs more.
- **Constraints.** Gilliam, Woerner and Gonciulea compute each constraint of a constrained polynomial problem into its own register and flag a point only if the objective and every constraint test are negative. Equality constraints can also be added to the objective as penalty terms.
- **Polynomials of higher degree.** The same construction of $A$ adds one controlled rotation for each monomial, so any polynomial in binary variables can be the objective.
- **Non-integer coefficients.** Scale the coefficients to fractions with a common denominator, or encode them as phases and accept a spread of values in the register, as in Appendix B of the paper.
- **Classical heuristics.** [Simulated annealing](/simulated-annealing/) and [local search](/local-search/) also improve a best point step by step, but they move to neighbours and have no general guarantee.

## When to use it

Use it for small unconstrained or constrained binary problems such as [maximum cut](/maximum-cut/) or [portfolio optimization](/portfolio-optimization/) in a QUBO form, when the problem has no structure that a classical solver can use and a fault-tolerant quantum computer is available. The speedup is only quadratic, and the circuit for $f$ adds $O(mn^2)$ gates to each query, so a classical solver such as [branch and bound](/branch-and-bound/) is often faster on real instances. On near-term hardware, the depth of the circuits is the main obstacle; Gilliam, Woerner and Gonciulea call the method one that likely requires a fault-tolerant quantum computer. Use the budget rule for a guarantee, and a patience that grows with $n$ when no guarantee is needed.

## Pitfalls

- **A fixed small patience.** "L3 while fails < 3" works for $n = 3$, with success $0.766$, but for $n = 10$ it finds the minimum with probability only $0.017$. Use the budget rule "L3 while used < B" with $B = 2Q(N)$, or a patience that grows with $n$, such as $P = 18$ for $n = 10$.
- **Measuring without a check.** "L7 $x \leftarrow x'$; $y \leftarrow f(x')$" accepts a measured point that is no improvement, so the threshold can rise. Use "L7 if $f(x') < y$ then $x \leftarrow x'$; $y \leftarrow f(x')$".
- **Marking equal values.** "L5 ... apply $G_y^r$ for the marking $f(x) \le y$" marks the current point and its ties, so many rounds measure a point that is no improvement. With many ties and one better point, the search then rarely finds the better point. Keep the strict marking $f(x) < y$, which the sign bit of the value register gives.
- **A fixed rotation count.** "L4 $r \leftarrow \lfloor\frac{\pi}{4}\sqrt N\rfloor$" is right only for one marked point and overshoots when many points are below the threshold, which is the case in the early rounds. Keep the random $r$ of line L4.
- **A value register that is too small.** If $m$ cannot hold $f(x) - y$, the value wraps in two's complement and the sign bit of a large positive value reads as negative. Choose $m$ so that every shifted value fits, and add one qubit for the shift by $-y$, as the paper does for its example.
- **Counting only the Grover iterations.** "L6 used $\leftarrow$ used $+ r$" leaves out the preparation and the reading of $f(x')$ in each round, and a run with many rounds of $r = 0$ then seems free. Use "L6 used $\leftarrow$ used $+ r + 1$".

## Implementations

## History

Dürr and Høyer gave the threshold loop with a time-out in 1996, for the minimum of a table. Bulger, Baritompa and Wood used Grover search in 2003 to implement pure adaptive search, a method of global optimization that samples each new point from the region below the best value so far, and in 2005 Baritompa, Bulger and Wood studied this framework and compared rules for the number of iterations. Gilliam, Woerner and Gonciulea gave efficient oracles for QUBO and other polynomial objectives in 2019, published in Quantum in 2021, with a simulation for portfolio optimization and a run on IBM hardware; their code is in the Qiskit optimization module.

## References
