---
tag: VY3HN5
kind: definition
slug: operator-precedence-grammar
name: Operator precedence grammar
aliases:
- operator grammar
area: automata-and-parsing/parser-generators
level: intro
summary: A grammar with no adjacent nonterminals and no epsilon productions, so precedence relations between terminals decide parsing.
prereqs: [context-free-grammar, operator-grammar]
see_also: [operator-precedence-parsing, shunting-yard-algorithm, pratt-parsing, shift-reduce-parsing, handle, lr-k-grammar, ambiguity, yacc]
sources:
  - paper: doi:10.1145/321172.321179
    title: Robert W. Floyd, Syntactic analysis and operator precedence, Journal of the ACM 10(3) (1963)
    locator: pp. 316 to 333 (operator grammars, the three precedence relations, and precedence functions)
  - book: isbn:9780201100884
    title: Alfred V. Aho, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, first edition
    locator: Section 4.6, Operator-Precedence Parsing (the relations, LEADING and TRAILING, precedence functions)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing, the section on precedence parsing
---

An operator precedence grammar is an [operator grammar](/operator-grammar/), that is, a [context-free grammar](/context-free-grammar/) with no $\varepsilon$-production and no right side with two adjacent nonterminals, in which at most one of three precedence relations $\lessdot$, $\doteq$, $\gtrdot$ holds between each ordered pair of terminals. Floyd defined the class in 1963. For such a grammar the relations alone find each [handle](/handle/) of a [shift-reduce parser](/shift-reduce-parsing/): the parser compares the terminal nearest the top of its stack with the next input token, and never looks at the nonterminals. The table has one row and one column for each terminal, so it is small, and it can often be replaced by two integer functions.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, $n$ is the input length and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ is the grammar size, as on all parsing pages of this site. Letters $a, b$ are terminals, $A, B, C$ nonterminals, and Greek letters are strings over $V \cup \Sigma$. The end marker $\$ \notin \Sigma$ is placed before and after the input.

**Operator grammar.** $G$ is an *operator grammar* if no production has the form $A \to \varepsilon$ and no right side contains two consecutive nonterminals $B C$.

**LEADING and TRAILING.** For a nonterminal $A$,

$$\mathrm{LEADING}(A) = \{ a \in \Sigma : A \Rightarrow^+ \gamma a \delta,\ \gamma \in V \cup \{\varepsilon\} \},$$

$$\mathrm{TRAILING}(A) = \{ a \in \Sigma : A \Rightarrow^+ \gamma a \delta,\ \delta \in V \cup \{\varepsilon\} \}.$$

So $\mathrm{LEADING}(A)$ holds the terminals that can appear first in a [sentential form](/sentential-form/) derived from $A$, possibly after one nonterminal, and $\mathrm{TRAILING}(A)$ the terminals that can appear last, possibly before one nonterminal.

**The relations.** For terminals $a, b$:

- $a \doteq b$ if some production has the form $A \to \alpha\, a\, \beta\, b\, \gamma$ with $\beta \in V \cup \{\varepsilon\}$;
- $a \lessdot b$ if some production has the form $A \to \alpha\, a\, B\, \gamma$ with $b \in \mathrm{LEADING}(B)$;
- $a \gtrdot b$ if some production has the form $A \to \alpha\, B\, b\, \gamma$ with $a \in \mathrm{TRAILING}(B)$.

The end marker is added with $\$ \lessdot b$ for each $b \in \mathrm{LEADING}(S)$ and $a \gtrdot \$$ for each $a \in \mathrm{TRAILING}(S)$. The symbols are not the orders $<$, $=$, $>$: a relation need not be transitive, and $a \lessdot a$ is allowed.

**Operator precedence grammar.** An operator grammar $G$ is an *operator precedence grammar* if for every pair $(a, b)$ of symbols in $\Sigma \cup \{\$\}$ at most one of $a \lessdot b$, $a \doteq b$, $a \gtrdot b$ holds. The *precedence matrix* lists the relation of each pair, with an empty cell where none holds.

**Computing the sets.** LEADING and TRAILING are the least sets that satisfy, for each production $A \to X_1 \cdots X_m$:

- if $X_1 \in \Sigma$, then $X_1 \in \mathrm{LEADING}(A)$;
- if $X_1 \in V$, then $\mathrm{LEADING}(X_1) \subseteq \mathrm{LEADING}(A)$, and if also $m \ge 2$ then $X_2 \in \mathrm{LEADING}(A)$;

