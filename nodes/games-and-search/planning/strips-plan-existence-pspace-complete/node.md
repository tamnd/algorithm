---
tag: NF2ETY
kind: theorem
slug: strips-plan-existence-pspace-complete
name: Plan existence is PSPACE-complete
aliases:
- PLANSAT
- Bylander's theorem
area: games-and-search/planning
level: advanced
summary: Deciding whether a propositional STRIPS task has a plan is PSPACE-complete (Bylander 1994), even with two positive preconditions per action. Shortest plans can be exponentially long.
prereqs: [strips, pspace, savitch-theorem, turing-machine]
see_also: [bounded-plan-existence-np-complete, tower-of-hanoi, qsat, classical-planning, delete-relaxation, forward-state-space-search, hsp-planner, optimal-planning]
sources:
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: Section 3.1, Theorem 3.1 (PLANSAT is PSPACE-complete) and Corollary 3.2 (two positive preconditions and two postconditions suffice); Section 3 for the restricted cases
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: "Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2) (1970)"
    locator: pp. 177 to 192 (the main theorem, nondeterministic space L(n) in deterministic space L(n)^2, which gives NPSPACE = PSPACE)
  - paper: doi:10.1016/0004-3702(94)00080-K
    title: "Kutluhan Erol, Dana S. Nau and V. S. Subrahmanian, Complexity, decidability and undecidability results for domain-independent planning, Artificial Intelligence 76(1-2) (1995)"
    locator: pp. 75 to 88 (planning with schematic operators and with function symbols; general locator)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 3 (the complexity of classical planning; general locator)
---

