---
tag: 744Z4H
kind: technique
slug: chart-parsing
name: Chart parsing
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Dynamic programming over a chart of partial parse items, avoiding repeated work.
prereqs: [context-free-grammar, parse-tree, overlapping-subproblems, cfg-membership-problem]
see_also: [earley-parser, cyk-algorithm, left-corner-parsing, shared-packed-parse-forest, probabilistic-context-free-grammar, cfl-reachability, backtracking-parsing, glr-parsing]
sources:
  - paper: doi:10.1145/362007.362035
    title: Jay Earley, An efficient context-free parsing algorithm, Communications of the ACM 13(2) (1970)
    locator: pp. 94 to 102 (dotted items in sets by position, with predictor, scanner and completer)
  - paper: doi:10.1016/0743-1066(95)00035-I
    title: Stuart M. Shieber, Yves Schabes and Fernando C. N. Pereira, Principles and implementation of deductive parsing, Journal of Logic Programming 24(1-2) (1995)
    locator: pp. 3 to 36 (parsers as deduction systems, run by one agenda-driven chart engine)
  - url: https://doi.org/10.1007/978-3-642-60541-3
    title: Klaas Sikkel, Parsing Schemata, A Framework for Specification and Analysis of Parsing Algorithms, Springer (1997)
    locator: Chapter 4, Item-based parsing schemata
  - book: isbn:9780131873216
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, second edition
    locator: Chapter 13, Syntactic Parsing (dynamic programming parsing methods, CKY, Earley and chart parsing)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 7, General Directional Bottom-Up Parsing (Earley parsing and chart parsing)
  - paper: doi:10.1093/comjnl/45.6.620
    title: John Aycock and R. Nigel Horspool, Practical Earley parsing, The Computer Journal 45(6) (2002)
    locator: pp. 620 to 630 (the problem with empty productions in set-at-a-time Earley parsers and its fix)
  - url: https://aclanthology.org/J99-4004/
    title: Joshua Goodman, Semiring parsing, Computational Linguistics 25(4) (1999)
    locator: pp. 573 to 605 (one item-based algorithm computes recognition, counts, Viterbi scores and inside probabilities)
  - paper: doi:10.3115/1073445.1073461
    title: Dan Klein and Christopher D. Manning, A* parsing, fast exact Viterbi parse selection, Proceedings of HLT-NAACL 2003
    locator: pp. 40 to 47 (an agenda ordered by score plus an admissible estimate)
---

