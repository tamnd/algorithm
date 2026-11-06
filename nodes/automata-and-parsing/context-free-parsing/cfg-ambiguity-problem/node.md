---
tag: K1M8FW
kind: problem
slug: cfg-ambiguity-problem
name: CFG ambiguity problem
aliases:
- grammar ambiguity decision
area: automata-and-parsing/context-free-parsing
level: core
summary: Decide whether a given context-free grammar is ambiguous; undecidable in general.
prereqs: [ambiguity, context-free-grammar, parse-tree, post-correspondence-problem]
see_also: [cfg-ambiguity-undecidable, inherent-ambiguity, lr-k-grammar, unambiguous-nfa, regex-ambiguity-detection, cfg-equivalence-problem, recursively-enumerable-language, glr-parsing]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.5.2, Undecidability of Ambiguity for CFG's (the reduction from Post's correspondence problem with the list grammars)
  - paper: doi:10.1145/321138.321145
    title: David G. Cantor, On the ambiguity problem of Backus systems, Journal of the ACM 9(4) (1962)
    locator: pp. 477 to 479 (the problem is undecidable)
  - paper: doi:10.1145/368959.368993
    title: Robert W. Floyd, On ambiguity in phrase structure languages, Communications of the ACM 5(10) (1962)
    locator: p. 526 (an independent proof of undecidability)
  - paper: doi:10.1145/321312.321318
    title: Seymour Ginsburg and Joseph Ullian, Ambiguity in context free languages, Journal of the ACM 13(1) (1966)
    locator: pp. 62 to 89 (inherent ambiguity of a language is undecidable too)
  - paper: doi:10.1007/978-3-540-73420-8_60
    title: Sylvain Schmitz, Conservative ambiguity detection in context-free grammars, ICALP 2007, Lecture Notes in Computer Science 4596
    locator: pp. 692 to 703 (approximations that never miss an ambiguity)
  - paper: doi:10.1007/978-3-540-70583-3_34
    title: Roland Axelsson, Keijo Heljanko and Martin Lange, Analyzing context-free grammars using an incremental SAT solver, ICALP 2008, Lecture Notes in Computer Science 5126
    locator: pp. 410 to 422 (search for ambiguous strings up to a length bound)
  - paper: doi:10.1016/j.scico.2009.11.002
    title: Claus Brabrand, Robert Giegerich and Anders Møller, Analyzing ambiguity of context-free grammars, Science of Computer Programming 75(3) (2010)
    locator: pp. 176 to 191 (vertical and horizontal ambiguity, checked on a regular approximation)
---