Plan existence for propositional [STRIPS](/strips/), called PLANSAT, asks whether a planning task has any plan at all. Bylander (1994) proved that this problem is [PSPACE](/pspace/)-complete. Membership is the easy half: a state is a set of $n$ facts, so a search needs to remember only a few states at a time, and [Savitch's theorem](/savitch-theorem/) turns the guessing of a plan step by step into a deterministic procedure in polynomial space. Hardness comes from the fact that a STRIPS state can hold the whole tape of a [Turing machine](/turing-machine/) that uses polynomial space, and actions can carry out its moves. The hardness survives strong limits on the actions: two positive preconditions per action and a goal of one fact are enough. A second fact, which is part of the reason, is that shortest plans can have $2^n - 1$ actions. So no planner for [classical planning](/classical-planning/) can run in polynomial time in the worst case unless P = PSPACE, and no planner can even write its plan in polynomial time. The version with a bound on the plan length is on [bounded plan existence](/bounded-plan-existence-np-complete/).

## Statement

A *propositional STRIPS task* is $T = (F, A, I, G)$ where $F$ is a finite set of facts with $n = |F|$, $A$ is a finite set of actions, $I \subseteq F$ is the initial state, and the goal $G = (G^+, G^-)$ is a pair of sets of facts that must be true and false. Each action $a$ has positive and negative preconditions $\mathit{pre}^+(a), \mathit{pre}^-(a) \subseteq F$, an add list $\mathit{add}(a)$ and a delete list $\mathit{del}(a)$. A state is a set $s \subseteq F$. The action $a$ is applicable in $s$ when $\mathit{pre}^+(a) \subseteq s$ and $\mathit{pre}^-(a) \cap s = \emptyset$, and then $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. A plan is a sequence of actions, each applicable in the state that the previous ones produce from $I$, that ends in a state $s$ with $G^+ \subseteq s$ and $G^- \cap s = \emptyset$. The size of $T$ is the total number of fact occurrences in its lists.

**PLANSAT.** Given a task $T$, does $T$ have a plan?

**Theorem (Bylander).**

1. PLANSAT is in PSPACE. It can be decided by a deterministic machine in space $O(n^2)$ besides the read-only input.
2. PLANSAT is PSPACE-hard under polynomial-time many-one reductions, even for tasks in which no action has a negative precondition, every action has at most two preconditions, at most two adds and at most two deletes, and the goal is a single positive fact.
3. So PLANSAT is PSPACE-complete, and so is its restriction to positive preconditions and goals, the STRIPS of the encyclopedia.

In addition, if a task has a plan, it has one of at most $2^n - 1$ actions, and this bound is attained: for every $n$ there is a task with $n$ facts whose shortest plan has exactly $2^n - 1$ actions.

## In plain words

A planning task describes a world by $n$ yes or no facts, so it has at most $2^n$ states. Asking whether some goal state can be reached is like asking whether there is a path in a huge graph that is never written down. You can answer it with memory for a few states at a time, by trying midpoints and checking each half of the path the same way. That uses little memory but a lot of time.

You cannot do much better in general. A planning task can copy any computer program that uses a bounded amount of memory: the facts store the memory, and the actions do the program's steps. So a fast planner would also be a fast solver for every such program, which is believed to be impossible.

## Proof

**Lemma 1 (short plans).** If $T$ has a plan, it has one with at most $2^n - 1$ actions.

*Proof.* Take a plan with the fewest actions, $a_1, \ldots, a_k$, with states $s_0 = I, s_1, \ldots, s_k$. If $s_i = s_j$ for some $i < j$, then $a_1, \ldots, a_i, a_{j+1}, \ldots, a_k$ is a shorter plan, because the actions after position $j$ see the same state. So the $k + 1$ states are pairwise distinct subsets of $F$, and $k + 1 \le 2^n$. $\square$

**Lemma 2 (reachability by midpoints).** For states $s, t$ and $i \ge 0$, let $\mathrm{REACH}(s, t, i)$ be true when $t$ can be reached from $s$ by at most $2^i$ actions. Then $\mathrm{REACH}(s, t, 0)$ holds exactly when $s = t$ or some action applicable in $s$ gives $t$, and for $i \ge 1$, $\mathrm{REACH}(s, t, i)$ holds exactly when there is a state $u$ with $\mathrm{REACH}(s, u, i - 1)$ and $\mathrm{REACH}(u, t, i - 1)$.

*Proof.* The case $i = 0$ is the definition with $2^0 = 1$. For $i \ge 1$, if a path from $s$ to $t$ has $\ell \le 2^i$ actions, let $u$ be its state after $\lfloor \ell / 2 \rfloor$ actions; both parts have at most $2^{i-1}$ actions. Conversely two paths of at most $2^{i-1}$ actions each join to one of at most $2^i$ actions. $\square$

**Membership.** By Lemma 1, $T$ has a plan exactly when some state $t$ with $G^+ \subseteq t$ and $G^- \cap t = \emptyset$ has $\mathrm{REACH}(I, t, n)$, since $2^n \ge 2^n - 1$. Decide this by a loop over all $2^n$ candidate states $t$, written as $n$ bits, and a recursive evaluation of REACH by Lemma 2, in which the existential over $u$ is a loop over all $2^n$ states. Each level of the recursion stores $s$, $t$, the current $u$, the level $i \le n$ and a return flag, which is $O(n)$ bits, and the depth is $n$. The base case checks each action against $s$ and $t$ with $O(n)$ extra bits, reading the actions from the input. So the space is $O(n^2)$ besides the input, and the input has size at least $n$ when every fact occurs in it. This places PLANSAT in PSPACE. The same bound follows from a shorter argument: a nondeterministic machine guesses a plan one action at a time and keeps only the current state and a counter up to $2^n$, which is $O(n)$ space; so PLANSAT is in NPSPACE, and NPSPACE = PSPACE by Savitch's theorem. The recursion above is Savitch's proof applied to the state graph.

**The reduction.** Let $L$ be a language in PSPACE. Then there are a deterministic one-tape Turing machine $M = (Q, \Sigma, \delta, q_0, q_{\mathrm{acc}}, \sqcup)$ and a polynomial $p$ with $p(\ell) \ge \max(\ell, 1)$ such that, on every input $w$, $M$ starts in $q_0$ with $w$ in cells $0, \ldots, |w| - 1$, blanks after it and the head on cell 0; it never moves its head outside the cells $0, \ldots, p(|w|) - 1$; and $w \in L$ exactly when $M$ enters $q_{\mathrm{acc}}$. Here $\delta(q, x)$ is a set of moves $(q', y, d)$ with $d \in \{-1, 0, +1\}$, at most one for a deterministic machine. Write $P = p(|w|)$. The task $T(w)$ has these parts.

- Facts: $\mathrm{head}(i, q)$ for $0 \le i < P$ and $q \in Q$ ("the head is on cell $i$ and the state is $q$"), $\mathrm{sym}(i, x)$ for $0 \le i < P$ and $x \in \Sigma$ ("cell $i$ holds $x$"), and one fact $\mathrm{accept}$.
- Initial state: $\mathrm{head}(0, q_0)$, $\mathrm{sym}(i, w_i)$ for $i < |w|$, and $\mathrm{sym}(i, \sqcup)$ for $|w| \le i < P$.
- Goal: the single fact $\mathrm{accept}$.
- For each cell $i$, each pair $(q, x)$ and each move $(q', y, d) \in \delta(q, x)$ with $0 \le i + d < P$, a step action with preconditions $\mathrm{head}(i, q)$ and $\mathrm{sym}(i, x)$, the add list $\{\mathrm{head}(i + d, q')\}$ and the delete list $\{\mathrm{head}(i, q)\}$, and in addition, when $y \ne x$, the add $\mathrm{sym}(i, y)$ and the delete $\mathrm{sym}(i, x)$. When $d = 0$ and $q' = q$, the head fact is left out of both lists.
- For each cell $i$, an accept action with the precondition $\mathrm{head}(i, q_{\mathrm{acc}})$ and the add list $\{\mathrm{accept}\}$.

The task has $P(|Q| + |\Sigma|) + 1$ facts and at most $P (|\delta| + 1)$ actions of constant size. $M$ is fixed, so the size is polynomial in $|w|$, and $T(w)$ can be written in polynomial time. Every action has at most two positive preconditions, at most two adds and at most two deletes, and no negative precondition.

**Encoding of configurations.** A configuration of $M$ on $P$ cells is $C = (q, i, \tau)$ with a state $q$, a head position $i$ and a tape $\tau \in \Sigma^P$. Say that a state $s$ of $T(w)$ *encodes* $C$ when $s \setminus \{\mathrm{accept}\} = \{\mathrm{head}(i, q)\} \cup \{\mathrm{sym}(j, \tau_j) : 0 \le j < P\}$. The initial state encodes the start configuration $C_0$.

**Lemma 3 (one action is one move).** Let $s$ encode $C = (q, i, \tau)$. A step action is applicable in $s$ exactly when it belongs to the cell $i$, the pair $(q, \tau_i)$ and a move $(q', y, d)$ of $M$ that stays inside the cells, and then $s[a]$ encodes the configuration $C'$ that the move produces from $C$. An accept action is applicable in $s$ exactly when $q = q_{\mathrm{acc}}$, and then $s[a]$ encodes $C$ too.

*Proof.* The only head fact of $s$ is $\mathrm{head}(i, q)$, and the only symbol fact of cell $i$ is $\mathrm{sym}(i, \tau_i)$, so the preconditions $\mathrm{head}(i', q'')$ and $\mathrm{sym}(i', x)$ hold exactly when $i' = i$, $q'' = q$ and $x = \tau_i$. The action then replaces $\mathrm{head}(i, q)$ by $\mathrm{head}(i + d, q')$ and, if $y \ne x$, $\mathrm{sym}(i, x)$ by $\mathrm{sym}(i, y)$; if $d = 0$ and $q' = q$, the head fact stays. The result has one head fact, $\mathrm{head}(i + d, q')$, and one symbol fact for each cell, with $y$ in cell $i$: it encodes $C'$. An accept action only adds $\mathrm{accept}$, which the encoding ignores. $\square$

