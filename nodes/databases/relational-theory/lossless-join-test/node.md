---
tag: R7WCET
kind: algorithm
slug: lossless-join-test
name: Tableau test for lossless join
aliases:
- Aho-Beeri-Ullman lossless join test
- chase test for lossless join
area: databases/relational-theory
level: core
summary: "Decide if a decomposition into any number of parts has a lossless join under FDs. Chase a tableau with one row per part; the join is lossless exactly when some row becomes all distinguished."
solves: [lossless-join-decomposition]
model: word-ram
complexity:
  vars: {k: the number of parts, a: the number of attributes, m: the total size of the functional dependencies}
  time: {worst: O(k^2 a (1 + m log k))}
  space: {extra: O(k a + m)}
properties: {deterministic: true, exact: true, external: false, online: false, in_place: false, recursive: false}
history:
  year: 1979
  people: [Alfred V. Aho, Catriel Beeri, Jeffrey D. Ullman]
  note: Aho, Beeri and Ullman gave the tableau test for a lossless join under functional dependencies in 1979. Maier, Mendelzon and Sagiv made it a special case of the chase in the same year.
prereqs: [functional-dependency, lossless-join-decomposition, attribute-closure-algorithm]
see_also: [chase-algorithm, heaths-theorem, join-dependency, bcnf-decomposition, third-normal-form-synthesis, multivalued-dependency, dependency-preserving-decomposition, normalization]
sources:
  - paper: doi:10.1145/320083.320091
    title: Alfred V. Aho, Catriel Beeri and Jeffrey D. Ullman, The theory of joins in relational databases, ACM Transactions on Database Systems 4(3), 297 to 314 (1979)
    locator: the tableau test for a lossless join under functional dependencies and its proof
  - paper: doi:10.1145/320107.320115
    title: David Maier, Alberto O. Mendelzon and Yehoshua Sagiv, Testing implications of data dependencies, ACM Transactions on Database Systems 4(4), 455 to 469 (1979)
    locator: the chase, of which the test is the case with functional dependencies only
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency, the chase) and Chapter 11 (design and dependencies)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), the test for a lossless join with a tableau
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Section 3.4 (the chase test for a lossless join)
---

The tableau test decides whether a decomposition of a schema into $k$ parts has a lossless join under a set of functional dependencies. It builds a table of symbols with one row for each part and applies the dependencies to it as repair rules. The [lossless join](/lossless-join-decomposition/) page defines the property and proves the test for two parts, which is one attribute closure. This page is the general test for any number of parts, due to Aho, Beeri and Ullman (1979). It is the [chase](/chase-algorithm/) with functional dependencies only, which is why it runs in polynomial time.

## In plain words

You split a table into smaller tables and want to know if joining them always gives back exactly the original rows.

Make a small grid with one line for each smaller table and one column for each column of the original. On each line, mark the columns its smaller table keeps as "known". Fill the other places with "unknown" marks of that line only.

Now apply the rules. If a rule says that rows which agree on some columns must also agree on another column, and two lines agree on those columns, make their marks in the other column the same. Prefer "known" when one of the two is known. Repeat until nothing changes.

If some line is now known in every column, the split is always safe. If not, the grid itself is a table that obeys the rules and gains a row when you split and join it.

## The problem

Let $U$ be a set of $a$ attributes and $F$ a finite set of [functional dependencies](/functional-dependency/) (FDs) over $U$, with total size $m$. We use set semantics: a relation is a finite set of tuples. A *decomposition* is a list $\rho = (R_1, \ldots, R_k)$ of subsets of $U$ with $R_1 \cup \cdots \cup R_k = U$. For a relation $r$ over $U$ write
$$m_\rho(r) = \pi_{R_1}(r) \bowtie \pi_{R_2}(r) \bowtie \cdots \bowtie \pi_{R_k}(r).$$
Always $r \subseteq m_\rho(r)$. The decomposition is *lossless under $F$* when $m_\rho(r) = r$ for each relation $r$ that satisfies $F$. In the notation of [join dependencies](/join-dependency/), the question is whether $F$ implies the join dependency $\bowtie[R_1, \ldots, R_k]$.

**Input:** $U$, $F$ and $\rho$. **Output:** *lossless* or *lossy*. When the answer is *lossy*, the test can also return a relation that satisfies $F$ and is not equal to $m_\rho$ of itself.

## The algorithm

A *tableau* is a table with $k$ rows and one column for each attribute of $U$. Its entries are *symbols*. Each column has its own symbols, and two columns never share one. The symbol $0$ is the *distinguished* symbol of a column (the textbooks write $a_j$), and the positive integers are the other symbols (the textbooks write $b_{ij}$).

