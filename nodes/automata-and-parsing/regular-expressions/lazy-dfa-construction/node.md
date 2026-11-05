---
tag: 1VRZ3Y
kind: algorithm
slug: lazy-dfa-construction
name: Lazy DFA construction
aliases:
- on-the-fly DFA
- lazy DFA matching
area: automata-and-parsing/regular-expressions
level: advanced
summary: Builds DFA states during matching and caches them, avoiding the full exponential DFA.
solves: [regex-matching]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, n: the length of the text, k: the cache capacity in DFA states, s: the number of distinct symbols in the text}
  time: {worst: O(m n)}
  space: {extra: O(k (m + s))}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [Alfred V. Aho]
  note: The Unix egrep of Aho used a precomputed DFA in the Seventh Edition (1979), and computed the DFA on the fly by the Eighth Edition (1985).
prereqs: [subset-construction, nfa-simulation]
see_also: [thompson-construction, glushkov-automaton, brzozowski-derivatives, regex-dfa-state-blowup, pike-vm, grep, cache-replacement-policy, memoization]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast (2007)
    locator: section Caching the NFA to build a DFA (the DFA states as a cache of the step function, a cache that is thrown away when it grows too large, and awk's limit of 32 cached states) and section History and References (egrep in the Seventh and Eighth Editions)
  - url: "https://swtch.com/~rsc/regexp/regexp3.html"
    title: Russ Cox, Regular Expression Matching in the Wild (2010)
    locator: section Step 4, Match (the RE2 DFA treats its states as a cache and frees them all when the cache fills) and section Caveats (RE2 falls back on an NFA search if it must discard the DFA too often)
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422 (the simulation of all automaton states at once, which the lazy DFA caches)
---

A lazy DFA matches a string against a [regular expression](/regular-expression/) by running the [subset construction](/subset-construction/) of an NFA only on the states that the input actually reaches. Each DFA state, a set of NFA states, is computed the first time it is needed and then kept in a cache together with the moves found so far, so later visits cost one table lookup per symbol. Because the text of length $n$ reaches at most $n + 1$ states, the exponential size of the full DFA never has to be paid, and a bound on the cache, with a flush when it is full, keeps the memory fixed.

## In plain words

An NFA can be in many states at once, and a program that tracks all of them pays for the whole set at every letter. A DFA is fast, one lookup per letter, but it can have an enormous number of states.

The lazy DFA is a middle way. It tracks the set of NFA states, as the slow method does, but it remembers each set it has seen and, for each letter, the set that came next. When the same set and letter come again, it looks the answer up instead of computing it.

Real text tends to revisit the same few sets, so most steps become lookups. If the memory fills up, the program throws all remembered sets away and starts remembering again from where it is.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

The input is an NFA $N$ with states $Q$, $\varepsilon$-moves, start state $q_0$ and accepting states $F$, usually built from an expression with $m$ nodes by the [Thompson construction](/thompson-construction/) or as the [Glushkov automaton](/glushkov-automaton/), a text $w = a_1 \cdots a_n$, and a capacity $k \ge 1$. The output is whether $N$ accepts $w$. This is [regex matching](/regex-matching/) once the NFA is built.

For a set $S \subseteq Q$, $\mathrm{MOVE}(S, c)$ is the set of states reached from $S$ by one move on $c$, and $\mathrm{CLOSURE}(S)$ is the set reachable from $S$ by $\varepsilon$-moves, including $S$. The subset DFA has the states $\mathrm{CLOSURE}(\mathrm{MOVE}(\cdots))$ reachable from $\mathrm{CLOSURE}(\{q_0\})$, and can have $2^{|Q|}$ of them.

## The algorithm

```pseudo id=main
LAZY-DFA-MATCH(N, w, k)             ▷ N has start q0 and accepting set F; k ≥ 1 is the cache capacity
L1  states ← an empty map from sets of NFA states to DFA states
L2  S ← STATE(CLOSURE({q0}))
L3  for each symbol c of w, from left to right do
L4      T ← S.next[c]
L5      if T is undefined then
L6          U ← CLOSURE(MOVE(S.set, c))
L7          if U is not a key of states and |states| ≥ k then clear states        ▷ flush the cache
L8          T ← STATE(U)
L9          S.next[c] ← T
L10     S ← T
L11 return S.accepting

STATE(U)
L12 if U is not a key of states then states[U] ← a new DFA state with set U, accepting ← (U ∩ F ≠ ∅) and an empty table next
L13 return states[U]
```

A DFA state stores its set of NFA states, whether the set contains an accepting state, and a partial table `next` from symbols to DFA states. Line L4 is the fast path: a cached move. Lines L6 to L9 are the slow path: one step of [NFA simulation](/nfa-simulation/), after which the result is stored. Line L7 makes room for a new state; the current state $S$ may be thrown away with the rest, which is harmless, because the loop moves on to $T$ at line L10. The map `states` makes sure that equal sets become the same DFA state, so moves found from one visit are reused on the next.

For *search*, where any substring may match, add $q_0$ to the result of MOVE at line L6 before the closure, and report each position where $S$ is accepting; this is Thompson's way of starting a new match at every symbol, and it is what the implementation does with `unanchored=True`.

## Example

**A small run.** Take $r = (a \mid b)^* ab$ and its Glushkov automaton, with positions $1{:}a$, $2{:}b$, $3{:}a$, $4{:}b$ and initial state 0, so that each set is short to write. On $w = abab$, unlimited capacity:

| step | symbol | $S$ before | cached? | $S$ after |
|---|---|---|---|---|
| 1 | $a$ | $\{0\}$ | no | $\{1, 3\}$ |
| 2 | $b$ | $\{1, 3\}$ | no | $\{2, 4\}$ |
| 3 | $a$ | $\{2, 4\}$ | no | $\{1, 3\}$, already a state |
| 4 | $b$ | $\{1, 3\}$ | yes | $\{2, 4\}$ |

The last set contains the accepting position 4, so $abab$ matches. Three DFA states were made and three moves computed; step 4 was a lookup. Running $abab$ again computes nothing new. With the Thompson NFA of the same expression, which has 16 states, the sets have 8, 10, 9, 10 and 9 NFA states, and again three DFA states and three computed moves suffice.

**Where the full DFA is too large.** Let $L_n = (a \mid b)^* a (a \mid b)^{n-1}$, the words whose $n$-th symbol from the end is $a$. Its subset DFA has $2^n + 1$ reachable states with the Glushkov automaton, checked for $n = 1, \ldots, 8$, and $2^n + 1 = 1025$ with the Thompson NFA for $n = 10$. On a random text of $10^4$ symbols over $\{a, b\}$ (seed 1), with the Thompson NFA:

| $n$ | capacity | DFA states made | moves computed | flushes |
|---|---|---|---|---|
| 10 | no limit | 1025 | 2035 | 0 |
| 10 | 1000 | 2942 | 4907 | 2 |
| 20 | no limit | 9940 | 9968 | 0 |
| 20 | 1000 | 9998 | 9999 | 9 |

For $n = 10$ the whole DFA is reached and then every step is a lookup. For $n = 20$ the full DFA would have $2^{20} + 1 = 1{,}048{,}577$ states, but the text reaches fewer than $10^4$; almost every step is a new state, so the lazy DFA does the work of an NFA simulation plus the cost of the cache. This is the input that RE2's fallback to an NFA search is meant for.

## Correctness

For a word $u$, let $\hat\delta(u)$ be the state of the subset DFA after $u$: $\hat\delta(\varepsilon) = \mathrm{CLOSURE}(\{q_0\})$ and $\hat\delta(ua) = \mathrm{CLOSURE}(\mathrm{MOVE}(\hat\delta(u), a))$. The standard fact about the subset construction is that $\hat\delta(u)$ is the set of NFA states reachable from $q_0$ by a path labelled $u$, so $N$ accepts $u$ if and only if $\hat\delta(u) \cap F \ne \emptyset$.

The algorithm keeps two invariants. First, every stored move is right: if $S.\mathrm{next}[c] = T$, then $T.\mathrm{set} = \mathrm{CLOSURE}(\mathrm{MOVE}(S.\mathrm{set}, c))$. Line L9 is the only place that stores a move, and it stores the value just computed at line L6; a flush only removes states from the map and never changes a stored set or move. Second, after $i$ rounds of the loop, $S.\mathrm{set} = \hat\delta(a_1 \cdots a_i)$: either the move is read from the table, which is right by the first invariant, or it is computed. So line L11 returns whether $\hat\delta(w)$ meets $F$, which is whether $N$ accepts $w$. The loop runs $n$ times and each closure is a search in the finite NFA, so the algorithm stops. The full proof is below.

## Complexity

- **Time.** A cached move costs $O(1)$ expected time, for one hash or table lookup. A computed move costs $O(|Q| + E)$ for MOVE and CLOSURE, where $E$ is the number of moves of the NFA, plus $O(|Q|)$ to hash the set; for a Thompson NFA, $|Q| \le 2m$ and $E = O(m)$, so this is $O(m)$. At most $n$ moves are computed, so the worst case is $O(mn)$, the same as NFA simulation. If the text revisits a bounded set of DFA states, the time is $O(n)$ plus $O(m)$ per distinct move, and the second and later passes over similar text cost $O(n)$.
- **Space.** At most $k$ DFA states are cached, each with a set of $O(m)$ NFA states and a table with at most $s$ entries, one per symbol that occurs in the text: $O(k(m + s))$. Without a capacity, the cache holds at most $n + 1$ states, since each step adds at most one.
- **Preprocessing.** Building the Thompson NFA takes $O(m)$ time. The full subset construction would take time and space proportional to the number of reachable DFA states, up to $2^{|Q|}$.
- **Flushes.** Each flush throws away work; in the worst case a flush happens every $k$ steps, and every step computes a move. Then the cost is the $O(mn)$ of NFA simulation plus the overhead of the cache, which is why RE2 counts flushes and switches to an NFA search when there are too many.

## Properties

- **Lazy subset construction.** The DFA states made are exactly the subset states that the text reaches, at most one new state per symbol.
- **Same answers as the DFA.** Caching never changes the result; only the time changes.
- **Bounded memory.** With a capacity, the memory is fixed in advance, whatever the expression and text, which matters for servers that match untrusted patterns.
- **Deterministic time per symbol after warm-up.** Once the states that a text uses are cached, each symbol costs one lookup, like a precomputed DFA.
- **No submatches.** A DFA state is a set without order or history, so it can tell whether and where a match ends, but not where the groups are. For groups, engines run a [Pike VM](/pike-vm/) or a backtracker on the part of the text that the DFA found.

## Variants and improvements

- **Search and match positions.** Adding $q_0$ after each symbol finds the ends of matches. RE2 also orders the NFA states in a DFA state by priority, to find where the leftmost match ends, and then runs a DFA for the reversed expression backward from there to find where it starts (Cox, 2010).
- **Replacement policies.** Flushing the whole cache, as in RE2, is simple and needs no bookkeeping; awk keeps at most 32 states (Cox, 2007). Policies that evict single states need to remove the moves that point to them, which costs more.
- **Fallback.** If the cache is flushed too often, switch to NFA simulation, whose cost per symbol is the same but without the overhead of hashing and storing states.
- **Byte classes.** Group the symbols that no NFA move tells apart into classes, so each table has one entry per class instead of per byte.
- **Derivatives.** With [Brzozowski derivatives](/brzozowski-derivatives/), the DFA states are expressions instead of sets, and memoizing derivatives is a lazy DFA of the same kind.
- **Full DFA.** When the expression is fixed and its DFA is small, as in a lexer, build it once in advance and drop the test at line L5.

## When to use it

Use a lazy DFA to decide whether, or where, a text matches an expression without backreferences, when the expression may have a large DFA and the text is long; RE2 uses it as its main matching engine (Cox, 2010). It gives DFA speed on typical text and the time bound of NFA simulation in the worst case. Do not use it for capture groups, which a DFA cannot track, or for backreferences, which describe languages that are not regular; engines with those features use a [Pike VM](/pike-vm/) or [backtracking](/backtracking-regex-matching/).

## Pitfalls

- **Unbounded growth.** Without a capacity, an expression like $L_{20}$ on random text makes a new state at almost every symbol, and the cache grows with the text. Set a limit.
- **Dangling pointers after a flush.** In languages with manual memory, the current state must be copied out, or kept, before the cache memory is freed. The implementation here keeps the current state object alive, but drops it from the map.
- **Equal sets, different states.** The set of NFA states must be stored in a canonical form, such as a sorted list or a frozen set, so that the same set found twice is found in the map.
- **Thrashing.** A small capacity on a text that cycles through more states than fit makes every step a computed move plus a flush; count flushes and fall back to NFA simulation.
- **Closure on every step.** The closure must be computed after MOVE, including the $\varepsilon$-moves that loop, and with an explicit stack: a recursive closure can overflow on long chains of $\varepsilon$-moves.

## Implementations

## History

Thompson (1968) matched regular expressions by following all states of the automaton at once, which is the step that a lazy DFA caches. According to Cox (2007), the egrep that Aho wrote for the Seventh Edition of Unix (1979) used a precomputed DFA, and by the Eighth Edition (1985) egrep computed the DFA on the fly; awk keeps a cache of at most 32 states. RE2, described by Cox (2010), treats its DFA states as a cache that it frees completely when full, and falls back to an NFA search if it must do so too often.

## References
