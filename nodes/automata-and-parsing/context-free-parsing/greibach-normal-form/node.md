---
tag: YZSW58
kind: definition
slug: greibach-normal-form
name: Greibach normal form
aliases:
- GNF
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A normal form where every production is A→aα with a terminal followed by nonterminals.
prereqs: [context-free-grammar, derivation, chomsky-normal-form]
see_also: [greibach-normal-form-conversion, chomsky-normal-form, left-recursion, pushdown-automaton, cfg-to-pda-conversion, ll-grammar, dyck-language, cfl-pumping-lemma]
sources:
  - paper: doi:10.1145/321250.321254
    title: Sheila A. Greibach, A new normal-form theorem for context-free phrase structure grammars, Journal of the ACM 12(1) (1965)
    locator: pp. 42 to 52
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, Addison-Wesley, 1979
    locator: Section 4.6, Greibach Normal Form
  - paper: doi:10.1145/321406.321412
    title: Daniel J. Rosenkrantz, Matrix equations and normal forms for context-free grammars, Journal of the ACM 14(3) (1967)
    locator: pp. 501 to 507 (Greibach normal form by matrix equations, and the double form)
  - paper: doi:10.1006/inco.1998.2772
    title: Norbert Blum and Robert Koch, Greibach normal form transformation revisited, Information and Computation 150(1) (1999)
    locator: pp. 112 to 118
  - paper: doi:10.1109/SWAT.1966.22
    title: A. J. Korenjak and John E. Hopcroft, Simple deterministic languages, 7th Annual Symposium on Switching and Automata Theory (1966)
    locator: pp. 36 to 46
---

A [context-free grammar](/context-free-grammar/) is in Greibach normal form when every right side is a terminal followed by zero or more nonterminals, $A \to a B_1 \cdots B_k$. Each step of a [derivation](/derivation/) then writes exactly one terminal, so a string of length $n$ has derivations of exactly $n$ steps, and no nonterminal is [left-recursive](/left-recursion/). Sheila Greibach proved in 1965 that every context-free language without the empty string has such a grammar.

## Definition

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

A grammar $G = (V, \Sigma, P, S)$ is in **Greibach normal form** (GNF) if every production has the form

$$A \to a B_1 B_2 \cdots B_k \qquad (a \in \Sigma,\ k \ge 0,\ B_1, \ldots, B_k \in V),$$

with one exception: the production $S \to \varepsilon$ is allowed when $S$ occurs on no right side. Without the exception, a grammar in Greibach normal form cannot generate $\varepsilon$.

**Theorem (Greibach 1965).** For every context-free grammar $G$ there is a grammar $G'$ in Greibach normal form with $L(G') = L(G)$.

The page on [Greibach normal form conversion](/greibach-normal-form-conversion/) gives the classical construction and its proof. The construction can make the grammar exponentially larger, but Blum and Koch give one whose output has size $O(|G|^4)$.

**Basic facts.** Let $G$ be in Greibach normal form.

- *One terminal per step.* In a leftmost derivation from $S$, every sentential form is $x \alpha$ with $x \in \Sigma^*$ and $\alpha \in V^*$, and each step adds one terminal to $x$. So every derivation of a nonempty $w$ has exactly $|w|$ steps, and the parse tree has $|w|$ internal nodes. In particular, membership is decidable by trying all leftmost derivations of $|w|$ steps.
- *No left recursion and no $\varepsilon$.* No right side starts with a nonterminal, so $A \Rightarrow^+ A \alpha$ is impossible, and no nonterminal other than $S$ derives $\varepsilon$.
- *A one-state real-time pushdown automaton.* Take one state, the nonterminals as stack symbols, $S$ as the initial stack symbol, and for each production $A \to a B_1 \cdots B_k$ the move "read $a$, pop $A$, push $B_1 \cdots B_k$ with $B_1$ on top". By the first fact, the automaton empties its stack on $w$ exactly when $S \Rightarrow^* w$, and every move reads one input symbol. So every context-free language without $\varepsilon$ is accepted by empty stack by a [pushdown automaton](/pushdown-automaton/) with one state and no $\varepsilon$-moves; this is the construction of [the conversion of a grammar to a pushdown automaton](/cfg-to-pda-conversion/) applied to a grammar in this form.

## Examples and non-examples

