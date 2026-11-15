---
tag: 131GMK
kind: algorithm
slug: supervision-based-on-place-invariants
name: Supervision based on place invariants
aliases:
- SBPI
- Petri net controller by place invariants
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: "Enforces linear marking constraints L mu <= b on a Petri net by adding one monitor place per constraint, with incidence -L D and initial marking b - L mu0. No reachability graph is built."
model: word-ram
complexity:
  vars: {n: the number of places, q: the number of transitions, c: the number of constraints}
  time: {worst: "O(c n q)"}
  space: {extra: "O(n q + c q)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1996
  people: [Katerina Yamalidou, John O. Moody, Michael D. Lemmon, Panos J. Antsaklis]
  note: "Giua, DiCesare and Silva (1992) introduced monitor places for generalized mutual exclusion constraints. Yamalidou, Moody, Lemmon and Antsaklis gave the construction from place invariants (CDC 1994, Automatica 1996)."
prereqs: [petri-net, discrete-event-system]
see_also: [supervisory-control-theory, supremal-controllable-sublanguage, controllable-language, petri-net-reachability-decidability, invariant-checking, semaphore, mutual-exclusion-problem, state-explosion-problem]
sources:
  - paper: doi:10.1016/0005-1098(95)00103-4
    title: Katerina Yamalidou, John Moody, Michael Lemmon and Panos Antsaklis, Feedback control of Petri nets based on place invariants, Automatica 32(1), 15-28, 1996
    locator: the monitor place construction D_c = -L D and mu_c0 = b - L mu0, and its maximal permissiveness; the conference version is in Proc. 33rd IEEE CDC, 1994, 3104-3109
  - paper: "Alessandro Giua, Frank DiCesare and Manuel Silva, Generalized mutual exclusion constraints on nets with uncontrollable transitions, Proc. IEEE International Conference on Systems, Man and Cybernetics, Chicago, 974-979, 1992"
    locator: generalized mutual exclusion constraints and their monitor places
  - book: isbn:9780792381990
    title: John O. Moody and Panos J. Antsaklis, Supervisory Control of Discrete Event Systems Using Petri Nets, Kluwer Academic Publishers, 1998
    locator: the place invariant method and the admissibility conditions for uncontrollable and unobservable transitions
  - paper: doi:10.1109/5.24143
    title: Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 541-580, 1989
    locator: the incidence matrix, the state equation and place invariants (S-invariants)
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: the chapter on Petri nets and the chapter on supervisory control
---

Supervision based on place invariants (SBPI) builds a supervisor for a [Petri net](/petri-net/) that must keep its marking $\mu$ inside a set of linear constraints $L \mu \le b$. For each constraint it adds one monitor place to the net. The arcs of the monitor places come from the product $-L D$, where $D$ is the incidence matrix of the plant, and their initial tokens are $b - L \mu_0$. The construction makes $L \mu + \mu_c = b$ a place invariant of the closed loop, so the constraint holds on every reachable marking. When the supervisor can disable and observe every transition, the closed loop blocks a firing only if that firing would break a constraint, so the supervisor is maximally permissive. The method needs one matrix product and never builds the reachability graph. This is the main difference from the automaton approach of [supervisory control theory](/supervisory-control-theory/), where the [supremal controllable sublanguage](/supremal-controllable-sublanguage/) is computed on the full state space.

## In plain words

A factory is modeled as a network of places that hold tokens, and of events that move tokens when they occur. Some combinations of tokens are not allowed, for example two robots in the same work cell, or more than three parts in a buffer. Each rule of this kind says that a weighted count of tokens must stay below a limit. The method adds one new place for each rule. This new place holds the "spare capacity" of the rule. An event that uses up capacity must first take tokens from the new place, and an event that frees capacity puts tokens back. When the new place is empty, the events that need it cannot occur. Because the new place always holds the exact spare capacity, it stops exactly the events that would break the rule, and nothing more.

## The problem

Input: a Petri net with $n$ places and $q$ transitions, given by nonnegative integer matrices $\mathrm{Pre}, \mathrm{Post} \in \mathbb{N}^{n \times q}$ ($\mathrm{Pre}_{it}$ is the weight of the arc from place $i$ to transition $t$, and $\mathrm{Post}_{it}$ the weight of the arc from $t$ to $i$), an initial marking $\mu_0 \in \mathbb{N}^n$, an integer matrix $L \in \mathbb{Z}^{c \times n}$ and an integer vector $b \in \mathbb{Z}^c$.

The incidence matrix is $D = \mathrm{Post} - \mathrm{Pre}$. Transition $t$ is enabled at $\mu$ if $\mu \ge \mathrm{Pre}_{\cdot t}$ entrywise, and firing it gives $\mu + D_{\cdot t}$. This is the notation of the [petri-net](/petri-net/) page, with $\mu$ for the marking.

Output: $c$ monitor places, given by $\mathrm{Pre}_c, \mathrm{Post}_c \in \mathbb{N}^{c \times q}$ and an initial marking $\mu_{c,0} \in \mathbb{N}^c$, such that in the closed loop (the plant with the monitor places added):

1. every reachable marking satisfies $L \mu \le b$, and
2. a firing sequence can fire in the closed loop if and only if it can fire in the plant and every marking along it satisfies $L \mu \le b$.

If $L \mu_0 \not\le b$, no supervisor exists, and the output is a report of this fact. Condition 2 assumes that the supervisor can disable and observe every transition; the section on variants treats uncontrollable and unobservable transitions.

## The algorithm

```pseudo id=main
SBPI(Pre, Post, mu0, L, b)
L1  D ← Post - Pre                                ▷ n by q incidence matrix of the plant
L2  D_c ← -L·D                                    ▷ c by q, one row per monitor place
L3  mu_c0 ← b - L·mu0                             ▷ the spare capacity of each constraint
L4  if some entry of mu_c0 < 0 then report "mu0 breaks L mu ≤ b"
L5  Pre_c ← max(0, -D_c); Post_c ← max(0, D_c)    ▷ entrywise
L6  return (Pre_c, Post_c, mu_c0)
```

Line L1 forms the incidence matrix. Line L2 gives the change of each monitor place when each transition fires: it is minus the change of the constrained count $L \mu$. Line L3 gives the initial tokens of the monitors: the slack of each constraint at $\mu_0$. A negative slack means that the initial marking is already illegal (line L4). Line L5 turns the signed incidence into arcs: a negative entry becomes an arc from the monitor to the transition, and a positive entry becomes an arc from the transition to the monitor. The monitors have no self-loops.

The closed loop is the plant with the rows of $\mathrm{Pre}_c$ and $\mathrm{Post}_c$ added below $\mathrm{Pre}$ and $\mathrm{Post}$, and with the initial marking $(\mu_0, \mu_{c,0})$.

## Example

**Mutual exclusion of two processes.** Process 1 cycles $p_1 \to t_1 \to p_2 \to t_2 \to p_1$, and process 2 cycles $p_3 \to t_3 \to p_4 \to t_4 \to p_3$. Places $p_2$ and $p_4$ are the critical sections. The initial marking is $\mu_0 = (1, 0, 1, 0)$: both processes are idle. The rule is that at most one process is in its critical section: $\mu_2 + \mu_4 \le 1$, so $L = [0\ 1\ 0\ 1]$ and $b = 1$.

| Line | Result |
|---|---|
| L1 | $D = \begin{bmatrix} -1 & 1 & 0 & 0 \\ 1 & -1 & 0 & 0 \\ 0 & 0 & -1 & 1 \\ 0 & 0 & 1 & -1 \end{bmatrix}$, columns $t_1, t_2, t_3, t_4$ |
| L2 | $L D = [1\ {-1}\ 1\ {-1}]$, so $D_c = [-1\ 1\ {-1}\ 1]$ |
| L3 | $\mu_{c,0} = 1 - (0 + 0) = 1$ |
| L4 | $1 \ge 0$, so the initial marking is legal |
| L5 | $\mathrm{Pre}_c = [1\ 0\ 1\ 0]$ (arcs to $t_1$ and $t_3$), $\mathrm{Post}_c = [0\ 1\ 0\ 1]$ (arcs from $t_2$ and $t_4$) |

The monitor place is the classic binary [semaphore](/semaphore/): entering a critical section takes its token, and leaving gives it back. The reachable markings, written $(\mu_1, \mu_2, \mu_3, \mu_4 \mid \mu_c)$, are:

| Marking | Plant | Closed loop | Enabled in the closed loop |
|---|---|---|---|
| $(1, 0, 1, 0 \mid 1)$ | reachable | reachable | $t_1$, $t_3$ |
| $(0, 1, 1, 0 \mid 0)$ | reachable | reachable | $t_2$ ($t_3$ is blocked by the empty monitor) |
| $(1, 0, 0, 1 \mid 0)$ | reachable | reachable | $t_4$ ($t_1$ is blocked) |
| $(0, 1, 0, 1)$ | reachable | not reachable | |

The plant reaches 4 markings and the closed loop reaches 3. The only removed marking is the one that breaks the rule, and the only blocked firings are $t_3$ from the second marking and $t_1$ from the third, which lead to it. The invariant $\mu_2 + \mu_4 + \mu_c = 1$ holds in every row.

## Correctness

The key fact is that $L \mu + \mu_c = b$ is a place invariant of the closed loop: when $t$ fires, $L \mu$ changes by $L D_{\cdot t}$ and $\mu_c$ changes by $-L D_{\cdot t}$, and the sum starts at $b$ by line L3. Since a marking is never negative, $\mu_c \ge 0$ gives $L \mu \le b$. For maximal permissiveness, look at one monitor $j$ and one transition $t$. If $(D_c)_{jt} < 0$, the monitor enables $t$ exactly when $\mu_{c,j} + (D_c)_{jt} \ge 0$, and by the invariant this is $L_j(\mu + D_{\cdot t}) \le b_j$. If $(D_c)_{jt} \ge 0$, the monitor never blocks $t$, and the firing cannot raise $L_j \mu$. So the closed loop allows $t$ exactly when the plant allows it and the next marking is legal. An induction on the firing sequence completes the proof. The full proof, with the conditions for uncontrollable and unobservable transitions, is in proofs/correctness.md.

## Complexity

The model is the word RAM, with $n$ places, $q$ transitions and $c$ constraints, and with integer entries of $\mathrm{Pre}$, $\mathrm{Post}$, $L$, $b$ and $\mu_0$ that fit in a word.

- Line L1: $n q$ subtractions.
- Line L2: the product of a $c \times n$ matrix by an $n \times q$ matrix, $c n q$ multiplications and additions.
- Lines L3 to L5: $c n + c + 2 c q$ operations.

The total is $O(c n q)$ time in the worst case. The extra space is $O(n q)$ for $D$ and $O(c q)$ for the monitor arcs. The bound is in the size of the net, not in the size of its reachability graph. The reachability graph of a bounded net can have a number of markings exponential in $n$ (the [state explosion problem](/state-explosion-problem/)), and for an unbounded net it is infinite. Methods that work on the reachability graph, such as the [supremal controllable sublanguage](/supremal-controllable-sublanguage/) on an automaton model, pay that size. The tests on this page build the reachability graph only to check the result.

## Properties

- Exact. All arithmetic is on integers, and the output is the unique monitor with incidence $-L D$.
- Maximally permissive when every transition is controllable and observable (proofs/correctness.md).
- Correct for any net, bounded or not, and for any initial marking that satisfies the constraints. The proof uses only the firing rule and the invariant, not the reachability set.
- The supervisor is itself a Petri net, so the closed loop can be analyzed with the same tools as the plant, for example [invariant checking](/invariant-checking/).
- The method does not ensure liveness or deadlock freedom. The closed loop can deadlock in a legal marking.

## Variants and improvements

- **Uncontrollable transitions.** If $(L D)_{\cdot t} \le 0$, the monitor has no arc into $t$, so it never needs to disable $t$. When this fails for some uncontrollable $t$, the constraint is not admissible as written. Moody and Antsaklis (1998) transform it into a stricter constraint $L' \mu \le b'$ that implies the original one and is admissible. The result may then be less permissive than the best admissible supervisor.
- **Unobservable transitions.** If $(L D)_{\cdot t} = 0$, the monitor has no arc at $t$ at all, so it does not need to see $t$ fire. The same transformation handles the other cases.
- **Generalized mutual exclusion constraints.** Giua, DiCesare and Silva (1992) called the constraints $L \mu \le b$ generalized mutual exclusion constraints (GMECs) and used monitor places for them. They also studied when a set of such constraints is equivalent to a smaller one.
- **Liveness.** Deadlock prevention by monitors, for example with siphons, is a separate problem. It adds further constraints and is not part of this method. See [deadlock](/deadlock/) for the general notion.

## When to use it

Use it when the specification is a set of linear inequalities on the marking: mutual exclusion, buffer capacities, resource counts. It works without the reachability graph, so it scales to nets whose state space is too large to enumerate. When the specification is a regular language or an arbitrary set of forbidden states, it does not apply directly; use the automaton methods of [supervisory control theory](/supervisory-control-theory/) instead. When some transitions are uncontrollable, check the condition $(L D)_{\cdot t} \le 0$ first.

## Pitfalls

- **Wrong sign on line L2.** Writing $D_c = L D$ gives a monitor that gains tokens when the constrained count grows. The invariant is then $L \mu - \mu_c = $ constant, which bounds nothing. The correct line is $D_c = -L D$.
- **Skipping line L4.** If $L \mu_0 \le b$ fails, line L3 gives a negative initial marking, which is not a marking. No supervisor can make an illegal initial state legal, and the code must report it.
- **Uncontrollable transitions with an arc from a monitor.** Line L5 creates an arc from monitor $j$ into $t$ whenever $(L D)_{jt} > 0$. If $t$ is uncontrollable, the supervisor cannot honor this arc. Check the condition from the section on variants before you use the monitor.
- **Building arcs from $L \cdot \mathrm{Pre}$ and $L \cdot \mathrm{Post}$ separately.** A transition that both takes and gives tokens in the constrained count then gets a self-loop on the monitor, and the monitor blocks it even when the net change is zero. Line L5 builds the arcs from the net change $D_c$, which gives the maximally permissive monitor.
- **Expecting liveness.** The mutual exclusion example stays live, but in general the closed loop can deadlock. Check deadlock freedom separately.

## Implementations

## History

Petri nets with place invariants were a standard analysis tool by the 1980s (Murata 1989). Giua, DiCesare and Silva (1992) used monitor places to enforce generalized mutual exclusion constraints on nets with uncontrollable transitions. Yamalidou, Moody, Lemmon and Antsaklis presented the construction from place invariants at the 33rd IEEE CDC in 1994 and in Automatica in 1996. They derived the monitor incidence $D_c = -L D$ from the invariant equation and showed that the result is maximally permissive. Moody and Antsaklis (1998) collected the method, its extensions to uncontrollable and unobservable transitions, and the constraint transformations in a book.

## References
