---
tag: 658DF6
kind: theorem
slug: cfg-equivalence-undecidable
name: Undecidability of CFG equivalence
area: automata-and-parsing/context-free-parsing
level: advanced
summary: No algorithm decides whether two context-free grammars generate the same language.
prereqs: [cfl-intersection-undecidable, post-correspondence-problem, context-free-grammar]
see_also: [cfg-equivalence-problem, cfg-ambiguity-undecidable, dfa-equivalence, nfa-universality, regex-equivalence, deterministic-context-free-language, rice-theorem, halting-problem]
sources:
  - paper: doi:10.1524/stuf.1961.14.14.143
    title: Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)
    locator: pp. 143 to 172
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.5.3, The Complement of a List Language, and Section 9.5.4, Other Undecidable Problems About CFG's
  - paper: doi:10.1090/psapm/019/0235938
    title: Juris Hartmanis, Context-free languages and Turing machine computations, Proceedings of Symposia in Applied Mathematics 19 (1967)
    locator: pp. 42 to 51 (invalid computations of a Turing machine form a context-free language)
  - paper: doi:10.1016/S0304-3975(00)00285-1
    title: Géraud Sénizergues, L(A)=L(B)? decidability results from complete formal systems, Theoretical Computer Science 251(1-2) (2001)
    locator: pp. 1 to 166 (equivalence of deterministic pushdown automata is decidable)
---

## Statement

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. Two grammars are *equivalent* if they generate the same language.

**Theorem.** Each of the following problems is undecidable, for context-free grammars $G, G_1, G_2$ over a terminal alphabet $\Delta$ and a regular expression $E$:

1. *Universality:* is $L(G) = \Delta^*$?
2. *Equivalence:* is $L(G_1) = L(G_2)$?
3. *Inclusion:* is $L(G_1) \subseteq L(G_2)$?
4. *Equality with a regular language:* is $L(G) = L(E)$?
5. *Regular inclusion:* is $L(E) \subseteq L(G)$?

Each is complete for the co-recursively-enumerable sets: its complement is recursively enumerable, because a string that witnesses the difference can be found by search, and every co-recursively-enumerable set reduces to it. Universality is undecidable already over the fixed alphabet $\{a, b, c, d\}$, so equivalence is undecidable even when $G_2$ is one fixed grammar for $\{a, b, c, d\}^*$.

## In plain words

Two grammars may look very different and still describe the same strings. A program that compares any two grammars and says whether their languages are equal would be very useful, for example to check that rewriting a grammar for a parser did not change the language. No such program exists.

Even the simplest case is impossible: deciding whether a grammar generates every string at all. The proof builds, from a domino puzzle, a grammar for every string that is *not* a solution of the puzzle. That grammar generates every string exactly when the puzzle has no solution, and no program can decide that.

A wrong answer can be refuted by finding a string in one language but not the other, so the search for a difference always ends when there is one. What cannot be done is to confirm that there is none.

## Proof

The full proof is in [the proof of undecidability](proofs/main.md). It extends the list languages used for [intersection emptiness](/cfl-intersection-undecidable/).