**Nonempty balanced parentheses.** The grammar

$$S \to (\,R \mid (\,S R \mid (\,R S \mid (\,S R S, \qquad R \to )$$

is in Greibach normal form and generates the nonempty strings of the [Dyck language](/dyck-language/) on one pair of brackets. Here $R$ stands for the closing bracket, which cannot appear after the first position of a right side. The usual grammar $S \to (\,S\,)\,S \mid \varepsilon$ is not in this form.

**$a^n b^n$ for $n \ge 1$.** $S \to a B \mid a S B$, $B \to b$. The derivation of $aaabbb$ is $S \Rightarrow a S B \Rightarrow aa S B B \Rightarrow aaa B B B \Rightarrow aaab B B \Rightarrow aaabb B \Rightarrow aaabbb$, with 6 steps for 6 terminals.

**Lists.** The left-recursive grammar $E \to E + T \mid T$, $T \to a$ is not in Greibach normal form. The grammar

$$E \to a \mid a R, \qquad R \to +\,T \mid +\,T R, \qquad T \to a$$

is, and it generates the same language $a (+a)^*$.

**Not in the form.**

- A grammar in [Chomsky normal form](/chomsky-normal-form/) with a production $A \to B C$: the right side starts with a nonterminal.
- $S \to a S b \mid a b$: the right sides start with a terminal, but a terminal also occurs later. Replacing $b$ by a new $B$ with $B \to b$ gives the form.
- $S \to a S \mid \varepsilon$ with $S$ on a right side: the exception allows $S \to \varepsilon$ only when $S$ is on no right side. A form for the same language is $S_0 \to \varepsilon \mid a \mid a S$, $S \to a \mid a S$.

## Related definitions

- **Chomsky normal form.** In [Chomsky normal form](/chomsky-normal-form/) every production is $A \to B C$ or $A \to a$; parse trees are binary, and derivations of $w$ have $2|w| - 1$ steps. The conversion to it is simpler and gives size $O(|G|^2)$.
- **Weak forms.** Some texts allow $A \to a \alpha$ with any $\alpha \in (V \cup \Sigma)^*$. Such a grammar becomes a grammar in Greibach normal form by replacing each terminal $b$ in a non-first position by a new nonterminal $T_b$ with $T_b \to b$.
- **Quadratic Greibach normal form.** At most two nonterminals follow the terminal: $A \to a$, $A \to a B$ or $A \to a B C$. Every grammar in Greibach normal form has an equivalent one in quadratic form. For every suffix $\beta$ with $|\beta| \ge 2$ of a string $B_1 \cdots B_k$ of a right side, add a nonterminal $[\beta]$, and write $[B] = B$ for one symbol. Replace $A \to a \gamma$ by $A \to a [\gamma]$, and give each $[B \beta']$ the productions $[B \beta'] \to b\, [\gamma]\, [\beta']$ for $B \to b \gamma$ with $\gamma \ne \varepsilon$, and $[B \beta'] \to b\, [\beta']$ for $B \to b$. By induction on the length of derivations, $[\beta]$ derives exactly the strings that $\beta$ derives. There are at most $|G|$ new nonterminals, and each has as many productions as some old nonterminal, so the size is $O(|G|^2)$. For the balanced parentheses grammar above the result has 14 productions.
- **Double Greibach normal form.** Every right side starts and ends with a terminal, or is a single terminal. Rosenkrantz's construction by matrix equations gives this form, and Hotz showed that a form that is both double and quadratic also exists.
- **Simple deterministic grammars.** A grammar in Greibach normal form is an *s-grammar* if for every nonterminal $A$ and terminal $a$ there is at most one production $A \to a \alpha$. Its pushdown automaton above is then deterministic. Korenjak and Hopcroft studied these grammars and showed that their equivalence is decidable. Every s-grammar is an [LL(1) grammar](/ll-grammar/); the parentheses grammar above is not an s-grammar, since $S$ has four productions that start with $($.
- **Use in proofs.** Greibach normal form is used to show that every context-free language without $\varepsilon$ is accepted by a real-time pushdown automaton, and to bound the length of derivations by the length of the string. Proofs about parse trees, such as the [pumping lemma](/cfl-pumping-lemma/), usually use Chomsky normal form instead, because its trees are binary.

## References
