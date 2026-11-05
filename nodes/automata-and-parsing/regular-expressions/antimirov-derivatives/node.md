---
tag: B0378X
kind: algorithm
slug: antimirov-derivatives
name: Antimirov partial derivatives
aliases:
- partial derivatives
- Antimirov construction
area: automata-and-parsing/regular-expressions
level: research
summary: Builds an NFA with at most k+1 states for a regex with k symbol occurrences, whose states are partial derivatives.
solves: [regex-to-nfa-conversion, regex-matching]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, k: the number of symbol occurrences in it, s: the number of distinct symbols in it, n: the length of the input string}
  time: {expected: O(s m k^2 + n k^2)}
  space: {extra: O(s m k^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1996
  people: [Valentin Antimirov]
  note: Antimirov split the Brzozowski derivative into a set of partial derivatives and showed that an expression with k symbol occurrences has at most k + 1 of them, which gives a small NFA.
prereqs: [regex-derivative, nondeterministic-finite-automaton]
see_also: [brzozowski-derivatives, brzozowski-finiteness-theorem, glushkov-automaton, thompson-construction, subset-construction, nfa-simulation, hash-consing, regex-equivalence]
sources:
  - paper: doi:10.1016/0304-3975(95)00182-4
    title: Valentin Antimirov, Partial derivatives of regular expressions and finite automaton constructions, Theoretical Computer Science 155(2) (1996)
    locator: pp. 291 to 319
  - paper: doi:10.1016/S0304-3975(01)00267-5
    title: Jean-Marc Champarnaud and Djelloul Ziadi, Canonical derivatives, partial derivatives and finite automaton constructions, Theoretical Computer Science 289(1) (2002)
    locator: pp. 137 to 163 (the partial derivative automaton is a quotient of the position automaton)
  - paper: doi:10.1142/S0218196701000772
    title: Jean-Marc Champarnaud and Djelloul Ziadi, From c-continuations to new quadratic algorithms for automaton synthesis, International Journal of Algebra and Computation 11(6) (2001)
    locator: pp. 707 to 735 (a quadratic time construction of the partial derivative automaton)
  - paper: doi:10.1007/978-3-031-07469-1_2
    title: Nelma Moreira and Rogerio Reis, Manipulation of regular expressions using derivatives, an overview, CIAA 2022, Lecture Notes in Computer Science 13276
    locator: pp. 19 to 33 (Section 3, partial derivatives, Mirkin's prebases and the bound of k + 1 states; Section 4.1, the cost of the known constructions)
  - paper: doi:10.1145/321239.321249
    title: Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)
    locator: pp. 481 to 494
---

Antimirov's partial derivatives turn a [regular expression](/regular-expression/) into a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) whose states are expressions. Where the [Brzozowski derivative](/brzozowski-derivatives/) by a symbol $a$ is one expression for the words that may follow $a$, the partial derivative is a set of expressions whose languages have that union. Antimirov (1996) showed that an expression with $k$ symbol occurrences has at most $k + 1$ partial derivatives by all words, with no need for the rules of union that the Brzozowski method requires. So the automaton is never larger than the [Glushkov automaton](/glushkov-automaton/), and it is often smaller.

## In plain words

A pattern describes what may still come. After reading one letter, the rest of the input must fit one of several smaller descriptions. The Brzozowski method keeps the choice between them as one big description. This method keeps them apart, as a list of separate descriptions.

Each separate description becomes a state of a machine. Reading a letter in a state leads to every description that the letter produces from it. A state accepts when its description allows the input to stop.

The descriptions that can ever appear are few: at most one more than the number of letters written in the pattern. They are also built only from pieces of the original pattern, so the machine can be built by trying each letter in each state until no new description appears.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

The input is a regular expression $r$ with $m$ nodes and $k$ symbol occurrences, over an alphabet $\Sigma$. The output is an NFA without $\varepsilon$-moves that accepts $L(r)$, with at most $k + 1$ states. Running it on a string $w$ solves [regex matching](/regex-matching/).

**Definitions.** The test $\nu(x)$ is true exactly when $\varepsilon \in L(x)$: false for $\emptyset$ and for a symbol, true for $\varepsilon$ and for a star, $\nu(s) \lor \nu(t)$ for $s \mid t$ and $\nu(s) \land \nu(t)$ for $st$. For a set $S$ of expressions and an expression $t$, let
$$S \odot t = \begin{cases} \emptyset & t = \emptyset, \\ S & t = \varepsilon, \\ \{\, t : \varepsilon \in S \,\} \cup \{\, z t : z \in S,\ z \ne \varepsilon \,\} & \text{otherwise.} \end{cases}$$
The *partial derivative* $\partial_a x$ of an expression $x$ by a symbol $a$ is the set of expressions given by lines L9 to L13 below. For words, $\partial_\varepsilon x = \{x\}$ and $\partial_{ua} x = \bigcup_{y \in \partial_u x} \partial_a y$. The *partial derivative automaton* has the states $\bigcup_u \partial_u r$, the start state $r$, the moves $x \xrightarrow{a} y$ for $y \in \partial_a x$, and the accepting states $x$ with $\nu(x)$.

## The algorithm

```pseudo id=main
PD-AUTOMATON(r)
L1  Q ← {r}; T ← ∅; todo ← [r]
L2  while todo is not empty do
L3      x ← pop(todo)
L4      for each symbol a that occurs in r do
L5          for each y in PARTIAL(x, a) do
L6              add the move (x, a, y) to T
L7              if y ∉ Q then add y to Q and push y on todo
L8  return (Q, T, start r, final {x ∈ Q : NULLABLE(x)})

PARTIAL(x, a)                      ▷ memoized on the pair (x, a); terms are hash-consed
L9  if x = ∅ or x = ε then return ∅
L10 if x is a symbol b then return {ε} if b = a, else ∅
L11 if x = s | t then return PARTIAL(s, a) ∪ PARTIAL(t, a)
L12 if x = s t then return PARTIAL(s, a) ⊙ t, joined with PARTIAL(t, a) if NULLABLE(s)
L13 if x = s* then return PARTIAL(s, a) ⊙ s*
L14 S ⊙ t: ∅ if t = ∅; S if t = ε; otherwise t for each ε in S and the node z t for each other z in S

PD-MATCH(r, w)                     ▷ w = a1 ... an
L15 build (Q, T, r, F) with PD-AUTOMATON(r)
L16 S ← {r}
L17 for i ← 1 to n do S ← {y : (x, ai, y) ∈ T for some x ∈ S}; if S = ∅ then return false
L18 return S ∩ F ≠ ∅
```

Terms are compared by structure. The implementation hash-conses them, so that each distinct term is one shared node and equality is a comparison of integers; the node $z t$ made at line L14 is one new node whose children are already stored. `PARTIAL` uses an explicit stack in place of recursion.

## Example

Let $r = (a \mid b)^* a b$, parsed as $((a \mid b)^* a)\, b$, with $k = 4$. Write $X = (a \mid b)^*$, so $\partial_a X = \partial_a(a \mid b) \odot X = \{\varepsilon\} \odot X = \{X\}$, and in the same way $\partial_b X = \{X\}$.

- $\partial_a(Xa) = \partial_a X \odot a \cup \partial_a a = \{Xa\} \cup \{\varepsilon\}$, since $\nu(X)$ holds. Then $\partial_a r = \{Xa, \varepsilon\} \odot b = \{r, b\}$, because $\varepsilon \odot b$ gives $b$ and $Xa$ followed by $b$ is $r$ itself.
- $\partial_b(Xa) = \{Xa\}$, so $\partial_b r = \{r\}$.
- $\partial_a b = \emptyset$ and $\partial_b b = \{\varepsilon\}$; $\varepsilon$ has no partial derivatives.

The automaton has the three states $r$, $b$ and $\varepsilon$, of which only $\varepsilon$ accepts, and four moves:

| state | on $a$ | on $b$ |
|---|---|---|
| $(a \mid b)^* a b$ (start) | $(a \mid b)^* a b$, $b$ | $(a \mid b)^* a b$ |
| $b$ | | $\varepsilon$ |
| $\varepsilon$ (accepting) | | |

The Glushkov automaton of the same expression has $k + 1 = 5$ states. On $w = aab$, the set of states is $\{r\}$, then $\{r, b\}$ after $a$, $\{r, b\}$ after the second $a$, and $\{r, \varepsilon\}$ after $b$, which contains the accepting state, so $aab \in L(r)$. The words of length at most 4 that the automaton accepts are $ab$, $aab$, $bab$, $aaab$, $abab$, $baab$ and $bbab$.

## Correctness

Two facts carry the proof. First, $\bigcup_{y \in \partial_a x} L(y) = a^{-1}L(x) = \{v : av \in L(x)\}$, by induction on $x$, with the same case analysis as for the Brzozowski derivative and the identity $L(S \odot t) = \big(\bigcup_{z \in S} L(z)\big) L(t)$. By induction on $u$, the union of the languages of $\partial_u r$ is $u^{-1} L(r)$, so the set $S$ after line L17 has this property for the prefix read so far, and line L18 tests whether $\varepsilon$ is in it.

Second, the states are few. Define $\pi(\emptyset) = \pi(\varepsilon) = \emptyset$, $\pi(a) = \{\varepsilon\}$, $\pi(s \mid t) = \pi(s) \cup \pi(t)$, $\pi(st) = \pi(s) \odot t \cup \pi(t)$ and $\pi(s^*) = \pi(s) \odot s^*$. By induction, $|\pi(x)|$ is at most the number of symbol occurrences in $x$, and both $\partial_a x$ and $\partial_a y$ for every $y \in \pi(x)$ are subsets of $\pi(x)$. So every state is $r$ or a member of $\pi(r)$, there are at most $k + 1$ of them, and the loop at lines L2 to L7 stops. The full proof is below.

## Complexity

Every term that `PARTIAL` meets is a subterm of $r$ or a member of $\pi(u)$ for a subterm $u$, because the children of a node $z t$ made at line L14 are again of these kinds. So at most $m + mk$ terms occur. For each of them and each of the $s$ symbols, the memoized call does a constant number of steps plus a union and a $\odot$ on sets of at most $k$ terms, which is $O(k)$ expected time with hashing. Building the automaton therefore costs $O(s m k^2)$ expected time, and the memo table holds the same amount of space. The automaton has at most $k + 1$ states and at most $s (k + 1) k$ moves. Each step of line L17 joins at most $k + 1$ sets of at most $k + 1$ states, so matching a string of length $n$ costs $O(n k^2)$.

The bound is coarse. Moreira and Reis report that Antimirov's own construction takes $O(k^3 m^2)$ time in the worst case, and that Champarnaud and Ziadi build the automaton in time quadratic in $m$.

## Properties

- **Size.** At most $k + 1$ states, against $k + 1$ for the Glushkov automaton and up to $2m$ for the [Thompson construction](/thompson-construction/). The expression $(a \mid \varepsilon)(a \mid \varepsilon) a$ has $k = 3$ and $4$ states, so the bound is reached.
- **Transitions.** There can be quadratically many moves: for $a_1^* a_2^* \cdots a_n^*$ the states are $a_i^* \cdots a_n^*$ for $1 \le i \le n$, and state $i$ has a move on each $a_j$ with $j \ge i$, for $n(n+1)/2$ moves.
- **No $\varepsilon$-moves.** The automaton reads one symbol per move, so it can be determinized directly by the [subset construction](/subset-construction/), and the subsets reached are the sets $\partial_u r$. Each is $\{r\}$ or a subset of $\pi(r)$, so there are at most $2^k + 1$ of them.
- **Syntactic states.** Each state is an expression built from subterms of $r$ with concatenation, so it can be printed, compared, and simplified further.
- **Large terms.** A single partial derivative can be large when it is written out, since it is a concatenation of up to about $m$ subterms. Hash-consing shares the subterms, so each new term costs one node.

## Variants and improvements

- **Brzozowski derivatives.** Taking the union of the set $\partial_a x$ as one expression gives the [Brzozowski derivative](/brzozowski-derivatives/), which needs similarity rules for union to have finitely many values ([finiteness theorem](/brzozowski-finiteness-theorem/)) and gives a DFA directly.
- **Mirkin's prebases.** Mirkin (1966) gave an equivalent construction through systems of equations; Champarnaud and Ziadi (2001) proved that the two give the same automaton.
- **Quotient of the position automaton.** Champarnaud and Ziadi (2002) showed that the partial derivative automaton is a quotient of the Glushkov automaton, which leads to a quadratic time construction through the position automaton.
- **Linear forms.** Antimirov computes all partial derivatives of a term at once as a set of pairs $(a, y)$, which avoids one pass per symbol.
- **Equivalence and inclusion.** Sets of partial derivatives can be compared pairwise to decide [equivalence](/regex-equivalence/) of expressions without building a DFA first.

## When to use it

- When an NFA with few states and no $\varepsilon$-moves is wanted, and its states should be readable expressions, for example for teaching or for proof assistants.
- As the first stage of a lazy or full DFA, where the partial derivative sets serve as DFA states.
- For extensions of regular expressions, such as shuffle, for which partial derivatives have been defined as well.
- Not when only the speed of matching matters: the Glushkov automaton has exactly $k + 1$ states, never fewer than the automaton here, but it is built in quadratic time without hash-consing.

## Pitfalls

- **Sets, not lists.** $\partial_a x$ must be a set. With lists, duplicates are kept: $\partial_a(a \mid a)$ has two copies of $\varepsilon$, and simulating $(a \mid a)^*$ on $a^n$ with lists gives $2^n$ copies of the start term.
- **The nullable side of a concatenation.** Line L12 must add $\partial_a t$ when $\nu(s)$ holds, for example in $a^* b$, whose partial derivative by $b$ is $\{\varepsilon\}$.
- **Structural equality.** States are compared as terms. Without hash-consing, comparing and hashing large terms costs time proportional to their size at every step.
- **Recursion depth.** The rules are recursive, and a recursive implementation overflows the stack on a long concatenation or a deep nest of stars. Use an explicit stack.
- **Empty states.** A term such as $z \emptyset$ never arises after line L14, but a subterm of $r$ with empty language can still be a state with no moves. It does no harm.

## Implementations

## History

Brzozowski (1964) defined derivatives of regular expressions. Moreira and Reis note that Mirkin (1966) gave an NFA construction based on prebases, and that Antimirov (1996), almost thirty years later and independently, introduced partial derivatives and the partial derivative automaton, with at most $k + 1$ states. Champarnaud and Ziadi proved that Mirkin's and Antimirov's constructions give the same automaton (2001), gave a quadratic time construction (2001), and showed that the automaton is a quotient of the position automaton (2002).

## References
