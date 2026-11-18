---
tag: D6WF2Z
kind: definition
slug: universal-solution
name: Universal solution
aliases:
- universal solution of data exchange
area: databases/data-integration-and-cleaning
level: advanced
summary: "A solution to a data exchange problem that maps homomorphically into every other solution; the chase computes one when it ends."
prereqs: [schema-mapping, data-exchange-problem, chase-algorithm]
see_also: [data-exchange-core-computation, certain-answers, weak-acyclicity, tuple-generating-dependency, conjunctive-query, chandra-merlin-theorem]
sources:
  - paper: doi:10.1016/j.tcs.2004.10.033
    title: "Ronald Fagin, Phokion G. Kolaitis, Renée J. Miller and Lucian Popa, Data exchange: semantics and query answering, Theoretical Computer Science 336(1), 2005"
    locator: "universal solutions, the chase and certain answers"
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "Chapter 6, Good solutions"
  - paper: doi:10.1145/1061318.1061323
    title: "Ronald Fagin, Phokion G. Kolaitis and Lucian Popa, Data exchange: getting to the core, ACM TODS 30(1), 2005"
    locator: "pages 174-210, the core of the universal solutions"
---

A universal solution of a [data exchange problem](/data-exchange-problem/) is a solution that has a homomorphism into every solution, so it holds what the mapping forces and nothing more. When the chase with the mapping stops without failure, its result is a universal solution. This page defines the notion and shows which solutions have it. The [data exchange problem](/data-exchange-problem/) page states the tasks that use it, and [core computation](/data-exchange-core-computation/) picks the smallest universal solution.

## Definition

Fix a [schema mapping](/schema-mapping/) $\mathcal M = (\mathbf S, \mathbf T, \Sigma_{st} \cup \Sigma_t)$ and a source instance $I$. Target instances hold constants and labeled nulls $\bot_1, \bot_2, \ldots$, and set semantics holds.

- A **solution** for $I$ is a target instance $J$ such that $(I, J)$ satisfies $\Sigma_{st} \cup \Sigma_t$.
- A **homomorphism** $h : J \to J'$ maps the values of $J$ to values of $J'$, is the identity on constants, and maps each fact $R(v_1, \ldots, v_k)$ of $J$ to a fact $R(h(v_1), \ldots, h(v_k))$ of $J'$.
- A **universal solution** for $I$ is a solution $J$ such that, for every solution $J'$ for $I$, there is a homomorphism $J \to J'$.

Facts that follow from the definition and from the theory of the chase:

- Two universal solutions have homomorphisms each way. So they are homomorphically equivalent, and they give the same null-free answers to each [conjunctive query](/conjunctive-query/).
- If $J$ is universal and $J'$ is a solution with homomorphisms each way with $J$, then $J'$ is universal too.
- If a chase of $I$ with $\Sigma_{st} \cup \Sigma_t$ stops without failure, the result is a universal solution (theorem, Fagin, Kolaitis, Miller and Popa). If it fails, $I$ has no solution.
- All universal solutions have the same core up to a renaming of nulls, and this core is the smallest universal solution (theorem, Fagin, Kolaitis and Popa).
- For a union of conjunctive queries $q$, the [certain answers](/certain-answers/) are the null-free tuples of $q(J)$ for any universal solution $J$ (theorem, Fagin, Kolaitis, Miller and Popa).

## Examples and non-examples

The mapping has $d_1 : \forall x, y\, (\text{Flight}(x, y) \to \exists z\, (\text{Leg}(x, z) \wedge \text{Leg}(z, y)))$ and $d_2 : \forall x, y\, (\text{Flight}(x, y) \to \exists u\, \text{Leg}(x, u))$, with no target dependencies, and $I = \{\text{Flight}(a, b), \text{Flight}(b, c)\}$.

**Universal: the canonical solution.** The chase gives

$$J = \{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c), \text{Leg}(a, \bot_3), \text{Leg}(b, \bot_4)\}.$$

