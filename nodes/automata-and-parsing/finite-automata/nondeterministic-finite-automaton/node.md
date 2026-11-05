---
tag: CJ87VG
kind: model
slug: nondeterministic-finite-automaton
name: Nondeterministic finite automaton
aliases:
- NFA
area: automata-and-parsing/finite-automata
level: intro
summary: Finite automaton that may have several transitions per symbol and accepts if some run accepts.
prereqs: [deterministic-finite-automaton]
see_also:
- subset-construction
- rabin-scott-theorem
- epsilon-nfa
- nfa-simulation
- nfa-universality
- nfa-minimization
- unambiguous-nfa
- thompson-construction
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.2, Nondeterminism (Definition 1.37 of an NFA, Theorem 1.39 on the equivalence with DFAs)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3, Nondeterministic Finite Automata (the extended transition function, the subset construction, and the bad case for the subset construction)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 5, Nondeterministic Finite Automata, and Lecture 6, The Subset Construction
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the definition of nondeterministic automata and the proof that they accept only regular sets)
  - paper: "Ian Glaister and Jeffrey Shallit, A lower bound technique for the size of nondeterministic finite automata, Information Processing Letters 59(2) (1996)"
    locator: pp. 75 to 77 (the fooling set lower bound)
  - paper: "Markus Holzer and Martin Kutrib, Nondeterministic descriptional complexity of regular languages, International Journal of Foundations of Computer Science 14(6) (2003)"
    locator: pp. 1087 to 1102 (the tight bounds on the number of NFA states for the operations)
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (the PSPACE lower bound for the universality and the equivalence of regular expressions and NFAs)
---

A nondeterministic finite automaton (NFA) is a [finite automaton](/deterministic-finite-automaton/) that can have zero, one or several next states for a state and an input symbol. It accepts a string when at least one of its runs on the string ends in an accepting state. NFAs accept exactly the [regular languages](/regular-language/), the same class as DFAs ([Rabin-Scott theorem](/rabin-scott-theorem/)), but an NFA can be exponentially smaller than every equivalent DFA. Regular expression engines and many proofs about regular languages use NFAs, because they are easy to build and to combine.

## The machine

An NFA is a tuple $N = (Q, \Sigma, \delta, q_0, F)$, where

- $Q$ is a finite, non-empty set of states,
- $\Sigma$ is a finite [alphabet](/alphabet/),
- $\delta : Q \times \Sigma \to \mathcal{P}(Q)$ is the transition function, which gives a set of next states,
- $q_0 \in Q$ is the start state, and
- $F \subseteq Q$ is the set of accepting states.

This is the notation of the [DFA](/deterministic-finite-automaton/) page, with one change: $\delta(q, a)$ is a set. The set can be empty, so an NFA need not be complete. An NFA on this page has no $\varepsilon$-moves. The [epsilon-NFA](/epsilon-nfa/) adds moves that read no input, with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$. A DFA is an NFA in which each set $\delta(q, a)$ has exactly one element. Some texts allow a set $I \subseteq Q$ of start states. A new start state $s$ with $\delta(s, a) = \bigcup_{q \in I} \delta(q, a)$, accepting when $I \cap F \ne \emptyset$, gives one start state and the same language.

**Runs and the language.** Let $w = a_1 a_2 \cdots a_n$ with $a_i \in \Sigma$. A run of $N$ on $w$ is a sequence of states $r_0, r_1, \ldots, r_n$ with $r_0 = q_0$ and $r_i \in \delta(r_{i-1}, a_i)$ for $1 \le i \le n$. The run is accepting when $r_n \in F$. A string can have many runs, one run, or none: a run stops when it meets an empty set of next states. The NFA accepts $w$ when some run on $w$ is accepting, and

$$L(N) = \{ w \in \Sigma^* : \text{some run of } N \text{ on } w \text{ is accepting} \}.$$

So acceptance is existential. A rejecting run says nothing; a string is rejected only when all its runs reject.

**The extended transition function.** For a set $S \subseteq Q$ define $\hat\delta(S, \varepsilon) = S$ and $\hat\delta(S, wa) = \bigcup_{q \in \hat\delta(S, w)} \delta(q, a)$ for $w \in \Sigma^*$ and $a \in \Sigma$.

**Lemma.** For each string $w$, $\hat\delta(\{q_0\}, w)$ is the set of the last states of the runs of $N$ on $w$. So $w \in L(N)$ if and only if $\hat\delta(\{q_0\}, w) \cap F \ne \emptyset$.

