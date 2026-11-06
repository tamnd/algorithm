---
tag: DG1K4Y
kind: problem
slug: cfg-finiteness-problem
name: CFG finiteness problem
area: automata-and-parsing/context-free-parsing
level: core
summary: Decide whether a context-free grammar generates finitely many strings.
model: word-ram
complexity:
  vars: {g: the grammar size}
  time: {worst: O(g)}
prereqs: [context-free-grammar, cfg-emptiness-problem, cfl-pumping-lemma, strongly-connected-components]
see_also: [cfg-emptiness-problem, useless-symbol-elimination, dfa-finiteness, chomsky-normal-form, tarjan-scc, cfg-membership-problem, nullable-symbol, parse-tree]
sources:
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, 1979
    locator: Section 6.3, Decision Algorithms for CFL's (Theorem 6.6, emptiness and finiteness, by a cycle in the graph of a grammar in Chomsky normal form)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.2, The Pumping Lemma for Context-Free Languages (7.2.1 The Size of Parse Trees), and Section 7.1.2, Eliminating Useless Symbols
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.5, Strongly connected components
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2) (1972)
    locator: pp. 146 to 160 (strongly connected components in linear time)
---

The CFG finiteness problem asks whether a [context-free grammar](/context-free-grammar/) generates only finitely many strings. It is decidable in time linear in the size of the grammar. After the [useless symbols](/useless-symbol-elimination/) are removed, the language is infinite exactly when some nonterminal can derive itself with a nonempty string beside it, $A \Rightarrow^+ x A y$ with $xy \ne \varepsilon$, and this is a test for a cycle in a graph of the nonterminals. It is the context-free analogue of [DFA finiteness](/dfa-finiteness/), and its proof is the same idea as the [pumping lemma](/cfl-pumping-lemma/).

## In plain words

A grammar has rules that build strings from pieces. If some piece can, through a chain of rules, contain a copy of itself together with at least one letter, you can repeat that chain as often as you like. Each repetition makes a longer string, so the grammar describes infinitely many strings.

If no piece can do that, every useful way to build a string has bounded depth, so there are only finitely many strings.

Two cautions. A piece that cannot finish at all, or that the start symbol never uses, must be thrown away first, because its loops build nothing. And a loop that only adds pieces that can be empty, such as "a piece is an empty thing followed by the same piece", does not make anything longer.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

**Input.** A context-free grammar $G$.

**Output.** "Finite" if $L(G)$ is a finite set, and "infinite" otherwise. The empty language counts as finite.

**The criterion.** Let $G$ have no useless symbols: each nonterminal is reachable from $S$ and derives some terminal string. Call a symbol *nonempty* if it is a terminal or a nonterminal that derives some string other than $\varepsilon$. The *growth graph* has the nonterminals as vertices and an edge $A \to B$ for each occurrence of $B$ in the right side of a production of $A$. The edge is *growing* if another symbol of that right side is nonempty. Then

$$L(G) \text{ is infinite} \iff \text{some growing edge lies on a cycle of the growth graph.}$$

*Proof.* If a growing edge $A \to B$ from $A \to \alpha B \beta$ lies on a cycle, the cycle gives $B \Rightarrow^* \mu A \nu$, so $A \Rightarrow^+ \alpha \mu A \nu \beta$, and some symbol of $\alpha\beta$ derives a nonempty string. Every symbol derives some terminal string, so $A \Rightarrow^+ x A y$ with $x, y$ terminal strings and $xy \ne \varepsilon$. Since $S \Rightarrow^* u A v$ and $A \Rightarrow^* z$, the strings $u x^i z y^i v$ for $i \ge 0$ are in $L(G)$ and have distinct lengths.

Conversely, assume that no growing edge is on a cycle. Take any string of $L(G)$ and a parse tree of it. If a path of the tree has two nodes with the same label $A$, the path between them follows a cycle of the growth graph, so none of its edges is growing, and every subtree that hangs off this part of the path has an empty yield. Replacing the subtree of the upper $A$ by that of the lower one keeps the yield. Repeat until no path repeats a label. The result is a parse tree of the same string with height at most $|V|$ and at most $m$ children per node, where $m$ is the longest right side. There are finitely many such trees, so $L(G)$ is finite. $\square$

## Variants