Chart parsing is a way to parse with any [context-free grammar](/context-free-grammar/) by storing every partial result in a table, the *chart*, so that no piece of the input is analysed twice for the same purpose. Each entry, or *item*, says that a part of a grammar rule matches a span of the input; new items are derived from old ones by a few inference rules, and an *agenda* holds the items that are derived but not yet used. Different choices of items, rules and agenda order give [CYK](/cyk-algorithm/), [Earley's parser](/earley-parser/), [left-corner](/left-corner-parsing/) parsers and best-first probabilistic parsers, all in $O(n^3 |G|)$ time with suitable indexes.

## In plain words

A naive parser tries one rule, fails later, backs up, and tries again, and it can rebuild the same phrase many times on the way. A chart parser writes down every phrase it has found, with its start and end position, and every half-finished rule it is waiting to complete.

When it finds a new phrase, it looks for half-finished rules that end just where the phrase starts and need exactly that kind of phrase, and extends them. When it starts a new half-finished rule, it looks for phrases that are already in the chart. A finished rule is a new phrase. Nothing is written twice, so the work stays bounded even when the sentence has many readings.

The sentence is grammatical when the chart holds a finished sentence that covers the whole input.

## When it applies

- **The grammar is general.** It can be ambiguous, left-recursive, or contain empty and unit productions. Chart parsing needs no special form of grammar, unlike [LL](/ll1-parsing/) and [LR](/lr-parsing/) parsing.
- **The subproblems are spans.** The question "does this symbol, or this part of a rule, derive the input between positions $i$ and $j$" has an answer that does not depend on how the rest of the input is parsed. This is what context-freeness gives, and it is what lets one stored answer be reused.
- **All analyses, or the best one, are needed.** The chart represents all parses at once, and a [shared forest](/shared-packed-parse-forest/) or a best tree can be read from it.
- **The input may be more than a string.** The same engine parses a word lattice or a graph, where positions are vertices, as in [CFL reachability](/cfl-reachability/).

## The template

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, the input is $w = w_1 \cdots w_n$ with positions $0, \ldots, n$ between the symbols, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

An *item* $[i, A \to \alpha \bullet \beta, j]$ says that $A \to \alpha \beta$ is a production and $\alpha \Rightarrow^* w_{i+1} \cdots w_j$. It is *active* if $\beta \ne \varepsilon$, waiting for $\beta$, and *passive* if $\beta = \varepsilon$, a finished constituent $A$ over the span $(i, j)$. The input symbols are passive items $[i-1, w_i, i]$.

```pseudo id=main
CHART-PARSE(G, w)
L1  chart ← ∅
L2  agenda ← the axioms                                   ▷ hole: AXIOMS(G, w)
L3  while agenda is not empty do
L4      x ← take an item from agenda                      ▷ hole: the agenda order
L5      if x ∈ chart then continue
L6      add x to chart
L7      for each item y that a rule derives from x and items of chart do   ▷ hole: the rules
L8          put y on agenda
L9  return whether [0, S → γ •, n] ∈ chart for some γ    ▷ hole: the goal and what to output
```

The *fundamental rule* is common to all chart parsers: from $[i, A \to \alpha \bullet B \beta, k]$ and $[k, B \to \gamma \bullet, j]$, derive $[i, A \to \alpha B \bullet \beta, j]$, and the same with a terminal $a = w_j$ for $B$ and $k = j - 1$, which is the *scan*. Line L7 applies it in both directions: a new active item is combined with the passive items already in the chart that start where it ends, and a new passive item with the active items that end where it starts.

The holes are filled by a *strategy*:

- **Top-down (Earley).** Axioms $[0, S \to \bullet \gamma, 0]$. Extra rule, *predict*: from $[i, A \to \alpha \bullet B \beta, j]$ derive $[j, B \to \bullet \gamma, j]$ for every production of $B$.
- **Bottom-up.** Axioms $[i, A \to \bullet \gamma, i]$ for every production and every position $i$. No extra rule.
- **Left corner.** Axioms $[i, A \to \bullet, i]$ for the empty productions. Extra rule: from a passive $[i, B \to \gamma \bullet, j]$, or an input symbol $B = w_j$ with $i = j - 1$, derive $[i, A \to B \bullet \beta, j]$ for every production $A \to B \beta$.

**Why it is correct.** *Soundness:* each rule keeps the invariant that $\alpha \Rightarrow^* w_{i+1} \cdots w_j$ for every item, so a goal item means $S \Rightarrow^* w$. *Completeness:* for the bottom-up and left-corner strategies, induction on the height of a parse tree shows that every constituent $A \Rightarrow^* w_{i+1} \cdots w_j$ becomes a passive item; for the top-down strategy, every constituent of every parse tree of $w$ does, by induction along a leftmost derivation. Line L5 makes the loop end, since there are finitely many items.

**Cost.** There are at most $O(|G| n^2)$ items, one per dotted production and pair of positions. With the active items indexed by their end and the symbol after the dot, and the passive items by their start and symbol, each fundamental-rule step for a new item meets at most $n$ partners per dotted production, so the total time is $O(|G| n^3)$ and the space $O(|G| n^2)$. For an unambiguous grammar the top-down strategy takes $O(|G| n^2)$ time, and for many [LR](/lr-parsing/) grammars linear time.

**From recognizer to parser.** Recording, for each item, the pairs of items that derived it turns the chart into a [shared packed parse forest](/shared-packed-parse-forest/) of size $O(|G| n^3)$, from which one tree, all trees, or their number can be read.

## Classic examples

**A prepositional phrase.** Take the grammar
$$S \to NP\ VP, \quad NP \to she \mid Det\ N \mid NP\ PP, \quad VP \to V\ NP \mid VP\ PP, \quad PP \to P\ NP,$$
with $Det \to the$, $N \to man \mid telescope$, $V \to saw$, $P \to with$, and the input "she saw the man with the telescope", $n = 7$. It has 2 parse trees: the telescope belongs to the seeing or to the man. Every strategy finds the same 15 constituents:
$$\begin{aligned}
&NP(0,1),\ V(1,2),\ Det(2,3),\ N(3,4),\ P(4,5),\ Det(5,6),\ N(6,7),\ NP(2,4),\ NP(5,7),\\
&VP(1,4),\ PP(4,7),\ S(0,4),\ NP(2,7),\ VP(1,7),\ S(0,7).
\end{aligned}$$
$VP(1,7)$ is built twice, as $V\ NP(2,7)$ and as $VP(1,4)\ PP(4,7)$, but it is stored once, so $S(0,7)$ is built once. The two readings share all the other constituents. A script counts the items: the top-down strategy makes 53 items, of which 37 are active, the bottom-up strategy 126, of which 110 are active, and the left-corner strategy 30, of which 14 are active. Top-down prediction avoids most useless active items, and the left-corner rule avoids starting rules whose first symbol is absent.

**CYK** is the chart parser for a grammar in [Chomsky normal form](/chomsky-normal-form/) whose items are only passive, $[A, i, j]$, with the agenda order "by span length", so that each item is complete when it is used. The fundamental rule is $A \to BC$ with $[B, i, k]$ and $[C, k, j]$.

**Earley's parser** is the top-down strategy with the agenda order "by end position", so that the chart is the sequence of Earley sets.

**Probabilistic parsing.** For a [probabilistic grammar](/probabilistic-context-free-grammar/), the agenda is a priority queue ordered by the probability of the best derivation of each item. Taking items in that order, as in [Dijkstra's algorithm](/dijkstra/), the first goal item gives the [most probable parse](/most-probable-parse/); A* parsing adds an estimate of the outside probability to the priority.

**Graphs.** With the vertices of a labelled graph as positions, the bottom-up strategy solves [CFL reachability](/cfl-reachability/).

## Variations

- **Agenda order.** A stack, a queue, an order by position, or a priority queue all give the same final chart when every item is processed, because the closure of the rules does not depend on the order. The order matters for parsing in one left-to-right pass, which needs the order by end position, and for best-first search, which may stop early.
- **Deductive parsing.** Shieber, Schabes and Pereira write each parser as axioms, inference rules and goals, and run all of them with one engine. Sikkel's *parsing schemata* compare parsers by mapping items of one onto items of another.
- **Semiring parsing.** Goodman replaces "the item exists" by a value in a semiring computed over all derivations of the item: Boolean for recognition, natural numbers for the number of trees, max-times for the best tree, and sum-times for the [inside probabilities](/inside-outside-algorithm/). The engine stays the same.
- **Filtering.** Lookahead, or a left-corner relation computed from the grammar, rejects items that cannot lead to a complete parse.
- **Rich grammars.** For unification and feature grammars, an item carries a feature structure, and the test of line L5 becomes a test whether the chart already has an item that is at least as general.
- **Generalized LR and GLL.** [GLR](/glr-parsing/) and [GLL](/gll-parsing/) parsers use states of an automaton in place of dotted productions, and a graph-structured stack in place of the active items.

## Pitfalls

- **Combining in one direction only.** If line L7 combines a new passive item only with the active items present at that moment, an active item that arrives later misses it. This happens with empty constituents: a top-down parser processing the items of one position in order can complete $[j, B \to \bullet, j]$ before the item that waits for $B$ at $j$ exists. Combining in both directions, or the fix of Aycock and Horspool for set-at-a-time Earley parsers, avoids it.
- **No duplicate test.** Without line L5 the loop does not end on a grammar with a cycle $A \Rightarrow^+ A$ or with left recursion under the top-down strategy, and it does exponential work on ambiguous inputs.
- **Missing indexes.** Scanning the whole chart for partners at line L7 makes each step cost $O(|G| n^2)$ in place of $O(n)$ per dotted production, and the total time $O(|G|^2 n^4)$. The indexes by position and symbol are what makes the bound cubic.
- **Listing all trees.** The chart is polynomial, but the number of trees can be exponential, or infinite with cyclic grammars. Output the forest, or enumerate trees lazily.
- **Constituents that cannot be used.** The bottom-up strategy builds every constituent of every substring, including many that fit in no complete parse. Top-down prediction or a left-corner filter removes most of them.

## Exercises

1. Write the deduction system for CYK on a grammar in Chomsky normal form, and show that the bottom-up strategy restricted to it builds exactly the CYK table.
2. Show that the top-down strategy builds $[i, A \to \alpha \bullet \beta, j]$ only if $S \Rightarrow^* w_1 \cdots w_i A \delta$ for some $\delta$.
3. For $S \to S S \mid a$ and the input $a^n$, count the passive items and the fundamental-rule steps, and show that the time is $\Theta(n^3)$.
4. Give the agenda order and the item values that make the chart engine compute the number of parse trees of $w$, and say what happens when the grammar has a cycle $A \Rightarrow^+ A$.
5. Extend the engine to a word lattice, a directed acyclic graph of word positions, and give its running time in the number of lattice nodes.

## References
