---
tag: 9DVCYR
kind: concept
slug: term-graph-rewriting
name: Term graph rewriting
aliases:
- graph rewriting of terms
- term graph reduction
area: automata-and-parsing/term-rewriting
level: advanced
summary: Rewriting on directed acyclic graphs representing shared terms.
prereqs: [term-rewriting-system, directed-acyclic-graph]
see_also: [graph-reduction, term-dag, hash-consing, reduction-strategy, parallel-rewriting, orthogonal-rewrite-system, congruence-closure, e-graph]
sources:
  - paper: doi:10.1007/3-540-17945-3_8
    title: Henk P. Barendregt, Marko C. J. D. van Eekelen, John R. W. Glauert, J. Richard Kennaway, Marinus J. Plasmeijer and M. Ronan Sleep, Term graph rewriting, PARLE Parallel Architectures and Languages Europe, Lecture Notes in Computer Science 259 (1987)
    locator: pp. 141 to 158 (term graphs, graph rewrite steps, and soundness and completeness for orthogonal systems)
  - paper: doi:10.1145/177492.177577
    title: J. Richard Kennaway, Jan Willem Klop, M. Ronan Sleep and Fer-Jan de Vries, On the adequacy of graph rewriting for simulating term rewriting, ACM Transactions on Programming Languages and Systems 16(3) (1994)
    locator: pp. 493 to 523
  - book: isbn:9789810240202
    title: Detlef Plump, Term graph rewriting, in Hartmut Ehrig and others (editors), Handbook of Graph Grammars and Computing by Graph Transformation, Volume 2, World Scientific, 1999
    locator: pp. 3 to 61
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 13, Term graph rewriting
---

**Term graph rewriting** applies the rules of a [term rewriting system](/term-rewriting-system/) to a graph instead of a tree. Equal subterms can then be stored once and shared, and a rule that copies a variable copies a pointer, not a subterm. A redex that is shared is contracted once for all its copies. This is how functional languages implement lazy evaluation ([graph reduction](/graph-reduction/)), and it can save an exponential amount of time and space. The price is that a graph step corresponds to several term steps at once, so graph rewriting simulates term rewriting exactly only for well-behaved systems, such as the [orthogonal](/orthogonal-rewrite-system/) ones.

## In plain words

An expression is usually drawn as a tree, where every part appears in its own copy. But many expressions contain the same part several times. A graph lets several places point to one shared copy of that part.

When a rule says "replace this by two copies of that", a graph does not copy anything: it adds two pointers to the same part. Later, when the shared part is simplified, all places that point to it see the result at once. So work is done once instead of many times.

This sharing has a side effect. Since the copies are one object, they always change together. If the rules allow a choice of results, a graph cannot give the copies different results, while a tree could.

## The idea

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions with root $\varepsilon$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

**Term graphs.** A term graph $g$ is a finite set of nodes, each with a label from $\Sigma \cup V$ and an ordered list of successors whose length is the arity of the label, together with a root node. Variable nodes have no successors, and each variable labels at most one node. A term graph is **acyclic** if it is a [directed acyclic graph](/directed-acyclic-graph/). The **unravelling** $U(g)$ is the term read off from the root by following successors; on an acyclic graph it is a finite term, and it can be exponentially larger than $g$. A tree has $U(g)$ of the same size; a graph with **maximal sharing**, where no two nodes have the same label and successors, is the [term DAG](/term-dag/) built by [hash-consing](/hash-consing/).

**A graph rewrite step.** For a rule $l \to r$ and a node $n$ of $g$:

1. **Match.** Find a map $\sigma$ from the variables of $l$ to nodes of $g$ such that the tree of $l$ maps into $g$ with its root at $n$, symbol by symbol. For a non-linear $l$, the two occurrences of a variable must map to the same node.
2. **Build.** Add new nodes for the function symbols of $r$. A variable $x$ of $r$ is not copied: its occurrences point to the node $\sigma(x)$.
3. **Redirect.** Every edge that pointed to $n$, and the root if it was $n$, now points to the root of the new copy of $r$. If $r$ is a variable $x$, they point to $\sigma(x)$.
4. **Collect garbage.** Remove the nodes no longer reachable from the root.

