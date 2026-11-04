---
tag: TFE5WF
kind: concept
slug: inductive-invariant
name: Inductive invariant
aliases:
- Inductive invariant of a transition system
area: foundations/correctness-and-invariants
level: advanced
summary: An invariant that holds initially and is preserved by every transition, so it holds in all reachable states.
prereqs: [invariant, induction]
see_also: [loop-invariant, floyd-inductive-assertions, hoare-logic, partial-correctness, assertion, abstract-interpretation]
sources:
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32, the method of inductive assertions on flowcharts
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10), 1969
    locator: the rule of iteration for the while statement
  - book: Zohar Manna and Amir Pnueli, The Temporal Logic of Reactive and Concurrent Systems, Specification, Springer (1992)
    locator: the invariance rule for safety properties of transition systems
---

An inductive invariant of a transition system is a set of states that contains all initial states and is closed under every transition. Each state that a run can reach is in this set, so the set is an [invariant](/invariant/). The converse is false: an invariant can be true in all reachable states and still fail the closure test. The proof of the closure test is a proof by [induction](/induction/) on the length of the run, which is why the closure test is the standard way to prove an invariant. The [loop invariant](/loop-invariant/) of a program loop is the most common case.

## In plain words

A system starts in some state and moves from state to state. You want to show that it never enters a bad state.

So you describe a set of safe states, and you check two things. First, the system starts inside the set. Second, one step from any state in the set always lands inside the set. If both checks pass, the system never leaves the set.

The second check does not ask if the system can really reach a state. So a rule that is true for every run can still fail the check. The rule may allow a state that the system never reaches, and one step from that state may leave the rule. Then you make the rule stronger, until every step from every allowed state stays inside.

## The idea

**Setting.** A *transition system* has a set $\Sigma$ of states, a set $I \subseteq \Sigma$ of initial states, and a relation $\to$ on $\Sigma$. The relation $s \to t$ means that the system can move from $s$ to $t$ in one step. A state $s$ is *reachable* when there are states $s_0, s_1, \dots, s_k$ with $s_0 \in I$, $s_i \to s_{i+1}$ for $0 \le i < k$, and $s_k = s$, for some $k \ge 0$. Let $R$ be the set of reachable states. A set $P \subseteq \Sigma$ is an *invariant* when $R \subseteq P$.

**Definition.** A set $P \subseteq \Sigma$ is an *inductive invariant* when

1. *Initiation:* $I \subseteq P$.
2. *Consecution:* for all $s, t \in \Sigma$, if $s \in P$ and $s \to t$, then $t \in P$.

**Theorem.** Each inductive invariant is an invariant.

*Proof.* Let $P$ be inductive. Show by induction on $k$ that each state reachable by a run with $k$ steps is in $P$. For $k = 0$, the state is in $I$, and $I \subseteq P$ by initiation. Assume the claim for $k$, and take a run $s_0, \dots, s_{k+1}$ from $I$. The state $s_k$ is in $P$ by the induction hypothesis, and $s_k \to s_{k+1}$, so $s_{k+1} \in P$ by consecution. $\square$

**The converse is false.** An invariant need not satisfy consecution. A failure of consecution is a pair $s \to t$ with $s \in P$ and $t \notin P$. It is called a *counterexample to induction*. If $P$ is an invariant, then $s$ is not reachable, because if $s$ were reachable then $t$ would be reachable and so in $P$. So each counterexample to induction starts in a state that the system never reaches.

**Strengthening.** To prove that a property $Q$ is an invariant, search for an inductive invariant $P$ with $P \subseteq Q$. Then $R \subseteq P \subseteq Q$. This is called *strengthening*: the proof of $Q$ goes through a smaller set $P$. Three facts help:

- The set $R$ of reachable states is itself inductive. So a strengthening always exists, and $R$ is the smallest one: each inductive invariant $P$ contains $R$ by the theorem above. But $R$ is usually a complicated set.
- The intersection of two inductive invariants is an inductive invariant, and so is the union.
- A counterexample to induction $s \to t$ for $Q$ tells you what to add. The added condition must be true in all reachable states and false in $s$. Then $s$ is excluded.

