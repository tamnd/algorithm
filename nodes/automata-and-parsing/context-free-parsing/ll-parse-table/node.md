---
tag: 3BZN2A
kind: data-structure
slug: ll-parse-table
name: LL parse table
aliases:
- predictive parse table
area: automata-and-parsing/context-free-parsing
level: core
summary: Table mapping a nonterminal and lookahead token to a production for LL(1) parsing.
model: word-ram
complexity:
  vars: {v: the number of nonterminals, σ: the number of terminals plus one for the end marker, g: the size of the grammar}
  time: {build: O(v σ^2 g), lookup: O(1)}
  space: {total: Θ(v σ)}
history:
  year: 1968
  people: [Philip M. Lewis II, Richard E. Stearns]
  note: Lewis and Stearns defined the grammars that a deterministic top-down parser with k symbols of lookahead can handle; the one-token table is the case k = 1.
prereqs: [context-free-grammar, nullable-symbol, first-and-follow-sets, leftmost-derivation]
see_also: [ll1-parsing, ll-grammar, ll-k-parsing, left-factoring, left-recursion-elimination, lr-parse-table, panic-mode-error-recovery, recursive-descent-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.2, FIRST and FOLLOW; Section 4.4.3, LL(1) Grammars (the construction of a predictive parsing table); Section 4.4.4, Nonrecursive Predictive Parsing
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.2, Predictive Parsing (FIRST and FOLLOW sets, constructing a predictive parser)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (Section 8.2, LL(1) parsing, with the FIRST and FOLLOW sets and the parse table)
  - paper: doi:10.1145/321466.321477
    title: P. M. Lewis II and R. E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3) (1968)
    locator: pp. 465 to 488 (the definition of LL(k) grammars)
---

An LL parse table is a two-dimensional table $M$ that tells a deterministic top-down parser which production to apply: the row is the nonterminal $A$ on top of the parser's stack, the column is the next input token $a$, and the cell $M[A, a]$ holds the production $A \to \alpha$ to expand $A$ with. It is built from the [nullable symbols](/nullable-symbol/) and the [FIRST and FOLLOW sets](/first-and-follow-sets/) of the grammar. A grammar is an [LL(1) grammar](/ll-grammar/) exactly when no cell gets two productions, and then the [LL(1) parser](/ll1-parsing/) runs in linear time with one table lookup per expansion.

## In plain words

A top-down parser holds a list of grammar symbols that it still has to match against the input. When the first symbol of that list is a placeholder, it must pick one of the placeholder's rules. The table makes this choice ahead of time.

For each placeholder and each possible next word of the input, the table names the rule that can start with that word. A rule can start with a word if the rule produces text that begins with it. A rule that can produce nothing is also chosen when the next word is one that may come after the placeholder. If two rules compete for the same box, the grammar needs more lookahead or a rewrite; if a box is empty, the input has an error at that point.

## The abstract type

The table is a finite map from pairs $(A, a)$, with $A$ a nonterminal and $a$ a terminal or the end marker $\$$, to sets of productions of $A$. It supports two operations:

- BUILD$(G)$ makes the table of a grammar $G$;
- LOOKUP$(M, A, a)$ returns the production in the cell $M[A, a]$, or *error* when the cell is empty, and reports a conflict when it has two or more productions.

The table is a static map: after BUILD it never changes. Parsers that use it are the [LL(1) parser](/ll1-parsing/), and with [panic-mode error recovery](/panic-mode-error-recovery/) the empty cells become recovery points.

## Representation

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The end marker $\$ \notin V \cup \Sigma$ stands for the end of the input.

The three sets that the table is made from are:

- $\mathrm{Null} = \{ A \in V : A \Rightarrow^* \varepsilon \}$; a string $\alpha$ is nullable when all its symbols are in $\mathrm{Null}$;
- $\mathrm{FIRST}(\alpha) = \{ a \in \Sigma : \alpha \Rightarrow^* a \beta \text{ for some } \beta \}$, for a string $\alpha$ of grammar symbols;
- $\mathrm{FOLLOW}(A) = \{ a \in \Sigma \cup \{\$\} : S\$ \Rightarrow^* \beta A a \gamma \text{ for some } \beta, \gamma \}$.

The cells are an array of $|V| \times (|\Sigma| + 1)$ entries, or a hash map from the pair $(A, a)$ to a list of production numbers. Each cell keeps this invariant:

> **(T)** $M[A, a]$ holds exactly the productions $A \to \alpha$ with $a \in \mathrm{PREDICT}(A \to \alpha)$, where $\mathrm{PREDICT}(A \to \alpha) = \mathrm{FIRST}(\alpha)$ if $\alpha$ is not nullable, and $\mathrm{FIRST}(\alpha) \cup \mathrm{FOLLOW}(A)$ if it is.

