---
tag: KW1F8D
kind: definition
slug: operator-grammar
name: Operator grammar
aliases:
- operator precedence grammar
area: automata-and-parsing/context-free-parsing
level: core
summary: A grammar with no adjacent nonterminals, enabling precedence-based parsing.
prereqs: [context-free-grammar, parse-tree]
see_also: [operator-precedence-parsing, shift-reduce-parsing, shunting-yard-algorithm, pratt-parsing, ambiguity, handle, chomsky-normal-form, lr-grammar]
sources:
  - paper: doi:10.1145/321172.321179
    title: Robert W. Floyd, Syntactic analysis and operator precedence, Journal of the ACM 10(3) (1963)
    locator: pp. 316 to 333 (operator grammars, the three precedence relations and precedence grammars)
  - book: isbn:9780201100884
    title: Alfred V. Aho, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, first edition
    locator: Section 4.6, Operator-Precedence Parsing (the definition of an operator grammar, LEADING and TRAILING, and the relations)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Section 9.2, Precedence Parsing
---

An operator grammar is a [context-free grammar](/context-free-grammar/) in which no right side is empty and no right side has two nonterminals next to each other. Between any two nonterminals of a sentential form there is then at least one terminal, which Floyd (1963) used to parse with relations between terminals only. If, in addition, at most one of the three relations $\lessdot$, $\doteq$, $\gtrdot$ holds between each pair of terminals, the grammar is an *operator precedence grammar*, and [operator-precedence parsing](/operator-precedence-parsing/) applies to it.

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. Lowercase letters $a, b$ are terminals, uppercase letters are nonterminals, and $\$ \notin \Sigma$ marks both ends of the input.

**Operator grammar.** $G$ is an *operator grammar* if no production has the form $A \to \varepsilon$ and no right side has the form $\alpha B C \beta$ with $B, C \in V$. By induction on the derivation, every sentential form of an operator grammar also has no two adjacent nonterminals, so its nonterminals are separated by terminals. Since there are no empty productions, $\varepsilon \notin L(G)$.

**Leading and trailing terminals.** For $A \in V$,

$$\mathrm{LEADING}(A) = \{ a : A \Rightarrow^+ \gamma a \delta, \ \gamma \in V \cup \{\varepsilon\} \}, \qquad \mathrm{TRAILING}(A) = \{ a : A \Rightarrow^+ \delta a \gamma, \ \gamma \in V \cup \{\varepsilon\} \}.$$

In an operator grammar, these are the first and last terminals that can appear in a string derived from $A$, possibly after one nonterminal. They are the least sets with: if $A \to a \ldots$ or $A \to B a \ldots$, then $a \in \mathrm{LEADING}(A)$, and if $A \to B \ldots$, then $\mathrm{LEADING}(B) \subseteq \mathrm{LEADING}(A)$; and symmetrically for TRAILING from the right end.

**Precedence relations.** For terminals $a, b$:

- $a \doteq b$ if some right side contains $a b$ or $a B b$;
- $a \lessdot b$ if some right side contains $a B$ with $b \in \mathrm{LEADING}(B)$;
- $a \gtrdot b$ if some right side contains $B b$ with $a \in \mathrm{TRAILING}(B)$.

For the end marker, $\$ \lessdot b$ for $b \in \mathrm{LEADING}(S)$ and $a \gtrdot \$$ for $a \in \mathrm{TRAILING}(S)$. In words, $a \lessdot b$ says that $b$ starts a phrase nested inside the right operand of $a$, $a \gtrdot b$ says that a phrase ending with $a$ is complete when $b$ comes, and $a \doteq b$ says that they belong to the same phrase. The three relations are not orders: none of them needs to be reflexive, symmetric or transitive.

**Operator precedence grammar.** An operator grammar is an *operator precedence grammar* if for every pair of terminals (including $\$$) at most one of the three relations holds. The table of the relations is the *precedence matrix*.

## Examples and non-examples

