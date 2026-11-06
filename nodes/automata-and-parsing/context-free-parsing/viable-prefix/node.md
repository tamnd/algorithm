---
tag: APMMBH
kind: concept
slug: viable-prefix
name: Viable prefix
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A prefix of a right-sentential form that can still be extended to a valid handle-containing form.
prereqs: [handle, sentential-form, shift-reduce-parsing]
see_also: [lr-item, lr0-parsing, lr-item-sets, canonical-lr-parsing, slr-parsing, knuth-lr-theorem, regular-language, deterministic-finite-automaton]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (the strings that can appear to the left of the handle form a regular set, and the construction of the automaton by item sets)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.5, Viable Prefixes (the definition, valid items, and the theorem that the LR(0) automaton recognizes them); Section 4.5.2, Handle Pruning
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 9, Deterministic Bottom-Up Parsing (the LR(0) automaton as a recognizer of the possible stack contents)
---

A viable prefix of a [context-free grammar](/context-free-grammar/) is a string of grammar symbols that can be the stack of a correct [shift-reduce parser](/shift-reduce-parsing/): a prefix of a right-sentential form that does not extend past the right end of the [handle](/handle/). The concept explains why LR parsing works. Knuth showed in 1965 that the viable prefixes of any grammar form a [regular language](/regular-language/), recognized by the automaton whose states are sets of [LR(0) items](/lr-item/). So a [finite automaton](/deterministic-finite-automaton/) can read the stack, and an LR parser can keep the stack viable with one table lookup per move.

## In plain words

A bottom-up parser keeps the part of the input it has read, partly combined, on a stack. Not every stack makes sense. For arithmetic, a stack that ends with a term followed by a plus sign is wrong: before reading the plus, the parser should have turned the term into an expression. A stack that ends with an expression and a plus sign is fine, since a term can follow.

A viable prefix is a stack content that is still on the way to a correct parse: some way of finishing the input exists, and the parser has not gone past a point where it had to combine. The surprising fact is that the set of all viable stacks is simple enough for a finite automaton to recognize. LR parsers are built on this fact.

## The idea

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size.

Augment $G = (V, \Sigma, P, S)$ with a fresh start symbol $S'$ and the production $S' \to S$. A rightmost derivation step $\varphi A z \Rightarrow_{rm} \varphi \beta z$, with $z \in \Sigma^*$, has the **handle** $\beta$ at the position after $\varphi$: the substring that a reduction by $A \to \beta$ turns back into $A$.

**Definition.** A string $\gamma \in (V \cup \Sigma)^*$ is a **viable prefix** if $\gamma$ is a prefix of $\varphi \beta$ for some rightmost derivation $S' \Rightarrow^*_{rm} \varphi A z \Rightarrow_{rm} \varphi \beta z$.

So a viable prefix is what lies to the left of some point at or before the right end of a handle. A shift-reduce parser that traces a rightmost derivation in reverse holds $\varphi \beta$ on the stack when it reduces, and a prefix of it before that, so its stack is always a viable prefix.

**Valid items.** An item $[A \to \beta_1 \cdot \beta_2]$ is **valid** for $\gamma$ if there is a rightmost derivation $S' \Rightarrow^*_{rm} \varphi A z \Rightarrow_{rm} \varphi \beta_1 \beta_2 z$ with $\gamma = \varphi \beta_1$. The item says: on top of the stack, $\beta_1$ is the start of a handle $\beta_1 \beta_2$.

**Theorem.** $\gamma$ is a viable prefix if and only if some item is valid for $\gamma$.

*If.* With the derivation in the definition of validity, $\gamma = \varphi \beta_1$ is a prefix of $\varphi \beta_1 \beta_2$, the left part and the handle of $\varphi \beta_1 \beta_2 z$.

*Only if.* Let $\gamma$ be a prefix of $\varphi \beta$ in a rightmost derivation $S' = \theta_0 \Rightarrow \theta_1 \Rightarrow \cdots \Rightarrow \theta_m = \varphi \beta z$, where step $j$ rewrites $\theta_{j-1} = \delta_j B_j z_j$ to $\delta_j \eta_j z_j$. Then $\gamma$ is a prefix of $\delta_m \eta_m$; choose the least $j$ with $\gamma$ a prefix of $\delta_j \eta_j$. If $j = 1$, then $\delta_1 = \varepsilon$ and $\eta_1 = S$, and $\gamma$ is $\varepsilon$ or $S$: the item $[S' \to \cdot S]$ or $[S' \to S \cdot]$ is valid. If $j > 1$, the rewritten nonterminal $B_j$ is the rightmost nonterminal of $\theta_{j-1} = \delta_{j-1} \eta_{j-1} z_{j-1}$, and $z_{j-1}$ has no nonterminal, so $\delta_j B_j$ is a prefix of $\delta_{j-1} \eta_{j-1}$. If $\gamma$ were a prefix of $\delta_j$, it would be a prefix of $\delta_{j-1} \eta_{j-1}$, against the choice of $j$. So $\gamma = \delta_j \eta'$ with $\eta_j = \eta' \eta''$, and $[B_j \to \eta' \cdot \eta'']$ is valid for $\gamma$, by the first $j$ steps. $\square$

