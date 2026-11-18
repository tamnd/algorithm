---
tag: 00291E
kind: problem
slug: schema-mapping-composition
name: Schema mapping composition
aliases:
- second-order tgds
- composing schema mappings
area: databases/data-integration-and-cleaning
level: research
summary: "Given mappings from A to B and from B to C, find one mapping from A to C with the same meaning; it may need second-order dependencies."
prereqs: [schema-mapping, tuple-generating-dependency, skolemization]
see_also: [data-exchange-problem, universal-solution, gav-and-lav, certain-answers, np-complete, three-coloring, data-and-combined-complexity, chase-algorithm]
sources:
  - paper: doi:10.1145/1114244.1114249
    title: "Ronald Fagin, Phokion G. Kolaitis, Lucian Popa and Wang-Chiew Tan, Composing schema mappings: second-order dependencies to the rescue, ACM TODS 30(4), 2005"
    locator: "pages 994-1055, the semantics of composition, second-order tgds, closure under composition, NP-complete compositions and the chase with second-order tgds"
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "the part on metadata management, the chapter on mapping composition"
---

Schema mapping composition takes a [schema mapping](/schema-mapping/) from schema A to schema B and one from B to C, and asks for a single mapping from A to C that relates exactly the pairs of instances linked through some instance of B. The problem is to find a language that can always write this mapping down and an algorithm that builds it. For source-to-target tgds the answer is a larger language, the second-order tgds. This page is about combining mappings. The [data exchange problem](/data-exchange-problem/) is about using one mapping to build a target instance, and composition is one of the operations that manage mappings before data exchange runs.

## In plain words

A company moves its data from an old design to a new one, and later the new design changes again. Each step has a set of rules that says how data in one design becomes data in the next. It would be simpler to have one set of rules from the oldest design straight to the newest.

When each step only copies and joins known values, the two rule sets can be merged by plugging one into the other. The trouble starts when the first step invents placeholder values and the second step tests them, for example by asking whether a placeholder equals a known value. The merged rule must then talk about the placeholders themselves. Ordinary rules cannot do that, so the merged rule needs a richer form that names functions which produce the placeholders.

## Definition

**Semantics.** A mapping $\mathcal M_{12}$ from $\mathbf S_1$ to $\mathbf S_2$ is identified with its set of pairs $(I_1, I_2)$ that satisfy its dependencies. The **composition** is

$$\mathcal M_{12} \circ \mathcal M_{23} = \{ (I_1, I_3) : \text{there is } I_2 \text{ with } (I_1, I_2) \in \mathcal M_{12} \text{ and } (I_2, I_3) \in \mathcal M_{23} \}.$$

Set semantics holds. The intermediate instance $I_2$ may be any instance over $\mathbf S_2$.

**The problem.** Given $\mathcal M_{12}$ and $\mathcal M_{23}$, each given by a finite set of source-to-target tgds $\forall x\, (\varphi(x) \to \exists y\, \psi(x, y))$, find a finite set $\Sigma_{13}$ of dependencies from $\mathbf S_1$ to $\mathbf S_3$ in some fixed language whose pairs are exactly $\mathcal M_{12} \circ \mathcal M_{23}$.

**Second-order tgds.** A *second-order tgd*, or *SO tgd*, has the form

$$\exists f_1 \ldots \exists f_m \big( \forall x_1 (\varphi_1 \to \psi_1) \wedge \cdots \wedge \forall x_n (\varphi_n \to \psi_n) \big),$$

where the $f_j$ are function symbols, each $\varphi_i$ is a conjunction of source atoms and of equalities between terms built from the variables $x_i$ and the $f_j$, and each $\psi_i$ is a conjunction of target atoms over such terms. A pair $(I, J)$ satisfies it if there are functions on the values of $I$ and $J$ that make all clauses true.

**Membership.** The decision task is: given $(I_1, I_3)$, is it in $\mathcal M_{12} \circ \mathcal M_{23}$? Its complexity is measured in data complexity, with the mappings fixed.

## Variants

