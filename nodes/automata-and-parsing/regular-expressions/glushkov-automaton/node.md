---
tag: 0FZKDT
kind: algorithm
slug: glushkov-automaton
name: Glushkov automaton
aliases:
- Glushkov construction
- position automaton
area: automata-and-parsing/regular-expressions
level: advanced
summary: Builds an epsilon-free NFA with one state per symbol occurrence plus one initial state.
solves: [regex-to-nfa-conversion]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, k: the number of symbol occurrences in the expression}
  time: {worst: O(m k^2)}
  space: {extra: O(m k)}
properties: {deterministic: true, recursive: false}
history:
  year: 1961
  people: [Victor M. Glushkov, Robert McNaughton, Hisao Yamada]
  note: Glushkov described the automaton whose states are the positions of the expression; McNaughton and Yamada used the same marking of symbol occurrences in 1960.
prereqs: [regular-expression, nondeterministic-finite-automaton]
see_also: [thompson-construction, regex-to-nfa-conversion, antimirov-derivatives, one-unambiguous-regular-expression, bit-parallel-regex-matching, brzozowski-derivatives, nfa-simulation, subset-construction]
sources:
  - paper: doi:10.1070/RM1961v016n05ABEH004112
    title: Victor M. Glushkov, The abstract theory of automata, Russian Mathematical Surveys 16(5) (1961)
    locator: pp. 1 to 53
  - paper: "Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata, IRE Transactions on Electronic Computers EC-9(1) (1960)"
    title: Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata
    locator: pp. 39 to 47 (the marking of each occurrence of a symbol with its own index)
  - paper: doi:10.1016/0304-3975(86)90088-5
    title: Gerard Berry and Ravi Sethi, From regular expressions to deterministic automata, Theoretical Computer Science 48 (1986)
    locator: pp. 117 to 126 (the position automaton described by the derivatives of the marked expression)
  - paper: doi:10.1016/0304-3975(93)90287-4
    title: Anne Brüggemann-Klein, Regular expressions into finite automata, Theoretical Computer Science 120(2) (1993)
    locator: pp. 197 to 213 (star normal form, and the construction of the Glushkov automaton in quadratic time, which is worst case optimal, and in linear time for deterministic expressions)
  - paper: doi:10.1006/inco.1997.2695
    title: Anne Brüggemann-Klein and Derick Wood, One-unambiguous regular languages, Information and Computation 142(2) (1998)
    locator: pp. 182 to 206 (an expression is one-unambiguous if and only if its Glushkov automaton is deterministic)
  - paper: doi:10.1016/S0304-3975(01)00267-5
    title: Jean-Marc Champarnaud and Djelloul Ziadi, Canonical derivatives, partial derivatives and finite automaton constructions, Theoretical Computer Science 289(1) (2002)
    locator: pp. 137 to 163 (the partial derivative automaton is a quotient of the position automaton)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press (2002)
    locator: Chapter 5, Regular expression matching (the Glushkov automaton and its use for bit-parallel search)
---

The Glushkov automaton, or position automaton, of a [regular expression](/regular-expression/) is a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) with no $\varepsilon$-moves and exactly $k + 1$ states, where $k$ is the number of occurrences of symbols in the expression: one initial state, and one state for each occurrence. It is built from three sets computed bottom-up on the syntax tree: the positions that can start a word, the positions that can end a word, and, for each position, the positions that can come next. Every move into a state reads the same symbol, a property used by [bit-parallel matching](/bit-parallel-regex-matching/), and the automaton is deterministic exactly when the expression is [one-unambiguous](/one-unambiguous-regular-expression/).

## In plain words

Give each letter of the pattern its own number, from left to right, so that the two a's of "(a or b), any number of times, then a, then b" become a1 and a3. Now the pattern describes sequences of numbered letters, and a sequence is allowed when it starts with a letter that can start, ends with a letter that can end, and each neighbour pair is allowed to follow each other.

These three facts can be read off the pattern piece by piece. Build an automaton with one state per numbered letter, plus a start state. Move from one numbered letter to the next when the pair is allowed, and read the letter of the target. Forget the numbers, and the automaton accepts exactly the words of the pattern.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

