---
tag: 37Y8RW
kind: data-structure
slug: parse-chart
name: Parse chart
aliases:
- chart
area: automata-and-parsing/context-free-parsing
level: core
summary: Table indexed by input span that stores recognized partial parses in chart parsers.
model: word-ram
complexity:
  vars: {n: the number of input tokens, g: the grammar size}
  time: {add: O(1) expected, lookup: O(1) expected, fill: O(g^2 n^3)}
  space: {total: O(g n^2)}
history:
  year: 1970
  people: [Jay Earley, Martin Kay]
  note: Earley's parser kept one set of dotted items per input position; Kay's chart parsing of the 1970s stated the table of edges over spans, the agenda and the fundamental rule as a general framework.
prereqs: [parse-tree, context-free-grammar, lr-item]
see_also: [chart-parsing, earley-parser, cyk-algorithm, shared-packed-parse-forest, glr-parsing, memoization, valiant-algorithm, hash-table]
sources:
  - paper: doi:10.1145/362007.362035
    title: Jay Earley, An efficient context-free parsing algorithm, Communications of the ACM 13(2) (1970)
    locator: pp. 94 to 102
  - paper: doi:10.1016/0743-1066(95)00035-I
    title: Stuart M. Shieber, Yves Schabes and Fernando C. N. Pereira, Principles and implementation of deductive parsing, Journal of Logic Programming 24(1-2) (1995)
    locator: pp. 3 to 36 (items, the chart and the agenda; the CYK and Earley deduction systems)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Section 7.2, The Earley Parser; Section 7.3, Chart Parsing
---

A parse chart is the table in which a chart parser stores what it has found about the input: for each span $(i, j)$ of positions, the *edges*, grammar facts of the form "the start $\alpha$ of the right side of $A \to \alpha \beta$ derives tokens $i + 1$ to $j$". Each edge is stored once, however many ways it was found, which turns the exponential number of partial parse trees of an ambiguous grammar into a polynomial table. The [CYK algorithm](/cyk-algorithm/), the [Earley parser](/earley-parser/) and [chart parsing](/chart-parsing/) in general are all ways of filling this table.

## In plain words

A parser that tries every way to read a sentence would redo the same work many times: "the cat" is a noun phrase no matter what follows. A chart is the notebook in which it writes such findings down once. Each note says which piece of the input it is about, from one position to another, and what has been recognized there, either a whole phrase or the first part of one.

Before the parser adds a note, it checks whether the note is already there; if so, nothing happens. New notes are combined with old ones: a note "the first part of a sentence ends here" and a note "a verb phrase starts here" give "a whole sentence ends there". When no new note appears, the parser looks for a note saying that a sentence covers the whole input.

## The abstract type

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The input is $w = a_1 \cdots a_n$, and $w[i:j] = a_{i+1} \cdots a_j$ for $0 \le i \le j \le n$.

An *edge* is a triple $(i, j, A \to \alpha \cdot \beta)$ of two positions and a dotted production, an [LR item](/lr-item/). It is *complete* (passive) when $\beta = \varepsilon$ and *active* otherwise. The chart holds a set of edges, each with a backpointer that records one way it was built, and supports:

- ADD$(e, b)$: insert edge $e$ with backpointer $b$ if it is not present; report whether it was new;
- MEMBER$(e)$: is $e$ in the chart;
- WAITING$(j, X)$: the active edges $(i, j, A \to \alpha \cdot X \beta)$ that end at $j$ and need $X$ next;
- COMPLETE$(i, A)$: the complete edges $(i, k, A \to \gamma \cdot)$ for $A$ that start at $i$.

The intended meaning of an edge $(i, j, A \to \alpha \cdot \beta)$ is $\alpha \Rightarrow^* w[i:j]$. A chart parser adds edges by inference rules that keep this meaning, and keeps an *agenda* of edges that have been added but not yet combined with the others.

## Representation

