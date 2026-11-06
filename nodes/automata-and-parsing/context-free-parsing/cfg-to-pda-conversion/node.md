---
tag: X117M6
kind: algorithm
slug: cfg-to-pda-conversion
name: CFG to pushdown automaton conversion
area: automata-and-parsing/context-free-parsing
level: core
summary: Builds a pushdown automaton that accepts exactly the language of a given context-free grammar.
model: word-ram
complexity:
  vars: {g: the grammar size, σ: the number of terminals}
  time: {worst: O(g + σ)}
  space: {extra: O(g + σ)}
properties: {deterministic: true, recursive: false}
history:
  year: 1963
  people: [Noam Chomsky, R. James Evey, Marcel-Paul Schützenberger]
  note: The equivalence of context-free grammars and pushdown-store machines was proved independently in 1962 and 1963; the one-state top-down automaton is the standard construction for the direction from grammars to automata.
prereqs: [context-free-grammar, pushdown-automaton, leftmost-derivation]
see_also: [cfg-pda-equivalence, top-down-parsing, ll1-parsing, greibach-normal-form, shift-reduce-parsing, recursive-descent-parsing, left-recursion, pushdown-automaton]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 6.3.1, From Grammars to Pushdown Automata (the one-state automaton and the proof by leftmost derivations), and Section 7.4.1, Complexity of Converting Among CFG's and PDA's
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.2, Pushdown Automata (Lemma 2.21, the automaton with states q_start, q_loop and q_accept and the bottom marker $)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 6, General Directional Top-Down Parsing (the pushdown automaton of a grammar and its simulation)
  - paper: doi:10.1016/S0019-9958(63)90306-1
    title: Marcel-Paul Schützenberger, On context-free languages and push-down automata, Information and Control 6(3) (1963)
    locator: pp. 246 to 264
---

The CFG to PDA conversion turns a [context-free grammar](/context-free-grammar/) into a [pushdown automaton](/pushdown-automaton/) that accepts the same language. The automaton has a single state. It keeps on its stack the part of the sentence that it still expects: a nonterminal on top is replaced by the right side of one of its productions, and a terminal on top is matched against the next input symbol. Its accepting runs are exactly the [leftmost derivations](/leftmost-derivation/) of the grammar, which proves one half of the [equivalence of grammars and pushdown automata](/cfg-pda-equivalence/) and is the model behind every [top-down parser](/top-down-parsing/).

## In plain words

Think of the stack as a list of things still to read. At the start it holds only the start symbol, which stands for "a whole sentence".

At each step the machine looks at the top of the list. If it is a rule symbol, the machine picks one of that symbol's rules and replaces the symbol by the rule's right side. If it is a letter, the next letter of the input must be the same; the machine reads it and removes it from the list.

The input is accepted when the list is empty at the moment the input ends. The machine guesses the rules, and it accepts if some sequence of guesses works. The guesses it makes are a derivation of the input, expanding the leftmost symbol first.

## The problem

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$, and $\sigma = |\Sigma|$. A PDA is $P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$, with configurations $(q, w, \gamma)$ that show the top of the stack on the left. It accepts $N(P)$ by empty stack and $L(P)$ by final state.

**Input.** A context-free grammar $G$ with $V \cap \Sigma = \emptyset$.

**Output.** A PDA $P$ with $N(P) = L(G)$, or, in the second version, with $L(P) = L(G)$.

## The algorithm

```pseudo id=main
CFG-TO-PDA(G)                              ▷ acceptance by empty stack
L1  P ← a PDA with one state q, stack alphabet V ∪ Σ, start symbol S and no moves
L2  for each production A → α in R do
L3      add (q, α) to δ(q, ε, A)                ▷ expand: replace A by α, read nothing
L4  for each terminal a in Σ do
L5      add (q, ε) to δ(q, a, a)                ▷ match: read a and pop a
L6  return P

CFG-TO-PDA-FINAL(G)                        ▷ acceptance by final state
L7  P ← CFG-TO-PDA(G); add new states s and f and a new stack symbol ⊥
L8  add (q, S⊥) to δ(s, ε, ⊥)                  ▷ put S above the bottom marker
L9  add (f, ⊥) to δ(q, ε, ⊥)                   ▷ the marker is on top: all of S was matched
L10 make s the start state and ⊥ the start symbol, set F ← {f}, and return P
```

