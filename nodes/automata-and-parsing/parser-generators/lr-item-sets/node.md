---
tag: TC4W90
kind: concept
slug: lr-item-sets
name: LR item sets and canonical collection
aliases:
- LR(0) items
- LR automaton
- closure and goto
area: automata-and-parsing/parser-generators
level: core
summary: Sets of dotted productions closed under closure and goto that form the states of an LR parser.
prereqs: [lr-item, viable-prefix, shift-reduce-parsing]
see_also: [lr0-parsing, slr-parsing, lalr-parsing, canonical-lr-parsing, lr-parse-table, lalr-lookahead-computation, subset-construction, parser-table-construction]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.2, Items and the LR(0) Automaton (CLOSURE, GOTO, the canonical collection, kernel items); Section 4.6.5, Viable Prefixes; Section 4.7.2, Constructing LR(1) Sets of Items
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (states as sets of dotted productions, and the construction of the states from the start state)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing (the LR(0) automaton as the subset construction of a nondeterministic automaton of items)
---

The canonical collection of LR(0) item sets of a [context-free grammar](/context-free-grammar/) is a finite automaton whose states are sets of [LR items](/lr-item/) and whose transitions are given by a GOTO function. It starts from the closure of the item $S' \to \cdot\, S$ and adds GOTO of each state on each grammar symbol until no new set appears. A path from the start state spells a [viable prefix](/viable-prefix/), and the state at its end is exactly the set of items valid for that prefix, which is what a [shift-reduce parser](/shift-reduce-parsing/) needs to decide its next move. Every LR method ([LR(0)](/lr0-parsing/), [SLR](/slr-parsing/), [LALR](/lalr-parsing/), [canonical LR(1)](/canonical-lr-parsing/)) builds its [parse table](/lr-parse-table/) from this automaton or from its version with lookaheads.

## In plain words

An LR parser reads tokens and keeps a stack of what it has read so far. At each moment it is partway through several rules of the grammar at once, and an item records one of these partial matches. The parser needs to know the whole set of partial matches that fit the stack, but it cannot afford to recompute it at every step.

The canonical collection precomputes all such sets. Start with "I am at the beginning of the whole program". Whenever a rule is expected to continue with some construct, add the rules for that construct at their beginning. Then ask, for each symbol, "what is the set after I see this symbol?" and repeat with each new set. The grammar is finite, so this ends. Each set becomes one state, and each "after this symbol" becomes an arrow between states.

## The idea

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, $n$ is the input length and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ is the grammar size, as on all parsing pages of this site. The *augmented grammar* adds a new start symbol $S'$ and the production $S' \to S$. An item $A \to \alpha \cdot \beta$ is a production $A \to \alpha\beta$ with a dot; $G$ has exactly $|G|$ items, plus one for $S' \to S$ and one for $S' \to S\,\cdot$. We assume that every nonterminal derives some terminal string; [useless symbols](/useless-symbol-elimination/) can be removed first.

**CLOSURE and GOTO.** For a set $I$ of items, $\mathrm{CLOSURE}(I)$ is the least set that contains $I$ and satisfies

$$A \to \alpha \cdot B \beta \in \mathrm{CLOSURE}(I),\ B \to \gamma \in P \implies B \to \cdot\, \gamma \in \mathrm{CLOSURE}(I).$$

For a grammar symbol $X \in V \cup \Sigma$,

$$\mathrm{GOTO}(I, X) = \mathrm{CLOSURE}\bigl(\{ A \to \alpha X \cdot \beta : A \to \alpha \cdot X \beta \in I \}\bigr).$$

