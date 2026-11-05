---
tag: AR0CS6
kind: model
slug: alternating-finite-automaton
name: Alternating finite automaton
aliases:
- AFA
area: automata-and-parsing/finite-automata
level: advanced
summary: Automaton with existential and universal states; recognizes regular languages with exponentially fewer states.
prereqs: [nondeterministic-finite-automaton, deterministic-finite-automaton, subset-construction]
see_also:
- alternating-turing-machine
- determinization-blowup-lower-bound
- state-complexity
- buchi-automaton
- ltl-to-buchi-translation
- regular-language
- two-way-finite-automaton
- pspace
sources:
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1) (1981)
    locator: pp. 114 to 133 (alternating machines, and alternating finite automata as a special case)
  - paper: doi:10.1016/0304-3975(80)90069-9
    title: Janusz A. Brzozowski and Ernst Leiss, On equations for regular languages, finite automata, and sequential networks, Theoretical Computer Science 10(1) (1980)
    locator: pp. 19 to 35 (Boolean automata and their relation to the reverse language)
  - paper: doi:10.1080/00207169008803893
    title: Abdelaziz Fellah, Helmut Jürgensen and Sheng Yu, Constructions for alternating finite automata, International Journal of Computer Mathematics 35(1-4) (1990)
    locator: pp. 117 to 132 (conversions between AFAs, NFAs and DFAs and their sizes)
  - paper: doi:10.1007/3-540-60915-6_6
    title: Moshe Y. Vardi, An automata-theoretic approach to linear temporal logic, Logics for Concurrency, Lecture Notes in Computer Science 1043 (1996)
    locator: pp. 238 to 266 (alternating automata on words and the translation of LTL)
---

An alternating finite automaton (AFA) generalizes the [NFA](/nondeterministic-finite-automaton/). In an NFA, a state accepts the rest of the input if *some* successor accepts it. In an AFA, each state and symbol give a Boolean condition on the successors, built with "and" as well as "or". So a state can demand that *all* of several successors accept the rest of the input. AFAs accept exactly the [regular languages](/regular-language/), but they can be exponentially smaller than NFAs and doubly exponentially smaller than [DFAs](/deterministic-finite-automaton/). Their decision problems are correspondingly harder: emptiness is [PSPACE](/pspace/)-complete. They are the finite-state case of the [alternating Turing machine](/alternating-turing-machine/), and alternating automata on infinite words are a standard step in model checking of temporal logic.

## The machine

Let $\mathcal{B}^+(Q)$ be the set of *positive Boolean formulas* over $Q$: the formulas built from the elements of $Q$ and the constants $\mathit{true}$ and $\mathit{false}$ with $\wedge$ and $\vee$, without negation. A set $S \subseteq Q$ *satisfies* a formula $\theta$, written $S \models \theta$, if $\theta$ is true when the states in $S$ are set to true and all others to false.

An AFA is a tuple $A = (Q, \Sigma, \delta, q_0, F)$, where $Q$, $\Sigma$, $q_0$ and $F$ are as for a DFA and

$$\delta : Q \times \Sigma \to \mathcal{B}^+(Q).$$

The transition function is total, so the AFA is *complete* in the sense that each pair has a formula, which may be $\mathit{false}$. There are no $\varepsilon$-moves.

**Acceptance.** For each string $w$, define the set $\mathrm{Acc}(w) \subseteq Q$ of the states from which $A$ accepts $w$:

$$\mathrm{Acc}(\varepsilon) = F, \qquad \mathrm{Acc}(a w) = \{ q \in Q : \mathrm{Acc}(w) \models \delta(q, a) \}.$$

$A$ accepts $w$ if $q_0 \in \mathrm{Acc}(w)$, and $L(A) = \{ w : q_0 \in \mathrm{Acc}(w) \}$. Equivalently, an accepting run is a tree whose root is labelled $q_0$, in which a node labelled $q$ at depth $i$ has a set of children that satisfies $\delta(q, a_{i+1})$, and every leaf at depth $|w|$ is labelled by a state of $F$. The definition by $\mathrm{Acc}$ reads the input from right to left; the run tree reads it from left to right.

