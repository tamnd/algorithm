---
tag: 86960D
kind: data-structure
slug: shared-packed-parse-forest
name: Shared packed parse forest
aliases:
- SPPF
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Compact representation of all parse trees of a string, sharing subtrees.
model: word-ram
complexity:
  vars: {n: the number of input tokens, g: the grammar size, t: the number of nodes of one parse tree}
  time: {build: O(g n^3), count: O(g n^3), extract: O(g n^3 + t n), contains: O(t n)}
  space: {total: O(g n^3)}
history:
  year: 1986
  people: [Masaru Tomita, Sylvie Billot, Bernard Lang, Elizabeth Scott]
  note: Tomita's generalized LR parser built a forest with subtree sharing and local ambiguity packing; Billot and Lang showed in 1989 that a forest is a grammar of cubic size when the productions are binary, and Scott's binarized SPPF of 2008 reaches that bound for every grammar.
prereqs: [parse-tree, ambiguity, parse-chart]
see_also: [glr-parsing, earley-parser, gll-parsing, graph-structured-stack, chart-parsing, inside-outside-algorithm, hash-consing, inherent-ambiguity]
sources:
  - book: isbn:9780898382020
    title: Masaru Tomita, Efficient Parsing for Natural Language, A Fast Algorithm for Practical Systems, Kluwer Academic Publishers, 1986
    locator: the chapters on subtree sharing and local ambiguity packing in the parse forest
  - url: https://aclanthology.org/P89-1018/
    title: Sylvie Billot and Bernard Lang, The structure of shared forests in ambiguous parsing, 27th Annual Meeting of the Association for Computational Linguistics (1989)
    locator: pp. 143 to 151 (a forest as a grammar; cubic size for binary productions)
  - paper: doi:10.1016/j.entcs.2008.03.044
    title: Elizabeth Scott, SPPF-style parsing from Earley recognisers, Electronic Notes in Theoretical Computer Science 203(2) (2008)
    locator: pp. 53 to 67 (binarized SPPFs with symbol, intermediate and packed nodes)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 3.7, parse forests and parse-forest grammars; Chapter 18, the annotations on Billot and Lang and on Nederhof's generalized left-corner parsing
---

A shared packed parse forest (SPPF) holds all parse trees of one string under an ambiguous [context-free grammar](/context-free-grammar/) in a single graph. Two ideas make it small. *Sharing*: a subtree that occurs in many trees, such as one reading of "the man with the telescope", is stored once and pointed to. *Packing*: when one nonterminal derives the same piece of the input in several ways, the alternatives hang as *packed nodes* below one node instead of being copied into separate trees. A string with exponentially many trees, or infinitely many when the grammar has cycles, gets a forest of $O(|G| n^3)$ nodes in the *binarized* form described here, in which long right sides are split into binary steps. The forest is the usual output of general parsers, such as the [Earley parser](/earley-parser/), [GLR parsing](/glr-parsing/) and [GLL parsing](/gll-parsing/), and later passes count, rank, filter or score the trees directly on it.

## In plain words

An ambiguous sentence has many readings, and their number can grow very quickly with its length. Most readings agree on most of the sentence and differ only in a few places. Writing each reading as a separate tree repeats the common parts again and again.

The forest stores each piece of a reading only once. A node says "this phrase covers these words", and every tree that needs that phrase points to the same node. When the same phrase over the same words can be built in two ways, the node gets two small alternative boxes underneath, one for each way. Choosing one box at every node you visit, starting from the top, spells out one complete tree. So the forest holds all trees in a space that grows only polynomially with the length of the sentence, and many questions can be answered on it without listing the trees.

## The abstract type

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The grammar is $G = (V, \Sigma, R, S)$, the input is $w = a_1 \cdots a_n$, and $w[i:j] = a_{i+1} \cdots a_j$ for $0 \le i \le j \le n$, so positions lie between tokens. A [parse tree](/parse-tree/) of $w$ has root $S$ and yield $w$.

A forest for $w$ is a directed graph with three kinds of nodes:

- a **symbol node** $(X, i, j)$, for a symbol $X$ with $X \Rightarrow^* w[i:j]$;
- an **intermediate node** $(A \to \alpha \cdot \beta, i, j)$, labeled with an [LR item](/lr-item/) with $|\alpha| \ge 2$, for $\alpha \Rightarrow^* w[i:j]$;
- a **packed node**, the child of a symbol or intermediate node, labeled with a production and a split position $k$, with at most two children: a left child that covers $w[i:k]$ and a right child that covers $w[k:j]$.

Each nonterminal symbol node and each intermediate node has one packed node for every way it can be built, and one tree is obtained by choosing a packed node at each node reached from the root $(S, 0, n)$. The type supports:

- BUILD$(G, w)$: the forest of all parse trees of $w$, or the empty forest if $w \notin L(G)$;
- COUNT: the number of parse trees, which is 0, a positive integer, or $\infty$;
- IS-AMBIGUOUS: whether $w$ has at least two parse trees;
- TREE$(r)$: the parse tree of rank $r$, for $0 \le r <$ COUNT, in a fixed order;
- ONE-TREE: some parse tree, also when there are infinitely many;
- CONTAINS$(t)$: whether $t$ is a parse tree of $w$.

## Representation

- **Hash-consed nodes.** Every symbol and intermediate node is identified by its key, $(X, i, j)$ or $(A \to \alpha \cdot \beta, i, j)$, and lives in a hash table from keys to the list of its packed nodes. Asking for a node with a known key returns the existing node, as in [hash-consing](/hash-consing/); this is what makes subtrees shared.
- **Packed nodes** are records (production, $k$, left, right), where left and right are node keys or absent. A packed node for an $\varepsilon$-production has no children, and one for the first symbol of a right side has a right child only.
- **Binarization.** A packed node of $(A, i, j)$ for $A \to x_1 \cdots x_m$ with $m \ge 2$ has the right child $(x_m, k, j)$ and as left child the intermediate node $(A \to x_1 \cdots x_{m-1} \cdot x_m, i, k)$, which in turn splits off $x_{m-1}$, and so on; for $m = 2$ the left child is the symbol node $(x_1, i, k)$. This chain of binary steps is the difference with Tomita's original forest, where a packed node had all $m$ children, and it is what keeps the size cubic.
- **Terminal nodes** $(a, j - 1, j)$ are leaves with no packed nodes.

## Operations

BUILD first runs a recognizer that fills a [parse chart](/parse-chart/), here a bottom-up agenda over the facts $(X, i, j) \in D$, meaning $X \Rightarrow^* w[i:j]$, and $(A \to \alpha \cdot \beta, i, j) \in P$, meaning $\alpha \Rightarrow^* w[i:j]$. Then it builds the forest top-down from the root, creating only the nodes that occur in some parse tree of $w$. NODE$(key)$ returns the node with that key, and when the key is new it creates the node and pushes it on the stack $Q$.

```pseudo id=main
BUILD-SPPF(G, w)
L1  compute the chart sets D and P of G on w
L2  if (S, 0, n) ∉ D then return the empty forest
L3  root ← NODE((S, 0, n))                          ▷ NODE pushes every new node on Q
L4  while Q is not empty do pop u from Q
L5      if u = (A, i, j) with A a nonterminal then for each A → α with (A → α ·, i, j) ∈ P do EXPAND(u, A → α ·, i, j)
L6      else if u = (A → α · β, i, j) is an intermediate node then EXPAND(u, A → α · β, i, j)

EXPAND(u, A → x_1 ⋯ x_m · β, i, j)
L7  if m = 0 then add to u a packed node (A → β, i) with no children; return
L8  if m = 1 then add to u a packed node (A → x_1 β, i) with right child NODE((x_1, i, j)); return
L9  for k ← i to j do
L10     if (A → x_1 ⋯ x_{m−1} · x_m β, i, k) ∈ P and (x_m, k, j) ∈ D then
L11         add to u a packed node (A → x_1 ⋯ x_m β, k) with right child NODE((x_m, k, j)) and left child NODE((x_1, i, k)) if m = 2, else NODE((A → x_1 ⋯ x_{m−1} · x_m β, i, k))
```

Line L5 calls EXPAND with the complete item of each production of $A$ that derives $w[i:j]$, and EXPAND splits off the last symbol before the dot. Line L7 is the packed node of an $\varepsilon$-production, and line L8 the first symbol of a right side, which has no left part. Line L11 is the binary step: the left child covers the shorter prefix, and the intermediate node it names is expanded later, when it is popped at line L4.

The queries walk the finished forest with explicit stacks:

- **COUNT.** A depth-first search looks for a cycle; if there is one, the count is $\infty$. Otherwise, in postorder, $c(a) = 1$ for a terminal node and $c(u) = \sum c(\ell) \cdot c(r)$ over the packed nodes of $u$ with children $\ell$ and $r$ (an absent child counts as 1). The answer is $c(\mathrm{root})$.
- **IS-AMBIGUOUS.** True when the forest has a cycle or some node reachable from the root has two or more packed nodes.
- **TREE$(r)$.** At a node with rank $r$, walk its packed nodes and subtract $c(\ell) c(r')$ from $r$ until the rank falls inside one; then the left child gets rank $\lfloor r / c(r') \rfloor$ and the right child $r \bmod c(r')$. Collect the right children along the chain of intermediate nodes to get the children of the tree node.
- **ONE-TREE.** Mark every terminal node. Mark a node, and remember the packed node, as soon as one of its packed nodes has all its children marked. Then build the tree from the root using the remembered packed nodes. This works on cyclic forests too: the remembered choices never loop.
- **CONTAINS$(t)$.** Compute the span of every node of $t$, and check that each internal node of $t$ with production $p$ and children boundaries $b_0, \ldots, b_m$ matches a symbol node and the chain of packed nodes $(p, b_{m-1}), (p, b_{m-2}), \ldots$ below it.

## Example

Take the ambiguous grammar $E \to E + E \mid \mathrm{id}$ and the input $\mathrm{id} + \mathrm{id} + \mathrm{id}$, so $n = 5$. Write $E_{ij}$ for the symbol node $(E, i, j)$ and $I_{ij}$ for the intermediate node $(E \to E + \cdot E, i, j)$. BUILD-SPPF creates these nodes and packed nodes (a packed node is written as split : left, right):

| node | packed nodes |
| --- | --- |
| $E_{05}$ | $2 : I_{02}, E_{25}$ and $4 : I_{04}, E_{45}$ |
| $E_{25}$ | $4 : I_{24}, E_{45}$ |
| $E_{03}$ | $2 : I_{02}, E_{23}$ |
| $I_{02}$ | $1 : E_{01}, (+, 1, 2)$ |
| $I_{04}$ | $3 : E_{03}, (+, 3, 4)$ |
| $I_{24}$ | $3 : E_{23}, (+, 3, 4)$ |
| $E_{01}, E_{23}, E_{45}$ | one packed node each, for $E \to \mathrm{id}$, with right child $(\mathrm{id}, 0, 1)$, $(\mathrm{id}, 2, 3)$, $(\mathrm{id}, 4, 5)$ |

The root has two packed nodes: split 2 gives $E_{01} + E_{25}$, the reading $\mathrm{id} + (\mathrm{id} + \mathrm{id})$, and split 4 gives $E_{03} + E_{45}$, the reading $(\mathrm{id} + \mathrm{id}) + \mathrm{id}$. The two trees share $E_{45}$, $E_{23}$, $E_{01}$ and also the intermediate node $I_{02}$, which stands for the common prefix "$E_{01}$ +". The forest has 11 symbol nodes (6 for $E$ and 5 for tokens), 3 intermediate nodes and 10 packed nodes, against 20 nodes for the two trees written out. COUNT gives $c(E_{25}) = c(E_{03}) = 1$ and $c(E_{05}) = 1 + 1 = 2$. The tests rebuild this table and both trees.

The saving grows quickly. For $S \to S S \mid a$ on $a^n$, the number of trees is the Catalan number $C_{n-1}$, while the forest grows like $n^3 / 6$:

| $n$ | parse trees | symbol nodes | packed nodes |
| --- | --- | --- | --- |
| 5 | 14 | 20 | 25 |
| 10 | 4862 | 65 | 175 |
| 15 | 2674440 | 135 | 575 |
| 20 | 1767263190 | 230 | 1350 |

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Define the trees *represented* at a node as those obtained by choosing a packed node at every node below it. Every node that BUILD creates satisfies its fact, because NODE is called only on facts checked in $D$ or $P$, so every represented tree is a parse tree (soundness). Conversely, for a parse tree $t$ with top production $A \to x_1 \cdots x_m$ and children boundaries $b_0, \ldots, b_m$, the expansion of $(A, b_0, b_m)$ adds the packed node with split $b_{m-1}$, which creates the intermediate node for the shorter prefix, and so on down the chain; induction on the height of $t$ shows that $t$ is represented at the root (completeness). The production and the boundaries of $t$ force the packed node chosen at every node, so each tree has exactly one choice of packed nodes, and COUNT counts trees, not choices. Each node is created once, because NODE looks keys up first, and expanded once, when it is popped, so BUILD stops. A cycle in the forest means some nonterminal derives itself over the same piece of input, and pumping it gives infinitely many trees.

## Complexity

Let $g = |G|$. There are at most $(|V| + |\Sigma|)(n + 1)^2$ symbol nodes and at most $g (n + 1)^2$ intermediate nodes, since an item has fewer than $g$ choices. Each of them has at most $n + 1$ packed nodes, one per split, so the forest has $O(g n^3)$ packed nodes and edges in total. The grammar $S \to S S \mid a$ shows that this is tight in $n$: on $a^n$ it has exactly $n + (n - 1) n (n + 1) / 6$ packed nodes.

BUILD costs $O(g n^3)$: the chart has $O(g n^2)$ facts, each combined with $O(n)$ partners, and the expansion of each node runs the loop over $k$ once. COUNT and IS-AMBIGUOUS are linear in the size of the forest, but the counts themselves can have $\Theta(n)$ digits, so COUNT uses $O(g n^3)$ big-number operations. TREE$(r)$ and ONE-TREE need $O(g n^3)$ for the counts or marks and then $O(t n)$ for a tree of $t$ nodes, since each packed node list has at most $n + 1$ entries; CONTAINS needs $O(t n)$. The space is $O(g n^3)$.

Without binarization, a packed node for a production with $p$ right-side symbols records $p - 1$ split points, and Tomita's forest can have $\Theta(n^{p+1})$ nodes and edges for a fixed grammar. Converting the grammar to binary productions first, as Billot and Lang observed, or binarizing inside the forest, as here, brings this down to cubic size.

## Variants

- **Tomita's forest.** Packed nodes have all $m$ children of the production, with no intermediate nodes. It is easier to read but can be of size $\Theta(n^{p+1})$, where $p$ is the length of the longest right side.
- **The forest as a grammar.** Billot and Lang read each node as a nonterminal of a new grammar that generates exactly $w$, and whose derivations are the parse trees of $w$. Intersection with other grammars and with regular languages then becomes a grammar operation.
- **Forests from GLR, Earley and GLL.** The RNGLR and BRNGLR algorithms of Scott and Johnstone build Tomita-style and binarized forests during GLR parsing, Scott built binarized forests directly from Earley sets in 2008, and GLL parsers produce the same binarized forest. Each parser gives a forest of the same shape for the same grammar; what differs is the order of construction and which nodes are created speculatively.
- **Packed forests with weights.** Attaching rule probabilities to packed nodes turns COUNT into the inside computation: replace the sum of products of counts by the sum (inside probability) or the maximum (Viterbi) of products of probabilities. This is how the [inside-outside algorithm](/inside-outside-algorithm/) and [most probable parse](/most-probable-parse/) search work on general grammars, and the same scheme gives semiring parsing.
- **Disambiguation filters.** Priority, associativity and reject rules, as in SDF and similar tools, remove packed nodes from the forest after or during parsing.

## When to use it

Use an SPPF when a general parser must return all parses of an ambiguous input, for example in natural-language parsing, in parsing of languages such as C++ whose grammar is ambiguous before type information is available, in grammar engineering where ambiguity must be detected and reported, and when later passes (types, probabilities, semantic filters) choose among the readings. When the grammar is deterministic, such as LR(1) or LL(1), there is only one tree and an ordinary [parse tree](/parse-tree/) is enough. When only the best tree is wanted under a probabilistic grammar, the Viterbi chart with back pointers is simpler than building the whole forest.

## Pitfalls

- **Exponential unpacking.** Listing all trees costs time proportional to their number, which can be exponential or infinite. Work on the forest (counts, inside sums, filters) instead, or unrank only the trees you need.
- **Cycles.** A grammar with $A \Rightarrow^+ A$, such as $S \to S \mid a$, or with $S \to S S \mid \varepsilon$ on the empty input, gives a forest with a cycle and infinitely many trees. Naive recursive traversal does not terminate; detect cycles first, and use a well-founded choice like ONE-TREE to extract a tree.
- **Missing binarization.** Packing at the level of whole productions gives $\Theta(n^{p+1})$ size for right sides of length $p$; a grammar with a few long rules can make the forest larger than the chart.
- **Spurious nodes.** A forest read directly off a recognizer's chart can contain nodes that occur in no parse tree of $w$, such as an $NP$ found inside a span that no sentence uses. Building top-down from the root, as BUILD-SPPF does, or pruning unreachable nodes afterwards, keeps only useful nodes.
- **Packed nodes are not unique per production.** Two packed nodes of the same node can have the same production and different splits; the key of a packed node is the pair (production, split), not the production alone, or trees are lost.
- **Deep trees.** A tree for a right-recursive grammar can be as deep as $n$; recursive traversal in a language with a small call stack fails on long inputs. The implementation uses explicit stacks throughout.

## Implementations

## History

Tomita built a parse forest during his generalized LR parsing of natural language (1985, and the 1986 book), with two devices he called subtree sharing and local ambiguity packing; the result became known as the shared packed forest. Billot and Lang (1989) showed that such a forest is itself a context-free grammar and that its size is $O(n^3)$ when the productions have at most two symbols on the right, while Nederhof's work on generalized left-corner parsing (1993) used a similar packing to bring Tomita's $O(n^{p+1})$ bound down to $O(n^3)$. Rekers' GLR algorithm (1991, 1992) gave a widely used formulation with separate packed nodes for the parser generators of the ASF+SDF environment. Scott and Johnstone made the binarized SPPF, with symbol, intermediate and packed nodes, the standard output of their RNGLR, BRNGLR and GLL parsers, and Scott (2008) showed how to build it from an Earley recognizer in cubic time and space.

## References
