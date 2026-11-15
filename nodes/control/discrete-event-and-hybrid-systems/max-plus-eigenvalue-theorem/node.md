---
tag: CAQ0PK
kind: theorem
slug: max-plus-eigenvalue-theorem
name: Max-plus eigenvalue theorem
aliases:
- cycle time theorem of max-plus systems
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: "An irreducible max-plus matrix has exactly one eigenvalue, the maximum cycle mean of its graph. It has a finite eigenvector, and x(k) / k of x(k+1) = A x(k) tends to that value."
prereqs: [max-plus-algebra, strongly-connected-components]
see_also: [karp-minimum-mean-cycle, minimum-mean-cycle-problem, timed-event-graph, perron-frobenius-theorem, policy-iteration, eigenvalue, longest-path-problem]
sources:
  - book: isbn:9780691117638
    title: Bernd Heidergott, Geert Jan Olsder and Jacob van der Woude, Max Plus at Work, Princeton University Press, 2006
    locator: Chapter 2, Spectral Theory (Section 2.2, Eigenvalues and Eigenvectors); Chapter 3, Periodic Behavior and the Cycle-Time Vector (Section 3.1, Cyclicity and Transient Time)
  - book: isbn:9780471936091
    title: François Baccelli, Guy Cohen, Geert Jan Olsder and Jean-Pierre Quadrat, Synchronization and Linearity, An Algebra for Discrete Event Systems, Wiley, 1992
    locator: the chapter on max-plus algebra, the spectral theory of irreducible matrices and the periodicity of their powers
  - paper: "Guy Cohen, Didier Dubois, Jean-Pierre Quadrat and Michel Viot, A linear-system-theoretic view of discrete-event processes and its use for performance evaluation in manufacturing, IEEE Transactions on Automatic Control AC-30(3), 210-220, 1985"
    locator: the periodic behavior of the powers of an irreducible max-plus matrix (cyclicity)
  - book: isbn:9783540091134
    title: Raymond Cuninghame-Green, Minimax Algebra, Lecture Notes in Economics and Mathematical Systems 166, Springer, 1979
    locator: the eigenvalue problem for max-plus matrices
  - paper: "Richard M. Karp, A characterization of the minimum cycle mean in a digraph, Discrete Mathematics 23(3), 309-311, 1978"
    locator: the formula for the minimum cycle mean, which gives the maximum cycle mean after a change of sign
---

