---
tag: HJ9YV3
kind: definition
slug: denial-constraint
name: Denial constraint
aliases:
- denial constraints
area: databases/data-integration-and-cleaning
level: advanced
summary: "A constraint that forbids any choice of tuples that makes a conjunction of comparisons true. It generalizes functional dependencies and is used to detect errors."
prereqs: [functional-dependency, relational-calculus]
see_also: [conditional-functional-dependency, functional-dependency, equality-generating-dependency, database-repair, consistent-query-answering, holoclean, functional-dependency-discovery, tuple-generating-dependency]
sources:
  - paper: doi:10.14778/2536258.2536262
    title: "Xu Chu, Ihab F. Ilyas and Paolo Papotti, Discovering denial constraints, PVLDB 6(13), 2013"
    locator: "pages 1498-1509, the definition of denial constraints, the inference rules and the implication problem"
  - paper: doi:10.1109/icde.2013.6544847
    title: "Xu Chu, Ihab F. Ilyas and Paolo Papotti, Holistic data cleaning: putting violations into context, ICDE 2013"
    locator: "pages 458-469, violation detection and repair with denial constraints"
  - paper: doi:10.1016/j.ic.2004.04.007
    title: "Jan Chomicki and Jerzy Marcinkowski, Minimal-change integrity maintenance using tuple deletions, Information and Computation 197(1-2), 2005"
    locator: "pages 90-121, repairs and consistent answers under denial constraints"
  - book: isbn:9783031007552
    title: "Leopoldo Bertossi, Database Repairing and Consistent Query Answering, Morgan and Claypool, 2011"
    locator: "the chapters on repairs and consistent answers, where denial constraints are a main class of integrity constraints"
---

A denial constraint says that some combination of tuples must not occur: no choice of tuples may make all of a list of comparisons true at once. A [functional dependency](/functional-dependency/) is the special case with two tuples, equalities on the left side and one inequality on the right side. A [conditional functional dependency](/conditional-functional-dependency/) is a different extension of the same idea. It adds constants to a functional dependency but keeps only equality, while a denial constraint allows the order comparisons $<$, $\le$, $>$, $\ge$ between any attributes. Data cleaning systems such as [HoloClean](/holoclean/) use denial constraints as their main language for errors.

## Definition

Let $R$ be a relation schema. A *predicate* has the form $t_x.A \;\theta\; t_y.B$ or $t_x.A \;\theta\; c$, where $t_x, t_y$ are tuple variables, $A, B$ are attributes, $c$ is a constant and $\theta$ is one of $=, \ne, <, \le, >, \ge$. A **denial constraint** is a sentence

$$\varphi \;=\; \forall t_1, \ldots, t_k \in R : \neg (P_1 \wedge \cdots \wedge P_m)$$

with predicates $P_1, \ldots, P_m$ over the tuple variables $t_1, \ldots, t_k$. Set semantics holds: $R$ is a set of tuples. An instance $I$ of $R$ *satisfies* $\varphi$ if no assignment of tuples of $I$ to the variables makes every $P_i$ true. An assignment that does is a *violation*. As in the work of Chu, Ilyas and Papotti, the tuple variables of one constraint take different tuples, so a constraint with two variables talks about pairs of different tuples. Most uses need only $k \le 2$, and this page and its code treat $k = 1$ and $k = 2$.

In first-order terms, a denial constraint is a universal sentence whose body is a negated conjunction of atoms and comparisons. Satisfaction is preserved by deleting tuples: a subset of an instance that satisfies $\varphi$ also satisfies it. This is why deletions alone can always [repair](/database-repair/) a violation of a set of denial constraints.

## Examples and non-examples

The table Tax has the attributes Name, State, Salary and Rate:

| row | Name | State | Salary | Rate |
|---|---|---|---|---|
| 0 | Ann | NY | 50 | 10 |
| 1 | Bob | NY | 70 | 8 |
| 2 | Cat | NY | 90 | 12 |
| 3 | Dan | CA | 40 | 9 |
| 4 | Eve | CA | -5 | 7 |

