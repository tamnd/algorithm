---
tag: M03DCZ
kind: theorem
slug: cfl-closure-properties
name: Closure properties of context-free languages
area: automata-and-parsing/context-free-parsing
level: core
summary: Context-free languages are closed under union, concatenation, star, and intersection with regular languages.
prereqs: [context-free-language, context-free-grammar, cfg-pda-equivalence, cfl-pumping-lemma]
see_also: [closure-properties-of-regular-languages, product-construction, deterministic-context-free-language, cfl-intersection-undecidable, chomsky-schutzenberger-theorem, parikh-theorem, regular-language-intersection, dyck-language]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.3, Closure Properties of Context-Free Languages (7.3.1 Substitutions, 7.3.2 Applications of the Substitution Theorem, 7.3.3 Reversal, 7.3.4 Intersection With a Regular Language, 7.3.5 Inverse Homomorphism)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.3, Non-Context-Free Languages (Example 2.36, the language a^n b^n c^n), and the exercises of Chapter 2 on intersection, complement and intersection with a regular language
  - paper: doi:10.1016/S0019-9958(63)90306-1
    title: Marcel-Paul Schützenberger, On context-free languages and push-down automata, Information and Control 6(3) (1963)
    locator: pp. 246 to 264
---

## Statement

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. For a language $L$, $L^R$ is the set of reversed strings and $\overline{L} = \Sigma^* \setminus L$. A *homomorphism* $h : \Sigma^* \to \Delta^*$ is given by strings $h(a)$ for $a \in \Sigma$, with $h(a_1 \cdots a_k) = h(a_1) \cdots h(a_k)$. A *substitution* $s$ maps each $a \in \Sigma$ to a language $s(a) \subseteq \Delta^*$, with $s(a_1 \cdots a_k) = s(a_1) \cdots s(a_k)$ and $s(L) = \bigcup_{x \in L} s(x)$.

**Theorem.** Let $L$, $L_1$ and $L_2$ be [context-free languages](/context-free-language/) over $\Sigma$, let $R \subseteq \Sigma^*$ be [regular](/regular-language/), let $h : \Sigma^* \to \Delta^*$ and $g : \Delta^* \to \Sigma^*$ be homomorphisms, and let $s$ be a substitution with $s(a)$ context-free for each $a$. Then the following languages are context-free:

1. $L_1 \cup L_2$, $L_1 L_2$ and $L^*$;
2. $L^R$;
3. $s(L)$ and $h(L)$;
4. $L \cap R$;
5. $g^{-1}(L) = \{ x \in \Delta^* : g(x) \in L \}$.

On the other hand, there are context-free $L_1, L_2$ over $\{a, b, c\}$ with $L_1 \cap L_2$ not context-free, and so the context-free languages are not closed under intersection, complement or difference.

All the constructions are effective. For grammars $G_1, G_2$, the grammars for parts 1 to 3 have size $O(|G_1| + |G_2|)$, $O(|G|)$, and $O(|G| + \sum_a |G_a|)$. For part 4 with a DFA of $m$ states and $G$ in a binary form, the grammar has $O(|G| m^3)$ size.

## In plain words

Gluing two grammars together is easy: a new start rule can say "either one or the other", "one then the other", or "the first one, any number of times". Turning every rule around gives the mirror images of all the strings. Replacing each letter by a whole sub-grammar still gives a grammar.

A grammar can also be combined with a finite automaton. Each piece of a sentence is labelled with the automaton state before it and after it, and the labels must fit together. The result keeps exactly the sentences that the automaton accepts.

What fails is combining two grammars by "and". One grammar can check that the numbers of a's and b's agree, and another that the numbers of b's and c's agree, but no grammar can check both, so "and" leaves the class. Complement fails too, because "and" can be written with "not" and "or".

## Proof

The full proof is in [the proof of the closure properties](proofs/main.md). It uses grammars with disjoint sets of nonterminals and one fact: if $X_1 \cdots X_k \Rightarrow^* w$, then $w$ splits as $w_1 \cdots w_k$ with $X_i \Rightarrow^* w_i$, because a derivation step rewrites one nonterminal without looking at its neighbours.

- **Union, concatenation, star.** With a new start symbol $S$, add $S \to S_1 \mid S_2$, or $S \to S_1 S_2$, or $S \to S_1 S \mid \varepsilon$.
- **Reversal.** Reverse every right side. By induction on derivations, $A \Rightarrow^* w$ before exactly when $A \Rightarrow^* w^R$ after.
- **Substitution.** Replace every terminal $a$ in the productions of $G$ by the start symbol $S_a$ of a grammar for $s(a)$, and add the productions of all these grammars. The top part of each parse tree is a parse tree of $G$, and the parts below the $S_a$ derive strings of $s(a)$. A homomorphism is the substitution with $s(a) = \{h(a)\}$.
- **Intersection with a regular language.** For a DFA with states $Q$, use the nonterminals $[p X q]$, meaning "$X$ derives a string that takes the DFA from $p$ to $q$". A production $A \to X_1 \cdots X_k$ gives $[p_0 A p_k] \to [p_0 X_1 p_1] \cdots [p_{k-1} X_k p_k]$ for all states, a terminal gives $[p a q] \to a$ when $\delta(p, a) = q$, and the start rules are $S' \to [q_0 S f]$ for final $f$. By induction on derivations, $[p X q] \Rightarrow^* w$ exactly when $X \Rightarrow^* w$ and $\delta^*(p, w) = q$. The same construction on automata is the [product construction](/product-construction/) of a PDA with a DFA.
- **Inverse homomorphism.** Take a [pushdown automaton](/cfg-pda-equivalence/) $P$ for $L$. A new PDA reads a symbol $a$, puts $g(a)$ into a buffer kept in its finite state, and feeds the buffer to $P$ one symbol at a time with $\varepsilon$-moves. It accepts when $P$ is in a final state and the buffer is empty.
- **Intersection fails.** $L_1 = \{a^i b^i c^j\}$ and $L_2 = \{a^i b^j c^j\}$ are context-free, with grammars $S \to X C$, $X \to aXb \mid \varepsilon$, $C \to cC \mid \varepsilon$ and $S \to A Y$, $A \to aA \mid \varepsilon$, $Y \to bYc \mid \varepsilon$. Their intersection $\{a^n b^n c^n\}$ is not context-free by the [pumping lemma](/cfl-pumping-lemma/). Since $L_1 \cap L_2 = \overline{\overline{L_1} \cup \overline{L_2}}$, closure under complement would give closure under intersection, and $\overline{L} = \Sigma^* \setminus L$ rules out difference. $\blacksquare$