- **Full first mapping.** $\mathcal M_{12}$ is given by full tgds, with no existential variables. Then the composition is again given by source-to-target tgds.
- **GAV with GAV.** Both mappings are full. Then the composition is given by full tgds, and the result is again a [GAV](/gav-and-lav/) mapping.
- **General source-to-target tgds.** The composition may need SO tgds.
- **SO tgds as the input language.** Both mappings are given by SO tgds. The composition is again an SO tgd.
- **Target dependencies.** The results above are stated for mappings with source-to-target dependencies only, and target tgds or egds in $\mathbf S_2$ or $\mathbf S_3$ make the problem harder.
- **Inversion.** The other basic operator on mappings, which asks for a mapping from B back to A.

## Examples

**Full first mapping.** Let $\mathcal M_{12}$ be $\forall x, y\, (\text{Flight}(x, y) \to \text{Hop}(x, y))$ and $\mathcal M_{23}$ be $\forall x, y, z\, (\text{Hop}(x, y) \wedge \text{Hop}(y, z) \to \exists w\, \text{Trip}(x, z, w))$. The composition is

$$\forall x, y, z\, (\text{Flight}(x, y) \wedge \text{Flight}(y, z) \to \exists w\, \text{Trip}(x, z, w)).$$

If $(I_1, I_3)$ is in the composition, the instance $I_2$ holds a Hop fact for each Flight fact, so this tgd holds. In the other direction, if the tgd holds, take $I_2$ to be exactly the Hop copy of the Flight facts. Then $\mathcal M_{12}$ holds and each pair of Hop facts comes from a pair of Flight facts, so $\mathcal M_{23}$ holds.

**A composition that needs a function.** Let $\mathcal M_{12}$ be $\forall e\, (\text{Emp}(e) \to \exists m\, \text{Rep}(e, m))$, each employee reports to some manager. Let $\mathcal M_{23}$ be $\forall e, m\, (\text{Rep}(e, m) \to \text{Mgr}(e, m))$ and $\forall e\, (\text{Rep}(e, e) \to \text{SelfMgr}(e))$. The composition is given by the SO tgd

$$\exists f \big( \forall e\, (\text{Emp}(e) \to \text{Mgr}(e, f(e))) \wedge \forall e\, (\text{Emp}(e) \wedge e = f(e) \to \text{SelfMgr}(e)) \big).$$

The function $f$ names the manager that $\mathcal M_{12}$ invents. Take $I_1 = \{\text{Emp}(a)\}$.

| $I_3$ | in the composition | reason |
|---|---|---|
| $\{\text{Mgr}(a, b)\}$ | yes | $f(a) = b$, from $I_2 = \{\text{Rep}(a, b)\}$ |
| $\{\text{Mgr}(a, a)\}$ | no | the only choice is $f(a) = a$, which needs $\text{SelfMgr}(a)$ |
| $\{\text{Mgr}(a, a), \text{Mgr}(a, b)\}$ | yes | $f(a) = b$ |
| $\{\text{Mgr}(a, a), \text{SelfMgr}(a)\}$ | yes | $f(a) = a$ |

No finite set of source-to-target tgds defines this composition (theorem, Fagin, Kolaitis, Popa and Tan). The second clause tests whether the invented manager equals the employee, and a first-order tgd has no name for the invented value.

## Known algorithms

- **Unfolding for a full first mapping.** For each tgd of $\mathcal M_{23}$, replace each body atom $R(y)$ by the body of a tgd of $\mathcal M_{12}$ whose head has an atom $R(u)$, with the equalities $y = u$, in all combinations. The result is a set of source-to-target tgds.
- **Composition of SO tgds** (Fagin, Kolaitis, Popa and Tan). First skolemize $\mathcal M_{12}$: replace each existential variable $y$ of a tgd by a term $f(x)$ with a new function symbol, see [skolemization](/skolemization/). Then unfold as above: each body atom of a clause of $\mathcal M_{23}$ is replaced by the body of a clause of $\mathcal M_{12}$ that makes it, together with the equalities between the terms. The functions of both mappings are put under one $\exists$. Applied to the Emp example, the clause $\text{Rep}(e, e) \to \text{SelfMgr}(e)$ meets $\text{Emp}(e') \to \text{Rep}(e', f(e'))$ and gives $\text{Emp}(e') \wedge e = e' \wedge e = f(e') \to \text{SelfMgr}(e)$, which simplifies to the second clause above.
- **Simplification.** When a function symbol occurs in the head of one clause only, never in a body, and always with the list of all universal variables of that clause as its arguments, it can be put back as an existential variable. If this works for all function symbols, the result is a set of first-order tgds.
- **The chase with SO tgds.** To use a composed mapping for data exchange, chase the source instance with the SO tgd: each term $f(t)$ gets one labeled null, reused at each place where the same term occurs. The result is a universal solution.

