---
tag: W4VDM7
kind: concept
slug: first-and-follow-sets
name: FIRST and FOLLOW sets
aliases:
- FIRST
- FIRST set
- FOLLOW
- FOLLOW set
area: automata-and-parsing/parser-generators
level: core
summary: FIRST gives the terminals that begin a derivation of a symbol; FOLLOW gives the terminals that can follow a nonterminal.
prereqs: [context-free-grammar, nullable-symbol]
see_also: [ll1-parsing, ll-1-grammar, slr-parsing, lr-item-sets, lookahead-symbols, ll-k-grammar, lalr-lookahead-computation, parser-error-recovery]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.2, FIRST and FOLLOW; Section 4.4.3, LL(1) Grammars; Section 4.6.4, Constructing SLR-Parsing Tables
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (the FIRST and FOLLOW sets of LL(1) parsing)
  - paper: "Frank DeRemer and Thomas Pennello, Efficient computation of LALR(1) look-ahead sets, ACM Transactions on Programming Languages and Systems 4(4) (1982)"
    locator: the Digraph procedure, which computes sets defined by F(x) = F'(x) together with the union of F(y) over all y related to x, with one union per edge
---

FIRST and FOLLOW are two families of terminal sets computed from a [context-free grammar](/context-free-grammar/). $\mathrm{FIRST}(\alpha)$ is the set of terminals that can begin a string derived from $\alpha$, and $\mathrm{FOLLOW}(A)$ is the set of terminals that can appear right after the nonterminal $A$ in some sentential form. Together with the [nullable](/nullable-symbol/) nonterminals they are the lookahead information from which [LL(1)](/ll1-parsing/) tables, [SLR](/slr-parsing/) tables and the lookaheads of LR(1) items are built.

## In plain words

A parser that reads one word ahead must decide what to do from that word alone. To decide, it needs to know two things about the grammar. First, for each rule, which words can come at the very start of the text the rule produces. Second, for each kind of phrase, which words can come right after it.

The first list tells a top-down parser which rule to pick: if the next word can only start one of the choices, take that one. The second list matters when a phrase may be empty: then the next word belongs to whatever comes after the phrase, so the parser must know what can come after. Both lists are found by a simple procedure that keeps adding words to them until nothing changes.

## The idea

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with nonterminals $V$, terminals $\Sigma$, productions $P$ written $A \to \alpha \mid \beta$, and start symbol $S$. Greek letters are strings over $V \cup \Sigma$, $\varepsilon$ is the empty string, $n$ is the input length and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ is the size of the grammar. The end marker $\$ \notin \Sigma$ stands for the end of the input.

**Definitions.** For a string $\alpha$ and a nonterminal $A$:

- $\alpha$ is *nullable* if $\alpha \Rightarrow^* \varepsilon$;
- $\mathrm{FIRST}(\alpha) = \{\, a \in \Sigma : \alpha \Rightarrow^* a\beta \text{ for some } \beta \,\}$;
- $\mathrm{FOLLOW}(A) = \{\, a \in \Sigma \cup \{\$\} : S\$ \Rightarrow^* \alpha A a \beta \text{ for some } \alpha, \beta \,\}$.

The derivations here are between sentential forms, so a terminal is in FOLLOW(A) when some sentential form has $A$ immediately followed by it, or by a nonterminal string that derives a string starting with it. This page keeps nullability apart from FIRST. The Dragon book instead puts $\varepsilon$ into $\mathrm{FIRST}(\alpha)$ when $\alpha$ is nullable; the two conventions carry the same information.

**FIRST of a string.** For $\alpha = X_1 X_2 \cdots X_k$, $\mathrm{FIRST}(\alpha)$ is the union of $\mathrm{FIRST}(X_1), \ldots, \mathrm{FIRST}(X_j)$, where $X_j$ is the first symbol that is not nullable (or $j = k$ if all are), and $\mathrm{FIRST}(a) = \{a\}$ for a terminal $a$. So the sets for single nonterminals are all that has to be stored.

**The equations.** The three families are the least solution of these rules, read as "add while something changes":