The set $\mathrm{PREDICT}(A \to \alpha)$ is the set of tokens that can be the next input when the parser expands $A$ by $A \to \alpha$ in a successful parse. A cell with two productions is a *conflict*; an empty cell is an *error entry*.

## Operations

```pseudo id=main
BUILD(G)                                   ▷ G = (V, Σ, R, S)
L1  compute Null, FIRST(A) and FOLLOW(A) for each A ∈ V
L2  M ← a table with rows V and columns Σ ∪ {$}, all cells empty
L3  for each production p = A → α in R do
L4      for each a ∈ FIRST(α) do add p to M[A, a]
L5      if α is nullable then
L6          for each b ∈ FOLLOW(A) do add p to M[A, b]

LOOKUP(M, A, a)
L7  C ← M[A, a]
L8  if C is empty then return error
L9  if |C| ≥ 2 then report a conflict between the productions of C
L10 return the production in C
```

Line L1 runs three fixed-point computations, each a loop over the productions until no set grows:

```pseudo id=sets
SETS(G)
L1  Null ← ∅; repeat: add A to Null if A → X1 ⋯ Xk with every Xi ∈ Null; until no change
L2  FIRST(A) ← ∅ for each A
L3  repeat: for each A → X1 ⋯ Xk and each i such that X1 ⋯ X(i−1) is nullable,
L4          add FIRST(Xi) to FIRST(A)          ▷ FIRST(a) = {a} for a terminal a
L5  until no change
L6  FOLLOW(S) ← {$}; FOLLOW(A) ← ∅ for each other A
L7  repeat: for each B → α A β,
L8          add FIRST(β) to FOLLOW(A); if β is nullable, add FOLLOW(B) to FOLLOW(A)
L9  until no change
```

FIRST of a string $X_1 \cdots X_k$ is the union of $\mathrm{FIRST}(X_i)$ over the $i$ such that $X_1 \cdots X_{i-1}$ is nullable. BUILD then puts each production in the column of each token of its PREDICT set (lines L3 to L6). LOOKUP is one access to the map (line L7); a parser that calls it with an empty cell reports a syntax error, and a cell with two productions means that BUILD found that the grammar is not LL(1).

## Example

Take the expression grammar without left recursion, with its productions numbered:

$$\begin{array}{llll} 0: E \to T E' & 1: E' \to + T E' & 2: E' \to \varepsilon & 3: T \to F T' \\ 4: T' \to * F T' & 5: T' \to \varepsilon & 6: F \to ( E ) & 7: F \to id \end{array}$$

Line L1 gives $\mathrm{Null} = \{E', T'\}$ and these sets:

| symbol | FIRST | FOLLOW |
|---|---|---|
| $E$ | ( id | ) \$ |
| $E'$ | + | ) \$ |
| $T$ | ( id | + ) \$ |
| $T'$ | * | + ) \$ |
| $F$ | ( id | + * ) \$ |

Lines L3 to L6 fill the table. Productions 2 and 5 have nullable right sides, so they go into the columns of $\mathrm{FOLLOW}(E')$ and $\mathrm{FOLLOW}(T')$:

| | id | + | * | ( | ) | \$ |
|---|---|---|---|---|---|---|
| $E$ | 0 | | | 0 | | |
| $E'$ | | 1 | | | 2 | 2 |
| $T$ | 3 | | | 3 | | |
| $T'$ | | 5 | 4 | | 5 | 5 |
| $F$ | 7 | | | 6 | | |

