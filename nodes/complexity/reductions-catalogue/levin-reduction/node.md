---
tag: F468J9
kind: definition
slug: levin-reduction
name: Levin reduction
aliases:
- Levin's reduction
- witness-preserving reduction
area: complexity/reductions-catalogue
level: advanced
summary: A Karp reduction between search problems together with polynomial-time maps that turn solutions of the image back into solutions of the input, and usually also forward.
prereqs: [polynomial-time-reduction, search-problem]
see_also: [parsimonious-reduction, cook-levin-theorem, search-to-decision-reduction, fnp, transitivity-of-reductions, turing-reduction, self-reducibility]
sources:
  - paper: "\"Universal sequential search problems\""
    title: "Leonid A. Levin, Universal sequential search problems, Problemy Peredachi Informatsii 9(3) (1973), 115-116; English translation in Problems of Information Transmission 9(3) (1973), 265-266"
    locator: the notion of a reduction between search problems that also transforms solutions, and the universal search problems
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.3.6, the definition of a Levin reduction and the remark that the Cook-Levin reduction is one; Section 2.5, decision versus search
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Section 2.3.1, definitions of Karp reductions and Levin reductions between search problems
---

A Levin reduction is a [Karp reduction](/polynomial-time-reduction/) between two [search problems](/search-problem/) that also carries solutions across in polynomial time. It maps an instance $x$ to an instance $f(x)$, and it comes with a map $g$ that turns any solution of $f(x)$ into a solution of $x$, and usually a map $h$ that turns any solution of $x$ into a solution of $f(x)$. A Levin reduction to a problem with an efficient solver gives an efficient solver that finds solutions, not only answers yes or no. Levin (1973) used reductions of this kind for his universal search problems, independently of Cook.

## Definition

A search problem is given by a relation $R \subseteq \{0,1\}^* \times \{0,1\}^*$; a string $w$ with $(x, w) \in R$ is a *solution* (witness) for the instance $x$. Write $R(x) = \{w : (x, w) \in R\}$ and $L_R = \{x : R(x) \neq \emptyset\}$ for the decision problem. In the cases of interest $R$ is an NP relation: $|w| \le q(|x|)$ for a polynomial $q$, and membership $(x, w) \in R$ is decidable in polynomial time ([certificate](/certificate/)).

**Definition.** Let $R$ and $R'$ be relations. A *Levin reduction* from $R$ to $R'$ is a triple $(f, g, h)$ of polynomial-time computable functions such that, for every $x$:

1. **(instances)** $x \in L_R \iff f(x) \in L_{R'}$;
2. **(back)** for every $w' \in R'(f(x))$: $\ g(x, w') \in R(x)$;
3. **(forward)** for every $w \in R(x)$: $\ h(x, w) \in R'(f(x))$.

Condition 1 says that $f$ is a Karp reduction from $L_R$ to $L_{R'}$. Conditions 2 and 3 imply condition 1, since a solution on either side gives a solution on the other side.

Two versions are in use. Arora and Barak (Section 2.3.6) require all three maps. Goldreich (Section 2.3.1) requires only $f$ and $g$, with condition 1, because the backward map is what turns a solver for $R'$ into a solver for $R$. The forward map matters when a known solution of $x$ must be turned into a solution of $f(x)$.

Note that $g$ must work for *every* solution $w'$ of $f(x)$, not only for the solutions that $h$ produces.

**Composition.** If $(f_1, g_1, h_1)$ reduces $R$ to $R'$ and $(f_2, g_2, h_2)$ reduces $R'$ to $R''$, then

$$f(x) = f_2(f_1(x)), \quad g(x, w'') = g_1\big(x,\ g_2(f_1(x), w'')\big), \quad h(x, w) = h_2\big(f_1(x),\ h_1(x, w)\big)$$

is a Levin reduction from $R$ to $R''$. Each map runs in polynomial time because $|f_1(x)|$ and the intermediate solutions have polynomial length ([transitivity of reductions](/transitivity-of-reductions/)).

## Examples and non-examples

### 3-SAT to independent set, with both maps

The standard reduction $f$ from [3-SAT](/3-sat/) to independent set builds a graph $G_\varphi$ with one vertex for each literal occurrence, a triangle on each clause and an edge between each pair of opposite literals $x_i$, $\neg x_i$, and asks for an independent set of size $m$, the number of clauses.

- $h(\varphi, a)$: for each clause, take the vertex of its first literal that is true under the assignment $a$.
- $g(\varphi, S)$: for an independent set $S$ of size $m$, set each variable $x_i$ to $1$ if the literal $x_i$ is in $S$ and to $0$ otherwise.

$h$ gives an independent set because the picked literals are in different triangles and are all true, so no two are opposite. $g$ gives a satisfying assignment because $S$ has one vertex in each triangle, no conflict edge lies inside $S$, and so every picked literal is true under $g(\varphi, S)$: a positive picked literal is set to $1$, and for a negative picked literal $\neg x_i$, the literal $x_i$ is not in $S$, so $x_i = 0$.

For $\varphi = (x_1 \lor x_2 \lor \neg x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor \neg x_3)$, which has $5$ satisfying assignments ($000$, $010$, $011$, $101$, $110$ as $x_1 x_2 x_3$):

| direction | input | output |
| --- | --- | --- |
| $h$ | $a = 110$ | the occurrences $x_1$, $x_2$, $\neg x_3$ (clauses 1, 2, 3) |
| $h$ | $a = 101$ | the occurrences $x_1$, $x_3$, $\neg x_2$ |
| $h$ | $a = 000$ | the occurrences $\neg x_3$, $\neg x_1$, $\neg x_1$ |
| $g$ | the occurrences $x_2$, $x_3$, $\neg x_1$ | $a = 011$ |

On all $164$ formulas with $1$ to $3$ clauses on $x_1, x_2, x_3$ (each clause with three different variables), $h$ always returns an independent set of size $m$ and that $g$ always returns a satisfying assignment.

### Other examples

- **Cook-Levin.** The reduction in the [Cook-Levin theorem](/cook-levin-theorem/) from any NP relation to SAT is a Levin reduction: from an accepting computation of the verifier one reads off a satisfying assignment, and the certificate is part of every satisfying assignment (Arora and Barak, Section 2.3.6). So SAT is complete for [FNP](/fnp/) under Levin reductions.
- **The trivial identity.** For every relation, $(f, g, h) = (x \mapsto x, (x, w) \mapsto w, (x, w) \mapsto w)$ is a Levin reduction to itself.

### Non-example

Let COMPOSITE be the set of composite numbers, with relation $R = \{(N, d) : 1 < d < N,\ d \text{ divides } N\}$. Primality is in P ([AKS primality test](/aks-primality-test/)), so the map $f(N) = (x_1)$ if $N$ is composite and $f(N) = (x_1) \land (\neg x_1)$ otherwise is a Karp reduction from COMPOSITE to SAT. It is not a Levin reduction unless [integer factorization](/integer-factorization/) has a polynomial-time algorithm for finding some factor: the target formula has the single solution $x_1 = 1$, which contains no information about $N$, so $g(N, 1)$ would have to find a divisor of $N$ alone. This shows that a Karp reduction can lose all the information in the solutions.

## Related definitions

- **[Parsimonious reduction](/parsimonious-reduction/)**: a Karp reduction that keeps the number of solutions. Many Levin reductions are parsimonious, with $h$ a bijection and $g$ its inverse; the 3-SAT example above is not ($5$ assignments, $12$ independent sets of size $3$).
- **[Search-to-decision reduction](/search-to-decision-reduction/)**: solves a search problem with a decision oracle. Combining a Levin reduction to SAT with the search-to-decision reduction for SAT shows that if P = NP then every NP search problem is solvable in polynomial time (Arora and Barak, Section 2.5).
- **[Self-reducibility](/self-reducibility/)**: Goldreich proves that the search problem of every NP-complete set is self-reducible by a Levin reduction to SAT.
- **[Cook reduction](/turing-reduction/)** between search problems: a polynomial-time machine with an oracle that returns solutions. A Levin reduction is the one-query special case.
- **Universal search.** Levin (1973) also gave a search algorithm for any NP relation that runs all programs in parallel with exponentially decreasing shares of time and checks each output. Its running time is within a constant factor of that of any fixed correct program, plus the time to check a solution.

## References
