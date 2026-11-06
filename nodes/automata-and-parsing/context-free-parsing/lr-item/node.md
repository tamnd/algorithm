---
tag: 0EGMM9
kind: concept
slug: lr-item
name: LR item
aliases:
- LR(0) item
- dotted rule
area: automata-and-parsing/context-free-parsing
level: core
summary: A production with a dot marking how much of its right side has been recognized.
prereqs: [context-free-grammar, leftmost-derivation, handle]
see_also: [lr-item-sets, viable-prefix, lr0-parsing, lr-parse-table, canonical-lr-parsing, slr-parsing, earley-parser, lr-grammar]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (states as sets of dotted productions with lookahead strings)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.2, Items and the LR(0) Automaton; Section 4.6.5, Viable Prefixes; Section 4.7.1, Canonical LR(1) Items
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing (LR(0) items and the LR(0) automaton)
---

An LR item is a production of a [context-free grammar](/context-free-grammar/) with a dot somewhere in its right side, such as $E \to E + \cdot\, T$. It says that a parser has recognized the part of the right side before the dot and may next see the part after it. Sets of items are the states of every [LR parser](/lr-parsing/), and an LR(k) item adds the $k$ tokens that may follow the production. The same dotted productions, with a start position added, are the entries of the [Earley parser](/earley-parser/).

## In plain words

When you read a sentence word by word, at each moment you are partway through several grammar rules at once. You have finished the subject, you are in the middle of a verb phrase, and you are at the start of whatever comes after the verb. An item writes down one such guess: a rule and a mark that says how much of it is done.

A parser cannot know which guesses are right, so it keeps all of them that fit what it has read. When a guess is finished, the parser may replace the words of that rule by the rule's name. When a guess waits for a word, the parser may read the next word. Items make this bookkeeping finite, because a grammar has only a fixed number of rules and mark positions.

## The idea

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. LR constructions use the *augmented grammar*, which adds a new start symbol $S'$ with the single production $S' \to S$, and the end marker $\$ \notin \Sigma$ after the input.

**Items.** An *LR(0) item* is a pair of a production $A \to \alpha\beta$ and a position in its right side, written $A \to \alpha \cdot \beta$. A production $A \to X_1 \cdots X_k$ has the $k + 1$ items with the dot before $X_1$, before $X_2$, ..., and after $X_k$; the production $A \to \varepsilon$ has the one item $A \to \cdot$. So $G$ has exactly $|G|$ items. An item is

- *complete* if the dot is at the end, $A \to \alpha \cdot$: the whole right side has been seen, and the parser may reduce;
- a *shift item* if a terminal follows the dot, $A \to \alpha \cdot a \beta$: the parser may read $a$;
- a *goto item* if a nonterminal follows the dot, $A \to \alpha \cdot B \beta$: the parser expects a string derived from $B$;
- a *kernel item* if it is $S' \to \cdot S$ or the dot is not at the start.

An *LR(k) item* $[A \to \alpha \cdot \beta, u]$ adds a *lookahead* string $u$ of at most $k$ terminals, ending with $\$$ if it is shorter than $k$. It means: the parser may be in this production, and after it come the tokens $u$.

**Validity.** The item $A \to \alpha \cdot \beta$ is *valid* for a string $\gamma \in (V \cup \Sigma)^*$ if there is a rightmost [derivation](/derivation/)

$$S' \Rightarrow_{rm}^* \delta A x \Rightarrow_{rm} \delta \alpha \beta x, \qquad \gamma = \delta \alpha, \quad x \in \Sigma^*.$$

The LR(k) item $[A \to \alpha \cdot \beta, u]$ is valid for $\gamma$ if, in addition, $u$ is the first $k$ symbols of $x\$^k$. A string with at least one valid item is a [viable prefix](/viable-prefix/): a prefix of a right-sentential form that does not extend past the [handle](/handle/). The stack of a shift-reduce parser always holds a viable prefix, and a complete item $A \to \alpha \cdot$ valid for the stack says that $\alpha$ on top of the stack may be the handle.

**Closure and goto.** Two operations compute the valid items without looking at derivations.

- $\mathrm{CLOSURE}(I)$ is the least set that contains $I$ and, for each item $A \to \alpha \cdot B \beta$ in it and each production $B \to \gamma$, contains $B \to \cdot \gamma$. If the parser may see $B$ next, it may see the start of any right side of $B$.
- $\mathrm{GOTO}(I, X) = \mathrm{CLOSURE}(\{ A \to \alpha X \cdot \beta : A \to \alpha \cdot X \beta \in I \})$ moves the dot over $X$.

For LR(k) items, closure adds $[B \to \cdot \gamma, v]$ for each $v$ in $\mathrm{FIRST}_k(\beta u)$, the set of first $k$ symbols of the strings derived from $\beta u$ (see [FIRST and FOLLOW sets](/first-and-follow-sets/)).

