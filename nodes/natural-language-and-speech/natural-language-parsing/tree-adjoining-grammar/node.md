---
tag: CT08GA
kind: model
slug: tree-adjoining-grammar
name: Tree-adjoining grammar
aliases:
- TAG
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: A mildly context-sensitive formalism that builds trees from elementary trees by substitution and adjunction, parsed in O(n^6) time.
prereqs: [context-free-grammar, parse-tree]
see_also: [combinatory-categorial-grammar, supertagging, cyk-algorithm, context-free-language, dependency-tree, feature-structure-unification, chart-parsing, synchronous-context-free-grammar]
sources:
  - paper: "Aravind K. Joshi, Leon S. Levy and Masako Takahashi, Tree adjunct grammars, Journal of Computer and System Sciences 10(1), 136-163, 1975"
    title: "Aravind K. Joshi, Leon S. Levy and Masako Takahashi, Tree adjunct grammars"
    locator: "the definition of tree adjunct grammars and their string languages"
  - paper: doi:10.1007/978-3-642-59126-6_2
    title: "Aravind K. Joshi and Yves Schabes, Tree-adjoining grammars, in Handbook of Formal Languages, Volume 3, Springer, 1997, 69-123"
    locator: "the definitions of substitution, adjunction and adjoining constraints, lexicalized TAG, derivation trees, the closure properties and the parsing algorithms"
  - paper: doi:10.3115/981210.981221
    title: "K. Vijay-Shanker and Aravind K. Joshi, Some computational properties of tree adjoining grammars, Proceedings of ACL 1985, 82-93"
    locator: "the CKY-style recognition algorithm in O(n^6) time"
  - paper: "K. Vijay-Shanker and David J. Weir, The equivalence of four extensions of context-free grammars, Mathematical Systems Theory 27(6), 511-546, 1994"
    title: "K. Vijay-Shanker and David J. Weir, The equivalence of four extensions of context-free grammars"
    locator: "the weak equivalence of TAG, CCG, linear indexed grammar and head grammar"
  - paper: "Srinivas Bangalore and Aravind K. Joshi, Supertagging: an approach to almost parsing, Computational Linguistics 25(2), 237-265, 1999"
    title: "Srinivas Bangalore and Aravind K. Joshi, Supertagging: an approach to almost parsing"
    locator: "the elementary trees of lexicalized TAG as supertags"
---

Tree-adjoining grammar (TAG) builds [parse trees](/parse-tree/) from a finite set of elementary trees with two operations: substitution, which plugs a tree into a leaf, and adjunction, which splices a tree into the middle of another tree. Adjunction lets a grammar stretch a tree from inside, so it can keep a verb and its arguments in one elementary tree however far apart they end up, and it generates some languages that no [context-free grammar](/context-free-grammar/) can. TAG is mildly context-sensitive: it is weakly equivalent to [combinatory categorial grammar](/combinatory-categorial-grammar/), which reaches the same languages with categories instead of trees, and its recognition problem takes $O(n^6)$ time for a sentence of $n$ words.

## The machine

**Grammar.** A TAG is a tuple $(N, \Sigma, I, A, S)$, which plays the role of $G = (N, \Sigma, R, S)$ for context-free grammars with the rules $R = I \cup A$ split in two. $N$ is the set of nonterminals, $\Sigma$ the set of terminals and $S \in N$ the start symbol. $I$ is a finite set of **initial trees** and $A$ a finite set of **auxiliary trees**. In both, every internal node has a label in $N$ and every leaf has a label in $\Sigma \cup N \cup \{\varepsilon\}$. A nonterminal leaf of an initial tree is a substitution node, marked $X{\downarrow}$. An auxiliary tree has exactly one special leaf, the **foot**, marked $X^*$, whose label equals the label $X$ of the root; its other nonterminal leaves are substitution nodes. The size $g$ is the total number of nodes of the elementary trees.

**Substitution.** A substitution node $X{\downarrow}$ is replaced by an initial tree, or a tree derived from one, whose root has the label $X$.

**Adjunction.** Let $\eta$ be an internal node with label $X$ in a tree $\gamma$, and let $\beta$ be an auxiliary tree with root and foot $X$. Adjoining $\beta$ at $\eta$ cuts out the subtree of $\gamma$ at $\eta$, puts $\beta$ in its place, and hangs the cut subtree at the foot of $\beta$. The words of $\beta$ left of the foot end up left of the words of the subtree, and the rest end up right of them, so one adjunction can add words on both sides.

**Constraints.** Each internal node can carry a null adjunction constraint (NA, no adjunction here), a selective one (SA, only these auxiliary trees) or an obligatory one (OA, some adjunction must happen here).

**Language.** A derived tree is complete if its root is labeled $S$, it came from an initial tree, no substitution node is left and every OA constraint is met. The string language is the set of yields of complete derived trees. The **derivation tree** records which elementary tree was substituted or adjoined at which node of which other tree; it is the main output of a TAG parser.

