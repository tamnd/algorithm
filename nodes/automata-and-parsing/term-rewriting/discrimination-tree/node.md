---
tag: R1941B
kind: data-structure
slug: discrimination-tree
name: Discrimination tree
aliases:
- discrimination net
- term discrimination tree
- term index
area: automata-and-parsing/term-rewriting
level: advanced
summary: A trie over preorder term symbols that retrieves candidate rewrite rules for a term.
solves: [term-matching]
model: word-ram
complexity:
  vars: {n: the size of the query term, m: the size of the inserted or deleted pattern, P: the number of nodes of the tree, k: the number of candidates, N: the total size of the stored patterns}
  time: {worst: O(n + P + k n), best: Θ(n)}
  space: {extra: O(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, term-matching, rewrite-rule, preorder-traversal]
see_also: [term-indexing, substitution-tree, hoffmann-odonnell-matching, ac-matching, tree-pattern-matching, knuth-bendix-completion, e-matching, superposition]
sources:
  - paper: doi:10.1007/BF00245458
    title: William McCune, Experiments with discrimination-tree indexing and path indexing for term retrieval, Journal of Automated Reasoning 9(2) (1992)
    locator: pp. 147 to 167 (discrimination trees and path indexing in the Otter prover, retrieval of generalizations, instances and unifiable terms, measured on real proof runs)
  - paper: doi:10.1007/BF00881866
    title: Jim Christian, Flatterms, discrimination nets, and fast term rewriting, Journal of Automated Reasoning 10(1) (1993)
    locator: pp. 95 to 113 (terms stored as flat preorder arrays with skip pointers, and discrimination nets to find the rules for a rewrite step)
  - book: isbn:9783540610403
    title: Peter Graf, Term Indexing, Lecture Notes in Computer Science 1053, Springer, 1996
    locator: the chapters Set-based indexing and Tree-based indexing, pp. 51 to 199 (a survey of indexing techniques for automated reasoning, with a comparison in the next chapter)
---

A **discrimination tree** is a [trie](/trie/) that stores terms by their preorder sequence of symbols, with every variable written as the same symbol $*$. It is a [term index](/term-indexing/): given a query term $t$, it returns the stored patterns that may match $t$, without trying each pattern in turn. A rewriting engine stores the left sides of its [rewrite rules](/rewrite-rule/) in one, and at each subterm it asks for the rules whose left side matches. Retrieval follows the symbols of $t$ and, at a $*$ edge, skips the whole subterm of $t$ at that point. Because $*$ forgets which variables are equal, the answer for a non-linear pattern such as $f(x, x)$ is only a candidate, and a [matcher](/term-matching/) checks it.

## In plain words

Write each pattern as a line of symbols, read from left to right as you would read it aloud, and put a star where the pattern has a variable. Store all these lines in a trie, so patterns that start the same way share the first part of the path.

To find the patterns that fit a term, read the term in the same way and walk down the trie. At each node there are two ways to go on. If the next symbol of the term has its own branch, follow it. If there is a star branch, follow it too, and jump over the whole part of the term that the star stands for. Each path that reaches the end of the term at the end of a stored line gives a pattern that fits. Patterns that start with a wrong symbol are never looked at.

## The abstract type

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, $\to^*$ for the reflexive transitive closure, positions as sequences of positive integers, and substitutions $\sigma$. A pattern $l$ **matches** a term $t$ if $l\sigma = t$ for some $\sigma$; this is [term matching](/term-matching/), and the variables of $t$ are treated as constants. For a pattern $l$, $lin(l)$ is $l$ with each variable occurrence replaced by a new variable, all distinct; $l$ is linear iff $lin(l)$ equals $l$ up to renaming.

The structure stores a multiset of entries $(l, v)$, a pattern with a value, for example the left side of a rule and the index of the rule. It has these operations.

- `insert(D, l, v)` adds the entry.
- `delete(D, l, v)` removes one copy of the entry, if there is one.
- `retrieve(D, t)` returns the entries with $lin(l)$ matching $t$: a superset of the entries whose pattern matches $t$, and equal to it when all patterns are linear.
- `match(D, t)` returns the entries whose pattern matches $t$, each with its matcher.

This is retrieval of **generalizations** of $t$. A term index may also offer retrieval of instances and of unifiable terms (see Variants).

## Representation

For a pattern $l$, $key(l)$ is the preorder sequence of its symbols, with a function symbol $f$ of arity $k$ written $f/k$ and every variable written $*$. For example $key(f(g(x), y)) = f/2\ g/1\ *\ *$. The arity is part of the symbol, so $f(a)$ and $f(a, b)$ have different keys. A preorder sequence with arities is a prefix code for terms: it fixes the term, and no key is a proper prefix of another key. The only loss is the names of the variables, so $key(f(x, x)) = key(f(x, y))$.

Each node $x$ has a map $x.next$ from symbols to children and a list $x.vals$ of entries. For a node $x$, $str(x)$ is the sequence of symbols on the path from the root to $x$.

**Invariant.**

- **(D1) Entries.** An entry $(l, v)$ is stored if and only if it is in $x.vals$ for the node $x$ with $str(x) = key(l)$.
- **(D2) No dead branch.** Each node other than the root has an entry or a child.
- **(D3) Count.** $D.n$ is the number of entries.

The query is flattened in the same order. Its symbols are $a_0, \ldots, a_{n-1}$, where a variable $y$ of the query becomes a symbol $?y$ that no key contains. Each $a_i$ starts a subterm $t_i$, and $skip[i]$ is the index just after the end of $t_i$. Christian (1993) calls this array form a flatterm. The skip array is computed from right to left: if $a_i = f/k$, the children of $t_i$ start at $i + 1$ and follow one another, so $skip[i]$ is found by $k$ jumps.

## Operations

```pseudo id=main
DT-INSERT(D, l, v)
L1  x ← D.root
L2  for each symbol c of key(l), in order do
L3      if x.next[c] = NIL then x.next[c] ← a new node with no entries and no children
L4      x ← x.next[c]
L5  append (l, v) to x.vals; D.n ← D.n + 1

DT-RETRIEVE(D, t)
L6  (a_0, …, a_{n−1}), skip ← the flattened t
L7  out ← empty list; stack ← [(D.root, 0)]
L8  while stack is not empty do
L9      (x, i) ← pop(stack)
L10     if i = n then append the entries of x.vals to out; continue
L11     if x.next[*] ≠ NIL then push (x.next[*], skip[i])            ▷ * stands for t_i
L12     if a_i is a function symbol and x.next[a_i] ≠ NIL then push (x.next[a_i], i + 1)
L13 return out

DT-MATCH(D, t)
L14 out ← empty list
L15 for each (l, v) in DT-RETRIEVE(D, t) do
L16     σ ← MATCH(l, t); if σ ≠ FAIL then append (v, σ) to out
L17 return out

DT-DELETE(D, l, v)
L18 (c_1, …, c_m) ← key(l); path ← [D.root]; x ← D.root
L19 for j ← 1 to m do
L20     x ← x.next[c_j]; if x = NIL then return false; append x to path
L21 if (l, v) is not in x.vals then return false; remove one copy; D.n ← D.n − 1
L22 for j ← m down to 1 do                                ▷ path[j] is the node of c_1 … c_j
L23     if path[j] has an entry or a child then return true
L24     remove the link path[j − 1].next[c_j]
L25 return true
```

**Insert.** Lines L1 to L4 walk the key and create the missing nodes, as in a trie. Line L5 stores the entry at the end of the key.

**Retrieve.** The stack holds pairs $(x, i)$: the node $x$ has consumed the query up to index $i$. Line L11 lets a variable of a pattern take the whole subterm $t_i$ in one step, by a jump to $skip[i]$. Line L12 follows a function symbol of the query; a query variable is consumed only by line L11. A pair with $i = n$ has consumed the whole query, and its entries are the answers (line L10). The order of the pushes makes the search try the symbol edge before the $*$ edge.

**Match.** Line L16 runs a full [term matching](/term-matching/) on each candidate. It removes the candidates whose repeated variables take different subterms.

**Delete.** Lines L18 to L20 walk the key. Line L21 removes the entry. Lines L22 to L24 prune the nodes that are left with no entry and no child, from the bottom up, as in a trie.

## Example

Store five patterns, with the values 1 to 5.

| value | pattern | key |
|---|---|---|
| 1 | $f(g(x), y)$ | $f\ g\ *\ *$ |
| 2 | $f(g(a), b)$ | $f\ g\ a\ b$ |
| 3 | $f(x, x)$ | $f\ *\ *$ |
| 4 | $g(x)$ | $g\ *$ |
| 5 | $f(x, b)$ | $f\ *\ b$ |

The tree has 12 nodes, the root included. The value of an entry is shown after the symbol of its node.

```
(root)
├── f
│   ├── g
│   │   ├── *
│   │   │   └── * 1
│   │   └── a
│   │       └── b 2
│   └── *
│       ├── * 3
│       └── b 5
└── g
    └── * 4
```

Retrieve with the query $t = f(g(a), b)$. Its flattened form is $f\ g\ a\ b$ with $skip = [4, 3, 3, 4]$, so $n = 4$: the subterm $g(a)$ that starts at index 1 ends before index 3. The stack is shown with its top on the right, and a node is named by its path.

| step | pop $(x, i)$ | action | stack after |
|---|---|---|---|
| 1 | (root, 0) | $a_0 = f$: push (f, 1) | (f, 1) |
| 2 | (f, 1) | push (f\*, $skip[1] = 3$), then (fg, 2) | (f\*, 3), (fg, 2) |
| 3 | (fg, 2) | push (fg\*, 3), then (fga, 3) | (f\*, 3), (fg\*, 3), (fga, 3) |
| 4 | (fga, 3) | $a_3 = b$: push (fgab, 4) | (f\*, 3), (fg\*, 3), (fgab, 4) |
| 5 | (fgab, 4) | $i = n$: output entry 2 | (f\*, 3), (fg\*, 3) |
| 6 | (fg\*, 3) | push (fg\*\*, 4) | (f\*, 3), (fg\*\*, 4) |
| 7 | (fg\*\*, 4) | output entry 1 | (f\*, 3) |
| 8 | (f\*, 3) | push (f\*\*, 4), then (f\*b, 4) | (f\*\*, 4), (f\*b, 4) |
| 9 | (f\*b, 4) | output entry 5 | (f\*\*, 4) |
| 10 | (f\*\*, 4) | output entry 3 | empty |

The candidates are 2, 1, 5 and 3. The tree never visits the node $g$ of pattern 4, because the query starts with $f$. DT-MATCH then checks each candidate: pattern 1 matches with $x \mapsto a$ and $y \mapsto b$, pattern 2 matches with the empty substitution, pattern 5 matches with $x \mapsto g(a)$, and pattern 3 fails, because $f(x, x)$ needs $g(a) = b$. So the matches are 1, 2 and 5.

With the query $f(g(b), g(b))$ the candidates are 1 and 3, and both match, pattern 3 with $x \mapsto g(b)$. Pattern 5 fails in the tree: after $*$ skips $g(b)$, the next symbol is $g$, not $b$. After `delete(D, f(g(a), b), 2)` the nodes fga and fgab are pruned, and 10 nodes remain.

## Correctness

Insert and delete keep (D1) to (D3), by the same argument as for a [trie](/trie/). For retrieval, define the walk of a key from index $i$: a function symbol must equal $a_i$ and moves to $i + 1$, and $*$ moves to $skip[i]$. By induction on the size of a sequence of patterns, the walk of $key(l_1) \cdots key(l_m)$ from $i$ succeeds iff $lin(l_1), \ldots, lin(l_m)$ match consecutive subterms of $t$ that start at $i$; the matchers combine because the variables of the linear forms are disjoint. The search pops $(x, i)$ iff the walk of $str(x)$ from 0 ends at $i$, and each node at most once, because the walk is deterministic. So line L10 outputs the entry $(l, v)$ iff $lin(l)$ matches $t$, exactly once. Since $l$ matching $t$ implies $lin(l)$ matching $t$, DT-MATCH returns exactly the entries whose pattern matches. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/) with hash maps for the children, so they are expected times. Let $n = |t|$, let $m = |l|$, let $P$ be the number of nodes, $k$ the number of candidates, and $N$ the total size of the stored patterns.