The cost of a step is $O(|l| + |r|)$ plus the cost of redirecting edges, which is $O(1)$ if $n$ is overwritten in place with the root of $r$ (an indirection node is used when $r$ is a variable).

**Soundness.** If $g \Rightarrow h$ is a graph step at node $n$, then $U(g) \rightrightarrows_R U(h)$ in one [parallel step](/parallel-rewriting/) that contracts every occurrence of the redex of $n$ in the unravelling, so $U(g) \to_R^+ U(h)$. The occurrences are at pairwise parallel positions, since none of them lies inside another copy of the same node in an acyclic graph.

**Completeness, and where it fails.** A graph step contracts all copies of a shared redex together. A term reduction that contracts the copies differently has no graph counterpart. For orthogonal systems this does not matter: every term reduction to a normal form has a graph reduction to the same normal form, so graph rewriting computes the same normal forms (Barendregt and others, 1987; Kennaway, Klop, Sleep and de Vries, 1994). For systems with overlapping rules, or with a choice of rule, the set of results changes. For non-left-linear rules, the match condition "same node" is stronger than "equal subterms": $f(x, x)$ does not match a node $f(m_1, m_2)$ whose arguments are equal terms stored in two places. Maximal sharing removes this gap, since equal subterms are then the same node.

**Cyclic term graphs.** If cycles are allowed, a graph can represent an infinite regular term. The rule for a recursive definition can then point back to its own node, as in the list $\mathit{ones} = 1 : \mathit{ones}$, a node with a pointer to itself. Its unravelling is infinite, and the link to term rewriting goes through infinitary rewriting.

## Examples

All counts below were checked by a program that implements both term rewriting and the graph steps above.

**Exponential saving.** The rule $f(x) \to g(x, x)$ copies its argument. Start from $f^n(a)$, a chain of $n$ nodes $f$ above $a$. The normal form as a term is a complete binary tree of $g$ nodes with $2^{n+1} - 1$ symbols. Outermost term rewriting needs $2^n - 1$ steps, since every copy of an inner $f$ is contracted separately: 1, 3, 7, 15, 31, 63 steps for $n = 1, \ldots, 6$. Graph rewriting needs $n$ steps, and the normal form graph has $n + 1$ nodes: a chain of $g$ nodes, each with both successors pointing to the next one.

| $n$ | term steps (outermost) | term size of normal form | graph steps | graph nodes |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 1 | 2 |
| 2 | 3 | 7 | 2 | 3 |
| 3 | 7 | 15 | 3 | 4 |
| 6 | 63 | 127 | 6 | 7 |

**Sharing removes choices.** Take $R = \{a \to b,\ a \to c,\ f(x) \to g(x, x)\}$, which is not confluent. From the term $f(a)$, term rewriting reaches 12 terms, including $g(b, c)$: the two copies of $a$ can take different rules. From the tree $f(a)$, graph rewriting reaches only 6: $f(a)$, $f(b)$, $f(c)$, $g(a, a)$, $g(b, b)$ and $g(c, c)$, where the last three are drawn with one shared argument. The normal form $g(b, c)$ is lost.

**Call by need.** $(\lambda x.\, x + x)\,(3 \times 4)$ in a lazy language: the argument is passed as a pointer to the unevaluated node $3 \times 4$; the first use of $x$ evaluates it and overwrites the node with $12$, and the second use reads $12$. This is outermost reduction with sharing; see [reduction strategy](/reduction-strategy/).

**Non-examples.**

- A tree, where each node has one parent, is a term graph without sharing; graph rewriting on it is term rewriting, except that a step on a duplicating rule creates sharing.
- An [e-graph](/e-graph/) also shares subterms, but its nodes stand for classes of equal terms, and it records equations instead of replacing nodes; it is used for [congruence closure](/congruence-closure/) and equality saturation, not for rewriting to one result.

## Where it is used

- Implementations of lazy functional languages, such as the G-machine and the spineless tagless G-machine of Haskell, and the language Clean, whose semantics is defined by term graph rewriting. See [graph reduction](/graph-reduction/).
- Rewriting engines and proof assistants that store terms with [hash-consing](/hash-consing/), so that equal subterms are one node and normal forms can be memoized.
- Compilers, where intermediate code is a graph of shared expressions and optimizations are rewrite rules on it.
- The theory of optimal reduction in the lambda calculus, which uses more refined sharing graphs.

## References
