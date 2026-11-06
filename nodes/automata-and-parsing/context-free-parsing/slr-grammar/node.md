---
tag: 64G56H
kind: definition
slug: slr-grammar
name: SLR grammar
aliases:
- SLR(1) grammar
area: automata-and-parsing/context-free-parsing
level: core
summary: A grammar whose LR(0) automaton can be resolved using FOLLOW sets as lookaheads.
prereqs: [lr-item, first-and-follow-sets, shift-reduce-conflict, reduce-reduce-conflict]
see_also: [slr-parsing, lr0-parsing, lalr-grammar, lr-grammar, ll-grammar, canonical-lr-parsing, deterministic-context-free-language, viable-prefix]
sources:
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460 (the definition of SLR(k) grammars by lookahead sets on the LR(0) automaton)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.4, Constructing SLR-Parsing Tables (Algorithm 4.46, the definition of SLR(1), and Example 4.48, a grammar that is not SLR)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.8, SLR(1)
  - paper: doi:10.1145/321958.321972
    title: M. Dennis Mickunas, Richard L. Lancaster and Victor B. Schneider, Transforming LR(k) grammars to LR(1), SLR(1), and (1,1) bounded right-context grammars, Journal of the ACM 23(3) (1976)
    locator: pp. 511 to 533 (every LR(k) grammar can be transformed into an SLR(1) grammar for the same language)
---

An SLR(1) grammar, for "simple LR", is a [context-free grammar](/context-free-grammar/) whose LR(0) automaton has no conflict once each reduction by $A \to \beta$ is restricted to the next tokens in $\text{FOLLOW}(A)$. These are the grammars that [SLR(1) parsing](/slr-parsing/) handles: it keeps the states of [LR(0) parsing](/lr0-parsing/) and adds one token of lookahead in the simplest way. DeRemer defined the class in 1969 and 1971. It contains every LR(0) grammar and most textbook expression grammars, and it is contained in the [LALR(1)](/lalr-grammar/) grammars.

## Definition

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size.

Let $G = (V, \Sigma, P, S)$ be a grammar in which every nonterminal derives some terminal string and is reachable from $S$ (a reduced grammar, see [useless symbol elimination](/useless-symbol-elimination/)). Augment it with a fresh start symbol $S'$ and the production $S' \to S$, and let $\$ \notin \Sigma$ be the end marker. FOLLOW is computed for the augmented grammar, so $\$ \in \text{FOLLOW}(S)$; see [FIRST and FOLLOW sets](/first-and-follow-sets/).