| operation | time |
|---|---|
| insert, delete | $\Theta(m)$ |
| flatten the query and compute skip | $\Theta(n)$ |
| retrieve | $O(n + V + k)$, where $V \le P$ is the number of nodes visited |
| match | the retrieve cost plus $O(n)$ for each candidate |
| space | at most $N + 1$ nodes and one list item for each entry |

**Retrieve.** Each node is popped at most once (by the correctness proof), and each pop does $O(1)$ work besides the output at line L10. The walk of a popped node consumes at least one symbol of $t$ for each edge, so only nodes of depth at most $n$ are visited. The bound $V \le P$ is reached when the query has many variables or the patterns have many stars: a query variable at the root can only take $*$ edges, but a pattern $*$ at the root accepts every query.

**Match.** The matcher of line L16 visits only positions of $l$ that are also positions of $t$, and the equality tests for repeated variables compare subterms of $t$ at disjoint positions, so one call costs $O(n)$. With linear patterns the check always succeeds, and it can be skipped.

**Space.** By (D1) and (D2), the nodes other than the root correspond one to one to the distinct nonempty prefixes of the stored keys, so there are at most $N + 1$ nodes, and patterns with a common beginning share nodes.

**Compared with a list.** Trying each of $r$ patterns in turn costs $\Theta(r)$ matcher calls for each query. A discrimination tree pays nothing for a pattern whose first symbol differs from the query, and the shared prefixes are compared one time for all the patterns below them.

