---
tag: NBNPFH
kind: algorithm
slug: string-transformation-synthesis
name: Gulwani's string transformation synthesis
aliases:
- FlashFill algorithm
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: The FlashFill method. Build a DAG over output positions with all substring and constant atoms for each example, intersect the DAGs, and pick the best-ranked path.
model: word-ram
complexity:
  vars: {n: the length of the longest input, m: the length of the longest output, k: the number of examples, p: the number of position expressions that denote one index}
  time: {one example: "O(m^2 n (m + p))", all examples: O(m^(2k) n^k p) worst case}
  space: {one example: O(m^2 n p), all examples: O(m^(2k) n^k p) worst case}
properties: {deterministic: true, recursive: false}
history:
  year: 2011
  people: [Sumit Gulwani]
  note: Published at POPL 2011 and shipped as Flash Fill in Microsoft Excel 2013. Polozov and Gulwani made the method general for any domain-specific language in FlashMeta (2015).
prereqs: [version-space-algebra, directed-acyclic-graph]
see_also: [programming-by-example, bottom-up-enumerative-synthesis, regular-expression, syntax-guided-synthesis, string-constraint-satisfiability, dag-shortest-paths]
sources:
  - paper: doi:10.1145/1926385.1926423
    title: Sumit Gulwani, Automating string processing in spreadsheets using input-output examples, Principles of Programming Languages (POPL 2011)
    locator: pp. 317-330, the language of trace expressions with ConstStr, SubStr, CPos and Pos, the DAG of one example, the intersection of DAGs, conditionals and loops, and the ranking
  - paper: doi:10.1145/2814270.2814310
    title: Oleksandr Polozov and Sumit Gulwani, FlashMeta, a framework for inductive program synthesis, Object-Oriented Programming, Systems, Languages and Applications (OOPSLA 2015)
    locator: pp. 107-126, the general form with witness functions and version space algebras, with FlashFill as one instance
  - paper: doi:10.1007/978-3-319-21690-4_23
    title: Rishabh Singh and Sumit Gulwani, Predicting a correct program in programming by example, Computer Aided Verification (CAV 2015)
    locator: pp. 398-414, a learned ranking function for FlashFill programs
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: chapter 7, programming by examples, with FlashFill as the main example
---

Gulwani's string transformation synthesis is the algorithm behind Flash Fill in Microsoft Excel. From one or a few examples of an input string and the wanted output, it finds a program that maps each input to its output. Programs concatenate pieces, and each piece is a constant or a substring of the input between two positions. For each example the algorithm builds a DAG over the indices of the output, where an edge holds every atom that produces that piece. It intersects the DAGs of the examples and takes the best path by a ranking. The DAGs are a [version space algebra](/version-space-algebra/) for this language; the general problem is [programming by example](/programming-by-example/).

## In plain words

Say that "Alan Turing" must become "A. Turing". Look at each piece of the output. The "A" can be copied from the start of the input, or written as a constant. The "." cannot be copied, so it must be a constant. " Turing" can be copied from the input, from the space to the end. A position in the input can be named in more than one way: "index 4", "the last space", or "where a run of letters ends and a space starts".

The algorithm writes all these choices into one graph, without listing whole programs. With a second example, such as "Grace Hopper" to "G. Hopper", it keeps only the choices that also work there. At the end it picks a path through the graph that copies as much as it can and uses simple position names.

## The problem

**Input.** Examples $(\sigma_1, o_1), \ldots, (\sigma_k, o_k)$ of input and output strings, with non-empty outputs.

**Output.** A program of the language below with $[\![P]\!](\sigma_j) = o_j$ for each $j$, of least cost, or "none".

**The language.** It is a part of the FlashFill language of Gulwani (2011), without conditionals, loops and several input columns:

- A program is Concat$(f_1, \ldots, f_n)$ with $n \ge 1$ atoms.
- An atom is ConstStr$(c)$ for a non-empty string $c$, or SubStr$(p_1, p_2)$, the input from position $p_1$ up to position $p_2$. It is defined only when $p_1 < p_2$, so every atom gives a non-empty string.
- A position is CPos$(k)$, the index $k$ for $k \ge 0$ and the index $|\sigma| + 1 + k$ for $k < 0$, so CPos$(-1)$ is the end. Or it is Pos$(r_1, r_2, c)$: the $c$-th index, from the left for $c > 0$ and from the right for $c < 0$, where a run of the token $r_1$ ends and a run of the token $r_2$ starts. The tokens are digits, letters, spaces, and the empty token $\varepsilon$, which matches at every index. A run is a maximal block of characters of one token. Here $c \in \{\pm 1, \pm 2, \pm 3\}$, and $r_1$ and $r_2$ are not both $\varepsilon$.

**Cost.** The cost of a program is the tuple (number of characters in constants, number of atoms, sum of position costs), compared from left to right. CPos$(0)$ and CPos$(-1)$ cost 1, a Pos costs 2, CPos$(k)$ with $k > 0$ costs 3, and CPos$(k)$ with $k < -1$ costs 4. This prefers copying to constants, short programs, and positions that are named by structure. Gulwani (2011) uses a ranking of the same kind; this exact cost is the one in the code on this page.