**The list languages.** For an instance $x = (x_1, \ldots, x_m)$, $y = (y_1, \ldots, y_m)$ of [Post's correspondence problem](/post-correspondence-problem/) over $\Sigma$, with new index symbols $I = \{1, \ldots, m\}$ and $\Delta = \Sigma \cup I$, let
$$L_x = \{ x_{i_1} \cdots x_{i_k}\, i_k \cdots i_1 : k \ge 1 \}, \qquad L_y = \{ y_{i_1} \cdots y_{i_k}\, i_k \cdots i_1 : k \ge 1 \}.$$
Then $L_x \cap L_y \ne \emptyset$ exactly when the instance has a solution.

**The complement of a list language is context-free.** A string $w \notin L_x$ either is not in $\Sigma^* I^+$, which is a regular condition, or is $w = u\, i_k \cdots i_1$ with $u \in \Sigma^*$ and $u \ne x_{i_1} \cdots x_{i_k}$. In the second case let $r$ be the number of blocks $x_{i_1}, \ldots, x_{i_r}$ that match a prefix of $u$. Either all $k$ match and $u$ has a nonempty rest, or block $r + 1$ fails, and then the rest of $u$ does not start with $x_{i_{r+1}}$. The grammar
$$D \to x_i\, D\, i \mid Y \mid Z_i\, i \quad (i \in I), \qquad Y \Rightarrow^* \Sigma^+, \qquad Z_i \Rightarrow^* (\Sigma^* \setminus x_i \Sigma^*)\, I^*,$$
generates exactly these strings: $D \to x_i D i$ matches one block with its index, $Y$ is a nonempty rest, and $Z_i\, i$ is a failed block followed by arbitrary indices. $Y$ and $Z_i$ generate regular languages, so they have right-linear grammars of size $O(|x_i| \cdot |\Sigma| + m)$. So $\overline{L_x} = (\Delta^* \setminus \Sigma^* I^+) \cup L(D)$ is context-free, with a grammar computable from $x$.

**The reduction.** Let $G_{\overline{x}}$ and $G_{\overline{y}}$ be these grammars for $\overline{L_x}$ and $\overline{L_y}$, and let $G$ be their union, $S \to S_{\overline{x}} \mid S_{\overline{y}}$. Then
$$L(G) = \overline{L_x} \cup \overline{L_y} = \overline{L_x \cap L_y},$$
so $L(G) = \Delta^*$ exactly when the instance has no solution. Since PCP is undecidable and complete for the recursively enumerable sets, universality is undecidable and complete for the co-recursively-enumerable sets. Problems 2 to 5 follow by taking $G_2$ or $E$ to describe $\Delta^*$: universality is the special case $L(G_1) = \Delta^*$, or $\Delta^* \subseteq L(G)$. Coding index $i$ as $d c^i$ fixes the alphabet to $\{a, b, c, d\}$. $\blacksquare$

**Example.** For $x = (a, ab)$ and $y = (aa, b)$ over $\Delta = \{a, b, 1, 2\}$, a script checks all 21845 strings of length at most 7: exactly one is missing from $\overline{L_x} \cup \overline{L_y}$, namely $aab21$, which encodes the solution $1, 2$. So this $G$ is not universal, and $aab21$ is the witness that a search for a difference would find. A second script compares the grammar for $\overline{L_x}$ with the complement of $L_x$ on all strings of length at most 5 for 40 random lists $x$, with no difference.

## Consequences

- **Grammar engineering.** There is no general tool that proves two grammars equivalent. Practical tools test equivalence on many generated strings, which can only find differences, or restrict the grammars to a class where equivalence is decidable.
- **Minimization.** No algorithm finds a smallest grammar for the language of a given grammar. If $L(G) = \Delta^*$, a smallest grammar for it is no larger than a fixed grammar for $\Delta^*$, and the grammars up to that size with language $\Delta^*$ form a finite list; checking the output against this list would decide universality.
- **Regularity.** It is also undecidable whether $L(G)$ is regular. If the instance has no solution, $L(G) = \Delta^*$ is regular. If $s$ is a solution, then $\overline{L(G)} \cap x_s^* \overleftarrow{s}^* = \{ x_s^j\, \overleftarrow{s}^j : j \ge 1 \}$, where $\overleftarrow{s}$ is the reversed index sequence, because the index suffix fixes the sequence $s^j$. This language is not regular, so neither is $L(G)$.
- **Pushdown automata.** All five problems are undecidable for nondeterministic [pushdown automata](/cfg-pda-equivalence/), since grammars and automata convert into each other.
- **The problem page.** The [equivalence problem](/cfg-equivalence-problem/) collects the decidable special cases and the practical approaches.

## Tightness

- **Deterministic languages.** Equivalence of [deterministic pushdown automata](/deterministic-context-free-language/) is decidable, by Sénizergues, a result for which he received the Gödel Prize in 2002. The list languages $L_x$ and $L_y$ are deterministic, but their complements are joined by a union, which leaves the deterministic class.
- **Inclusion stays undecidable for deterministic languages.** $L_x \cap L_y = \emptyset$ is the same as $L_x \subseteq \overline{L_y}$, and $\overline{L_y}$ is also deterministic, since deterministic languages are closed under complement. So inclusion of deterministic languages is undecidable while their equivalence is decidable.
- **Regular languages.** Equivalence of finite automata is decidable, by [DFA equivalence](/dfa-equivalence/), and universality of [NFAs](/nfa-universality/) is decidable but PSPACE-complete. The step from one stack to none changes undecidable to decidable.
- **Inclusion in a regular language.** $L(G) \subseteq L(E)$ is decidable: it says $L(G) \cap \overline{L(E)} = \emptyset$, which is an [emptiness](/cfg-emptiness-problem/) question after the [product construction](/cfl-closure-properties/). The other direction, $L(E) \subseteq L(G)$, is undecidable by part 5.

## History

Bar-Hillel, Perles and Shamir proved in 1961 that equivalence and inclusion of context-free grammars are undecidable, by reductions from Post's correspondence problem. Hartmanis (1967) gave a second proof: the strings that are *not* valid computations of a Turing machine form a context-free language, which is universal exactly when the machine accepts nothing. The proof here, with the complement of the list language, follows Hopcroft, Motwani and Ullman. Sénizergues announced the decidability of equivalence for deterministic pushdown automata in 1997 and published the full proof in 2001.

## References
