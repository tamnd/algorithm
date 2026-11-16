---
tag: 3NQ1V4
kind: theorem
slug: clique-w1-completeness
name: Clique is W[1]-complete
aliases:
- Downey-Fellows theorem
area: complexity/parameterized-complexity
level: advanced
summary: "Clique with the clique size k as parameter is W[1]-complete under parameterized reductions (Downey and Fellows 1995), so it has no FPT algorithm unless FPT = W[1]."
prereqs: [w-hierarchy, parameterized-reduction, clique-problem]
see_also: [parameterized-clique, parameterized-independent-set, w-hardness, weighted-satisfiability, fpt-w1-conjecture, clique-inapproximability, parameterized-inapproximability, maximum-clique]
sources:
  - paper: doi:10.1016/0304-3975(94)00097-3
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness II: on completeness for W[1], Theoretical Computer Science 141(1-2), 109-131 (1995)"
    locator: the main theorem, independent set is W[1]-complete, with clique by the complement graph
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the definition of W[t] by weft and the normalization of weighted circuits
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (the proof that clique and independent set are W[1]-hard, and multicolored clique), and Theorem 14.21 (no f(k) n^o(k) algorithm under ETH)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 6, The First Level of the Hierarchies (W[1]-completeness of clique and of weighted q-CNF satisfiability)
  - paper: doi:10.1016/j.jcss.2006.04.007
    title: "Jianer Chen, Xiuzhen Huang, Iyad A. Kanj and Ge Xia, Strong computational lower bounds via parameterized complexity, Journal of Computer and System Sciences 72(8), 1346-1367 (2006)"
    locator: the lower bound f(k) n^o(k) for clique and independent set under ETH
---

Clique with the clique size $k$ as the parameter is W[1]-complete: it is in the class $\mathsf{W}[1]$ of the [W-hierarchy](/w-hierarchy/), and every problem in $\mathsf{W}[1]$ has a [parameterized reduction](/parameterized-reduction/) to it. Downey and Fellows proved the result in 1995 for independent set, and the [complement graph](/complement-graph/) moves it to clique. It is the first and most used W[1]-hardness result: it says that clique has no algorithm in time $f(k) \cdot n^{O(1)}$ unless $\mathsf{FPT} = \mathsf{W}[1]$. The membership half is short and is proved in full below; the hardness half is given as a sketch with its source.

## Statement

The problem is [p-Clique](/parameterized-clique/): given a graph $G$ with $n$ vertices as an adjacency matrix and an integer $k$, with parameter $k$, decide whether $G$ has a clique of size $k$. The independent set problem p-Independent-Set is the same with "independent set" in place of "clique".

**Theorem (Downey and Fellows 1995).** p-Clique and p-Independent-Set are W[1]-complete under parameterized reductions.

Here $\mathsf{W}[1]$ is the class of parameterized problems that reduce to weighted satisfiability of circuits of weft at most 1 and constant depth (see [weighted satisfiability](/weighted-satisfiability/)). A gate is small when its fan-in is at most 2 and large otherwise, and the weft is the largest number of large gates on a path from an input to the output.

## In plain words

Finding a group of a given size in which everyone knows everyone else is as hard as any problem in a whole class of "choose a few items" problems. If someone finds a method whose cost grows only mildly with the network and possibly fast with the group size, the same method would work for every problem in that class. Experts think that this will not happen, so they treat the group problem as having no such method.

## Proof

The proof has two parts: clique is in W[1], and clique is W[1]-hard. A short reduction between clique and independent set shows that each statement for one problem gives the same statement for the other.

### Clique and independent set are equivalent

Map $(G, k)$ to $(\overline{G}, k)$, where $\overline{G}$ has the same vertices and an edge exactly where $G$ has none. A set $S$ is a clique in $G$ if and only if no pair in $S$ is an edge of $\overline{G}$, that is, if and only if $S$ is independent in $\overline{G}$. Both directions hold for every set, so $(G, k)$ is a yes-instance of clique if and only if $(\overline{G}, k)$ is a yes-instance of independent set. The map takes $O(n^2)$ time, keeps $k' = k$, and is its own inverse. So it is a parameterized reduction in both directions.

