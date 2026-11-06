---
tag: P8PFGP
kind: algorithm
slug: left-corner-parsing
name: Left-corner parsing
aliases:
- left corner parser
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Hybrid parser that predicts from the leftmost symbol of each production.
solves: [context-free-language-recognition, cfg-membership-problem]
model: word-ram
complexity:
  vars: {n: the length of the input string, G: the grammar size (the sum over all productions of the right side length plus one), N: the number of nonterminals}
  time: {worst: O(n^3 N G), best: O(n)}
  space: {extra: O(n^2 N G)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1970
  people: [Daniel J. Rosenkrantz, Philip M. Lewis II]
  note: Rosenkrantz and Lewis defined deterministic left-corner parsing and the LC(k) grammars in 1970. Tabular forms for all grammars came later from computational linguistics.
prereqs: [top-down-parsing, bottom-up-parsing, left-recursion]
see_also: [earley-parser, recursive-descent-parsing, ll1-parsing, lr-parsing, chart-parsing, left-recursion-elimination, shift-reduce-parsing, pushdown-automaton]
sources:
  - paper: doi:10.1109/swat.1970.5
    title: Daniel J. Rosenkrantz and Philip M. Lewis II, Deterministic left corner parsing, 11th Annual Symposium on Switching and Automata Theory (1970)
    locator: pp. 139 to 152
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 10.1.1, Left-Corner Parsing, p. 344
  - paper: doi:10.3115/976744.976780
    title: Mark-Jan Nederhof, Generalized left-corner parsing, Sixth Conference of the European Chapter of the Association for Computational Linguistics (1993)
    locator: the paper starting on p. 305
  - paper: doi:10.1007/1-4020-2295-6_9
    title: Robert C. Moore, Improved left-corner chart parsing for large context-free grammars, in New Developments in Parsing Technology, Kluwer (2004)
    locator: pp. 185 to 201
  - paper: doi:10.3115/992066.992098
    title: Philip Resnik, Left-corner parsing and psychological plausibility, COLING 1992
    locator: the paper starting on p. 191
---

A left-corner parser recognizes the first symbol of each production bottom-up, from the input, and predicts the remaining symbols top-down, as goals. It decides to use a production only after it has found the production's left corner, the first symbol of its right side, so it handles [left recursion](/left-recursion/), which defeats [top-down parsers](/top-down-parsing/), and it makes fewer guesses than a purely top-down parser. The tabular form on this page runs all choices of a left-corner parser at once with a chart, accepts every [context-free grammar](/context-free-grammar/), and takes $O(n^3)$ time for a fixed grammar.

## In plain words

A top-down parser guesses which rule to use before it reads anything, and it can loop forever on a rule that starts with itself. A bottom-up parser waits until a whole rule is read, and it often has to remember many unfinished pieces. A left-corner parser is in between. It reads the first piece of the input and asks which rules can start with it. It picks such a rule, and only then does it predict the rest of that rule. When the finished rule is the thing it was looking for, the goal is reached. If not, the finished rule may in turn be the first piece of a larger rule, and the parser goes up one more step. The chart version tries all rules that fit and remembers every result, so it never repeats work.

## The problem

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

The input is a context-free grammar $G = (V, \Sigma, P, S)$, with any productions, and a word $w = a_1 \cdots a_n$. The output is yes when $S \Rightarrow^* w$ and no otherwise ([membership problem](/cfg-membership-problem/)). Let $N = |V|$.

## The algorithm

**Left corners.** The left corner of a production $A \to X \gamma$ is its first symbol $X$. A nonterminal $B$ is a **left corner of** $C$, written $B \in L(C)$, if $B = C$ or there is a chain of productions $C \to B_1 \gamma_1$, $B_1 \to B_2 \gamma_2$, $\ldots$, $B_{m-1} \to B \gamma_m$. So $L(C)$ is the set of nonterminals that can appear on the left edge of a [parse tree](/parse-tree/) of $C$, with the left edge followed only through first symbols.

**The left-corner parser.** A left-corner parser is a [pushdown](/pushdown-automaton/) parser with a stack of goals. To find a goal $C$ at the current position, it reads a terminal $a$ or uses an empty production $D \to \varepsilon$, which gives a found symbol $X$. Then it repeats two moves. If $X = C$, the goal is reached, and the parser may stop here. If some production $D \to X \gamma$ has $D \in L(C)$, the parser may *announce* it: it pushes the symbols of $\gamma$ as new goals, finds them one by one from left to right, and then has found $D$, which is the new $X$. The first symbol of each production is found bottom-up, and the rest top-down. When the choices are fixed by $k$ symbols of lookahead, this is the deterministic LC($k$) parser of Rosenkrantz and Lewis. For other grammars, the parser has to guess.

**The chart.** The algorithm below follows all choices at once, in the manner of the [Earley parser](/earley-parser/). An item $[C, i, B \to \alpha \bullet \beta]$ in the set $E[k]$ says: while looking for the goal $C$ from position $i$, the parser has found $\alpha$ from $i$ to $k$, and $B \in L(C)$. The set $\mathrm{DONE}$ holds the triples $(C, i, k)$ such that the goal $C$ was found from $i$ to $k$. An item with $\beta = Y \beta'$ for a nonterminal $Y$ **waits** on the goal $(Y, k)$.

```pseudo id=main
LEFT-CORNER(G, w)                                  ▷ w = a1 … an
L1  for each C ∈ V compute L(C), the nonterminals B such that C = B or C → B₁ …, B₁ → B₂ …, …, B_{m−1} → B …
L2  E[0], …, E[n] ← ∅; DONE ← ∅; START(S, 0)
L3  for k ← 0 to n do
L4      for each item [C, i, B → α • β] in E[k], in the order of insertion, do   ▷ E[k] grows during the loop
L5          if β = ε then                          ▷ B found from i to k; once for each (C, i, B, k)
L6              if B = C and (C, i, k) ∉ DONE then add (C, i, k) to DONE, and for each [C′, i′, D → γ • C δ] waiting on (C, i) add [C′, i′, D → γ C • δ] to E[k]
L7              for each D → B γ in P with D ∈ L(C) do add [C, i, D → B • γ] to E[k]   ▷ announce D
L8          else if β = Y β′ with Y ∈ V then
L9              if (Y, k) is not yet a goal then START(Y, k)
L10             record the item as waiting on (Y, k)
L11             for each (Y, k, k′) ∈ DONE do add [C, i, B → α Y • β′] to E[k′]
L12         else if k < n and β = a_{k+1} β′ then add [C, i, B → α a_{k+1} • β′] to E[k + 1]
L13 return true if (S, 0, n) ∈ DONE, else false

START(C, k)                                         ▷ make (C, k) a goal: find its left corners
L14 if k < n then for each D → a_{k+1} γ in P with D ∈ L(C) do add [C, k, D → a_{k+1} • γ] to E[k + 1]
L15 for each D → ε in P with D ∈ L(C) do add [C, k, D → •] to E[k]
```

"Add" does nothing when the item is already in the set. Line L1 is a graph search from each nonterminal along the edges $A \to B$ for the productions whose right side starts with the nonterminal $B$. Lines L14 and L15 start a goal from the bottom: a terminal or an empty right side. Line L7 goes up one level, from a found symbol to a production that starts with it, but only to productions whose left side is a left corner of the goal. This test is the top-down filter. Lines L9 to L11 are the top-down part: they make the next symbol a goal and use what is known about it. A completion found later reaches the waiting item by line L6, and one found earlier by line L11, so the order of the work does not matter. At line L11, every entry $(Y, k, k')$ in DONE has $k' = k$, because the sets are processed in the order of $k$.

## Example

Take the left-recursive grammar $E \to E + T \mid T$, $T \to a$, and $w = a + a$. Then $L(E) = \{E, T\}$ and $L(T) = \{T\}$. START$(E, 0)$ adds $[E, 0, T \to a \bullet]$ to $E[1]$, since $T \in L(E)$ and $T \to a$ starts with $a_1 = a$. The chart:

| Set | Items, in the order of insertion | New in DONE |
|---|---|---|
| $E[0]$ | none | |
| $E[1]$ | $[E, 0, T \to a \bullet]$, $[E, 0, E \to T \bullet]$, $[E, 0, E \to E \bullet + T]$ | $(E, 0, 1)$ |
| $E[2]$ | $[E, 0, E \to E + \bullet T]$ | |
| $E[3]$ | $[T, 2, T \to a \bullet]$, $[E, 0, E \to E + T \bullet]$, $[E, 0, E \to E \bullet + T]$ | $(T, 2, 3)$, $(E, 0, 3)$ |

In $E[1]$, the item for $T \to a$ is complete and $T \ne E$, so line L7 announces $E \to T$. That item is complete with $E$ equal to the goal, so line L6 records $(E, 0, 1)$, and line L7 announces $E \to E + T$, since $E$ is its own left corner. This is how the parser handles left recursion: it never predicts $E \to E + T$ before it has found an $E$. Line L12 matches $+$. In $E[2]$, the item waits on $T$, and START$(T, 2)$ adds $[T, 2, T \to a \bullet]$ to $E[3]$. In $E[3]$, this item completes the goal $(T, 2)$, line L6 moves the waiting item to $[E, 0, E \to E + T \bullet]$, and this completes $(E, 0, 3)$. Line L13 accepts. An Earley parser on the same input also predicts $E \to \bullet E + T$, $E \to \bullet T$ and $T \to \bullet a$ at position 0, before it reads anything.

## Correctness

**Claim.** When the loop of line L3 ends, $(C, i, k) \in \mathrm{DONE}$ exactly when $(C, i)$ is a goal and $C \Rightarrow^* a_{i+1} \cdots a_k$. Since $(S, 0)$ is a goal from line L2, line L13 returns true if and only if $w \in L(G)$.

*Soundness.* Every item $[C, i, B \to \alpha \bullet \beta] \in E[k]$ has $B \in L(C)$ and $\alpha \Rightarrow^* a_{i+1} \cdots a_k$, with $\alpha \ne \varepsilon$ unless $B \to \varepsilon$. Each line keeps this: lines L14 and L15 start with a terminal that matches or an empty right side, line L7 uses a found $B$ as the first symbol of $D \to B \gamma$ with $D \in L(C)$, and lines L6, L11 and L12 extend $\alpha$ by a symbol that derives the next part of the input. A complete item with $B = C$ then gives $C \Rightarrow^* a_{i+1} \cdots a_k$.

*Completeness.* Take a parse tree of $C$ for $a_{i+1} \cdots a_k$, and follow its left edge from the root down to the bottom, a terminal leaf or a node with an empty production. All nodes on this edge are in $L(C)$, so START$(C, i)$ adds the item of the bottom production. Going up the left edge, each production is completed by goals for its other children, which are smaller trees and so are found by induction, and then line L7 announces the production above, until line L6 reaches the root. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The items of a set are hashed, the productions are indexed by their first symbol, and the waiting items are stored by goal.

- **Size.** There are at most $N (n + 1)$ goals. An item is a goal, one of $|G|$ dotted productions and an end position, so the chart holds $O(N |G| n^2)$ items, and this is the space.
- **Time.** Each item is processed once. Line L7 runs once for each goal, found symbol and end, and costs the number of productions that start with that symbol, $O(N |P| n^2)$ in total. Lines L9, L10 and L12 take $O(1)$ time per item, and line L11 adds at most one item, since $k' = k$. Line L6 moves each waiting item once for each end of its goal, at most $n + 1$ times, for $O(N |G| n^3)$ time. So the time is $O(N |G| n^3)$, which is $O(n^3)$ for a fixed grammar.
- **Linear cases.** On many grammars the chart stays small. For $S \to S a \mid b$ there is one goal, and for $S \to a S \mid b$ there is one goal per position with $O(1)$ items each, so the time is $O(n)$.

## Properties

- **General.** The tabular form accepts every context-free grammar, with empty and unit productions, cycles, left recursion and ambiguity. The deterministic LC($k$) form needs an LC($k$) grammar.
- **Online.** The sets are processed from left to right, and $E[k]$ depends only on $a_1 \cdots a_k$.
- **Left recursion.** A left-recursive production is announced only after its left corner is found, so the parser never predicts an unbounded chain of the same goal at one position.
- **Fewer predictions than Earley.** Only symbols after the first of a production become goals. The first symbol is reached from the input, through the left-corner relation.
- **Deterministic.** The chart is a function of the grammar and the input.

## Variants and improvements

- **Deterministic LC($k$) parsing.** If $k$ symbols of lookahead always decide between the announce and the goal moves, the parser runs in $O(n)$ time with a stack and a table. Rosenkrantz and Lewis defined the LC($k$) grammars and showed that an LC($k$) grammar can be transformed into an LL($k$) grammar.
- **The left-corner transform.** A grammar can be rewritten into an equivalent grammar whose top-down parse follows the left-corner parse of the original. The result has no left recursion, so it can be used with [recursive descent](/recursive-descent-parsing/) or [LL(1) parsing](/ll1-parsing/), and it is one way of [left recursion elimination](/left-recursion-elimination/).
- **Lookahead filters.** A production is announced only if the next input symbol can follow in it. Moore found that left-corner chart parsing with such filters runs faster than other chart parsers on large grammars.
- **Generalized LC parsing.** Nederhof applied the techniques of [GLR parsing](/glr-parsing/) to left-corner parsing, so that the parser follows all choices with shared stacks.
- **Parse trees.** Each item keeps the reason for its first insertion, as in the Earley parser, and following these back pointers gives a parse tree.
- **Arc-eager parsing.** Variants that attach found constituents as early as possible are used as models of human sentence processing.

## When to use it

Use left-corner parsing when the grammar is left-recursive but you want the goal-directed structure of a top-down parser, for example for a natural-language grammar or a grammar written by hand. Its tabular form is a general parser like [Earley's](/earley-parser/), often with smaller charts. For a programming-language grammar, an [LR parser](/lr-parsing/) or an [LL(1)](/ll1-parsing/) parser after [left recursion elimination](/left-recursion-elimination/) is usually simpler. If you need a deterministic parser for a left-recursive grammar with simple semantic actions, a deterministic LC($k$) parser or the left-corner transform followed by recursive descent is a good choice.

## Pitfalls

- **Left corners through empty symbols.** With $D \to \varepsilon$, the first terminal of $A \to D\, a$ is $a$, but its left corner is $D$. Some descriptions skip nullable symbols when they compute left corners. On this page, $L$ follows first symbols only, and the parser reaches $a$ through $D \to \varepsilon$ (line L15), the announce step to $A \to D \bullet a$, and a match. Mixing the two definitions gives wrong tables.
- **Completions found too early.** A goal can be completed at its own position, by empty productions, before an item waits on it. Without line L11 that item never advances. With $S \to S\, S\, a \mid \varepsilon$ and the input $a$, the goal $(S, 0)$ is completed at 0 before the item $[S, 0, S \to S \bullet S\, a]$ waits on it, and the input is then rejected.
- **No top-down filter.** Announcing every production that starts with a found symbol, without the test $D \in L(C)$, is still correct, but it builds many items that no goal can use.
- **Naive backtracking.** A backtracking left-corner parser, without a chart, loops on cycles such as $A \to B$, $B \to A$, and on some grammars with empty productions, and can take exponential time.
- **Recursion depth.** Chains of goals can have length $n$, as in $S \to a S \mid b$. Process the sets with loops, not with recursive calls for goals.

## Implementations

## History

Rosenkrantz and Lewis introduced deterministic left-corner parsing and the LC($k$) grammars in 1970, as a class between the LL($k$) and the LR($k$) grammars. In computational linguistics, left-corner parsing became popular because it handles left-recursive grammars, and Nederhof (1993) and Moore (2004) gave general forms for all grammars. Resnik (1992) studied left-corner parsing as a model of human memory use during sentence processing.

## References
