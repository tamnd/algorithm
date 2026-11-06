---
tag: V2G516
kind: definition
slug: linear-grammar
name: Linear grammar
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A grammar where each production has at most one nonterminal on its right-hand side.
prereqs: [context-free-grammar, regular-language, cfl-pumping-lemma]
see_also: [context-free-language, cfl-closure-properties, cyk-algorithm, dyck-language, cfg-ambiguity-undecidable, cfl-intersection-undecidable, pushdown-automaton, nondeterministic-finite-automaton]
sources:
  - book: isbn:9781284077247
    title: Peter Linz, An Introduction to Formal Languages and Automata, sixth edition
    locator: Section 3.3, Regular Grammars (right-linear, left-linear and linear grammars); Section 8.1, Two Pumping Lemmas (the pumping lemma for linear languages)
  - paper: doi:10.1137/0304034
    title: Seymour Ginsburg and Edwin H. Spanier, Finite-turn pushdown automata, SIAM Journal on Control 4(3) (1966)
    locator: pp. 429 to 453 (the linear languages are the languages of one-turn pushdown automata)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.5.2, the reduction from the Post correspondence problem to ambiguity of context-free grammars
---

A linear grammar is a [context-free grammar](/context-free-grammar/) in which every right side contains at most one nonterminal, so that each production has the form $A \to u B v$ or $A \to u$ with terminal strings $u$ and $v$. Every sentential form of a linear grammar has at most one nonterminal, and a derivation grows the string from the outside in, at both ends. If all productions put the nonterminal at the right end, the grammar is right-linear and generates a [regular language](/regular-language/); in general, the linear languages lie strictly between the regular and the [context-free languages](/context-free-language/).

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. Below, $u, v \in \Sigma^*$.

**Linear grammar.** $G$ is *linear* if every production has the form $A \to u B v$ with $B \in V$, or $A \to u$. It is *right-linear* if every production has the form $A \to u B$ or $A \to u$, and *left-linear* if every production has the form $A \to B v$ or $A \to v$. A language is *linear* if some linear grammar generates it.

**Basic facts.**

- *One nonterminal at a time.* By induction on the derivation, every sentential form of a linear grammar is $x B y$ or $x$ with $x, y \in \Sigma^*$. The derivation is therefore both leftmost and rightmost, and the [parse tree](/parse-tree/) is a path of inner nodes with terminal leaves hanging off both sides.
- *Right-linear means regular.* A right-linear grammar is a finite automaton in disguise: the nonterminals are the states, $A \to u B$ is a path from $A$ to $B$ that reads $u$, and $A \to u$ is a path from $A$ to an accepting state. Conversely, every [NFA](/nondeterministic-finite-automaton/) gives a right-linear grammar with the productions $A \to a B$ for its transitions and $A \to \varepsilon$ for its accepting states. Left-linear grammars generate the reversals of the languages of right-linear ones, so they also generate exactly the regular languages.
- *One-turn pushdown automata.* The linear languages are exactly the languages of [pushdown automata](/pushdown-automaton/) that, in every run, first only push and then only pop, with one turn between the two phases (Ginsburg and Spanier, 1966).
- *Parsing in quadratic time.* Let $T(i, j)$ be the set of nonterminals that derive $w[i:j] = a_{i+1} \cdots a_j$. A production $A \to u B v$ puts $A$ into $T(i, j)$ when $w[i:j]$ starts with $u$, ends with $v$ and $B \in T(i + |u|, j - |v|)$, so each of the $O(n^2)$ cells is filled in $O(|G|)$ time, smaller spans first; productions with $u = v = \varepsilon$ need a fixed-point inside the cell. This $O(|G| n^2)$ bound is a factor $n$ better than the [CYK algorithm](/cyk-algorithm/), because there is no split point to choose.

