---
tag: C4WSKR
kind: technique
slug: backtracking-parsing
name: Backtracking parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Top-down parsing that tries alternatives and undoes choices on failure.
prereqs: [context-free-grammar, top-down-parsing, leftmost-derivation, left-recursion]
see_also: [recursive-descent-parsing, packrat-parsing, parsing-expression-grammar, backtracking-regex-matching, earley-parser, left-recursion-elimination, generic-backtracking-algorithm, memoization]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.1, Recursive-Descent Parsing (the backtracking parser for S → c A d, A → a b | a, and the loop on left recursion)
  - book: isbn:9780139145568
    title: Alfred V. Aho and Jeffrey D. Ullman, The Theory of Parsing, Translation, and Compiling, Volume I, Parsing, Prentice Hall, 1972
    locator: Chapter 4, General Parsing Methods, Section 4.1, Backtrack Parsing
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 6, General Directional Top-Down Parsing (depth-first search, and the problems with left recursion)
  - paper: doi:10.1145/581478.581483
    title: Bryan Ford, Packrat parsing, simple, powerful, lazy, linear time, ICFP 2002
    locator: pp. 36 to 47 (exponential backtracking and its removal by memoization)
---

Backtracking parsing is the simplest general [top-down parsing](/top-down-parsing/) method: to expand a nonterminal it tries the alternatives of the [grammar](/context-free-grammar/) one after the other, and when a choice leads to a mismatch it undoes the choice and tries the next one. It is a depth-first search for a [leftmost derivation](/leftmost-derivation/) of the input. It accepts every grammar without [left recursion](/left-recursion/), including ambiguous ones, but it can take exponential time, and it loops forever on a left-recursive grammar. [Recursive descent](/recursive-descent-parsing/), [packrat parsing](/packrat-parsing/) and the [Earley parser](/earley-parser/) are the ways to keep its simplicity and remove its cost.

## In plain words

You read the input from left to right and keep a list of things that you still expect to see, at first only "a whole program". If the first expected thing is a token, it must be the next token of the input; if it is, move on, and if not, this attempt has failed. If the first expected thing is a grammar rule with several forms, pick the first form, put its parts at the front of the list, and continue.

When an attempt fails, go back to the last place where you had a choice, and take the next form there. You undo everything that you did after that choice, including the tokens that you read. You succeed when the list and the input run out at the same time. You fail when no choice is left anywhere.

## When it applies

- **A small or one-off grammar.** The template is a few lines of code, needs no table, and works for any grammar without left recursion, including ambiguous grammars and grammars that are not LL(k).
- **Short inputs or shallow nesting.** The cost of backtracking grows with the number of choices that fail late, so it is acceptable for commands, configuration lines and test inputs.
- **The grammar is written as code.** A hand-written [recursive descent](/recursive-descent-parsing/) parser that sometimes needs to try two branches, for example to tell a cast `(T) x` from a parenthesized expression, uses local backtracking.
- **Logic programming.** A definite clause grammar in Prolog runs exactly this search, through the backtracking of the Prolog engine.

It does not apply to grammars with left recursion unless you first [remove the left recursion](/left-recursion-elimination/), and it is a poor choice for long inputs with deep nesting.

## The template

**Notation.** The grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, the input is $w = w_1 \cdots w_n$, and $|G|$ is the size of the grammar. A position $i \in \{0, \ldots, n\}$ means that the first $i$ tokens are read.

The call PARSE$(\beta, i)$ answers the question "does the string of grammar symbols $\beta$ derive exactly the rest $w_{i+1} \cdots w_n$ of the input?". The string $\beta$ is the list of expected things from the plain description.

```pseudo id=main
PARSE(β, i)                                ▷ true if β ⇒* w[i+1 .. n]
L1  if β = ε then return ACCEPT(i)          ▷ hole ACCEPT: usually i = n
L2  X ← the first symbol of β;  γ ← the rest of β
L3  if X ∈ Σ then
L4      if i < n and w[i + 1] = X then return PARSE(γ, i + 1)
L5      return false                        ▷ mismatch: back up
L6  for each production X → α in ORDER(X) do  ▷ hole ORDER: the order of the alternatives
L7      RECORD(X → α)                       ▷ hole RECORD: build the derivation
L8      if PARSE(α γ, i) then return true
L9      UNDO(X → α)                         ▷ this choice failed: forget it
L10 return false

RECOGNIZE(w)
L11 return PARSE(S, 0)
```

Line L1 succeeds when nothing is expected and the input is used up. Lines L3 to L5 match a token. Lines L6 to L9 are the backtracking: each alternative of $X$ is tried with the same position $i$, so a failed alternative gives back every token it read. The holes are these.

- **ORDER(X)** fixes which alternative is tried first. It changes the time and the first parse found, but not the answer of RECOGNIZE.
- **RECORD and UNDO** keep a stack of the productions used. When RECOGNIZE returns true, the stack holds a leftmost derivation of $w$.
- **ACCEPT(i)** decides what counts as success. With $i = n$ the parser recognizes $w$. To list every parse, let ACCEPT output the recorded derivation and return false; the search then goes on through all choices.

**Correctness.** The call PARSE$(\beta, i)$ returns true if and only if $\beta \Rightarrow^* w_{i+1} \cdots w_n$. If it returns true, the recorded productions, applied in order, rewrite $\beta$ to the rest of the input, so the answer is sound. For the converse, take a leftmost derivation $\beta \Rightarrow^*_{lm} w_{i+1} \cdots w_n$. Its first step either matches the first symbol (a token) or expands it with some production $X \to \alpha$. The loop of line L6 tries that production, and by induction on the length of the derivation the inner call returns true. So the answer is complete, provided the search stops.

