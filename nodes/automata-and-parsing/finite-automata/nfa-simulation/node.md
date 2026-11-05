---
tag: B4QP59
kind: algorithm
slug: nfa-simulation
name: NFA simulation
aliases:
- on-the-fly subset simulation
- set-of-states simulation
area: automata-and-parsing/finite-automata
level: core
summary: Runs an NFA on an input of length l by tracking the set of active states, in O(l(n + m)) time and O(n) space.
solves: [nfa-membership]
model: word-ram
complexity:
  vars: {ℓ: the length of the input, n: the number of NFA states, m: the number of NFA transitions}
  time: {worst: O(ℓ(n + m))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1968
  people: [Ken Thompson]
  note: Thompson's regular expression search compiled a pattern into code that follows all states of its automaton at once, one input character at a time.
prereqs: [nondeterministic-finite-automaton, epsilon-closure]
see_also: [nfa-membership, subset-construction, thompson-nfa-simulation, epsilon-nfa, regex-matching, backtracking-regex-matching, bit-parallel-regex-matching, nfa-determinization]
sources:
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.7, From Regular Expressions to Automata (the simulation of an NFA with two stacks of states and the time of the simulation)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.2, Nondeterminism (the computation of an NFA as parallel copies of the machine)
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast, 2007
    locator: sections Regular Expression Search Algorithms and Performance (Thompson's simulation against backtracking)
---

NFA simulation decides whether a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) accepts an input string by keeping, after each symbol, the set of all states in which some run of the automaton can be. It reads the input once, from left to right, and never builds the full DFA. For an NFA with $n$ states and $m$ transitions and an input of length $\ell$ it takes $O(\ell (n + m))$ time and $O(n)$ extra space, while trying the runs one by one can take exponential time. It solves [NFA membership](/nfa-membership/), and it is the core of the regular expression engines that guarantee linear time in the length of the input.

## In plain words

An NFA can have several moves for one letter, so a string can have many runs. Do not follow them one by one. Instead, keep a list of the states that the runs can be in now, with no state written twice. To read the next letter, take every move on that letter from every state in the list; the targets form the new list. If the NFA has free moves, which read no letter, add every state that they reach.

The list never has more states than the NFA, so each letter costs a bounded amount of work. At the end, the string is accepted when the list holds an accepting state. If the list becomes empty, no run survives, and you can stop early.

## The problem

The input is an NFA $N = (Q, \Sigma, \delta, q_0, F)$ that may have $\varepsilon$-moves, $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$, as on the [epsilon-NFA](/epsilon-nfa/) page, and a string $w = a_1 \cdots a_\ell \in \Sigma^*$. The NFA need not be complete. The output is yes if $w \in L(N)$ and no otherwise. Let $n = |Q|$ and let $m$ be the number of transitions, $\varepsilon$-moves included.

For $S \subseteq Q$, the closure $E(S)$ is the set of states that a path of zero or more $\varepsilon$-moves reaches from a state of $S$. For an NFA without $\varepsilon$-moves, $E(S) = S$.

## The algorithm

```pseudo id=main
NFA-SIMULATION(N, w)                   ▷ N = (Q, Σ, δ, q0, F), ε-moves allowed; w = a1 ... aℓ
L1  S ← CLOSE({q0})
L2  for i ← 1 to ℓ do
L3      T ← ∅
L4      for each q ∈ S do
L5          for each r ∈ δ(q, a_i) do add r to T
L6      S ← CLOSE(T)
L7      if S = ∅ then return false
L8  return S ∩ F ≠ ∅

CLOSE(S)                               ▷ the ε-closure E(S)
L9  C ← S;  K ← a stack that holds the elements of S
L10 while K is not empty do
L11     q ← pop K
L12     for each r ∈ δ(q, ε) with r ∉ C do add r to C and push r on K
L13 return C
```

Line L1 makes the set of states that $N$ can be in before it reads a symbol. Lines L3 to L5 take one step on $a_i$ from each active state, and line L6 adds the states that $\varepsilon$-moves reach after the step. Line L7 stops when no run survives, since no later symbol can bring a state back. Line L8 accepts when some run ends in an accepting state. The sets $S$ and $T$ are kept as a boolean array over $Q$ plus a list of the members, so that "add $r$" and the test $r \notin C$ cost $O(1)$ and no state is stored twice.

## Example

Let $N$ accept $a^* b^* \cup (ab)^*$, with $Q = \{0, 1, 2, 3, 4\}$, $q_0 = 0$, $F = \{2, 3\}$, and the moves $0 \xrightarrow{\varepsilon} 1$, $0 \xrightarrow{\varepsilon} 3$, $1 \xrightarrow{a} 1$, $1 \xrightarrow{\varepsilon} 2$, $2 \xrightarrow{b} 2$ for the part $a^* b^*$, and $3 \xrightarrow{a} 4$, $4 \xrightarrow{b} 3$ for the part $(ab)^*$. Line L1 gives $S = E(\{0\}) = \{0, 1, 2, 3\}$.

| input | $T$ and $S$ after each symbol | result |
|---|---|---|
| $abab$ | $a$: $T = \{1, 4\}$, $S = \{1, 2, 4\}$; $b$: $T = \{2, 3\}$, $S = \{2, 3\}$; $a$: $S = \{4\}$; $b$: $S = \{3\}$ | $3 \in F$: accept |
| $aab$ | $a$: $S = \{1, 2, 4\}$; $a$: $T = \{1\}$, $S = \{1, 2\}$; $b$: $S = \{2\}$ | $2 \in F$: accept |
| $bab$ | $b$: $S = \{2\}$; $a$: $S = \emptyset$ | stop at line L7: reject |
| $aba$ | $a$: $S = \{1, 2, 4\}$; $b$: $S = \{2, 3\}$; $a$: $S = \{4\}$ | $\{4\} \cap F = \emptyset$: reject |

In the first row, the step on $a$ from $\{0, 1, 2, 3\}$ moves 1 to 1 and 3 to 4, and the closure adds 2 because of $1 \xrightarrow{\varepsilon} 2$. The two parts of the language run side by side in one set until the input rules one of them out.

**Many runs, small sets.** Let $N'$ have the states 0 and 1, no accepting state, and $\delta(q, a) = \{0, 1\}$ for both states. On $a^{20} c$ it has $2^{20} = 1{,}048{,}576$ runs that read $a^{20}$, and a [backtracking](/backtracking-regex-matching/) search visits all of them before it rejects. The simulation holds $S = \{0, 1\}$ after each $a$ and $S = \emptyset$ after the $c$, so it takes 21 steps.

## Correctness

For a string $w$, let $R(w)$ be the set of states in which some run of $N$ on $w$ ends, where a run may take $\varepsilon$-moves before, between and after the symbols. Then $w \in L(N)$ if and only if $R(w) \cap F \ne \emptyset$.

**CLOSE.** Each state in $C$ is in $E(S)$, because it is in $S$ or was added along an $\varepsilon$-move from a state of $C$. Each state is pushed at most once, because it is pushed only when it enters $C$, so the loop stops. When the loop stops, each state of $C$ has been popped, so for each $\varepsilon$-move $q \to r$ with $q \in C$, also $r \in C$. A path of $\varepsilon$-moves from $S$ therefore stays in $C$, and $E(S) \subseteq C$.

**Invariant.** After the $i$-th pass of the loop at line L2, $S = R(a_1 \cdots a_i)$. Before the loop, $S = E(\{q_0\}) = R(\varepsilon)$ by line L1. If $S = R(v)$ for $v = a_1 \cdots a_{i-1}$, then after lines L3 to L6, $S = E(\bigcup_{q \in R(v)} \delta(q, a_i))$. This equals $R(v a_i)$: a run on $v a_i$ is a run on $v$, then one $a_i$-move, then $\varepsilon$-moves, and each such combination is a run. The full argument, with both inclusions, is the lemma on the [Rabin-Scott theorem](/rabin-scott-theorem/) page.

**Early exit.** If $R(a_1 \cdots a_i) = \emptyset$, then no run reads $a_1 \cdots a_i$, so no run reads $w$, and $w \notin L(N)$. So line L7 is correct. Otherwise line L8 returns $R(w) \cap F \ne \emptyset$, which is the definition of acceptance.

## Complexity

- **Time.** One pass of the loop at line L2 reads, at lines L4 and L5, the $a_i$-moves of the states of $S$, at most $m$ of them, and touches at most $n$ states. CLOSE pushes each state at most once and reads each $\varepsilon$-move at most once, so it costs $O(n + m)$. Clearing the boolean array costs $O(n)$, or $O(1)$ with a pass number stored per state instead of a boolean. So one symbol costs $O(n + m)$, and the whole run costs $O(\ell (n + m))$ on the [word RAM](/word-ram/) in the worst case.
- **Space.** Two sets of at most $n$ states, the stack of CLOSE and the boolean array: $O(n)$ words beyond the input.
- **Fixed automaton.** For a fixed $N$, the time is $O(\ell)$ with a constant of order $n + m$, and the space is constant, as for a DFA.
- **Comparison.** Backtracking can take $\Theta(2^\ell)$ time, as in the example. Building the DFA first costs up to $2^n$ states, after which each symbol costs $O(1)$. The simulation never pays either exponential.

## Properties

- **Online.** It reads the input once, from left to right, and after each prefix it knows whether that prefix is accepted. So it also reports all accepted prefixes in the same time.
- **No recursion.** CLOSE uses an explicit stack, and the main loop is iterative.
- **Deterministic.** It makes no choices; the order of the states in $S$ does not change the result.
- **Exact sets.** The sets $S$ are exactly the states that the [subset construction](/subset-construction/) would visit on $w$, one per prefix.
- **Works for partial automata.** Missing transitions are empty sets, and they only shrink $S$.

## Variants and improvements

- **Thompson's simulation.** [Thompson's NFA simulation](/thompson-nfa-simulation/) runs this algorithm on the automaton that the [Thompson construction](/thompson-construction/) builds from a regular expression, where each state has at most two outgoing moves, so $m \le 2n$ and one symbol costs $O(n)$.
- **Search.** To find the substrings of $w$ that $N$ accepts, add $E(\{q_0\})$ to $S$ before each symbol. Then $S$ holds the states of all runs that started at any earlier position, and line L8 at each position reports where a match ends. This is [regex search](/regex-search/).
- **Bit-parallel sets.** When $n$ fits in a machine word, store $S$ as one word. For automata of regular expressions with simple structure, such as the [Glushkov automaton](/glushkov-automaton/), one step is a few word operations and table lookups ([bit-parallel regex matching](/bit-parallel-regex-matching/)).
- **Lazy DFA.** Cache each set $S$ and its successor on each symbol. When the input revisits a cached set, the step is one lookup. This is the subset construction done on demand.
- **Counting runs.** Replace the set by a vector of counts, with $c'(r) = \sum_{q : r \in \delta(q, a)} c(q)$ for an NFA without $\varepsilon$-moves. The result is the number of accepting runs, as for a [weighted automaton](/weighted-automaton/) over the natural numbers.
- **Submatch positions.** Regular expression engines keep, with each active state, the positions where the groups of the expression started, and keep only one thread per state by a fixed priority. This finds submatches in the same time bound.

