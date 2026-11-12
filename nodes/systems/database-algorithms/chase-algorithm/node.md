---
tag: JMAKT7
kind: algorithm
slug: chase-algorithm
name: Chase algorithm
aliases:
- tableau chase
- chase procedure for dependencies
area: systems/database-algorithms
level: advanced
summary: "Repair a tableau of symbols with functional and join dependencies until none is violated. The result decides implication of these dependencies and tests a lossless join."
solves: [lossless-join-decomposition, dependency-implication-problem]
model: word-ram
complexity:
  vars: {s: the number of rows of the starting tableau, n: the number of attributes, m: the total size of the functional dependencies}
  time: {worst: O(s^2 n (n + m))}
  space: {extra: O(s n)}
prereqs: [functional-dependency, relational-algebra, lossless-join-decomposition]
see_also: [dependency-implication-problem, armstrongs-axioms, attribute-closure-algorithm, bcnf-decomposition, chandra-merlin-theorem, query-containment-problem, normalization]
sources:
  - paper: doi:10.1145/320107.320115
    title: David Maier, Alberto O. Mendelzon and Yehoshua Sagiv, Testing implications of data dependencies, ACM Transactions on Database Systems 4(4), 455 to 469 (1979)
    locator: the chase of a tableau with functional and join dependencies, its termination, and the decision of implication
  - paper: doi:10.1145/320083.320091
    title: Alfred V. Aho, Catriel Beeri and Jeffrey D. Ullman, The theory of joins in relational databases, ACM Transactions on Database Systems 4(3), 297 to 314 (1979)
    locator: the tableau test for a lossless join under functional dependencies
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency), the chase and its use for implication
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), the tableau test and the chase
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Section 3.4 (the chase test for a lossless join)
---

The chase is a procedure on a tableau, a table whose entries are symbols instead of values. It applies the dependencies of a set $D$ to the tableau as repair rules. A [functional dependency](/functional-dependency/) makes two symbols equal, and a join dependency adds rows. When no rule applies, the tableau satisfies $D$. With a suitable start, the final tableau tells whether $D$ implies a given dependency, and when it does not, the final tableau is a counterexample. The test for a [lossless join](/lossless-join-decomposition/) of Aho, Beeri and Ullman (1979) is the chase with functional dependencies. Maier, Mendelzon and Sagiv (1979) gave the chase for functional and join dependencies together and proved that it decides implication for them.

## In plain words

You want to know whether some rules about a table force another rule. Instead of trying real tables, you build a small table of placeholders. Two placeholders that are the same must hold the same value. One kind of placeholder stands for "the value we care about"; the others are free.

Then you repair the table. If a rule says that two rows that agree on some columns must agree on another column, and they do not, you make those two placeholders the same. If a rule says that some combinations of row parts must also be rows, you add those rows. You repeat until no rule is broken.

At the end you look for a pattern. If you find it, the rules force the new rule. If not, the repaired table itself is a table that obeys all the rules and breaks the new one.

## The problem

Let $R$ be a schema with $n$ attributes and $D$ a finite set of dependencies over $R$ of two kinds:

- a *functional dependency* (FD) $X \to Y$, which holds in a relation $r$ when two tuples of $r$ that agree on $X$ also agree on $Y$;
- a *join dependency* (JD) $\bowtie[S_1, \ldots, S_k]$ with $S_1 \cup \cdots \cup S_k = R$, which holds in $r$ when $r = \pi_{S_1}(r) \bowtie \cdots \bowtie \pi_{S_k}(r)$. A *multivalued dependency* (MVD) $X \twoheadrightarrow Y$ is the JD $\bowtie[XY,\ X(R - Y)]$.

The *implication problem* asks, for a further dependency $\sigma$, whether $D \models \sigma$: does every relation that satisfies $D$ also satisfy $\sigma$? The [lossless-join problem](/lossless-join-decomposition/) is the case where $\sigma$ is the JD of the parts of a decomposition. With FDs only and $\sigma$ an FD, this is the [dependency implication problem](/dependency-implication-problem/).

A *tableau* is a finite set of rows over $R$ whose entries are *symbols*. Each column has its own symbols, and one of them, written $0$ (often $a$ in the textbooks), is the *distinguished* symbol of the column. The others are written as positive integers (often $b_{ij}$).

## The algorithm

