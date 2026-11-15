---
tag: 4T1SEM
kind: data-structure
slug: version-space-algebra
name: Version space algebra
aliases:
- version space
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: A shared DAG of union and join nodes that stores all programs consistent with some examples, often exponentially many in polynomial space, with intersection and counting.
model: word-ram
complexity:
  vars: {s: the size bound on programs, d: the largest number of distinct outputs of programs of one size on the example input, e: the number of nodes and edges of the larger operand}
  time: {build: O(s^2 d^2) expected, intersect: O(e^2) expected, count: O(e)}
  space: {build: O(s^2 d^2), intersect: O(e^2)}
history:
  year: 2000
  people: [Tessa Lau, Pedro Domingos, Daniel S. Weld]
  note: Mitchell described version spaces of hypotheses with boundary sets in 1982. Lau, Domingos and Weld built version spaces of programs from smaller ones by union and join in 2000, and Gulwani used them in FlashFill in 2011.
prereqs: [programming-by-example, directed-acyclic-graph, memoization]
see_also: [string-transformation-synthesis, bottom-up-enumerative-synthesis, shared-packed-parse-forest, e-graph, hash-consing, binary-decision-diagram]
sources:
  - paper: doi:10.1016/0004-3702(82)90040-6
    title: Tom M. Mitchell, Generalization as search, Artificial Intelligence 18(2), 1982
    locator: pp. 203-226, version spaces of consistent hypotheses, the boundary sets S and G, and the candidate elimination algorithm
  - paper: doi:10.1023/A:1025671410623
    title: Tessa Lau, Steven A. Wolfman, Pedro Domingos and Daniel S. Weld, Programming by demonstration using version space algebra, Machine Learning 53(1-2), 2003
    locator: pp. 111-156, the version space algebra with union and join of version spaces, and its use in the SMARTedit text editor
  - paper: "Tessa Lau, Pedro Domingos and Daniel S. Weld, Version space algebra and its application to programming by demonstration, Proceedings of the 17th International Conference on Machine Learning (ICML 2000), pp. 527-534"
    locator: the first description of composite version spaces
  - paper: doi:10.1145/1926385.1926423
    title: Sumit Gulwani, Automating string processing in spreadsheets using input-output examples, Principles of Programming Languages (POPL 2011)
    locator: pp. 317-330, the shared data structure for all consistent string programs and its intersection over several examples
  - paper: doi:10.1145/2814270.2814310
    title: Oleksandr Polozov and Sumit Gulwani, FlashMeta, a framework for inductive program synthesis, Object-Oriented Programming, Systems, Languages and Applications (OOPSLA 2015)
    locator: pp. 107-126, version space algebras with union and join nodes in general, intersection, ranking, and their construction by witness functions
---

A version space algebra (VSA) stores the set of all programs that agree with some examples, in a language given by a grammar. It is a shared graph with two kinds of inner nodes. A union node holds the programs of any of its kids, and a join node holds every program that applies one operator to a program from each kid. Because the kids are shared, a graph with a few hundred nodes can hold millions of programs. Synthesizers for [programming by example](/programming-by-example/) build one VSA for each example, intersect them, and then count, rank or list the programs. This page is about the data structure; [string transformation synthesis](/string-transformation-synthesis/) is one algorithm that uses it.

## In plain words

Suppose that the answer must be "something plus something". You do not need to write every full answer. You can write one box of choices for the left side and one box for the right side. Two boxes with ten choices each stand for a hundred answers.

A version space algebra does this again and again, at every level of the program. Boxes can be shared, so the same box of small programs is used in many places. The whole structure stays small while it stands for a huge number of programs.

When a second example arrives, the tool keeps only the programs that fit both examples. It does this box by box, and it never lists the programs one by one. At the end it can count the programs, pick the best one, or show a few of them.

## The abstract type

A version space $N$ stands for a finite set $R(N)$ of programs. The operations are:

- BUILD$(i, o, S)$: a version space for all programs of size at most $S$ whose output on the input $i$ is $o$.
- INTERSECT$(a, b)$: a version space for $R(a) \cap R(b)$.
- COUNT$(n)$: the number $|R(n)|$, without listing the programs.
- BEST$(n)$: a program of $R(n)$ with the best rank, for a rank that is computed from the ranks of the parts.
- LIST$(n)$: all programs of $R(n)$, one at a time.