```pseudo id=main
LOSSLESS-JOIN-TEST(U, F, R₁, …, Rₖ)
L1  T ← k rows over U; row i has 0 in each column of Rᵢ and the symbol i elsewhere
L2  repeat
L3      changed ← false
L4      for each FD X → Y in F do
L5          for each group G of rows of T that agree on every column of X do
L6              for each A ∈ Y such that the rows of G have two or more symbols in column A do
L7                  s ← the smallest of these symbols
L8                  in column A of every row of T, replace each of these symbols by s; changed ← true
L9  until not changed
L10 if some row of T is all 0 then return (lossless, T)
L11 return (lossy, T)
```

Line L1 encodes the decomposition: row $i$ stands for a tuple that agrees with the target tuple on $R_i$ and is free elsewhere. Lines L5 to L8 are the FD rule. Rows that agree on $X$ must agree on $Y$ in any relation that satisfies $X \to Y$, so their symbols in each column of $Y$ are made equal. Line L7 keeps the smallest symbol, so $0$ always wins and a known value is never lost. Line L8 renames in the whole column, not only in $G$, because equal symbols stand for equal values everywhere.

## Example

Let $U = ABCDE$, $F = \{A \to C,\ B \to C,\ C \to D,\ DE \to C,\ CE \to A\}$ and $\rho = (AD, AB, BE, CDE, AE)$. The table lists the rows after each FD that changes the tableau. The columns are $A, B, C, D, E$.

| step | row 1 ($AD$) | row 2 ($AB$) | row 3 ($BE$) | row 4 ($CDE$) | row 5 ($AE$) |
|---|---|---|---|---|---|
| start (L1) | 0 1 1 0 1 | 0 0 2 2 2 | 3 0 3 3 0 | 4 4 0 0 0 | 0 5 5 5 0 |
| $A \to C$: rows 1, 2, 5 agree on $A$ | 0 1 1 0 1 | 0 0 1 2 2 | 3 0 3 3 0 | 4 4 0 0 0 | 0 5 1 5 0 |
| $B \to C$: rows 2, 3 agree on $B$ | 0 1 1 0 1 | 0 0 1 2 2 | 3 0 1 3 0 | 4 4 0 0 0 | 0 5 1 5 0 |
| $C \to D$: rows 1, 2, 3, 5 agree on $C$ | 0 1 1 0 1 | 0 0 1 0 2 | 3 0 1 0 0 | 4 4 0 0 0 | 0 5 1 0 0 |
| $DE \to C$: rows 3, 4, 5 agree on $DE$ | 0 1 0 0 1 | 0 0 0 0 2 | 3 0 0 0 0 | 4 4 0 0 0 | 0 5 0 0 0 |
| $CE \to A$: rows 3, 4, 5 agree on $CE$ | 0 1 0 0 1 | 0 0 0 0 2 | 0 0 0 0 0 | 0 4 0 0 0 | 0 5 0 0 0 |

In the step for $DE \to C$, the group holds the symbols $0$ and $1$ in column $C$, and the symbol $1$ is replaced in all four rows that hold it, rows 1 and 2 included. The second round changes nothing. Row 3 is all $0$, so the decomposition is lossless.

Each of the five FDs is needed. Without $CE \to A$, the chase stops one step earlier with row 3 equal to $(3, 0, 0, 0, 0)$ and no row all $0$. The five final rows, read as tuples, satisfy the other four FDs. Their projections on $AD$, $AB$, $BE$, $CDE$ and $AE$ (from rows 1, 2, 3, 4 and 5) all contain an all-$0$ tuple, so $(0,0,0,0,0)$ is in the join and not in the relation.

## Correctness

The proof has two directions and rests on one invariant.

*Lossless answer.* Let $r$ satisfy $F$ and let $w \in m_\rho(r)$, with tuples $t_i \in r$ that agree with $w$ on $R_i$. Map the symbol $0$ of column $A$ to $w[A]$ and the symbol $i$ to $t_i[A]$. Then row $i$ of the start maps to $t_i \in r$. A step merges symbols that occur in rows which agree on $X$. Their images are tuples of $r$ that agree on $X$, so they agree on $Y$, and the merged symbols already had the same image. So after each step every row still maps into $r$. If a row ends all $0$, it maps to $w$, so $w \in r$.

*Lossy answer.* The final tableau satisfies $F$, because the last round finds no group with two symbols in a column of a right side. The symbol $0$ is never replaced, so row $i$ still holds $0$ on $R_i$. So the all-$0$ tuple is in $m_\rho(T)$, and it is not a row of $T$. Thus $T$ is a counterexample.