and the mirror rules with $X_m$ and $X_{m-1}$ for TRAILING. They are found by passes over the productions until no set changes. Each pass except the last adds a terminal to some set, so there are at most $2|V| \cdot |\Sigma| + 1$ passes of $O(|G|)$ set operations each.

*Proof that the rules give LEADING.* Write $L'$ for the least solution. Each rule adds a terminal $a$ to $L'(A)$ only when $A \Rightarrow^+ \gamma a \delta$ with $\gamma \in V \cup \{\varepsilon\}$: the first two rules give a derivation of one step, and the third extends a derivation $X_1 \Rightarrow^+ \gamma a \delta$ to $A \Rightarrow X_1 X_2 \cdots X_m \Rightarrow^+ \gamma a \delta X_2 \cdots X_m$. So $L'(A) \subseteq \mathrm{LEADING}(A)$. For the converse, take a shortest derivation $A \Rightarrow X_1 \cdots X_m \Rightarrow^* \gamma a \delta$ with $\gamma \in V \cup \{\varepsilon\}$, and use induction on its length. In an operator grammar no nonterminal derives $\varepsilon$, so every symbol of a sentential form keeps at least one symbol in each later form. If the $a$ comes from $X_1 \in \Sigma$ or $X_2 \in \Sigma$, the first two rules apply. Otherwise, at most one symbol stands before $a$ in the final form, so all of that prefix comes from $X_1$: the terminal $a$ comes from $X_1$, which is then a nonterminal with a shorter derivation $X_1 \Rightarrow^+ \gamma a \delta'$, and by induction $a \in L'(X_1) \subseteq L'(A)$. The case of TRAILING is the mirror image. $\square$

## Examples and non-examples

