---
tag: T3WXP4
kind: theorem
slug: bounded-plan-existence-np-complete
name: Bounded plan existence is NP-complete
aliases:
- PLANLEN
area: games-and-search/planning
level: advanced
summary: Deciding whether a STRIPS task has a plan of at most k actions is NP-complete when k is in unary or polynomially bounded, and PSPACE-complete when k is in binary.
prereqs: [strips-plan-existence-pspace-complete, np-complete, sat]
see_also: [optimal-planning, satplan, 3-sat, delete-relaxation, cook-levin-theorem, savitch-theorem, h-max-heuristic, classical-planning]
sources:
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: Section 4.1, Theorem 4.1 (PLANMIN is PSPACE-complete), Theorem 4.2 (the reduction from 3SAT to delete-free PLANMIN) and Corollary 4.3 (one positive precondition and one positive postcondition)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 3 (the complexity of classical planning; general locator)
---

Bounded plan existence asks whether a propositional [STRIPS](/strips/) task has a plan of at most $k$ actions, where $k$ is part of the input. Bylander (1994) called this problem PLANMIN. How hard it is depends on how $k$ is written. If $k$ is written in unary, or if it is at most a fixed polynomial in the size of the task, the problem is [NP-complete](/np-complete/): a short plan is a certificate that can be checked quickly, and a reduction from [SAT](/sat/) makes the problem hard even for tasks without deletes in which every action has one precondition and one add. If $k$ is written in binary, a bound such as $2^n - 1$ fits in $n$ digits, and the problem is [PSPACE](/pspace/)-complete like [plan existence](/strips-plan-existence-pspace-complete/) itself. The NP-hard case is the one that matters for [optimal planning](/optimal-planning/) and for planning as satisfiability, because both look for plans of a given length.

## Statement

Use the definitions of the [plan existence page](/strips-plan-existence-pspace-complete/): a task $T = (F, A, I, G)$ with $n = |F|$ facts, actions with positive and negative preconditions, adds and deletes, and a goal of facts that must be true and false. A plan of length $\ell$ has $\ell$ actions.

**PLANLEN.** Given a task $T$ and a natural number $k$, does $T$ have a plan of length at most $k$?

**Theorem.**

1. *(Unary bound.)* If $k$ is written in unary, PLANLEN is NP-complete. The same holds for every version in which $k \le q(|T|)$ for a fixed polynomial $q$, with $k$ written in any way. Hardness holds even for tasks in which the initial state is empty, no action has a delete or a negative precondition, every action has at most one precondition and exactly one add, and the goal is a set of positive facts.
2. *(Binary bound.)* If $k$ is written in binary, PLANLEN is PSPACE-complete.
3. *(Delete-free tasks.)* For tasks without deletes and with only positive preconditions and goals, PLANLEN is NP-complete for both ways of writing $k$.

Bylander proves part 2 and the hardness in part 1 and part 3 (Theorem 4.1, Theorem 4.2 and Corollary 4.3). Membership in NP in part 1 is the plain certificate argument below.

## In plain words

Asking for any plan at all is very hard, because plans can be exponentially long. If you also say "and at most $k$ actions" with a small $k$, the problem gets easier: someone can show you a plan, and you can check it action by action in a short time. That is the class NP.

It is still hard to find such a plan. A logic formula can be turned into a task in which a short plan must pick true or false for each variable once and then satisfy each clause. So a fast planner for short plans would also solve SAT fast. If $k$ is a huge number written in binary, the short plan is not short any more, and the problem is as hard as plan existence.

## Proof

**Membership in NP for a polynomial bound.** A certificate is a sequence of at most $k$ actions of $T$. If $k$ is written in unary, or $k \le q(|T|)$, the certificate has size polynomial in the input. The verifier applies the actions one by one from $I$, checks each precondition, and checks the goal at the end. Each step takes time $O(|T|)$ with $s$ stored as a bit vector, so the check takes time $O(k \, |T|)$, which is polynomial. A task has a plan of length at most $k$ exactly when some certificate passes. $\square$

**The reduction from SAT.** Let $\varphi$ be a CNF formula with the variables $x_1, \ldots, x_m$ and the clauses $c_1, \ldots, c_r$, each clause a nonempty set of literals. Build $T(\varphi)$ as follows.

