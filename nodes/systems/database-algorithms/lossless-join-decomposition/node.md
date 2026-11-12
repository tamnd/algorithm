---
tag: M09NZ8
kind: problem
slug: lossless-join-decomposition
name: Lossless-join decomposition problem
aliases:
- lossless decomposition
- lossless-join property
- nonadditive join decomposition
area: systems/database-algorithms
level: core
summary: "Decide whether splitting a schema into parts loses information: every relation that satisfies the dependencies must equal the natural join of its projections on the parts."
prereqs: [functional-dependency, relational-algebra, attribute-closure-algorithm]
see_also: [chase-algorithm, bcnf-decomposition, dependency-preserving-decomposition, third-normal-form-synthesis, relational-join, boyce-codd-normal-form, normalization]
sources:
  - paper: doi:10.1145/320083.320091
    title: Alfred V. Aho, Catriel Beeri and Jeffrey D. Ullman, The theory of joins in relational databases, ACM Transactions on Database Systems 4(3), 297 to 314 (1979)
    locator: the tableau test for a lossless join under functional dependencies and its proof
  - paper: "I. J. Heath, Unacceptable file operations in a relational data base, Proceedings of the 1971 ACM SIGFIDET Workshop on Data Description, Access and Control, pages 19 to 33"
    locator: the sufficient condition X -> Y for a lossless split into XY and the rest
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency, the chase) and Chapter 11 (design and dependencies)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), lossless-join decomposition and the tableau test
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Section 3.4 (decomposition, the good, bad and ugly, with the chase test for lossless join)
---

The lossless-join decomposition problem asks whether a decomposition of a relation schema into smaller schemas keeps all the information. The decomposition is lossless when every relation that satisfies the given [functional dependencies](/functional-dependency/) equals the natural [join](/relational-join/) of its projections on the parts. For two parts the answer is one [attribute closure](/attribute-closure-algorithm/): the common attributes must fix one of the two parts. For any number of parts the [chase](/chase-algorithm/) of a tableau decides it in polynomial time (Aho, Beeri and Ullman 1979).

## In plain words

You store a big table as a few smaller tables, each with some of the columns. To get the big table back, you join the small tables on their shared columns. The join always gives back every row you had. The danger is that it can also give rows you never had, because rows of different small tables match by chance on the shared columns. Such extra rows are called spurious rows.

A split is lossless when this can never happen, for any table that follows the known rules between columns. "Lossless" means that no information is lost: with extra rows you can no longer tell which rows were real. For a split into two tables, it is enough that the shared columns fix all the columns of one of the two tables.

## Definition

Let $R$ be a finite set of attributes, $F$ a set of functional dependencies over $R$, and $\rho = (R_1, \ldots, R_k)$ a list of subsets of $R$ with $R_1 \cup \cdots \cup R_k = R$. A relation $r$ over $R$ is *legal* when it satisfies $F$. Write

$$m_\rho(r) = \pi_{R_1}(r) \bowtie \pi_{R_2}(r) \bowtie \cdots \bowtie \pi_{R_k}(r).$$

For every $r$, $r \subseteq m_\rho(r)$, since each tuple of $r$ agrees with its own projections. The tuples of $m_\rho(r) \setminus r$ are the *spurious tuples*.

**Input.** $R$, $F$ and $\rho$.

**Question.** Is $\rho$ *lossless* for $F$, that is,

$$\forall r \text{ legal over } R:\quad r = m_\rho(r)\ ?$$

Equivalently, $F$ implies the join dependency $\bowtie[R_1, \ldots, R_k]$. A decomposition that is not lossless is *lossy*.

**The binary test.** For $k = 2$, $(R_1, R_2)$ is lossless for $F$ if and only if

$$F \models R_1 \cap R_2 \to R_1 \quad\text{or}\quad F \models R_1 \cap R_2 \to R_2 ,$$

that is, if $R_1 \subseteq (R_1 \cap R_2)^+$ or $R_2 \subseteq (R_1 \cap R_2)^+$. *Proof of "if".* Let $X = R_1 \cap R_2$ and say $X \to R_1$ holds. Let $t \in m_\rho(r)$, so there are $u, v \in r$ with $u[R_1] = t[R_1]$ and $v[R_2] = t[R_2]$. Then $u[X] = v[X]$, so $u[R_1] = v[R_1]$ by $X \to R_1$, and $v$ agrees with $t$ on $R_1 \cup R_2 = R$. So $t = v \in r$. This is Heath's theorem (1971). *Proof of "only if".* Assume that neither dependency holds. Take a relation $r = \{u, v\}$ of two tuples that agree exactly on $X^+$ (so $u$ and $v$ differ on each attribute outside $X^+$). It satisfies $F$, since if the two tuples agree on a left side $L$, then $L \subseteq X^+$, so the right side is in $X^+$ too. Neither $R_1$ nor $R_2$ is inside $X^+$, so $u$ and $v$ differ somewhere on $R_1 \setminus R_2$ and somewhere on $R_2 \setminus R_1$. The tuple $t$ with $t[R_1] = u[R_1]$ and $t[R_2] = v[R_2]$ is in $m_\rho(r)$, and it is neither $u$ nor $v$. $\square$

## Variants

