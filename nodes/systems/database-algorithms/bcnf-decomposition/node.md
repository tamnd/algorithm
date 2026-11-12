---
tag: F3CVSY
kind: algorithm
slug: bcnf-decomposition
name: BCNF decomposition
aliases:
- BCNF decomposition algorithm
- decomposition into Boyce-Codd normal form
area: systems/database-algorithms
level: core
summary: "Split a relation schema on a functional dependency that violates BCNF, again and again, until every part is in BCNF. The result is a lossless join, but it can lose dependencies."
solves: [lossless-join-decomposition]
model: word-ram
complexity:
  vars: {n: the number of attributes, m: the total size of the set of functional dependencies}
  time: {worst: O(4^n m)}
  space: {extra: O(n^2)}
prereqs: [boyce-codd-normal-form, attribute-closure-algorithm, functional-dependency]
see_also: [lossless-join-decomposition, dependency-preserving-decomposition, third-normal-form-synthesis, chase-algorithm, normalization, third-normal-form]
sources:
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), lossless-join decomposition into BCNF
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Section 3.3 (decomposition into BCNF) and Section 3.4 (the chase test and dependency preservation)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies), decomposition into BCNF
  - paper: doi:10.1145/990511.990513
    title: Don-Min Tsou and Patrick C. Fischer, Decomposition of a relation scheme into Boyce-Codd normal form, ACM SIGACT News 14(3), 23 to 29 (1982)
    locator: the polynomial-time algorithm for a lossless BCNF decomposition, and the NP-hardness of deciding whether a dependency-preserving BCNF decomposition exists
  - paper: "I. J. Heath, Unacceptable file operations in a relational data base, Proceedings of the 1971 ACM SIGFIDET Workshop on Data Description, Access and Control, pages 19 to 33"
    locator: the theorem that a relation satisfying X -> Y equals the join of its projections on XY and X with the other attributes
---

BCNF decomposition turns a relation schema $R$ with [functional dependencies](/functional-dependency/) $F$ into a set of schemas that are each in [Boyce-Codd normal form](/boyce-codd-normal-form/). It finds a dependency $X \to Y$ that violates BCNF in a part $S$, replaces $S$ by $X \cup Y$ and $S \setminus Y$, and repeats. Each split is a [lossless join](/lossless-join-decomposition/) by Heath's theorem, so the whole result is lossless. The result is not unique, and it may not be [dependency preserving](/dependency-preserving-decomposition/).

## In plain words

A table stores the same fact many times when some columns fix other columns but are not a key. For example, a zip code fixes the city, so each row with that zip code repeats the city.

The method finds such a group of columns. It moves the group and the columns that it fixes into a new small table. It leaves the group, but not the fixed columns, in the old table. The group is in both tables, so a join on the group puts the rows back together with no extra rows. The method then looks at each of the two tables again, and stops when no table has such a group. The tables you get depend on which group you split first, and some rules between columns can end up split over two tables.

## The problem

The input is a finite set of attributes $R$ and a set $F$ of functional dependencies over $R$. The output is a list of schemas $R_1, \ldots, R_k$ with $R_1 \cup \cdots \cup R_k = R$ such that:

- each $R_i$ is in BCNF under the projection $\pi_{R_i}(F)$, the set of all $X \to A$ with $X \cup \{A\} \subseteq R_i$ that $F$ implies;
- the decomposition is lossless: $r = \pi_{R_1}(r) \bowtie \cdots \bowtie \pi_{R_k}(r)$ for every relation $r$ over $R$ that satisfies $F$.

This is the BCNF case of the [lossless-join decomposition problem](/lossless-join-decomposition/). It always has a solution, for example the result of this algorithm. A solution that also preserves the dependencies may not exist.

## The algorithm

$X^+$ is the closure of $X$ under $F$, computed by the [attribute closure algorithm](/attribute-closure-algorithm/).

```pseudo id=main
BCNF-DECOMPOSE(R, F)
L1  todo ← [R], done ← [ ]
L2  while todo is not empty do
L3      S ← pop(todo)
L4      find X ⊂ S with (X⁺ ∩ S) ≠ X and S ⊄ X⁺      ▷ a violation in S
L5      if there is no such X then
L6          append S to done; continue
L7      Y ← (X⁺ ∩ S) − X
L8      push S − Y and X ∪ Y onto todo
L9  return done
```

