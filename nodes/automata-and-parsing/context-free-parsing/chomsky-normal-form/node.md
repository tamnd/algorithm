---
tag: AZJ5NZ
kind: definition
slug: chomsky-normal-form
name: Chomsky normal form
aliases:
- CNF
area: automata-and-parsing/context-free-parsing
level: core
summary: A normal form where every production is A→BC or A→a, with no epsilon or unit productions except S→ε.
prereqs: [context-free-grammar, derivation, parse-tree]
see_also: [chomsky-normal-form-conversion, cfg-normal-form-conversion, greibach-normal-form, cyk-algorithm, cfl-pumping-lemma, inside-outside-algorithm, valiant-algorithm, epsilon-production-elimination]
sources:
  - paper: doi:10.1016/S0019-9958(59)90362-6
    title: Noam Chomsky, On certain formal properties of grammars, Information and Control 2(2) (1959)
    locator: pp. 137 to 167 (grammars whose rules have the forms A → BC and A → a)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1.5, Chomsky Normal Form, and Section 7.2.1, The Size of Parse Trees
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Chomsky Normal Form (Definition 2.8 and Theorem 2.9)
---

A [context-free grammar](/context-free-grammar/) is in Chomsky normal form when every production either replaces a nonterminal by exactly two nonterminals or by exactly one terminal, $A \to B C$ or $A \to a$, with $S \to \varepsilon$ allowed only when the start symbol $S$ appears on no right side. Every parse tree is then a binary tree over the letters of the string, so a string of length $n$ has derivations of exactly $2n - 1$ steps. Chomsky showed in 1959 that every context-free language has such a grammar, and the form is the input of the [CYK algorithm](/cyk-algorithm/) and of the proof of the [pumping lemma](/cfl-pumping-lemma/).

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, $n$ is the length of a string $w$, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

A grammar $G = (V, \Sigma, R, S)$ is in **Chomsky normal form** if every production has one of the forms

$$A \to B C \quad (B, C \in V), \qquad A \to a \quad (a \in \Sigma), \qquad S \to \varepsilon,$$

and if $S \to \varepsilon \in R$, then $S$ appears on no right side.

So there are no *unit productions* $A \to B$, no *$\varepsilon$-productions* $A \to \varepsilon$ other than $S \to \varepsilon$, no right sides of length 3 or more, and no terminals in right sides of length 2.

Texts differ in the treatment of the empty string. Hopcroft, Motwani and Ullman allow no $\varepsilon$-production at all, so a grammar in their form generates $L \setminus \{\varepsilon\}$. Sipser allows $S \to \varepsilon$ and forbids $S$ on every right side, $A \to BC$ with $B, C \ne S$. The three versions describe the same languages up to $\varepsilon$, and each converts to the others in linear time by adding or removing a fresh start symbol.

**Theorem (Chomsky 1959).** For every context-free grammar $G$ there is a grammar $G'$ in Chomsky normal form with $L(G') = L(G)$. It can be computed in $O(|G|^2)$ time and has size $O(|G|^2)$.

The construction is the [Chomsky normal form conversion](/chomsky-normal-form-conversion/).

**Basic facts.** Let $G$ be in Chomsky normal form and let $w \in L(G)$ with $n = |w| \ge 1$.

- *Shape of parse trees.* A [parse tree](/parse-tree/) of $w$ has $n$ leaves, $n$ nodes that use a production $A \to a$, and $n - 1$ nodes that use $A \to B C$: removing the leaves leaves a full binary tree with $n$ leaves. So it has $3n - 1$ nodes.
- *Length of derivations.* Every derivation of $w$ from $S$ has exactly $2n - 1$ steps, one for each inner node: $n - 1$ steps that lengthen the sentential form and $n$ steps that turn a nonterminal into a terminal.
- *Height and length.* A tree of height $h$, the number of edges on a longest root-to-leaf path, has a yield of length at most $2^{h-1}$. This is the key step of the [pumping lemma](/cfl-pumping-lemma/).
- *Finitely many trees.* Since each tree of $w$ has $3n - 1$ nodes, $w$ has finitely many parse trees, at most $C_{n-1} |V|^{2n-1}$, where $C_{n-1}$ is the Catalan number that counts the shapes of binary trees with $n$ leaves. In a general grammar a cycle $A \Rightarrow^+ A$ can give infinitely many.
- *Substrings and spans.* A node that uses $A \to BC$ over the span $w_{i+1} \cdots w_j$ splits it at some $k$ with $i < k < j$ into a nonempty part for $B$ and a nonempty part for $C$. This is the recurrence of the [CYK algorithm](/cyk-algorithm/), which decides membership in $O(n^3 |G|)$ time.