**The expression grammar.** $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$ is an operator grammar. Its sets are $\mathrm{LEADING}(E) = \{+, *, (, \mathit{id}\}$, $\mathrm{LEADING}(T) = \{*, (, \mathit{id}\}$, $\mathrm{LEADING}(F) = \{(, \mathit{id}\}$, and TRAILING is the same with $)$ in place of $($. The precedence matrix has the row symbol on the left of the relation and the column symbol on the right:

| | $+$ | $*$ | $($ | $)$ | $\mathit{id}$ | $\$$ |
|---|---|---|---|---|---|---|
| $+$ | $\gtrdot$ | $\lessdot$ | $\lessdot$ | $\gtrdot$ | $\lessdot$ | $\gtrdot$ |
| $*$ | $\gtrdot$ | $\gtrdot$ | $\lessdot$ | $\gtrdot$ | $\lessdot$ | $\gtrdot$ |
| $($ | $\lessdot$ | $\lessdot$ | $\lessdot$ | $\doteq$ | $\lessdot$ | |
| $)$ | $\gtrdot$ | $\gtrdot$ | | $\gtrdot$ | | $\gtrdot$ |
| $\mathit{id}$ | $\gtrdot$ | $\gtrdot$ | | $\gtrdot$ | | $\gtrdot$ |
| $\$$ | $\lessdot$ | $\lessdot$ | $\lessdot$ | | $\lessdot$ | |

No cell has two relations, so the grammar is an operator precedence grammar. The matrix encodes the usual rules: $+ \lessdot *$ because $*$ binds more tightly, $+ \gtrdot +$ because $+$ groups to the left, and an empty cell such as $(\mathit{id}, \mathit{id})$ is a syntax error. In the input $\mathit{id} + \mathit{id} * \mathit{id}$ the relations between neighbouring terminals are

$$\$ \lessdot \mathit{id} \gtrdot + \lessdot \mathit{id} \gtrdot * \lessdot \mathit{id} \gtrdot \$,$$

and each pair $\lessdot \ldots \gtrdot$ with nothing of the same kind inside marks a handle: here each $\mathit{id}$. After these are reduced, the relations between the remaining terminals give $\$ \lessdot + \lessdot * \gtrdot \$$, and the handle is $E * E$ around the $*$. A nonterminal never takes part in a comparison, which is why the grammar must keep terminals between nonterminals.

**Precedence functions.** For this matrix there are integer functions $f$ and $g$ with $f(a) < g(b)$ when $a \lessdot b$, $f(a) = g(b)$ when $a \doteq b$, and $f(a) > g(b)$ when $a \gtrdot b$:

| | $+$ | $*$ | $($ | $)$ | $\mathit{id}$ | $\$$ |
|---|---|---|---|---|---|---|
| $f$ | 2 | 4 | 0 | 4 | 4 | 0 |
| $g$ | 1 | 3 | 5 | 0 | 5 | 0 |

They come from a graph with a node $f_a$ and a node $g_b$ for each terminal, the nodes of each pair $a \doteq b$ merged, an edge $f_a \to g_b$ for $a \gtrdot b$ and an edge $g_b \to f_a$ for $a \lessdot b$: the value of a node is the length of the longest path that starts there. Functions exist exactly when this graph has no cycle. They store $2|\Sigma|$ numbers instead of $|\Sigma|^2$ cells, but they lose the empty cells: $f(\mathit{id}) = 4 < 5 = g(\mathit{id})$ claims $\mathit{id} \lessdot \mathit{id}$, so a parser with functions detects the error $\mathit{id}\ \mathit{id}$ later, when it tries to reduce.

**Not an operator grammar: adjacent nonterminals.** $S \to A B$, $A \to a$, $B \to b$ has the right side $A B$. Between $A$ and $B$ there is no terminal to compare, so the relations cannot see the boundary. The same language has the operator grammar $S \to a b$.

**Not an operator grammar: an empty right side.** $E' \to + T E' \mid \varepsilon$, from the [LL(1)](/ll-1-grammar/) form of the expression grammar, has an $\varepsilon$-production and the adjacent nonterminals $T E'$. Grammars written for top-down parsing are usually not operator grammars.

**An operator grammar that is not operator precedence: ambiguity.** $E \to E + E \mid E * E \mid \mathit{id}$ is an operator grammar, but the production $E \to E + E$ gives both $+ \lessdot +$ (the $+$ before $E$, with $+ \in \mathrm{LEADING}(E)$) and $+ \gtrdot +$ (the $+$ after $E$, with $+ \in \mathrm{TRAILING}(E)$). The pairs $(+, *)$, $(*, +)$ and $(*, *)$ have two relations in the same way. The grammar does not say how operators group; a hand-written matrix that says so turns the method into the [shunting-yard algorithm](/shunting-yard-algorithm/).

**An operator grammar that is not operator precedence: the dangling else.** $S \to i\, S \mid i\, S\, e\, S \mid x$ is an operator grammar. The production $S \to i S e S$ gives $i \doteq e$, and $S \to i S$ puts $i$ in $\mathrm{TRAILING}(S)$, so the same production also gives $i \gtrdot e$. The conflict is the familiar question of which $i$ an $e$ belongs to.

**Operator precedence, yet ambiguous.** $E \to F \mid G$, $F \to \mathit{id}$, $G \to \mathit{id}$ is an operator precedence grammar: the only relations are $\$ \lessdot \mathit{id}$ and $\mathit{id} \gtrdot \$$. The sentence $\mathit{id}$ still has two parse trees. The relations fix where each handle is, but they never look at nonterminal names, so they cannot choose between two productions with the same terminals in the same places. An operator precedence parser builds the tree without these names, or the grammar must avoid such pairs.

## Related definitions

- An [operator grammar](/operator-grammar/) is the wider class without the condition on the relations.
- [Operator-precedence parsing](/operator-precedence-parsing/) is the shift-reduce algorithm that uses the matrix; the [shunting-yard algorithm](/shunting-yard-algorithm/) and [Pratt parsing](/pratt-parsing/) are close relatives that take precedences and associativities directly.
- A *simple precedence grammar* defines the three relations between all grammar symbols, nonterminals included, and has no condition on adjacent nonterminals.
- Operator precedence grammars are not a subclass of the [LR(k) grammars](/lr-k-grammar/): the grammar $E \to F \mid G$, $F \to \mathit{id}$, $G \to \mathit{id}$ above is operator precedence and ambiguous, so it is LR(k) for no $k$. [Yacc](/yacc/) keeps the convenience of precedence for operators only, through `%left`, `%right` and `%nonassoc`, and uses it to settle [shift-reduce conflicts](/shift-reduce-conflict/) of an LALR(1) table.
- A [handle](/handle/) is the substring that a bottom-up parser reduces next; the relations mark its left end by $\lessdot$ and its right end by $\gtrdot$.

## References