*Proof.* By induction on $|w|$. For $w = \varepsilon$ the only run is $r_0 = q_0$, and $\hat\delta(\{q_0\}, \varepsilon) = \{q_0\}$. For $wa$, a run on $wa$ is a run on $w$ that ends in some state $q$, followed by a state of $\delta(q, a)$. By the induction hypothesis the possible states $q$ are the elements of $\hat\delta(\{q_0\}, w)$, so the possible last states are the elements of $\bigcup_{q \in \hat\delta(\{q_0\}, w)} \delta(q, a) = \hat\delta(\{q_0\}, wa)$. $\square$

The lemma is the base of the [subset construction](/subset-construction/) and of [NFA simulation](/nfa-simulation/): both follow the set of active states instead of one run.

**The graph view.** An NFA is a [directed graph](/directed-graph/) with an edge $q \to r$ labelled $a$ for each $r \in \delta(q, a)$. A vertex can have several outgoing edges with the same label, or none. The runs on $w$ are the walks from $q_0$ whose labels spell $w$, and $w$ is accepted when one of these walks ends in $F$.

**Example.** Let $N_3$ accept the strings over $\{a, b\}$ whose third symbol from the end is $a$. Take $Q = \{0, 1, 2, 3\}$, $q_0 = 0$, $F = \{3\}$, and

| $\delta$ | $a$ | $b$ |
|---|---|---|
| 0 | $\{0, 1\}$ | $\{0\}$ |
| 1 | $\{2\}$ | $\{2\}$ |
| 2 | $\{3\}$ | $\{3\}$ |
| 3 | $\emptyset$ | $\emptyset$ |

The NFA stays in state 0 and, on some $a$, guesses that this $a$ is the third symbol from the end. It then counts two more symbols. The sets of active states on $baabb$ are $\{0\}, \{0\}, \{0, 1\}, \{0, 1, 2\}, \{0, 2, 3\}, \{0, 3\}$. The last set holds 3, so $N_3$ accepts $baabb$. On $babba$ the sets are $\{0\}, \{0\}, \{0, 1\}, \{0, 2\}, \{0, 3\}, \{0, 1\}$, and $N_3$ rejects. The same construction with $n + 1$ states accepts the strings whose $n$-th symbol from the end is $a$.

## What it counts

The size of an NFA is its number of states $n = |Q|$. The number of transitions is $m = \sum_{q \in Q} \sum_{a \in \Sigma} |\delta(q, a)|$, which is at most $|\Sigma| n^2$. The description of an NFA takes $O(n + m)$ space.

An NFA is not a model of a real machine that guesses. It is a description of a language, and the cost of a computation depends on how a deterministic program uses it.

- **Run on one string.** [NFA simulation](/nfa-simulation/) follows the set of active states and decides acceptance of a string of length $\ell$ in $O(\ell (n + m))$ time and $O(n)$ space on the [word RAM](/word-ram/). Trying the runs one at a time by backtracking can take time exponential in $\ell$. This is the problem of [NFA membership](/nfa-membership/).
- **Conversion to a DFA.** The [subset construction](/subset-construction/) gives a DFA with at most $2^n$ states, and some NFAs need all of them.

So the number of states measures how short the description is. The main tool to bound it from below is a *fooling set*: a set of pairs $(x_1, y_1), \ldots, (x_k, y_k)$ of strings with $x_i y_i \in L$ for each $i$ and $x_i y_j \notin L$ for each $i \ne j$.

**Lemma (fooling set).** If $L$ has a fooling set of size $k$, then each NFA for $L$ has at least $k$ states.

*Proof.* Fix an NFA for $L$. For each $i$, take an accepting run on $x_i y_i$, and let $p_i$ be its state after the prefix $x_i$. Suppose $p_i = p_j$ for some $i \ne j$. Then the first part of the run for $x_i y_i$, up to $p_i$, followed by the second part of the run for $x_j y_j$, from $p_j$, is an accepting run on $x_i y_j$. This contradicts $x_i y_j \notin L$. So the $k$ states $p_i$ are distinct. $\square$

For the language of $N_3$ above, the pairs $(\varepsilon, abb)$, $(a, bb)$, $(ab, b)$ and $(abb, \varepsilon)$ form a fooling set. Each pair gives the string $abb$. For two different pairs, $x_i y_j$ is shorter than three symbols or has $b$ as its third symbol from the end. So $N_3$ is a smallest NFA for its language. The same pairs for general $n$ show that $n + 1$ states are necessary. The [fooling set method](/fooling-set-method/) of communication complexity uses the same idea.

## Relation to other models