The input is a regular expression $r$ over an alphabet $\Sigma$, with $m$ nodes in its syntax tree and $k$ leaves that are symbols. The output is an NFA without $\varepsilon$-moves that accepts $L(r)$. This is [regex to NFA conversion](/regex-to-nfa-conversion/); the [Thompson construction](/thompson-construction/) solves the same problem with $\varepsilon$-moves and about $2m$ states.

**Positions.** Number the symbol leaves of $r$ from left to right as $1, \ldots, k$, and let $\mathrm{sym}(p)$ be the symbol of leaf $p$. The *marked expression* $\bar r$ is $r$ with leaf $p$ replaced by the letter $p$; it is an expression over the alphabet $\{1, \ldots, k\}$ in which each letter occurs once. For a node $x$ of $r$, the algorithm computes:

- $N(x)$, true if and only if $\varepsilon \in L(x)$;
- $\mathrm{First}(x)$, the positions that can begin a word of $L(\bar x)$;
- $\mathrm{Last}(x)$, the positions that can end a word of $L(\bar x)$;
- $\mathrm{Follow}(p)$, for each position $p$, the positions that can come right after $p$.

## The algorithm

```pseudo id=main
GLUSHKOV(r)                                 ▷ r has k symbol leaves
L1  number the symbol leaves of r from left to right as positions 1, ..., k
L2  for each node x of r in postorder do
L3      if x = ∅ then N(x) ← false; First(x) ← ∅; Last(x) ← ∅
L4      if x = ε then N(x) ← true; First(x) ← ∅; Last(x) ← ∅
L5      if x is position p then N(x) ← false; First(x) ← {p}; Last(x) ← {p}
L6      if x = s | t then N(x) ← N(s) or N(t); First(x) ← First(s) ∪ First(t); Last(x) ← Last(s) ∪ Last(t)
L7      if x = s t then
L8          for each p ∈ Last(s) do Follow(p) ← Follow(p) ∪ First(t)
L9          N(x) ← N(s) and N(t)
L10         First(x) ← First(s) ∪ (First(t) if N(s), else ∅)
L11         Last(x) ← Last(t) ∪ (Last(s) if N(t), else ∅)
L12     if x = s* then
L13         for each p ∈ Last(s) do Follow(p) ← Follow(p) ∪ First(s)
L14         N(x) ← true; First(x) ← First(s); Last(x) ← Last(s)
L15 Follow(0) ← First(r)
L16 δ ← {(p, sym(q), q) : 0 ≤ p ≤ k and q ∈ Follow(p)}
L17 F ← Last(r), and also 0 if N(r)
L18 return the NFA with states {0, ..., k}, initial state 0, moves δ and accepting states F
```

All $\mathrm{Follow}$ sets start empty. Line L8 records that a word of $s$ may end at $p$ and a word of $t$ begin right after it; line L13 records that one iteration of the star may end at $p$ and the next begin. Lines L15 and L16 turn the sets into moves: state 0 goes to each first position, and each position goes to its followers, always reading the symbol of the target.

## Example

Let $r = (a \mid b)^* ab$. The marked expression is $(1 \mid 2)^* 3\, 4$, with $\mathrm{sym}(1) = \mathrm{sym}(3) = a$ and $\mathrm{sym}(2) = \mathrm{sym}(4) = b$. The postorder steps are:

| node | $N$ | First | Last | added to Follow |
|---|---|---|---|---|
| $1$, $2$ | false | $\{1\}$, $\{2\}$ | $\{1\}$, $\{2\}$ | |
| $1 \mid 2$ | false | $\{1, 2\}$ | $\{1, 2\}$ | |
| $(1 \mid 2)^*$ | true | $\{1, 2\}$ | $\{1, 2\}$ | $1, 2 \to \{1, 2\}$ |
| $(1 \mid 2)^* 3$ | false | $\{1, 2, 3\}$ | $\{3\}$ | $1, 2 \to \{3\}$ |
| $(1 \mid 2)^* 3\, 4$ | false | $\{1, 2, 3\}$ | $\{4\}$ | $3 \to \{4\}$ |