The states of the **LR(0) automaton** are the sets of [LR(0) items](/lr-item/) reachable from $\text{CLOSURE}(\{S' \to \cdot S\})$ by GOTO. In a state $I$:

- a **shift item** is an item $B \to \alpha \cdot a \gamma$ with $a \in \Sigma$; it calls for shifting $a$;
- a **complete item** is an item $A \to \beta \cdot$; for $A \ne S'$ it calls for reducing by $A \to \beta$ on every $a \in \text{FOLLOW}(A)$, and the item $S' \to S \cdot$ calls for accepting on $\$$.

**Definition.** $G$ is **SLR(1)** if, in every state $I$ of its LR(0) automaton,

1. for every complete item $A \to \beta \cdot$ and every shift item $B \to \alpha \cdot a \gamma$ in $I$, $a \notin \text{FOLLOW}(A)$ (no [shift-reduce conflict](/shift-reduce-conflict/)); and
2. for every two different complete items $A \to \beta \cdot$ and $B \to \gamma \cdot$ in $I$, $\text{FOLLOW}(A) \cap \text{FOLLOW}(B) = \emptyset$ (no [reduce-reduce conflict](/reduce-reduce-conflict/)).

Equivalently, the SLR(1) parsing table built from these actions has at most one action in each entry. The accept item counts as a reduction by $S' \to S$ on $\text{FOLLOW}(S') = \{\$\}$.

**SLR(k).** DeRemer's definition is for every $k \ge 0$: replace $\text{FOLLOW}(A)$ by $\text{FOLLOW}_k(A)$, the strings of length $k$ (or shorter, ending at $\$$) that can follow $A$, and compare them with the strings of length $k$ that can start after the dot of each shift item. In practice "SLR grammar" means SLR(1).

The test is mechanical: build the LR(0) automaton, compute FOLLOW, and check every state. The number of states can be exponential in $|G|$ in the worst case, but for programming language grammars it is a few hundred.

## Examples and non-examples

The following classifications, state counts and FOLLOW sets were computed by a script that builds the LR(0), SLR(1), LALR(1) and canonical LR(1) tables of each grammar. Strict LR(0) here means the automaton with $S' \to S$ and no end marker.

**SLR(1) but not LR(0): expressions.** The grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to ( E ) \mid \mathtt{id}$$

has 12 LR(0) states. The state $\{E \to T \cdot,\ T \to T \cdot * F\}$ has a conflict in LR(0): reduce, or shift $*$. Since $\text{FOLLOW}(E) = \{+, ), \$\}$ does not contain $*$, SLR(1) reduces on $+$, $)$, $\$$ and shifts on $*$. The same holds for $\{E \to E + T \cdot,\ T \to T \cdot * F\}$ and for $\{S' \to E \cdot,\ E \to E \cdot + T\}$, where accepting happens only on $\$$. The SLR(1) table has no conflict. This is the standard example of the method.

**SLR(1) with empty productions.** $S \to a\, S\, b \mid \varepsilon$ is not LR(0): after $a$, the state has the complete item $S \to \cdot$ and the shift item $S \to \cdot a S b$. With $\text{FOLLOW}(S) = \{b, \$\}$, SLR(1) reduces on $b$ and $\$$ and shifts on $a$, with no conflict (5 states). The left-recursive $S \to S\, a \mid \varepsilon$ is SLR(1) as well.

**Not SLR(1), but LALR(1): assignments.** The grammar

$$S \to L = R \mid R, \qquad L \to * R \mid \mathtt{id}, \qquad R \to L$$

is unambiguous. Its LR(0) state $\{S \to L \cdot = R,\ R \to L \cdot\}$ shifts $=$, and since $\text{FOLLOW}(R) = \{=, \$\}$, SLR(1) also reduces $R \to L$ on $=$: a shift-reduce conflict. In this state $R$ can only be followed by $\$$ (an $R$ followed by $=$ must come after a $*$), which is what LALR(1) finds: its 10-state table has no conflict.

**Not SLR(1), but LALR(1) and LL(1): empty alternatives.** $S \to A\, a\, A\, b \mid B\, b\, B\, a$, $A \to \varepsilon$, $B \to \varepsilon$. In the start state both $A \to \cdot$ and $B \to \cdot$ are complete, and $\text{FOLLOW}(A) = \text{FOLLOW}(B) = \{a, b\}$: reduce-reduce conflicts on $a$ and on $b$. Yet at the start an $A$ is followed by $a$ and a $B$ by $b$, and LALR(1) separates them. The grammar is [LL(1)](/ll-grammar/), so LL(1) grammars need not be SLR(1).

**Not SLR(1) because of FOLLOW in other contexts.** $S \to A\, a \mid B\, b \mid d\, A\, b \mid e\, B\, a$, $A \to c$, $B \to c$. After $c$ at the start, the state $\{A \to c \cdot,\ B \to c \cdot\}$ has reduce-reduce conflicts on $a$ and $b$, because the later alternatives put $b$ into $\text{FOLLOW}(A)$ and $a$ into $\text{FOLLOW}(B)$. The grammar is LALR(1). Without the alternatives $d\,A\,b$ and $e\,B\,a$ it is SLR(1).

**Not SLR(1) because ambiguous.** $E \to E + E \mid \mathtt{id}$ and the dangling-else grammar $S \to i\, E\, t\, S \mid i\, E\, t\, S\, e\, S \mid a$, $E \to b$ are ambiguous, so they have a conflict in every LR table: after $E + E$ on $+$, and after $i\,E\,t\,S$ on $e$.

## Related definitions

- **Inclusions.** Every strict LR(0) grammar is SLR(1), since SLR(1) only removes actions from the LR(0) table. Every SLR(1) grammar is [LALR(1)](/lalr-grammar/), because the LALR(1) lookahead set of a complete item $A \to \beta \cdot$ in a state is a subset of $\text{FOLLOW}(A)$; and every LALR(1) grammar is [LR(1)](/lr-grammar/). All these inclusions are strict, by the examples above. So every SLR(1) grammar is unambiguous.
- **LL(1).** [LL(1)](/ll-grammar/) and SLR(1) are incomparable: the expression grammar is SLR(1) and left recursive, so not LL(1), and the grammar with $A \to \varepsilon$, $B \to \varepsilon$ is LL(1) but not SLR(1).
- **Languages.** Mickunas, Lancaster and Schneider (1976) showed that every LR($k$) grammar can be transformed into an SLR(1) grammar for the same language. So the SLR(1) grammars describe exactly the [deterministic context-free languages](/deterministic-context-free-language/), the same languages as LALR(1) and LR(1); the classes differ only as sets of grammars.
- **Viable prefixes.** The LR(0) automaton recognizes the [viable prefixes](/viable-prefix/) of $G$. The SLR(1) condition adds one token of lookahead to its complete items, approximated by FOLLOW, which ignores the state the parser is in. LALR(1) replaces FOLLOW by lookaheads that depend on the state, and canonical LR(1) splits the states themselves.
- **SLR parsing.** A grammar is SLR(1) exactly when the [SLR(1) parsing](/slr-parsing/) table has no multiple entries; the parser then runs in time linear in $n$.

## References