## Bounds

All bounds are in data complexity unless stated.

- **Upper bound.** For mappings given by source-to-target tgds, and more generally by SO tgds, membership in the composition is in NP (theorem, Fagin, Kolaitis, Popa and Tan). The certificate is the values of the functions on the terms that the clauses use, which are polynomially many.
- **Lower bound.** There are mappings $\mathcal M_{12}$ and $\mathcal M_{23}$ given by source-to-target tgds whose composition has an NP-complete membership problem (theorem, same paper). One such pair is in the Reductions section. Each first-order property has a polynomial-time check, so such a composition is not definable in first-order logic unless P = NP.
- **Full first mapping.** The composition is given by source-to-target tgds, so membership takes polynomial time.
- **Data exchange with an SO tgd.** The chase builds a universal solution in polynomial time, and certain answers of unions of conjunctive queries take polynomial time (theorem, same paper).
- **Size of the result.** If a clause of $\mathcal M_{23}$ has $k$ body atoms and each atom can be made by up to $r$ clauses of $\mathcal M_{12}$, the unfolding gives up to $r^k$ clauses for it. So the composed mapping can be exponentially larger than the input mappings.

## Reductions

- **From 3-colorability.** Let $\mathbf S_1$ have $\text{Node}(x)$ and $\text{Edge}(x, y)$. Let $\mathcal M_{12}$ be $\forall x\, (\text{Node}(x) \to \exists c\, \text{Color}(x, c))$ and $\forall x, y\, (\text{Edge}(x, y) \to \text{E}(x, y))$. Let $\mathcal M_{23}$ be $\forall x, c\, (\text{Color}(x, c) \to \text{Col}(c))$ and $\forall x, y, u\, (\text{E}(x, y) \wedge \text{Color}(x, u) \wedge \text{Color}(y, u) \to \text{Mono}(x, y))$. For a graph $G$, let $I_1$ hold its nodes and edges, and $I_3 = \{\text{Col}(r), \text{Col}(g), \text{Col}(b)\}$ with no Mono facts. Then $(I_1, I_3)$ is in the composition if and only if $G$ is [3-colorable](/three-coloring/). If $\chi$ is a 3-coloring, $I_2 = \{\text{Color}(x, \chi(x))\} \cup \{\text{E}(x, y)\}$ works. In the other direction, each node has a Color fact whose color is in $\{r, g, b\}$, choose one for each node, and an edge with one color at both ends would force a Mono fact. So membership is [NP-complete](/np-complete/).
- **SO tgds and composition.** Each set of source-to-target tgds is an SO tgd, by skolemization. The SO tgds are the smallest class that contains the source-to-target tgds and is closed under conjunction and composition (theorem, Fagin, Kolaitis, Popa and Tan). So SO tgds are the right language for this problem, not only a sufficient one.
- **Composition and certain answers.** If $\Sigma_{13}$ defines $\mathcal M_{12} \circ \mathcal M_{23}$, data exchange from $\mathbf S_1$ to $\mathbf S_3$ with $\Sigma_{13}$ has the same solutions as the two steps in sequence, so it gives the same [certain answers](/certain-answers/).

## Applications

- **Schema evolution.** A mapping from a source to a database, followed by a mapping from the old to the new design of the database, composes into a mapping from the source to the new design.
- **Chains of mappings.** Systems where each peer has a mapping only to its neighbors answer a query along a path of mappings, and composition replaces the path by one mapping.
- **Mapping management.** Composition and inversion are the basic operators of tools that store, combine and reuse schema mappings.
- **Data exchange.** A composed SO tgd can run directly with the chase, with no need to build the intermediate instance.

## References