**Lexicalized TAG.** In a lexicalized TAG (LTAG), every elementary tree has at least one terminal leaf, its anchor. The tree of a transitive verb holds the verb, the subject slot and the object slot, so all the arguments of the verb are local to one tree, and adjunction adds modifiers or stretches the tree for long-distance dependencies.

**An example.** Let the initial tree be $\alpha = S \to \varepsilon$, and let $\beta$ be the auxiliary tree whose root $S_{NA}$ has the children $a$, $S$, $d$, where that middle $S$ has the children $b$, $S^*_{NA}$, $c$. Adjoining $\beta$ at the root of $\alpha$ gives the yield $a\,b\,c\,d$. Adjoining $\beta$ again at the middle $S$ of the copy just added gives $a\,a\,b\,b\,c\,c\,d\,d$, and in general the grammar generates $\{a^m b^m c^m d^m : m \ge 0\}$. This language is not context-free (theorem, by the pumping lemma for context-free languages). The same mechanism gives the cross-serial dependencies of Dutch and Swiss German verb clusters.

## What it counts

**Recognition time.** Vijay-Shanker and Joshi (1985) gave a CKY-style recognizer that runs in $O(n^6)$ time for a fixed grammar (theorem). An item says that the subtree at a node $\eta$ of an elementary tree, with any adjunctions inside it, derives the words of a span $(i, l)$, where spans are fenceposts: $(i, l)$ covers the words $i + 1$ to $l$. If the subtree contains the foot of an auxiliary tree, the item also records the gap $(j, k)$ that the foot covers. So there are $O(g\,n^4)$ items. The costly step adjoins an auxiliary tree, whose item has span $(i, l)$ and gap $(j, k)$, at a node whose item has the span $(j, k)$ and its own gap $(p, q)$; it combines six positions, which gives $O(n^6)$ steps for a fixed grammar. Space is $O(n^4)$ for a fixed grammar.

**Comparison.** For context-free grammars the [CYK algorithm](/cyk-algorithm/) takes $O(n^3)$, so the extra power costs three more factors of $n$. In practice, lexicalized parsers first prune the elementary trees of each word with a [supertagger](/supertagging/) (heuristic).

**Closure and growth.** Tree-adjoining languages are closed under union, concatenation, Kleene star, homomorphism and intersection with regular languages, so they form a full abstract family of languages (theorem, Joshi and Schabes 1997). They have the constant growth property: the lengths of the strings, in increasing order, differ by bounded steps (theorem).

## Relation to other models

- **Context-free grammar.** A TAG with substitution only, a tree substitution grammar, generates exactly the [context-free languages](/context-free-language/) (theorem). Every context-free grammar has a weakly equivalent TAG, so tree-adjoining languages contain the context-free ones, and the example above shows that the inclusion is strict.
- **CCG and others.** TAG, [CCG](/combinatory-categorial-grammar/), linear indexed grammar and head grammar generate the same string languages (theorem, Vijay-Shanker and Weir 1994). These classes are the standard examples of mildly context-sensitive grammars, a notion Joshi proposed in 1985: they contain the context-free languages, capture limited cross-serial dependencies, have constant growth and parse in polynomial time. The derivations differ: TAG composes trees, CCG composes categories.
- **Dependency trees.** In a lexicalized TAG each node of the derivation tree is a word, and each edge joins a word to a word that it substitutes into or adjoins to. The derivation tree is therefore close to a [dependency tree](/dependency-tree/), and TAG parsers are often evaluated by its arcs.
- **Feature structures.** Feature-based TAG puts a top and a bottom feature structure on each node and joins them by [feature structure unification](/feature-structure-unification/) when the derivation is complete, which replaces the adjunction constraints.
- **Synchronous grammars.** Synchronous TAG pairs the trees of two grammars, in the way that a [synchronous context-free grammar](/synchronous-context-free-grammar/) pairs rules, for translation or for syntax-semantics mappings.

## Known results in the model

- **Lexicalization.** Tree substitution grammars cannot in general lexicalize a finitely ambiguous context-free grammar while keeping its trees, and TAGs can (theorem, discussed in Joshi and Schabes 1997). This is one of the main arguments for adjunction.
- **Supertagging.** Bangalore and Joshi (1999) treated the elementary trees of an LTAG as rich part-of-speech tags and chose them with a tagger before parsing, which they called almost parsing. This idea is the [supertagging](/supertagging/) technique that CCG parsers later adopted.
- **Wide-coverage grammars.** Large hand-written LTAGs for English, such as the XTAG grammar, and grammars extracted from treebanks were built in the 1990s and 2000s. They give each common word many elementary trees, which is the ambiguity that supertagging reduces.

## References
