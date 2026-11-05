---
tag: MBRBPG
kind: model
slug: deterministic-finite-automaton
name: Deterministic finite automaton
aliases:
- DFA
area: automata-and-parsing/finite-automata
level: intro
summary: Finite-state machine with exactly one transition per state and symbol; recognizes regular languages.
prereqs: [alphabet, directed-graph]
see_also:
- nondeterministic-finite-automaton
- regular-language
- kleene-theorem
- myhill-nerode-theorem
- dfa-minimization
- closure-properties-of-regular-languages
- string-matching-automaton
- pushdown-automaton
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.1, Finite Automata (the formal definition and the closure under union); Section 4.1 (the decidability of emptiness and equivalence for DFAs)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.2, Deterministic Finite Automata; Chapter 4, Properties of Regular Languages
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 3, Finite Automata and Regular Sets; Lectures 13 to 16 (state minimization and the Myhill-Nerode theorem)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.3, String matching with finite automata
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125
  - paper: "Stephen C. Kleene, Representation of events in nerve nets and finite automata, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 3 to 41
  - paper: "Sheng Yu, Qingyu Zhuang and Kai Salomaa, The state complexities of some basic operations on regular languages, Theoretical Computer Science 125(2) (1994)"
    locator: pp. 315 to 328 (the state complexity of concatenation, star and the Boolean operations)
---

A deterministic finite automaton (DFA) is a machine with a finite set of states that reads a string one symbol at a time and has exactly one next state for each state and each symbol. It accepts the string when the last state is an accepting state. DFAs recognize exactly the [regular languages](/regular-language/), and each of them runs in one pass over the input with constant memory. Lexical analyzers, the [string-matching automaton](/string-matching-automaton/) and protocol checkers are DFAs.

## The machine

A DFA is a tuple $M = (Q, \Sigma, \delta, q_0, F)$, where

- $Q$ is a finite, non-empty set of states,
- $\Sigma$ is a finite [alphabet](/alphabet/),
- $\delta : Q \times \Sigma \to Q$ is the transition function,
- $q_0 \in Q$ is the start state, and
- $F \subseteq Q$ is the set of accepting states.

The encyclopedia uses this notation on all pages about finite automata. On these pages a DFA is *complete*: $\delta$ is a total function, so it gives one next state for every pair of a state and a symbol. A DFA has no $\varepsilon$-moves, that is, no move that reads no input. The [nondeterministic finite automaton](/nondeterministic-finite-automaton/) and the [epsilon-NFA](/epsilon-nfa/) relax these two rules.

Some texts allow a *partial* DFA, where $\delta(q, a)$ can be undefined, and the run rejects when it meets a missing transition. Add a new dead state $d \notin F$, send each missing transition to $d$, and set $\delta(d, a) = d$ for each $a \in \Sigma$. The new DFA is complete and accepts the same strings. So the two views define the same languages, and they differ in size by at most one state.

**Runs and the language.** On an input $w = a_1 a_2 \cdots a_n$ with $a_i \in \Sigma$, the run is the sequence of states $r_0, r_1, \ldots, r_n$ with $r_0 = q_0$ and $r_i = \delta(r_{i-1}, a_i)$ for $1 \le i \le n$. The extended transition function $\delta^* : Q \times \Sigma^* \to Q$ gives the last state of a run: $\delta^*(q, \varepsilon) = q$, and $\delta^*(q, wa) = \delta(\delta^*(q, w), a)$ for $w \in \Sigma^*$ and $a \in \Sigma$. So $r_n = \delta^*(q_0, w)$. The DFA accepts $w$ if $\delta^*(q_0, w) \in F$, and the language of $M$ is

$$L(M) = \{ w \in \Sigma^* : \delta^*(q_0, w) \in F \}.$$

**Lemma.** For each state $q$ and all strings $x, y \in \Sigma^*$, $\delta^*(q, xy) = \delta^*(\delta^*(q, x), y)$.