## Examples and non-examples

**$a^n b^n$ with the empty string.** The grammar $S \to a S b \mid \varepsilon$ is not in the form. An equivalent grammar in Chomsky normal form, the output of the conversion, is

$$S_0 \to A X \mid \varepsilon, \quad S \to A X, \quad X \to S B \mid b, \quad A \to a, \quad B \to b.$$

$X$ derives the strings $a^n b^{n+1}$ for $n \ge 0$, and $S$ the strings $a^n b^n$ for $n \ge 1$. The derivation of $aabb$ has $2 \cdot 4 - 1 = 7$ steps:

$$S_0 \Rightarrow A X \Rightarrow a X \Rightarrow a S B \Rightarrow a A X B \Rightarrow a a X B \Rightarrow a a b B \Rightarrow a a b b.$$

A script confirms that the grammar generates the same strings as $S \to a S b \mid \varepsilon$ up to length 10, and that $aabb$ has one parse tree.

**Balanced parentheses.** The nonempty strings of the [Dyck language](/dyck-language/), generated by $S \to ( S ) \mid S S \mid ( )$, have the grammar

$$S \to S S \mid L X \mid L R, \quad X \to S R, \quad L \to (, \quad R \to ).$$

A script confirms that both grammars generate the same 64 strings up to length 10. The string $()()()$ has 2 parse trees, from the two ways of grouping three pieces with $S \to S S$; the grammar is ambiguous, as the original is.

**Not in the form.**

- $S \to a S b$: a right side of length 3, with terminals. TERM and BIN in the conversion replace it by $S \to A X$, $X \to S B$.
- $A \to B$: a unit production. It is removed by copying the productions of $B$ to $A$.
- $A \to a B$: a terminal in a right side of length 2. It becomes $A \to T_a B$ with $T_a \to a$.
- $A \to \varepsilon$ with $A \ne S$: an $\varepsilon$-production. It is removed by [$\varepsilon$-production elimination](/epsilon-production-elimination/).
- $S \to S S \mid \varepsilon$: $S \to \varepsilon$ is present and $S$ occurs on a right side. A fresh start symbol fixes it: $S_0 \to S \mid \varepsilon$ becomes, after removing the unit production, $S_0 \to S S \mid \varepsilon$, and then the language of $S$ without $\varepsilon$ is empty, so the grammar is just $S_0 \to \varepsilon$.

## Related definitions

- **Binary normal form.** Every right side has length at most 2, with unit and $\varepsilon$-productions allowed. It is reached in $O(|G|)$ time by splitting long right sides, and CYK and Earley-style algorithms can work on it directly with a precomputed relation for unit productions and nullable symbols, which avoids the square blow-up of the full form.
- **[Greibach normal form](/greibach-normal-form/).** Every production is $A \to a B_1 \cdots B_k$, so each derivation step writes one terminal. It suits top-down parsing and pushdown automata, while Chomsky normal form suits bottom-up dynamic programming.
- **Weighted and probabilistic forms.** A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) in Chomsky normal form has a probability on each production; the [inside-outside algorithm](/inside-outside-algorithm/) and the Viterbi version of CYK use this form.
- **Other normal forms.** The [normal form conversion](/cfg-normal-form-conversion/) page lists the reduced, proper, binary and Greibach forms and the cost of reaching each. For context-sensitive grammars, the analogue is the Kuroda normal form, with productions $A B \to C D$, $A \to B C$, $A \to B$ and $A \to a$.

## References
