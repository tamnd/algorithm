---
tag: E2XSG7
kind: definition
slug: max-plus-algebra
name: Max-plus algebra
aliases:
- max-plus semiring
- maxplus algebra
area: control/discrete-event-and-hybrid-systems
level: core
summary: "The reals with minus infinity, where addition is max and multiplication is +. Matrix powers give longest paths, and timed synchronization becomes a linear system."
prereqs: [directed-graph]
see_also: [max-plus-eigenvalue-theorem, timed-event-graph, min-plus-matrix-multiplication, karp-minimum-mean-cycle, longest-path-problem, floyd-warshall, critical-path-method, discrete-event-system]
sources:
  - book: isbn:9780471936091
    title: François Baccelli, Guy Cohen, Geert Jan Olsder and Jean-Pierre Quadrat, Synchronization and Linearity, An Algebra for Discrete Event Systems, Wiley, 1992
    locator: the chapter on max-plus algebra (dioids, matrices over R_max, the precedence graph and the star operation)
  - book: isbn:9780691117638
    title: Bernd Heidergott, Geert Jan Olsder and Jacob van der Woude, Max Plus at Work, Princeton University Press, 2006
    locator: Chapter 1, Max-Plus Algebra
  - book: isbn:9783540091134
    title: Raymond Cuninghame-Green, Minimax Algebra, Lecture Notes in Economics and Mathematical Systems 166, Springer, 1979
    locator: the algebra of max and plus on matrices, and the connection with longest paths
---

Max-plus algebra is the set $\mathbb{R}_{\max} = \mathbb{R} \cup \{-\infty\}$ with the operations $a \oplus b = \max(a, b)$ and $a \otimes b = a + b$. In this algebra, max plays the role of addition and ordinary addition plays the role of multiplication. Matrix products then compute longest paths in a weighted [directed graph](/directed-graph/). Systems where an event waits for the last of several earlier events, such as a machine that starts when both of its input parts have arrived, become linear: $x(k+1) = A \otimes x(k)$. This is the basis of the [timed event graph](/timed-event-graph/) model and of the [max-plus eigenvalue theorem](/max-plus-eigenvalue-theorem/). The min-plus algebra, with min and $+$, is the same structure under $x \mapsto -x$; it computes shortest paths and is the subject of [min-plus matrix multiplication](/min-plus-matrix-multiplication/).

## Definition

The max-plus semiring is $\mathbb{R}_{\max} = (\mathbb{R} \cup \{-\infty\}, \oplus, \otimes, \varepsilon, e)$ with

$$a \oplus b = \max(a, b), \qquad a \otimes b = a + b, \qquad \varepsilon = -\infty, \qquad e = 0,$$

where $-\infty + a = -\infty$ for every $a$. It satisfies these laws for all $a, b, c$:

- $\oplus$ is associative and commutative, with zero element $\varepsilon$: $a \oplus \varepsilon = a$.
- $\otimes$ is associative and commutative, with unit element $e$: $a \otimes e = a$.
- $\otimes$ distributes over $\oplus$: $a \otimes (b \oplus c) = (a \otimes b) \oplus (a \otimes c)$, because $a + \max(b, c) = \max(a + b, a + c)$.
- $\varepsilon$ is absorbing for $\otimes$: $a \otimes \varepsilon = \varepsilon$.
- $\oplus$ is idempotent: $a \oplus a = a$.

A semiring with an idempotent addition is called a dioid. Each $a \ne \varepsilon$ has the multiplicative inverse $-a$, so $\mathbb{R}_{\max}$ is an idempotent semifield. The order $a \preceq b \iff a \oplus b = b$ is the usual order of the reals. Powers are $a^{\otimes k} = k a$.

**Matrices.** For $A, B \in \mathbb{R}_{\max}^{n \times m}$ and $C \in \mathbb{R}_{\max}^{m \times p}$,

$$(A \oplus B)_{ij} = \max(A_{ij}, B_{ij}), \qquad (A \otimes C)_{ij} = \max_{k} \left(A_{ik} + C_{kj}\right).$$

The identity matrix $E$ has $e = 0$ on the diagonal and $\varepsilon$ elsewhere. Matrix $\otimes$ is associative and distributes over $\oplus$, but it is not commutative.

**The graph of a matrix.** For a square $A \in \mathbb{R}_{\max}^{n \times n}$, the precedence graph $\mathcal{G}(A)$ has the nodes $1, \dots, n$ and an arc from $j$ to $i$ with weight $A_{ij}$ whenever $A_{ij} \ne \varepsilon$. (This follows Baccelli et al. 1992 and Heidergott et al. 2006; some books reverse the arcs.) By induction on $k$,

$$\left(A^{\otimes k}\right)_{ij} = \text{the maximum weight of a path of length } k \text{ from } j \text{ to } i,$$

and $\varepsilon$ if there is no such path. $A$ is irreducible if $\mathcal{G}(A)$ is strongly connected.

