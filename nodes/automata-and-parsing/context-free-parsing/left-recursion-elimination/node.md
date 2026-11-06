---
tag: KFFADV
kind: algorithm
slug: left-recursion-elimination
name: Left recursion elimination algorithm
aliases:
- Left recursion elimination
- Paull's algorithm
- removing left recursion
area: automata-and-parsing/context-free-parsing
level: core
summary: Systematic procedure that removes direct and indirect left recursion from a grammar.
solves: [left-recursion-removal]
model: word-ram
complexity:
  vars: {g: the size of the input grammar, m: the number of nonterminals, h: the size of the output grammar}
  time: {worst: O(g + m h)}
  space: {extra: O(h)}
properties: {deterministic: true, recursive: false}
history:
  year: 1965
  people: [Sheila A. Greibach]
  note: Greibach's construction of her normal form orders the nonterminals and removes left recursion one nonterminal at a time; the textbook algorithm that does only this step is usually credited to Marvin C. Paull.
prereqs: [left-recursion, nullable-symbol, epsilon-production-elimination]
see_also: [left-recursion-removal, left-factoring, ll-grammar, ll1-parsing, recursive-descent-parsing, greibach-normal-form-conversion, unit-production-elimination, useless-symbol-elimination]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.3.3, Elimination of Left Recursion (Algorithm 4.19 and Example 4.20)
  - paper: "Robert C. Moore, Removing left recursion from context-free grammars, Proceedings of the 1st North American Chapter of the Association for Computational Linguistics Conference (NAACL 2000)"
    locator: pp. 249 to 255 (the size of the output of the standard algorithm, and better orderings and variants)
  - paper: doi:10.1145/321250.321254
    title: Sheila A. Greibach, A new normal-form theorem for context-free phrase structure grammars, Journal of the ACM 12(1) (1965)
    locator: pp. 42 to 52
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.2, Predictive Parsing (eliminating left recursion)
---

The left recursion elimination algorithm, often called Paull's algorithm, turns a [context-free grammar](/context-free-grammar/) into one that generates the same language and has no [left recursion](/left-recursion/): no nonterminal $A$ derives a string that starts with $A$. It orders the nonterminals, substitutes earlier nonterminals at the left end of the right sides of later ones, and then replaces each direct left recursion $A \to A \alpha \mid \beta$ by the right recursion $A \to \beta A'$, $A' \to \alpha A' \mid \varepsilon$. It is the standard step that makes a grammar fit for [LL(1) parsing](/ll1-parsing/) and [recursive descent](/recursive-descent-parsing/), which loop forever on left recursion.

## In plain words

A rule like "a list is a list followed by a comma and an item, or just an item" refers to itself at its left end. A parser that works from the top down tries to find a list by first finding a list, and never gets anywhere.

The fix rewrites the rule from the other side: "a list is an item followed by a tail, and a tail is a comma, an item and a tail, or nothing". Both describe the same lists, but now each rule starts with something other than itself. When the self-reference goes through other rules, say a list starts with a block and a block starts with a list, the algorithm first plugs the rules of the earlier symbol into the later one, so that the self-reference becomes direct, and then fixes it in the same way.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

A nonterminal $A$ is *left-recursive* if $A \Rightarrow^+ A \gamma$ for some $\gamma$. The recursion is *direct* when $G$ has a production $A \to A \alpha$, and *indirect* otherwise, as in $A \to B c$, $B \to A d$; it is *hidden* when it goes through a [nullable](/nullable-symbol/) prefix, as in $A \to B A c$ with $B \Rightarrow^* \varepsilon$. The task, [left recursion removal](/left-recursion-removal/), is to find a grammar $G'$ with $L(G') = L(G)$ and no left-recursive nonterminal.

The main loop needs a grammar with three properties: every nonterminal derives some terminal string, there is no production $A \to \varepsilon$, and there is no cycle $A \Rightarrow^+ A$. A cycle cannot be removed by any rewriting that keeps it, and empty productions can hide left recursion from the loop. A preparation step establishes the three properties, and changes the language only by the empty string, which is added back at the end.

## The algorithm

```pseudo id=prepare
PREPARE(G)
P1  remove every production that uses a symbol deriving no terminal string
P2  remove ε-productions: for each A → X1 ⋯ Xk add every version with some nullable Xi left out; drop A → ε
P3  remove again the productions that use a symbol deriving no terminal string
P4  merge the nonterminals of each cycle of unit productions A → B → ⋯ → A into one; drop A → A
P5  record whether ε ∈ L(G), that is, whether S was nullable
```

Line P2 is [epsilon-production elimination](/epsilon-production-elimination/). After it, a cycle $A \Rightarrow^+ A$ can only use unit productions $A \to B$, and line P4 removes these cycles by giving all the nonterminals of one cycle the same name; they derive the same strings, since each derives each other. The main loop is:

