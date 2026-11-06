---
tag: 2FPR6N
kind: definition
slug: attribute-grammar
name: Attribute grammar
aliases:
- attributed grammar
- syntax-directed definition
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A context-free grammar extended with attributes computed by semantic rules on parse trees.
prereqs: [context-free-grammar, parse-tree, topological-sort]
see_also: [syntax-directed-translation, abstract-syntax-tree, ll1-parsing, lr-parsing, recursive-descent-parsing, shift-reduce-parsing, tree-traversal, cfg-parsing-problem]
sources:
  - paper: doi:10.1007/BF01692511
    title: Donald E. Knuth, Semantics of context-free languages, Mathematical Systems Theory 2(2) (1968)
    locator: pp. 127 to 145 (synthesized and inherited attributes, the binary numeral example, and a test for circularity)
  - paper: doi:10.1007/BF01702865
    title: Donald E. Knuth, Semantics of context-free languages, correction, Mathematical Systems Theory 5(2) (1971)
    locator: pp. 95 to 96 (a corrected circularity test)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Chapter 5, Syntax-Directed Translation (5.1 Syntax-Directed Definitions, 5.2 Evaluation Orders for SDD's, with S-attributed and L-attributed definitions)
  - paper: doi:10.1145/361227.361231
    title: Mehdi Jazayeri, William F. Ogden and William C. Rounds, The intrinsically exponential complexity of the circularity problem for attribute grammars, Communications of the ACM 18(12) (1975)
    locator: pp. 697 to 706
  - paper: doi:10.1007/BF00288644
    title: Uwe Kastens, Ordered attributed grammars, Acta Informatica 13(3) (1980)
    locator: pp. 229 to 256 (a polynomial test and evaluation by visit sequences)
  - paper: doi:10.1145/210376.197409
    title: Jukka Paakki, Attribute grammar paradigms, a high-level methodology in language implementation, ACM Computing Surveys 27(2) (1995)
    locator: pp. 196 to 255 (a survey of classes, evaluators and extensions)
---

An attribute grammar is a [context-free grammar](/context-free-grammar/) in which every symbol carries named values, its *attributes*, and every production carries *semantic rules* that compute the attributes of its symbols from each other. On a [parse tree](/parse-tree/), the rules give one equation for each attribute of each node, and the meaning of the input is the value of an attribute at the root. Knuth introduced them in 1968, with the distinction between *synthesized* attributes, which flow up the tree, and *inherited* attributes, which flow down; compilers use them to describe type checking, translation and code generation.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, $n$ is the length of the input, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. A production is written $p : X_0 \to X_1 \cdots X_k$, with the positions $0, \ldots, k$ naming its symbols.

An **attribute grammar** consists of

1. a context-free grammar $G$;
2. for each symbol $X \in V \cup \Sigma$, two disjoint finite sets of attributes, the *synthesized* attributes $\mathrm{Syn}(X)$ and the *inherited* attributes $\mathrm{Inh}(X)$, each with a set of possible values, where $\mathrm{Inh}(S) = \emptyset$ and the synthesized attributes of a terminal are given by the lexical analyser;
3. for each production $p : X_0 \to X_1 \cdots X_k$, exactly one *semantic rule*
$$X_i.a = f_{p,i,a}(X_{j_1}.b_1, \ldots, X_{j_r}.b_r)$$
for each pair $(i, a)$ with $i = 0$ and $a \in \mathrm{Syn}(X_0)$, or $i \ge 1$ and $a \in \mathrm{Inh}(X_i)$. The arguments are attributes of the symbols of the same production.

So a production defines the synthesized attributes of its left side and the inherited attributes of its right side. A synthesized attribute of a node is computed from its children, and an inherited one from its parent and siblings.

**Attribute instances and the dependency graph.** Let $T$ be a parse tree. Every node $u$ labelled $X$ has one *attribute instance* $u.a$ for each attribute $a$ of $X$. Each internal node $u$, expanded by the production $p$, gives the equations of $p$ with the positions replaced by $u$ and its children, and every instance, except the synthesized attributes of leaves, is defined by exactly one equation. The *dependency graph* $D(T)$ has an edge from $v.b$ to $u.a$ when $v.b$ is an argument in the equation for $u.a$.

**Well-defined grammars.** The grammar is *noncircular* if $D(T)$ is acyclic for every parse tree $T$. Then the equations of every tree have exactly one solution, computed by evaluating the instances in a [topological order](/topological-sort/) of $D(T)$, in time linear in the size of $T$ plus the cost of the functions $f$. The *meaning* of a sentence is the value of a chosen synthesized attribute of the root.

**Important classes.**

- **S-attributed:** there are only synthesized attributes. Every attribute can be evaluated in postorder, so during a bottom-up [shift-reduce](/shift-reduce-parsing/) parse, at each reduction.
- **L-attributed:** in every production $X_0 \to X_1 \cdots X_k$, each inherited attribute of $X_i$ depends only on inherited attributes of $X_0$ and on attributes of $X_1, \ldots, X_{i-1}$. All attributes can be evaluated in one depth-first left-to-right traversal, so during a top-down [LL(1)](/ll1-parsing/) or [recursive descent](/recursive-descent-parsing/) parse. Every S-attributed grammar is L-attributed.
- **Ordered (Kastens):** for each symbol there is a fixed order of the attributes, computable in polynomial time, which lets every node be evaluated by a fixed sequence of visits. Ordered grammars are noncircular.

## Examples and non-examples

**Binary numerals (Knuth).** The grammar
$$N \to L \mid L\,.\,L, \qquad L \to L B \mid B, \qquad B \to 0 \mid 1$$
has the synthesized attributes $v$ (value) for $N$, $L$ and $B$ and $l$ (length) for $L$, and the inherited attribute $s$ (scale, the power of 2 of the rightmost digit) for $L$ and $B$. The rules are:

| production | semantic rules |
|---|---|
| $B \to 0$ | $B.v = 0$ |
| $B \to 1$ | $B.v = 2^{B.s}$ |
| $L \to B$ | $L.v = B.v$, $B.s = L.s$, $L.l = 1$ |
| $L_0 \to L_1 B$ | $L_0.v = L_1.v + B.v$, $B.s = L_0.s$, $L_1.s = L_0.s + 1$, $L_0.l = L_1.l + 1$ |
| $N \to L$ | $N.v = L.v$, $L.s = 0$ |
| $N \to L_1\,.\,L_2$ | $N.v = L_1.v + L_2.v$, $L_1.s = 0$, $L_2.s = -L_2.l$ |

For $1101.01$ the tree has 31 attribute instances, and evaluating them in a topological order gives $N.v = 8 + 4 + 1 + 0.25 = 13.25$. A script checks the evaluator on this grammar against direct conversion for 500 random numerals. The grammar is noncircular: $l$ depends only on the shape of the tree, $s$ on $l$ and $s$ higher up, and $v$ on $s$. It is not L-attributed, because $L_2.s$ depends on $L_2.l$, an attribute of the same symbol; an evaluator needs one pass up the fractional part for $l$ and a second pass down for $s$.

**Expression values (S-attributed).** For $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid \mathit{num}$ with one synthesized attribute $val$, the rules $E_0.val = E_1.val + T.val$, $T_0.val = T_1.val \times F.val$, $F.val = \mathit{num}.val$ and so on compute the value of the expression. For $3 + 4 * 5$ the root gets $23$, because the tree groups $4 * 5$ first. An LR parser computes it on a stack of values, one per grammar symbol.

**Declarations (L-attributed).** For $D \to T\, L$, $T \to \mathit{int} \mid \mathit{real}$, $L \to L , \mathit{id} \mid \mathit{id}$, the inherited attribute $L.type$ is set by $L.type = T.type$ in the first production and copied down by $L_1.type = L_0.type$, and each $\mathit{id}$ records its type in a symbol table. In "real $x, y, z$" all three names get the type real, which is known before the names are read. This is the usual way to pass context, such as types and scopes, from left to right.

**Non-example, circular.** With $A \to B$ and $B \to b$, the rules $A.s = B.s$ and $B.i = A.s$ in the first production and $B.s = B.i$ in the second give the cycle $A.s \to B.i \to B.s \to A.s$ in the dependency graph of the only tree, so the equations have no well-defined solution, and an evaluator finds no topological order.

**Non-example, not well-formed.** A rule of the production $X_0 \to X_1 \cdots X_k$ that defines a synthesized attribute of $X_1$, or a production that gives no rule for some inherited attribute of $X_2$, breaks the definition: on some tree an instance has two equations or none.

## Related definitions

- **Syntax-directed definition and translation scheme.** Aho, Lam, Sethi and Ullman call an attribute grammar whose rules may also have side effects, such as entering a name in a table, a *syntax-directed definition*. A [syntax-directed translation](/syntax-directed-translation/) scheme places the actions inside the right sides, at the point of the parse where they run, which fixes the evaluation order.
- **Circularity test.** Whether an attribute grammar is noncircular is decidable, by Knuth's test, which computes for each nonterminal the possible dependency relations between its attributes over all subtrees. Jazayeri, Ogden and Rounds proved that the problem needs exponential time in the worst case. Stronger conditions, such as being *absolutely noncircular* or ordered, have polynomial tests.
- **Abstract syntax trees.** Attributes are often defined on an [abstract syntax tree](/abstract-syntax-tree/), described by an abstract grammar, in place of the parse tree; one attribute of the parse tree can build the abstract syntax tree itself.
- **Extensions.** Higher-order attribute grammars let an attribute hold a tree that is itself attributed, and reference attribute grammars let an attribute point to another node, for example from the use of a name to its declaration. Tools such as JastAdd, Silver and Eli are based on these extensions.
- **Parsing and evaluation together.** A [shift-reduce parser](/shift-reduce-parsing/) evaluates S-attributed grammars, and an [LL parser](/ll1-parsing/) evaluates L-attributed ones, without building the tree. Other grammars need the tree and a separate pass, in the order given by the dependency graph or by the visit sequences of an ordered grammar.

## References
