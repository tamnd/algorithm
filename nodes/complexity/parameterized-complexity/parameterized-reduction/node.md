---
tag: 15NJ5Y
kind: definition
slug: parameterized-reduction
name: Parameterized reduction
aliases:
- FPT reduction
- fpt-reduction
area: complexity/parameterized-complexity
level: advanced
summary: "Maps (x, k) to an equivalent (x', k') in time f(k) |x|^O(1), with k' bounded by a function of k alone. FPT and every W[t] are closed under it."
prereqs: [parameterized-problem, fixed-parameter-tractable, polynomial-time-reduction]
see_also: [w-hardness, w-hierarchy, polynomial-parameter-transformation, parameterized-clique, parameterized-independent-set, parameterized-dominating-set, turing-reduction, fine-grained-reduction]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (parameterized reductions and the first W[1]-hardness proofs)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 2, Reductions and Parameterized Intractability
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: the chapters on parameterized reductions and the W hierarchy
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the parameterized reductions and the classes closed under them
---

A parameterized reduction maps an instance $(x, k)$ of one [parameterized problem](/parameterized-problem/) to an instance $(x', k')$ of another, with the same answer. It may use time $f(k) \cdot |x|^{O(1)}$, and the new parameter $k'$ must be bounded by a function of $k$ alone. These two conditions make [FPT](/fixed-parameter-tractable/) closed under the reduction, so it is the reduction that defines [W[t]-hardness](/w-hardness/). A [polynomial-time reduction](/polynomial-time-reduction/) of the classical problems is often not a parameterized reduction, because it does not control the parameter.

## Definition

A parameterized problem is a set $Q \subseteq \Sigma^* \times \mathbb{N}$, where the second part of a pair $(x, k)$ is the [parameter](/parameter/). Write $|x|$ for the length of $x$. Machines are [multitape Turing machines](/multitape-turing-machine/); the class FPT and the reductions below do not change under a polynomial-time simulation by another standard model.

Let $Q$ and $Q'$ be parameterized problems. A *parameterized reduction* (also *fpt-reduction*) from $Q$ to $Q'$ is an algorithm $R$ that maps each pair $(x, k)$ to a pair $(x', k')$ such that, for computable functions $f$ and $g$ and a constant $c$:

1. $(x, k) \in Q$ if and only if $(x', k') \in Q'$;
2. $R$ runs in time at most $f(k) \cdot |x|^c$;
3. $k' \le g(k)$.

Write $Q \le_{\mathrm{fpt}} Q'$. Condition 3 is the important one. The new parameter may grow, but only by an amount that depends on $k$, never on $|x|$.

