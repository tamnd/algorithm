---
tag: 46EP4P
kind: problem
slug: weighted-satisfiability
name: Weighted satisfiability
aliases:
- WSAT
- weighted circuit satisfiability
area: complexity/parameterized-complexity
level: advanced
summary: "Decide whether a formula or circuit has a satisfying assignment with exactly k true variables, with parameter k. Its restrictions are complete for W[1], W[2], ..., W[SAT] and W[P]."
prereqs: [sat, boolean-circuit, parameterized-reduction]
see_also: [w-hierarchy, w-hardness, clique-w1-completeness, parameterized-independent-set, parameterized-dominating-set, parameterized-hitting-set, circuit-sat, k-sat]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (weighted circuit satisfiability and the definition of W[t] and W[P])
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 3 (The Class W[P]), Chapter 6 (The First Level of the Hierarchies) and Chapter 7 (The W-Hierarchy)
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the weighted satisfiability problems, the normalization to t-normalized formulas, and W[2]-completeness of weighted CNF satisfiability
  - paper: doi:10.1016/0304-3975(94)00097-3
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness II: on completeness for W[1], Theoretical Computer Science 141(1-2), 109-131 (1995)"
    locator: the main theorem, which reduces weighted q-CNF satisfiability to independent set
---

Weighted satisfiability asks whether a Boolean formula or circuit has a satisfying assignment with exactly $k$ variables set to true, where $k$ is the [parameter](/parameter/). The number of true variables is the Hamming weight of the assignment. The restrictions of the problem to circuits of bounded weft define the classes of the [W-hierarchy](/w-hierarchy/), and each class has a natural complete restriction: weighted 2-CNF satisfiability for W[1], weighted CNF satisfiability for W[2], formulas for W[SAT] and circuits for W[P]. This page is not about WalkSAT, a local search method for SAT with a similar short name.

## In plain words

You have a list of yes-or-no switches and a rule that tells you whether a setting of the switches is good. Plain satisfiability asks whether some setting is good. Here you must also turn on exactly a given number of switches, and that number is small.

If the number is small, you can try every choice of that many switches. That works, but the work grows with the number of switches raised to the power of the number you turn on. The question is whether some method avoids that growth. For simple rules the answer is yes. For most rules, nobody knows such a method, and the problem is the standard example of one that seems to have none.

## Definition

An assignment to variables $x_1, \ldots, x_n$ is a vector in $\{0, 1\}^n$. Its *weight* is the number of ones. For a class $\mathcal{C}$ of Boolean circuits (or formulas), the problem is:

**p-WEIGHTED-SAT[$\mathcal{C}$]**

- Instance: a circuit $C \in \mathcal{C}$ with $n$ input variables, given as a list of gates, and an integer $k \ge 0$.
- Parameter: $k$.
- Question: does $C$ have a satisfying assignment of weight exactly $k$?

The size of the instance is the number of gates and wires of $C$ plus the length of $k$. A yes-instance has a certificate of $k$ variable names, which takes $O(k \log n)$ bits. Weights other than "exactly $k$" give different problems: for a monotone circuit, any satisfying assignment stays satisfying when more ones are added, so "at least $k$" is the same as "exactly $k$" as long as $k \le n$.

The main cases are:

- *weighted q-CNF satisfiability*: $C$ is a CNF formula with at most $q$ literals per clause, for a fixed $q$;
- *weighted CNF satisfiability*: $C$ is a CNF formula with clauses of any length;
- *weighted t-normalized satisfiability*: $C$ is an AND of ORs of ANDs, and so on, with $t$ levels of alternation;
- *weighted formula satisfiability*: $C$ is any Boolean formula;
- *weighted circuit satisfiability*: $C$ is any Boolean circuit.

## Variants

| Restriction | Parameterized complexity, parameter $k$ |
|---|---|
| q-CNF for a fixed $q \ge 2$ | W[1]-complete |
| antimonotone 2-CNF (every literal negated) | W[1]-complete; this is [independent set](/parameterized-independent-set/) |
| monotone 2-CNF (no literal negated) | FPT; this is vertex cover with a cover of size exactly $k$ |
| CNF | W[2]-complete |
| monotone CNF | W[2]-complete; this is [hitting set](/hitting-set/) |
| t-normalized formulas, $t \ge 2$ | W[t]-complete |
| Boolean formulas | W[SAT]-complete |
| Boolean circuits | W[P]-complete |

The completeness results are by Downey and Fellows (1995), with the reductions under [parameterized reductions](/parameterized-reduction/).

Monotone and antimonotone 2-CNF behave differently. In the antimonotone case, a clause $\neg x_u \vee \neg x_v$ says "not both", so the true variables form an independent set in the graph of clauses. In the monotone case, a clause $x_u \vee x_v$ says "at least one", so the true variables form a vertex cover; a cover of size at most $k$ can be filled up to exactly $k$ when $k \le n$, and vertex cover is FPT.

With $k$ as part of the input and no parameter, even the antimonotone 2-CNF case is NP-complete, because it is the classical [independent set](/independent-set/) problem.