### Membership: clique is in W[1]

Let $(G, k)$ be an instance. If $G$ is complete, the answer is yes exactly when $k \le n$, and the reduction outputs a fixed yes-instance or no-instance. Otherwise build the circuit $C_G$:

- one input $x_v$ for each vertex $v$;
- for each pair $\{u, v\}$ that is not an edge of $G$, a gate $g_{uv} = \neg x_u \vee \neg x_v$, made of two NOT gates and one OR gate of fan-in 2;
- one AND gate over all the gates $g_{uv}$, which is the output.

Every path from an input to the output passes one NOT gate, one OR gate and the AND gate. Only the AND gate can be large, so $C_G$ has weft at most 1 and depth 3. It has $O(n^2)$ gates and is built in time $O(n^2)$. The reduction outputs $(C_G, k)$, so $k' = k$.

*If $G$ has a clique $S$ of size $k$, then $C_G$ has a satisfying assignment of weight $k$.* Set $x_v = 1$ for $v \in S$ and $x_v = 0$ otherwise. The weight is $|S| = k$. For a non-edge $\{u, v\}$, the vertices $u$ and $v$ are not both in $S$, because $S$ is a clique. So one of $x_u, x_v$ is 0 and $g_{uv} = 1$. All the inputs of the AND gate are 1, and the circuit outputs 1.

*If $C_G$ has a satisfying assignment $a$ of weight $k$, then $G$ has a clique of size $k$.* Let $S = \{v : a_v = 1\}$; then $|S| = k$. Take any two vertices $u \ne v$ in $S$. If $\{u, v\}$ were a non-edge, the gate $g_{uv}$ would get $\neg 1 \vee \neg 1 = 0$, and the AND gate would output 0. This contradicts the choice of $a$. So every pair in $S$ is an edge, and $S$ is a clique of size $k$.

So p-Clique reduces to weighted satisfiability for circuits of weft 1 and depth 3, and p-Clique is in W[1]. By the reduction above, p-Independent-Set is in W[1] as well. As a weighted formula, $C_G$ is the antimonotone 2-CNF formula $\bigwedge_{uv \notin E} (\neg x_u \vee \neg x_v)$.

### Hardness: every problem in W[1] reduces to independent set (sketch)

This part is a sketch. The full proof is the main theorem of Downey and Fellows, Theoretical Computer Science 141 (1995); textbook versions are in Chapter 13 of Cygan et al. and Chapter 6 of Flum and Grohe. Let $Q$ be in $\mathsf{W}[1]$. By definition, $Q$ reduces to weighted satisfiability for circuits of weft 1 and depth at most $d$, for some constant $d$. By transitivity, it is enough to reduce that problem to independent set with a new parameter bounded by a function of $k$ and $d$. The proof has two steps.

1. *Normalization to bounded clauses.* In a circuit of weft 1 and depth $d$, a gate below the large gate depends on at most $2^d$ inputs, and only a bounded number of small gates lie above the large gates. The first step rewrites such a circuit as a weighted q-CNF formula, with $q$ and the new parameter bounded by functions of $d$ and $k$. Large OR gates are the difficult case, because a q-CNF formula has only one large gate, the AND at the top; the reduction adds new variables that record which input of such an OR is true.
2. *From q-CNF to independent set.* The second step reduces weighted q-CNF satisfiability to weighted antimonotone 2-CNF satisfiability, which is independent set: one clause $\neg x_u \vee \neg x_v$ for each edge $uv$. The construction builds a graph in which an independent set of a size that depends only on $k$ and $q$ encodes an assignment of weight $k$ that satisfies every clause.

The sketch leaves out the exact construction in both steps, the proof that each step keeps the answer in both directions, and the bounds on the new parameter. With these steps, every problem in W[1] reduces to independent set, and by the complement map to clique.

### Worked example

Let $G$ be the house graph: a square with vertices 0, 1, 2, 3 in order and a roof vertex 4 joined to 0 and 1. It has 6 edges and the 4 non-edges 02, 13, 24 and 34. Take $k = 3$.