## When to use it

Use the simulation when an NFA runs on one long input or on few inputs, when the DFA may be large, or when a linear bound in the input length is a requirement, as for untrusted input to a regular expression engine. When the same small automaton runs on many inputs, build the DFA once with the [subset construction](/subset-construction/) and pay $O(1)$ per symbol. A lazy DFA gets most of the speed of a DFA with the safety of the simulation.

## Pitfalls

- **Duplicate states.** If $T$ is a list that allows repeats, the same state can appear once for each run, and the list grows like the number of runs, which is exponential in the example. Keep a set, or mark the states already added.
- **No closure of the start state.** Line L1 must close $\{q_0\}$. In the example, without the closure, $S = \{0\}$ has no move on $a$, and the algorithm rejects $a$, which is in $a^* b^*$.
- **No closure after the last symbol.** Line L6 closes $T$ after every step, the last one included. Without the closure after the last $a$ of $aa$, the set is $\{1\}$, and $aa$ is rejected, because only state 2 is accepting.
- **Recursion in CLOSE.** A recursive closure overflows the stack on a long chain of $\varepsilon$-moves. Use an explicit stack as in lines L9 to L13.
- **Clearing the marks.** Resetting a boolean array of size $n$ at each step is $O(n)$, which is fine; resetting a structure of size $m$ or rebuilding a hash set of all states each step can raise the cost. A per-state pass number avoids any reset.
- **Backtracking instead.** A depth-first search over runs looks simpler, but it is exponential in the worst case; that is the failure mode of backtracking regex engines.

## Implementations

## History

Thompson (1968) described a regular expression search for the QED editor that compiled the expression into machine code for the IBM 7094 and followed all active states of its automaton in parallel, one input character at a time. Aho, Lam, Sethi and Ullman present the same idea as the simulation of an NFA. Cox (2007) compared it with the backtracking engines of common libraries and showed the exponential gap on small examples.

## References