- Facts: $\mathrm{T}(i)$, $\mathrm{F}(i)$ and $\mathrm{V}(i)$ for $1 \le i \le m$, and $\mathrm{C}(j)$ for $1 \le j \le r$.
- Initial state: $I = \emptyset$. Goal: all $\mathrm{V}(i)$ and all $\mathrm{C}(j)$.
- For each $i$: $\mathrm{setT}(i)$ with no precondition and the add $\mathrm{T}(i)$; $\mathrm{setF}(i)$ with no precondition and the add $\mathrm{F}(i)$; $\mathrm{doneT}(i)$ with the precondition $\mathrm{T}(i)$ and the add $\mathrm{V}(i)$; $\mathrm{doneF}(i)$ with the precondition $\mathrm{F}(i)$ and the add $\mathrm{V}(i)$.
- For each clause $c_j$ and each literal $\lambda \in c_j$: $\mathrm{sat}(j, \lambda)$ with the precondition $\mathrm{T}(i)$ if $\lambda = x_i$ and $\mathrm{F}(i)$ if $\lambda = \neg x_i$, and the add $\mathrm{C}(j)$.
- The bound: $k = 2m + r$, written in unary.

The task has $3m + r$ facts and $4m + \sum_j |c_j|$ actions, so it is built in time linear in the size of $\varphi$, and it has the restricted form of part 1.

**Lemma 1 (a satisfying assignment gives a plan).** If $\varphi$ is satisfiable, $T(\varphi)$ has a plan of length $2m + r$.

*Proof.* Let $\beta$ satisfy $\varphi$. For each $i$, apply $\mathrm{setT}(i)$ and $\mathrm{doneT}(i)$ if $\beta(x_i)$ is true, and $\mathrm{setF}(i)$ and $\mathrm{doneF}(i)$ otherwise. Then for each $j$ pick a literal $\lambda \in c_j$ that $\beta$ makes true, and apply $\mathrm{sat}(j, \lambda)$; its precondition was added in the first part. No action deletes, so every fact stays true once added, and the final state has all $\mathrm{V}(i)$ and all $\mathrm{C}(j)$. The plan has $2m + r$ actions. $\square$

**Lemma 2 (a short plan gives a satisfying assignment).** If $T(\varphi)$ has a plan of length at most $2m + r$, then $\varphi$ is satisfiable.

*Proof.* Fix such a plan. $I$ is empty and each goal fact must be added by some action of the plan. The fact $\mathrm{V}(i)$ is added only by $\mathrm{doneT}(i)$ or $\mathrm{doneF}(i)$, so the plan has at least one done action for each $i$, at least $m$ in total. Each done action of $i$ needs $\mathrm{T}(i)$ or $\mathrm{F}(i)$, which only $\mathrm{setT}(i)$ or $\mathrm{setF}(i)$ add, so the plan has at least one set action for each $i$, at least $m$ in total. The fact $\mathrm{C}(j)$ is added only by sat actions of the clause $j$, so the plan has at least $r$ sat actions. These three groups of actions are disjoint and give at least $2m + r$ actions. With the bound, each count is exact, and in particular each $i$ has exactly one set action. Let $\beta(x_i)$ be true if it is $\mathrm{setT}(i)$ and false if it is $\mathrm{setF}(i)$. Then $\mathrm{T}(i)$ is true at some point of the plan exactly when $\beta(x_i)$ is true, and $\mathrm{F}(i)$ exactly when it is false. For each $j$ the plan applies some $\mathrm{sat}(j, \lambda)$, whose precondition holds at that point, so $\beta$ makes $\lambda$ true, and $\beta$ satisfies $c_j$. $\square$

**Hardness for a unary bound.** By Lemmas 1 and 2, $\varphi \mapsto (T(\varphi), 2m + r)$ is a polynomial-time reduction from SAT, which is NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/), to PLANLEN with a unary bound, and also to the delete-free version of part 3. The bound $2m + r$ is less than the size of the task, so the reduction also works for every version with $k \le q(|T|)$. With membership, part 1 follows. $\square$

**Membership in PSPACE for a binary bound.** First, if $k \ge 2^n - 1$, a plan of length at most $k$ exists exactly when any plan exists, because a shortest plan has at most $2^n - 1$ actions (Lemma 1 of the [plan existence page](/strips-plan-existence-pspace-complete/)); decide PLANSAT in space $O(n^2)$. Otherwise $k < 2^n$, so $k$ has at most $n$ bits. Let $\mathrm{R}(s, t, \ell)$ be true when $t$ can be reached from $s$ by at most $\ell$ actions. Then $\mathrm{R}(s, t, 0)$ means $s = t$, $\mathrm{R}(s, t, 1)$ means $s = t$ or $t = s[a]$ for some applicable $a$, and for $\ell \ge 2$, $\mathrm{R}(s, t, \ell)$ holds exactly when some state $u$ has $\mathrm{R}(s, u, \lceil \ell / 2 \rceil)$ and $\mathrm{R}(u, t, \lfloor \ell / 2 \rfloor)$, by the same splitting of a path at its middle state as for PLANSAT. The recursion halves $\ell$, so its depth is at most $\lceil \log_2 k \rceil + 1 \le n + 1$, and each frame stores three states and a number below $2^n$, which is $O(n)$ bits. A loop over the goal states $t$ with $\mathrm{R}(I, t, k)$ decides PLANLEN in space $O(n^2)$. $\square$