1. $A$ is nullable if some production $A \to X_1 \cdots X_k$ has every $X_i$ nullable (in particular if $A \to \varepsilon$).
2. For each production $A \to X_1 \cdots X_k$ and each $i$ with $X_1, \ldots, X_{i-1}$ nullable, $\mathrm{FIRST}(X_i) \subseteq \mathrm{FIRST}(A)$.
3. $\$ \in \mathrm{FOLLOW}(S)$.
4. For each production $A \to \alpha B \beta$ with $B$ a nonterminal, $\mathrm{FIRST}(\beta) \subseteq \mathrm{FOLLOW}(B)$.
5. For each production $A \to \alpha B \beta$ with $\beta$ nullable, $\mathrm{FOLLOW}(A) \subseteq \mathrm{FOLLOW}(B)$.

Rule 5 carries what follows a whole phrase down to its last symbols. Nullable must be known before FIRST, and FIRST before FOLLOW, but each family is itself a fixed point because the rules refer to the sets being computed: $A \to A b$ makes $\mathrm{FIRST}(A)$ depend on itself.

**Why the iteration is right.** Start with all sets empty and apply the rules until none adds anything. Every element added has a derivation behind it, by induction on the order of additions, so the result is contained in the true sets. Conversely, induct on the length of a derivation $A \Rightarrow^* a\beta$: the first step uses some $A \to X_1 \cdots X_k$, the symbols before the one that produces $a$ derive $\varepsilon$ in fewer steps, and that symbol derives a string starting with $a$ in fewer steps, so rule 2 adds $a$. The argument for FOLLOW inducts on the derivation of the sentential form $\alpha A a \beta$ from $S\$$ in the same way. The computed sets equal the definitions for every grammar whose nonterminals are all reachable from $S$. Productions of an unreachable nonterminal still fire rules 4 and 5, so in a grammar with unreachable nonterminals the computed FOLLOW sets can be too large; remove [useless symbols](/useless-symbol-elimination/) first.

**Cost.** Each pass over the productions costs $O(|G| \cdot |\Sigma|)$ with bit-set unions, and each pass but the last adds at least one terminal to some set, so at most $|V| \cdot (|\Sigma| + 1) + 1$ passes are needed. In practice the number of passes is small. A better bound comes from viewing rule 2 as a graph on nonterminals with an edge from $A$ to $X_i$ for each use, and rule 5 likewise: the solution is a union over everything reachable in the graph. DeRemer and Pennello's Digraph procedure, a variant of the [strongly connected components](/strongly-connected-components/) search, solves such systems with one set union per edge, so all three families take $O(|G| \cdot |\Sigma|)$ time.

## Examples

**The LL(1) expression grammar.** $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to (\,E\,) \mid \mathit{id}$. The nullable nonterminals are $E'$ and $T'$.

| nonterminal | FIRST | FOLLOW |
|---|---|---|
| $E$ | $($, $\mathit{id}$ | $)$, $\$$ |
| $E'$ | $+$ | $)$, $\$$ |
| $T$ | $($, $\mathit{id}$ | $+$, $)$, $\$$ |
| $T'$ | $*$ | $+$, $)$, $\$$ |
| $F$ | $($, $\mathit{id}$ | $+$, $*$, $)$, $\$$ |

$\mathrm{FOLLOW}(T)$ gets $+$ from rule 4 on $E \to T E'$, since $\mathrm{FIRST}(E') = \{+\}$, and gets $)$ and $\$$ from rule 5, since $E'$ is nullable. Taking the productions in the order written, the iteration for FIRST changes something in three passes and confirms the fixed point in a fourth: $F$ is filled in the first pass, $T$ in the second and $E$ in the third, because each production refers to a nonterminal defined later.

**Nullable chains and left recursion.** $S \to A\,C\,a \mid B$, $A \to A\,b \mid \varepsilon$, $B \to c\,B \mid C$, $C \to d \mid \varepsilon$. All four nonterminals are nullable: $A$ and $C$ directly, $B$ through $B \to C$, and $S$ through $S \to B$.