- *Membership circuit.* $C_G$ has 4 OR gates, $\neg x_0 \vee \neg x_2$, $\neg x_1 \vee \neg x_3$, $\neg x_2 \vee \neg x_4$ and $\neg x_3 \vee \neg x_4$, under one AND gate. The clique $\{0, 1, 4\}$ maps to the assignment $x_0 = x_1 = x_4 = 1$, $x_2 = x_3 = 0$, of weight 3, which satisfies all four gates. In the other direction, $C_G$ has exactly one satisfying assignment of weight 3, and its set of ones is $\{0, 1, 4\}$, the only triangle of $G$. For weight 2 there are 6 satisfying assignments, one for each edge, and for weight 4 there are none.
- *Complement.* $\overline{G}$ has the 4 edges 02, 13, 24 and 34. The set $\{0, 1, 4\}$ is independent in $\overline{G}$, and it is the only independent set of size 3 there.
- *Multicolored clique.* The map to multicolored clique uses the vertices $(i, v)$ for $i = 1, 2, 3$ and $v = 0, \ldots, 4$, with $(i, u)$ joined to $(j, v)$ when $i \ne j$ and $uv$ is an edge of $G$. The new graph has 15 vertices and 36 edges. The clique $\{0, 1, 4\}$ maps to $\{(1, 0), (2, 1), (3, 4)\}$. The new graph has 6 multicolored triangles, one for each order of $\{0, 1, 4\}$, and each maps back to $\{0, 1, 4\}$.

## Consequences

- *No FPT algorithm unless FPT = W[1].* If p-Clique had an algorithm in time $f(k) \cdot n^{O(1)}$, every problem in W[1] would have one, because FPT is closed under parameterized reductions. See the [FPT versus W[1] conjecture](/fpt-w1-conjecture/).
- *A source for hardness proofs.* The same holds for p-Independent-Set and for multicolored clique (the map in the worked example works for every $k$). Most W[1]-hardness proofs in the literature start from multicolored clique, because each color class is a gadget for one choice.
- *Weighted q-CNF satisfiability is W[1]-complete* for each fixed $q \ge 2$, since it is between clique and independent set in the chain of reductions above.
- *Approximation.* The exact problem is hard; whether a constant-factor approximation of the clique size is FPT is the subject of [parameterized inapproximability](/parameterized-inapproximability/). The classical inapproximability of [maximum clique](/maximum-clique/) is on [clique inapproximability](/clique-inapproximability/).

## Tightness

- *The XP algorithm.* Trying all $\binom{n}{k}$ sets takes time $O(n^k k^2)$, so p-Clique is in [XP](/xp/). W[1]-hardness does not rule this out, and it does not say how the exponent must grow.
- *Fast matrix multiplication.* Nešetřil and Poljak (1985) solve p-Clique in time $O(n^{\omega k/3})$ when 3 divides $k$, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). See [parameterized clique](/parameterized-clique/).
- *The ETH bound.* Conditional on the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), p-Clique has no algorithm in time $f(k) \cdot n^{o(k)}$ for any computable $f$ (Chen, Huang, Kanj and Xia 2006; Theorem 14.21 in Cygan et al.). This is a separate statement under a separate assumption, and it shows that the exponent of the XP algorithm must grow linearly in $k$.
- *Restricted inputs.* The hardness is for general graphs. On graphs of maximum degree $\Delta$, a clique lies in some closed neighborhood of at most $\Delta + 1$ vertices, so the problem is FPT in $\Delta$. On [planar graphs](/planar-graph/) a clique has at most 4 vertices.

## History

Downey and Fellows started the theory of fixed-parameter tractability in a series of papers in the early 1990s. Part I (SIAM Journal on Computing, 1995) defined the W-hierarchy by the weft of circuits and showed that dominating set is W[2]-complete. Part II (Theoretical Computer Science, 1995) proved that independent set, and so clique, is W[1]-complete; the main difficulty was the reduction from bounded-depth weft-1 circuits to a graph problem. Chen, Huang, Kanj and Xia (2006) later turned the reductions into running time bounds under ETH. Today the result is taught through multicolored clique, which makes most reductions from clique short.

## References
