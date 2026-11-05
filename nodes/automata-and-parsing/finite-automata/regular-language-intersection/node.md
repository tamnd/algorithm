---
tag: 02HNZZ
kind: problem
slug: regular-language-intersection
name: Regular language intersection
aliases:
- DFA intersection
- intersection of finite automata
area: automata-and-parsing/finite-automata
level: core
summary: Given automata for two regular languages, build an automaton for their intersection, or decide whether it is empty.
model: word-ram
complexity:
  vars: {n: the number of states of the first DFA, k: the number of states of the second DFA, σ: the alphabet size}
  time: {worst: O(n k σ)}
prereqs: [deterministic-finite-automaton, regular-language]
see_also: [product-construction, closure-properties-of-regular-languages, dfa-emptiness, state-complexity, nfa-equivalence, cfl-intersection-undecidable, ltl-model-checking, alternating-finite-automaton]
sources:
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: Definition 7 (the direct product of two automata), pp. 114 to 125
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.2.1, Closure of Regular Languages Under Boolean Operations, and Section 4.3, Decision Properties of Regular Languages
  - paper: doi:10.1109/SFCS.1977.16
    title: Dexter Kozen, Lower bounds for natural proof systems, 18th Annual Symposium on Foundations of Computer Science (FOCS 1977)
    locator: pp. 254 to 266 (the emptiness of the intersection of a given list of DFAs is PSPACE-complete)
  - paper: doi:10.1016/0304-3975(92)00011-F
    title: Sheng Yu, Qingyu Zhuang and Kai Salomaa, The state complexities of some basic operations on regular languages, Theoretical Computer Science 125(2) (1994)
    locator: pp. 315 to 328 (the state complexity mn of intersection)
  - paper: "Markus Holzer and Martin Kutrib, Nondeterministic descriptional complexity of regular languages, International Journal of Foundations of Computer Science 14(6) (2003)"
    locator: pp. 1087 to 1102 (the bound n1 n2 for the intersection of NFAs)
---

Regular language intersection is the problem of building an automaton for $L_1 \cap L_2$ from automata for two [regular languages](/regular-language/) $L_1$ and $L_2$, or, in its decision form, of deciding whether $L_1 \cap L_2$ is empty. The [product construction](/product-construction/) solves both for two [DFAs](/deterministic-finite-automaton/) with $n$ and $k$ states in $O(nk\sigma)$ time, and the bound $nk$ on the number of states is tight. With a list of DFAs as input, the emptiness question becomes PSPACE-complete. Intersection is the core step of inclusion tests, of model checking, and of the regular expression operators "and" and lookahead.

## In plain words

Two machines each check one rule about a string. You want one machine that accepts a string only when both rules hold, or you want to know whether any string at all satisfies both rules.

Run the two machines side by side on the same letters, and remember the pair of their states. A pair where both machines accept means that both rules hold. To build the combined machine, collect all pairs that some string can reach. To test whether any string passes both rules, search these pairs until you find one where both accept, or run out of pairs.

## Definition

**Construction form.** The input is two complete DFAs $M_1 = (Q_1, \Sigma, \delta_1, s_1, F_1)$ and $M_2 = (Q_2, \Sigma, \delta_2, s_2, F_2)$ over the same alphabet, with $\delta_i : Q_i \times \Sigma \to Q_i$ and no $\varepsilon$-moves. Let $n = |Q_1|$, $k = |Q_2|$ and $\sigma = |\Sigma|$. The output is a DFA $P$ with $L(P) = L(M_1) \cap L(M_2)$.

**Decision form (intersection emptiness).** The same input; the output is yes if $L(M_1) \cap L(M_2) = \emptyset$, and no otherwise. A witness version also outputs a string in the intersection when there is one.

**Many automata.** The input is a list $M_1, \ldots, M_t$ of DFAs, and the question is whether $\bigcap_{i=1}^{t} L(M_i) = \emptyset$. Here $t$ is part of the input.

## Variants

- **NFAs.** For [NFAs](/nondeterministic-finite-automaton/) the product with $\delta((p, q), a) = \delta_1(p, a) \times \delta_2(q, a)$ is an NFA for the intersection, with $nk$ states. No determinization is needed, unlike for complement.
- **Regular expressions.** Given two [regular expressions](/regular-expression/), build an expression or an automaton for the intersection. Expressions with an intersection operator can be exponentially more succinct than plain ones.
- **Fixed number of automata.** For a fixed $t$, the product of $t$ DFAs with at most $n$ states each has at most $n^t$ states, so emptiness is decidable in polynomial time for each fixed $t$.
- **Intersection with a context-free language.** The intersection of a [context-free language](/context-free-language/) and a regular language is context-free, by a product of a pushdown automaton and a DFA. The intersection of two context-free languages need not be context-free, and its emptiness is undecidable ([CFL intersection](/cfl-intersection-undecidable/)).
- **Infinite words.** For [Büchi automata](/buchi-automaton/), the product needs an extra flag to make sure that both automata accept infinitely often.

## Examples

**Even number of $a$s and contains $bb$.** With a 2-state DFA for the first language and a 3-state DFA for the second, all 6 pairs are reachable, and the 6-state product is the minimal DFA for the intersection. The pairs and their moves are in the example of the [product construction](/product-construction/). The shortest string in the intersection is $bb$, and the strings of length 4 in it are $aabb$, $abba$, $bbaa$ and $bbbb$.

