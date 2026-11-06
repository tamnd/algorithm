---
tag: WJNC3K
kind: theorem
slug: cfg-ambiguity-undecidable
name: Undecidability of CFG ambiguity
area: automata-and-parsing/context-free-parsing
level: advanced
summary: No algorithm decides whether an arbitrary context-free grammar is ambiguous.
prereqs: [ambiguity, post-correspondence-problem, cfl-intersection-undecidable]
see_also: [cfg-ambiguity-problem, inherent-ambiguity, cfg-equivalence-undecidable, lr-k-grammar, unambiguous-nfa, regex-ambiguity-detection, linear-grammar, rice-theorem]
sources:
  - paper: doi:10.1145/321138.321145
    title: David G. Cantor, On the ambiguity problem of Backus systems, Journal of the ACM 9(4) (1962)
    locator: pp. 477 to 479
  - paper: doi:10.1145/368959.368993
    title: Robert W. Floyd, On ambiguity in phrase structure languages, Communications of the ACM 5(10) (1962)
    locator: p. 526
  - paper: doi:10.1016/S0049-237X(08)72023-8
    title: Noam Chomsky and Marcel-Paul Schützenberger, The algebraic theory of context-free languages, in Computer Programming and Formal Systems, Studies in Logic and the Foundations of Mathematics 35 (1963)
    locator: pp. 118 to 161
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.5.2, Undecidability of Ambiguity for CFG's (the list languages and the grammar with S → A | B)
  - paper: doi:10.1145/321312.321318
    title: Seymour Ginsburg and Joseph Ullian, Ambiguity in context free languages, Journal of the ACM 13(1) (1966)
    locator: pp. 62 to 89 (undecidability of inherent ambiguity)
---

