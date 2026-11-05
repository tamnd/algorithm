---
tag: 9NPRBR
kind: model
slug: two-way-finite-automaton
name: Two-way finite automaton
aliases:
- 2DFA
- two-way DFA
- 2NFA
area: automata-and-parsing/finite-automata
level: advanced
summary: Finite automaton whose head may move left or right; still recognizes only regular languages.
prereqs: [deterministic-finite-automaton, nondeterministic-finite-automaton, myhill-nerode-theorem]
see_also: [regular-language, rabin-scott-theorem, state-complexity, turing-machine, alternating-finite-automaton, regular-language-intersection, logspace, nondeterministic-logspace]
sources:
  - paper: doi:10.1147/rd.32.0198
    title: John C. Shepherdson, The reduction of two-way automata to one-way automata, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 198 to 200 (the tables of a prefix, and the equivalence with one-way automata)
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (two-way automata and the proof with crossing sequences that they accept only regular sets)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lectures 17 and 18 (two-way finite automata, and the proof that 2DFAs accept only regular sets)
  - paper: "Christos A. Kapoutsis, Removing bidirectionality from nondeterministic finite automata, 30th International Symposium on Mathematical Foundations of Computer Science (MFCS 2005), Lecture Notes in Computer Science 3618"
    locator: pp. 544 to 555 (the exact costs of the conversions of 2DFAs and 2NFAs to one-way automata)
  - paper: "William J. Sakoda and Michael Sipser, Nondeterminism and the size of two way finite automata, Tenth Annual ACM Symposium on Theory of Computing (STOC 1978)"
    locator: pp. 275 to 286 (the question of the cost of removing nondeterminism from two-way automata)
---

A two-way finite automaton is a finite automaton that reads its input from a read-only tape and may move its head to the left as well as to the right. The deterministic form is the 2DFA, and the nondeterministic form the 2NFA. Both recognize exactly the [regular languages](/regular-language/) (Rabin and Scott, 1959; Shepherdson, 1959), so moving back does not add power, but it can save states: some languages need exponentially more states on a one-way [DFA](/deterministic-finite-automaton/). Whether 2NFAs can be made deterministic with only polynomially many more states is the open Sakoda-Sipser question.

## The machine

The input $w = a_1 \cdots a_\ell \in \Sigma^*$ sits on a tape between two endmarkers, $\vdash a_1 \cdots a_\ell \dashv$, with $\vdash, \dashv \notin \Sigma$. The cells are numbered $0$ to $\ell + 1$.

A 2DFA is $M = (Q, \Sigma, \delta, q_0, F)$ where $Q$ is a finite set of states, $q_0 \in Q$, $F \subseteq Q$, and $\delta$ is a partial function

$$\delta : Q \times (\Sigma \cup \{\vdash, \dashv\}) \to Q \times \{-1, +1\}.$$

There are no $\varepsilon$-moves: each step reads the current cell and moves the head one cell. The machine never moves left from $\vdash$ or right from $\dashv$. It starts in $q_0$ on cell 0. It *accepts* when it reaches a state of $F$, where it halts; it *rejects* when it reaches a pair $(q, c)$ with no move, or when it runs forever. Other texts accept when the head leaves $\dashv$ to the right, or use one accepting and one rejecting state; these conventions give the same class of languages and change the number of states by at most a constant.

A *configuration* is a pair $(q, i)$ of a state and a head position. On input $w$ there are $|Q| (\ell + 2)$ configurations, so a run that has not halted after $|Q| (\ell + 2)$ steps repeats a configuration and, being deterministic, runs forever.

A 2NFA has $\delta : Q \times (\Sigma \cup \{\vdash, \dashv\}) \to \mathcal{P}(Q \times \{-1, +1\})$ and accepts if some run reaches $F$. A one-way automaton is the special case in which every move is $+1$.

## What it counts

- **States.** The main measure is the number of states $n = |Q|$, as in [state complexity](/state-complexity/): two-way motion trades head moves for states.
- **Steps.** A 2DFA halts within $n (\ell + 2)$ steps or never halts, so its membership test runs in $O(n \ell)$ time on the [word RAM](/word-ram/), with a step counter or a visited table to detect loops. For a 2NFA, membership is [reachability](/graph-reachability/) in the graph of the $n (\ell + 2)$ configurations, in $O(m \ell)$ time where $m$ is the number of transitions.
- **Reversals.** Some results count the number of times the head turns, a measure between one-way automata (no reversals) and the general model.

## Relation to other models

- **One-way automata.** Every DFA is a 2DFA and every NFA a 2NFA. Conversely, every 2NFA accepts a regular language, so the four models DFA, NFA, 2DFA and 2NFA recognize the same languages.
- **Turing machines.** A 2DFA is a deterministic [Turing machine](/turing-machine/) with a read-only input tape and no work tape. Work space bounded by a constant is the same as a 2DFA with more states, so constant space recognizes only regular languages.
- **Logarithmic space.** With a few heads, or with counters bounded by the input length, two-way automata recognize the languages of [deterministic logspace](/logspace/) and [nondeterministic logspace](/nondeterministic-logspace/). With one head, they stay regular.
- **Alternating automata.** [Alternating finite automata](/alternating-finite-automaton/) generalize nondeterminism with universal branches. Their one-way and two-way forms also recognize only regular languages.

## Known results in the model

### Two-way automata accept only regular languages

**Theorem (Rabin and Scott, 1959; Shepherdson, 1959).** For every 2DFA $M$ with $n$ states, $L(M)$ is regular, with a DFA of at most $(n + 2)^{n + 1}$ states.

