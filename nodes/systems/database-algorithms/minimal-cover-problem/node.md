---
tag: M2Z1TE
kind: problem
slug: minimal-cover-problem
name: Minimal cover problem
aliases:
- canonical cover
- minimal cover of functional dependencies
- irreducible set of dependencies
area: systems/database-algorithms
level: core
summary: "Find an FD set equivalent to F with single-attribute right sides, no extraneous left-side attribute and no redundant FD. Polynomial, but minimal covers are not unique."
prereqs: [dependency-implication-problem]
see_also: [third-normal-form-synthesis, attribute-closure-algorithm, armstrongs-axioms, third-normal-form, normalization, dependency-preserving-decomposition, horn-clause]
sources:
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.3 (covers of sets of dependencies, minimal covers)
  - paper: doi:10.1145/322217.322223
    title: David Maier, Minimum covers in relational database model, Journal of the ACM 27(4), 664 to 674 (1980)
    locator: a polynomial algorithm for covers with the fewest FDs, and the NP-completeness of covers with the fewest attribute occurrences
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: nonredundant and reduced covers and their computation with the linear closure algorithm
  - paper: doi:10.1145/320493.320489
    title: Philip A. Bernstein, Synthesizing third normal form relations from functional dependencies, ACM Transactions on Database Systems 1(4), 277 to 298 (1976)
    locator: the reduced cover as the first step of 3NF synthesis
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 8.2 (covers of sets of functional dependencies); Section 11.2 (their use in 3NF synthesis)
---

The minimal cover problem asks for a simpler set of [functional dependencies](/functional-dependency/) that is equivalent to a given set $F$. A minimal cover has one attribute on each right side, no attribute that can be dropped from a left side, and no FD that the others imply. Three passes of [attribute closure](/attribute-closure-algorithm/) compute one in polynomial time, and the order of the passes matters. A set can have several minimal covers of different sizes, and the minimal cover is the input of [3NF synthesis](/third-normal-form-synthesis/).

## In plain words

A designer often writes rules that say the same thing more than once. Some rules follow from the others. Some rules ask for more columns on the left than they need. The goal is a clean list that says exactly the same thing. First, split each rule so that it fixes one column. Then remove extra columns from each left side. Last, remove each rule that the other rules already give. Do the steps in this order, because removing columns can make a rule redundant. The clean list is not always unique, and it is not always the shortest one.

## Definition

Let $F$ and $G$ be sets of FDs over $U$. $G$ is a *cover* of $F$ if $G^+ = F^+$, that is, $F$ and $G$ are equivalent. A cover $G$ is *minimal* if:

1. each FD of $G$ has the form $X \to A$ with one attribute $A$, and $A \notin X$;
2. no FD is *redundant*: for each $X \to A$ in $G$, $G - \{X \to A\}$ is not equivalent to $G$;
3. no left-side attribute is *extraneous*: for each $X \to A$ in $G$ and $B \in X$, $(G - \{X \to A\}) \cup \{X - B \to A\}$ is not equivalent to $G$.

Condition 2 holds if and only if $A \notin X^+$ under $G - \{X \to A\}$. Condition 3 holds if and only if $A \notin (X - B)^+$ under $G$, since $X - B \to A$ implies $X \to A$, so the new set always implies $G$.

**Input.** $U$ and $F$, of size $n = |U|$ and $m = \|F\|$. **Output.** A minimal cover of $F$.

Every $F$ has a minimal cover, and the algorithm below finds one with at most $m$ FDs.

## Variants

- **Canonical cover.** Some textbooks combine the FDs with the same left side, $X \to A_1, \ldots, X \to A_k$, into $X \to A_1 \cdots A_k$, and call the result a canonical cover. It is a minimal cover in a different notation.
- **Nonredundant cover.** Only condition 2. Checking it needs one closure per FD.
- **Left-reduced cover.** Only conditions 1 and 3.
- **Minimum cover.** A cover with the fewest FDs among all covers, where a right side can be a set of attributes. Maier (1980) gave a polynomial algorithm, based on the classes of left sides that are equivalent under $F$.
- **Optimum cover.** A cover with the fewest attribute occurrences $\|G\|$. This is NP-complete (Maier 1980).
- **Cover of a projection.** Given $F$ over $U$ and $R \subseteq U$, find a cover of the FDs that hold on $R$. The projected set can need exponentially many FDs. This is the main cost of testing [dependency preservation](/dependency-preserving-decomposition/) and [BCNF decomposition](/bcnf-decomposition/) in general.

## Examples

**A simple case.** Let $F = \{A \to BC,\ B \to C,\ A \to B,\ AB \to C\}$ over $ABC$.

1. Split right sides: $A \to B$, $A \to C$, $B \to C$, $AB \to C$.
2. Left-reduce: in $AB \to C$, $A^+ = ABC$ holds $C$, so $B$ is extraneous and the FD becomes $A \to C$. Now the set is $\{A \to B, A \to C, B \to C\}$.
3. Remove redundant FDs: $A \to C$ is implied by $A \to B$ and $B \to C$.

The minimal cover is $\{A \to B, B \to C\}$.