**Counting modulo $m$ and $n$: the bound $mn$ is reached.** Let $L_1$ be the strings over $\{a, b\}$ whose number of $a$s is divisible by $m$ (an $m$-state DFA), and $L_2$ those whose number of $b$s is divisible by $n$ (an $n$-state DFA). The strings $a^i b^j$ with $0 \le i < m$ and $0 \le j < n$ are pairwise distinguishable for $L_1 \cap L_2$: the suffix $a^{m - i} b^{n - j}$ puts $a^i b^j$ in the intersection and each other $a^{i'} b^{j'}$ out of it. So the minimal DFA of the intersection has exactly $mn$ states, by the [Myhill-Nerode theorem](/myhill-nerode-theorem/). This holds for all $m, n \ge 1$, coprime or not.

**Unary lengths.** Over $\{a\}$, let $L_1$ be the strings of even length and $L_2$ those whose length is 1 modulo 3. The product of a 2-cycle and a 3-cycle is a 6-cycle, and the intersection is $\{a^\ell : \ell \equiv 4 \pmod 6\}$, by the Chinese remainder theorem. Its shortest strings are $a^4$ and $a^{10}$.

**An empty intersection.** For $L_1 = a\{a, b\}^*$ (strings that start with $a$) and $L_2 = b\{a, b\}^*$ (strings that start with $b$), the reachable pairs are the start pair, (after $a$, dead) and (dead, after $b$), and none of them has two accepting components. So the intersection is empty, and the search shows it after visiting 3 pairs.

## Known algorithms

- **[Product construction](/product-construction/).** Search the pairs reachable from $(s_1, s_2)$, with accepting pairs $F_1 \times F_2$. Time and space $O(N \sigma)$ for $N \le nk$ reachable pairs.
- **On-the-fly emptiness.** Run the same breadth-first search without storing the table, and stop at the first pair in $F_1 \times F_2$. The parent links of the search give a shortest string in the intersection. This is [DFA emptiness](/dfa-emptiness/) on the implicit product, in $O(nk\sigma)$ time and $O(nk)$ space.
- **Partial product for NFAs and lazy inputs.** The same search works when the input automata are NFAs, or are given only by a function that returns the successors of a state, as in model checking.
- **De Morgan.** $L_1 \cap L_2 = \overline{\overline{L_1} \cup \overline{L_2}}$. For DFAs this gives the same product. For NFAs it needs two determinizations and is much worse than the direct product.
- **Many automata.** For a list of $t$ DFAs, search the $t$-tuples of states. The search needs up to $n^t$ states. A nondeterministic search that keeps only the current tuple, of $t \log n$ space, shows that the problem is in NPSPACE, so in PSPACE by Savitch's theorem.

## Bounds

**State complexity.** For complete DFAs with $n$ and $k$ states, the intersection needs at most $nk$ states, and the counting example reaches $nk$ for all $n, k \ge 1$ over a two-letter alphabet (Yu, Zhuang and Salomaa, 1994). For NFAs the bound is also $nk$, and it is reached (Holzer and Kutrib, 2003). For a list of $t$ DFAs with $n$ states each, $n^t$ states are needed in the worst case, by the same counting argument with $t$ letters.

**Time for two DFAs.** $O(nk\sigma)$ on the [word RAM](/word-ram/) for both forms, by the product. The output of the construction form can have $nk\sigma$ transitions, so this is optimal for that form.

**Many DFAs.** Deciding whether the intersection of $t$ given DFAs is empty is PSPACE-complete (Kozen, 1977). So unless P = PSPACE, no algorithm runs in time polynomial in $t$ and $n$.

## Reductions

- **Inclusion to intersection.** $L(M_1) \subseteq L(M_2)$ if and only if $L(M_1) \cap \overline{L(M_2)} = \emptyset$. For DFAs, complement $M_2$ by swapping its accepting states, then test emptiness of the product.
- **Equivalence to intersection.** $L(M_1) = L(M_2)$ if and only if both inclusions hold, or if and only if the product with accepting pairs "exactly one component accepts" is empty. For NFAs this route needs complementation, and [NFA equivalence](/nfa-equivalence/) is PSPACE-complete.
- **Intersection emptiness of many DFAs is PSPACE-hard.** Kozen's proof encodes the computation of a Turing machine with polynomial space: each DFA checks one local condition on a string of configurations, and the intersection is non-empty exactly when an accepting computation exists.
- **To emptiness.** The decision form is [DFA emptiness](/dfa-emptiness/) on the product.

## Applications

- **Model checking.** A system satisfies a property when the system automaton intersected with an automaton for the negation of the property is empty, as in [LTL model checking](/ltl-model-checking/).
- **Regular expression features.** Intersection operators and lookahead in regular expression engines, and the combination of several input constraints into one validator.
- **String constraint solving.** Solvers for constraints of the form "$x$ matches $r_1$ and $x$ matches $r_2$" intersect the automata and search for a witness.
- **Compilers.** A lexer generator checks whether two token patterns can match the same string, which is an intersection emptiness test.

## References