So $\mathrm{Follow}(0) = \mathrm{Follow}(1) = \mathrm{Follow}(2) = \{1, 2, 3\}$, $\mathrm{Follow}(3) = \{4\}$, $\mathrm{Follow}(4) = \emptyset$, and $F = \{4\}$. The automaton has 5 states and 10 moves. On $abab$ the sets of current states are $\{0\}$, $\{1, 3\}$, $\{2, 4\}$, $\{1, 3\}$, $\{2, 4\}$, and the last one contains 4, so $abab$ is accepted. A Thompson NFA with two states per node has 16 states, 14 $\varepsilon$-moves and 4 symbol moves for the same expression.

**Determinism.** The automaton above is not deterministic: from state 0, the symbol $a$ leads to 1 and to 3. For $r = (a \mid b)^* a$ the same happens. The equivalent expression $b^* a (b^* a)^*$, marked $1^* 2 (3^* 4)^*$, gives $\mathrm{Follow}(0) = \mathrm{Follow}(1) = \{1, 2\}$ and $\mathrm{Follow}(2) = \mathrm{Follow}(3) = \mathrm{Follow}(4) = \{3, 4\}$, and in each set the two positions carry different symbols, so this Glushkov automaton is a DFA.

**Repeated work.** For $(a^* b^*)^*$, the inner stars already add $1 \to \{1\}$ and $2 \to \{2\}$, the concatenation adds $1 \to \{2\}$, and the outer star adds $1, 2 \to \{1, 2\}$ again. The result is the same automaton as for $(a \mid b)^*$, with 3 states and 6 moves.

## Correctness

Let $h$ map each position $p$ to $\mathrm{sym}(p)$; then $L(r) = h(L(\bar r))$, since marking only renames leaves. The key fact is that $L(\bar r)$ is *local*: a nonempty word $p_1 \cdots p_n$ of positions is in $L(\bar r)$ if and only if $p_1 \in \mathrm{First}(r)$, $p_n \in \mathrm{Last}(r)$ and $p_{i+1} \in \mathrm{Follow}(p_i)$ for each $i$. This is proved by induction on the tree, for the sets as the algorithm computes them. In a union, no follow pair links the two sides, so a word stays on one side. In a concatenation, the only pairs from $s$ to $t$ are those of line L8, so a word is a word of $s$ followed by a word of $t$. Under a star, cut the word wherever a pair comes from line L13; each piece is a word of $s$.

A run of the automaton on $w = a_1 \cdots a_n$ that ends in an accepting state is a sequence $0, p_1, \ldots, p_n$ with $p_1 \in \mathrm{First}(r)$, each $p_{i+1} \in \mathrm{Follow}(p_i)$, $\mathrm{sym}(p_i) = a_i$ and $p_n \in \mathrm{Last}(r)$, or the empty run when $N(r)$ holds and $n = 0$. By the key fact, this is a word of $L(\bar r)$ whose image under $h$ is $w$, so the automaton accepts $L(r)$. The loop visits each of the $m$ nodes once, so the algorithm stops. The full proof is below.

## Complexity

- **States and moves.** There are $k + 1$ states and at most $k^2 + k$ moves, since each state has at most $k$ followers. The bound is reached: $(a_1 \mid \cdots \mid a_k)^*$, with $k$ different leaves, has $k^2 + k$ moves.
- **Time, as written.** The sets First and Last have at most $k$ elements, so lines L3 to L14 cost $O(k)$ per node for them, $O(mk)$ in all. At a concatenation, line L8 adds pairs from the left subtree to the right one, and each pair of positions is added at only one node, their lowest common ancestor, so all concatenations together cost $O(k^2)$. A star costs up to $|\mathrm{Last}(s)| \cdot |\mathrm{First}(s)| \le k^2$ at line L13, and nested stars, as in the example $(a^* b^*)^*$, can add the same pairs again. The total is $O(mk + k^2 + m k^2) = O(m k^2)$.
- **Optimal time.** Brüggemann-Klein (1993) first rewrites the expression in *star normal form*, where no star adds a pair that is already present, and then builds the automaton in time quadratic in the size of the expression, which is worst case optimal since the output can have $k^2 + k$ moves. For deterministic expressions her method takes linear time.
- **Space.** The Follow sets take $O(k^2)$, and the stack of pending First and Last sets takes $O(mk)$, so $O(mk)$ in all.
- **Matching.** Running the automaton on a text of length $n$ with a set of current states costs $O(n k^2)$ time in the worst case, or $O(n \lceil k / w \rceil)$ word operations with bit-parallelism on words of $w$ bits, after a table of size $2^k$ or a split table.

