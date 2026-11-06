---
tag: A02ZD9
kind: problem
slug: cfg-equivalence-problem
name: CFG equivalence problem
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Decide whether two context-free grammars generate the same language; undecidable.
prereqs: [context-free-grammar, cfg-membership-problem, post-correspondence-problem]
see_also: [cfg-equivalence-undecidable, cfl-intersection-undecidable, cfg-ambiguity-problem, dfa-equivalence, regex-equivalence, nfa-universality, deterministic-context-free-language, rice-theorem]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.5.3, The Complement of a List Language, and Section 9.5.4, Other Undecidable Problems About CFG's
  - paper: doi:10.1524/stuf.1961.14.14.143
    title: Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)
    locator: pp. 143 to 172
  - paper: doi:10.1109/SWAT.1966.22
    title: A. J. Korenjak and John E. Hopcroft, Simple deterministic languages, 7th Annual Symposium on Switching and Automata Theory (1966)
    locator: pp. 36 to 46 (equivalence of simple deterministic grammars is decidable)
  - paper: doi:10.1016/S0304-3975(00)00285-1
    title: Géraud Sénizergues, L(A)=L(B)? decidability results from complete formal systems, Theoretical Computer Science 251(1-2) (2001)
    locator: pp. 1 to 166 (equivalence of deterministic pushdown automata is decidable)
  - paper: doi:10.1007/3-540-45465-9_70
    title: Colin Stirling, Deciding DPDA equivalence is primitive recursive, ICALP 2002, Lecture Notes in Computer Science 2380
    locator: pp. 821 to 832
  - paper: doi:10.1016/0304-3975(84)90092-6
    title: Dung T. Huynh, Deciding the inequivalence of context-free grammars with 1-letter terminal alphabet is Σ2p-complete, Theoretical Computer Science 33(2-3) (1984)
    locator: pp. 305 to 326
  - paper: doi:10.1007/BF01691341
    title: Sheila A. Greibach, A note on undecidable properties of formal languages, Mathematical Systems Theory 2(1) (1968)
    locator: pp. 1 to 6 (a Rice-like theorem for classes of languages)
  - paper: doi:10.1145/800125.804029
    title: Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Proceedings of the Fifth Annual ACM Symposium on Theory of Computing (1973)
    locator: pp. 1 to 9 (inequivalence of regular expressions without star is NP-complete)
  - paper: doi:10.1145/2814270.2814304
    title: Ravichandhran Madhavan, Mikaël Mayer, Sumit Gulwani and Viktor Kuncak, Automating grammar comparison, OOPSLA 2015
    locator: pp. 183 to 200 (counterexample search by enumeration and proofs of equivalence for practical grammars)
---

