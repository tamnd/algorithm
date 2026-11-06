---
tag: 8VPCRP
kind: problem
slug: tree-pattern-matching
name: Tree pattern matching
aliases:
- ordered tree pattern matching
- subtree matching
- term pattern matching
area: automata-and-parsing/term-rewriting
level: advanced
summary: Find all occurrences of a set of tree patterns in a subject tree.
model: word-ram
complexity:
  vars: {n: the number of nodes of the subject tree, m: the number of nodes of the pattern, h: the height of the pattern}
  time: {worst: O(n m^(1/2) polylog m)}
prereqs: [term-matching, subterm]
see_also: [hoffmann-odonnell-matching, discrimination-tree, substitution-tree, aho-corasick, string-matching, multiple-string-matching, normal-form-computation, term-graph-rewriting]
sources:
  - paper: doi:10.1145/322290.322295
    title: Christoph M. Hoffmann and Michael J. O'Donnell, Pattern matching in trees, Journal of the ACM 29(1) (1982)
    locator: pp. 68 to 95 (bottom-up matching with match sets and tables, and top-down matching by root-to-leaf path strings)
  - paper: doi:10.1109/SFCS.1989.63475
    title: S. Rao Kosaraju, Efficient tree pattern matching, 30th IEEE Symposium on Foundations of Computer Science (FOCS 1989)
    locator: pp. 178 to 183 (the first algorithm faster than O(n m), with time O(n m^0.75 polylog m))
  - paper: doi:10.1145/174652.174653
    title: Moshe Dubiner, Zvi Galil and Edith Magen, Faster tree pattern matching, Journal of the ACM 41(2) (1994)
    locator: pp. 205 to 213 (time O(n m^(1/2) polylog m), and the observation that the naive algorithm takes O(n h) time)
  - paper: doi:10.1145/258533.258553
    title: Richard Cole and Ramesh Hariharan, Tree pattern matching and subset matching in randomized O(n log^3 m) time, 29th ACM Symposium on Theory of Computing (STOC 1997)
    locator: pp. 66 to 75
  - paper: doi:10.1137/s0097539700382704
    title: Richard Cole and Ramesh Hariharan, Tree pattern matching to subset matching in linear time, SIAM Journal on Computing 32(4) (2003)
    locator: pp. 1056 to 1066
---

**Tree pattern matching** asks for every place in a subject tree where a pattern tree occurs, when a variable leaf of the pattern may stand for any subtree. It is [term matching](/term-matching/) done at all positions at once, for one pattern or for a set of patterns. It is the inner loop of every rewriting engine, which must find a redex before it can rewrite, and of compilers that select machine instructions by covering an expression tree with patterns. The naive method costs $O(n m)$ for a subject of $n$ nodes and a pattern of $m$ nodes; faster algorithms either preprocess a fixed set of patterns into tables, as Hoffmann and O'Donnell did, or reduce the problem to string problems.

## In plain words

Think of an expression as a tree: the operator at the top, its arguments below it. A pattern is a small tree with some holes, and a hole can be filled by any subtree. You want to find every node of a big tree where the pattern fits, with the holes covering whatever hangs below.

You could try the pattern at every node, which is slow when both trees are big. Better methods look at the pattern set once in advance and build tables, so that one pass over the big tree, from the leaves upwards, tells at each node which patterns fit there.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ for the subterm at position $p$, and substitutions $\sigma$. A pattern $l$ **matches** a term $s$ if $l\sigma = s$ for some substitution $\sigma$.

**Input.** A finite set of patterns $l_1, \ldots, l_k \in T(\Sigma, V)$ and a subject term $t \in T(\Sigma)$, usually ground.

**Output.** All pairs $(p, i)$ such that $l_i$ matches $t|_p$.

The patterns are usually **linear**: each variable occurs at most once. Then a variable is a wildcard, and whether $l$ matches $t|_p$ depends only on the symbols of $t$ at the positions of the function symbols of $l$. The output can have up to $n k$ pairs.

## Variants

- **One pattern or many.** One pattern $l$ of size $m$, or a fixed set of patterns that is preprocessed once and then matched against many subjects, as in a rewriting engine.
- **Non-linear patterns.** A repeated variable requires equal subtrees, as in $f(x, x)$. With a [term DAG](/term-dag/) or hashing, the equality test costs $O(1)$ per pair of subtrees after linear preprocessing.
- **Unordered trees, or patterns modulo theories.** Children are unordered, as in matching modulo commutativity, or sums are flattened, as in [AC-matching](/ac-matching/), which is NP-complete.
- **Indexing.** The subject changes and the patterns are many, or the reverse: [discrimination trees](/discrimination-tree/) and [substitution trees](/substitution-tree/) store many terms to retrieve those that match a query.
- **Matching during rewriting.** After a rewrite step only the nodes on the path to the root change, so incremental methods recompute match information along that path only.

## Examples

**Matches.** Take the patterns $l_1 = f(x, g(y))$ and $l_2 = g(a)$, and the subject $t = f(g(a), g(f(a, g(b))))$. A program that tries every pattern at every position finds the three matches $(\varepsilon, 1)$, $(1, 2)$ and $(2.1, 1)$: $l_1$ at the root with $x \mapsto g(a)$, $y \mapsto f(a, g(b))$; $l_2$ at $g(a)$; and $l_1$ at $f(a, g(b))$ with $x \mapsto a$, $y \mapsto b$. The node $g(f(a, g(b)))$ at position 2 matches neither pattern.