**Hardness for a binary bound.** Map a task $T$ with $n$ facts to $(T, 2^n - 1)$. The number $2^n - 1$ has $n$ binary digits, so the map takes polynomial time, and by Lemma 1 of the plan existence page, $T$ has a plan exactly when it has one of length at most $2^n - 1$. PLANSAT is PSPACE-hard, so PLANLEN with a binary bound is PSPACE-hard, and with membership it is PSPACE-complete. $\square$

**Delete-free tasks.** Let $T$ have no deletes and only positive preconditions and goals. If $T$ has a plan, it has one of at most $n$ actions: in a shortest plan every action adds a fact that is not yet true, since otherwise the action changes nothing and can be removed, and no fact is ever deleted. So PLANLEN on such tasks equals PLANLEN with the bound $\min(k, n)$, which is at most $n$ for $k$ in any notation; the certificate argument puts it in NP, and the SAT reduction above is delete-free. So part 3 holds. $\square$

## Consequences

- **Optimal planning is NP-hard, even without deletes.** A planner that finds a plan of minimum length also decides PLANLEN, so [optimal planning](/optimal-planning/) is NP-hard on delete-free tasks. In particular the optimal delete relaxation heuristic $h^+$ of [delete relaxation](/delete-relaxation/) is NP-hard to compute. This is why practical planners use the polynomial estimates [h-max](/h-max-heuristic/) and [h-add](/h-add-heuristic/) in place of $h^+$.
- **Planning as satisfiability.** For a fixed $k$ in unary, the question "is there a plan of length at most $k$?" can be written as a propositional formula of size polynomial in $|T|$ and $k$. [SATPLAN](/satplan/) does this for $k = 0, 1, 2, \ldots$ and calls a SAT solver; the theorem shows that this is a reduction between problems of the same class for each fixed polynomial bound.
- **Length is what moves the problem between classes.** Plan existence is PSPACE-complete because plans can be exponentially long. Any limit that keeps the plans of interest polynomially short puts the problem in NP.
- **Costs.** With positive integer action costs and a cost bound $k$ in unary in place of a length bound, a plan of cost at most $k$ has at most $k$ actions, so the same proofs work. With unit costs the two problems are the same. Actions of cost 0 break the certificate argument, since a cheap plan can then be exponentially long.

## Tightness

- **The unary bound is needed for NP.** With $k$ in binary the problem is PSPACE-complete by part 2, so it is not in NP unless NP = PSPACE. The binary counter task of the plan existence page has $n$ facts and the shortest plan of length $2^n - 1$, so a certificate can be exponentially long.
- **The reduction uses very weak actions.** One precondition and one add per action, no deletes and an empty initial state already give NP-hardness. Without any preconditions, a shortest plan of a delete-free task picks, for each goal fact, an action that adds it, which is the [set cover](/set-cover/) problem and so still NP-hard.
- **A constant bound is easy.** For a fixed constant $k$, a search over all sequences of at most $k$ actions takes time $O(|A|^k \, k \, |T|)$, which is polynomial. The hardness needs $k$ to grow with the input.
- **Hardness for 3-CNF.** The reduction works for every CNF formula, so it also works for [3-SAT](/3-sat/), which is the source problem that Bylander uses.

## History

Bylander (1994) defined PLANMIN, the question whether a STRIPS task has a plan of at most $k$ operators, in the same paper in which he proved PLANSAT PSPACE-complete. He showed that PLANMIN is PSPACE-complete in general (Theorem 4.1), and that it is NP-complete for the restricted classes in which shortest plans are short, with a reduction from 3SAT to tasks with positive preconditions and positive postconditions (Theorem 4.2 and Corollary 4.3). The construction above, with the facts for true, false, done and clause, follows his reduction. The NP-completeness of the version with a unary bound is a standard remark of later texts and follows from the certificate argument. Kautz and Selman's planning as satisfiability, and later SAT and constraint encodings of planning, rest on this view of bounded planning as a problem in NP.

## References