- **Functional dependencies only.** The case above. Decidable in polynomial time by the chase.
- **With multivalued and join dependencies.** $F$ may also hold multivalued dependencies (MVDs) and join dependencies. The chase still decides the question (Maier, Mendelzon and Sagiv 1979), but each step can add rows, and the tableau can grow exponentially in the number of attributes. For two parts with MVDs, $(R_1, R_2)$ is lossless if and only if $R_1 \cap R_2 \twoheadrightarrow R_1 \setminus R_2$ follows.
- **No dependencies.** With $F = \emptyset$, $\rho$ is lossless if and only if some $R_i$ equals $R$. (The chase applies no step, so it must start with an all-distinguished row.)
- **The design problem.** Find a lossless decomposition with an extra goal: each part in [BCNF](/boyce-codd-normal-form/) ([BCNF decomposition](/bcnf-decomposition/), always possible), or each part in [3NF](/third-normal-form/) with all dependencies kept ([3NF synthesis](/third-normal-form-synthesis/), always possible).
- **Lossless on one instance.** For one given relation $r$, compute $m_\rho(r)$ and compare. This is a different and easier question; a decomposition can be lossless on one instance and lossy for $F$.

## Examples

**A lossy split with spurious tuples.** Let $R = \{\mathit{supplier}, \mathit{part}, \mathit{city}\}$ with $F = \{\mathit{supplier} \to \mathit{city}\}$, and the legal relation

| supplier | part | city |
|---|---|---|
| s1 | p1 | Paris |
| s2 | p2 | Paris |

Split it into $(\mathit{city}, \mathit{supplier})$ and $(\mathit{city}, \mathit{part})$. The common attribute is $\mathit{city}$, and $\mathit{city}^+ = \{\mathit{city}\}$ fixes neither part, so the split is lossy. Here the join on $\mathit{city}$ gives four tuples: the two real ones and the spurious tuples $(s1, p2, \text{Paris})$ and $(s2, p1, \text{Paris})$. The split into $(\mathit{supplier}, \mathit{city})$ and $(\mathit{supplier}, \mathit{part})$ is lossless, because $\mathit{supplier} \to \mathit{city}$ fixes the first part.

**Three parts.** Let $R = ABCD$ with $F = \{A \to B,\ C \to D\}$. The pair $(AB, CD)$ is lossy: the parts share no attribute, so the join is a cross product, and $\{(1,1,1,1), (2,1,2,1)\}$ gives back four tuples. Add the part $AC$. The chase on the three rows

| | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| $AB$ | $a$ | $a$ | $b_{13}$ | $b_{14}$ |
| $CD$ | $b_{21}$ | $b_{22}$ | $a$ | $a$ |
| $AC$ | $a$ | $b_{32}$ | $a$ | $b_{34}$ |

uses $A \to B$ on rows 1 and 3, which sets $b_{32}$ to $a$, and $C \to D$ on rows 2 and 3, which sets $b_{34}$ to $a$. Row 3 is then all $a$, so $(AB, CD, AC)$ is lossless. With $BD$ in place of $AC$ the chase changes nothing, and the split stays lossy.

**Trivial cases.** A list that contains $R$ itself is lossless. A split $(AB, BC)$ of $ABC$ with $B \to C$ is lossless by the binary test.

## Known algorithms

- **Binary test.** One closure of $R_1 \cap R_2$, in $O(m)$ time with the linear-time [attribute closure algorithm](/attribute-closure-algorithm/), where $m$ is the size of $F$.
- **The chase of a tableau.** The [chase algorithm](/chase-algorithm/) builds a tableau with one row for each part, applies the dependencies of $F$, and answers "lossless" when a row becomes all distinguished. With $k$ parts and $n$ attributes there are at most $kn$ symbol merges, so it runs in time polynomial in $k$, $n$ and the size of $F$. This is the test of Aho, Beeri and Ullman.
- **Splits on dependencies.** A decomposition built by binary splits $S \to (XY, S - Y)$ with $X \to Y$, as in [BCNF decomposition](/bcnf-decomposition/), is lossless by construction, with no test needed.

## Bounds

- With functional dependencies only, the problem is in polynomial time, by the chase. A counterexample, when one exists, is a relation of at most $k$ tuples: the final tableau read as a relation.
- With multivalued or join dependencies in $F$, the chase still decides the problem, but its tableau can have up to $k^n$ rows, so this test takes exponential time in the worst case.

## Reductions

- **To implication of a join dependency.** $\rho$ is lossless for $F$ if and only if $F \models\ \bowtie[R_1, \ldots, R_k]$. So the problem is a special case of the implication problem for data dependencies, which the chase solves.
- **From the binary case to closure.** The binary case reduces to one instance of the [attribute closure problem](/attribute-closure-problem/), by the binary test above.

## Applications

- **Schema design.** A decomposition used in [normalization](/normalization/) must be lossless, or the stored tables cannot give back the original data. It should also be [dependency preserving](/dependency-preserving-decomposition/), and BCNF cannot always have both.
- **Query evaluation over views.** When a relation is stored as projections, a query must join them. A lossless decomposition makes the join give the original relation.
- **Acyclic schemas.** Joins of a decomposition with an acyclic hypergraph are well behaved: the [Yannakakis algorithm](/yannakakis-algorithm/) evaluates them in time linear in the input and the output.

## References