Line L4 looks for a set $X$ inside the part $S$ that fixes some other attribute of $S$ but not all of $S$. That is a violation of BCNF in the projection of $F$ onto $S$. Line L7 takes all the attributes of $S$ that $X$ fixes, not only the right side of one dependency. This makes the part $X \cup Y$ as large as possible and the other part as small as possible. Line L8 keeps $X$ in both parts, so $X$ is the common attribute set of the join.

The search of line L4 tries the subsets of $S$ in order of size. For the first part, $S = R$, it is enough to check the dependencies of $F$ themselves. For a later part it is not: a violation can come from a dependency that $F$ implies but does not list (see Pitfalls).

## Example

Let $R = ABCDE$ and $F = \{A \to B,\ B \to C,\ CD \to E\}$. The closures are $A^+ = ABC$, $B^+ = BC$, $CD^+ = CDE$ and $AD^+ = ABCDE$, so $AD$ is the only key. The table shows each pop of line L3, with the parts pushed last popped first.

| step | part $S$ | violation $X \to Y$ (L4, L7) | pushed (L8) | done |
|---|---|---|---|---|
| 1 | $ABCDE$ | $A \to BC$ | $ADE$, $ABC$ | |
| 2 | $ABC$ | $B \to C$ | $AB$, $BC$ | |
| 3 | $BC$ | none | | $BC$ |
| 4 | $AB$ | none | | $BC$, $AB$ |
| 5 | $ADE$ | none ($AD^+ \supseteq ADE$) | | $BC$, $AB$, $ADE$ |

The output is $\{AB, BC, ADE\}$. It is lossless and each part is in BCNF. But it loses $CD \to E$: no part contains $C$, $D$ and $E$, and the projected dependencies $A \to B$, $B \to C$ and $AD \to E$ give $CD^+ = CD$.

A different first split gives a better result. Split first on $CD \to E$: this gives $CDE$ and $ABCD$. Then $ABCD$ splits on $A \to BC$ into $ABC$ and $AD$, and $ABC$ splits into $AB$ and $BC$. The output $\{CDE, AD, AB, BC\}$ is lossless, in BCNF and it preserves all three dependencies. So the order of the splits changes the result.

## Correctness

The algorithm stops, and its output covers $R$, is in BCNF part by part, and is lossless. The two key facts are these. First, each split makes two proper, nonempty subsets of $S$: $X \cup Y \subseteq X^+ \cap S \ne S$, and $S - Y \supseteq X$ is a proper subset because $Y \ne \emptyset$; it is not empty because $S \not\subseteq Y$. Second, Heath's theorem: if a relation $s$ over $S$ satisfies $X \to Y$, then $s = \pi_{XY}(s) \bowtie \pi_{S - Y}(s)$. By induction over the split tree, each projection $\pi_S(r)$ equals the join of the projections on the leaves below $S$, so $r$ equals the join of all the output parts. Each output part passed the exhaustive test of line L4, so it is in BCNF. The full proof is in the proof file of this page.

## Complexity

The cost depends on the test of line L4. Let $n = |R|$ and let $m$ be the total size of $F$.

- **Split tree.** Each child is a proper subset of its parent, so the tree of parts has depth at most $n - 1$ and fewer than $2^n$ nodes. The stack `todo` holds at most $n$ parts, so the extra space is $O(n^2)$ besides the output.
- **One test.** Line L4 tries up to $2^{|S|}$ subsets, and each closure costs $O(m)$ with the linear-time closure algorithm. So the worst case of the whole run is $O(2^n \cdot 2^n m) = O(4^n m)$.
- **Lower bound for this approach.** The exhaustive test is not a weakness of the code alone: to decide whether a subschema violates BCNF is NP-complete (Beeri and Bernstein 1979). A run that decides at each node whether the part is in BCNF therefore solves a coNP-complete problem.

The polynomial variant below avoids this by never deciding the question exactly.

## Properties