```pseudo id=main
CHASE(T, D)
L1  T ← the starting tableau
L2  repeat
L3      changed ← false
L4      for each FD X → Y in D do
L5          while rows u, v of T have u[X] = v[X] and u[A] ≠ v[A] for some A ∈ Y do
L6              old ← max(u[A], v[A]); new ← min(u[A], v[A])
L7              replace old by new in column A of every row; changed ← true
L8      for each JD ⋈[S₁, …, Sₖ] in D do
L9          J ← π_{S₁}(T) ⋈ ⋯ ⋈ π_{Sₖ}(T)
L10         if J ⊄ T then
L11             T ← T ∪ J; changed ← true
L12 until not changed; return T
```

Lines L5 to L7 are the *FD rule*. Two rows agree on $X$, so in any relation that satisfies $X \to Y$ they must also agree on $Y$. The rule makes the two symbols of column $A$ equal. It keeps the smaller one, so the distinguished symbol $0$ always wins and is never lost. Lines L9 to L11 are the *JD rule*. Any relation that satisfies the JD contains the join of its own projections, so the rule adds the rows of that join that are missing. It makes no new symbols.

**The starting tableaux.**

- *To test $D \models X \to Y$:* two rows, $u$ all $0$, and $v$ with $0$ on $X$ and the symbol $1$ elsewhere. The answer is yes when the chase replaces the symbol $1$ by $0$ in each column of $Y$.
- *To test $D \models\ \bowtie[S_1, \ldots, S_k]$:* one row for each $S_i$, with $0$ on $S_i$ and the symbol $i$ elsewhere. The answer is yes when the final tableau has a row that is all $0$. For the parts of a decomposition, this is the lossless-join test.

## Example

Let $R = ABC$ and $D = \{A \twoheadrightarrow B,\ B \to C\}$, where $A \twoheadrightarrow B$ is the JD $\bowtie[AB, AC]$. Does $D$ imply $A \to C$? Start with $u = (0, 0, 0)$ and $v = (0, 1, 1)$, which agree only on $A$.

| round | rule | tableau after the rule |
|---|---|---|
| start | | $(0,0,0)$, $(0,1,1)$ |
| 1 | $B \to C$: $u$ and $v$ differ on $B$, so no step | $(0,0,0)$, $(0,1,1)$ |
| 1 | JD $\bowtie[AB, AC]$: the projections are $\{00, 01\}$ on $AB$ and $\{00, 01\}$ on $AC$; the join adds $(0,0,1)$ and $(0,1,0)$ | $(0,0,0)$, $(0,1,1)$, $(0,0,1)$, $(0,1,0)$ |
| 2 | $B \to C$: $(0,0,0)$ and $(0,0,1)$ agree on $B$, so $1$ becomes $0$ in column $C$ | $(0,0,0)$, $(0,1,0)$ |
| 2 | JD: the join gives no new row | $(0,0,0)$, $(0,1,0)$ |
| 3 | no rule applies | $(0,0,0)$, $(0,1,0)$ |

The symbol $1$ is gone from column $C$, so $D \models A \to C$. The symbol $1$ stays in column $B$, so $D \not\models A \to B$, and the final tableau, read as a relation of two tuples, is the counterexample: it satisfies $A \twoheadrightarrow B$ and $B \to C$, and its two tuples agree on $A$ but not on $B$.

The lossless-join page has an example of the test for a decomposition with three parts and two FDs.

## Correctness

The proof rests on one fact about a single step. Say that a map $h$ from symbols to values *embeds* the tableau in a relation $r$ when it maps each row to a tuple of $r$. If $r$ satisfies $D$ and $h$ embeds $T$ in $r$, then $h$ also embeds the tableau after one step in $r$. For an FD step, the two rows map to tuples of $r$ that agree on $X$, so they agree on $A$, and the two symbols that the step makes equal already have the same value under $h$. For a JD step, each new row is in the join of projections of $T$, so its image is in the join of projections of $r$, which is $r$.

*Termination.* No step makes a new symbol. An FD step removes one symbol from one column, so there are at most $sn$ of them. A JD step adds rows built from the present symbols, and there are at most $s^n$ such rows. So the chase stops.

*The final tableau satisfies $D$*, because in the last round no rule applies.

