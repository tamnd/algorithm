---
tag: EBSXCH
kind: abstract-type
slug: symbol-graph
name: Symbol graph
area: graphs/graph-representation
level: intro
summary: Graph whose vertices are named by strings, built with a symbol table that maps names to integer vertex indices.
prereqs: [graph, adjacency-list, dictionary]
see_also: [graph, labeled-graph, string-symbol-table, hash-table, dictionary, adjacency-list, trie, vertex]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the SymbolGraph API and its implementation with a symbol table, an inverted index array and a Graph, and the degrees-of-separation client
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), vertices numbered 1 to |V|; Chapter 11 (Hash tables)
  - book: isbn:9781118290279
    title: Michael T. Goodrich, Roberto Tamassia and Michael H. Goldwasser, Data Structures and Algorithms in Python, Wiley, 2013
    locator: Section 14.2 (Data structures for graphs), the adjacency map structure with vertex objects and hash maps
---

A symbol graph is a [graph](/graph/) whose [vertices](/vertex/) have outside names, such as city names, airport codes, user names or URLs, and that stores them as the integers $0, \ldots, n - 1$ inside. A symbol table maps each name to its integer, an array maps each integer back to its name, and an ordinary integer graph such as an [adjacency list](/adjacency-list/) holds the edges. So every algorithm written for integer vertices runs unchanged, and only the input and output pass through the names. The structure is the `SymbolGraph` of Sedgewick and Wayne, and it is how almost all real graph data, given as lines of text like "JFK ORD", is loaded.

## In plain words

Graph programs like to number the places $0, 1, 2$ and so on, because a number can be the position in a list. People like to call places by names, like "Paris" or "JFK". A symbol graph keeps both. It has a phone book that gives the number of each name, and a list that gives the name of each number.

When a new name appears in the data, it gets the next free number. When a program asks about "Paris", the phone book turns it into a number, the graph work is done with numbers, and the answer is turned back into names at the end.

## Operations

**The values.** A symbol graph is a triple $(S, \iota, G)$ of a finite set $S$ of names (keys from some key type $K$, usually strings), a bijection $\iota : S \to \{0, \ldots, n - 1\}$ with $n = |S|$, and a graph $G = (\{0, \ldots, n - 1\}, E)$, [directed](/directed-graph/) or [undirected](/undirected-graph/). The named graph it stands for is $(S, \{(a, b) : (\iota(a), \iota(b)) \in E\})$. The order of the indices is the order in which the names first appeared.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to H$ | the empty symbol graph, $n = 0$ |
| `add-vertex` | $\text{add-vertex}(H, a) \to (i, H)$ | if $a \in S$, returns $\iota(a)$; otherwise adds $a$ with $\iota(a) = n$, increments $n$, and returns it |
| `contains` | $\text{contains}(H, a) \to \text{bool}$ | true if and only if $a \in S$ |
| `index` | $\text{index}(H, a) \to i$ | $\iota(a)$, for $a \in S$ |
| `name` | $\text{name}(H, i) \to a$ | $\iota^{-1}(i)$, for $0 \le i < n$ |
| `add-edge` | $\text{add-edge}(H, a, b) \to H$ | adds the names $a$ and $b$ if new, then the edge $(\iota(a), \iota(b))$ to $G$ |
| `graph` | $\text{graph}(H) \to G$ | the integer graph, for any algorithm on the [graph](/graph/) type |

Neighbour queries go through `graph`: the neighbours of the name $a$ are $\text{name}(H, j)$ for each $j$ in $\text{neighbors}(G, \text{index}(H, a))$.

**Building from text.** The usual input is a file in which each line lists names separated by a delimiter. In the Sedgewick-Wayne form, each line "$a\ b_1\ b_2 \ldots$" adds the edges $ab_1, ab_2, \ldots$. Their implementation reads the file twice: once to build the symbol table and count $n$, and once to add the edges to a graph of the right size. With a growable adjacency list, one pass suffices.

### Example

Start with `new` and read the undirected lines "JFK ORD", "ORD DEN", "JFK ATL", "DEN JFK".

| step | operation | new names | $\iota$ after | edges of $G$ |
|---|---|---|---|---|
| 1 | add-edge JFK ORD | JFK, ORD | JFK 0, ORD 1 | $01$ |
| 2 | add-edge ORD DEN | DEN | DEN 2 | $01, 12$ |
| 3 | add-edge JFK ATL | ATL | ATL 3 | $01, 12, 03$ |
| 4 | add-edge DEN JFK | none | | $01, 12, 03, 20$ |
| 5 | index DEN | | returns 2 | |
| 6 | name 3 | | returns ATL | |
| 7 | contains LAX | | returns false | |