**Lemma 4 (plans are accepting runs).** $T(w)$ has a plan exactly when $M$ accepts $w$.

*Proof.* If $M$ accepts $w$, it has a run $C_0, C_1, \ldots, C_t$ inside the $P$ cells that ends in the state $q_{\mathrm{acc}}$. By Lemma 3 and induction on $t$, the step actions of its moves are applicable in order from $I$ and reach a state that encodes $C_t$. The accept action of the head cell of $C_t$ is then applicable and adds the goal. Conversely, let $a_1, \ldots, a_k$ be a plan. By Lemma 3 and induction, every state on it encodes a configuration that $M$ reaches from $C_0$. The goal fact $\mathrm{accept}$ is not in $I$ and only accept actions add it, and an accept action applies only in a state that encodes a configuration with the state $q_{\mathrm{acc}}$. So $M$ enters $q_{\mathrm{acc}}$ and accepts $w$. $\square$

**Hardness.** The map $w \mapsto T(w)$ is a polynomial-time reduction from $L$ to PLANSAT by Lemma 4, for every $L$ in PSPACE, and its tasks have the restricted form of part 2. With membership, PLANSAT and its positive restriction are PSPACE-complete. Nothing in Lemma 3 or Lemma 4 uses that $M$ is deterministic, so the same construction reduces every language of NPSPACE, which gives the same class.