*Deciding implication.* Take the JD test. If the all-$0$ row appears, let $r$ satisfy $D$ and let $w$ be in the join of the projections of $r$, with $t_i \in r$ equal to $w$ on $S_i$. Map $0$ to $w$ and the symbol $i$ to $t_i$; this embeds the start in $r$, so at the end the all-$0$ row maps to $w$, and $w \in r$. If the all-$0$ row does not appear, the final tableau satisfies $D$ but not the JD, since each row $i$ keeps its $0$ entries on $S_i$, so the all-$0$ row is in the join of its projections. The FD test is the same argument with two rows. The full proof is in the proof file of this page.

## Complexity

Let $s$ be the number of rows of the starting tableau, $n$ the number of attributes and $m$ the total size of the FDs. With $s = k$ parts for the lossless test, or $s = 2$ for an FD test:

- **FDs only.** Each FD step removes a symbol, so there are at most $sn$ steps. One pass over all FDs that finds a violation costs $O(sm)$ with hashing of the rows on $X$, and one replacement costs $O(sn)$. So the chase takes $O(s^2 n (n + m))$ time and $O(sn)$ extra space. This is the bound in the header. It makes the lossless-join test polynomial.
- **With JDs or MVDs.** The tableau can grow to $s^n$ rows, so the chase can take time exponential in $n$. Implication of a JD by MVDs is already NP-hard (Fischer and Tsou 1983), so a polynomial worst case is not expected for the general JD case. For FDs and MVDs alone, implication is decidable in polynomial time by other methods (Beeri 1980, with dependency bases), so the chase is not the fastest method there.

## Properties

- **Sound and complete for FDs and JDs.** A yes answer is a proof of implication, and a no answer comes with a counterexample, the final tableau.
- **Result is unique up to renaming.** The final tableau does not depend, up to a renaming of the symbols, on the order in which the rules are applied (Maier, Mendelzon and Sagiv 1979). The answers to the tests above therefore do not depend on the order.
- **Works on finite relations.** For FDs and JDs, implication over all relations and over finite relations are the same, and the counterexample is finite.
- **Does not need a minimal cover.** The FD set can be in any form.

## Variants and improvements

- **Chase with tuple-generating dependencies.** The JD rule is a special case of a *tuple-generating dependency* (TGD): if some rows are present, then a row must be present. A full TGD only uses symbols that are already there, so its chase stops like the JD chase. An *embedded* TGD may need a new symbol for a column that it does not fix. Then the chase can add rows with new symbols forever and need not stop, and implication of general TGDs is undecidable (Beeri and Vardi 1981).
- **Chase for query containment and optimization.** A conjunctive query is a tableau. The chase of a query with the dependencies of a schema, followed by the [Chandra-Merlin](/chandra-merlin-theorem/) homomorphism test, decides [query containment](/query-containment-problem/) under FDs and full dependencies. Later work uses the chase for data exchange and for query answering under constraints.
- **Union-find for the FD rule.** Keep the symbols of each column in a union-find structure, so that line L7 only merges two classes and does not rewrite the rows.
- **The binary test.** For two parts with FDs only, the chase reduces to one [attribute closure](/attribute-closure-algorithm/): the split is lossless when the common attributes fix one part.

## When to use it

Use the chase to test whether a decomposition with more than two parts has a lossless join, and to test implication when MVDs or JDs occur, where the attribute closure is not enough. It also gives a counterexample when the answer is no, which helps to explain a design error. For FDs alone and an FD target, use the [attribute closure algorithm](/attribute-closure-algorithm/) instead, which is linear.

## Pitfalls

- **Keeping the wrong symbol.** When the FD rule equates a distinguished symbol with a free one, the distinguished one must stay. If the free symbol wins, the test misses implied dependencies.
- **Renaming only in the two rows.** Line L7 must replace the symbol in every row of the column, since equal symbols stand for equal values.
- **Mixing columns.** A symbol belongs to one column. If the same name is used in two columns, a replacement in one column must not change the other.
- **Stopping after one pass.** An FD step can enable a JD step and the other way around. The chase must loop until a whole round changes nothing.
- **Expecting termination for any dependency.** With embedded TGDs, as in data exchange, the chase may run forever. Bound it or check a sufficient condition for termination.

## Implementations

## History

Aho, Beeri and Ullman introduced the tableau test for a lossless join in 1979, and Maier, Mendelzon and Sagiv named the chase and gave it for functional and join dependencies in the same year, with the proof that it decides implication. Tableaux as queries come from Aho, Sagiv and Ullman (1979), and the link between the chase and query containment came soon after. The chase is now a basic tool of database theory, used for implication, query optimization under constraints and data exchange.

## References