The CFG ambiguity problem asks whether a [context-free grammar](/context-free-grammar/) is [ambiguous](/ambiguity/), that is, whether some string has two different parse trees. No algorithm decides it: Cantor, Floyd, and Chomsky and Schützenberger proved in 1962 and 1963 that it is [undecidable](/cfg-ambiguity-undecidable/), by a reduction from [Post's correspondence problem](/post-correspondence-problem/). Ambiguity can be confirmed by finding a witness, so the problem is semi-decidable, and practical tools either search for witnesses up to a length bound or prove unambiguity by a sufficient condition such as being [LR(k)](/lr-k-grammar/).

## In plain words

A grammar is ambiguous when one string can be built in two different ways. For a grammar of arithmetic, "1 + 2 * 3" could mean adding first or multiplying first, which is why compilers care.

If a grammar is ambiguous, you can find out: try the strings one by one, count the ways to build each, and stop at the first string with two. If it is not ambiguous, this search runs forever, and there is no general shortcut. Any program that claims to answer the question for every grammar is wrong on some grammar.

So in practice you ask a weaker question. Either "is there an ambiguous string shorter than 20 letters?", which a search can answer, or "does the grammar pass a test that only unambiguous grammars pass?", which may say "don't know".

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $n$ is the length of a string, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

**Input.** A context-free grammar $G$.

**Output.** "Ambiguous" if some $w \in L(G)$ has two different [parse trees](/parse-tree/) with root $S$, and "unambiguous" otherwise.

Two parse trees of $w$ are different exactly when the two [leftmost derivations](/leftmost-derivation/) they give are different, so the problem can be stated with leftmost derivations as well. Only strings of $L(G)$ count: a nonterminal that is not reachable from $S$, or derives no terminal string, cannot make the grammar ambiguous.

**Status.** The set of ambiguous grammars is recursively enumerable but not recursive. It is enumerable because, for each $w$ in order of length, the number of parse trees of $w$ can be computed, capped at 2, by the dynamic programming of [CYK](/cyk-algorithm/) over the substrings of $w$. A grammar has a string with infinitely many trees exactly when some useful nonterminal satisfies $A \Rightarrow^+ A$, which the same table detects. It is not recursive by the reduction below, and so the set of unambiguous grammars is not even recursively enumerable.

## Variants

- **Inherent ambiguity.** Given $G$, decide whether *every* grammar for $L(G)$ is ambiguous. This is a question about the language, and it is undecidable too (Ginsburg and Ullian). The language $\{a^i b^j c^k : i = j \text{ or } j = k\}$ is [inherently ambiguous](/inherent-ambiguity/).
- **Bounded ambiguity.** Given $G$ and a bound $k$, decide whether some string of length at most $k$ has two parse trees. This is decidable, since there are finitely many strings, and the search can be done by a SAT solver, as in the CFGAnalyzer tool of Axelsson, Heljanko and Lange.
- **Degree of ambiguity.** Decide whether the number of parse trees of strings of length $n$ is bounded by a constant, by a polynomial in $n$, or grows exponentially. For grammars the bound 1 is already undecidable; for [finite automata](/unambiguous-nfa/) these questions are decidable.
- **Restricted grammars.** For a right-linear grammar, which is a finite automaton, ambiguity is decidable in polynomial time: trim the automaton, form its product with itself, and look for a reachable and co-reachable pair of different states. For [regular expressions](/regex-ambiguity-detection/) the same holds. For linear grammars, with at most one nonterminal on each right side, it is still undecidable, because the grammars of the reduction are linear.
- **Fixed lookahead.** Deciding whether $G$ is LR($k$) for a given $k$ is decidable by building the [LR(k)](/lr-k-grammar/) table, and an LR($k$) grammar is unambiguous. Deciding whether $G$ is LR($k$) for some $k$ is undecidable (Knuth 1965).

## Examples

| grammar | ambiguous | shortest witness | trees |
|---|---|---|---|
| $E \to E + E \mid a$ | yes | $a + a + a$ | 2 |
| $S \to S S \mid a b$ | yes | $ababab$ | 2 |
| $S \to a S \mid S a \mid a$ | yes | $aa$ | 2 |
| $S \to a S b \mid a S \mid \varepsilon$ | yes | $aab$ | 2 |
| $S \to A \mid a$, $A \to a$ | yes | $a$ | 2 |
| $S \to S \mid a$ | yes | $a$ | infinitely many |
| $S \to a S b \mid \varepsilon$ | no | | 1 for every string |

In the first two rows, $a + a + \cdots + a$ with $k$ plus signs and $(ab)^{k+1}$ have $C_k$ parse trees, the Catalan numbers $1, 1, 2, 5, 14$ for $k = 0, \ldots, 4$. The fourth row is a grammar for $\{a^i b^j : i \ge j\}$ whose second rule can be used before or after the first: $aab$ is derived as $a(a\,\varepsilon\,b)$ and as $(a(a\,\varepsilon)b)$. Replacing it by $S \to a S b \mid T$, $T \to a T \mid \varepsilon$ removes the ambiguity, because then every $a$ that is matched with a $b$ comes first.

**A grammar from Post's correspondence problem.** Take the lists $x = (a, ab)$ and $y = (aa, b)$ and index symbols $1, 2$. The grammar
$$S \to A \mid B, \quad A \to a A 1 \mid ab A 2 \mid a 1 \mid ab\,2, \quad B \to aa B 1 \mid b B 2 \mid aa 1 \mid b 2$$
is unambiguous inside $A$ and inside $B$, because the index symbols at the end name the productions used. A string has two trees only if $A$ and $B$ both derive it. The index sequence $1, 2$ gives $x_1 x_2 = aab = y_1 y_2$, so $aab21$ is derived from both, and it is the only ambiguous string up to length 6.

## Known algorithms

No algorithm decides the problem. The methods in use answer weaker questions.

- **Semi-decision.** List the strings in order of length and count the parse trees of each, capped at 2, by a CYK-style table. It stops with a witness when $G$ is ambiguous and runs forever otherwise. For a string of length $n$ the count costs $O(n^3 |G|)$ time after binarization.
- **Bounded search.** Stop the semi-decision at length $k$, or encode "two different trees of the same string of length $k$" in propositional logic and call a SAT solver (Axelsson, Heljanko and Lange). Either answers "ambiguous with this witness" or "no witness up to $k$".
- **Sufficient conditions for unambiguity.** If the [LR(1)](/canonical-lr-parsing/), [LALR(1)](/lalr-parsing/) or [LL(1)](/ll1-parsing/) table has no conflict, the grammar is unambiguous. A conflict says nothing: many unambiguous grammars are not LR($k$) for any $k$, such as $S \to a S a \mid b S b \mid a \mid b \mid \varepsilon$ for the palindromes.
- **Conservative approximation.** Schmitz builds an approximation of the pairs of positions in parse trees that can be confused, and reports "unambiguous" only when no confusion is possible; otherwise it reports a possible ambiguity, which may be spurious. Brabrand, Giegerich and Møller check two local conditions on productions with the same left side, again against a regular approximation of the language.

## Bounds

**Undecidability.** Post's correspondence problem reduces to ambiguity, so ambiguity is undecidable, even for linear grammars over a fixed alphabet. The full proof is on the page [ambiguity of CFGs is undecidable](/cfg-ambiguity-undecidable/).

**Degree.** Ambiguity is complete for the recursively enumerable sets: it is in the class by the semi-decision, and Post's correspondence problem, which is complete for the class, reduces to it. Its complement is complete for the co-enumerable sets.

**Bounded version.** For a bound $k$, enumeration checks fewer than $(|\Sigma| + 1)^{k+1}$ strings, each in time polynomial in $k$ and $|G|$, so the bounded problem is decidable in time exponential in $k$.

## Reductions

- **From Post's correspondence problem.** For lists $x_1, \ldots, x_m$ and $y_1, \ldots, y_m$ over $\Sigma$, and new symbols $1, \ldots, m$, the grammar $S \to A \mid B$, $A \to x_i A\, i \mid x_i\, i$, $B \to y_i B\, i \mid y_i\, i$ is ambiguous exactly when the instance has a solution.
- **To the emptiness of an intersection.** In the grammar above, the ambiguity is the nonemptiness of $L(A) \cap L(B)$, and this is the same reduction that shows [intersection emptiness undecidable](/cfl-intersection-undecidable/).
- **From halting.** Through Post's correspondence problem, a grammar can be built from a Turing machine and an input so that it is ambiguous exactly when the machine halts; this is how the [halting problem](/halting-problem/) is turned into a question about grammars.

## Applications

- **Parser generators.** Yacc and Bison report shift-reduce and reduce-reduce conflicts, which flag possible ambiguity, and resolve them by precedence declarations; the user must decide whether a conflict is a real ambiguity.
- **Language design.** The [dangling else](/ambiguity/) and the precedence of operators are ambiguities that a language definition must settle, and bounded search finds such witnesses in grammars of real languages.
- **Generalized parsing.** A [GLR](/glr-parsing/) or [Earley](/earley-parser/) parser accepts every grammar, so an ambiguity shows up only at parse time, as a parse forest with several trees; ambiguity detection before deployment avoids that.
- **Bioinformatics.** Grammars for RNA secondary structure must be unambiguous for their probabilities to be meaningful, and the check of Brabrand, Giegerich and Møller was designed for such grammars.

## References
