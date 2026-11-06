---
tag: 2CXDB3
kind: definition
slug: lalr-grammar
name: LALR grammar
aliases:
- LALR(1) grammar
area: automata-and-parsing/context-free-parsing
level: core
summary: A grammar whose LR(1) states, merged by core, produce no conflicts.
prereqs: [context-free-grammar, lr-item, lr-grammar]
see_also: [lalr-parsing, slr-grammar, lr-grammar, ll-grammar, reduce-reduce-conflict, deterministic-context-free-language, canonical-lr-parsing, knuth-lr-theorem]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7.4, Constructing LALR Parsing Tables (the definition by merging LR(1) states, and a grammar that is LR(1) but not LALR(1))
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.7, LALR(1), and Section 9.7.2, Identifying LALR(1) Conflicts
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460
  - paper: doi:10.1145/321958.321972
    title: M. Dennis Mickunas, Richard L. Lancaster and Victor B. Schneider, Transforming LR(k) grammars to LR(1), SLR(1), and (1,1) bounded right-context grammars, Journal of the ACM 23(3) (1976)
    locator: pp. 511 to 533
  - paper: doi:10.1016/S0019-9958(70)90446-8
    title: Daniel J. Rosenkrantz and Richard E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)
    locator: pp. 226 to 256 (every LL(k) grammar is LR(k))
---

An LALR(1) grammar is a [context-free grammar](/context-free-grammar/) whose canonical LR(1) automaton, after merging the states that have the same LR(0) items, has no parsing conflict. These are exactly the grammars that [LALR(1) parsing](/lalr-parsing/), the method of yacc and Bison, accepts without complaint. The class lies strictly between the [SLR(1)](/slr-grammar/) and the [LR(1)](/lr-grammar/) grammars, and it describes exactly the [deterministic context-free languages](/deterministic-context-free-language/).

## Definition

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol. Let $G = (V, \Sigma, P, S)$ be a grammar in which every nonterminal derives some terminal string, augmented with a fresh start symbol $S'$ and the production $S' \to S$. Let $\$ \notin \Sigma$ be the end marker.