Lines L3 and L5 are the whole idea. An expand move does one step of a leftmost derivation: the nonterminal on top of the stack is the leftmost nonterminal of the sentential form that is not yet matched. A match move checks one terminal of the sentential form against the input. The stack, read from the top, is always the unmatched rest of the current sentential form.

The second version is for definitions of PDAs that accept by final state, as in Sipser's book. The bottom marker $\bot$ lets the machine see that the stack above it is empty, which a PDA cannot otherwise test.

## Example

For $G$ with $S \to a S b \mid \varepsilon$, the algorithm gives two expand moves and two match moves:
$$\delta(q, \varepsilon, S) = \{(q, aSb), (q, \varepsilon)\}, \qquad \delta(q, a, a) = \{(q, \varepsilon)\}, \qquad \delta(q, b, b) = \{(q, \varepsilon)\}.$$
An accepting run on $aabb$, with the derivation step that each expand move performs:

| move | state | unread input | stack (top first) | sentential form |
|---|---|---|---|---|
| start | $q$ | $aabb$ | $S$ | $S$ |
| expand $S \to aSb$ | $q$ | $aabb$ | $aSb$ | $aSb$ |
| match $a$ | $q$ | $abb$ | $Sb$ | $aSb$ |
| expand $S \to aSb$ | $q$ | $abb$ | $aSbb$ | $aaSbb$ |
| match $a$ | $q$ | $bb$ | $Sbb$ | $aaSbb$ |
| expand $S \to \varepsilon$ | $q$ | $bb$ | $bb$ | $aabb$ |
| match $b$ | $q$ | $b$ | $b$ | $aabb$ |
| match $b$ | $q$ | $\varepsilon$ | $\varepsilon$ | $aabb$ |

The run has $7 = |w| + 3$ moves: one match move for each input symbol and one expand move for each step of the derivation $S \Rightarrow aSb \Rightarrow aaSbb \Rightarrow aabb$. At every row, the input read so far followed by the stack is the sentential form. On the input $abab$ every run fails. After the first $a$ the stack is $Sb$ and the next input is $b$, so only $S \to \varepsilon$ can continue; matching $b$ then empties the stack with $ab$ still unread, and a machine with an empty stack has no move.

For the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid a$ the machine has $6 + 5 = 11$ moves, and the test suite checks that it accepts $a$, $a + a * a$ and $(a + a) * a$ and rejects $a+$, $(a$ and the empty input.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). The key lemma is that for all terminal strings $x, y$ and every string $\alpha$ of grammar symbols,
$$(q, xy, \alpha) \vdash^* (q, y, \varepsilon) \iff \alpha \Rightarrow^*_{lm} x.$$
The direction from left to right is an induction on the number of moves: the first move is a match, which removes a terminal from both sides, or an expand by $A \to \beta$, which is the first step of a leftmost derivation from $A\alpha'$. The other direction is an induction on the length of the derivation and the length of $\alpha$. With $\alpha = S$ and $y = \varepsilon$ this gives $N(P) = L(G)$, since every derivation can be made leftmost. For the second version, the bottom marker is on top exactly when the run of the first version has emptied its stack, so $L(P') = L(G)$.

## Complexity

**Time and size.** Lines L2 and L3 store each right side once, $O(|G|)$ work and space, and lines L4 and L5 add $\sigma$ moves. So the algorithm takes $O(|G| + \sigma)$ time, and the PDA has $|R| + \sigma$ moves, plus 2 in the second version, with total size $O(|G| + \sigma)$. This is optimal, since the output must contain every production.

**Runs of the output.** An accepting run on $w$ has $|w| + k$ moves, where $k$ is the length of the leftmost derivation. The machine is nondeterministic, and with [left recursion](/left-recursion/) it has infinite runs that read nothing: from $E$ on top it can expand $E \to E + T$ forever. So the PDA is a description of the language, not an efficient recognizer. Deciding whether it accepts $w$ needs a general method, such as the summary computation of [pushdown saturation](/pushdown-saturation/) or a grammar algorithm like [CYK](/cyk-algorithm/) or [Earley](/earley-parser/).