*Proof (Shepherdson's tables).* For a string $x \in \Sigma^*$ consider the left part $\vdash x$ of the tape. Let $\bot$ mean "never leaves to the right", and let $\mathrm{acc}$ mean "accepts inside $\vdash x$". Define the table $T_x : \{\star\} \cup Q \to Q \cup \{\bot, \mathrm{acc}\}$ by

- $T_x(\star)$: run $M$ on $\vdash x$ from $q_0$ on cell 0, until it first moves right from the last cell of $\vdash x$; the value is the state after that move. If it first reaches $F$, the value is $\mathrm{acc}$; if it gets stuck or loops inside $\vdash x$, the value is $\bot$.
- $T_x(p)$ for $p \in Q$: the same, but starting in state $p$ on the last cell of $\vdash x$, as if the machine had just moved left into it.

These values depend only on $x$, since the run stays inside $\vdash x$ until it leaves to the right. Suppose $T_x = T_y$, and let $z \in \Sigma^*$. Cut the run of $M$ on $\vdash x z \dashv$ at the moments when the head crosses the border between $\vdash x$ and $z \dashv$. The run alternates between pieces inside $\vdash x$ and pieces inside $z \dashv$. A piece inside $z \dashv$ is determined by $z$ and the state in which it starts, and it ends with a move left across the border in some state $p$, or with acceptance, rejection or a loop inside $z \dashv$. A piece inside $\vdash x$ that starts in $p$ ends as $T_x(p)$ says. So, by induction on the number of crossings, the runs on $\vdash x z \dashv$ and $\vdash y z \dashv$ cross the border in the same states, in the same order, and they end in the same way. Hence $xz \in L(M)$ if and only if $yz \in L(M)$.

So the relation $T_x = T_y$ refines the Myhill-Nerode relation of $L(M)$. There are at most $(n + 2)^{n + 1}$ tables, so $L(M)$ has at most that many Myhill-Nerode classes and is regular by the [Myhill-Nerode theorem](/myhill-nerode-theorem/). The DFA whose states are the tables reached from $T_\varepsilon$ accepts $L(M)$: $T_{xa}$ is computed from $T_x$ and $a$ alone, by following the moves on the cell of $a$ and the calls to $T_x$, which terminates or loops within at most $n + 1$ calls, and $x$ is accepted if and only if the run on $\vdash x \dashv$, computed in the same way from $T_x$, accepts. $\square$

For a 2NFA the same proof works with relations instead of functions: $T_x \subseteq (\{\star\} \cup Q) \times (Q \cup \{\mathrm{acc}\})$ records which exits are possible. There are at most $2^{(n + 1)(n + 1)}$ such relations, so 2NFAs also accept only regular languages.

### The cost of removing two-way motion

| conversion | exact number of states in the worst case |
|---|---|
| 2DFA with $n$ states to DFA | $n (n^n - (n - 1)^n)$ |
| 2NFA with $n$ states to NFA | $\binom{2n}{n + 1}$ |

Both values are from Kapoutsis (2005), who also gave exact bounds for the other conversions. The bound for 2DFAs is $2^{\Theta(n \log n)}$, against $2^n$ for removing nondeterminism from one-way automata ([Rabin-Scott theorem](/rabin-scott-theorem/)).

### An example of the savings

Let $L_n$ be the strings over $\{a, b\}$ whose $n$-th symbol from the end is $a$. A one-way DFA needs $2^n$ states. A 2DFA needs only $n + 1$ states that do not accept, plus one accepting state: in state $R$ it moves right over $\vdash$ and all symbols; on $\dashv$ it moves left into state $C_1$. In state $C_i$ with $i < n$ it moves left into $C_{i + 1}$ on each symbol of $\Sigma$, and has no move on $\vdash$, which rejects the strings shorter than $n$. In state $C_n$ it is on the $n$-th symbol from the end, and it moves to the accepting state on $a$ and has no move on $b$ or $\vdash$. On an accepted input of length $\ell$, the run takes $\ell + n + 2$ steps.

### Sweeps and intersections

A 2DFA can check several one-way DFAs in turn: run the first from left to right, walk back to $\vdash$, run the second, and so on. For DFAs with $n_1, \ldots, n_t$ states this needs $O(n_1 + \cdots + n_t)$ states, while a one-way DFA for the intersection can need $n_1 n_2 \cdots n_t$ states (see [regular language intersection](/regular-language-intersection/)). The same idea shows that emptiness of a 2DFA is PSPACE-hard, since emptiness of the intersection of a list of DFAs is; it is in PSPACE, since the tables $T_x$ of polynomial size can be guessed symbol by symbol.

### The Sakoda-Sipser question

Sakoda and Sipser (1978) asked whether every 2NFA with $n$ states has an equivalent 2DFA with a number of states polynomial in $n$. The question is open. The known simulations go through one-way DFAs and cost $2^{O(n^2)}$ states, and the known lower bounds are much smaller. The question is linked to space complexity: a polynomial simulation for 2NFAs that work on short inputs relates to the question whether [deterministic logspace](/logspace/) equals [nondeterministic logspace](/nondeterministic-logspace/).

### Pitfalls

- **Halting.** A 2DFA can loop forever, unlike a one-way DFA. Membership tests must detect a repeated configuration, and the complement is not obtained by swapping accepting and non-accepting states without first making the machine halt on every input.
- **Endmarkers.** Without endmarkers, a 2DFA cannot detect the ends of the input and must keep its head on the input; the class of languages stays the same, but constructions and state counts change.
- **Moves that stay.** Some texts allow a move of $0$ cells. A stationary move can be removed by remembering the move in the state, so the class of languages does not change.

## References