- **A hash set of edges** with the backpointers, for ADD and MEMBER in $O(1)$ expected time.
- **Two indexes** for the fundamental rule: an array over positions $j$ of maps from symbols $X$ to the active edges ending at $j$ that need $X$, and an array over positions $i$ of maps from nonterminals $A$ to the complete edges for $A$ starting at $i$. ADD appends to one of them.
- **CYK form.** For a grammar in [Chomsky normal form](/chomsky-normal-form/), only complete edges are needed, and they can be stored as an $(n + 1) \times (n + 1)$ triangle of bit sets over $V$, the classic CYK table.
- **Earley form.** Earley stores $n + 1$ sets $E_0, \ldots, E_n$, where $E_j$ holds the items $(A \to \alpha \cdot \beta, i)$ of all edges ending at $j$. This is the same chart, grouped by the end position.

## Operations

```pseudo id=main
ADD(i, j, A → α·β, b)
L1  if the edge (i, j, A → α·β) is in the chart then return false
L2  store it with the backpointer b
L3  if β = Xβ' then append it to WAITING(j, X)
L4  else append it to COMPLETE(i, A); return true

FILL(w)                                        ▷ every ADD that returns true also pushes the edge on the agenda
L5  for each production S → γ do ADD(0, 0, S → ·γ, none)
L6  while the agenda is not empty do pop an edge (i, j, A → α·β)
L7      if β = Bβ' with B ∈ V then for each B → γ do ADD(j, j, B → ·γ, none)                ▷ predict
L8          for each (k, B → γ·) in COMPLETE(j, B) do ADD(i, k, A → αB·β', ⟨edge, child⟩)      ▷ fundamental rule
L9      else if β = aβ' and a = w[j + 1] then ADD(i, j + 1, A → αa·β', ⟨edge, a⟩)            ▷ scan
L10     else if β = ε then for each (h, C → μ·Aν) in WAITING(i, A) do ADD(h, j, C → μA·ν, ⟨that edge, edge⟩)

READ(w)
L11 if some complete edge (0, n, S → γ·) is in the chart then
L12     follow the backpointers from it to build a parse tree, else report an error
```

The fundamental rule is applied from both sides, at L8 when the active edge is taken from the agenda and at L10 when the complete one is. So every pair of an active edge and a complete edge that fit together is combined, whichever was found first. This is what makes empty productions safe: a complete edge $(i, i, B \to \cdot)$ found before an active edge that waits for $B$ at $i$ is still used.

## Example

For the ambiguous grammar $E \to E + E \mid id$ and the input $id + id + id$ ($n = 5$), FILL adds 21 edges over 12 spans:

| span | edges |
|---|---|
| (0, 0), (2, 2), (4, 4) | $E \to \cdot E + E$, $E \to \cdot id$ |
| (0, 1), (2, 3), (4, 5) | $E \to id \cdot$, $E \to E \cdot + E$ |
| (0, 2), (2, 4), (0, 4) | $E \to E + \cdot E$ |
| (0, 3), (2, 5), (0, 5) | $E \to E + E \cdot$, $E \to E \cdot + E$ |

The complete edge $(0, 5, E \to E + E \cdot)$ can be built in two ways: from $(0, 2, E \to E + \cdot E)$ with $(2, 5, E \to E + E \cdot)$, which is $id + (id + id)$, or from $(0, 4, E \to E + \cdot E)$ with $(4, 5, E \to id \cdot)$, which is $(id + id) + id$. The chart stores the edge once. With $k$ plus signs, the number of trees is the Catalan number $C_k$, which grows like $4^k$, but the number of edges grows only quadratically in $k$. Here the first backpointer gives the tree $id + (id + id)$; storing all backpointers instead of one turns the chart into a [shared packed parse forest](/shared-packed-parse-forest/).

## Correctness

Every edge in the chart is *sound*: $(i, j, A \to \alpha \cdot \beta)$ implies $\alpha \Rightarrow^* w[i:j]$, and moreover $S \Rightarrow^* w[0:i] A \delta$ for some $\delta$. Each rule keeps this: prediction adds empty $\alpha$, scan appends a matched token, and the fundamental rule appends a $B$ with $B \Rightarrow^* w[j:k]$. Conversely every edge with these two properties is added, by induction on the size of the derivation, because the fundamental rule is applied in both orders. In particular $w \in L(G)$ if and only if a complete edge $(0, n, S \to \gamma \cdot)$ is in the chart, and the backpointers of any edge point to edges added before it, so following them always ends and gives a parse tree. The full proof is below.