- **An order constraint.** "In one state, a higher salary may not have a lower tax rate" is $\forall t_1, t_2 : \neg (t_1.\text{State} = t_2.\text{State} \wedge t_1.\text{Salary} < t_2.\text{Salary} \wedge t_1.\text{Rate} > t_2.\text{Rate})$. The only violation is $(t_1, t_2) = (\text{row } 0, \text{row } 1)$: Ann earns less than Bob in NY but pays a higher rate. No functional dependency can say this.
- **A single-tuple constraint.** $\forall t : \neg (t.\text{Salary} < 0)$ has one violation, row 4.
- **A functional dependency.** $\text{State} \to \text{Rate}$ is $\forall t_1, t_2 : \neg (t_1.\text{State} = t_2.\text{State} \wedge t_1.\text{Rate} \ne t_2.\text{Rate})$. In general, $X \to Y$ gives one denial constraint for each attribute of $Y$.
- **A constant CFD.** The pattern "if the country code is 01 and the area code is 908, the city is MH" is the single-tuple constraint $\forall t : \neg (t.\text{CC} = 01 \wedge t.\text{AC} = 908 \wedge t.\text{CT} \ne \text{MH})$.
- **Non-example: an inclusion dependency.** "Each order has a customer" asks for a tuple to exist. Deleting the customer creates a violation, so no denial constraint can express it. It is a [tuple-generating dependency](/tuple-generating-dependency/).
- **Non-example: a constraint over the same tuple twice.** Under the convention of different tuples, $\forall t_1, t_2 : \neg (t_1.A = t_2.A)$ says that $A$ is a key, not that the table is empty. With the same tuple allowed, every nonempty table would violate it.

To find the violations of a constraint with two tuple variables, hash the rows on the attributes joined by equality, and compare only the rows in one bucket:

```pseudo id=main
VIOLATIONS(I, phi)
L1  E <- the predicates t1.A = t2.B of phi; P <- the other predicates
L2  H <- an empty hash table
L3  for each row t of I do add t to H under the key (t.B for each predicate of E)
L4  for each row s of I do
L5      for each row t in H under the key (s.A for each predicate of E) do
L6          if t ≠ s and every predicate of P holds for (s, t) then report (s, t)
```

This finds the same set of pairs as checking all $n^2$ ordered pairs, which is what the code tests against. It takes $O(n p)$ time to build the table, for $n$ rows and $p$ predicates, plus $O(p)$ for each pair of rows that share a key. With no equality predicate, as in "no two rows with $t_1.A < t_2.A$ and $t_1.B > t_2.B$", every pair shares the empty key and the cost is $O(n^2 p)$.

## Related definitions

- **[Functional dependency](/functional-dependency/).** The denial constraints with two tuple variables, equalities and one inequality on the same attribute.
- **[Conditional functional dependency](/conditional-functional-dependency/).** Functional dependencies on the tuples that match a pattern of constants. Each CFD is a set of denial constraints, one per pattern and attribute.
- **[Equality-generating dependency](/equality-generating-dependency/).** A formula $\forall \bar x (\varphi(\bar x) \to x_i = x_j)$ with a conjunction of atoms $\varphi$. Read as $\neg (\varphi \wedge x_i \ne x_j)$, it is a denial constraint without order comparisons.
- **Implication.** Chu, Ilyas and Papotti give a sound set of inference rules for denial constraints, in the spirit of [Armstrong's axioms](/armstrongs-axioms/), and show that deciding whether a set of denial constraints implies another one is coNP-complete.
- **Repairs and consistent answers.** Under denial constraints, a [subset repair](/database-repair/) is a maximal consistent subset. [Consistent query answering](/consistent-query-answering/) asks which answers hold in all of them. Chomicki and Marcinkowski study both for denial constraints.

## References