With examples $(i_1, o_1), \ldots, (i_k, o_k)$, the set of consistent programs is
$$V = R(\mathrm{BUILD}(i_1, o_1, S)) \cap \cdots \cap R(\mathrm{BUILD}(i_k, o_k, S)).$$

## Representation

A VSA is a directed acyclic graph with three kinds of nodes:

- LEAF$(A)$, with $R = A$, a finite set of programs without parts, such as variables and constants.
- UNION$(k_1, \ldots, k_r)$, with $R = R(k_1) \cup \cdots \cup R(k_r)$.
- JOIN$(\mathit{op}, a, b)$, with $R = \{ \mathit{op}(p, q) : p \in R(a), q \in R(b) \}$. Operators with other arities have one kid for each argument.

EMPTY is the union with no kids. The constructors never build another node with an empty set: a join with an EMPTY kid is EMPTY, and a union drops EMPTY kids. A union with one kid is the kid itself.

A union is *disjoint* when its kids have pairwise disjoint sets. All unions built below are disjoint, and this makes COUNT exact.

The language on this page, and in the code, is
$$E \to x \mid y \mid 1 \mid 2 \mid E + E \mid E - E \mid E \times E$$
over pairs of integers $(x, y)$. The size of a program is the number of nodes of its tree, so it is odd. There are $4$, $48$, $1152$ and $34560$ programs of size $1$, $3$, $5$ and $7$.

## Operations

```pseudo id=main
BUILD(i, o, S)                        ▷ all programs of size at most S with output o on input i
L1  for each terminal t: add t to T[value of t on i]
L2  vals[1] ← the keys of T
L3  for s = 3, 5, …, S do
L4      for each split s1 + s2 = s - 1, a ∈ vals[s1], b ∈ vals[s2], op ∈ {+, -, ×} do
L5          append (op, s1, a, b) to how[s][op(a, b)]
L6      vals[s] ← the keys of how[s]
L7  return UNION(NODE(s, o) for each odd s ≤ S with o ∈ vals[s])

NODE(s, v)                            ▷ memoized: one node for each pair (s, v)
L8  if s = 1 then return LEAF(T[v])
L9  return UNION(JOIN(op, NODE(s1, a), NODE(s - 1 - s1, b)) for each (op, s1, a, b) in how[s][v])

INTERSECT(a, b)                       ▷ memoized on the pair of nodes
L10 if a = EMPTY or b = EMPTY then return EMPTY
L11 if a = UNION(k1, …, kr) then return UNION(INTERSECT(kj, b) for j = 1 … r)
L12 if b = UNION(k1, …, kr) then return UNION(INTERSECT(a, kj) for j = 1 … r)
L13 if a = LEAF(A) and b = LEAF(B) then return LEAF(A ∩ B)
L14 if a = JOIN(op, a1, a2) and b = JOIN(op, b1, b2) then return JOIN(op, INTERSECT(a1, b1), INTERSECT(a2, b2))
L15 return EMPTY                       ▷ a leaf and a join, or two joins with different operators

COUNT(n)                              ▷ memoized
L16 if n = LEAF(A) then return |A|
L17 if n = UNION(k1, …, kr) then return COUNT(k1) + … + COUNT(kr)
L18 if n = JOIN(op, a, b) then return COUNT(a) · COUNT(b)
```

**BUILD.** Lines L1 to L6 run forward over sizes. They compute, for each size, the set of outputs that programs of that size can have on the input $i$, and for each output, the ways to get it from two smaller outputs. This is dynamic programming over pairs (size, output), with [memoization](/memoization/) of the nodes. Line L9 makes one union for each pair, with one join for each way. The node NODE$(s, v)$ is made once and shared by every join that needs a program of size $s$ with output $v$. Line L7 joins the sizes up to $S$.

**INTERSECT.** Lines L11 and L12 push the intersection into the kids of a union. Line L14 is the key step: two joins with the same operator meet in a join of the pairwise intersections, because two trees with the same root are equal exactly when their subtrees are equal. The memo table makes each pair of nodes cost one call.

**COUNT, BEST and LIST.** COUNT adds over unions and multiplies over joins. BEST works the same way with the rule "best of the kids" at a union and "combine the best parts" at a join. This is exact when the rank of $\mathit{op}(p, q)$ grows with the ranks of $p$ and $q$, as size does. LIST walks the graph and yields the programs one by one.