> **Theorem (Knuth 1965).** Let $I_0 = \mathrm{CLOSURE}(\{S' \to \cdot S\})$ and $\mathrm{GOTO}(I, X_1 \cdots X_m) = \mathrm{GOTO}(\cdots \mathrm{GOTO}(I, X_1) \cdots, X_m)$. Then for every string $\gamma$, the set of LR(0) items valid for $\gamma$ is $\mathrm{GOTO}(I_0, \gamma)$. The same holds for LR(k) items, starting from $[S' \to \cdot S, \$^k]$.

*Proof sketch.* For $\gamma = \varepsilon$: an item valid for $\varepsilon$ comes from a derivation $S' \Rightarrow_{rm}^* A x \Rightarrow_{rm} \beta x$, so $\delta = \alpha = \varepsilon$. Following the leftmost path of the tree from $S'$ to this $A$, each node is $B \to \cdot\, C \beta'$ with the next node $C$, which is exactly the chain that closure follows; conversely each closure step extends such a derivation. For $\gamma X$: an item valid for $\gamma X$ either has $X$ just before the dot, and then the same item with the dot one step back is valid for $\gamma$, which is the kernel step of GOTO; or it has the dot at the start, and then it hangs below such a kernel item on a leftmost path, which is the closure step. Induction on $|\gamma|$ with both directions gives the theorem. $\blacksquare$

The sets $\mathrm{GOTO}(I_0, \gamma)$ are therefore the states of a [deterministic finite automaton](/deterministic-finite-automaton/), the *LR(0) automaton*, whose start state is $I_0$ and whose transitions are GOTO. It accepts exactly the viable prefixes. This is the core fact of LR parsing: the language of viable prefixes is regular, so a finite automaton can read the stack. The collection of all its states is the [canonical collection of item sets](/lr-item-sets/).

## Examples

**The expression grammar.** Augment $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$ with $S' \to E$. The grammar has $20$ items, and the LR(0) automaton has 12 states. Some of them:

| viable prefix $\gamma$ | items valid for $\gamma$ |
|---|---|
| $\varepsilon$ | $S' \to \cdot E$, $E \to \cdot E + T$, $E \to \cdot T$, $T \to \cdot T * F$, $T \to \cdot F$, $F \to \cdot ( E )$, $F \to \cdot id$ |
| $T$ | $E \to T \cdot$, $T \to T \cdot * F$ |
| $E +$ | $E \to E + \cdot T$, $T \to \cdot T * F$, $T \to \cdot F$, $F \to \cdot ( E )$, $F \to \cdot id$ |
| $E + T$ | $E \to E + T \cdot$, $T \to T \cdot * F$ |
| $($ | $F \to ( \cdot E )$, $E \to \cdot E + T$, $E \to \cdot T$, $T \to \cdot T * F$, $T \to \cdot F$, $F \to \cdot ( E )$, $F \to \cdot id$ |

The first row is $I_0$: the kernel $S' \to \cdot E$ and six items added by closure. In the second row the stack holds $T$; the complete item $E \to T \cdot$ says "reduce $T$ to $E$" and the shift item $T \to T \cdot * F$ says "read $*$". LR(0) items cannot choose, so the grammar is not [LR(0)](/lr0-parsing/).

**Lookahead decides.** The LR(1) items valid for $T$ are $[E \to T \cdot, +]$, $[E \to T \cdot, \$]$, $[T \to T \cdot * F, *]$, $[T \to T \cdot * F, +]$ and $[T \to T \cdot * F, \$]$. The complete item carries the lookaheads $+$ and $\$$, and the shift item wants $*$ next, so the next token decides: reduce on $+$ or $\$$, shift on $*$. The canonical LR(1) automaton of this grammar has 22 states.

**Empty right sides.** In $S \to A a$, $A \to \varepsilon$, the set $I_0$ is $\{S' \to \cdot S, S \to \cdot A a, A \to \cdot\}$. The complete item $A \to \cdot$ is valid for the empty prefix: the parser must reduce $\varepsilon$ to $A$ before it reads anything.

**Not valid.** In the expression grammar, $E \to E + T \cdot$ is not valid for $T$, because $T$ does not end with $E +$; and no item is valid for $E \, T$, which is not a viable prefix, because no right-sentential form has $E$ and $T$ next to each other.

## Where it is used

- **LR parsers.** [LR(0) parsing](/lr0-parsing/), [SLR](/slr-parsing/), [LALR](/lalr-parsing/) and [canonical LR(1)](/canonical-lr-parsing/) all use sets of items as states; they differ in the lookahead attached to the complete items. The [LR parse table](/lr-parse-table/) is read off the item sets.
- **Conflicts.** A [shift-reduce conflict](/shift-reduce-conflict/) is a set with a complete item and a shift item that the lookahead cannot separate; a [reduce-reduce conflict](/reduce-reduce-conflict/) is a set with two such complete items. Parser generators such as [yacc](/yacc/) report conflicts by printing these items.
- **Earley parsing.** The [Earley parser](/earley-parser/) keeps items $[A \to \alpha \cdot \beta, i]$, where $i$ is the input position at which the production started. Its predictor is closure and its scanner and completer are goto.
- **GLR parsing.** [GLR parsing](/glr-parsing/) runs the LR(0) or LALR automaton and splits the stack at conflicts.

## References