- **Chomsky normal form.** If $G$ is in [Chomsky normal form](/chomsky-normal-form/) without useless symbols, every edge is growing, because the other symbol of $A \to BC$ derives a nonempty string. So $L(G)$ is infinite exactly when the graph has any cycle. This is the textbook test of Hopcroft and Ullman, Theorem 6.6.
- **The size of a finite language.** When $L(G)$ is finite, every string has length at most $m^{|V|}$, from the bounded trees above. The language can still be huge: $A_1 \to A_2 A_2$, $\ldots$, $A_{k-1} \to A_k A_k$, $A_k \to a \mid b$ generates all $2^{2^{k-1}}$ strings of length $2^{k-1}$ with a grammar of size $3k + 1$.
- **The longest string.** For a finite language, the length of a longest string is computed by dynamic programming over the growth graph in topological order, $\lambda(A) = \max$ over $A \to X_1 \cdots X_k$ of $\sum_i \lambda(X_i)$, in $O(|G|)$ time.
- **Counting.** For a finite language given by an unambiguous grammar, the number of strings is computed the same way with sums and products. With ambiguity, counting the distinct strings is harder.
- **Pushdown automata.** For a [pushdown automaton](/pushdown-automaton/), convert it to a grammar first.
- **Regular languages.** For a finite automaton the same question is [DFA finiteness](/dfa-finiteness/), a cycle on a path from the start to an accepting state.

## Examples

| grammar | answer | why |
|---|---|---|
| $S \to a S b \mid \varepsilon$ | infinite | the edge $S \to S$ is growing, because of $a$ |
| $S \to A B$, $A \to a \mid b$, $B \to c \mid d$ | finite, 4 strings | the graph has no cycle |
| $S \to A S \mid b$, $A \to \varepsilon$ | finite, $\{b\}$ | the cycle $S \to S$ is not growing: $A$ is not nonempty |
| $S \to A \mid b$, $A \to S$ | finite, $\{b\}$ | the cycle $S \to A \to S$ uses unit productions only |
| $S \to a \mid B S$, $B \to C C$, $C \to c \mid \varepsilon$ | infinite | $B$ is nonempty, so the edge $S \to S$ is growing |
| $S \to a \mid C$, $C \to C D$, $D \to d D$ | finite, $\{a\}$ | $D$ and then $C$ derive no terminal string; the loops are useless |
| $S \to S S \mid \varepsilon$ | finite, $\{\varepsilon\}$ | $S$ is not nonempty, so $S \to SS$ is not growing |

The third, fourth and last rows show why a plain test for a cycle is wrong: each of these grammars has a cycle and a finite language. The sixth row shows why the useless symbols must go first.

## Known algorithms

- **Linear time.** Compute the generating symbols ([emptiness](/cfg-emptiness-problem/)), drop the productions that use other symbols, compute the symbols reachable from $S$ and drop the rest. If $S$ is gone, the language is empty. Compute the nonempty nonterminals by a work list: $A$ is nonempty when some production of $A$ has a terminal or a nonempty nonterminal. For each production, count its nonempty symbols, which tells which of its edges are growing. Find the [strongly connected components](/strongly-connected-components/) of the growth graph with [Tarjan's algorithm](/tarjan-scc/), and answer "infinite" when a growing edge joins two vertices of one component. Each step takes $O(|G|)$ time.
- **Through Chomsky normal form.** Convert to [Chomsky normal form](/chomsky-normal-form-conversion/), remove useless symbols, and look for any cycle. Correct, but the conversion takes $O(|G|^2)$ time.
- **Through the pumping lemma.** $L(G)$ is infinite exactly when it has a string with length between $p$ and $2p$, for a pumping length $p$, and this can be tested by [membership](/cfg-membership-problem/) of all such strings. This is the classical proof of decidability, of exponential cost.

## Bounds

**Upper bound.** $O(|G|)$ time on a word RAM, by the linear algorithm. A lower bound of $\Omega(|G|)$ holds because each production can be the one that creates a growing cycle.

**P-hardness.** Emptiness reduces to infiniteness in logarithmic space: for a new start symbol $S_0$ and a new nonterminal $X$, the grammar with $S_0 \to S X$, $X \to a X \mid \varepsilon$ added has an infinite language exactly when $L(G) \ne \emptyset$. [Emptiness](/cfg-emptiness-problem/) is P-complete, so finiteness is P-complete too, and the two problems have the same complexity.

## Reductions

- **From emptiness**, as above, in logarithmic space.
- **To emptiness and strongly connected components.** The linear algorithm uses the generating symbols and one search for components.
- **To DFA finiteness**, for a grammar that is right-linear: it is a finite automaton, and the growth graph is its transition graph.

## Applications

- **Bounded languages of formats.** A grammar of a file header or a command set is meant to be finite; the test checks that no rule allows unbounded repetition by mistake.
- **Test generation.** A generator that lists all strings of a grammar stops only when the language is finite, and the test tells in advance whether listing is possible.
- **A step of other algorithms.** The bounded trees of a finite language give its longest string and, for an unambiguous grammar, its size, for example to size a buffer that must hold any string of the language.

## References