## Statement

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. $G$ is [ambiguous](/ambiguity/) if some $w \in \Sigma^*$ has two different parse trees with root $S$. An instance of [Post's correspondence problem](/post-correspondence-problem/) is a pair of lists $x = (x_1, \ldots, x_m)$ and $y = (y_1, \ldots, y_m)$ of strings over $\Sigma$, and a solution is a nonempty index sequence $i_1, \ldots, i_k$ with $x_{i_1} \cdots x_{i_k} = y_{i_1} \cdots y_{i_k}$.

**Theorem (Cantor 1962; Floyd 1962; Chomsky and Schützenberger 1963).** The set of ambiguous context-free grammars is recursively enumerable but not decidable. It is complete for the recursively enumerable sets under many-one reductions, so the set of unambiguous grammars is not even recursively enumerable. This holds already for [linear grammars](/linear-grammar/) over a fixed alphabet of four symbols.

## In plain words

A grammar is ambiguous if some sentence can be built in two different ways. One might hope for a program that reads a grammar and says whether this ever happens. No such program exists.

The proof turns a domino puzzle into a grammar. The grammar has two halves: one builds rows of dominoes read along the top, and the other the same rows read along the bottom, each followed by the list of dominoes used. Each half alone builds every sentence in only one way. A sentence built by both halves, and so in two ways, is exactly a row of dominoes that spells the same string on top and at the bottom. Since no program solves the puzzle, no program detects ambiguity.

What can be done is to search: if a grammar is ambiguous, trying longer and longer sentences eventually finds a witness.

## Proof

The full proof is in [the proof of undecidability](proofs/main.md). It uses the list grammars of the page on [intersection emptiness](/cfl-intersection-undecidable/).

**The reduction.** For an instance $(x, y)$ of PCP, let $1, \ldots, m$ be new index symbols and let $G_{x,y}$ have the productions
$$S \to A \mid B, \qquad A \to x_i\, A\, i \mid x_i\, i, \qquad B \to y_i\, B\, i \mid y_i\, i \qquad (1 \le i \le m).$$
The map $(x, y) \mapsto G_{x,y}$ is computable, and $G_{x,y}$ is linear.

**Each half is unambiguous.** A string derived from $A$ is $x_{i_1} \cdots x_{i_k}\, i_k \cdots i_1$. Its longest suffix of index symbols gives back $i_1, \ldots, i_k$, which fixes every production of the derivation. So $A$ derives each string by only one tree, and so does $B$.

**Two trees come from a solution.** Two different trees of $w$ with root $S$ cannot both start with $S \to A$, since then they would be two trees of $w$ from $A$; nor both with $S \to B$. So one starts with $S \to A$ and the other with $S \to B$, and $w \in L_A \cap L_B$. By the argument on the intersection page, this means that the index suffix of $w$ is a solution. Conversely, a solution $s$ gives the string $x_s \overleftarrow{s} = y_s \overleftarrow{s}$, with one tree through $A$ and one through $B$. So $G_{x,y}$ is ambiguous exactly when the instance has a solution.

**Recursive enumerability.** Parse trees are finite objects. A program that lists all pairs of different parse trees of $G$ with root $S$ and stops when two have the same yield halts exactly when $G$ is ambiguous. Together with the reduction from PCP, which is complete for the recursively enumerable sets, the set of ambiguous grammars is complete, and its complement is not recursively enumerable.

**Fixed alphabet.** PCP stays undecidable over $\Sigma = \{a, b\}$, and the index $i$ can be written as $d\, c^i$ with two new letters $c$ and $d$. The longest suffix in $\{c, d\}^*$ still gives back the index sequence, so the proof works over $\{a, b, c, d\}$. $\blacksquare$

**Example.** For $x = (a, ab)$ and $y = (aa, b)$ the sequence $1, 2$ is a solution, $x_1 x_2 = a \cdot ab = aab = aa \cdot b = y_1 y_2$. The string $aab\,21$ has the two leftmost derivations
$$S \Rightarrow A \Rightarrow a A 1 \Rightarrow a\, ab\, 21, \qquad S \Rightarrow B \Rightarrow aa B 1 \Rightarrow aa\, b\, 21.$$
A script that counts parse trees confirms that $aab21$ is the only string of length at most 7 with two trees, and that with the coding $1 \mapsto dc$, $2 \mapsto dcc$ the only such string of length at most 8 is $aab\,dccdc$.

## Consequences

- **Parser generators cannot check ambiguity exactly.** Tools that accept only unambiguous grammars use a sufficient condition instead, such as the absence of conflicts in an [LR(k)](/lr-k-grammar/) table, which implies unambiguity but rejects many unambiguous grammars. Tools that search for ambiguity, by bounded search or by approximation, give answers in one direction only. See the [ambiguity problem](/cfg-ambiguity-problem/) for these methods.
- **Inherent ambiguity.** Ginsburg and Ullian showed that it is also undecidable whether a context-free *language* is [inherently ambiguous](/inherent-ambiguity/), that is, whether every grammar for it is ambiguous.
- **Related questions.** The same list grammars show that [equivalence](/cfg-equivalence-undecidable/) and [intersection emptiness](/cfl-intersection-undecidable/) are undecidable. Like those, ambiguity is a non-trivial semantic question about an infinite object, though it concerns the grammar and not only its language, so [Rice's theorem](/rice-theorem/) does not apply directly.

## Tightness

- **Finite automata.** For finite automata the corresponding question is decidable in polynomial time: an NFA is [unambiguous](/unambiguous-nfa/) if no string has two accepting runs, and a product of the automaton with itself detects two different runs on the same string. The same holds for [regular expressions](/regex-ambiguity-detection/) and right-linear grammars.
- **Finite languages.** If $L(G)$ is finite, ambiguity is decidable. After removing useless symbols, a cycle $A \Rightarrow^+ A$ makes $G$ ambiguous, since it gives infinitely many trees for some string. Without such a cycle, every string has finitely many trees and there are finitely many strings, so the trees can be counted.
- **Linear and fixed alphabet.** The reduction already gives linear grammars with two nonterminals besides $S$ and four terminal symbols, so restricting to these does not help.

## History

Cantor and Floyd proved independently in 1962 that ambiguity of context-free grammars, then called Backus systems or phrase structure grammars, is undecidable, and Chomsky and Schützenberger gave a proof in 1963. All used Post's correspondence problem. Ginsburg and Ullian (1966) extended the result to inherent ambiguity of languages. The list-language presentation is the one of Hopcroft, Motwani and Ullman.

## References
