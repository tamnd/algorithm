---
tag: 8MXJX3
kind: definition
slug: parse-tree
name: Parse tree
aliases:
- derivation tree
area: automata-and-parsing/context-free-parsing
level: intro
summary: A rooted tree showing how a string is derived from the start symbol by a grammar.
prereqs: [context-free-grammar, derivation]
see_also: [leftmost-derivation, abstract-syntax-tree, ambiguity, shared-packed-parse-forest, sentential-form, cyk-algorithm, earley-parser, cfl-pumping-lemma]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 5.2, Parse Trees (5.2.1 Constructing Parse Trees, 5.2.2 The Yield of a Parse Tree, 5.2.3 to 5.2.6 the equivalence of inference, derivations and trees); Section 7.2.1, The Size of Parse Trees
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Context-Free Grammars (parse trees and ambiguity); Section 2.3, the proof of the pumping lemma for context-free languages
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 2.2.3, Parse Trees; Section 4.2.4, Parse Trees and Derivations
---

A parse tree of a [context-free grammar](/context-free-grammar/) is an ordered rooted tree that shows how a string comes from a nonterminal: each inner node is a nonterminal, and its children, read from left to right, are the right side of one production of that nonterminal. The leaves, read from left to right, spell the derived string. A parse tree records the structure of a [derivation](/derivation/) and forgets the order of its steps, so it is the usual output of a parser and the input to the construction of an [abstract syntax tree](/abstract-syntax-tree/).

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

**Parse tree.** Let $X \in V \cup \Sigma$. A *parse tree with root $X$* is a finite ordered tree whose nodes carry labels in $V \cup \Sigma \cup \{\varepsilon\}$ such that:

1. the root has the label $X$;
2. each inner node has a label $A \in V$, and if its children have the labels $Y_1, \ldots, Y_k$ from left to right, then either $k \ge 1$, each $Y_i \in V \cup \Sigma$ and $A \to Y_1 \cdots Y_k$ is in $R$, or $k = 1$, $Y_1 = \varepsilon$ and $A \to \varepsilon$ is in $R$;
3. each leaf has a label in $V \cup \Sigma \cup \{\varepsilon\}$, and a leaf with the label $\varepsilon$ is the only child of its parent.

The *yield* of the tree is the string of the labels of its leaves, read from left to right, with each $\varepsilon$ dropped. A tree is *complete* when every leaf has a label in $\Sigma \cup \{\varepsilon\}$, so that the yield is in $\Sigma^*$. A *parse tree of $w$* is a complete tree with root $S$ and yield $w$. When a parser is asked for "the parse tree" of the input, it means this kind.

**Trees and derivations.** For each $A \in V$ and $\alpha \in (V \cup \Sigma)^*$:

$$A \Rightarrow^* \alpha \iff \text{there is a parse tree with root } A \text{ and yield } \alpha.$$

From left to right, induction on the length of the derivation: add the children of the rewritten leaf at each step. From right to left, induction on the height of the tree: if the root has the children $Y_1, \ldots, Y_k$ and the subtree of $Y_i$ has the yield $\alpha_i$, then $A \Rightarrow Y_1 \cdots Y_k \Rightarrow^* \alpha_1 \cdots \alpha_k$ by the induction hypothesis on each subtree. So $L(G)$ is exactly the set of yields of parse trees of $G$. The complete trees with root $S$ are in bijection with the [leftmost derivations](/leftmost-derivation/) from $S$ to terminal strings, and also with the rightmost ones.

**Size.** The *height* of a tree is the number of edges on a longest path from the root to a leaf. Let $r \ge 1$ be the length of the longest right side of $G$. A tree of height $h$ has at most $r^h$ leaves, so its yield has length at most $r^h$. This bound is the first step of the proof of the [pumping lemma for context-free languages](/cfl-pumping-lemma/): a long string needs a tall tree, and a tall tree repeats a nonterminal on some path. In [Chomsky normal form](/chomsky-normal-form/) a parse tree of a string of length $n \ge 1$ has exactly $2n - 1$ inner nodes.