**Special cases.**

- If every $\delta(q, a)$ is a disjunction $p_1 \vee \cdots \vee p_k$ (with the empty disjunction $\mathit{false}$), then $q \in \mathrm{Acc}(aw)$ if and only if some $p_i \in \mathrm{Acc}(w)$, and $A$ is an NFA with $\delta(q, a) = \{p_1, \ldots, p_k\}$.
- If every $\delta(q, a)$ is a single state, $A$ is a DFA.
- If every formula is a conjunction, $A$ is a *universal* automaton. In the view of states as players, a state whose formulas are disjunctions is *existential* and one whose formulas are conjunctions is *universal*; this is the form of Chandra, Kozen and Stockmeyer (1981).
- A *Boolean* automaton allows arbitrary Boolean formulas, including negation (Brzozowski and Leiss, 1980). The results below hold for both forms, with the same bounds.

**Example: all letters occur.** Let $\Sigma = \{a_1, \ldots, a_k\}$ and $L = \{ w : \text{each } a_i \text{ occurs in } w \}$. An AFA with $k + 1$ states has the states $q_0, s_1, \ldots, s_k$, where $s_i$ means "$a_i$ is still to come", and

$$\delta(s_i, a_i) = \mathit{true}, \qquad \delta(s_i, a_j) = s_i \ (j \neq i), \qquad \delta(q_0, a) = \delta(s_1, a) \wedge \cdots \wedge \delta(s_k, a),$$

with $F = \emptyset$ (for $k \ge 1$). So $s_i \in \mathrm{Acc}(w)$ exactly when $a_i$ occurs in $w$, and $q_0$ accepts $w$ when all of them do. A script checked the language for $k \le 5$ and all strings of length at most $k + 2$.

## What it counts

A run is measured by its input length, and the size of an AFA by its number of states, or by the total size of its formulas. A single step of an AFA can start many copies of the automaton at once, so a run is a tree, not a path, and an algorithm that simulates an AFA pays for this.

- **Membership.** Computing $\mathrm{Acc}$ from the right end of $w$ evaluates each formula once per position, so it takes $O(|w| \cdot |\delta|)$ time, where $|\delta|$ is the total size of the formulas. It needs all of $w$ in advance, or a reversed input.
- **Left-to-right simulation.** Reading the input from the left, a program must remember which Boolean function of $\mathrm{Acc}(\text{rest})$ decides acceptance; there are up to $2^{2^n}$ of them. This is the source of the doubly exponential DFA size.

## Relation to other models

- **NFAs and DFAs.** Both are special cases, as above. In the other direction, every AFA has an equivalent NFA and DFA, by the constructions in the next section.
- **Reversed DFAs.** The sets $\mathrm{Acc}(w)$ change deterministically from right to left. So $L(A)^R$ has a DFA whose states are the subsets of $Q$. Brzozowski and Leiss (1980) and Fellah, Jürgensen and Yu (1990) showed that this is a characterization for Boolean automata: up to the choice of an initial formula in place of $q_0$, a language has an AFA with $n$ states if and only if its reverse has a DFA with $2^n$ states.
- **Alternating Turing machines.** An AFA is an [alternating Turing machine](/alternating-turing-machine/) that only reads its input from left to right and uses no work tape. Two-way alternating finite automata also accept only regular languages (Ladner, Lipton and Stockmeyer, 1984).
- **Automata on infinite words.** Alternating [Büchi automata](/buchi-automaton/) read infinite words. A formula of [linear temporal logic](/linear-temporal-logic/) translates into an alternating Büchi automaton with a number of states linear in the size of the formula, and the exponential cost of the [translation to Büchi automata](/ltl-to-buchi-translation/) then comes only from removing the alternation (Vardi, 1996).