- **DFAs.** Each DFA is an NFA. The [subset construction](/subset-construction/) turns an NFA with $n$ states into a DFA with at most $2^n$ states, so both models accept the same languages ([Rabin-Scott theorem](/rabin-scott-theorem/)). For $N_3$ the construction gives 8 reachable subsets, and the smallest DFA also has $8 = 2^3$ states. In general the language "the $n$-th symbol from the end is $a$" has an NFA with $n + 1$ states, and its smallest DFA has $2^n$ states. See the [determinization blow-up lower bound](/determinization-blowup-lower-bound/).
- **Epsilon-NFAs.** An [epsilon-NFA](/epsilon-nfa/) also allows moves on the empty string. Its [epsilon-closure](/epsilon-closure/) removes these moves with no new states, so it accepts the same languages.
- **Regular expressions.** The [Thompson construction](/thompson-construction/) turns a [regular expression](/regular-expression/) of length $k$ into an epsilon-NFA with $O(k)$ states, and the [Glushkov automaton](/glushkov-automaton/) gives an NFA without $\varepsilon$-moves with one state more than the number of letters of the expression. [Kleene's theorem](/kleene-theorem/) gives the other direction.
- **Restricted nondeterminism.** An [unambiguous NFA](/unambiguous-nfa/) has at most one accepting run on each string. $N_3$ is unambiguous: an accepting run must guess the $a$ at the right position.
- **More general branching.** An [alternating finite automaton](/alternating-finite-automaton/) adds universal branching, and a [two-way finite automaton](/two-way-finite-automaton/) moves its head both ways. Both still accept only regular languages.
- **Weights and probabilities.** A [weighted automaton](/weighted-automaton/) over the Boolean semiring is an NFA. A [probabilistic finite automaton](/probabilistic-finite-automaton/) replaces the choice of a next state with a random choice.
- **Turing machines.** A [nondeterministic Turing machine](/nondeterministic-turing-machine/) that only reads its input and only moves right is an NFA.

## Known results in the model

Below, $n$ and $m$ are the numbers of states and transitions, and the time bounds are for the [word RAM](/word-ram/).

### Closure and size

The regular languages are closed under the operations below, and NFAs give small constructions for most of them. The bounds are the worst-case number of states of the result, for NFAs with $n_1$ and $n_2$ states. Each bound is reached for some languages, over a suitable alphabet (Holzer and Kutrib, 2003).

| operation | NFA states |
|---|---|
| union | $n_1 + n_2 + 1$ |
| intersection | $n_1 n_2$ |
| concatenation | $n_1 + n_2$ |
| star | $n + 1$ |
| reversal | $n + 1$ |
| complement | $2^n$ |

The union adds a new start state $s$ with $\delta(s, a) = \delta_1(q_1, a) \cup \delta_2(q_2, a)$. The intersection is the [product construction](/product-construction/). The reversal reverses each edge and adds a new start state with the incoming edges of the old accepting states. The complement is the expensive one: an NFA has no simple complement, so the usual method determinizes first. The proofs are on the [closure properties](/closure-properties-of-regular-languages/) page.

### Decision problems

- **Membership.** $O(\ell (n + m))$ time for a string of length $\ell$. See [NFA membership](/nfa-membership/).
- **Emptiness.** $L(N) \ne \emptyset$ if and only if a state of $F$ is reachable from $q_0$ in the graph view. A [breadth-first search](/breadth-first-search/) decides this in $O(n + m)$ time.
- **Universality.** Deciding $L(N) = \Sigma^*$ is [PSPACE](/pspace/)-complete (Meyer and Stockmeyer, 1972). See [NFA universality](/nfa-universality/).
- **Equivalence and inclusion.** Deciding $L(N_1) = L(N_2)$ or $L(N_1) \subseteq L(N_2)$ is PSPACE-complete. See [NFA equivalence](/nfa-equivalence/).
- **Minimization.** Finding an NFA with the fewest states for $L(N)$ is PSPACE-hard, and a smallest NFA need not be unique. See [NFA minimization](/nfa-minimization/).

For DFAs all these problems take polynomial time. The gap comes from complement: a DFA is complemented by swapping $F$ and $Q \setminus F$, and an NFA is not.

### Pitfalls

- **Swapping accepting states does not complement an NFA.** In $N_3$ make $\{0, 1, 2\}$ accepting and 3 not. Every string has a run that stays in state 0, so the new NFA accepts all of $\Sigma^*$, not the complement. The swap complements an automaton only when each string has exactly one run, as in a complete DFA.
- **A rejecting run does not reject the string.** A program that follows one run, and stops when that run fails, decides a different language. It must try all runs, or follow the set of active states.
- **Nondeterministic and incomplete are different things.** A DFA with missing transitions is a partial DFA, not an NFA with real choices. The two notions are often mixed up when states are counted.
- **The blow-up is in the worst case.** Many NFAs from practice determinize to DFAs of about their own size. The $2^n$ bound is a worst case, not a typical cost.

## References