## Examples and non-examples

**A tree.** In the grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid a$, the string $a + a * a$ has one parse tree. In bracket notation, where $[A \ \ldots]$ is a node $A$ and its children:

$$[E \ [E \ [T \ [F \ a]]] \ + \ [T \ [T \ [F \ a]] \ * \ [F \ a]]].$$

It has 8 inner nodes, one for each step of a derivation, and 5 leaves, which spell $a + a * a$. Its height is 4, along $E, E, T, F, a$. The subtree $[T \ [T \ [F \ a]] \ * \ [F \ a]]$ shows that $a * a$ is one operand of $+$: the grammar gives $*$ the higher precedence.

| inner node | production | yield of its subtree |
|---|---|---|
| root $E$ | $E \to E + T$ | $a + a * a$ |
| left $E$ | $E \to T$ | $a$ |
| right $T$ | $T \to T * F$ | $a * a$ |
| each of three $F$ | $F \to a$ | $a$ |

**Two trees for one string.** In $E \to E + E \mid E * E \mid a$, the string $a + a * a$ has the two trees $[E \ [E \ a] \ + \ [E \ [E \ a] * [E \ a]]]$ and $[E \ [E \ [E \ a] + [E \ a]] \ * \ [E \ a]]$. The grammar is [ambiguous](/ambiguity/). The string $a + a + \cdots + a$ with $k$ plus signs has $\frac{1}{k+1}\binom{2k}{k}$ trees, the Catalan number: 1, 2, 5, 14, 42 for $k = 1$ to $5$.

**An empty yield.** In $S \to a S b \mid \varepsilon$, the parse tree of $\varepsilon$ is $[S \ \varepsilon]$, and the parse tree of $ab$ is $[S \ a \ [S \ \varepsilon] \ b]$. The leaf $\varepsilon$ is part of the tree but not of the yield.

**Infinitely many trees.** In $S \to S \mid a$, the string $a$ has the trees $[S \ a]$, $[S \ [S \ a]]$, $[S \ [S \ [S \ a]]]$, and so on. A grammar with a derivation $A \Rightarrow^+ A$ can give one string infinitely many trees, and a parser that wants all trees must then return them in a finite shared form, a [shared packed parse forest](/shared-packed-parse-forest/).

**Non-examples.**

- A node $E$ with the children $E, +, E$ in the grammar $E \to E + T \mid T$: the production $E \to E + E$ is not in $R$, so condition 2 fails.
- A node $S$ with the children $a, \varepsilon, b$: an $\varepsilon$ leaf must be the only child, so condition 3 fails. The right tree for $S \to ab$ has the children $a, b$.
- The tree $[E \ E + T]$ satisfies conditions 1 to 3, but its leaves $E$ and $T$ are nonterminals. It is a parse tree with yield $E + T$, a [sentential form](/sentential-form/), but it is not complete, so it is not a parse tree of any string of terminals.
- An [abstract syntax tree](/abstract-syntax-tree/) such as $+(a, *(a, a))$ is not a parse tree: its node labels are operators, not nonterminals, and it has no node for $F \to a$ or for $E \to T$.

## Related definitions

- [Derivation](/derivation/) and [leftmost derivation](/leftmost-derivation/): the sequences of steps that a tree records; each complete tree has exactly one leftmost and one rightmost derivation.
- [Sentential form](/sentential-form/): the yield of a tree with root $S$ that need not be complete.
- [Ambiguity](/ambiguity/): a grammar is ambiguous when some string has two parse trees.
- [Abstract syntax tree](/abstract-syntax-tree/): the tree that compilers keep after they drop punctuation and chain productions from the parse tree.
- [Shared packed parse forest](/shared-packed-parse-forest/): a graph that stores all parse trees of one string in polynomial space.
- [Parse chart](/parse-chart/): the table of the [CYK algorithm](/cyk-algorithm/) and the [Earley parser](/earley-parser/), from which the parse trees are read out.
- [Handle](/handle/): in a bottom-up parse, the children of the next inner node that the parser builds.

## References