An **LR(1) item** $[A \to \alpha \bullet \beta,\ a]$ is a production with a dot and a lookahead $a \in \Sigma \cup \{\$\}$; its **core** is the [LR(0) item](/lr-item/) $A \to \alpha \bullet \beta$. The **canonical LR(1) collection** of $G$ is the set of item sets reachable from $\mathrm{CLOSURE}_1(\{[S' \to \bullet S, \$]\})$ by the transitions $\mathrm{GOTO}_1$, as on the page on [canonical LR parsing](/canonical-lr-parsing/). The core of a set of items is the set of the cores of its items.

**Merging by core.** For each set $c$ of LR(0) items that is the core of some state, let $M_c$ be the union of all canonical LR(1) states with core $c$. The **LALR(1) table** has one row for each $M_c$:

- shift on $a \in \Sigma$ if some item $[A \to \alpha \bullet a \beta, b]$ is in $M_c$;
- reduce by $A \to \alpha$ on $b$ if $[A \to \alpha \bullet, b] \in M_c$ and $A \ne S'$;
- accept on $\$$ if $[S' \to S \bullet, \$] \in M_c$.

**Definition.** $G$ is **LALR(1)** if no entry of its LALR(1) table has two actions. A conflict is a [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/) between two reductions.

The rows $M_c$ correspond one to one to the states of the LR(0) automaton, and the GOTO of a merged state on a symbol is the merged state of the targets, which all have the same core. The table can be built without the canonical collection, by propagating lookaheads on the LR(0) automaton; the page on [LALR(1) parsing](/lalr-parsing/) gives this method and proves that it gives the same table.

**LALR(k).** With lookahead strings of length at most $k$ in place of single terminals, the same construction defines LALR($k$) grammars. In practice "LALR grammar" means LALR(1).

## Examples and non-examples

The following classifications were computed with the LALR(1) table, the canonical LR(1) collection, and the SLR(1) and LL(1) tests.

**LALR(1) but not SLR(1).** The grammar of assignments through pointers,

$$S \to L = R \mid R, \qquad L \to * R \mid \mathit{id}, \qquad R \to L,$$

has an LR(0) state with the items $S \to L \bullet = R$ and $R \to L \bullet$. SLR(1) reduces $R \to L$ on all of $\mathrm{FOLLOW}(R) = \{=, \$\}$ and gets a shift-reduce conflict on $=$. In that state, LALR(1) has only the lookahead $\$$ for $R \to L \bullet$, and its table of 10 states has no conflict. The canonical LR(1) collection has 14 states. The [LALR(1) parsing](/lalr-parsing/) page shows the full table.

**LR(1) but not LALR(1).** The grammar

$$S \to a A d \mid b B d \mid a B e \mid b A e, \qquad A \to c, \qquad B \to c$$

is LR(1) with 14 canonical states. After $a\,c$ the LR(1) state is $\{[A \to c \bullet, d], [B \to c \bullet, e]\}$, and after $b\,c$ it is $\{[A \to c \bullet, e], [B \to c \bullet, d]\}$. These two states have the same core and merge into one, in which both reductions have the lookaheads $\{d, e\}$: two reduce-reduce conflicts. The LALR(1) table has 13 states. The language $\{acd, bcd, ace, bce\}$ is finite, and the grammar $S \to a c d \mid b c d \mid a c e \mid b c e$ for it is LALR(1), so the failure belongs to the grammar and not to the language.

**LL(1) but not LALR(1).** The grammar

$$S \to a A \mid b B, \quad A \to C a \mid D b, \quad B \to C b \mid D a, \quad C \to E, \quad D \to E, \quad E \to \varepsilon$$

is [LL(1)](/ll-grammar/): the alternatives of $A$ and of $B$ start with different terminals. After $a$, the LR(1) state that follows the empty $E$ is $\{[C \to E \bullet, a], [D \to E \bullet, b]\}$; after $b$ it is $\{[C \to E \bullet, b], [D \to E \bullet, a]\}$. Merging them gives reduce-reduce conflicts on $a$ and on $b$. So LL(1) grammars, which are all LR(1), need not be LALR(1).

**LALR(1) but not LL(1).** The left-recursive expression grammar $E \to E + T \mid T$, $T \to a$ is SLR(1) and so LALR(1), but it is not LL(1), because $E + T$ and $T$ both start with $a$.

**LL(1) and LALR(1) but not SLR(1).** The grammar $S \to A a A b \mid B b B a$, $A \to \varepsilon$, $B \to \varepsilon$ is LL(1). In the start state SLR(1) reduces both $A \to \varepsilon$ and $B \to \varepsilon$ on $\mathrm{FOLLOW}(A) = \mathrm{FOLLOW}(B) = \{a, b\}$, a reduce-reduce conflict. LALR(1) reduces $A \to \varepsilon$ only on $a$ and $B \to \varepsilon$ only on $b$.

**Not LR at all.** An ambiguous grammar, such as $E \to E + E \mid a$, is not LR($k$) for any $k$ and so not LALR(1): after $E + E$ with $+$ next, the table has both "shift $+$" and "reduce $E \to E + E$".

## Related definitions

- **Inclusions between grammar classes.** Every LR(0) grammar is SLR(1), every SLR(1) grammar is LALR(1), and every LALR(1) grammar is LR(1); each inclusion is strict. Every LL(1) grammar is LR(1), but LL(1) is incomparable with SLR(1) and with LALR(1), by the examples above. Every LALR(1) grammar is unambiguous, because every LR(1) grammar is.
- **The languages are the same.** Every [deterministic context-free language](/deterministic-context-free-language/) has an SLR(1) grammar (Mickunas, Lancaster and Schneider), and so an LALR(1) grammar. Conversely, the language of every LR(1) grammar is deterministic, by [Knuth's theorem](/knuth-lr-theorem/). So SLR(1), LALR(1) and LR(1) grammars describe the same languages; the classes differ only as sets of grammars.
- **SLR(1) grammar.** The [SLR(1)](/slr-grammar/) table uses the same LR(0) automaton but puts each reduction on all of $\mathrm{FOLLOW}(A)$. The LALR(1) lookaheads of a completed item are a subset of $\mathrm{FOLLOW}(A)$, so an SLR(1) table without conflict gives an LALR(1) table without conflict.
- **What merging can do.** Merging states with the same core never creates a shift-reduce conflict that is not already in one of the merged LR(1) states, because every shift item of the merged state is in each part with the same core. It can create reduce-reduce conflicts, as in the examples above.
- **Testing.** Whether a grammar is LALR(1) is decidable: build the LR(0) automaton, compute the lookaheads, and check the table. The LR(0) automaton can have many states, but for programming language grammars it has a few hundred.

## References