```pseudo id=main
PAULL(G)                          ▷ G prepared: no ε-productions, no cycles, no useless symbols
L1  order the nonterminals A1, …, Am; let Ri be the set of right sides of Ai
L2  for i ← 1 to m do
L3      for j ← 1 to i − 1 do
L4          for each Ai → Aj γ with Aj γ ∈ Ri do
L5              replace it by Ai → δ γ for every δ ∈ Rj
L6      split Ri into Ai → Ai α1 | ⋯ | Ai αp and Ai → β1 | ⋯ | βq, the βs not starting with Ai
L7      if p ≥ 1 then
L8          Ri ← {β1 Ai', …, βq Ai'}, where Ai' is a new nonterminal
L9          add the productions Ai' → α1 Ai' | ⋯ | αp Ai' | ε
L10 return the productions of A1, …, Am and of the new nonterminals
```

If line P5 found $\varepsilon \in L(G)$, the result gets a new start symbol $S_0$ with $S_0 \to S \mid \varepsilon$. $S_0$ appears on no right side, so it adds no left recursion.

Lines L3 to L5 make sure that, when $A_i$ is processed, none of its productions starts with an earlier nonterminal $A_j$: each such production is replaced by the productions that begin with the right sides of $A_j$, which by then start with a terminal or with a nonterminal later than $A_j$. Lines L6 to L9 remove the direct left recursion that remains. The right sides $\alpha_j$ and $\beta_j$ are never empty, so each new production starts with a symbol other than its left side.

## Example

**Direct left recursion.** The expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$ has no empty productions and no cycles, so PREPARE changes nothing. With the order $E, T, F$, line L5 has nothing to substitute, because no right side of $T$ or $F$ starts with an earlier nonterminal. Lines L6 to L9 handle each nonterminal on its own:

| nonterminal | $\alpha$s | $\beta$s | new productions |
|---|---|---|---|
| $E$ | $+ T$ | $T$ | $E \to T E'$, $E' \to + T E' \mid \varepsilon$ |
| $T$ | $* F$ | $F$ | $T \to F T'$, $T' \to * F T' \mid \varepsilon$ |
| $F$ | none | $( E )$, $id$ | unchanged |

The result is the LL(1) expression grammar used on the [LL parse table](/ll-parse-table/) page.

**Indirect left recursion and an empty production.** Take $S \to A a \mid b$, $A \to A c \mid S d \mid \varepsilon$. Here $S \Rightarrow A a \Rightarrow S d a$, so $S$ is left-recursive through $A$.

1. PREPARE: $A$ is nullable and $S$ is not, so $\varepsilon \notin L(G)$. Line P2 gives $S \to A a \mid a \mid b$ and $A \to A c \mid c \mid S d$.
2. $i = 1$, $A_1 = S$: nothing to substitute, and no production of $S$ starts with $S$.
3. $i = 2$, $A_2 = A$: line L5 replaces $A \to S d$ by $A \to A a d \mid a d \mid b d$. Now $A \to A c \mid A a d \mid c \mid a d \mid b d$, with $\alpha_1 = c$, $\alpha_2 = a d$ and the $\beta$s $c$, $a d$, $b d$.
4. Lines L8 and L9 give $A \to c A' \mid a d A' \mid b d A'$ and $A' \to c A' \mid a d A' \mid \varepsilon$.

The result is $S \to A a \mid a \mid b$, $A \to c A' \mid a d A' \mid b d A'$, $A' \to c A' \mid a d A' \mid \varepsilon$, without left recursion. Both grammars generate the same strings, for example $b d a$ and $a d c a$.

## Correctness

The output generates the same language as the input and has no left-recursive nonterminal. Language: each step of PREPARE keeps the nonempty strings of $L(G)$, and $S_0$ restores $\varepsilon$; substituting the productions of $A_j$ for the leading $A_j$ at line L5 keeps the strings derived from every nonterminal, because each tree that uses $A_i \to A_j \gamma$ and then $A_j \to \delta$ corresponds to one that uses $A_i \to \delta \gamma$; and lines L8 and L9 keep them, because both $A \to A \alpha \mid \beta$ and $A \to \beta A'$, $A' \to \alpha A' \mid \varepsilon$ give $A$ the strings of $\beta \alpha^*$. No left recursion: after round $i$, every production of $A_k$ with $k \le i$ starts with a terminal or with an $A_l$ for $l > k$, and every production of a new $A_k'$ starts with a part that cannot vanish. The second fact needs the absence of cycles: if some $\alpha$ could derive $\varepsilon$, then $A_i \Rightarrow A_i \alpha \Rightarrow^* A_i$. The full proof is below.

## Complexity

Let $g$ be the size of the input, $m$ the number of nonterminals and $h$ the size of the output.