**The expression grammar.** $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$ is an operator grammar. Here $\mathrm{LEADING}(E) = \{+, *, (, id\}$, $\mathrm{LEADING}(T) = \{*, (, id\}$, $\mathrm{LEADING}(F) = \{(, id\}$, and TRAILING is the same with $)$ in place of $($. The relations, row $a$ and column $b$:

| $a \backslash b$ | $id$ | $+$ | $*$ | $($ | $)$ | $\$$ |
|---|---|---|---|---|---|---|
| $id$ | | $\gtrdot$ | $\gtrdot$ | | $\gtrdot$ | $\gtrdot$ |
| $+$ | $\lessdot$ | $\gtrdot$ | $\lessdot$ | $\lessdot$ | $\gtrdot$ | $\gtrdot$ |
| $*$ | $\lessdot$ | $\gtrdot$ | $\gtrdot$ | $\lessdot$ | $\gtrdot$ | $\gtrdot$ |
| $($ | $\lessdot$ | $\lessdot$ | $\lessdot$ | $\lessdot$ | $\doteq$ | |
| $)$ | | $\gtrdot$ | $\gtrdot$ | | $\gtrdot$ | $\gtrdot$ |
| $\$$ | $\lessdot$ | $\lessdot$ | $\lessdot$ | $\lessdot$ | | |

No cell has two relations, so this is an operator precedence grammar. The matrix says that $+ \lessdot *$ and $* \gtrdot +$: $*$ binds more tightly. It also says $+ \gtrdot +$, so $a + b + c$ groups as $(a + b) + c$: left associativity. The empty cells are errors, such as $id$ followed by $($.

**Ambiguous, but still an operator grammar.** $E \to E + E \mid E * E \mid ( E ) \mid id$ is an operator grammar, but both $+ \lessdot +$ (from $E +$ followed by $E$ with $+ \in \mathrm{LEADING}(E)$) and $+ \gtrdot +$ hold, and the same for the other three pairs of operators. It is not an operator precedence grammar. Operator precedence parsers for such grammars take the matrix from declared precedences and associativities instead of computing it.

**Unary minus.** $E \to E - T \mid T$, $T \to - T \mid id$ is an operator grammar with one conflict: $- \lessdot -$, because a binary minus can be followed by a unary one, and $- \gtrdot -$, because a unary minus can end a left operand. Practical operator precedence parsers let the lexer give unary and binary minus different tokens.

**Not an operator grammar.** $E \to E A E \mid id$, $A \to + \mid *$ has the adjacent nonterminals $E A$. Substituting the productions of $A$ gives $E \to E + E \mid E * E \mid id$, which is an operator grammar for the same language. $S \to a S b \mid \varepsilon$ is not an operator grammar because of the empty production; $S \to a S b \mid a b$ is one, for $\{a^m b^m : m \ge 1\}$.

**Ambiguity in the labels.** $S \to A \mid B$, $A \to a$, $B \to a$ is an operator precedence grammar ($\$ \lessdot a \gtrdot \$$), yet it is ambiguous. The relations see only terminals, so they fix the shape of the tree but not the names of its inner nodes.

**Every language without $\varepsilon$.** Every context-free language $L$ with $\varepsilon \notin L$ has an operator grammar. Start from a grammar in [Chomsky normal form](/chomsky-normal-form/) and use, for each nonterminal $A$ and terminal $a$, a new nonterminal $A^a$ for the nonempty strings $u$ with $u a \in L(A)$. Since $u a \in L(BC)$ with $u \ne \varepsilon$ means $u = x b y$ with $x b \in L(B)$ and $y a \in L(C)$, a production $A \to B C$ gives

$$A^a \to B^b \, b \, C^a \mid b \, C^a \mid B^b \, b \mid b,$$

for every terminal $b$, where the version without $B^b$ is kept only if $b \in L(B)$, that is, $B \to b \in R$, and the version without $C^a$ only if $C \to a \in R$. The new start symbol has $S_0 \to S^a \, a$ for each $a$, and $S_0 \to a$ if $S \to a \in R$. Every right side alternates nonterminals and terminals, so the result is an operator grammar, of size $O(|G| \cdot |\Sigma|^2)$. The precedence relations of the result usually conflict, so this shows only that the operator form is no restriction on the language.

## Related definitions

- [Operator-precedence parsing](/operator-precedence-parsing/): the [shift-reduce parser](/shift-reduce-parsing/) that uses the precedence matrix to find each [handle](/handle/), shifting under $\lessdot$ and $\doteq$ and reducing under $\gtrdot$.
- *Precedence functions*: two maps $f, g$ from terminals to integers with $f(a) < g(b)$ when $a \lessdot b$, $f(a) = g(b)$ when $a \doteq b$, and $f(a) > g(b)$ when $a \gtrdot b$. They replace the matrix by two arrays when they exist, at the price of turning error cells into some relation.
- *Simple precedence grammars* (Wirth and Weber, 1966) define the three relations between all grammar symbols, not only terminals, and need no operator form.
- *Floyd languages*: the languages of operator precedence grammars. They are deterministic context-free languages, and for a fixed precedence matrix they are closed under union, intersection and complement.
- [Shunting yard](/shunting-yard-algorithm/) and [Pratt parsing](/pratt-parsing/) use the same idea of comparing operator precedences, specified directly by binding powers instead of by a grammar.
- [LR grammars](/lr-grammar/) handle all deterministic languages and do not need the operator form, which is why LR parser generators replaced operator precedence for general syntax.

## References