**Termination.** If no nonterminal $A$ has $A \Rightarrow^+ A \delta$, every call stops. The recursion has finite branching, so an infinite run needs an infinite chain of nested calls, by König's lemma. Along the chain the position never decreases and is at most $n$, so from some point the position stays at one value $i$, and no token is read. Each call in this part expands the first symbol of $\beta$, and the expansions build a tree whose finished parts all derive $\varepsilon$. This tree is infinite and finitely branching, so it has an infinite path of nodes, each a child of the one before, whose left siblings all derive $\varepsilon$. Some label $A$ appears twice on the path, which gives $A \Rightarrow^+ A \delta$, a contradiction.

**Cost.** Without left recursion the run is finite, but it can be exponential in $n$. Each failure late in the input undoes all the work since the last choice, and the same subproblem is solved again in each branch.

## Classic examples

- **The textbook case.** For $S \to c A d$, $A \to a b \mid a$ and the input $cad$, the parser matches $c$, tries $A \to ab$, matches $a$, fails on $d \ne b$, backs up to the same position, tries $A \to a$, and then matches $d$. This is the example of Aho, Lam, Sethi and Ullman, Section 4.4.1.
- **Exponential work.** For $E \to T + E \mid T$, $T \to a \mid ( E )$ and the input $(^d\, a\, )^d$ with $d$ levels of parentheses, each level first tries $T + E$, parses the whole inner part, fails on the missing $+$, and parses it again with the second alternative. The template makes $c(d)$ calls with $c(0) = 8$ and $c(d) = 2 c(d-1) + 10$, so $c(d) = 18 \cdot 2^d - 10$: 26 calls for $d = 1$ and 18422 calls for $d = 10$, on an input of 21 tokens.
- **[Recursive descent](/recursive-descent-parsing/).** For an [LL(1)](/ll1-parsing/) grammar the next token selects the alternative, ORDER puts only that one first, and no alternative ever fails after it has read a token. The template then runs in linear time with no backtracking.
- **[Backtracking regex matching](/backtracking-regex-matching/).** The engines of Perl, Python and Java run the same search on the parts of a regular expression, with the same exponential worst case.
- **[Packrat parsing](/packrat-parsing/).** It memoizes the result of each nonterminal at each position for a [parsing expression grammar](/parsing-expression-grammar/), which makes the limited backtracking of PEGs linear.
- **[Earley parsing](/earley-parser/).** It explores all alternatives at once, breadth first, and shares the subproblems in a chart. It parses every context-free grammar, left-recursive or not, in $O(n^3)$ time.

## Variations

- **Full backtracking (the template).** Complete for each grammar without left recursion: it finds a parse whenever one exists.
- **Limited backtracking, or ordered choice.** Each call of a nonterminal returns the first way its alternatives match and never retries it when a later part fails. This is the semantics of PEGs, and of many hand-written parsers. It is not complete for context-free grammars: with $S \to A c$, $A \to a \mid a b$, it rejects $abc$, because $A$ commits to $a$ and the later failure on $c$ does not come back into $A$.
- **Memoized sets of end positions.** Let a call of $X$ at position $i$ return the set of all $j$ with $X \Rightarrow^* w_{i+1} \cdots w_j$, and store it. Each pair $(X, i)$ is computed once, and each production costs $O(n^2)$ set work per symbol, so the total is $O(|G| \, n^3)$ time for a grammar without left recursion.
- **Breadth-first search.** Keep all partial parses at once and advance them token by token. This is the start of [chart parsing](/chart-parsing/) and of the Earley parser.
- **Cut and lookahead.** A parser can drop the other alternatives once a token proves a choice right (a cut in Prolog), or test a token before it tries an alternative. Both reduce the backtracking without changing the template.

## Pitfalls

- **Left recursion.** With $E \to E + a \mid a$, the call PARSE$(E, 0)$ tries $E \to E + a$ first and calls PARSE$(E + a, 0)$, which expands $E$ again at the same position, forever. Hidden left recursion loops in the same way: with $S \to A S c \mid b$ and $A \to \varepsilon$, the expansion $S \Rightarrow A S c \Rightarrow S c$ reads no token. Remove left recursion first, or use a method that handles it.
- **Committing too early.** A parser that returns from a nonterminal at its first success and never retries it is the limited variant above, not the template. It rejects strings of the language, and no order of the alternatives fixes this in general (see the exercises).
- **State that is not undone.** If an alternative changes a global variable, a symbol table or an output buffer, and UNDO does not restore it, the next alternative starts from a wrong state. Keep side effects out of the search, or undo them in line L9.
- **Deep recursion.** The depth of the calls grows with the length of $\beta$ and the input. In a language with a small call stack, use an explicit stack of goals.
- **Exponential time hidden by tests.** A parser that passes all tests on short inputs can take minutes on one deep input, as the example with $18 \cdot 2^d - 10$ calls shows. Add memoization, or use a deterministic or chart-based parser.

## Exercises

1. For $E \to T + E \mid T$, $T \to a \mid ( E )$, show that the number of calls on $(^d a )^d$ satisfies $c(d) = 2 c(d-1) + 10$, and solve the recurrence.
2. Let $S \to A a$ and $A \to a \mid a a$. Show that the limited variant with the order $a, aa$ rejects $aaa$, and with the order $aa, a$ rejects $aa$, although both strings are in the language. Show that the full template accepts both with either order.
3. Remove the left recursion from $E \to E + a \mid a$, run the template on $a + a + a$, and give the leftmost derivation that RECORD builds.
4. Change ACCEPT so that the template counts the parse trees of $w$ for $E \to E' + E \mid E'$, $E' \to a$ and for an ambiguous grammar of your choice. What happens for a grammar where some nonterminal has $A \Rightarrow^+ A$?

## References