**Knuth's theorem: viable prefixes are regular.** Build a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) whose states are the items. The start state is $[S' \to \cdot S]$. There is a transition on $X$ from $[A \to \alpha \cdot X \beta]$ to $[A \to \alpha X \cdot \beta]$, and an $\varepsilon$-transition from $[A \to \alpha \cdot B \beta]$ to $[B \to \cdot \eta]$ for each production of $B$. Every state accepts. If $G$ is reduced (every nonterminal is reachable and derives a terminal string, see [useless symbol elimination](/useless-symbol-elimination/)), the set of states reachable on $\gamma$ is exactly the set of items valid for $\gamma$. The subset construction applied to this automaton gives the LR(0) automaton of [LR(0) parsing](/lr0-parsing/), whose states are CLOSURE and GOTO sets, the [canonical collection](/lr-item-sets/). It accepts exactly the viable prefixes, and its state on $\gamma$ is the set of items valid for $\gamma$. The proof that the states equal the sets of valid items is Lemma 1 of the correctness proof of [SLR parsing](/slr-parsing/).

The automaton has at most $2^{|G|}$ states, since there are at most $|G|$ items; for programming languages it has a few hundred to a few thousand.

**Parsing as keeping the stack viable.** An LR parser with stack $\gamma$ and next token $a$ looks up the state $\delta(\gamma)$. A complete item $[A \to \beta \cdot]$ in it says that $\beta$ on top may be a handle; an item $[B \to \alpha \cdot a \eta]$ says that shifting $a$ gives a viable prefix. The lookahead (none in LR(0), FOLLOW in SLR(1), item lookaheads in LALR(1) and [canonical LR(1)](/canonical-lr-parsing/)) decides between them. The LR(1) items refine validity with the next token, and a canonical LR(1) parser never shifts a token unless the stack followed by that token can still lead to a sentence. This is the **viable prefix property**: an error is found at the first token that cannot continue a sentence.

## Examples

The classifications below were checked by a script that compares the LR(0) automaton with a brute-force enumeration of rightmost derivations.

**Expressions.** For $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid \mathtt{id}$:

| string | viable? | why |
|---|---|---|
| $E +$ | yes | a prefix of $E + T$, the handle in $E + T\, z$ |
| $T +$ | no | in every right-sentential form $T + \cdots$, the handle is $T$ (to be reduced by $E \to T$), so the prefix may not go past it |
| $T *$ | yes | a prefix of $T * F$ |
| $E + T *$ | yes | a prefix of $E + T * F$ |
| $( ( E$ | yes | a prefix of $( ( E )$ |
| $E\, T$ | no | no right-sentential form has $E$ directly before $T$ |
| $T * \mathtt{id}$ | yes | $\mathtt{id}$ is the handle in $T * \mathtt{id}\, z$ |

The string $T +$ is why the parser must reduce $T$ to $E$ before shifting $+$: after a shift, the stack would not be viable.

**Balanced pairs.** For $S \to a\, S\, b \mid \varepsilon$, the right-sentential forms are $S$, $a^k S b^k$ for $k \ge 1$, and $a^k b^k$ for $k \ge 0$. Their handles give the viable prefixes

$$a^k, \qquad a^k S \ (k \ge 0), \qquad a^k S b \ (k \ge 1),$$

a regular set, although the language $\{a^k b^k\}$ is not regular. The right-sentential form $a\, a\, S\, b\, b$ has the handle $a\, S\, b$, so its prefix $a\, a\, S\, b\, b$ is not viable: the stack may hold at most $a\, a\, S\, b$ before the parser reduces. The LR(0) automaton has 5 states.

**After an error.** On the input $\mathtt{id} + * \, \mathtt{id}$ of the expression grammar, the parser reaches the stack $E +$ with $*$ next. No viable prefix starts with $E + *$, so no reduction or shift can help, and the parser reports the error at $*$. An SLR(1) or LALR(1) parser may make some reductions before it notices an error, but it never shifts the bad token.

## Where it is used

- **Constructing LR parsers.** The LR(0) automaton, the CLOSURE and GOTO construction and the [LR parse table](/lr-parse-table/) are the recognizer of viable prefixes with actions attached. SLR, LALR and canonical LR differ only in the lookahead used at complete items.
- **Proving LR parsers correct.** The invariant "the stack is a viable prefix and the state is the set of its valid items" is the core of the correctness proofs of [LR(0)](/lr0-parsing/), [SLR(1)](/slr-parsing/) and [canonical LR(1)](/canonical-lr-parsing/) parsing.
- **Defining LR(k) grammars.** Knuth's test for LR($k$) is a conflict check on the items valid for each viable prefix, with $k$ lookahead symbols. The [Knuth LR theorem](/knuth-lr-theorem/) relates the LR($k$) grammars to the deterministic context-free languages.
- **Error detection and recovery.** The viable prefix property tells where a syntax error is: at the first token that makes the stack not viable. Recovery methods such as [panic mode](/panic-mode-error-recovery/) pop the stack to a viable prefix from which a known token can be shifted.
- **Grammar debugging.** A parser generator explains a conflict by showing a viable prefix that leads to the conflicting state, the shortest path in the LR(0) automaton.

## References