## Properties

- **One state.** The state carries no information; the stack does all the work. So every context-free language is accepted by empty stack by a one-state PDA.
- **Runs are derivations.** Accepting runs on $w$ correspond one to one to leftmost derivations of $w$, so to the [parse trees](/parse-tree/) of $w$. The number of accepting runs is the degree of [ambiguity](/ambiguity/) of $w$.
- **Prefix property of the stack.** In every configuration, the input read so far followed by the stack contents is a left sentential form.
- **Nondeterminism.** The machine is deterministic exactly when every nonterminal has one production, which almost never holds. Using lookahead to choose among the productions is [LL(1) parsing](/ll1-parsing/).
- **$\varepsilon$-moves.** Every expand move reads nothing, so the machine is not real-time.

## Variants and improvements

- **Greibach normal form.** If $G$ is in [Greibach normal form](/greibach-normal-form/), each production is $A \to a B_1 \cdots B_k$, and the move $(q, B_1 \cdots B_k) \in \delta(q, a, A)$ does the expand and the match at once. The machine then has no $\varepsilon$-moves and reads one symbol per move, so every run on $w$ has exactly $|w|$ moves.
- **Bottom-up automaton.** A second construction shifts input symbols onto the stack and replaces a right side $\alpha$ on top by $A$. Its runs are rightmost derivations in reverse. Popping $|\alpha|$ symbols needs a chain of intermediate states, since a move pops one symbol. This is the model of [shift-reduce parsing](/shift-reduce-parsing/).
- **Deterministic versions.** A table that picks the production from the next input symbol turns the top-down machine into an [LL(1) parser](/ll1-parsing/), and [recursive descent](/recursive-descent-parsing/) implements the same machine with the call stack.
- **The reverse direction.** The [triple construction](/cfg-pda-equivalence/) builds a grammar from any PDA; applied to the output of this algorithm it gives back a grammar with the same language.

## When to use it

Use it in proofs, to move a question about grammars to automata, for example to intersect a context-free language with a regular one by running a finite automaton beside the PDA, or to show that the [CFL emptiness](/cfg-emptiness-problem/) and membership questions for PDAs and grammars are the same. Use it to explain top-down parsing. Do not use the raw machine as a parser: its nondeterminism and its infinite runs on left-recursive grammars make a direct simulation exponential or nonterminating. For parsing, use a deterministic version such as LL(1), or a general algorithm.

## Pitfalls

- **Simulating by depth-first search.** A backtracking simulation that always tries $E \to E + T$ first never reads input on a left-recursive grammar. Remove [left recursion](/left-recursion-elimination/) first, or bound the stack by the input that is left.
- **Accepting with input left over.** Acceptance by empty stack requires that the stack becomes empty exactly when the input ends. A run that empties the stack earlier is stuck, not accepting.
- **Names.** A symbol must not be both a terminal and a nonterminal, or a match move and an expand move get the same top symbol. The implementation rejects such grammars.
- **Final state without a marker.** Under acceptance by final state, the version without $\bot$ cannot see that its stack is empty, and making $q$ final would accept every prefix that the run has read. Lines L7 to L10 add the marker for this reason.
- **Empty string.** If $S$ is [nullable](/nullable-symbol/), the machine accepts $\varepsilon$ by expand moves alone. No special case is needed, but a test should include the empty input.

## Implementations

## History

Chomsky in 1962, and Evey and Schützenberger in 1963, proved independently that pushdown-store machines accept exactly the context-free languages. The one-state automaton whose runs are leftmost derivations is the textbook form of the direction from grammars to automata, given by Hopcroft, Motwani and Ullman; Sipser's version adds start and accept states and a bottom marker, and pushes the right side one symbol at a time. The same machine, made deterministic with lookahead, is the LL parser studied by Lewis and Stearns (1968) and by Rosenkrantz and Stearns (1970).

## References