**Pumping lemma for linear languages.** For every linear language $L$ there is a $p$ such that every $w \in L$ with $|w| \ge p$ can be written $w = x u z v y$ with $|x u v y| \le p$, $|u v| \ge 1$, and $x u^i z v^i y \in L$ for all $i \ge 0$. Compared with the [pumping lemma for context-free languages](/cfl-pumping-lemma/), the pumped parts are close to the two ends of $w$, not anywhere in it: the repeated nonterminal is found among the first $|V| + 1$ steps of the derivation, each of which adds a bounded number of terminals at each end.

## Examples and non-examples

**Linear, not regular.** $S \to a S b \mid \varepsilon$ generates $\{a^m b^m : m \ge 0\}$. The palindromes over $\{a, b\}$ come from $S \to a S a \mid b S b \mid a \mid b \mid \varepsilon$; see [palindrome](/palindrome/). The language $\{a^m b^k : m \neq k\}$ comes from $S \to a S b \mid A \mid B$, $A \to a A \mid a$, $B \to b B \mid b$: the first production matches $a$'s with $b$'s, and $A$ or $B$ produces the surplus. None of these languages is regular.

**Right-linear.** $S \to a b S \mid \varepsilon$ generates $(ab)^*$, and its nonterminal $S$ is the one state of a two-state automaton with an extra state for the middle of $ab$.

**A linear language with a nonlinear grammar.** $S \to S S \mid a$ is not linear, but its language $a^+$ is regular and so linear, with $S \to a S \mid a$. Linearity of a grammar is a property of the grammar; linearity of a language asks whether some linear grammar exists.

**Context-free, not linear.** $L = \{a^m b^m a^k b^k : m, k \ge 0\}$ is generated by $S \to A A$, $A \to a A b \mid \varepsilon$, but by no linear grammar. Take $w = a^p b^p a^p b^p$ in the pumping lemma. Since $|x u| \le p$ and $|v y| \le p$, the part $u$ lies in the first block of $a$'s and $v$ in the last block of $b$'s. Pumping with $i = 2$ gives $a^{p + |u|} b^p a^p b^{p + |v|}$, which is in $L$ only if $|u| = |v| = 0$, a contradiction. The [Dyck language](/dyck-language/) of balanced brackets is not linear either: in $w = (^p )^p (^p )^p$ the part $u$ lies in the first block of opening brackets and $v$ in the last block of closing ones, and pumping down with $i = 0$ gives a string with a prefix $(^{p - |u|} )^p$ that closes more brackets than it opens when $|u| \ge 1$, or with unequal counts when $|u| = 0$.

**Closure.** The linear languages are closed under union (add $S \to S_1 \mid S_2$), under reversal, under homomorphisms, and under intersection with a regular language. The example above shows that they are not closed under concatenation, since $L$ is the concatenation of a linear language with itself, and not under star. They are not closed under intersection either: $\{a^m b^m c^k\} \cap \{a^m b^k c^k\}$ is $\{a^m b^m c^m\}$, which is not context-free. See [closure properties](/cfl-closure-properties/).

## Related definitions

- *Metalinear grammars* allow one start production $S \to A_1 \cdots A_k$ with linear $A_i$; their languages are the finite unions of concatenations of linear languages, and include the example $L$ above.
- *Even linear grammars* require $|u| = |v|$ in each $A \to u B v$, and generate a smaller class that behaves in some ways like the regular languages.
- *Undecidability.* Many questions are already undecidable for linear grammars. The reduction from the [Post correspondence problem](/post-correspondence-problem/) to [ambiguity](/cfg-ambiguity-undecidable/) builds two linear grammars, $S_1 \to w_i S_1 c_i \mid w_i c_i$ and $S_2 \to x_i S_2 c_i \mid x_i c_i$ with index symbols $c_i$, so ambiguity is undecidable for linear grammars, and so is the emptiness of the [intersection of two linear languages](/cfl-intersection-undecidable/).
- [Regular languages](/regular-language/) are the languages of right-linear grammars; [context-free languages](/context-free-language/) are the languages of all grammars.

## References