## Known results in the model

Below, $n = |Q|$.

### Size of the conversions

**AFA to DFA for the reverse.** The DFA $D^R$ with the states $2^Q$, start state $F$, transitions $S \xrightarrow{a} \{ q : S \models \delta(q, a) \}$ and accepting states $\{ S : q_0 \in S \}$ accepts $L(A)^R$. *Proof.* By induction on $|w|$, $D^R$ reaches $\mathrm{Acc}(w)$ on the input $w^R$: for $w = \varepsilon$ it is $F$, and on $(aw)^R = w^R a$ it moves from $\mathrm{Acc}(w)$ to $\mathrm{Acc}(aw)$ by the definition. So $D^R$ accepts $w^R$ if and only if $q_0 \in \mathrm{Acc}(w)$. $\square$

**AFA to NFA and DFA.** Reversing the transitions of $D^R$ gives an NFA with $2^n$ states for $L(A)$, and the [subset construction](/subset-construction/) turns it into a DFA with at most $2^{2^n}$ states. The doubly exponential bound for DFAs is reached in the worst case (Chandra, Kozen and Stockmeyer, 1981; Fellah, Jürgensen and Yu, 1990), and the example below shows that the NFA bound is reached up to one state. A script found Boolean automata with 2 states over three letters whose minimal DFA has $2^{2^2} = 16$ states.

**AFAs are exponentially smaller than NFAs.** The language "all letters occur" of the example has an AFA with $k + 1$ states, but every NFA for it has at least $2^k$ states. *Proof.* For $S \subseteq \Sigma$ let $x_S$ list the letters of $S$ and $y_S$ the letters not in $S$, in a fixed order. Each $x_S y_S$ is in $L$. Fix an accepting run of an NFA on each $x_S y_S$, and let $p_S$ be its state after $x_S$. If $p_S = p_T$ for $S \neq T$, say with $a_i \in S \setminus T$, then the first half of the run on $x_T y_T$ and the second half of the run on $x_S y_S$ form an accepting run on $x_T y_S$. But $a_i$ is in neither $T$ nor the complement of $S$, so $x_T y_S \notin L$. Hence the $2^k$ states $p_S$ are distinct. $\square$ The minimal DFA also has $2^k$ states, one for each set of letters seen; a script checked this for $k \le 5$.

### Decision problems

- **Membership** takes $O(|w| \cdot |\delta|)$ time by the definition of $\mathrm{Acc}$.
- **Emptiness, universality, inclusion and equivalence** are PSPACE-complete. They are in [PSPACE](/pspace/) because a counterexample can be guessed one symbol at a time, from the right, while storing only the current set $\mathrm{Acc}(w)$ in $n$ binary digits, and nondeterministic polynomial space equals deterministic polynomial space. They are PSPACE-hard because the emptiness of the intersection of several DFAs, which is PSPACE-complete (Kozen, 1977), is the emptiness of the AFA whose start state has the conjunction of the DFAs' start transitions as its formula.

### Pitfalls

- **Direction of reading.** The natural deterministic simulation of an AFA reads the input backwards. A left-to-right simulation must track Boolean functions, not sets of states, and can need doubly exponential memory.
- **Complement is cheap, but only with duals.** For a positive AFA, the complement is obtained by swapping $\wedge$ with $\vee$, $\mathit{true}$ with $\mathit{false}$, and $F$ with $Q \setminus F$. This takes linear time, unlike the complement of an NFA. Forgetting to swap $F$ gives a wrong result.
- **$\mathit{false}$ and $\mathit{true}$ transitions.** A transition to $\mathit{false}$ rejects at once, like a missing NFA transition, and a transition to $\mathit{true}$ accepts the rest of the input at once. A run tree has a leaf before depth $|w|$ only at a $\mathit{true}$ transition.
- **Counting states.** Some authors count an initial formula instead of a start state, which changes state counts by one, as in the characterization above.

## References
