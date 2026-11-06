---
tag: VZZYM9
kind: definition
slug: abstract-syntax-tree
name: Abstract syntax tree
aliases:
- AST
area: automata-and-parsing/context-free-parsing
level: intro
summary: A simplified parse tree that omits punctuation and grammar-only nodes, keeping program structure.
prereqs: [context-free-grammar, parse-tree]
see_also: [expression-tree, syntax-directed-translation, attribute-grammar, ambiguity, term, term-algebra, derivation]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 2.5.1, Abstract and Concrete Syntax, and Section 5.3.1, Construction of Syntax Trees
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Chapter 4, Abstract Syntax (semantic actions, abstract parse trees, and positions)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 2, Grammars as a Generating Device (production trees), and Chapter 3, Introduction to Parsing
---

An abstract syntax tree (AST) is a tree that shows the structure of a program or an expression: each inner node is an operation or a construct, and its children are the operands or the parts. It is made from the [parse tree](/parse-tree/) of a [context-free grammar](/context-free-grammar/) by dropping the tokens that only guide the parser, such as parentheses, semicolons and keywords, and the nodes that exist only to encode precedence. Compilers, interpreters and program analysis tools work on the AST, not on the parse tree.

## Definition

**Notation.** A context-free grammar is $G = (V, \Sigma, R, S)$, with the nonterminals $V$, the terminals (tokens) $\Sigma$, the productions $R$ and the start symbol $S$. A production is written $A \to \alpha$, and $A \to \alpha \mid \beta$ lists two productions with the same left side. $\varepsilon$ is the empty string, $n$ is the length of the input and $|G|$ is the size of the grammar, the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. The other pages of this area use the same notation.

**Abstract syntax.** An abstract syntax is a finite set of *sorts* (for example `Expr` and `Stmt`) and a finite set of *constructors*. Each constructor $c$ has a type $c : s_1 \times \cdots \times s_k \to s$, with $k \ge 0$ and sorts $s_1, \ldots, s_k, s$. A constructor with $k = 0$ can carry a value from a fixed set, for example the integer of a literal or the name of a variable.

**Abstract syntax tree.** An AST of sort $s$ is a finite ordered tree whose root is labeled by a constructor $c : s_1 \times \cdots \times s_k \to s$ and has exactly $k$ children, where the $i$-th child is an AST of sort $s_i$. In other words, an AST is a [term](/term/) over the constructors, an element of the many-sorted [term algebra](/term-algebra/).

**Abstraction map.** A parser builds the AST with a map $\mathcal{A}$ from parse trees to ASTs that is defined by one rule for each production. For a parse tree with root production $A \to X_1 \cdots X_m$ and subtrees $t_1, \ldots, t_m$, the rule computes $\mathcal{A}(t)$ from the values $\mathcal{A}(t_i)$ of some of the children. The rule may skip a child (a parenthesis), pass one child up unchanged (a chain production $E \to T$), or apply a constructor. Because the map is defined by structural recursion on the parse tree, a [syntax-directed translation](/syntax-directed-translation/) computes it during the parse, and the parse tree itself need not be stored.

The grammar that the parser uses is the *concrete syntax*. Two strings with the same AST can differ in their concrete syntax, for example `(a + b)` and `a + b`, or two layouts of the same program.

## Examples and non-examples

**An expression.** Take the usual grammar of arithmetic, with the tokens `+`, `*`, `(`, `)` and `num`:

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to ( E ) \mid \mathtt{num}.$$

The input `2 * (3 + 4)` has 7 tokens and one parse tree. That tree has 18 nodes: 11 nodes labeled $E$, $T$ or $F$, and 7 leaves. The AST has 5 nodes:

```text
parse tree                                AST
E                                         Mul
└─ T                                      ├─ Num 2
   ├─ T ─ F ─ num(2)                      └─ Add
   ├─ *                                      ├─ Num 3
   └─ F                                      └─ Num 4
      ├─ (
      ├─ E
      │  ├─ E ─ T ─ F ─ num(3)
      │  ├─ +
      │  └─ T ─ F ─ num(4)
      └─ )
```

The abstraction map has these rules: $E \to E + T$ gives $\mathrm{Add}(\mathcal{A}(E), \mathcal{A}(T))$; $T \to T * F$ gives $\mathrm{Mul}(\mathcal{A}(T), \mathcal{A}(F))$; $F \to (E)$ gives $\mathcal{A}(E)$, which drops both parentheses; the chain rules $E \to T$ and $T \to F$ pass the value of the child up; and $F \to \mathtt{num}$ gives $\mathrm{Num}(v)$ with the value $v$ of the token. The parentheses do not appear in the AST, because the shape of the tree already says that the addition is done first.

**Associativity.** With the grammar $E \to E - T \mid T$, $T \to \mathtt{num}$, the input `8 - 3 - 2` has one parse tree, and its AST is $\mathrm{Sub}(\mathrm{Sub}(8, 3), 2)$, with the value 3. The tree $\mathrm{Sub}(8, \mathrm{Sub}(3, 2))$ has the value 7. Both are well-formed ASTs, so the AST of a string depends on the grammar and on how it resolves [ambiguity](/ambiguity/).

**A statement.** For `if (x) y = 1; else y = 2;` a typical AST is $\mathrm{If}(\mathrm{Var}\ x, \mathrm{Assign}(y, \mathrm{Num}\ 1), \mathrm{Assign}(y, \mathrm{Num}\ 2))$. The keywords `if` and `else`, the parentheses and the semicolons are gone: the constructor `If` and the order of its three children carry the same information.

**Non-example: the parse tree.** The parse tree above is not an AST of this abstract syntax. It has nodes for the parentheses and for the chain productions $E \to T$ and $T \to F$, which are not constructors.

**Non-example: a shared graph.** If a compiler merges the two equal subtrees of `(a + b) * (a + b)` into one node with two parents, the result is a directed acyclic graph, not a tree. Such a DAG is a common later form, used for common subexpression elimination, but it is not an AST.

**Non-example: a token list.** The sequence of tokens `2 * ( 3 + 4 )` is the input of the parser, not a tree. It does not say which operation applies first.

## Related definitions

- [Parse tree](/parse-tree/): the tree of a [derivation](/derivation/), with one leaf for each token and one inner node for each use of a production. The AST is its image under the abstraction map.
- [Expression tree](/expression-tree/): the AST of an arithmetic expression, with operators at the inner nodes and operands at the leaves.
- [Syntax-directed translation](/syntax-directed-translation/) and [attribute grammars](/attribute-grammar/): the standard ways to attach the rules of the abstraction map to the productions.
- [Term](/term/) and [term algebra](/term-algebra/): the algebraic view of ASTs, used in [term rewriting](/term-rewriting-system/).
- [Ambiguity](/ambiguity/): when a grammar is ambiguous, one string has several parse trees and can have several ASTs.

## References