## The algorithm

```pseudo id=main
SYNTHESIZE((σ1, o1), …, (σk, ok))
L1  for j = 1 … k do Wj ← DAG(σj, oj)
L2  start ← (0, …, 0); goal ← (|o1|, …, |ok|)
L3  for each state u reachable from start, in increasing order of u1 + … + uk do
L4      for each w with uj < wj ≤ |oj| for every j do
L5          A ← W1(u1, w1) ∩ … ∩ Wk(uk, wk)
L6          if A ≠ ∅ then relax w: cost(w) ← min(cost(w), cost(u) + cost of the cheapest atom of A)
L7  return the program on a cheapest path from start to goal, or none if goal is not reached

DAG(σ, o)                              ▷ P(t): all position expressions that denote t on σ
L8  for each pair 0 ≤ i < j ≤ |o| do
L9      W(i, j) ← {ConstStr(o[i .. j))}
L10     for each a with σ[a .. a + j - i) = o[i .. j) do
L11         add the rectangle SubStr(P(a), P(a + j - i)) to W(i, j)
L12 return W
```

**The DAG of one example (lines L8 to L12).** The nodes are the indices $0, \ldots, |o|$ of the output, and there is an edge from $i$ to $j$ for each $i < j$. Its label $W(i, j)$ holds every atom that gives $o[i .. j)$ on $\sigma$. The constant is always there. For each place $a$ where the piece occurs in the input, line L11 adds the set of atoms SubStr$(p_1, p_2)$ with $p_1 \in P(a)$ and $p_2 \in P(a + j - i)$. This set is stored as a pair of sets, a *rectangle*, so a label with $s$ choices on each side holds $s^2$ atoms in $2s$ entries. A path from $0$ to $|o|$, with one atom on each edge, is a program that gives $o$.

**Intersection (lines L3 to L6).** The states of the product are tuples of indices, one for each example. An edge of the product moves every component forward, and its label is the intersection of the labels. Two rectangles meet in the rectangle of the pairwise intersections. Only states that can be reached from the start are built.

**Ranking (lines L6 and L7).** Every edge raises the sum of the components, so this order is topological, and one pass of dynamic programming finds a cheapest path, as in [shortest paths in a DAG](/dag-shortest-paths/). The cheapest atom of a rectangle takes the cheapest position from each set.

Gulwani's full algorithm also learns conditionals: it groups the examples so that each group has a non-empty intersection, and it learns a Boolean classifier that picks the group from the input. It also has a loop construct for repeated patterns. Neither is in the pseudocode above.

## Example

Take $\sigma_1$ = "Alan Turing" and $o_1$ = "A. Turing". The DAG has the 10 nodes $0, \ldots, 9$ and the 45 edges $i < j$. Some labels:

| edge | piece | constant | rectangles | atoms |
|---|---|---|---|---|
| $(0, 1)$ | "A" | "A" | SubStr$(\{$CPos$(0)$, CPos$(-12)$, Pos$(\varepsilon, L, 1)$, Pos$(\varepsilon, L, -2)\}, \{$CPos$(1)$, CPos$(-11)\})$ | 9 |
| $(1, 3)$ | ". " | ". " | none, since "." is not in the input | 1 |
| $(1, 2)$ | "." | "." | none | 1 |
| $(2, 9)$ | " Turing" | " Turing" | one rectangle, from index 4 to index 11, with 8 and 4 positions | 33 |
| $(3, 9)$ | "Turing" | "Turing" | one rectangle, from index 5 to index 11, with 8 and 4 positions | 33 |

The index 4 is the space. Eight expressions denote it: CPos$(4)$, CPos$(-8)$, Pos$(L, \varepsilon, 1)$ and Pos$(L, \varepsilon, -2)$ (the first of the two places where a run of letters ends), Pos$(\varepsilon, S, \pm 1)$ and Pos$(L, S, \pm 1)$. The index 1 is inside the run "Alan", so only CPos names it.

The 45 labels together hold 5,389 programs with at most 3 atoms, and 514,150,720 programs in all. The cheapest has cost $(1, 3, 7)$:

Concat(SubStr(CPos(0), CPos(1)), ConstStr("."), SubStr(Pos($\varepsilon$, S, $-1$), CPos($-1$)))

It uses one constant character, because the space of ". " can be copied as the first character of " Turing". On "Grace Hopper" it gives "G. Hopper".

**A second example.** Add "Grace Hopper" $\mapsto$ "G. Hopper". The product of the two DAGs has 17 reachable states and 83 edges. On the edge from $(2, 2)$ to $(9, 9)$ the rectangles meet in SubStr with 7 start positions and 3 end positions. CPos$(4)$ drops out, because the space is at index 4 in the first input and at index 5 in the second. CPos$(-8)$ stays, because both last names have 6 letters. At the end, CPos$(11)$ drops out and CPos$(-1)$ stays. Of the programs with at most 3 atoms, 126 remain, and 775,656 programs remain in all. The cheapest program is the same as above.