- **Lossless.** Always, by the proof above.
- **Not dependency preserving in general.** The schema $\{\mathit{street}, \mathit{city}, \mathit{zip}\}$ with $\mathit{street}\,\mathit{city} \to \mathit{zip}$ and $\mathit{zip} \to \mathit{city}$ has no dependency-preserving BCNF decomposition at all. The algorithm returns $\{\mathit{zip}, \mathit{city}\}$ and $\{\mathit{street}, \mathit{zip}\}$.
- **Not unique.** The result depends on the order in which violations are found, as in the example.
- **Not minimal.** The output can have a part that is a subset of another part, or more parts than needed.
- **Deterministic.** With a fixed order of the subsets in line L4, the output is fixed.

## Variants and improvements

- **Polynomial time by a pair test (Tsou and Fischer 1982).** If a part $Y$ is not in BCNF, then there are attributes $A \ne B$ in $Y$ with $A \in (Y - \{A, B\})^+$. (Take a violation $X \to A$ and an attribute $B$ of $Y$ outside $X^+$; then $X \subseteq Y - \{A, B\}$.) So a part where no pair passes this test is in BCNF. The variant starts with $Y = Z$ and, while some pair $A, B$ of $Y$ passes the test, deletes $B$ from $Y$. When it stops, $Y$ is in BCNF, and the last pair found gives $(Y - \{A\}) \to A$. So $Z$ splits losslessly into $Y$ and $Z - \{A\}$, and the variant goes on with $Z - \{A\}$. This uses $O(n^4)$ closures. The test is only sufficient for a violation, so the variant can split a part that is already in BCNF: for $ABC$ with $A \to BC$ it returns $AB$ and $AC$. On the example above it returns $\{AB, AC, ADE\}$, which loses both $B \to C$ and $CD \to E$. This pair-test form is the idea of the polynomial algorithm of Tsou and Fischer; their paper gives the exact procedure and its analysis.
- **Choose the splits to keep dependencies.** Split first on violations whose $X \cup Y$ contains a whole dependency of $F$, as in the second run of the example. This is a heuristic. Tsou and Fischer proved that to decide whether a dependency-preserving BCNF decomposition exists is NP-hard.
- **Use 3NF instead.** [3NF synthesis](/third-normal-form-synthesis/) always gives a lossless and dependency-preserving decomposition into [third normal form](/third-normal-form/), in polynomial time, at the price of some redundancy.

## When to use it

Use BCNF decomposition when the redundancy of the data matters more than checking each dependency inside one table. Check the result with the test for [dependency preservation](/dependency-preserving-decomposition/). If a dependency is lost, either accept that it must be checked with a join, or use 3NF synthesis. For a schema with many attributes, use the polynomial variant, or check only the dependencies of $F$ at the root and accept the extra splits.

## Pitfalls

- **Checking only the listed dependencies in a later part.** Let $R = ABCD$ and $F = \{A \to B,\ B \to C\}$. A split on $A \to B$ with $Y = B$ gives $AB$ and $ACD$. No dependency of $F$ lies inside $ACD$, so a test that uses only $F$ stops there. But $A \to C$ holds and $A$ is not a key of $ACD$. Line L4 must test the projection, with closures, not the list $F$.
- **Forgetting to intersect with the part.** Line L7 must be $Y \leftarrow (X^+ \cap S) - X$. With $Y \leftarrow X^+ - X$, the part $X \cup Y$ can get attributes that are no longer in $S$, and the parts no longer cover $R$ exactly.
- **Splitting on a superkey.** If $S \subseteq X^+$, then $X \to Y$ is not a violation, and line L8 pushes $X \cup Y = S$ again, so the loop never stops. Line L4 must check $S \not\subseteq X^+$.
- **Expecting dependency preservation.** BCNF decomposition can lose a dependency. Test it, and do not assume it.

## Implementations

## History

Codd defined BCNF in 1974. Heath proved in 1971 that a relation that satisfies $X \to Y$ is the join of its projections on $XY$ and on $X$ with the other attributes, which is the reason each split is lossless. The decomposition by repeated splits is the standard method of the textbooks, for example Ullman (1988) and Garcia-Molina, Ullman and Widom. Beeri and Bernstein showed in 1979 that the exact test of a subschema is NP-hard, and Tsou and Fischer gave a polynomial-time lossless BCNF decomposition in 1982, together with the NP-hardness of finding a dependency-preserving one.

## References