## Variants

- **Perfect discrimination trees.** Number the variables of a pattern by first occurrence, $*_1, *_2, \ldots$, and record in the search which subterm each one took. A repeated variable then checks equality during the walk, and every result is a match, with its matcher. The imperfect tree on this page needs the check of line L16.
- **Retrieval of instances.** Find the stored terms that are instances of a query pattern, as forward subsumption and backward demodulation need. A variable of the query skips a whole stored subterm, so the tree must know where each stored subterm ends, for example through jump links or a count of the open arguments.
- **Retrieval of unifiable terms.** Both sides may have variables, and both kinds of skips are used. The result is again a set of candidates, which [unification](/most-general-unifier/) checks.
- **Other term indexes.** Path indexing stores each path from the root to a leaf of a term, and answers queries by set intersections. The [substitution tree](/substitution-tree/) shares common substitutions instead of common prefixes. Hoffmann and O'Donnell compile all patterns into one tree automaton, the [Hoffmann-O'Donnell matcher](/hoffmann-odonnell-matching/), that finds every match in one pass. The [term indexing](/term-indexing/) page compares them.
- **Modulo theories.** For associative and commutative symbols the key of a flattened argument multiset has no fixed order, and indexes are extended for [AC matching](/ac-matching/).

## When to use it

Use a discrimination tree when the same set of patterns is matched against many terms, and the patterns differ near their roots: the left sides of the rules of a rewriting engine, the demodulators of an equational prover, or the facts of a rule system. With a few patterns, try them one after the other, because the tree costs a flatten for each query. Use a perfect tree when many patterns are non-linear and the candidate check dominates. When the set of patterns does not change, a compiled matcher such as the [Hoffmann-O'Donnell matcher](/hoffmann-odonnell-matching/) can be faster.

## Pitfalls

- **Forgetting the arity.** If the key symbol is only the name $f$ and $f$ is used with one and with two arguments, then $f(f(a, b))$ and $f(f(a), b)$ both have the key $f\ f\ a\ b$, and preorder no longer fixes the term. Use $f/k$, or a signature with one arity for each name.
- **Trusting candidates for non-linear patterns.** $f(x, x)$ is retrieved for $f(a, b)$. Without the check of line L16 a rewriting engine would apply the rule where it does not match.
- **Query variables.** A variable of the query must not follow an edge with the same name, because pattern variables and query variables are unrelated. Here a query variable is a symbol $?y$ that no key contains, so only $*$ edges consume it.
- **Recursion depth.** Terms in rewriting can be very deep, for example numbers in unary notation. A recursive flatten or match overflows the Python stack. The implementation uses explicit stacks, and the skip array is computed by a loop from right to left.
- **Skip by search.** Finding the end of $t_i$ by scanning and counting arities costs $O(|t_i|)$ for each $*$ edge. Precompute the skip array once for each query.

## Implementations

## History

Discrimination nets come from artificial intelligence programming, where they indexed facts and patterns for retrieval in rule-based systems. In automated reasoning, McCune (1992) built discrimination-tree indexing and path indexing into the Otter prover, and measured both on retrieval of generalizations, instances and unifiable terms. Christian (1993) combined flat preorder arrays with skip pointers, which he called flatterms, with discrimination nets to make rewriting fast in a completion procedure. Graf's book (1996) surveys these and other term indexes, such as substitution trees. Many current equational provers and rewriting engines use variants of discrimination trees to find the rules for a rewrite step.

## References