**What the examples do not decide.** The program that uses Pos$(\varepsilon, S, 1)$, the first space, also fits both examples and has the same cost. On "Mary Ann Evans" the chosen program gives "M. Evans", and the other gives "M. Ann Evans". Only a third example, or a better ranking, can decide which one the user wants.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Every atom gives a non-empty string, so a program that gives $o$ cuts $o$ into pieces at unique indices, and each atom is in the label of its piece. So the programs that give $o_j$ are exactly the paths of the $j$-th DAG with an atom from each label. A program fits all examples exactly when its index tuples form a path in the product whose labels hold its atoms, and the intersection of rectangles is exact. The cost is a sum of atom costs under a lexicographic order, which is compatible with addition, so dynamic programming in topological order returns a cheapest consistent program, and "none" exactly when no program fits.

## Complexity

Let $n$ be the length of the longest input, $m$ that of the longest output, $k$ the number of examples, and $p$ the number of position expressions that denote one index (at most 2 CPos and 90 Pos here).

- **One example.** There are $O(m^2)$ edges. For each edge, line L10 compares the piece with $O(n)$ places in $O(m)$ time each, and each match adds a rectangle of two sets of size at most $p$. So the time is $O(m^2 n (m + p))$ and the space $O(m^2 n p)$, after computing $P(t)$ for all $t$ once.
- **Several examples.** The product has at most $(m + 1)^k$ states and $(m + 1)^{2k}$ edges, and a label can have $n^k$ rectangles. So the worst case is exponential in $k$. In practice the labels shrink fast and most states are not reachable: in the example above, the product has 17 states, not $10^2 = 100$.
- **The number of programs.** A DAG of size polynomial in $m$ and $n$ holds a number of programs exponential in $m$, as the counts above show.

A unit step is one comparison of characters or one operation on a hash set.

## Properties

- **Complete for the language.** If any program of the language fits the examples, the algorithm finds one. This holds for this language without conditionals; the full FlashFill algorithm may need to split the examples into groups.
- **Exact optimum.** The result is a cheapest program for the stated cost. The cost does not ensure that it is the intended program.
- **All programs at once.** The product DAG holds every consistent program. A tool can count them, show several, or find an input on which two of them disagree.
- **Deterministic.** Ties in cost are broken by a fixed order on atoms.

## Variants and improvements

- **Conditionals.** FlashFill partitions the examples into classes with a non-empty DAG intersection, and learns a Boolean condition over the inputs for each class.
- **Loops.** A Loop construct concatenates the outputs of an expression for the values $1, 2, \ldots$ of a counter until it fails, for outputs such as all initials of a name.
- **Several inputs.** SubStr takes an input column as an argument.
- **Semantic transformations.** Later work adds lookup tables and the parsing of numbers and dates.
- **FlashMeta.** Polozov and Gulwani (2015) build such structures for any domain-specific language from witness functions, which give, for an operator and a wanted output, the outputs that its arguments must have.
- **Learned ranking.** Singh and Gulwani (2015) learn the weights of the ranking from tasks with known programs.

## When to use it

Use it for string tasks in a language of concatenations, constants and substrings, when the user gives one to a few examples and the inputs share a layout. It is fast for short strings, and it keeps all consistent programs, so a tool can ask the user about inputs where they disagree. For numeric functions or deeper expressions, use [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/) or a solver; for a general grammar, a [version space algebra](/version-space-algebra/) with witness functions.

## Pitfalls

- **One example is rarely enough.** One example usually fits thousands of programs, and the best by cost can still be wrong on other rows, as the "Mary Ann Evans" case shows. Show the result on all rows.
- **Constants that look like copies.** "A. Turing" with the constant "A. " works on one row and fails on all others. The cost must make constants expensive.
- **Empty pieces.** If an atom could give the empty string, the DAG would need edges from a node to itself, and the cut of the output into pieces would not be unique. The language here forbids empty substrings.
- **Products grow with the number of examples.** Intersect the DAGs one after the other, and drop states that cannot reach the goal.
- **Positions by index.** CPos$(4)$ fits one row and fails when the first name has another length. Prefer token positions in the ranking.
- **Tokens.** Two strings with the same characters but different runs, such as "ab1" and "a b1", have different token positions. The choice of tokens is part of the language.

## Implementations

## History

Gulwani (2011) presented the language, the DAG of one example, the intersection of DAGs, the learning of conditionals and the ranking at POPL 2011. The method shipped as Flash Fill in Microsoft Excel 2013. Singh and Gulwani (2015) replaced the hand-made ranking by a learned one. Polozov and Gulwani (2015) made the method general in FlashMeta, which builds version space algebras for any domain-specific language with witness functions, and which they used for FlashFill and for other tasks such as text extraction.

## References