For any solution $J'$, $d_1$ gives values $s_1, s_2$ with $\text{Leg}(a, s_1), \text{Leg}(s_1, b), \text{Leg}(b, s_2), \text{Leg}(s_2, c)$ in $J'$, and $d_2$ gives $t_1, t_2$ with $\text{Leg}(a, t_1), \text{Leg}(b, t_2)$. The map $\bot_1 \mapsto s_1$, $\bot_2 \mapsto s_2$, $\bot_3 \mapsto t_1$, $\bot_4 \mapsto t_2$ is a homomorphism $J \to J'$.

**Universal: the core.** $C = \{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c)\}$ is a solution, because $\text{Leg}(a, \bot_1)$ and $\text{Leg}(b, \bot_2)$ also satisfy $d_2$. It is a subset of $J$, so it maps into each solution, and it is universal. It is the smallest universal solution.

**A solution that is not universal: a guess made concrete.** $J_1 = \{\text{Leg}(a, b), \text{Leg}(b, b), \text{Leg}(b, c), \text{Leg}(c, c)\}$ sets the stops to $b$ and $c$. It is a solution. The map $\bot_1, \bot_3, \bot_4 \mapsto b$, $\bot_2 \mapsto c$ is a homomorphism $J \to J_1$. But $J_1$ has no homomorphism into $J$, because a homomorphism fixes constants and $\text{Leg}(b, b)$ is not in $J$. So $J_1$ claims more than the mapping says. The query "is there a loop $\text{Leg}(x, x)$" is true on $J_1$ and false on $J$.

**A solution that is not universal: a new constant.** $J_2 = \{\text{Leg}(a, d), \text{Leg}(d, b), \text{Leg}(b, d), \text{Leg}(d, c)\}$, where $d$ is a constant, is a solution. It does not map into $J$, since $\text{Leg}(a, d)$ would have to stay as it is. On $J_2$, the query $Q(x, y) \text{ :- } \text{Leg}(x, z), \text{Leg}(z, y)$ returns $(a, c)$, which is not a certain answer.

**Solutions exist but no universal solution.** Take the source-to-target tgd $\forall x, y\, (S(x, y) \to E(x, y))$, the target tgd $\forall x, y\, (E(x, y) \to \exists z\, E(y, z))$, and $I = \{S(a, b)\}$. The instance $\{E(a, b), E(b, b)\}$ is a solution. A finite solution $U$ must contain a walk of $E$ edges from $b$ that never ends, so it has a cycle reached from $b$ by a path of some length $L$. For $m > L$, the instance $J_m = \{E(a, b), E(b, \bot_1), E(\bot_1, \bot_2), \ldots, E(\bot_{m-1}, \bot_m), E(\bot_m, \bot_m)\}$ is a solution whose only cycle is the loop at $\bot_m$, at distance $m$ from $b$. A homomorphism $U \to J_m$ maps $b$ to $b$, so it maps the end of the path to the node at distance $L$ from $b$, which is not $\bot_m$, and it maps the cycle to a closed walk that starts there. No closed walk of $J_m$ starts there. So no finite solution is universal. Here the chase runs forever, and the target tgd is not [weakly acyclic](/weak-acyclicity/).

## Related definitions

- **Solution.** Any target instance that satisfies the mapping; see [data exchange problem](/data-exchange-problem/).
- **Canonical universal solution.** The result of the oblivious chase with source-to-target tgds, where each trigger fires one time with fresh nulls.
- **Core.** The smallest universal solution, unique up to a renaming of nulls; see [core computation for data exchange](/data-exchange-core-computation/). It is the analogue for instances of the minimal query of the [Chandra-Merlin theorem](/chandra-merlin-theorem/).
- **Certain answers.** The answers true in all solutions; universal solutions compute them for unions of conjunctive queries; see [certain answers](/certain-answers/).
- **Closed world solutions.** Universal solutions that also hold only what the mapping justifies. They give a different, stricter semantics for queries with negation.

## References
