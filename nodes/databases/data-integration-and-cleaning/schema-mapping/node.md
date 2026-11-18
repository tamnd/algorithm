---
tag: DPX9ZV
kind: definition
slug: schema-mapping
name: Schema mapping
aliases:
- source-to-target dependencies
area: databases/data-integration-and-cleaning
level: core
summary: "A specification, usually by tuple-generating dependencies, of how the data of a source schema relates to a target schema."
prereqs: [relational-model, conjunctive-query, tuple-generating-dependency]
see_also: [gav-and-lav, data-exchange-problem, schema-matching, schema-mapping-composition, universal-solution, certain-answers, equality-generating-dependency, weak-acyclicity]
sources:
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "Chapter 3, Data exchange: key definitions, and Chapter 17, What is metadata management?"
  - paper: doi:10.1016/j.tcs.2004.10.033
    title: "Ronald Fagin, Phokion G. Kolaitis, Renée J. Miller and Lucian Popa, Data exchange: semantics and query answering, Theoretical Computer Science 336(1), 2005"
    locator: the definition of a data exchange setting
  - paper: doi:10.1145/543613.543644
    title: "Maurizio Lenzerini, Data integration: a theoretical perspective, PODS 2002"
    locator: pages 233-246
  - book: isbn:9780124160446
    title: "AnHai Doan, Alon Halevy and Zachary Ives, Principles of Data Integration, Morgan Kaufmann, 2012"
    locator: "Chapter 5, Schema Matching and Mapping"
---

A schema mapping is a formal statement of how the data of a source schema relates to the data of a target schema, usually given as a set of source-to-target [tuple-generating dependencies](/tuple-generating-dependency/). Its meaning is the set of pairs of a source instance and a target instance that satisfy it. This page gives the general form and its semantics. The page on [GAV and LAV](/gav-and-lav/) covers the two restricted forms that data integration uses, where one side of each rule is a single relation, and how queries are answered under them.

## Definition

Let $\mathbf{S}$ and $\mathbf{T}$ be two relational schemas with no relation name in common. Instances are sets of facts. Source instances hold constants only. Target instances may also hold labeled nulls $\bot_1, \bot_2, \ldots$, which stand for unknown values.

A **schema mapping** is a triple $\mathcal{M} = (\mathbf{S}, \mathbf{T}, \Sigma)$, where $\Sigma = \Sigma_{st} \cup \Sigma_t$ is a finite set of dependencies.

- $\Sigma_{st}$ is a set of **source-to-target tgds** $\forall x\, (\varphi_{\mathbf S}(x) \to \exists y\, \psi_{\mathbf T}(x, y))$, where $\varphi_{\mathbf S}$ is a conjunction of atoms over $\mathbf{S}$ and $\psi_{\mathbf T}$ is a conjunction of atoms over $\mathbf{T}$.
- $\Sigma_t$ is a set of **target dependencies** over $\mathbf{T}$ alone, usually tgds $\forall x\, (\varphi_{\mathbf T}(x) \to \exists y\, \psi_{\mathbf T}(x, y))$ and [egds](/equality-generating-dependency/) $\forall x\, (\varphi_{\mathbf T}(x) \to x_i = x_j)$. It may be empty.

The **semantics** of $\mathcal M$ is the set

$$[\![\mathcal M]\!] = \{\, (I, J) \;:\; I \text{ is an instance of } \mathbf S,\ J \text{ is an instance of } \mathbf T,\ (I, J) \models \Sigma \,\}.$$

For a source instance $I$, a target instance $J$ with $(I, J) \in [\![\mathcal M]\!]$ is a **solution** for $I$. Two mappings are **equivalent** if they have the same semantics.

Some named forms of source-to-target tgds:

- **Full:** no existential variables, so the head uses only values of the source.
- **GAV:** full, with a single atom in the head.
- **LAV:** a single atom in the body.

The general form, with conjunctions on both sides, contains both GAV and LAV rules.

## Examples and non-examples

**A mapping with new values.** The source has $\text{Flight}(x, y)$, a direct flight from $x$ to $y$. The target has $\text{Leg}(x, y)$, a leg of a trip. The mapping has the two source-to-target tgds

$$d_1 : \forall x, y\, (\text{Flight}(x, y) \to \exists z\, (\text{Leg}(x, z) \wedge \text{Leg}(z, y))),$$
$$d_2 : \forall x, y\, (\text{Flight}(x, y) \to \exists u\, \text{Leg}(x, u)).$$

So each flight becomes two legs through an unknown stop. For $I = \{\text{Flight}(a, b), \text{Flight}(b, c)\}$, the instance $\{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c)\}$ is a solution. So is $\{\text{Leg}(a, b), \text{Leg}(b, b), \text{Leg}(b, c), \text{Leg}(c, c)\}$, with the stops set to $b$ and $c$. The mapping does not fix one target instance. The [data exchange problem](/data-exchange-problem/) asks which solution to build.

**A full mapping.** $\forall x, y, z\, (\text{Emp}(x, y) \wedge \text{Dept}(y, z) \to \text{WorksIn}(x, z))$ copies a join of the source into the target. It makes no nulls.

**Not definable: an exact copy.** Let $\mathbf S$ have one relation $R$ and $\mathbf T$ one relation $R'$. The relation "$J$ is $I$ with $R$ renamed to $R'$" is not the semantics of any mapping of the form above. Assume a mapping has this semantics, and let $I \subsetneq I_2$ be two source instances with copies $J \subsetneq J_2$. Then $(I_2, J_2)$ satisfies $\Sigma$, so $J_2$ satisfies $\Sigma_t$. The bodies of $\Sigma_{st}$ read only the source, and their heads stay true when facts are added, so $(I, J_2)$ satisfies $\Sigma_{st}$ as $(I, J)$ does. So $(I, J_2)$ is in the semantics, but $J_2$ is not the copy of $I$.

**Not closed under composition.** Two mappings given by source-to-target tgds can compose to a mapping that no finite set of first-order tgds defines. The page on [schema mapping composition](/schema-mapping-composition/) gives the example and the second-order tgds that repair this.

## Related definitions

- **Correspondences.** A [schema matching](/schema-matching/) step finds pairs of elements that mean the same, such as the first column of Flight and the first column of Leg. A mapping adds the joins, the new values and the grouping that the correspondences leave open. Tools generate candidate mappings from correspondences and let a person choose.
- **GAV and LAV.** The restricted forms used for a virtual, integrated view of many sources; see [GAV and LAV](/gav-and-lav/).
- **Universal solution.** A solution with a homomorphism into every solution; see [universal solution](/universal-solution/). The chase builds one.
- **Certain answers.** The answers of a target query that hold in every solution; see [certain answers](/certain-answers/).
- **Weak acyclicity.** A condition on $\Sigma_t$ that makes the chase stop; see [weak acyclicity](/weak-acyclicity/).
- **Operators on mappings.** Composition, inversion and the test that a mapping has a solution for some source are studied as metadata management.

## References