The max-plus eigenvalue theorem says that a square matrix $A$ over the [max-plus algebra](/max-plus-algebra/) whose graph is strongly connected has exactly one eigenvalue $\lambda$: the maximum, over all circuits of the graph, of the circuit weight divided by the circuit length. The matrix has an eigenvector with all entries finite, and every solution of $x(k+1) = A \otimes x(k)$ grows like $k \lambda$ in each entry. In a [timed event graph](/timed-event-graph/), $\lambda$ is the cycle time, the mean time between two firings of each transition once the system runs. The theorem is the max-plus counterpart of the [Perron-Frobenius theorem](/perron-frobenius-theorem/) for nonnegative matrices. The value $\lambda$ is a maximum cycle mean, so [Karp's algorithm](/karp-minimum-mean-cycle/) computes it after a change of sign; this page states and proves the theorem and does not repeat the algorithm.

## Statement

Notation is that of [max-plus algebra](/max-plus-algebra/): $\varepsilon = -\infty$, $a \oplus b = \max(a, b)$, $a \otimes b = a + b$. For $A \in \mathbb{R}_{\max}^{n \times n}$, the graph $\mathcal{G}(A)$ has an arc $j \to i$ of weight $A_{ij}$ when $A_{ij} \ne \varepsilon$. A circuit $\zeta$ has a weight $|\zeta|_w$ (the sum of its arc weights) and a length $|\zeta|_\ell \ge 1$ (its number of arcs). The maximum cycle mean is

$$\rho(A) = \max_{\zeta} \frac{|\zeta|_w}{|\zeta|_\ell},$$

over all elementary circuits of $\mathcal{G}(A)$. A circuit that reaches the maximum is critical. A scalar $\lambda \in \mathbb{R}_{\max}$ is an eigenvalue of $A$ if $A \otimes v = \lambda \otimes v$ for some vector $v$ with at least one entry different from $\varepsilon$.

**Theorem.** Let $A \in \mathbb{R}_{\max}^{n \times n}$ be irreducible: $\mathcal{G}(A)$ is strongly connected and has at least one arc. Then:

1. $A$ has exactly one eigenvalue, and it is $\lambda = \rho(A)$, a finite real number.
2. Every eigenvector of $A$ has all entries finite. For any node $c$ on a critical circuit, the column $c$ of $\left((-\lambda) \otimes A\right)^+$ is an eigenvector.
3. For every $x(0) \in \mathbb{R}^n$, the solution of $x(k+1) = A \otimes x(k)$ satisfies $\lim_{k \to \infty} x_i(k)/k = \lambda$ for every $i$. More precisely, $\max_i |x_i(k) - k\lambda - v_i|$ stays bounded for any eigenvector $v$.

The theorem is in Heidergott, Olsder and van der Woude (2006), Chapter 2, and in Baccelli, Cohen, Olsder and Quadrat (1992). A stronger fact, the cyclicity theorem, is stated under Consequences with its source; it is not proved here.

## In plain words

Think of a network of tasks. Each task starts again only after certain other tasks have finished, and each link has a fixed delay. Follow any closed loop of links: the total delay divided by the number of links is that loop's average delay per step. The theorem says that the slowest loop sets the pace of the whole network. Every task repeats, in the long run, once per this average delay, no matter how the network starts. Faster loops must wait for the slowest one, because the network is connected and every task depends, directly or not, on every other task. There is also a steady pattern of start times that moves forward by exactly this amount at each step.

## Proof

Let $A$ be irreducible. For $n = 1$, $A = [a]$ with $a$ finite, and the steps below give $\lambda = a$.

**Step 1: eigenvectors are finite, and eigenvalues are finite.** Let $A \otimes v = \lambda \otimes v$ with $v_j \ne \varepsilon$ for some $j$. Since $\mathcal{G}(A)$ is strongly connected with an arc, some arc $j \to i$ exists. Then $\lambda + v_i = (A \otimes v)_i \ge A_{ij} + v_j > -\infty$, so $\lambda \ne \varepsilon$ and $v_i \ne \varepsilon$. Following arcs, finiteness spreads from $j$ to every node, because every node can be reached from $j$. Also $\lambda < +\infty$ since all entries are in $\mathbb{R}_{\max}$.

**Step 2: $\lambda \ge \rho(A)$.** Let $v$ be a finite eigenvector. For every arc $j \to i$, the eigen equation gives $\lambda + v_i \ge A_{ij} + v_j$. Add these inequalities along a circuit $\zeta$ with nodes $i_1 \to i_2 \to \cdots \to i_\ell \to i_1$. Each $v$ appears once on each side, so they cancel, and $\ell \lambda \ge |\zeta|_w$. So $\lambda$ is at least the mean of every circuit.

**Step 3: $\lambda \le \rho(A)$.** For each node $i$, the maximum in $(A \otimes v)_i = \max_j (A_{ij} + v_j)$ is reached at some $j = \pi(i)$ with $A_{i\pi(i)} \ne \varepsilon$, and there $\lambda + v_i = A_{i \pi(i)} + v_{\pi(i)}$. The sequence $i, \pi(i), \pi(\pi(i)), \dots$ takes values in a finite set, so it repeats; the repeated part is a circuit of $\mathcal{G}(A)$, run along the arcs $\pi(i) \to i$. Adding the equalities along it gives $\ell \lambda = |\zeta|_w$ for that circuit. So $\lambda$ equals some circuit mean, and with Step 2, $\lambda = \rho(A)$. Steps 1 to 3 show that every eigenvalue equals $\rho(A)$, so there is at most one.

**Step 4: an eigenvector exists.** Let $\lambda = \rho(A)$ and $B = (-\lambda) \otimes A$, that is $B_{ij} = A_{ij} - \lambda$. Every circuit of $\mathcal{G}(B)$ has weight $|\zeta|_w - |\zeta|_\ell \lambda \le 0$, and critical circuits have weight 0. A walk of length $n + 1$ or more repeats a node, so it contains a circuit; removing the circuit does not lower the weight. So $B^{\otimes k} \preceq B \oplus \cdots \oplus B^{\otimes n}$ for all $k > n$, and $B^+ = B \oplus \cdots \oplus B^{\otimes n}$. Every entry of $B^+$ is finite by strong connectivity. From the definition, $B^+ = B \oplus B \otimes B^+$.

Let $c$ be a node on a critical circuit. Then $(B^+)_{cc} = 0$: the critical circuit gives a closed walk of weight 0 through $c$, and no closed walk has positive weight, because it splits into circuits. Let $v$ be column $c$ of $B^+$, so $v_c = 0$. Column $c$ of $B^+ = B \oplus B \otimes B^+$ reads $v = B_{\cdot c} \oplus B \otimes v$. For each $i$, $(B \otimes v)_i \ge B_{ic} + v_c = B_{ic}$, so the term $B_{\cdot c}$ is absorbed and $v = B \otimes v$. Adding $\lambda$ to both sides gives $A \otimes v = \lambda \otimes v$.

**Step 5: the cycle time.** The map $x \mapsto A \otimes x$ is monotone ($x \le y$ entrywise gives $A \otimes x \le A \otimes y$) and homogeneous ($A \otimes (\alpha + x) = \alpha + A \otimes x$ for a real scalar $\alpha$). Let $v$ be a finite eigenvector and $x(0) \in \mathbb{R}^n$, and set $\alpha = \min_i (x_i(0) - v_i)$ and $\beta = \max_i (x_i(0) - v_i)$. Then $\alpha + v \le x(0) \le \beta + v$, and $k$ applications of the map give

$$\alpha + k\lambda + v \le x(k) \le \beta + k\lambda + v.$$

So $|x_i(k) - k\lambda - v_i| \le \max(|\alpha|, |\beta|)$, and $x_i(k)/k \to \lambda$. $\blacksquare$

**Example.** For $A = \begin{bmatrix} 3 & 7 \\ 2 & 4 \end{bmatrix}$ the circuits are the loops of means 3 and 4, and $1 \to 2 \to 1$ with mean $(2 + 7)/2 = 4.5$. So $\lambda = 4.5$. Then $B = \begin{bmatrix} -1.5 & 2.5 \\ -2.5 & -0.5 \end{bmatrix}$, $B^{\otimes 2} = \begin{bmatrix} 0 & 2 \\ -3 & 0 \end{bmatrix}$ and $B^+ = \begin{bmatrix} 0 & 2.5 \\ -2.5 & 0 \end{bmatrix}$. Column 1 gives $v = (0, -2.5)$, and indeed $A \otimes v = (\max(3, 4.5), \max(2, 1.5)) = (4.5, 2) = 4.5 \otimes v$. Column 2 is $2.5 \otimes v$, the same eigenvector up to a scalar. From $x(0) = (0, 0)$ the recurrence gives $x(4) = (20, 18)$ and $x(5) = (25, 22)$; the bounds of Step 5 with $\alpha = 0$ and $\beta = 2.5$ give $18 \le x_1(4) \le 20.5$ and $15.5 \le x_2(4) \le 18$, which hold.

## Consequences

- **Cycle time of timed event graphs.** In a strongly connected [timed event graph](/timed-event-graph/), each transition fires once per $\lambda$ time units in the long run, and $1/\lambda$ is the throughput. The critical circuits are the bottleneck: lowering a delay that is not on a critical circuit does not change $\lambda$.
- **Computation.** $\lambda$ is a maximum cycle mean. Negating the weights turns it into a minimum cycle mean, which [Karp's algorithm](/karp-minimum-mean-cycle/) computes in $O(n m)$ time for $m$ arcs (Karp 1978); see the [minimum mean cycle problem](/minimum-mean-cycle-problem/). A max-plus form of Howard's [policy iteration](/policy-iteration/) also computes it. Heidergott et al. (2006) describe numerical procedures in Chapter 5.
- **Cyclicity.** For irreducible $A$ there are integers $K \ge 0$ and $c \ge 1$ with $A^{\otimes (k + c)} = (c \lambda) \otimes A^{\otimes k}$ for all $k \ge K$ (Cohen, Dubois, Quadrat and Viot 1985; Heidergott et al. 2006, Section 3.1). So $x(k)$ becomes periodic up to the shift $k\lambda$ after a finite transient. For the example above, $A^{\otimes 4} = 9 \otimes A^{\otimes 2}$, so $c = 2$ works with $K = 2$ for the powers; the trajectory from $(0, 0)$ goes $(7, 4), (11, 9), (16, 13), (20, 18), \dots$ and repeats the increments $(4, 5)$ and $(5, 4)$.
- **The eigenspace.** The eigenvectors are the max-plus combinations of the columns of $B^+$ at critical nodes, and two critical nodes on the same critical circuit give proportional columns, as in the example. The proof is in Heidergott et al. (2006), Chapter 2.

## Tightness

Irreducibility cannot be dropped. Take $A = \begin{bmatrix} 1 & \varepsilon \\ \varepsilon & 2 \end{bmatrix}$, whose graph has two loops and no arc between the nodes. Then $(0, \varepsilon)$ is an eigenvector for the eigenvalue 1 and $(\varepsilon, 0)$ is an eigenvector for the eigenvalue 2. So the eigenvalue is not unique, the eigenvectors are not finite, and $x(k) = (x_1(0) + k, x_2(0) + 2k)$ grows at two different rates. The rates of a reducible matrix form a cycle time vector, which can have different entries (Heidergott et al. 2006, Chapter 3).

The bound in Step 5 cannot be replaced by convergence of $x(k) - k\lambda$ in general: in the example the difference keeps switching between two values, because the cyclicity is 2.

## History

Cuninghame-Green studied the max-plus eigenvalue problem for models of industrial processes in the 1960s and collected the theory of max and plus on matrices in his 1979 book. Cohen, Dubois, Quadrat and Viot (1985) gave the linear system view of discrete event systems in max-plus algebra and proved the periodic behavior of matrix powers. Baccelli, Cohen, Olsder and Quadrat (1992) presented the full theory, and Heidergott, Olsder and van der Woude (2006) gave a textbook account with applications to railway timetables. Karp (1978) gave the minimum cycle mean algorithm independently, in graph theory.

## References
