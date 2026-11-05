---
tag: GVY1JV
kind: algorithm
slug: state-elimination
name: State elimination
aliases:
- Brzozowski-McCluskey algorithm
- GNFA state elimination
- Kleene construction
area: automata-and-parsing/regular-expressions
level: core
summary: Converts an automaton to a regular expression by removing states and merging edge labels.
solves: [dfa-to-regex-conversion]
model: word-ram
complexity:
  vars: {n: the number of states of the automaton, t: the number of its moves}
  time: {worst: O(n^3 + t)}
  space: {extra: O(n^3 + t)}
properties: {deterministic: true, recursive: false}
history:
  year: 1963
  people: [Janusz Brzozowski, Edward J. McCluskey]
  note: Brzozowski and McCluskey adapted the reduction of signal flow graphs to state diagrams, removing one node at a time and labelling the new edges with regular expressions.
prereqs: [nondeterministic-finite-automaton, regular-expression]
see_also: [dfa-to-regex-conversion, kleene-theorem, arden-lemma, thompson-construction, floyd-warshall, gaussian-elimination, state-complexity, regex-minimization]
sources:
  - paper: "Janusz A. Brzozowski and Edward J. McCluskey, Signal flow graph techniques for sequential circuit state diagrams, IEEE Transactions on Electronic Computers EC-12(2) (1963)"
    locator: pp. 67 to 76 (the removal of nodes from a state diagram with expressions on its edges)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.3, Lemma 1.60 (generalized nondeterministic finite automata, the procedure CONVERT and its proof)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.2.2, Converting DFA's to Regular Expressions by Eliminating States
  - paper: "Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata, IRE Transactions on Electronic Computers EC-9(1) (1960)"
    locator: pp. 39 to 47
  - paper: "Andrzej Ehrenfeucht and Paul Zeiger, Complexity measures for regular expressions, Journal of Computer and System Sciences 12(2) (1976)"
    locator: pp. 134 to 146 (complete automata with n states whose shortest expressions have length 2^(n-1))
  - paper: doi:10.1007/978-3-540-70583-3_4
    title: Hermann Gruber and Markus Holzer, Finite automata, digraph connectivity, and regular expression size, ICALP 2008, Lecture Notes in Computer Science 5126
    locator: pp. 39 to 50 (lower bounds of 2^Ω(n) over a binary alphabet)
  - paper: "Manuel Delgado and José Morais, Approximation to the smallest regular expression for a given regular language, CIAA 2004, Lecture Notes in Computer Science 3317"
    locator: pp. 312 to 314 (the greedy choice of the state of least weight)
---