*Proof.* By induction on $|y|$. If $y = \varepsilon$, both sides are $\delta^*(q, x)$. If $y = y'a$ with $a \in \Sigma$, then $\delta^*(q, xy'a) = \delta(\delta^*(q, xy'), a)$ by the definition, which is $\delta(\delta^*(\delta^*(q, x), y'), a)$ by the induction hypothesis, which is $\delta^*(\delta^*(q, x), y'a)$ by the definition again. $\square$

The lemma is the reason a DFA needs no memory other than its state: after it reads $x$, the rest of the run depends only on the state $\delta^*(q_0, x)$, not on $x$ itself.

**The graph view.** A DFA is a [directed graph](/directed-graph/) with the states as vertices and an edge $q \to \delta(q, a)$ labelled $a$ for each pair $(q, a)$. Each vertex has exactly one outgoing edge for each symbol. The run on $w$ is the walk from $q_0$ that follows the labels of $w$. A state is *reachable* when some string leads to it from $q_0$, and it is *dead* when no accepting state is reachable from it.

**Example 1.** Let $M_1$ accept the binary strings with an even number of 1s. Take $Q = \{e, o\}$, $\Sigma = \{0, 1\}$, $q_0 = e$, $F = \{e\}$, and

| $\delta$ | 0 | 1 |
|---|---|---|
| $e$ | $e$ | $o$ |
| $o$ | $o$ | $e$ |

On $1001$ the run is $e, o, o, o, e$, which ends in $F$, so $M_1$ accepts $1001$. On $10110$ the run is $e, o, o, e, o, o$, so $M_1$ rejects $10110$, which has three 1s.

**Example 2.** Let $M_2$ read a binary number, most significant digit first, and accept it when the number is divisible by 3. The states are the residues $Q = \{0, 1, 2\}$, $q_0 = 0$, $F = \{0\}$, and $\delta(r, b) = (2r + b) \bmod 3$. Reading a digit $b$ after a prefix with value $v$ gives the value $2v + b$, so by induction the state after a prefix is its value modulo 3. On $10010$, the number 18, the run is $0, 1, 2, 1, 0, 0$, and $M_2$ accepts. On $1101$, the number 13, the run is $0, 1, 0, 0, 1$, and $M_2$ rejects.

## What it counts

The cost of a run is the number of steps. A step reads one input symbol and looks up one entry of $\delta$. On every input of length $n$ the run makes exactly $n$ steps. The input is read once, from left to right, and the head never moves back. The basic model has no early exit, so a run that enters a dead state still reads the rest of the input.

The only memory is the current state. A DFA has no stack, no tape and no counter. To store the state, a program needs $\lceil \lg |Q| \rceil$ binary digits. The transition table has $|Q| \cdot |\Sigma|$ entries. It is part of the description of the machine and is fixed before the input arrives.

The size of a DFA is its number of states. The main tool to bound it from below is a set of pairwise distinguishable strings. Two strings $x$ and $y$ are *distinguishable* for a language $L$ if some $z \in \Sigma^*$ has $xz \in L$ and $yz \notin L$, or the other way around. If a DFA for $L$ reaches the same state $q$ on $x$ and on $y$, the lemma gives $\delta^*(q_0, xz) = \delta^*(q, z) = \delta^*(q_0, yz)$ for each $z$, so $x$ and $y$ are not distinguishable. Hence a DFA for $L$ has at least as many states as any set of pairwise distinguishable strings has members. The [Myhill-Nerode theorem](/myhill-nerode-theorem/) shows that this bound is exact for the smallest DFA.

For example, let $L$ be the set of strings over $\{1\}$ with exactly $k$ symbols. The strings $1^0, 1^1, \ldots, 1^{k+1}$ are pairwise distinguishable: for $i < j \le k + 1$ the suffix $1^{k-i}$ puts $1^i$ in $L$ and $1^j$ out of $L$. So every DFA for $L$ has at least $k + 2$ states, and a DFA that counts to $k$ and then falls into a dead state has exactly $k + 2$.

## Relation to other models

- **Nondeterministic finite automata.** An [NFA](/nondeterministic-finite-automaton/) can have several next states or none. Each DFA is an NFA. The [subset construction](/subset-construction/) turns an NFA with $n$ states into a DFA with at most $2^n$ states, so the two models define the same languages ([Rabin-Scott theorem](/rabin-scott-theorem/)). The $2^n$ cannot be lowered: see the [determinization blow-up lower bound](/determinization-blowup-lower-bound/).
- **Epsilon-NFAs and regular expressions.** An [epsilon-NFA](/epsilon-nfa/) adds moves that read no input, and it also defines only regular languages. [Kleene's theorem](/kleene-theorem/) shows that [regular expressions](/regular-expression/) define the same class.
- **Two-way automata.** A [two-way finite automaton](/two-way-finite-automaton/) can move its head back, and it still accepts only regular languages.
- **Alternating automata.** An [alternating finite automaton](/alternating-finite-automaton/) has universal and existential branching. It accepts only regular languages, with up to doubly exponentially fewer states than a DFA.
- **Machines with output.** A [Moore machine](/moore-machine/) gives an output in each state, and a [Mealy machine](/mealy-machine/) gives one on each transition. A DFA is a Moore machine with the output alphabet $\{0, 1\}$ when only the last output counts.
- **Pushdown automata.** A [pushdown automaton](/pushdown-automaton/) adds a stack and accepts more languages. The language $\{0^n 1^n : n \ge 0\}$ has infinitely many pairwise distinguishable prefixes $0^0, 0^1, 0^2, \ldots$ (the suffix $1^i$ separates $0^i$ from $0^j$), so no DFA accepts it, but a pushdown automaton does.
- **Turing machines and the word RAM.** A DFA is a [Turing machine](/turing-machine/) that only reads its tape and only moves right. On a [word RAM](/word-ram/), a DFA runs in $O(n)$ time on an input of length $n$, with one table lookup per symbol.

## Known results in the model

Below, $n = |Q|$ and $\sigma = |\Sigma|$, and the time bounds are for the word RAM with the table of $\delta$ in memory.

### The class of languages

- A language is regular if and only if some DFA accepts it. See [regular language](/regular-language/) and [Kleene's theorem](/kleene-theorem/).
- The DFA languages are closed under complement, union, intersection, difference, concatenation, star, reversal, homomorphism and inverse homomorphism. The proofs are on the [closure properties](/closure-properties-of-regular-languages/) page. The complement swaps $F$ and $Q \setminus F$, which works only because $\delta$ is complete. The [product construction](/product-construction/) gives the union and the intersection.
- The [pumping lemma](/pumping-lemma-for-regular-languages/) follows from the [pigeonhole principle](/pigeonhole-principle/): a run of a DFA with $p$ states on a string of length at least $p$ visits $p + 1$ states, so it visits one state twice.

### The minimal DFA

- Every regular language has a DFA with the least number of states, and this DFA is unique up to a renaming of the states ([uniqueness of the minimal DFA](/minimal-dfa-uniqueness/)). Its number of states is the number of classes of the [Myhill-Nerode relation](/myhill-nerode-relation/) of the language.
- The problem of [DFA minimization](/dfa-minimization/) has three classic algorithms. [Moore's algorithm](/moore-minimization/) takes $O(\sigma n^2)$ time in the worst case. [Hopcroft's algorithm](/hopcroft-minimization/) takes $O(\sigma n \log n)$ time (Hopcroft, 1971). [Brzozowski's algorithm](/brzozowski-minimization/) reverses and determinizes twice and can take exponential time.

### Decision problems

- **Membership.** Deciding $w \in L(M)$ takes $|w|$ steps.
- **Emptiness.** $L(M) \ne \emptyset$ if and only if some accepting state is reachable from $q_0$. A graph search decides this in $O(\sigma n)$ time. See [DFA emptiness](/dfa-emptiness/).
- **Finiteness.** $L(M)$ is infinite if and only if some cycle lies on a path from $q_0$ to an accepting state. See [DFA finiteness](/dfa-finiteness/).
- **Equivalence.** $L(M_1) = L(M_2)$ can be decided by a search of the product in $O(\sigma n_1 n_2)$ time, or by the [Hopcroft-Karp algorithm](/hopcroft-karp-equivalence/) in $O(\sigma (n_1 + n_2) \, \alpha(n_1 + n_2))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). See [DFA equivalence](/dfa-equivalence/).
- **Learning.** A DFA can be learned from membership and equivalence queries in polynomial time by the [L* algorithm](/lstar-algorithm/), but finding the smallest DFA that agrees with a set of labelled examples is NP-hard. See [DFA learning](/dfa-learning/).

### Size of the operations

The state complexity of an operation is the worst-case number of states of the minimal DFA of the result, as a function of the numbers of states $m$ and $n$ of the minimal DFAs of the arguments. See [state complexity](/state-complexity/).

| operation | worst-case number of states |
|---|---|
| complement | $n$ |
| union, intersection | $mn$ |
| reversal | $2^n$ |
| concatenation | $m 2^n - 2^{n-1}$ |
| star | $2^{n-1} + 2^{n-2}$ |

The values for concatenation and star hold for $m, n \ge 2$ over a large enough alphabet (Yu, Zhuang and Salomaa, 1994). The value for intersection is reached by the languages "the number of $a$s is divisible by $m$" and "the number of $b$s is divisible by $n$": the $mn$ prefixes $a^i b^j$ with $0 \le i < m$ and $0 \le j < n$ are pairwise distinguishable, because the suffix $a^{m-i} b^{n-j}$ puts $a^i b^j$ in the intersection and every other prefix of the set out of it.

### Pitfalls

- **Complement of a partial DFA.** Swapping the accepting states of a partial DFA gives a wrong result: a string that falls off a missing transition is rejected before and after the swap. Complete the DFA with a dead state first.
- **Unreachable states.** A DFA can have states that no input reaches. They change neither the language nor the run time, but they make the state count larger than needed, and a minimization that does not remove them first returns a DFA that is not minimal.
- **Counting the dead state.** The minimal complete DFA of a language may have a dead state that the minimal partial DFA does not have. State counts from two sources can differ by one for this reason.
- **The alphabet is part of the machine.** The complement of $L(M)$ is taken in $\Sigma^*$. The same set of strings has different complements over $\{a, b\}$ and over $\{a, b, c\}$.

## References