## Examples

Take five variables and the 3-CNF formula

$$\varphi = (x_1 \vee x_2) \wedge (\neg x_1 \vee \neg x_3) \wedge (x_3 \vee x_4) \wedge (\neg x_2 \vee \neg x_4) \wedge (x_1 \vee x_4 \vee x_5).$$

It has 3 satisfying assignments in total. By weight, they are:

| Weight $k$ | Satisfying assignments, as the set of true variables |
|---|---|
| 0, 1 | none |
| 2 | $\{x_1, x_4\}$ |
| 3 | $\{x_2, x_3, x_5\}$ and $\{x_1, x_4, x_5\}$ |
| 4, 5 | none |

So $(\varphi, 2)$ and $(\varphi, 3)$ are yes-instances, and $(\varphi, 1)$ and $(\varphi, 4)$ are no-instances. With $k = 1$ the first and third clauses need $x_1$ or $x_2$, and $x_3$ or $x_4$, which is two true variables.

A graph example. For the house graph (a square 0, 1, 2, 3 and a roof vertex 4 joined to 0 and 1), the antimonotone 2-CNF with one clause $\neg x_u \vee \neg x_v$ for each non-edge has the four clauses for the non-edges 02, 13, 24 and 34. Its weight-$k$ satisfying assignments are the cliques of size $k$: 5 of weight 1, 6 of weight 2, 1 of weight 3 (the triangle $\{0, 1, 4\}$) and none of weight 4.

## Known algorithms

- Brute force tries all $\binom{n}{k} \le n^k$ assignments of weight $k$ and evaluates $C$ on each, in time $O(n^k \cdot |C|)$. This is an [XP](/xp/) algorithm for every class of circuits, and it puts W[P] inside XP.
- For antimonotone 2-CNF, which is independent set, the reduction to [clique](/parameterized-clique/) on the complement graph and the Nešetřil and Poljak algorithm give time $O(n^{\omega k/3})$ when $3$ divides $k$, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/).
- For monotone CNF in the form of dominating set, the best known algorithm runs in time $n^{k + o(1)}$ for $k \ge 7$; see [parameterized dominating set](/parameterized-dominating-set/).
- For monotone 2-CNF, the FPT algorithms of [vertex cover](/parameterized-vertex-cover/) apply.

## Bounds

- Weighted q-CNF satisfiability is not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$, and weighted CNF satisfiability is not FPT unless $\mathsf{FPT} = \mathsf{W}[2]$.
- Conditional on the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), weighted antimonotone 2-CNF satisfiability has no algorithm in time $f(k) \cdot n^{o(k)}$ for any computable $f$, because independent set has none (Chen, Huang, Kanj and Xia, 2006). This bound is separate from the W[1]-hardness.
- All the bounds are about the parameter $k$. With the number of variables $n$ as the parameter, every case is FPT by trying all $2^n$ assignments.

## Reductions

- *From clique, k' = k.* The circuit with one clause $\neg x_u \vee \neg x_v$ for each non-edge $uv$ has the $k$-cliques as its weight-$k$ satisfying assignments. The map takes $O(n^2)$ time. It shows that clique is in W[1]; see [clique is W[1]-complete](/clique-w1-completeness/).
- *From and to independent set, k' = k.* One clause $\neg x_u \vee \neg x_v$ for each edge, and back again. This is a direct translation in both directions.
- *From and to dominating set, k' = k.* One clause $\bigvee_{u \in N[v]} x_u$ for each vertex $v$ gives a monotone CNF formula with $n$ clauses and $2m + n$ literals. This puts dominating set in W[2].
- *Weighted q-CNF to independent set.* This is the hard step of Downey and Fellows (1995, Theoretical Computer Science 141). The proof is long, and its new parameter $k'$ depends on $k$ and $q$ only.
- *Circuits of weft t to t-normalized formulas.* The normalization theorem of Downey and Fellows (1995, SIAM Journal on Computing 24) turns a circuit of weft $t$ and constant depth into a t-normalized formula with a new parameter bounded by a function of $k$ and the depth.
- *Not a parameterized reduction.* Plain [SAT](/sat/) reduces to weighted satisfiability by adding, for each variable $x_i$, a copy $y_i$ with $y_i = \neg x_i$; every satisfying assignment then has weight exactly $n$. The new parameter is $n$, so the map is a polynomial-time reduction but not a parameterized one.

## Applications

- *Definition of the hierarchy.* The classes $\mathsf{W}[t]$, $\mathsf{W}[\mathsf{SAT}]$ and $\mathsf{W}[\mathsf{P}]$ are defined as the problems that reduce to a restriction of weighted satisfiability. See [W-hierarchy](/w-hierarchy/).
- *Source problems.* Weighted q-CNF and weighted CNF satisfiability are convenient sources when a hardness proof needs a logical form instead of a graph. Most graph proofs start from multicolored clique instead.
- *Counting.* Counting the satisfying assignments of weight $k$ is the base of the counting classes, such as #W[1]; see [parameterized counting complexity](/parameterized-counting-complexity/).

## References