**The bound $2^n - 1$ is attained.** Take facts $b_0, \ldots, b_{n-1}$ and actions $\mathrm{inc}_k$ for $0 \le k < n$ with preconditions $b_0, \ldots, b_{k-1}$, the add $b_k$, and the deletes $b_0, \ldots, b_{k-1}$, the carry of a binary counter. Let $I = \emptyset$ and $G = \{b_0, \ldots, b_{n-1}\}$, and let $T(n)$ be the length of a shortest plan. The first $n - 1$ facts change only by $\mathrm{inc}_0, \ldots, \mathrm{inc}_{n-2}$, which do not look at $b_{n-1}$, and $b_{n-1}$ is added only by $\mathrm{inc}_{n-1}$ and deleted by no action. A plan must use $\mathrm{inc}_{n-1}$. Before its first use the lower facts go from all false to all true with the lower actions only, which takes at least $T(n - 1)$ actions. After its last use the lower facts are all false and must become all true again, at least $T(n - 1)$ more. So $T(n) \ge 2 T(n - 1) + 1$, and $T(1) = 1$ gives $T(n) \ge 2^n - 1$. Counting in binary from 0 to $2^n - 1$ is a plan of that length, so $T(n) = 2^n - 1$, which meets Lemma 1. $\square$

## Consequences

- **No polynomial planner, unless P = PSPACE.** Every complete planner for STRIPS, such as [forward search](/forward-state-space-search/) or [HSP2](/hsp-planner/), takes more than polynomial time on some tasks, unless P = PSPACE. Heuristics change the typical case, not the worst case.
- **Plans can be exponentially long.** The counter has $n$ facts and needs $2^n - 1$ actions. The [Tower of Hanoi](/tower-of-hanoi/) with $d$ disks has $O(d^2)$ facts and needs $2^d - 1$ moves. A planner that outputs plans must take exponential time on such tasks no matter how P and PSPACE relate; this lower bound is about the length of the output, not about the decision problem.
- **Bounded plans.** With a bound $k$ in binary, the question "is there a plan of at most $k$ actions?" is still PSPACE-complete, since $k = 2^n - 1$ has $n$ binary digits. With $k$ in unary it is NP-complete; see [bounded plan existence](/bounded-plan-existence-np-complete/).
- **Other PSPACE-complete problems.** PLANSAT is interreducible with [QSAT](/qsat/) and with the acceptance problem of polynomial space machines, so methods for one carry over to the other. Planning with multi-valued variables (SAS+) and with ground PDDL is PSPACE-complete by the same arguments.
- **Optimal planning is hard as well.** A cheapest plan solves PLANSAT, so [optimal planning](/optimal-planning/) is PSPACE-hard.
- **Schematic operators.** When the actions are given as schemas over objects, the ground task can be exponentially larger than the input. Erol, Nau and Subrahmanian (1995) show that plan existence then becomes EXPSPACE-complete, and undecidable when function symbols are allowed.

## Tightness

- **The restrictions in part 2 are close to the limit.** Bylander (1994) shows that hardness also holds with two positive preconditions and two postconditions in total per action (Corollary 3.2, with a reduction that splits each move into three actions), and with one postcondition per action and any number of preconditions (Theorem 3.3).
- **Without deletes the problem becomes easy.** If no action has a delete and all preconditions are positive, the reachable facts are found by a fixed point in polynomial time; see [delete relaxation](/delete-relaxation/). With only positive postconditions but negative preconditions allowed, PLANSAT is NP-complete (Bylander, Theorem 3.5), because negative preconditions can force a choice between two facts.
- **Other polynomial cases.** Bylander gives further restrictions under which PLANSAT is polynomial, among them positive preconditions with one postcondition per action (Theorem 3.7), which covers a blocks world encoding, and actions without preconditions (Theorem 3.9).
- **The space bound.** The $O(n^2)$ space of the midpoint recursion is the quadratic overhead of Savitch's theorem. Whether PLANSAT can be decided in space $O(n)$ is open, since it is the question whether the deterministic and the nondeterministic classes for linear space are equal.
- **Lemma 1 is tight**, by the binary counter in the proof.

## History

Chapman (1987) proved that planning with a general action language is undecidable, which turned attention to restricted languages. Bylander (1994) gave the complexity of propositional STRIPS planning in detail: PLANSAT is PSPACE-complete (Theorem 3.1), the problem stays PSPACE-complete under strong syntactic limits, and it is NP-complete or polynomial under others. His membership proof is the nondeterministic one with Savitch (1970), and his hardness proof encodes a polynomial space Turing machine with conditions for the head position and the tape contents, as above. Erol, Nau and Subrahmanian (1995) studied the same questions for planning with schematic operators and function symbols. Later work, for example by Bäckström and Nebel (1995) on SAS+, found further polynomial and NP-complete classes.

## References