**Other ways to build.** FlashFill and FlashMeta build the VSA top-down from the output. A *witness function* for an operator gives, from the wanted output, the outputs that its arguments must have, for example all ways to split a string into a prefix and a suffix for concatenation. This needs no forward table of values and works for infinite value domains, but it needs one witness function for each operator. The forward method above needs only the semantics.

## Example

Take the examples $(1, 2) \mapsto 3$, $(2, 1) \mapsto 3$ and $(0, 0) \mapsto 0$, and the size bound $S = 3$.

**The first example.** On $(x, y) = (1, 2)$, the terminals have the outputs $x = 1$, $y = 2$, $1 = 1$, $2 = 2$, so $T[1] = \{x, 1\}$ and $T[2] = \{y, 2\}$. No terminal has the output 3. Of size 3, the output 3 comes only from $1 + 2$ and $2 + 1$. So
$$V_1 = \mathrm{UNION}(\mathrm{JOIN}(+, \{x, 1\}, \{y, 2\}),\ \mathrm{JOIN}(+, \{y, 2\}, \{x, 1\})),$$
which holds $2 \cdot 2 + 2 \cdot 2 = 8$ programs with 5 nodes.

**The second example.** On $(2, 1)$, $T[1] = \{y, 1\}$ and $T[2] = \{x, 2\}$, and
$$V_2 = \mathrm{UNION}(\mathrm{JOIN}(+, \{y, 1\}, \{x, 2\}),\ \mathrm{JOIN}(+, \{x, 2\}, \{y, 1\})).$$

**The intersection.** Lines L11 and L12 give four pairs of joins. All have the operator $+$, so line L14 intersects the leaves:

| join of $V_1$ | join of $V_2$ | result |
|---|---|---|
| $\{x, 1\} + \{y, 2\}$ | $\{y, 1\} + \{x, 2\}$ | $1 + 2$ |
| $\{x, 1\} + \{y, 2\}$ | $\{x, 2\} + \{y, 1\}$ | $x + y$ |
| $\{y, 2\} + \{x, 1\}$ | $\{y, 1\} + \{x, 2\}$ | $y + x$ |
| $\{y, 2\} + \{x, 1\}$ | $\{x, 2\} + \{y, 1\}$ | $2 + 1$ |

COUNT gives 4. The third example has $T[0] = \{x, y\}$ and keeps only $x + y$ and $y + x$, because $1 + 2$ and $2 + 1$ output 3 on $(0, 0)$.

**Growth.** The code builds the VSA of the single example $(1, 2) \mapsto 3$ for larger bounds. The number of programs grows much faster than the graph:

| bound $S$ | programs | nodes | edges |
|---|---|---|---|
| 5 | 144 | 26 | 59 |
| 7 | 3,552 | 103 | 267 |
| 9 | 98,816 | 282 | 775 |
| 11 | 3,071,552 | 653 | 1,850 |
| 13 | 102,003,648 | 1,315 | 3,789 |

Here a leaf counts its programs as edges. With all three examples and $S = 9$, the intersection holds 7,284 programs in 1,098 nodes, and BEST returns $x + y$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By induction on the size, NODE$(s, v)$ holds exactly the programs of size $s$ with output $v$, and its unions are disjoint, because two ways to get $v$ differ in the operator, in the size of the left part or in the output of a part. INTERSECT is correct by induction on the two graphs, with line L14 as the main case, and it keeps unions disjoint. COUNT is then exact: the sum is right for disjoint unions, and the product is right because $(p, q) \mapsto \mathit{op}(p, q)$ is one to one. So the intersection of the BUILD results for all examples holds exactly the consistent programs up to the bound.

## Complexity

Let $s$ be the size bound, $d$ the largest number of different outputs of the programs of one size on the input, and $e$ the number of nodes and edges of a version space.