## Complexity

- **Size.** An edge is a dotted production and two positions, so there are at most $|G| (n + 1)^2$ edges, $O(|G| n^2)$ space with the backpointers and the indexes.
- **ADD and MEMBER** cost $O(1)$ expected time with hashing.
- **FILL.** Each edge is popped once. Prediction costs $O(|G|)$ per edge. The fundamental rule pairs an active edge ending at $j$ with the complete edges starting at $j$: at most $n + 1$ end positions, each with at most $|G|$ dotted items, so $O(|G| n)$ per edge, and the same from the side of a complete edge. In total FILL takes $O(|G|^2 n^3)$ time. Grouping the complete edges by $(i, A, k)$ instead of by item removes one factor $|G|$, which gives Earley's $O(|G| n^3)$ bound.
- **Better cases.** For an unambiguous grammar the chart holds $O(n^2)$ edges and FILL takes $O(n^2)$ time; for many grammars, such as left-recursive lists, it is linear. Right recursion makes the chart quadratic, which Leo's refinement of Earley's algorithm avoids.
- **READ** takes time linear in the size of the tree it returns.

## Variants

- **Bottom-up chart.** Without prediction, start with an edge $(j, j, A \to \cdot \gamma)$ for every production and every position. This gives all constituents anywhere in the input, useful for robust and partial parsing, at the cost of more edges.
- **CYK chart.** For a grammar in Chomsky normal form, only complete edges $(i, j, A)$ are stored, filled by span length; see the [CYK algorithm](/cyk-algorithm/).
- **Weighted chart.** Store with each edge the best weight or probability of a derivation, and replace "already present" by "found with a better weight"; this is the Viterbi chart of probabilistic parsing.
- **Agenda order.** Any order of the agenda gives the same final chart. A stack, a queue, or an order by end position, which gives Earley's left-to-right sets, all work; a priority order by weight gives best-first parsing.
- **Packed forest.** Keep every backpointer of an edge, not only the first, to represent all parse trees; see the [shared packed parse forest](/shared-packed-parse-forest/).
- **Matrix multiplication.** The complete edges of CYK can be filled with Boolean matrix products, which gives [Valiant's algorithm](/valiant-algorithm/) in subcubic time.

## When to use it

Use a parse chart when the grammar is ambiguous, not LR or LL, or changes often, as in natural language processing, grammar development and parsing of programming languages with GLR-like tools. For deterministic grammars, an [LR parse table](/lr-parse-table/) or [LL parse table](/ll-parse-table/) gives linear time with far less memory.

## Pitfalls

- **The empty-production bug.** Applying the fundamental rule only when a complete edge arrives misses complete edges $(i, i, B \to \cdot)$ that were added before the active edges that need them. Either combine in both directions, as here, or advance the dot over nullable symbols at prediction time.
- **Cycles in the backpointers.** With unit cycles like $S \to S$, an edge can be rebuilt from itself. Keeping only the first backpointer, which points to older edges, keeps the tree finite; a forest of all backpointers must be read with cycle checks.
- **Memory.** The chart is quadratic in the input for every grammar with right recursion, and cubic work is common for ambiguous grammars. For such grammars, a chart over an input of 100 000 tokens does not fit in memory.
- **Recursion when reading trees.** Trees of long inputs are deep; build them from the backpointers with an explicit stack.

## Implementations

## History

Earley (1970) gave the first general context-free parser in $O(n^3)$ time, $O(n^2)$ for unambiguous grammars, with one set of items per input position. Kay, in work on natural language parsing in the 1970s (published in 1980), described the chart as a table of active and inactive edges together with an agenda and the fundamental rule, so that top-down, bottom-up and mixed strategies are all orders of one procedure. Shieber, Schabes and Pereira (1995) recast these parsers as deduction systems over items, with the chart as the store of proved items.

## References
