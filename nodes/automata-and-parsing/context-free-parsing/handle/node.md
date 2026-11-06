---
tag: ESG3QR
kind: concept
slug: handle
name: Handle
area: automata-and-parsing/context-free-parsing
level: core
summary: The substring matching a production's right side whose reduction is a step in a rightmost derivation.
prereqs: [derivation, sentential-form, bottom-up-parsing]
see_also: [shift-reduce-parsing, viable-prefix, lr-parsing, lr0-parsing, operator-precedence-parsing, knuth-lr-theorem, ambiguity, lr-item]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.5.2, Handle Pruning; Section 4.5.3, Shift-Reduce Parsing; Section 4.6.1, Why LR Parsers? (viable prefixes)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 9, Deterministic Bottom-Up Parsing (Section 9.1, Simple Handle-Finding Techniques)
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (handles of right sentential forms and the LR(k) condition)
---

A handle of a sentential form is the occurrence of a production's right side that was produced by the last step of a rightmost [derivation](/derivation/), together with that production. Replacing the handle by the production's left side undoes that step. A [bottom-up parser](/bottom-up-parsing/) repeats this "handle pruning" from the input back to the start symbol, and the whole difficulty of bottom-up parsing is to find the handle without seeing the derivation.

## In plain words

Think of building a sentence by expanding the rightmost placeholder again and again. Now run the film backwards. At each step backwards, one piece of the current line turns back into the placeholder it came from. That piece is the handle.

A piece that matches some rule is not always the handle. Turning the wrong matching piece back can lead to a line from which the start symbol can never be reached. So a parser that reads from the bottom up must decide which matching piece is the real one. It can do this by looking at what it has read so far and at the next few input symbols.

## The idea

Let $G = (V, \Sigma, P, S)$ be a [context-free grammar](/context-free-grammar/), in the notation of that page: productions $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the input length. A **right sentential form** is a [sentential form](/sentential-form/) that occurs in some rightmost derivation from $S$.

**Definition.** Let $\gamma$ be a right sentential form. A **handle** of $\gamma$ is a pair (production $A \to \beta$, position $k$) such that

$$S \Rightarrow^*_{rm} \alpha A w \Rightarrow_{rm} \alpha \beta w = \gamma, \qquad |\alpha| = k, \quad w \in \Sigma^*.$$

So $\beta$ occurs in $\gamma$ starting after the first $k$ symbols, and $\gamma$ is the result of a rightmost step that rewrote that $A$. Often the string $\beta$ itself is called the handle, when the production and the position are clear.

Three facts make handles the basis of [shift-reduce parsing](/shift-reduce-parsing/).

**1. Only terminals follow a handle.** The part $w$ to the right of the handle is in $\Sigma^*$, because a rightmost step rewrites the rightmost nonterminal. So a parser that has read the input up to the end of the handle has not yet needed any symbol of $w$ except as lookahead.

**2. Handle pruning gives the rightmost derivation in reverse.** If $\gamma_0 = x \in \Sigma^*$ and $\gamma_{i+1}$ is $\gamma_i$ with its handle replaced by the left side of the handle's production, the sequence ends with $S$ exactly when $x \in L(G)$, and read backwards it is a rightmost derivation of $x$. A grammar is **unambiguous** if and only if every right sentential form has exactly one handle, when every nonterminal derives some terminal string. *Proof.* Two different handles of $\gamma$ give two rightmost derivations of $\gamma$ that differ in their last step; extending both by one rightmost derivation $\gamma \Rightarrow^*_{rm} x$ gives two rightmost derivations of the terminal string $x$, so $x$ has two [parse trees](/parse-tree/). Conversely, if $x$ has two rightmost derivations, read them from $x$ backwards; at the first form $\gamma$ where the previous steps differ, the two steps have different productions or positions, which are two handles of $\gamma$. $\square$

**3. The handle never sinks into the stack.** A shift-reduce parser keeps a stack $\delta$ and the rest $y$ of the input, with $\delta y$ a right sentential form. After it reduces the handle $\beta$ of $\alpha \beta w$ to $A$, the stack is $\alpha A$. *Claim:* the handle of the new form $\alpha A w$ ends at or after the position of $A$. *Proof.* Take a rightmost derivation whose last step produces $\alpha A w$ by some $B \to \mu$, so $\alpha A w = \rho\, \mu\, z$ with $z \in \Sigma^*$ by fact 1, and the handle is $\mu$ after $\rho$. $A$ is a nonterminal, so it does not lie in $z$; it lies in $\rho \mu$, at or before the right end of $\mu$. $\square$ So the parser only needs two moves: **shift** the next input symbol until the handle's right end is on top of the stack, then **reduce**. The handle is always a suffix of the stack, never buried below its top.