The adjacency lists of $G$ are $0: [1, 3, 2]$, $1: [0, 2]$, $2: [1, 0]$, $3: [0]$. A [breadth-first search](/breadth-first-search/) from $\text{index}(\text{ATL}) = 3$ gives the path $3, 0, 2$, which `name` prints as ATL, JFK, DEN.

## Laws

For each symbol graph $H$, names $a, b, x$ and index $i$:

$$\begin{aligned}
&(\text{S1})\quad \text{name}(H, \text{index}(H, a)) = a \text{ for } a \in S, \text{ and } \text{index}(H, \text{name}(H, i)) = i \text{ for } 0 \le i < n,\\
&(\text{S2})\quad \text{if } (i, H') = \text{add-vertex}(H, a) \text{ and } a \notin S, \text{ then } i = n \text{ and } \text{size}(H') = n + 1,\\
&(\text{S3})\quad \text{if } (i, H') = \text{add-vertex}(H, a) \text{ and } a \in S, \text{ then } i = \text{index}(H, a) \text{ and } H' = H,\\
&(\text{S4})\quad \text{indices never change: } \text{index}(H', x) = \text{index}(H, x) \text{ for each } x \in S \text{ after any operation},\\
&(\text{S5})\quad \text{if } H' = \text{add-edge}(H, a, b), \text{ then } \text{adjacent}(\text{graph}(H'), \text{index}(H', a), \text{index}(H', b)) = \text{true}.
\end{aligned}$$

Law (S1) says $\iota$ is a bijection and `name` is its inverse. Laws (S2) and (S3) make `add-vertex` idempotent, so reading the same name twice makes one vertex. Law (S4) is why the type has no `remove-vertex`: removing a name would either leave a hole in $\{0, \ldots, n - 1\}$ or change other indices, and arrays indexed by vertex in the client would break. Where removal is needed, mark the vertex deleted, or use vertex objects instead of indices.

## Implementations

Let $n$ be the number of names, $m$ the number of edges, $\ell$ the length of the name in a call, and $L$ the total length of all names. The integer graph is an adjacency list in each row.

| symbol table | space | index, contains | name | add-vertex | add-edge |
|---|---|---|---|---|---|
| [hash table](/hash-table/) | $\Theta(n + m + L)$ | $O(\ell)$ expected | $O(1)$ | $O(\ell)$ expected amortized | $O(\ell_a + \ell_b)$ expected amortized |
| balanced search tree, such as a [red-black tree](/red-black-tree/) | $\Theta(n + m + L)$ | $O(\ell \log n)$ | $O(1)$ | $O(\ell \log n)$ | $O((\ell_a + \ell_b)\log n)$ |
| [trie](/trie/) with an array of $\sigma$ children per node | $\Theta(n + m + L\sigma)$ | $O(\ell)$ | $O(1)$ | $O(\ell)$ amortized | $O(\ell_a + \ell_b)$ amortized |
| sorted array, static | $\Theta(n + m + L)$ | $O(\ell \log n)$ | $O(1)$ | rebuild | rebuild |

In each row `name` is a read of the array of names, which is a [dynamic array](/dynamic-array/) indexed by vertex. The cost of a string comparison is $O(\ell)$ in the worst case, which is the factor $\ell$ in the search-tree rows. The hash table is the default; a search tree or a trie is chosen when the names must be listed in sorted order or searched by prefix. A program that needs no integers can instead use an *adjacency map*, in which each vertex is an object and holds a hash map from neighbours to edges, as in Goodrich, Tamassia and Goldwasser; it gives up the array-indexed attributes that the integer form allows.

## Lower bounds

**Reading the name.** Each `index` or `contains` call on a name of length $\ell$ must read all $\ell$ characters in the worst case, since two names may differ only in the last one. So $\Omega(\ell)$ time per call. The hash table meets this bound in expectation, and the array trie meets it in the worst case, at the cost of $\sigma$ words per node for an alphabet of size $\sigma$. A [ternary search tree](/ternary-search-tree/) saves that space and adds a term for the comparisons at each character.

**Comparison-based tables.** If names can only be compared, a lookup among $n$ names needs $\lceil \lg(n + 1) \rceil$ comparisons in the worst case, by the [decision-tree](/decision-tree-model/) argument: there are $n + 1$ outcomes, each name or "absent". So a search tree pays $\Omega(\log n)$ comparisons per lookup, which hashing avoids.

**Space.** The structure must store the names, $\Theta(L)$ characters, plus the graph, $\Omega(n + m)$ words for the adjacency list. Both terms are needed: the names cannot be recovered from the graph, and the graph cannot be recovered from the names.

## References