**Match sets, bottom up.** Write $\omega$ for a variable, and collect the subpatterns of the patterns: $\omega$, $a$, $g(\omega)$, $g(a)$ and $f(\omega, g(\omega))$. The match set of a node is the set of subpatterns that match the subtree at the node. It depends only on the symbol of the node and the match sets of its children, so it can be computed from the leaves upward:

| node | match set |
| --- | --- |
| $a$ | $\omega$, $a$ |
| $b$ | $\omega$ |
| $g(a)$ | $\omega$, $g(\omega)$, $g(a)$ |
| $g(b)$ | $\omega$, $g(\omega)$ |
| $f(a, g(b))$ | $\omega$, $f(\omega, g(\omega))$ |
| $g(f(a, g(b)))$ | $\omega$, $g(\omega)$ |
| $t$ | $\omega$, $f(\omega, g(\omega))$ |

A pattern matches at the nodes whose match set contains it. If the possible match sets and a table from (symbol, child sets) to the parent set are computed in advance, each node costs one table lookup; this is the bottom-up algorithm of Hoffmann and O'Donnell.

**Non-example.** The pattern $f(x, x)$ does not match $f(a, b)$, although the linear pattern $f(x, y)$ does. Wildcard methods that ignore repeated variables report false matches for non-linear patterns, which then need an equality check.

## Known algorithms

- **Naive matching.** Try each pattern at each node, comparing symbol by symbol: $O(n m)$ for one pattern. Dubiner, Galil and Magen observed that it takes $O(n h)$ time, where $h$ is the height of the pattern, since a node of the subject is compared only in the attempts that start at itself or at one of its $h$ nearest ancestors, once in each.
- **Bottom-up automata** (Hoffmann and O'Donnell, 1982). Precompute all match sets that can occur, and a table for each symbol from the child match sets to the parent match set. Matching is then one pass in $O(n)$ time plus the output. The tables are a deterministic bottom-up tree automaton, and they can be exponential in the size of the pattern set, though they are small for many practical sets. See [Hoffmann-O'Donnell matching](/hoffmann-odonnell-matching/).
- **Top-down by path strings** (Hoffmann and O'Donnell, 1982). Write each root-to-leaf path of each pattern as a string of symbols and argument numbers, and search all of them along the root-to-leaf paths of the subject with an [Aho-Corasick](/aho-corasick/) automaton. A pattern matches at a node iff every one of its path strings is found starting there, which is checked with one counter per (node, pattern).
- **Discrimination nets and decision trees.** Compile the patterns into a tree of tests on the symbols at chosen positions, as done in rewriting engines and in the compilation of pattern matching in functional languages; see [discrimination trees](/discrimination-tree/).
- **Faster one-pattern algorithms.** Kosaraju (1989) gave the first algorithm that beats $O(n m)$, in $O(n m^{0.75} \operatorname{polylog} m)$ time. Dubiner, Galil and Magen improved this to $O(n m^{1/2} \operatorname{polylog} m)$ by exploiting periodicities of paths. Cole and Hariharan reduced tree pattern matching to subset matching and obtained a randomized $O(n \log^3 m)$ algorithm (1997), and later a reduction to subset matching in linear time (2003).

## Bounds

- **Lower bound.** $\Omega(n + m)$ time, since every node of the subject and of the pattern can matter, plus the size of the output.
- **One pattern.** $O(n m)$ naively, $O(n h)$ by the observation of Dubiner, Galil and Magen, and $O(n m^{1/2} \operatorname{polylog} m)$ deterministically; with randomization, $O(n \log^3 m)$.
- **Fixed pattern set.** $O(n)$ per subject after preprocessing with bottom-up tables, whose size can be exponential in the patterns.
- **Non-linear patterns.** The same bounds hold after building a term DAG of the subject in $O(n)$ expected time with hashing, since equality of subtrees becomes equality of nodes.

## Reductions

- **String matching is a special case.** A string $a_1 \cdots a_n$ is a tree of unary symbols $a_1(a_2(\cdots))$, and a pattern $b_1 \cdots b_m$ becomes $b_1(\cdots b_m(x))$, with $x$ matching any suffix. So [string matching](/string-matching/) and [multiple string matching](/multiple-string-matching/) are tree pattern matching on paths.
- **Tree matching to string matching.** The top-down method reduces matching of linear patterns to multiple string matching along root-to-leaf paths, plus counting.
- **Tree matching to subset matching.** Cole and Hariharan reduce tree pattern matching to subset matching, a string problem in which each text position holds a set of characters, in linear time.

## Applications

- Rewriting engines: finding redexes for [normal form computation](/normal-form-computation/), in interpreters for term rewriting, in theorem provers and in algebraic simplifiers.
- Code generation: instruction selection covers an intermediate-code tree with patterns, each standing for one machine instruction with a cost, and picks a cheapest cover by dynamic programming over the match sets.
- Compilers for functional languages: patterns in function definitions are compiled into decision trees of tests.
- Query languages for trees and documents, such as XPath-style queries over XML trees, which find all nodes where a tree pattern fits.

## References