The CFG equivalence problem asks whether two [context-free grammars](/context-free-grammar/) generate the same language. No algorithm solves it: Bar-Hillel, Perles and Shamir showed in 1961 that it is [undecidable](/cfg-equivalence-undecidable/), by a reduction from [Post's correspondence problem](/post-correspondence-problem/), even when one of the two grammars is fixed to generate every string. Inequivalence can be confirmed by finding a string in one language and not the other, so the problem is co-recursively-enumerable, and it becomes decidable for restricted classes such as deterministic grammars and grammars over one letter.

## In plain words

Two grammars may look very different and still describe the same strings, as when a grammar is rewritten to suit a parser. One would like a program that checks that a rewrite did not change the language.

Such a program cannot exist. If the grammars differ, trying all strings in order of length will eventually find one that only one grammar accepts. But if they agree, the search never ends, and no cleverer method can always tell that it should stop. The obstacle is the same as for the halting problem: grammars can encode the runs of arbitrary programs.

The question can be answered for special grammars, such as those that a deterministic parser accepts, or grammars over a single letter.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, $n$ is the length of a string, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. Two grammars are *equivalent* if they generate the same language.

**Input.** Context-free grammars $G_1$ and $G_2$ over a terminal alphabet $\Sigma$.

**Output.** Yes if $L(G_1) = L(G_2)$, and no otherwise. A *witness* of inequivalence is a string in the symmetric difference $L(G_1) \mathbin{\triangle} L(G_2)$.

## Variants

- **Inclusion.** Decide $L(G_1) \subseteq L(G_2)$. Equivalence is two inclusions, and inclusion is undecidable too.
- **Universality.** Decide $L(G) = \Sigma^*$, which is equivalence with the fixed grammar $S \to a S \mid \varepsilon$ for $a \in \Sigma$. It is undecidable over a four-letter alphabet, and over two letters by coding.
- **Grammar against a regular language.** Decide $L(G) = L(E)$ for a regular expression or automaton $E$. Undecidable, since $E$ can describe $\Sigma^*$. The inclusion $L(G) \subseteq L(E)$ is decidable: intersect $L(G)$ with the complement of $L(E)$, a [closure property](/cfl-closure-properties/), and test [emptiness](/cfg-emptiness-problem/). This is polynomial for a DFA and exponential through determinization for an NFA or regular expression.
- **Bounded equivalence.** Given $G_1$, $G_2$ and a bound $k$ in unary, decide whether the languages agree on the strings of length at most $k$. A witness is a string of length at most $k$, checked by [CYK](/cyk-algorithm/), so the problem is in coNP. It is coNP-hard already for regular expressions without star, whose inequivalence Stockmeyer and Meyer showed NP-complete.
- **Deterministic grammars.** For [LR(k)](/lr-k-grammar/) grammars, or equivalently deterministic pushdown automata, equivalence is decidable (Sénizergues), even in primitive recursive time (Stirling). Earlier results covered simple deterministic grammars (Korenjak and Hopcroft, 1966), [LL(k)](/ll-k-grammar/) grammars (Rosenkrantz and Stearns, 1970) and parenthesis grammars (McNaughton, 1967).
- **One letter.** Over $\Sigma = \{a\}$ every context-free language is [regular](/regular-language/), by [Parikh's theorem](/parikh-theorem/), so equivalence is decidable. Huynh showed that inequivalence is complete for $\Sigma_2^p$, the second level of the polynomial hierarchy.
- **Finite languages.** If neither grammar is recursive, both languages are finite and can be listed, so equivalence is decidable.

## Examples

**Equivalent grammars.** The grammars
$$S \to a S b S \mid b S a S \mid \varepsilon \qquad\text{and}\qquad S \to a S b \mid b S a \mid S S \mid \varepsilon$$
both generate the strings with as many $a$'s as $b$'s. A script confirms that both give exactly the 351 such strings of length at most 10. Similarly $S \to ( S ) S \mid \varepsilon$ and $S \to S S \mid ( S ) \mid \varepsilon$ both give the 197 balanced strings of length at most 12. These checks are evidence, not proofs; a proof of equivalence needs an argument about all lengths, here an induction on the length of the string.

**Inequivalent grammars.** Dropping $S \to S S$ from the second grammar gives $S \to a S b \mid b S a \mid \varepsilon$, which generates only 63 of the 351 strings up to length 10. Its shortest witnesses are $abba$ and $baab$: each would need a production that adds the first and the last letter, and both letters are equal.

**From correspondence problems.** For the instance $x = (a, ab)$, $y = (aa, b)$ of Post's problem, the grammar $G$ built in the [proof of undecidability](/cfg-equivalence-undecidable/) generates every string over $\{a, b, 1, 2\}$ except those that encode a solution, the shortest being $aab21$. Deciding whether $G$ is equivalent to a grammar for all strings is deciding whether the instance has a solution.

## Known algorithms

- **Witness search.** List the strings of $\Sigma^*$ in order of length and test each for membership in both languages with [CYK](/cyk-algorithm/) or [Earley](/earley-parser/) parsing. The search halts exactly when the grammars are inequivalent; checking all strings up to length $k$ takes $O(|\Sigma|^k k^3 |G|)$ time. Practical tools enumerate the strings of one grammar instead of all strings, sample them at random, or use a SAT solver to find a witness up to a length bound.
- **Proof search.** For equivalent grammars, a tool can try to prove equivalence, for example by transforming both grammars into a common normal form or by a bisimulation argument when they are deterministic. Madhavan and coauthors combine both directions in one tool for grammars of programming languages.
- **Deterministic pushdown automata.** Sénizergues's algorithm and its simplifications by Stirling and by Jančar decide equivalence by a complete proof system together with a search for a counterexample. They are far from practical.
- **Restricted classes.** For simple deterministic grammars, LL(k) grammars and parenthesis grammars there are direct algorithms, and over one letter one can compute the ultimately periodic sets of lengths of both languages and compare them.

## Bounds

**Undecidable.** No algorithm decides equivalence, inclusion or universality. The proof of [undecidability](/cfg-equivalence-undecidable/) shows that each is complete for the co-recursively-enumerable sets: the complement of [PCP](/post-correspondence-problem/) reduces to universality, and a negative answer always has a finite witness.

**No bound on witnesses.** No computable function $f$ bounds the length of the shortest witness by $f(|G_1| + |G_2|)$, since otherwise checking all strings up to that length would decide the problem.

**Decidable cases.** Equivalence of deterministic pushdown automata is primitive recursive, and its exact complexity is open. Over one letter equivalence is complete for $\Pi_2^p$. Bounded equivalence is coNP-complete.

## Reductions

- **From PCP.** For an instance $(x, y)$, the union of grammars for the complements of the two [list languages](/cfl-intersection-undecidable/) is universal exactly when the instance has no solution.
- **Between the variants.** Equivalence reduces to inclusion, since $L_1 = L_2$ when both inclusions hold. Universality reduces to equivalence with a fixed grammar, and inclusion $L_1 \subseteq L_2$ reduces to equivalence, since it holds when $L_1 \cup L_2 = L_2$ and the union of two grammars is a grammar.
- **Greibach's theorem.** Greibach generalized the method to a theorem like [Rice's theorem](/rice-theorem/): for a class closed under union and concatenation with regular sets in which universality is undecidable, every nontrivial property that holds for all regular sets and is kept by the quotient $a \backslash L = \{w : aw \in L\}$ is undecidable. For context-free grammars this shows that being regular, or being equal to a given regular language, is undecidable.
- **To equivalence of regular expressions.** For regular expressions and automata the problem is decidable, [PSPACE-complete](/regex-equivalence/) for expressions and NFAs, and almost linear for [DFAs](/dfa-equivalence/).

## Applications

- **Grammar refactoring.** Rewriting a grammar for a parser, for example by [left recursion elimination](/left-recursion-elimination/) or a conversion to [Chomsky normal form](/chomsky-normal-form-conversion/), should not change the language. Since this cannot be checked in general, these transformations are proved correct once, and ad hoc rewrites are tested by witness search.
- **Grading and teaching.** Tools that grade grammars written by students compare them with a reference grammar by enumerating and sampling strings.
- **Compiler testing.** Two parsers for the same language are compared by generating strings from one grammar and checking them with the other parser.
- **Program equivalence.** Equivalence of monadic recursive program schemes reduces to equivalence of deterministic pushdown automata, so Sénizergues's result decides it.

## References