**The canonical collection.** Let $I_0 = \mathrm{CLOSURE}(\{S' \to \cdot\, S\})$. The canonical collection $\mathcal{C}$ is the least set of item sets that contains $I_0$ and contains $\mathrm{GOTO}(I, X)$ whenever $I \in \mathcal{C}$ and $\mathrm{GOTO}(I, X) \ne \emptyset$. As an automaton, its states are the sets of $\mathcal{C}$, its start state is $I_0$, and it has a transition $I \xrightarrow{X} \mathrm{GOTO}(I, X)$. It is a deterministic automaton over the alphabet $V \cup \Sigma$.

```pseudo id=main
CANONICAL-COLLECTION(G)                    ▷ G augmented with S′ → S
L1  I0 ← CLOSURE({S′ → • S})
L2  states ← [I0]; index[kernel of I0] ← 0; q ← 0
L3  while q < |states| do
L4      for each symbol X after a dot in states[q] do
L5          K ← { A → αX • β : A → α • Xβ ∈ states[q] }      ▷ the kernel of the next state
L6          if K is not in index then index[K] ← |states|; append CLOSURE(K) to states
L7          GOTO[q, X] ← index[K]
L8      q ← q + 1
L9  return states and GOTO
```

The *kernel* of a state is its set of items with the dot not at the left end, plus $S' \to \cdot\, S$ in $I_0$. The other items, of the form $B \to \cdot\, \gamma$, follow from the kernel by CLOSURE, so line L6 compares kernels only, and a generator stores only the kernels.

**The automaton recognizes viable prefixes.** An item $A \to \beta_1 \cdot \beta_2$ is *valid* for a string $\gamma \in (V \cup \Sigma)^*$ if there is a rightmost derivation $S' \Rightarrow_{rm}^* \delta A w \Rightarrow_{rm} \delta \beta_1 \beta_2 w$ with $\gamma = \delta\beta_1$ and $w \in \Sigma^*$. A [viable prefix](/viable-prefix/) is a string with at least one valid item. Let $V(\gamma)$ be the set of items valid for $\gamma$.

*Theorem.* For every $\gamma \in (V \cup \Sigma)^*$, $V(\gamma)$ is the state reached from $I_0$ by the path labelled $\gamma$, or $V(\gamma) = \emptyset$ if no such path exists. In particular, $\gamma$ is a viable prefix if and only if the path exists.

*Proof.* We show $V(\varepsilon) = I_0$ and $V(\gamma X) = \mathrm{GOTO}(V(\gamma), X)$, with $\mathrm{GOTO}(\emptyset, X) = \emptyset$; induction on $|\gamma|$ then gives the theorem.

1. *Closure step.* If $A \to \alpha \cdot B \beta$ is valid for $\gamma$ and $B \to \eta \in P$, then $B \to \cdot\, \eta$ is valid for $\gamma$. Take the derivation $S' \Rightarrow_{rm}^* \delta A w \Rightarrow_{rm} \delta \alpha B \beta w$ with $\gamma = \delta\alpha$. Since every symbol derives a terminal string, $\beta \Rightarrow_{rm}^* x$ for some $x \in \Sigma^*$, and rewriting $\beta$ first keeps the derivation rightmost: $S' \Rightarrow_{rm}^* \delta\alpha B x w \Rightarrow_{rm} \delta\alpha\, \eta\, x w$. This shows $B \to \cdot\, \eta$ valid for $\delta\alpha = \gamma$. So each $V(\gamma)$ is closed under CLOSURE.
2. *Start.* The derivation of length zero makes $S' \to \cdot\, S$ valid for $\varepsilon$, and step 1 gives $I_0 \subseteq V(\varepsilon)$. Conversely an item $B \to \cdot\, \eta$ valid for $\varepsilon$ comes from a derivation $S' \Rightarrow_{rm}^* B w \Rightarrow_{rm} \eta w$; by induction on its length, the occurrence of $B$ was created by a step $C \to B \mu$ with $C \to \cdot\, B\mu$ valid for $\varepsilon$, or $B = S'$. So $V(\varepsilon) \subseteq I_0$.
3. *Kernel items.* $A \to \alpha X \cdot \beta$ is valid for $\gamma X$ exactly when $A \to \alpha \cdot X \beta$ is valid for $\gamma$: the same derivation witnesses both, with $\delta$ unchanged. So the kernel of $\mathrm{GOTO}(V(\gamma), X)$ is the set of items of $V(\gamma X)$ whose dot is not at the left, and with step 1, $\mathrm{GOTO}(V(\gamma), X) \subseteq V(\gamma X)$.
4. *Items with the dot at the left.* Let $B \to \cdot\, \eta$ be valid for $\gamma X$, by $S' \Rightarrow_{rm}^* \zeta B w \Rightarrow_{rm} \zeta \eta w$ with $\zeta = \gamma X$. The occurrence of $B$ in $\zeta B w$ was created by an earlier step $C \to \mu B \nu$ of the same derivation: $S' \Rightarrow_{rm}^* \zeta_1 C w_1 \Rightarrow_{rm} \zeta_1 \mu B \nu w_1 \Rightarrow_{rm}^* \zeta_1 \mu B w$, where only $\nu$ is rewritten after the step, because the derivation is rightmost. So $C \to \mu \cdot B \nu$ is valid for $\zeta_1 \mu = \zeta = \gamma X$. If $\mu \ne \varepsilon$, step 3 puts this item in the kernel of $\mathrm{GOTO}(V(\gamma), X)$, and CLOSURE adds $B \to \cdot\, \eta$. If $\mu = \varepsilon$, repeat the argument with the item $C \to \cdot\, B\nu$ and the shorter derivation up to the step that created $C$. The derivation gets shorter each time, and the chain cannot end at $S' \to \cdot\, S$, which is valid only for the empty string while $\gamma X$ is not empty; so it ends at an item with $\mu \ne \varepsilon$. Hence $V(\gamma X) \subseteq \mathrm{GOTO}(V(\gamma), X)$.

Steps 3 and 4 give $V(\gamma X) = \mathrm{GOTO}(V(\gamma), X)$, and steps 1 and 2 give $V(\varepsilon) = I_0$. $\square$

The theorem is why a stack of states suffices: after the parser has the viable prefix $\gamma$ on its stack, the top state holds $V(\gamma)$. A complete item $A \to \beta \cdot$ in it says that $\beta$ may be the [handle](/handle/), and an item $A \to \alpha \cdot a \beta$ says that shifting $a$ keeps a viable prefix.

**The automaton is a subset construction.** Make a nondeterministic automaton whose states are the items, with a transition $A \to \alpha \cdot X\beta \xrightarrow{X} A \to \alpha X \cdot \beta$ and an $\varepsilon$-transition $A \to \alpha \cdot B\beta \to B \to \cdot\, \gamma$. CLOSURE is the [$\varepsilon$-closure](/epsilon-closure/), GOTO is one step of the [subset construction](/subset-construction/), and the canonical collection is the set of reachable subsets. So the LR(0) automaton of $G$ is the deterministic automaton for the regular language of viable prefixes.

**Size and cost.** A state is a set of items, so $|\mathcal{C}| \le 2^{|G| + 2}$, and the bound is exponential in a real sense. For $m \ge 1$, take the productions $S \to A_i\, b_i$ for $1 \le i \le m$, $A_i \to a_j A_i$ for all $j \ne i$, and $A_i \to c$. The size is $|G| = 3m^2 + 2m$. After reading a word that uses exactly the letters $a_j$ with $j \notin R$, for any nonempty $R \subseteq \{1, \ldots, m\}$, and then $c$, the state is $\{A_i \to c\, \cdot : i \in R\}$: an item $A_i \to a_j \cdot A_i$ survives a letter $a_j$ only when $j \ne i$, so exactly the $A_i$ with $i \in R$ are still alive. These $2^m - 1$ states are distinct, so $|\mathcal{C}| \ge 2^m - 1$, which is $2^{\Omega(|G|^{1/2})}$. For $m = 1, \ldots, 7$ the collection has 5, 13, 30, 65, 138, 293 and 626 states. In practice grammars of programming languages give a few hundred to a few thousand states. With kernels stored in a hash table, CANONICAL-COLLECTION takes $O(|\mathcal{C}| \cdot |G|)$ expected time: each state's closure has at most $|G| + 2$ items and is computed once, and each item produces at most one kernel item of one GOTO.

**LR(1) item sets.** An LR(1) item $[A \to \alpha \cdot \beta,\ a]$ adds a [lookahead](/lookahead-symbols/) terminal $a \in \Sigma \cup \{\$\}$. The closure rule becomes: if $[A \to \alpha \cdot B\beta,\ a]$ is in the set and $B \to \gamma \in P$, add $[B \to \cdot\, \gamma,\ b]$ for each $b \in \mathrm{FIRST}(\beta a)$, with the [FIRST sets](/first-and-follow-sets/). GOTO moves the dot and keeps the lookahead. The start state is the closure of $[S' \to \cdot\, S,\ \$]$. The resulting *canonical LR(1) collection* drives [canonical LR(1) parsing](/canonical-lr-parsing/). Its states with the lookaheads removed are states of the LR(0) collection, and merging the LR(1) states with the same LR(0) items gives the LALR(1) automaton, whose lookaheads the [LALR lookahead computation](/lalr-lookahead-computation/) finds without building the LR(1) states.

## Examples

**The expression grammar.** Augment $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$ with $E' \to E$. The canonical collection has 12 states. The table lists the kernels, the items added by CLOSURE, and the transitions.

| state | kernel | added by CLOSURE | GOTO |
|---|---|---|---|
| 0 | $E' \to \cdot\, E$ | $E \to \cdot\, E + T$, $E \to \cdot\, T$, $T \to \cdot\, T * F$, $T \to \cdot\, F$, $F \to \cdot\, (E)$, $F \to \cdot\, \mathit{id}$ | $E$: 1, $T$: 2, $F$: 3, $($: 4, $\mathit{id}$: 5 |
| 1 | $E' \to E\, \cdot$, $E \to E \cdot + T$ | | $+$: 6 |
| 2 | $E \to T\, \cdot$, $T \to T \cdot * F$ | | $*$: 7 |
| 3 | $T \to F\, \cdot$ | | |
| 4 | $F \to (\, \cdot\, E)$ | the six items of state 0 without $E' \to \cdot\, E$ | $E$: 8, $T$: 2, $F$: 3, $($: 4, $\mathit{id}$: 5 |
| 5 | $F \to \mathit{id}\, \cdot$ | | |
| 6 | $E \to E + \cdot\, T$ | $T \to \cdot\, T * F$, $T \to \cdot\, F$, $F \to \cdot\, (E)$, $F \to \cdot\, \mathit{id}$ | $T$: 9, $F$: 3, $($: 4, $\mathit{id}$: 5 |
| 7 | $T \to T * \cdot\, F$ | $F \to \cdot\, (E)$, $F \to \cdot\, \mathit{id}$ | $F$: 10, $($: 4, $\mathit{id}$: 5 |
| 8 | $E \to E \cdot + T$, $F \to (E \cdot)$ | | $+$: 6, $)$: 11 |
| 9 | $E \to E + T\, \cdot$, $T \to T \cdot * F$ | | $*$: 7 |
| 10 | $T \to T * F\, \cdot$ | | |
| 11 | $F \to (E)\, \cdot$ | | |

The path $0 \xrightarrow{E} 1 \xrightarrow{+} 6 \xrightarrow{T} 9$ spells the viable prefix $E + T$, and state 9 says that $E + T$ may be reduced to $E$ or that a $*$ may follow. States 1, 2 and 9 hold a complete item and an item with a terminal after the dot, so the grammar is not LR(0); the [SLR](/slr-parsing/) method separates the moves with the FOLLOW sets, for instance reducing $E \to T$ in state 2 only on $+$, $)$ and $\$$. The string $E\,T$ has no path from state 0, and indeed no right-sentential form starts with $E\,T$.

**An empty production.** For $S \to A\, a$, $A \to \varepsilon$, the start state is $\{S' \to \cdot\, S,\ S \to \cdot\, A a,\ A \to \cdot\}$. The complete item $A \to \cdot$ in the start state says that the parser must reduce $\varepsilon$ to $A$ before it reads anything; the item sets need no special case for $\varepsilon$.

**Lookaheads double the state count.** The canonical LR(1) collection of the expression grammar has 22 states against 12, because states such as $F \to \mathit{id}\, \cdot$ appear once with the lookaheads that may follow inside parentheses and once with those that may follow at the top level. Merging them by their LR(0) items gives back the 12 states.

**An exponential collection.** For $m = 2$ the family above has the productions $S \to A_1 b_1 \mid A_2 b_2$, $A_1 \to a_2 A_1 \mid c$, $A_2 \to a_1 A_2 \mid c$, size 16, and 13 states. Reading $c$ from the start state gives $\{A_1 \to c\,\cdot,\ A_2 \to c\,\cdot\}$; reading $a_1\, c$ gives $\{A_2 \to c\,\cdot\}$; reading $a_2\, c$ gives $\{A_1 \to c\,\cdot\}$.

## Where it is used

- [LR(0) parsing](/lr0-parsing/), [SLR parsing](/slr-parsing/) and [LALR parsing](/lalr-parsing/) build their tables on the LR(0) collection; [canonical LR(1) parsing](/canonical-lr-parsing/) uses the LR(1) collection.
- The [LR parse table](/lr-parse-table/) has one row for each state of the collection, and [parser table construction](/parser-table-construction/) states the general problem.
- The [LALR lookahead computation](/lalr-lookahead-computation/) of DeRemer and Pennello works on the transitions of the LR(0) collection.
- [GLR parsing](/glr-parsing/) runs the same automaton nondeterministically, so its table may keep conflicts.
- Parser generators such as [yacc](/yacc/) print the item sets of each state in their report files, so that a grammar author can see where a [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/) comes from.

## References