*Two parts.* For $k = 2$ the two rows agree exactly on the columns of the closure $(R_1 \cap R_2)^+$ at the end, so the test reduces to the closure test of the [lossless join](/lossless-join-decomposition/) page. The proof file has all the details and the bound on the rounds.

## Complexity

Let $k$ be the number of parts, $a$ the number of attributes and $m$ the total size of $F$.

- **Rounds.** Each column starts with at most $k$ symbols, one per row, and each change at line L8 removes at least one of them. So there are at most $a(k-1)$ changes, and at most $a(k-1) + 1$ rounds, since each round except the last one makes a change.
- **One round.** Grouping the rows on $X$ by sorting costs $O(k |X| \log k)$ for one FD, so a round costs $O(k m \log k)$ apart from line L8. One change at line L8 costs $O(k)$, and all changes together cost $O(a k^2)$.
- **Total.** $O(k^2 a (1 + m \log k))$ time in the worst case, or $O(k^2 a (1 + m))$ expected time with a hash table for the groups. The extra space is $O(ka + m)$ for the tableau and the FDs.

This is polynomial in the size of the input. The answer does not need $m_\rho(r)$ for any real relation, which can have up to $|r|^k$ tuples.

## Properties

- **Exact.** A *lossless* answer is a proof for every relation that satisfies $F$, and a *lossy* answer comes with a counterexample of $k$ tuples.
- **Independent of the order.** The order of the FDs and of the parts does not change the answer, because the final tableau of the chase is unique up to a renaming of the symbols.
- **Small counterexamples.** If a decomposition into $k$ parts is lossy under $F$, there is a counterexample with at most $k$ tuples, and the final tableau is one.
- **No preprocessing.** $F$ need not be a minimal cover, and implied FDs need not be listed.

## Variants and improvements

- **FDs and MVDs or JDs.** If the constraints include [multivalued dependencies](/multivalued-dependency/) or join dependencies, add the JD rule of the [chase](/chase-algorithm/), which adds rows. The test then still decides the question, but the tableau can grow, and the polynomial bound is lost.
- **Union-find.** Keep the symbols of each column in a union-find structure. Line L8 then merges two classes and does not rewrite the column, and the groups are found on the class representatives.
- **Two parts.** For $k = 2$, compute $(R_1 \cap R_2)^+$ with the [attribute closure algorithm](/attribute-closure-algorithm/) in linear time. This is [Heath's theorem](/heaths-theorem/) together with its converse for FDs.
- **Decompositions that are lossless by construction.** [BCNF decomposition](/bcnf-decomposition/) splits on an FD at each step, so each split is lossless by Heath's theorem and the whole result is lossless. [3NF synthesis](/third-normal-form-synthesis/) adds a part that holds a key, and the row of that part becomes all $0$ in the test.

## When to use it

Use the test when a designer proposes a decomposition with three or more parts, or when parts are merged or split by hand after an algorithm has run. For two parts, the closure test is simpler and faster. For a decomposition produced by the BCNF or 3NF algorithms, the test is not needed, but it is a good check of an implementation of those algorithms. When the answer is *lossy*, show the final tableau: its rows are a small instance that loses information, which helps to explain the problem.

## Pitfalls

- **Testing two parts at a time.** With $F = \{A \to B,\ C \to D\}$ and $\rho = (AB, CD, AC)$, the pair $AB$, $CD$ has no common attribute, so its join is a cross product. Yet the three parts together are lossless. A lossless join is a property of the whole decomposition, not of each pair.
- **Keeping the wrong symbol.** If a free symbol replaces $0$, the test can miss an all-$0$ row and answer *lossy* for a lossless decomposition.
- **Renaming only inside the group.** The replacement at line L8 must cover the whole column. Otherwise a later FD sees two different symbols for one value.
- **Stopping after one pass.** A later FD can create agreement that an earlier FD needs. The loop must run until a whole round changes nothing.
- **Using only the FDs that fit in one part.** The test needs $F$ over all of $U$. In the example, $A \to C$, $B \to C$ and $CE \to A$ fit in no part, and without any one of them the answer is *lossy*.

## Implementations

## History

Aho, Beeri and Ullman (1979) studied when the natural join of projections gives back a relation, and gave this test for functional dependencies in their paper on the theory of joins. In the same year Maier, Mendelzon and Sagiv defined the chase, which applies functional and join dependencies to a tableau, and showed that it decides the implication of these dependencies. The lossless-join test is the case of the chase with FDs only and a start with one row per part. The textbooks of Ullman (1988) and of Garcia-Molina, Ullman and Widom present it as the standard test, and Abiteboul, Hull and Vianu (1995) present it as an instance of the chase.

## References