**The order matters.** Let $F = \{B \to A,\ C \to A,\ AC \to B\}$. With redundancy removal first, no FD is redundant: $B^+ = B$ without $B \to A$, $C^+ = C$ without $C \to A$, and $AC^+ = AC$ without $AC \to B$. Left reduction then changes $AC \to B$ into $C \to B$, because $C^+ = ABC$. The result $\{B \to A, C \to A, C \to B\}$ is not minimal: $C \to A$ now follows from $C \to B$ and $B \to A$. In the correct order, left reduction comes first and gives $\{B \to A, C \to A, C \to B\}$, and redundancy removal then drops $C \to A$. The minimal cover is $\{B \to A, C \to B\}$.

**Minimal covers are not unique.** Let $F = \{A \to BC,\ B \to AC,\ C \to AB\}$, so $A$, $B$ and $C$ determine each other. Then

- $\{A \to B,\ B \to C,\ C \to A\}$ is a minimal cover,
- $\{A \to C,\ C \to B,\ B \to A\}$ is another one, and
- $\{A \to C,\ B \to C,\ C \to A,\ C \to B\}$ is a third one, with 4 FDs.

The algorithm below, with the FDs in sorted order, returns the third. So two minimal covers of one set can have different numbers of FDs, and the result depends on the order in which the algorithm tests the FDs.

**Ullman's course schema.** $F = \{C \to T, HR \to C, HT \to R, CS \to G, HS \to R\}$ is already a minimal cover. Each left side of two attributes is needed: for example, $H^+ = H$ and $R^+ = R$, so $HR \to C$ cannot lose an attribute.

## Known algorithms

**The three-step algorithm.** Ullman (1988) and Beeri and Bernstein (1979) give this algorithm, with closures from the [attribute closure algorithm](/attribute-closure-algorithm/).

1. **Split.** Replace each $X \to Y$ by the FDs $X \to A$ for $A \in Y - X$.
2. **Left-reduce.** For each $X \to A$, and for each $B \in X$ in turn: if $A \in (X - B)^+_F$, replace $X$ by $X - B$.
3. **Remove redundant FDs.** For each FD $X \to A$ of the current set $G$ in turn: if $A \in X^+$ under $G - \{X \to A\}$, remove it from $G$.

*Why it works.*

- Each step keeps an equivalent set. Step 1 uses the union and decomposition rules. In step 2, $A \in (X - B)^+_F$ means $F \models X - B \to A$, so the new FD is implied, and it implies the old one. In step 3, a removed FD is implied by the rest.
- Since each set in step 2 is equivalent to $F$, closures can be taken under the original $F$; they do not change. One pass over the attributes of $X$ is enough: if $B$ is kept, then $A \notin (X - B)^+$, and later removals make the left side smaller, so $A$ stays outside the closure of each smaller set minus $B$.
- Step 3 keeps condition 3. Removing an FD makes the closures smaller, so an attribute that was not extraneous stays not extraneous. It also leaves no redundant FD: if an FD is kept, it is not implied by the others, and later removals only make the others weaker.
- Doing step 3 before step 2 is wrong, as the example above shows: left reduction makes an FD stronger, which can make another FD redundant.

*Cost.* After step 1, there are at most $m$ FDs, with at most $m$ left-side attributes in total. Step 2 makes one closure per left-side attribute, and step 3 one closure per FD. With linear closures, the time is $O(m \cdot (n + m))$.

**Minimum covers.** Maier (1980) groups the FDs by the closures of their left sides, and inside each group keeps as few FDs as possible. The algorithm runs in polynomial time and returns a cover with the fewest FDs.

## Bounds

- A minimal cover is computed in $O(m(n + m))$ time with the three-step algorithm.
- A minimum cover (fewest FDs) takes polynomial time (Maier 1980).
- An optimum cover (fewest attribute occurrences) is NP-hard to find; its decision version is NP-complete (Maier 1980).
- Testing whether a given $G$ is a minimal cover of $F$ takes one equivalence test and $O(m)$ closures. The implementation checks the output of the algorithm against a brute-force test of the three conditions, on 300 random sets.

## Reductions

- **Equivalence.** The minimal cover problem is built from the [dependency implication problem](/dependency-implication-problem/): each test in steps 2 and 3 is one membership query.
- **Horn formulas.** Under the map of FDs to [Horn clauses](/horn-clause/), a minimal cover is an equivalent Horn formula with no redundant clause, in which no clause can lose a body literal. The questions about minimum and optimum covers are questions about the shortest equivalent Horn formula, in two measures of size.

## Applications

- **3NF synthesis.** [Bernstein's synthesis](/third-normal-form-synthesis/) makes one relation schema per left side of a minimal cover. A cover with fewer FDs gives fewer or smaller schemas.
- **Constraint checking.** A database system checks each declared FD on each update. A minimal cover checks fewer and smaller FDs and enforces the same constraints.
- **Dependency preservation.** To test whether a decomposition preserves $F$, test whether the union of the projected FDs implies each FD of a cover of $F$. A small cover makes fewer tests.
- **Normal form tests.** The tests for [third normal form](/third-normal-form/) work on FDs with one attribute on the right side, which is condition 1.

## References