| nonterminal | FIRST | FOLLOW |
|---|---|---|
| $S$ | $a$, $b$, $c$, $d$ | $\$$ |
| $A$ | $b$ | $a$, $b$, $d$ |
| $B$ | $c$, $d$ | $\$$ |
| $C$ | $d$ | $a$, $\$$ |

$a \in \mathrm{FIRST}(S)$ because $A$ and $C$ in $S \to A\,C\,a$ can both vanish. $\mathrm{FOLLOW}(A)$ gets $b$ from $A \to A\,b$, $d$ from $\mathrm{FIRST}(C)$ in $S \to A\,C\,a$, and $a$ because $C$ is nullable there. $\mathrm{FOLLOW}(C)$ gets $\$$ through $S \to B$ and $B \to C$ by rule 5 twice. The grammar is not LL(1): for $A$ on lookahead $b$ both $A \to A\,b$ (whose FIRST is $\{b\}$) and $A \to \varepsilon$ (whose FOLLOW contains $b$) apply, and for $S$ on lookahead $d$ both alternatives apply.

**The left-recursive expression grammar.** $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$. Nothing is nullable, every FIRST set is $\{(, \mathit{id}\}$, $\mathrm{FOLLOW}(E) = \{+, ), \$\}$ and $\mathrm{FOLLOW}(T) = \mathrm{FOLLOW}(F) = \{+, *, ), \$\}$. These are the lookaheads that an SLR(1) parser uses for the reductions $E \to T$, $T \to F$ and so on, and with them the SLR(1) table of this grammar has no conflicts.

**Where FOLLOW is too coarse.** $S \to L = R \mid R$, $L \to * R \mid \mathit{id}$, $R \to L$. Here $= \in \mathrm{FOLLOW}(R)$, because $S \to L = R$ and $L \to * R$ put $=$ after $R$ in the form $* R = R$. In the [LR(0) state](/lr-item-sets/) reached on $L$, which holds $S \to L \cdot = R$ and $R \to L \cdot$, the SLR(1) table therefore both shifts and reduces on $=$. Yet this state is entered only from the start state, where a reduction to $R$ must be followed by the end of the input, because no right sentential form begins with $R\,=$. The LALR(1) lookahead of $R \to L \cdot$ in this state is just $\$$, and the LALR(1) table has no conflict. FOLLOW is a property of the nonterminal, not of the parser state.

## Where it is used

- **LL(1) tables.** The production $A \to \alpha$ goes into the entry $M[A, a]$ for each $a \in \mathrm{FIRST}(\alpha)$, and also for each $a \in \mathrm{FOLLOW}(A)$ when $\alpha$ is nullable. A grammar is [LL(1)](/ll-1-grammar/) exactly when no entry gets two productions; see [LL(1) parsing](/ll1-parsing/).
- **SLR(1) tables.** A completed item $A \to \alpha \cdot$ calls for a reduction on every terminal of $\mathrm{FOLLOW}(A)$; see [SLR parsing](/slr-parsing/).
- **LR(1) closure.** The item $[A \to \alpha \cdot B \beta, a]$ adds $[B \to \cdot \gamma, b]$ for each $b \in \mathrm{FIRST}(\beta a)$, which is $\mathrm{FIRST}(\beta)$ plus $a$ when $\beta$ is nullable. The same computation finds the spontaneous lookaheads of [LALR lookahead computation](/lalr-lookahead-computation/), and the DeRemer and Pennello method reuses the Digraph idea for its own relations.
- **Error recovery.** Panic-mode recovery in an LL parser uses $\mathrm{FOLLOW}(A)$ as the set of tokens on which it gives up on $A$; see [parser error recovery](/parser-error-recovery/).
- **Longer lookahead.** $\mathrm{FIRST}_k$ and $\mathrm{FOLLOW}_k$ replace single terminals by strings of up to $k$ terminals and are the basis of [LL(k) grammars](/ll-k-grammar/) and of the general notion of [lookahead symbols](/lookahead-symbols/).

## References