**The star.** $A^+ = A \oplus A^{\otimes 2} \oplus A^{\otimes 3} \oplus \cdots$ and $A^* = E \oplus A^+$. If every circuit of $\mathcal{G}(A)$ has weight at most 0, a longest path can skip every circuit, so the series stops: $A^* = E \oplus A \oplus \cdots \oplus A^{\otimes (n-1)}$ and $(A^+)_{ij}$ is the weight of a longest path from $j$ to $i$. If some circuit has positive weight, the entries on it grow without bound. When the star is finite, the equation $x = A \otimes x \oplus b$ has the least solution $x = A^* \otimes b$.

## Examples and non-examples

**Scalars.** $3 \oplus 5 = 5$, $3 \otimes 5 = 8$, $3 \oplus \varepsilon = 3$, $7 \otimes \varepsilon = \varepsilon$, $5^{\otimes 3} = 15$ and $(-2) \otimes 2 = 0 = e$.

**A matrix and its powers.** Take

$$A = \begin{bmatrix} 3 & 7 \\ 2 & 4 \end{bmatrix}.$$

Its graph has a loop at node 1 with weight 3, a loop at node 2 with weight 4, an arc $2 \to 1$ with weight 7 and an arc $1 \to 2$ with weight 2. Then

$$A^{\otimes 2} = \begin{bmatrix} \max(3+3, 7+2) & \max(3+7, 7+4) \\ \max(2+3, 4+2) & \max(2+7, 4+4) \end{bmatrix} = \begin{bmatrix} 9 & 11 \\ 6 & 9 \end{bmatrix}.$$

Entry $(1, 1)$ is the circuit $1 \to 2 \to 1$ of weight $2 + 7 = 9$, which beats twice the loop at node 1 ($6$). Further powers are $A^{\otimes 3} = \begin{bmatrix} 13 & 16 \\ 11 & 13 \end{bmatrix}$ and $A^{\otimes 4} = \begin{bmatrix} 18 & 20 \\ 15 & 18 \end{bmatrix} = 9 \otimes A^{\otimes 2}$. The growth of 9 every two steps is the maximum cycle mean $4.5$, as the [max-plus eigenvalue theorem](/max-plus-eigenvalue-theorem/) says.

**A star.** Let $B = (-4.5) \otimes A = \begin{bmatrix} -1.5 & 2.5 \\ -2.5 & -0.5 \end{bmatrix}$. Its circuits have weights $-1.5$, $-0.5$ and $0$, all at most 0, so $B^+ = B \oplus B^{\otimes 2} = \begin{bmatrix} 0 & 2.5 \\ -2.5 & 0 \end{bmatrix}$ and $B^* = B^+$ (the diagonal is already 0).

**A linear recurrence.** With $x(0) = (0, 0)$, the recurrence $x(k+1) = A \otimes x(k)$ gives $x(1) = (7, 4)$, $x(2) = (11, 9)$, $x(3) = (16, 13)$. Read $x_i(k)$ as the time of the $k$-th event at node $i$: each event waits for the latest of its predecessors plus a delay. This is the [timed event graph](/timed-event-graph/) reading.

**Non-examples.**

- $(\mathbb{R}, \max, +)$ without $-\infty$ has no zero element for $\oplus$, so it is not a semiring in the sense above, and matrices cannot express a missing arc.
- $\mathbb{R}_{\max}$ is not a ring: no element except $\varepsilon$ has an additive inverse. If $a \oplus b = \varepsilon$, then $a = b = \varepsilon$. So the equation $a \oplus x = b$ has a solution only when $a \preceq b$, and every $x \preceq b$ is a solution when $a = b$. Methods that need subtraction, such as Gaussian elimination, do not carry over.
- $(\mathbb{R} \cup \{\pm\infty\}, \max, \min)$ is the bottleneck algebra. It is a dioid too, but its matrix products compute widest paths, not longest paths.
- The min-plus semiring $(\mathbb{R} \cup \{+\infty\}, \min, +)$ is not a different theory: $x \mapsto -x$ maps it onto $\mathbb{R}_{\max}$. The max-times semiring on the nonnegative reals is also isomorphic, through $x \mapsto \log x$.

## Related definitions

- [Max-plus eigenvalue theorem](/max-plus-eigenvalue-theorem/): an irreducible matrix has exactly one eigenvalue, its maximum cycle mean, which [Karp's algorithm](/karp-minimum-mean-cycle/) computes.
- [Timed event graph](/timed-event-graph/): the class of timed Petri nets whose firing times obey $x(k+1) = A \otimes x(k)$.
- [Min-plus matrix multiplication](/min-plus-matrix-multiplication/) and [Floyd-Warshall](/floyd-warshall/): the min-plus product and the star of a matrix give all pairs shortest paths. The star above is the same computation in max-plus form.
- [Longest path problem](/longest-path-problem/) and [critical path method](/critical-path-method/): on an acyclic graph, the longest paths from the max-plus star give the earliest start times of a project.
- [Discrete event system](/discrete-event-system/): the general model class; max-plus models cover the part where all choices are fixed and only synchronization remains.

## References