**Example.** Let $G$ be $S \to a S b \mid S S \mid \varepsilon$, the balanced strings, and let $R = a^* b^*$, accepted by the DFA with states $0$ (start, only $a$ so far) and $1$ (some $b$ read), both final, with $\delta(0, a) = 0$, $\delta(0, b) = 1$, $\delta(1, b) = 1$. The construction gives 31 productions, and after removing [useless symbols](/useless-symbol-elimination/) 13 remain:
$$\begin{aligned}
S' &\to [0S0] \mid [0S1], \qquad [0a0] \to a, \qquad [0b1] \to b, \qquad [1b1] \to b,\\
[0S1] &\to [0a0][0S0][0b1] \mid [0a0][0S1][1b1] \mid [0S0][0S1] \mid [0S1][1S1],\\
[0S0] &\to [0S0][0S0] \mid \varepsilon, \qquad [1S1] \to [1S1][1S1] \mid \varepsilon.
\end{aligned}$$
A script confirms that it generates exactly $\varepsilon, ab, aabb, aaabbb, aaaabbbb$ up to length 8, which is $L(G) \cap a^*b^* = \{a^n b^n\}$. The same script checks the construction against direct filtering on 150 random grammars and DFAs, and checks that $L_1 \cap L_2$ above contains, up to length 9, only $\varepsilon$, $abc$, $aabbcc$ and $aaabbbccc$.

## Consequences

- **Proving languages not context-free.** To show that $L$ is not context-free, intersect it with a regular language or apply a homomorphism to reach a known non-context-free language. For example $\{ w \in \{a, b, c\}^* : w \text{ has equally many } a, b \text{ and } c \}$ is not context-free, because its intersection with $a^* b^* c^*$ is $\{a^n b^n c^n\}$.
- **Parsing with a regular filter.** The intersection construction is the basis of parsing a lattice or a regular set of inputs, and of [CFL reachability](/cfl-reachability/), where the regular language is the set of paths of a graph.
- **Emptiness of intersections.** $L(G) \cap R = \emptyset$ is decidable, by the construction and the [emptiness test](/cfg-emptiness-problem/). For two grammars the question is [undecidable](/cfl-intersection-undecidable/).
- **Abstract families of languages.** Closure under union, concatenation, star, homomorphism, inverse homomorphism and intersection with regular languages makes the context-free languages a full abstract family of languages, a notion of Ginsburg and Greibach. By the [Chomsky-Schützenberger theorem](/chomsky-schutzenberger-theorem/), every context-free language is $h(D \cap R)$ for a [Dyck language](/dyck-language/) $D$, a regular $R$ and a homomorphism $h$.
- **Further operations.** The class is also closed under taking prefixes and under the quotient $L / R$ by a regular language, both by intersection and homomorphism tricks.

## Tightness

- **Intersection of two.** The intersection of two context-free languages can fail to be context-free, as shown. Every recursively enumerable language is a homomorphic image of the intersection of two context-free languages, so a closure under intersection would include very much more.
- **Deterministic languages.** The [deterministic context-free languages](/deterministic-context-free-language/) are closed under complement and under intersection with regular languages, but not under union or intersection. $L_1$ and $L_2$ above are deterministic, and their intersection is not context-free. If the class were closed under union, $\overline{L_1} \cup \overline{L_2}$ would be deterministic, and then so would its complement $L_1 \cap L_2$.
- **One letter.** Over a one-letter alphabet every context-free language is regular, by [Parikh's theorem](/parikh-theorem/), so there the class is closed under intersection and complement.
- **Size.** The intersection construction is polynomial in the DFA, but a grammar for $L \cap R$ can need many nonterminals, since the regular language may need a DFA of exponential size compared to an NFA. With an NFA the same construction works, with $[p X q]$ for NFA states.

## History

Bar-Hillel, Perles and Shamir proved in 1961 that the intersection of a context-free language with a regular language is context-free, together with the pumping lemma and the failure of closure under intersection and complement. Schützenberger (1963) and Ginsburg and his coauthors studied closure under homomorphisms, inverse homomorphisms and substitutions in the early 1960s, which led to the theory of abstract families of languages of Ginsburg and Greibach (1969).

## References