- **BUILD.** There is one node NODE$(s', v)$ for each odd size $s' \le s$ and each output $v$, so at most $\frac{s+1}{2} d$ union nodes. Each join comes from one split, one pair of outputs and one operator, so there are at most $3 \bigl(\frac{s+1}{2}\bigr)^2 d^2$ joins. With a hash table, the time is $O(s^2 d^2)$ expected.
- **INTERSECT.** Each pair of nodes is handled once. A pair with a union costs the number of kids, and a pair of joins costs a constant. The total is $O(e_a e_b)$, which is $O(e^2)$ for the larger operand. The result can have this many nodes, so intersecting $k$ examples one after the other can grow like a product. In practice most pairs are empty.
- **COUNT and BEST.** One pass over the graph, $O(e)$ arithmetic operations. The counts are big integers with $O(s)$ digits, because there are at most $c^s$ programs of size at most $s$ for some constant $c$.
- **Compactness.** A version space can hold exponentially more programs than it has nodes. A chain $J_k = \mathrm{JOIN}(+, L, J_{k-1})$ over the leaf $L = \{x, y\}$, with $J_0 = L$, holds $2^{k+1}$ programs with $k + 1$ nodes. The table above shows the same effect for a real example.

The bound on $d$ depends on the language. Here $d$ is at most the number of programs of one size, but it is far smaller in practice, because most outputs are reached in many ways. Over the integers, $d$ can grow quickly when multiplication is allowed. FlashFill keeps $d$ small because every value is a substring or a position of the given strings.

## Variants

- **Mitchell's version spaces.** The first version spaces were sets of hypotheses ordered from specific to general. Mitchell (1982) stores such a set by its two boundary sets: $S$, the most specific consistent hypotheses, and $G$, the most general ones. The *candidate elimination* algorithm updates $S$ and $G$ for each positive or negative example. This needs a partial order of generality on the hypotheses; a version space algebra needs none.
- **Composite version spaces.** Lau, Domingos and Weld (2000, 2003) build version spaces of programs from smaller version spaces by union and join, with a transform that maps the hypotheses of one space into another. They used them to learn text edits from demonstrations in SMARTedit.
- **FlashFill and FlashMeta.** Gulwani (2011) stores all consistent string programs in a graph of this kind and intersects the graphs of the examples. Polozov and Gulwani (2015) give the general form with union and join nodes and witness functions, for any domain-specific language.
- **Cycles.** Without a size bound, a recursive grammar can give infinite sets. A graph with cycles can represent them, as a [context-free grammar](/context-free-grammar/) does, but COUNT and LIST then need a bound.
- **Close structures.** A [shared packed parse forest](/shared-packed-parse-forest/) stores all parse trees of one string in the same way, with union nodes for the choices and packed nodes for the parts. An [e-graph](/e-graph/) stores classes of equal terms, not of terms with a fixed output. A [binary decision diagram](/binary-decision-diagram/) shares subgraphs to store a Boolean function.

## When to use it

Use a VSA when the language is a small domain-specific language, each operator can be inverted or the outputs of small programs can be listed, and the user wants all consistent programs, not just one. It is the right choice when the examples arrive one at a time, when the tool must rank many candidates, or when it must find an input on which two candidates disagree. For a single smallest program in a language with large or infinite value domains, [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/) is simpler.

## Pitfalls

- **Counting with overlapping unions.** COUNT adds over unions, so it counts a program twice if two kids hold it. Keep unions disjoint, as BUILD and INTERSECT do here, or count with another method.
- **Growth under intersection.** The intersection of two version spaces can have as many nodes as the product of their sizes. Drop EMPTY nodes at once, or the graph fills with dead parts.
- **Ranks that are not compositional.** BEST at a union takes the best kid, which is correct only when the rank of a program is computed from the ranks of its parts. A rank that looks at the whole program needs the programs listed.
- **Equal values are not equal programs.** Two programs with the same outputs on all examples are both kept. A VSA does not merge programs by behaviour; that is what observational equivalence does in [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/).
- **A size bound hides programs.** A program longer than the bound is not in the set, even if it is the intended one. The empty result means "none up to this bound", not "none".

## Implementations

## History

Mitchell (1982) defined the version space of a learning problem as the set of hypotheses that agree with all examples, and stored it by its boundary sets. Lau, Domingos and Weld (2000) turned version spaces into an algebra, so that a space of programs is built from spaces of smaller programs by union and join. Lau, Wolfman, Domingos and Weld (2003) give the full account and the SMARTedit editor. Gulwani (2011) used the same idea for FlashFill, which stores all consistent string programs and intersects them over the examples. Polozov and Gulwani (2015) stated version space algebras in general for any domain-specific language, built top-down by witness functions, in the FlashMeta framework.

## References