**Closure of FPT.** If $Q \le_{\mathrm{fpt}} Q'$ and $Q'$ is in FPT, then $Q$ is in FPT. Proof: let $A'$ decide $Q'$ in time $h(k') \cdot |x'|^d$, and take $h$ and $g$ nondecreasing (replace each by its running maximum). On input $(x, k)$, run $R$ and then $A'$. Since $R$ writes at most one symbol per step, $|x'| \le f(k) |x|^c$. The total time is at most

$$f(k) |x|^c + h(g(k)) \cdot \big(f(k) |x|^c\big)^d = f(k) |x|^c + h(g(k)) f(k)^d \cdot |x|^{cd},$$

which has the form $f^*(k) \cdot |x|^{c^*}$ with $f^*$ computable. Without condition 3 the step fails: $h(k')$ could be $2^{k'}$ with $k' = |x|$.

**Transitivity.** If $Q \le_{\mathrm{fpt}} Q'$ by $(f_1, g_1, c_1)$ and $Q' \le_{\mathrm{fpt}} Q''$ by $(f_2, g_2, c_2)$, the composition is a parameterized reduction with new parameter at most $g_2(g_1(k))$ and time $f_1(k) |x|^{c_1} + f_2(g_1(k)) (f_1(k) |x|^{c_1})^{c_2}$, by the same computation. So "$Q$ is at least as hard as $Q'$" is a preorder, as for [many-one reductions](/many-one-reducibility/).

## Examples and non-examples

**Clique and independent set.** Map $(G, k)$ to $(\overline{G}, k)$, where $\overline{G}$ is the [complement graph](/complement-graph/). A set is a clique in $G$ exactly when it is independent in $\overline{G}$. The map takes $O(n^2)$ time and keeps $k' = k$, so it is a parameterized reduction in both directions between [p-Clique](/parameterized-clique/) and [p-Independent-Set](/parameterized-independent-set/).

**Clique to multicolored clique.** Given $(G, k)$, build $G'$ with the vertices $(i, v)$ for $1 \le i \le k$ and $v \in V(G)$, and join $(i, u)$ to $(j, v)$ when $i \ne j$, $u \ne v$ and $uv \in E(G)$. The classes $V_i = \{(i, v)\}$ are the colors. A $k$-clique $\{v_1, \ldots, v_k\}$ of $G$ gives the multicolored clique $\{(1, v_1), \ldots, (k, v_k)\}$. Conversely, a clique with one vertex $(i, v_i)$ from each class has $v_i \ne v_j$ and $v_i v_j \in E$ for all $i \ne j$, so $\{v_1, \ldots, v_k\}$ is a $k$-clique of $G$. The map takes $O(k^2 n^2)$ time and keeps $k' = k$. For the house graph (a square 0, 1, 2, 3 and a roof vertex 4 joined to 0 and 1) and $k = 3$, $G'$ has 15 vertices and 36 edges. It has 6 multicolored triangles, one for each order of the single triangle $\{0, 1, 4\}$ of $G$. Multicolored clique is the usual source problem for W[1]-hardness proofs, because each color class acts as a gadget for one choice.

**Dominating set to set cover.** Map a graph $G$ and $k$ to the universe $V$, the family of closed neighborhoods $N[v]$ for $v \in V$, and the same $k$. A set $D$ of vertices dominates $G$ exactly when the sets $N[v]$ for $v \in D$ cover $V$. This is a parameterized reduction from [p-Dominating-Set](/parameterized-dominating-set/) to set cover with $k$ sets.

**Non-example: a lost parameter.** The map $(G, k) \mapsto (G, n - k)$ is a polynomial-time reduction from [vertex cover](/parameterized-vertex-cover/) to independent set, because $S$ is a vertex cover exactly when $V \setminus S$ is independent. It is not a parameterized reduction: the new parameter $n - k$ depends on the size of $G$. Indeed vertex cover with parameter $k$ is FPT, while independent set with parameter $k$ is W[1]-complete. The same thing happens with every "dual" parameter: the complement of a small solution is a large one.

**Non-example: too much time.** The map that solves $(G, k)$ for clique by trying all $\binom{n}{k}$ sets and then writes a fixed yes-instance or no-instance of a trivial problem keeps the answer and the parameter. It runs in time about $n^k$, which is not of the form $f(k) \cdot n^c$, so it is not a parameterized reduction. If time $n^{O(k)}$ were allowed, every problem in [XP](/xp/) would reduce to a trivial problem, and the notion of hardness would be empty.

**Non-example: a classical NP-hardness proof.** The usual reduction from [3-SAT](/3-sat/) to clique builds a graph with one group of vertices for each clause and sets $k$ to the number of clauses. If 3-SAT is given the parameter "number of variables", the new $k$ is not bounded by a function of it, because the number of clauses can be much larger. A classical reduction gives a parameterized one only when its new parameter happens to depend on the old parameter alone.

## Related definitions

- *[Polynomial parameter transformation](/polynomial-parameter-transformation/).* The map runs in polynomial time and $k' \le k^{O(1)}$. It is a special parameterized reduction. Kernel lower bounds move along it, because it keeps polynomial kernels.
- *FPT Turing reduction.* An algorithm in time $f(k) \cdot |x|^{O(1)}$ with an oracle for $Q'$, where every query $(x', k')$ has $k' \le g(k)$. It is the parameterized form of a [Turing reduction](/turing-reduction/). [Parameterized counting complexity](/parameterized-counting-complexity/) uses it, because many counting reductions ask several queries and combine the answers.
- *Para-L reduction.* A parameterized reduction computed in space $f(k) + O(\log |x|)$. It is the reduction for classes inside FPT, such as [para-L](/para-l/).
- *[W[t]-hardness](/w-hardness/).* A problem $Q$ is W[t]-hard if every problem in W[t] reduces to $Q$ by a parameterized reduction. The classes of the [W-hierarchy](/w-hierarchy/) are defined as closures under this reduction.
- *[Fine-grained reduction](/fine-grained-reduction/).* It also controls the exact running time, but it has no parameter. The ETH lower bounds for clique use reductions that control $k'$ linearly, $k' = O(k)$, which is stronger than condition 3.

## References