An inductive invariant proves a *safety* property: nothing bad happens. It does not prove that the system makes progress, or that it stops. For progress and termination you need a [variant function](/variant-function/) or another argument.

**Programs.** For a loop $\mathbf{while}\ B\ \mathbf{do}\ S$, take the states to be the values of the variables, and take $s \to t$ when $B$ is true in $s$ and the body $S$ takes $s$ to $t$. The initial states are the states at the first test. A [loop invariant](/loop-invariant/) is an inductive invariant of this system: initialization is initiation, and maintenance is consecution. This is the premise of the rule of iteration in [Hoare logic](/hoare-logic/). In the method of [Floyd](/floyd-inductive-assertions/), one assertion is attached to each cut point of a flowchart, and the consecution test is done for each path between cut points.

## Examples

**A true invariant that is not inductive.** Let the states be the integers, $I = \{0\}$, and $x \to x + 2$ when $x < 10$. The reachable states are $0, 2, 4, 6, 8, 10$.

- $Q_1$: $x \ne 5$ is an invariant, because $5$ is not reachable. It is not inductive: $3 \in Q_1$ and $3 \to 5$, and $5 \notin Q_1$. The state $3$ is unreachable.
- $Q_2$: $x \le 10$ is an invariant. It is not inductive: $9 \in Q_2$ and $9 \to 11$, and $11 \notin Q_2$.
- $P$: $x$ is even and $x \le 10$ is inductive. Initiation: $0$ is even and $0 \le 10$. Consecution: if $x$ is even, $x \le 10$ and $x < 10$, then $x \le 8$, so $x + 2$ is even and $x + 2 \le 10$.
- $P$ implies both $Q_1$ and $Q_2$, because an even number is not $5$. So $P$ is a strengthening for both properties. The counterexample $9 \to 11$ for $Q_2$ leads to the added condition "$x$ is even", which excludes $9$.

**The loop invariant of ISQRT.** The program ISQRT is on the page for [correctness](/correctness/). Fix $n \ge 0$. The states are the pairs $(lo, hi)$, the initial state is $(0, n + 1)$, and $(lo, hi) \to (lo', hi')$ when $hi - lo > 1$ and one body step gives $(lo', hi')$, where $mid = lo + \lfloor (hi - lo)/2 \rfloor$. Let $P$ be $0 \le lo < hi \wedge lo^2 \le n < hi^2$. Initiation: $0 < n + 1$, and $0 \le n < (n+1)^2$ for $n \ge 0$. Consecution: when $hi - lo \ge 2$, then $lo < mid < hi$. If $mid^2 \le n$, the new pair is $(mid, hi)$, and it satisfies $P$. Otherwise the new pair is $(lo, mid)$, and $n < mid^2$ gives $P$. This is a test for all states in $P$ and not only the reachable ones, and so $P$ is inductive. At exit, $hi = lo + 1$, so $P$ gives $lo^2 \le n < (lo+1)^2$.

**Non-examples.**

- $x$ is odd is not an invariant of the first system, because $0 \in I$ is even. It fails initiation.
- The set $\{0, 2, 4, 6, 8\}$ satisfies initiation, and it is not closed: $8 \to 10$ leaves it. It is not an invariant either, because $10$ is reachable.

## Where it is used

- *Program verification.* The loop invariants of [Hoare logic](/hoare-logic/) and the assertions of [Floyd's method](/floyd-inductive-assertions/) are inductive invariants. A verifier asks the user for them, or infers them, and then checks initiation and consecution with a prover.
- *Reactive and concurrent systems.* Safety properties of a system with many processes are proved with an invariant that is inductive over the transitions of all the processes. Manna and Pnueli call the rule the invariance rule.
- *Static analysis.* A tool for [abstract interpretation](/abstract-interpretation/) computes a set of states that is closed under the transitions, and it takes it as an inductive invariant.

## References