No cell has two productions, so the grammar is LL(1). LOOKUP$(M, T', +)$ returns production 5, $T' \to \varepsilon$: after a term, a plus sign ends the term. LOOKUP$(M, E, +)$ returns error, because an expression cannot start with a plus sign.

**A conflict.** For the dangling else, $S \to i \, S \, E \mid x$ and $E \to e \, S \mid \varepsilon$, the set $\mathrm{FOLLOW}(E) = \{e, \$\}$ contains $e$, because an inner statement can be followed by the $e$ of an outer one. Line L4 puts $E \to e \, S$ in $M[E, e]$ and line L6 puts $E \to \varepsilon$ there too. The cell $M[E, e]$ has two productions, and the grammar is not LL(1). Parsers usually keep $E \to e S$ in that cell, which attaches each else to the nearest if.

## Correctness

The correctness claim is that BUILD computes $\mathrm{Null}$, FIRST and FOLLOW exactly as defined, when every nonterminal is reachable from $S$, and so fills every cell as invariant (T) says; LOOKUP then returns the content of the cell. For an unreachable nonterminal $A$ the computed $\mathrm{FOLLOW}(A)$ can be too large, but a parser never uses row $A$. Each set is the least fixed point of its rules: every element that a rule adds has a derivation that proves it (soundness, by induction on the passes), and every element with a derivation is added (completeness, by induction on the length of a leftmost derivation for FIRST and on the length of a derivation for FOLLOW). The loops stop because each pass that changes something adds at least one element to a finite set. The full proof is below.

## Complexity

Let $v = |V|$, $\sigma = |\Sigma| + 1$ and $g = |G|$.

- **BUILD.** The $\mathrm{Null}$ loop makes at most $v + 1$ passes of $O(g)$ time. The FIRST loop makes at most $v \sigma + 1$ passes, because each pass that changes something adds one of at most $v(\sigma - 1)$ pairs $(A, a)$; a pass handles each symbol occurrence once with a set union of $O(\sigma)$ time, so a pass costs $O(g \sigma)$. The FOLLOW loop has the same bounds. So line L1 takes $O(v \sigma^2 g)$ time in the worst case, and lines L3 to L6 take $O(g \sigma)$. With bit vectors and $\sigma$ at most the word size, a union is $O(1)$ word operations and the bound drops by a factor $\sigma$.
- **LOOKUP.** One array access, or one hash lookup in expected $O(1)$ time on the [word RAM](/word-ram/).
- **Space.** The table has $v \sigma$ cells, so $\Theta(v \sigma)$ space; the sets take $O(v \sigma)$ more.

| operation | time | case |
|---|---|---|
| build | $O(v \sigma^2 g)$ | worst |
| lookup | $O(1)$ | worst with an array, expected with a hash map |
| space | $\Theta(v \sigma)$ | total |

## Variants

- **Faster FIRST and FOLLOW.** FIRST and FOLLOW are reachability questions on a graph with one node for each nonterminal and one edge for each rule of lines L3 and L7 of SETS. All nonterminals of one strongly connected component get the same set, so one pass over the components in topological order computes the sets in $O(g \sigma)$ time.
- **LL(k) tables.** With $k$ tokens of lookahead the columns are strings of up to $k$ tokens. For $k \ge 2$ one row per nonterminal is not enough in general: a full [LL(k) parser](/ll-k-parsing/) uses one table for each pair of a nonterminal and a set of possible right contexts.
- **Default entries.** An error entry in a row whose productions include one with a nullable right side can be filled with that production. The parser then finds some errors one step later, but the table has fewer distinct entries and compresses better.
- **Recursive descent.** A [recursive descent parser](/recursive-descent-parsing/) stores the same table in its code: the function for $A$ switches on the next token, with one case for each nonempty cell of row $A$.
- **Compression.** Rows of LL tables are sparse. The same comb and row-displacement methods that compress an [LR parse table](/lr-parse-table/) apply.

## When to use it

Use an LL(1) table when the grammar is LL(1) or can be made LL(1) by [left factoring](/left-factoring/) and [left recursion elimination](/left-recursion-elimination/), and when you want a small table and clear error messages: each empty cell names the tokens that were expected. For grammars that are not LL(1), use an [LR parse table](/lr-parse-table/), which accepts all LR(1) grammars and so all LL(1) grammars, or a parser with more lookahead such as [LL(*) parsing](/ll-star-parsing/).

## Pitfalls

- **Forgetting the FOLLOW columns.** If lines L5 and L6 are left out, a production $A \to \varepsilon$ never enters the table, and a parser rejects every input in which $A$ derives the empty string. In the example, productions 2 and 5 vanish from rows $E'$ and $T'$, and the parser rejects the input $id$.
- **Testing the first symbol only.** FIRST$(X_1 X_2 \cdots)$ must continue past $X_1$ when $X_1$ is nullable. With $A \to B c$ and $B \to \varepsilon$, the token $c$ is in FIRST$(Bc)$.
- **No end marker.** Put $\$$ in FOLLOW$(S)$ at line L6 of SETS. Without it, no nullable production gets a column for the end of the input, and the parser cannot finish when the input ends inside a nullable suffix.
- **Overwriting a cell.** An implementation that stores one production per cell and lets a later one overwrite an earlier one hides conflicts. Keep a list, or check the cell before writing.
- **Unproductive symbols.** FIRST and FOLLOW are defined on sentential forms. A production that uses a symbol which derives no terminal string still gets cells, and these can cause conflicts that disappear after [useless symbol elimination](/useless-symbol-elimination/).

## Implementations

## History

Lewis and Stearns (1968) defined the grammars that a deterministic top-down parser with $k$ symbols of lookahead can handle, and Rosenkrantz and Stearns (1970) studied their properties. The table form with FIRST and FOLLOW sets, filled by the rules of lines L3 to L6, is the presentation of the compiler textbooks, for example Aho, Lam, Sethi and Ullman, and Appel.

## References
