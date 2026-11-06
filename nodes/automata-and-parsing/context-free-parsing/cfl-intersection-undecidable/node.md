---
tag: AFJZ2E
kind: theorem
slug: cfl-intersection-undecidable
name: Undecidability of CFL intersection
area: automata-and-parsing/context-free-parsing
level: advanced
summary: The intersection of two context-free languages is not necessarily context-free, and emptiness of intersections is undecidable.
prereqs: [post-correspondence-problem, context-free-grammar, cfl-closure-properties]
see_also: [cfg-equivalence-undecidable, cfg-ambiguity-undecidable, cfl-reachability, regular-language-intersection, deterministic-context-free-language, linear-grammar, halting-problem, many-one-reducibility]
sources:
  - paper: doi:10.1524/stuf.1961.14.14.143
    title: Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)
    locator: pp. 143 to 172
  - paper: doi:10.1090/S0002-9904-1946-08555-9
    title: Emil L. Post, A variant of a recursively unsolvable problem, Bulletin of the American Mathematical Society 52(4) (1946)
    locator: pp. 264 to 268
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.5, Other Undecidable Problems (9.5.2 Undecidability of Ambiguity for CFG's, the list languages L_A and L_B, and 9.5.3 The Complement of a List Language)
  - paper: doi:10.1145/345099.345137
    title: Thomas Reps, Undecidability of context-sensitive data-dependence analysis, ACM Transactions on Programming Languages and Systems 22(1) (2000)
    locator: pp. 162 to 186
---

## Statement

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. An instance of [Post's correspondence problem](/post-correspondence-problem/) (PCP) is a pair of lists $x = (x_1, \ldots, x_m)$ and $y = (y_1, \ldots, y_m)$ of nonempty strings over $\Sigma$; a *solution* is a nonempty sequence $i_1, \ldots, i_k$ of indices with $x_{i_1} \cdots x_{i_k} = y_{i_1} \cdots y_{i_k}$.

**Theorem.**

1. The intersection of two context-free languages need not be context-free.
2. The *intersection emptiness problem*, given context-free grammars $G_1$ and $G_2$, decide whether $L(G_1) \cap L(G_2) = \emptyset$, is undecidable. Its complement, nonemptiness, is recursively enumerable and complete for the recursively enumerable sets under [many-one reductions](/many-one-reducibility/).
3. It is also undecidable whether $L(G_1) \cap L(G_2)$ is infinite.
4. Both stay undecidable when $G_1$ and $G_2$ are [linear](/linear-grammar/), unambiguous, and generate [deterministic context-free languages](/deterministic-context-free-language/).

## In plain words

Two grammars can each check one thing about a string, but nothing can check both at once. Asking whether some string satisfies both grammars is therefore a hard question, and in fact no algorithm can answer it for all pairs of grammars.

The reason is a puzzle with dominoes. Each domino has a top string and a bottom string, and the question is whether some row of dominoes spells the same string on top and at the bottom. No algorithm solves this puzzle in general. One grammar describes all rows read along the top, and the other all rows read along the bottom, each followed by the numbers of the dominoes used. A string in both languages is exactly a row that solves the puzzle.

## Proof

Part 1 is shown on the [closure properties](/cfl-closure-properties/) page: $\{a^i b^i c^j\} \cap \{a^i b^j c^j\} = \{a^n b^n c^n\}$, which is not context-free by the [pumping lemma](/cfl-pumping-lemma/). The full proof of parts 2 to 4 is in [the proof of undecidability](proofs/main.md). Its outline:

**The list grammars.** Let $1, \ldots, m$ be new *index symbols*, not in $\Sigma$. For the lists $x$ and $y$ let
$$G_x:\ A \to x_i\, A\, i \mid x_i\, i \quad (1 \le i \le m), \qquad G_y:\ B \to y_i\, B\, i \mid y_i\, i \quad (1 \le i \le m).$$
Then $L(G_x) = \{ x_{i_1} \cdots x_{i_k}\, i_k \cdots i_1 : k \ge 1 \}$, and likewise for $G_y$. Each grammar has size $O(\sum_i |x_i| + m)$ and is linear.

**Reading back the indices.** A string $w \in L(G_x)$ ends with a maximal block of index symbols, $i_k \cdots i_1$, which determines the sequence $i_1, \ldots, i_k$; the part before it is then $x_{i_1} \cdots x_{i_k}$. The same holds for $G_y$. So $w \in L(G_x) \cap L(G_y)$ exactly when $w = x_{i_1} \cdots x_{i_k}\, i_k \cdots i_1$ for a sequence with $x_{i_1} \cdots x_{i_k} = y_{i_1} \cdots y_{i_k}$, that is, a solution.

**The reduction.** The map from $(x, y)$ to $(G_x, G_y)$ is computable, and $L(G_x) \cap L(G_y) \ne \emptyset$ exactly when the instance has a solution. PCP is undecidable and complete for the recursively enumerable sets, so intersection emptiness is undecidable. A solution repeated twice is again a solution, so the intersection is infinite exactly when it is nonempty, which gives part 3. Nonemptiness is recursively enumerable: list all strings and test each for membership in both grammars with the [CYK algorithm](/cyk-algorithm/).

**Restricted grammars.** $G_x$ and $G_y$ are linear, they are unambiguous because the index block fixes the derivation, and a deterministic pushdown automaton accepts $L(G_x)$: it pushes the symbols of $\Sigma$, and on each index symbol $i$ it pops $|x_i|$ symbols and checks that they spell $x_i$ backwards. This gives part 4. $\blacksquare$

**Example.** Take $x = (a, abaaa, ab)$ and $y = (aaa, ab, b)$ over $\Sigma = \{a, b\}$. The sequence $2, 1, 1, 3$ is a solution:
$$x_2 x_1 x_1 x_3 = abaaa \cdot a \cdot a \cdot ab = abaaaaaab = ab \cdot aaa \cdot aaa \cdot b = y_2 y_1 y_1 y_3.$$
So $abaaaaaab\,3112$ is in both $L(G_x)$ and $L(G_y)$. A script finds that $2, 1, 1, 3$ is the only solution of length at most 4, confirms that the string is in both languages, and checks on 60 random instances with lists of up to 3 strings of length at most 3 that the strings of length at most 7 in $L(G_x) \cap L(G_y)$ are exactly the encodings of solutions.

## Consequences

- **Equivalence and universality.** The complement of $L(G_x)$ is also context-free, so $\overline{L(G_x)} \cup \overline{L(G_y)}$ is context-free and equals the set of all strings exactly when the instance has no solution. So it is undecidable whether $L(G) = \Sigma^*$, and whether two grammars are [equivalent](/cfg-equivalence-undecidable/), and whether $L(G_1) \subseteq L(G_2)$.
- **Ambiguity.** The grammar $S \to A \mid B$ with the productions of $G_x$ and $G_y$ is [ambiguous](/cfg-ambiguity-undecidable/) exactly when the instance has a solution, since each of $G_x$ and $G_y$ is unambiguous.
- **Pushdown automata.** Emptiness of the intersection of two pushdown automata is undecidable, even for deterministic ones; a product of two stacks would be a [Turing machine](/turing-machine/).
- **Program analysis.** In [CFL reachability](/cfl-reachability/), one context-free language, such as matched calls and returns, gives a cubic algorithm. Asking for paths that are matched for two languages at once, such as calls and returns together with stores and loads of fields, is an intersection problem, and Reps showed that this context-sensitive and structure-sensitive analysis is undecidable.

## Tightness

- **One side regular.** If one language is regular, $L(G) \cap R$ is context-free by the product construction of the [closure properties](/cfl-closure-properties/), and its emptiness is decided by the [emptiness test](/cfg-emptiness-problem/) in polynomial time.
- **One side finite.** If $L(G_2)$ is finite, test each of its strings for membership in $L(G_1)$.
- **One letter.** Over a one-letter alphabet every context-free language is regular, by [Parikh's theorem](/parikh-theorem/), and the problem is decidable.
- **Two languages are enough.** The list languages are linear and deterministic, so no restriction to these classes helps. What helps is giving up one of the two stacks: a regular language, a finite one, or one over one letter.

## History

Bar-Hillel, Perles and Shamir proved in 1961 that emptiness of the intersection of two context-free languages, and several related questions, are undecidable, by reductions from Post's correspondence problem, which Post had shown undecidable in 1946. The presentation with the list languages $L_A$ and $L_B$ is the one of Hopcroft, Motwani and Ullman. Reps (2000) carried the result to program analysis.

## References