**Viable prefixes.** A prefix of a right sentential form that does not extend past the right end of its handle is a [viable prefix](/viable-prefix/). These are exactly the possible stack contents of a correct shift-reduce parser. Knuth proved that the viable prefixes of any grammar form a [regular language](/regular-language/), recognized by the automaton of [LR items](/lr-item/), and an LR parser uses that automaton, with lookahead, to tell when the top of the stack is a handle.

## Examples

**Handle pruning of $a + a * a$.** With the expression grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to (\,E\,) \mid a,$$

the rightmost derivation of $a + a * a$, read backwards, prunes these handles:

| right sentential form | handle | production |
|---|---|---|
| $a + a * a$ | first $a$ | $F \to a$ |
| $F + a * a$ | $F$ | $T \to F$ |
| $T + a * a$ | $T$ | $E \to T$ |
| $E + a * a$ | second $a$ | $F \to a$ |
| $E + F * a$ | $F$ | $T \to F$ |
| $E + T * a$ | third $a$ | $F \to a$ |
| $E + T * F$ | $T * F$ | $T \to T * F$ |
| $E + T$ | $E + T$ | $E \to E + T$ |
| $E$ | | |

In the form $E + T * a$, the prefix $E + T$ matches the right side of $E \to E + T$, but it is not the handle. Reducing it gives $E * a$, which is not a right sentential form, since no production puts $*$ directly after $E$; the parse would then fail. An LR parser avoids the wrong choice because it sees $*$ as the next input symbol. In the form $T + a * a$, the handle is $T$ and not $a$: the parser must reduce $T$ to $E$ before it shifts $+$.

**Two handles in an ambiguous grammar.** With $E \to E + E \mid E * E \mid a$, the string $a + a * a$ has the two rightmost derivations

$$E \Rightarrow E + E \Rightarrow E + E * E \Rightarrow E + E * a \Rightarrow E + a * a \Rightarrow a + a * a,$$

$$E \Rightarrow E * E \Rightarrow E * a \Rightarrow E + E * a \Rightarrow E + a * a \Rightarrow a + a * a.$$

They agree on the last three forms, so the right sentential form $E + E * a$ has two handles: the last $a$ with $E \to a$ at position 4, from the first derivation, and $E + E$ with $E \to E + E$ at position 0, from the second. The first groups $a + (a * a)$ and the second $(a + a) * a$. A shift-reduce parser with $E + E$ on its stack and $*$ as the next input must choose between reducing $E + E$ and shifting $*$: a shift-reduce conflict, which parser generators settle with precedence declarations.

**A handle of length zero.** With $S \to A b$, $A \to \varepsilon$, the right sentential form $b$ comes from $S \Rightarrow_{rm} A b \Rightarrow_{rm} b$, so its handle is $A \to \varepsilon$ at position 0: an empty string before $b$. A shift-reduce parser reduces it on an empty stack, before it shifts anything.

## Where it is used

- A [shift-reduce parser](/shift-reduce-parsing/) is a handle-pruning machine: it shifts until a handle is on top of the stack and then reduces it. The LR family ([LR(0)](/lr0-parsing/), [SLR](/slr-parsing/), [LALR(1)](/lalr-parsing/), [canonical LR(1)](/canonical-lr-parsing/)) differs only in how much it knows to recognize the handle.
- A grammar is [LR(k)](/lr-grammar/) when $k$ symbols of lookahead after the handle always determine it; [Knuth's theorem](/knuth-lr-theorem/) ties this class to the deterministic context-free languages.
- A [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/) in a parse table is a state where the lookahead does not determine the handle.
- [Operator-precedence parsing](/operator-precedence-parsing/) finds handles by precedence relations between terminals, and older precedence methods do the same between all symbols.
- [GLR parsing](/glr-parsing/) keeps all candidate handles at once when the grammar is not deterministic.

## References