- **PREPARE.** The nullable and productive sets take $O(g)$ time with worklists, and the cycles of unit productions are the strongly connected components of a graph of size $O(g)$. Line P2 writes every version of every production, so its output size can be up to $2^r$ times the size of a production with $r$ nullable symbols. Each production of the prepared grammar ends up, possibly extended, in the output, so the prepared grammar has size at most $h$ and PREPARE takes $O(g + h)$ time.
- **The main loop.** In round $i$, each substitution at line L5 replaces a production by productions that are at least as long, and at least one of them, because every nonterminal has a production. So the productions of $A_i$ only grow during the round, and the $i - 1$ substitutions and the split cost $O(i)$ times the final size of $R_i$. Over all rounds this is $O(m h)$.
- **Output size.** $h$ can be exponential in $g$. With $A_0 \to a$ and $A_i \to A_{i-1} x \mid A_{i-1} y$ for $i = 1, \ldots, m - 1$, in the order $A_0, A_1, \ldots$, line L5 expands $A_i$ into $2^i$ productions, one for each string $a \{x, y\}^i$, although the grammar has no left recursion at all. In the reverse order nothing is substituted and the grammar stays as it is.

| measure | bound |
|---|---|
| time | $O(g + m h)$ |
| extra space | $O(h)$ |
| output size $h$ | at most exponential in $g$; depends on the order |

## Properties

- **Exact language.** $L(G') = L(G)$, including the empty string.
- **Left parses change.** The parse trees of $G'$ are not the trees of $G$: a left-associative chain $((a - b) - c)$ in $G$ becomes a right-leaning chain of $A'$ nodes. A compiler that wants the original associativity rebuilds it, for example by passing the left operand down as an inherited attribute of $A'$.
- **Empty productions return.** The output has the empty productions $A' \to \varepsilon$, but they cause no hidden left recursion: a new $A'$ only appears at the end of a right side, after a symbol that does not derive $\varepsilon$.
- **Not always LL(1).** The output has no left recursion, but it may still need [left factoring](/left-factoring/), and it may not be LL(k) for any $k$, for instance when $G$ is ambiguous.

## Variants and improvements

- **Direct recursion only.** Many grammars have only direct left recursion, and then lines L6 to L9 alone suffice; no ordering or substitution is needed. Hand-written recursive descent parsers often turn $A \to A \alpha \mid \beta$ into a loop: parse $\beta$, then parse $\alpha$ while the next token can start it.
- **Substitute only what is needed.** Moore (2000) shows that substituting only the nonterminals that are left-recursive, and using an order that puts them late, gives much smaller grammars in practice; he also uses a left-corner transform that avoids the exponential growth of the standard order.
- **Without empty productions.** The direct step can produce $A \to \beta \mid \beta A'$ and $A' \to \alpha \mid \alpha A'$ instead, which keeps the grammar free of empty productions. This form is used on the way to [Greibach normal form](/greibach-normal-form-conversion/), where every right side must start with a terminal.
- **Parsers that accept left recursion.** [LR parsing](/lr-parsing/), the [Earley parser](/earley-parser/) and some extensions of [packrat parsing](/packrat-parsing/) handle left recursion directly, so a grammar for them can keep it.

## When to use it

Use it before you build an [LL(1) table](/ll-parse-table/) or a recursive descent parser for a grammar that has left recursion, typically for left-associative operators and for lists. For only direct left recursion, use lines L6 to L9 alone. For a grammar meant for an LR or Earley parser, keep the left recursion: it is natural for left-associative operators, and LR parsers use less stack with it.

## Pitfalls

- **Empty productions hide recursion.** With $A \to B A c \mid a$ and $B \to b \mid \varepsilon$, the left-recursive path goes through the nullable $B$, and no production starts with $A$, so lines L6 to L9 see nothing. Line P2 exposes it as $A \to A c$.
- **Cycles cannot be removed this way.** With $A \to B \mid a$ and $B \to A$, the round of $B$ makes $B \to B \mid a$, and $B \to B$ has $\alpha = \varepsilon$, which would give $B' \to B'$. Line P4 removes such cycles first.
- **Forgetting the ordering.** Running only lines L6 to L9 on each nonterminal leaves indirect recursion such as $S \to A a$, $A \to S d$ untouched.
- **The empty string.** PREPARE removes $\varepsilon$ from the language; a version that forgets line P5 loses it.
- **Blow-up.** A bad order can make the grammar exponentially larger, as in the complexity section, even when there is nothing to remove. Run the full algorithm only on grammars that have indirect left recursion, and put nonterminals that start many right sides late in the order.

## Implementations

## History

Greibach (1965) proved that every context-free language without $\varepsilon$ has a grammar in which every right side starts with a terminal. Her construction orders the nonterminals, substitutes earlier ones at the left end of later ones, and removes direct left recursion, which is the algorithm on this page plus a final substitution pass. The textbook version, which stops once no left recursion remains, is usually credited to Marvin C. Paull. Moore (2000) measured its output on large natural-language grammars, found it too large in practice, and gave improved methods.

## References