State elimination turns a finite automaton into a [regular expression](/regular-expression/) for the same language. It allows regular expressions as labels on the moves, adds a new start and a new accepting state, and removes the old states one at a time; each path through a removed state is replaced by one move whose label is an expression for that path. When only the new start and accepting states remain, the label between them is the answer. It is the usual proof of the harder direction of [Kleene's theorem](/kleene-theorem/) and the standard method for [DFA to regex conversion](/dfa-to-regex-conversion/). With labels stored as shared pointers it takes $O(n^3 + t)$ time for $n$ states and $t$ moves, but the expression, written out, can have size exponential in $n$, and for some automata no method can do better.

## In plain words

Draw the automaton as points and arrows, and write on every arrow what it reads. Now pick a point and take it out. For every arrow that came into it and every arrow that went out of it, draw a new arrow that skips the point, and write on it: the first label, then the loop at the removed point any number of times, then the second label. If there was already an arrow between the same two points, join the two labels with "or".

The automaton accepts the same words after each removal, because every way of passing through the removed point is now one arrow. Keep removing points until only a fresh start and a fresh end are left. The label of the one arrow between them is the regular expression.

## The problem

The input is a nondeterministic finite automaton $N = (Q, \Sigma, \delta, q_0, F)$ with $n$ states and $t$ moves, where a move reads a symbol or is an $\varepsilon$-move. A DFA is a special case. The output is a regular expression $r$, in the syntax of the [regular expression](/regular-expression/) page (union $\mid$, concatenation, star $^*$, $\varepsilon$, $\emptyset$), with $L(r) = L(N)$.

## The algorithm

A *generalized* automaton has a regular expression $R[p][q]$ on each ordered pair of states, with $\emptyset$ meaning "no move". A path that reads $w$ is a sequence of moves whose labels match consecutive pieces of $w$. The algorithm keeps $R$ as one table of nonempty labels, stored as lists of incoming and outgoing labels per state.

```pseudo id=main
STATE-ELIMINATION(N)                      ▷ N = (Q, Σ, δ, q0, F); labels not stored are ∅
L1  add new states s, f; R[s][q0] ← ε; R[q][f] ← ε for each q in F
L2  for each move p --a--> q of N do R[p][q] ← R[p][q] | a      ▷ a ∈ Σ, or a = ε
L3  for each state k of Q, in the chosen order do
L4      L ← (R[k][k])*                     ▷ ε if k has no loop
L5      for each p ≠ k with R[p][k] ≠ ∅ do
L6          for each q ≠ k with R[k][q] ≠ ∅ do
L7              R[p][q] ← R[p][q] | R[p][k] · L · R[k][q]
L8      delete k and all labels into and out of k
L9  return R[s][f]
```

The new start $s$ has no incoming move and the new accepting state $f$ has no outgoing move, so neither is ever a loop state, and at the end only the label $R[s][f]$ can remain. The operations $\mid$, $\cdot$ and $^*$ in lines L2, L4 and L7 build expressions with the simplifications $\emptyset \mid r = r$, $r \mid r = r$ for the same stored $r$, $\emptyset \cdot r = r \cdot \emptyset = \emptyset$, $\varepsilon \cdot r = r \cdot \varepsilon = r$, $\emptyset^* = \varepsilon^* = \varepsilon$ and $(r^*)^* = r^*$, which keep the output free of useless constants and do not change any language. Each new label at line L7 points to the old labels instead of copying them, so the update costs $O(1)$.

The order of line L3 is free. The result is correct for every order, but its size depends on the order, often a lot.

## Example

Take the DFA over $\{0, 1\}$ that reads a binary number from the most significant digit and accepts when it is divisible by 3. Its states are the remainders 0, 1, 2, the start state and the only accepting state is 0, and the move from $r$ on the digit $b$ goes to $2r + b \bmod 3$:

| state | on 0 | on 1 |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 2 | 0 |
| 2 | 1 | 2 |

Lines L1 and L2 add $s \xrightarrow{\varepsilon} 0$ and $0 \xrightarrow{\varepsilon} f$. Remove the states in the order 2, 1, 0:

- **Remove 2.** Its loop is $1$, so $L = 1^*$. The only move into 2 is $1 \xrightarrow{0} 2$ and the only move out is $2 \xrightarrow{0} 1$, so state 1 gets the loop $R[1][1] = 01^*0$.
- **Remove 1.** Now $L = (01^*0)^*$, the move in is $0 \xrightarrow{1} 1$ and the move out is $1 \xrightarrow{1} 0$. The loop of 0 becomes $R[0][0] = 0 \mid 1(01^*0)^*1$.
- **Remove 0.** $L = (0 \mid 1(01^*0)^*1)^*$, the move in is $s \xrightarrow{\varepsilon} 0$ and the move out is $0 \xrightarrow{\varepsilon} f$, so $R[s][f] = \varepsilon \cdot L \cdot \varepsilon = L$.

The answer is $(0 \mid 1(01^*0)^*1)^*$, of size 14. It accepts the empty string, which this DFA also accepts. Other orders give other expressions for the same language:

| order | result | size |
|---|---|---|
| 2, 1, 0 | $(0 \mid 1(01^*0)^*1)^*$ | 14 |
| 1, 2, 0 | $(0 \mid 11 \mid 10(1 \mid 00)^*01)^*$ | 21 |
| 0, 1, 2 | $0^* \mid 0^*1(10^*1)^*10^* \mid 0^*1(10^*1)^*0(1 \mid 0(10^*1)^*0)^*0(10^*1)^*10^*$ | 65 |

Removing the start and accepting state of the DFA last, as in the first two rows, avoids copying the part before the first visit and after the last visit to 0.

## Correctness

Call the states removed so far *eliminated*. The invariant is: for each pair $p, q$ of remaining states, $L(R[p][q])$ is the set of words read by the paths of $N$ (with the moves of line L1) that go from $p$ to $q$, use at least one move, and pass only through eliminated states in between. After line L2 no state is eliminated, and $R[p][q]$ is the union of the labels of the direct moves, so the invariant holds. When $k$ is removed, a path from $p$ to $q$ whose inner states are eliminated or equal to $k$ either avoids $k$, and is counted in the old $R[p][q]$, or splits at its visits to $k$ into a first part from $p$ to $k$, zero or more loops from $k$ to $k$, and a last part from $k$ to $q$, each with only old eliminated states inside. These are counted by $R[p][k]$, $(R[k][k])^*$ and $R[k][q]$, so line L7 restores the invariant. At the end all states of $Q$ are eliminated, and $R[s][f]$ denotes the words of all paths from $s$ to $f$, which are the words accepted by $N$. The details are in the proof below.

## Complexity

- **Setup.** Lines L1 and L2 cost $O(n + t)$.
- **One removal.** Removing $k$ costs $O(\mathrm{in}(k) \cdot \mathrm{out}(k))$, where $\mathrm{in}(k)$ and $\mathrm{out}(k)$ count the remaining states with a label into and out of $k$. Both are at most $n + 1$.
- **Total.** The $n$ removals cost $O(n^3)$, so the time is $O(n^3 + t)$ on the [word RAM](/word-ram/) when labels are shared. Each update creates $O(1)$ new nodes, so the expression is stored as a directed acyclic graph with $O(n^3 + t)$ nodes, which is also the space.
- **Output size.** Written out as a tree, the expression can be much larger. Each removal can replace a label by an expression that contains up to four labels of the previous stage, so the size can grow by a factor of about 4 per state. On the complete automaton with a distinct symbol on each of its $n^2$ moves, removal in the order $0, 1, \ldots, n-1$ gives:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| size | 2 | 22 | 118 | 534 | 2262 | 9302 | 37718 | 151894 | 609622 |

- **Lower bound.** No order and no other method avoids exponential output in general. Ehrenfeucht and Zeiger (1976) showed that some automata with $n$ states over an alphabet of size $n^2$ need expressions of length $2^{n-1}$, and Gruber and Holzer (2008) gave lower bounds of $2^{\Omega(n)}$ for DFAs over two letters. See [state complexity](/state-complexity/).

## Properties

- **Works for any automaton.** DFAs, NFAs and NFAs with $\varepsilon$-moves are handled alike, since $\varepsilon$ is a valid label.
- **Order-sensitive.** The language never depends on the order, but the size of the expression does.
- **Unreachable states are harmless.** A state that cannot be reached from $s$ or cannot reach $f$ only adds labels that never connect $s$ to $f$; removing such states first is a cheap way to shrink the output.
- **Same sets as McNaughton and Yamada.** If the states are removed in the order $1, \ldots, n$, the label $R[p][q]$ after $k$ removals denotes the set $R^{(k)}_{pq}$ of the McNaughton-Yamada construction, the paths from $p$ to $q$ through states numbered at most $k$. State elimination computes only the sets that are still needed.
- **An instance of a general pattern.** The update of line L7 is the step of [Gaussian elimination](/gaussian-elimination/) and of the [Floyd-Warshall algorithm](/floyd-warshall/), over the algebra of regular languages, with $\mid$ for addition, concatenation for multiplication and star for the inverse of $1 - x$. Solving the equations of the automaton with [Arden's lemma](/arden-lemma/) is the same computation.

## Variants and improvements

- **Order heuristics.** Remove first the state whose removal adds the least total label size. Delgado and Morais (2004) proposed such a weight, and experiments by Gruber, Holzer and Tautschnig (2009) found this greedy rule to be among the best practical choices. Removing states of low in-degree times out-degree first is a simpler variant.
- **Simplification.** Apply more algebraic laws during the construction, such as $r \mid r = r$, $\varepsilon \mid r r^* = r^*$ and $r^* r^* = r^*$. This shrinks the output but needs equality tests on expressions, which can be costly.
- **Structural decomposition.** Split the automaton at bridges or at states that every accepting path visits, convert the parts separately and concatenate the results. Han and Wood (2005) used this idea to get shorter expressions.
- **The reverse direction.** [Thompson's construction](/thompson-construction/) turns an expression back into an automaton of linear size, so the two directions are very unequal: automaton to expression can blow up, expression to automaton cannot.

## When to use it

Use it when an automaton must be shown to a person or handed to a tool that only accepts regular expressions, and the automaton is small or has little cyclic structure. For learning and proofs, it is the clearest constructive proof that every finite automaton has a regular expression. Do not use it as a step inside a pipeline that ends in an automaton again: the output can be exponentially large, and most questions about automata, such as emptiness, equivalence and inclusion, are answered directly on them.

## Pitfalls

- **Skipping the new start and accepting states.** If the start state has incoming moves or there are several accepting states, removing all other states leaves a small automaton whose language is not one label. Line L1 adds $s$ and $f$ to avoid this; the cost is two states.
- **Forgetting the old label.** Line L7 must join the new path label with the existing $R[p][q]$. Overwriting it loses the direct moves.
- **Forgetting $p = q$.** When $p$ and $q$ are the same state, the update creates or extends a loop on $p$, which later removals must use.
- **Copying labels.** Building each new label as a copied string makes every step cost the size of the labels, and the running time follows the exponential output size. Sharing the subexpressions keeps the work at $O(n^3 + t)$ until the result is printed.
- **Deep recursion when printing.** The output can be a very deep tree; a long chain of states gives depth proportional to $n$. Print and measure it with an explicit stack.

## Implementations

## History

McNaughton and Yamada (1960) gave the first algorithm from state graphs to regular expressions, the dynamic program over the sets $R^{(k)}_{pq}$, in the same paper as their construction in the other direction; Kleene's 1956 proof was of the same kind. Brzozowski and McCluskey (1963) took the reduction of signal flow graphs from electrical engineering, in which nodes are removed one at a time and the gains of the bypassing paths are combined, and applied it to state diagrams with regular expressions on the edges. This is the form in which textbooks such as Sipser's present the conversion, through generalized nondeterministic finite automata. The question of good removal orders became a research topic around 2004, with work by Delgado and Morais, Han and Wood, and Gruber and Holzer.

## References
