---
tag: 8F8GKB
kind: definition
slug: equality-generating-dependency
name: Equality-generating dependency
aliases:
- EGD
area: databases/relational-theory
level: advanced
summary: A first-order constraint that whenever some tuples are present, two of their values must be equal; functional dependencies are a case.
prereqs: [conjunctive-query, functional-dependency]
see_also: [tuple-generating-dependency, inclusion-dependency, chase-algorithm, candidate-key, armstrongs-axioms, dependency-implication-problem, data-exchange-problem, universal-solution]
sources:
  - paper: doi:10.1145/1634.1636
    title: Catriel Beeri and Moshe Y. Vardi, A proof procedure for data dependencies, Journal of the ACM 31(4), 718 to 741 (1984)
    locator: equality-generating dependencies, and the chase step that equates two values
  - paper: doi:10.1145/322344.322347
    title: Ronald Fagin, Horn clauses and database dependencies, Journal of the ACM 29(4), 952 to 985 (1982)
    locator: embedded implicational dependencies with equalities in the conclusion
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency), the chase for functional dependencies, and Chapter 10 (a larger perspective), equality-generating dependencies
---

An equality-generating dependency (EGD) says that whenever some pattern of tuples occurs in a database, two values of that pattern are equal. The pattern is a conjunction of atoms, as in a [conjunctive query](/conjunctive-query/). Every [functional dependency](/functional-dependency/) and every key constraint is an EGD, but an EGD can also join several relations. Beeri and Vardi (1984) named the class, and it is one half of the embedded implicational dependencies of Fagin (1982). The other half are the [tuple-generating dependencies](/tuple-generating-dependency/). In the [chase](/chase-algorithm/), an EGD makes two values equal, or fails when they are two different constants.

## Definition

We use set semantics: a relation is a set of tuples.

**Definition (Beeri and Vardi 1984).** An *equality-generating dependency* is a first-order sentence

$$\forall \bar x \, \big( \varphi(\bar x) \rightarrow x_i = x_j \big),$$

where $\varphi$ is a nonempty conjunction of relational atoms and $x_i$ and $x_j$ are variables of $\varphi$. In ASCII it is written `phi(x) -> x_i = x_j`. A database $D$ *satisfies* the EGD if every valuation $v$ with $v(\varphi) \subseteq D$ has $v(x_i) = v(x_j)$. The EGD is *trivial* if $x_i$ and $x_j$ are the same variable.

A conclusion with several equalities, $x_1 = y_1 \wedge \cdots \wedge x_p = y_p$, is the same as $p$ EGDs with the same body. Some authors also allow a constant on the right side, as in $x_i = c$.

**As a query.** $D$ satisfies the EGD if and only if the conjunctive query $Q(x_i, x_j) \mathbin{:\!-} \varphi$ returns only pairs of equal values on $D$.

**The chase step.** If $v(\varphi) \subseteq D$ and $a = v(x_i)$ differs from $b = v(x_j)$, the [chase](/chase-algorithm/) acts as follows.

- If $b$ is a labeled null, replace $b$ by $a$ everywhere in $D$. If $a$ is a null and $b$ is a constant, replace $a$ by $b$.
- If $a$ and $b$ are two different constants, the chase *fails*: no way of replacing the nulls of $D$ by values gives a database that satisfies the EGD.

Each step that does not fail makes the number of distinct values smaller by one. So a chase with EGDs alone stops after fewer steps than there are values in $D$. In a test for implication, the values are the variables of a tableau, and they are all treated as nulls, so this chase never fails.

## Examples and non-examples

- **Functional dependency.** On $R(A, B, C)$, the FD $A \to B$ is the EGD
  $$\forall a, b, c, b', c' \, \big( R(a, b, c) \wedge R(a, b', c') \rightarrow b = b' \big).$$
  An FD $X \to Y$ with several attributes in $Y$ is one EGD for each attribute of $Y$.
- **Key.** $A$ is a key of $R(A, B, C)$ if $A \to B$ and $A \to C$ hold, which are two EGDs. See [candidate key](/candidate-key/).
- **Across two relations.** With $\mathit{Emp}(\mathit{name}, \mathit{dept})$ and $\mathit{Head}(\mathit{dept}, \mathit{name})$, the EGD
  $$\mathit{Head}(d, m) \wedge \mathit{Emp}(m, d') \rightarrow d = d'$$
  says that the head of a department works in that department. It is not an FD, because its body has atoms of two relations.
- **A chase step with nulls.** Let $R = \{(a, n_1, c),\ (a, b, n_2)\}$ with nulls $n_1$ and $n_2$, and the FD $A \to B$. The chase replaces $n_1$ by $b$, and $R$ becomes $\{(a, b, c),\ (a, b, n_2)\}$.
- **A failing chase.** $R = \{(a, b, c),\ (a, b', c)\}$ with constants $b \ne b'$ violates $A \to B$, and the chase fails. In [data exchange](/data-exchange-problem/), a failed chase with the target EGDs means that there is no solution.
- **Non-example: inclusion dependency.** "Each order has a known customer" asks for a tuple to exist, not for two values to be equal. It is an [inclusion dependency](/inclusion-dependency/), which is a TGD.
- **Non-example: inequality.** $R(x, y) \rightarrow x \ne y$ is not an EGD. It is a *denial constraint*, and the chase can not repair it by equating values.

## Related definitions

- **Tuple-generating dependency.** A [TGD](/tuple-generating-dependency/) has a conjunction of atoms as its conclusion. EGDs and TGDs together are the embedded implicational dependencies of Fagin.
- **Functional dependency and Armstrong's axioms.** FDs are the EGDs over one relation whose body has two atoms that share exactly the variables of the left side. [Armstrong's axioms](/armstrongs-axioms/) are complete for them, and attribute closure decides implication in linear time.
- **Implication.** For EGDs, possibly with full TGDs, the chase on the body of the goal stops and decides implication. With embedded TGDs the chase may not stop, and implication of TGDs and EGDs together is undecidable. See the [dependency implication problem](/dependency-implication-problem/).
- **Interaction with TGDs in the chase.** Steps of EGDs and TGDs can alternate. An EGD step can make a TGD step needed or not needed, so the order of the steps can change the result, and with embedded TGDs it can change whether the chase stops. A chase that stops without failure gives a [universal solution](/universal-solution/).

## References