## Properties

- **No $\varepsilon$-moves.** A simulation needs no $\varepsilon$-closure, and the [subset construction](/subset-construction/) works directly on sets of positions.
- **Homogeneous.** All moves into a state $q \ge 1$ read $\mathrm{sym}(q)$. So the set of states after reading $c$ is $\{q \in \mathrm{Follow}(S) : \mathrm{sym}(q) = c\}$, the follow set of the old set intersected with a fixed set for $c$. This is the basis of bit-parallel matching.
- **No moves into the initial state.** State 0 has no incoming move, so the automaton is easy to combine with others.
- **Size.** It has $k + 1$ states, against about $2m$ for Thompson's construction, but up to $k^2 + k$ moves, against $O(m)$ for Thompson.
- **Determinism.** The automaton is deterministic if and only if no two positions in First, and no two positions in one Follow set, carry the same symbol. Brüggemann-Klein and Wood (1998) call such an expression one-unambiguous, and the property is required for the content models of SGML and XML.
- **Quotients.** The [Antimirov](/antimirov-derivatives/) partial derivative automaton, which has at most $k + 1$ states, is a quotient of the Glushkov automaton (Champarnaud and Ziadi, 2002).

## Variants and improvements

- **Star normal form.** Rewrite the expression so that no star body can already loop, for example $(a^* b^*)^*$ into $(a \mid b)^*$, and then each pair is added once.
- **McNaughton and Yamada.** Build a DFA directly whose states are sets of positions, by running the subset construction on the Glushkov automaton without building it first. Berry and Sethi (1986) explain this DFA with the derivatives of the marked expression.
- **Follow automaton.** Merge the states that have the same Follow set and the same acceptance; the result is smaller and still has no $\varepsilon$-moves.
- **Bit-parallel simulation.** Store a set of positions as a bit vector; with the homogeneity property, one step is a table lookup for the union of the Follow sets and one AND with the mask of the symbol. See [bit-parallel regex matching](/bit-parallel-regex-matching/).
- **Extended operators.** Counted repetition $x\{i, j\}$ must be unfolded into copies of $x$, which multiplies the number of positions; see [bounded repetition](/bounded-repetition/).

## When to use it

Use the Glushkov automaton when an NFA without $\varepsilon$-moves is needed, for a simulation without closures, for bit-parallel matching, for a subset construction on sets of positions, or to test whether an expression is deterministic. When the expression has many symbols under one star, the $k^2$ moves can cost more than the $O(m)$ moves of the Thompson construction, and a [Pike VM](/pike-vm/) or a Thompson simulation may use less memory.

## Pitfalls

- **Nullable parts.** Lines L10 and L11 must test $N(s)$ and $N(t)$: in $a^* b$, the first positions are those of $a^*$ and of $b$. Forgetting this loses words.
- **The empty language.** A subexpression $\emptyset$ has no positions but blocks its concatenations: in $(ab)\emptyset$, $\mathrm{Last}$ is empty, so no word is accepted, although the move from $a$ to $b$ is present. The move is harmless, but it means that Follow can contain pairs that occur in no word.
- **Repeated pairs.** Without star normal form, nested stars add the same pairs again and again; use sets, not lists, for Follow, or the output contains duplicate moves.
- **Recursion depth.** The usual recursive definitions of First, Last and Follow overflow the call stack on deep expressions; walk the tree with an explicit stack.

## Implementations

## History

McNaughton and Yamada (1960) marked each occurrence of a symbol in an expression with its own index, and used the marked expression to build a deterministic automaton. Glushkov (1961) described the nondeterministic automaton whose states are the positions, which is why the construction carries his name. Berry and Sethi (1986) showed that it can be described by the derivatives of the marked expression. Brüggemann-Klein (1993) gave the quadratic-time construction through star normal form, and with Wood (1998) characterized the expressions whose Glushkov automaton is deterministic.

## References
