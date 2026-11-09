---
title: Forward chaining returns the least model of a Horn formula, or UNSAT exactly when there is no model
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a Horn formula over $x_1, \ldots, x_n$ with clauses $C_1, \ldots, C_m$. For a clause $C$, its *head* is the variable of its positive literal, if it has one, and its *body* is the list of the occurrences of negative literals $\neg x_v$ in $C$, with repeats. A variable is *entailed* when it is true in each model of $F$. For two assignments, $\alpha \le \beta$ means that each variable true under $\alpha$ is true under $\beta$.

**Invariants.** Each time the test of line L4 runs:

> **(I1)** For each clause $C$, $count[C]$ is the number of occurrences $\neg x_v$ in the body of $C$ with $val[v] = \text{false}$.
>
> **(I2)** Each variable with $val[v] = \text{true}$ is entailed.
>
> **(I3)** The queue holds the clauses with $count[C] = 0$ that have not been taken out by line L5 yet. Each clause has been put in the queue at most once.

*Initialization.* Lines L1 to L3 set each $val[v]$ to false, set $count[C]$ to the size of the body of $C$, and put in the queue exactly the clauses with an empty body. So (I1) and (I3) hold, and (I2) holds because no variable is true.

*Maintenance.* Line L5 takes out a clause $C$. By (I3), $count[C] = 0$, so by (I1) each variable of the body of $C$ is true, and by (I2) each of them is true in each model of $F$. So each model makes each negative literal of $C$ false.

- If $C$ has no head (line L6), then each model of $F$ makes $C$ false. So $F$ has no model, and the answer UNSAT is right.
- Else let $h$ be the head (line L7). Each model makes $C$ true and its negative literals false, so it makes $x_h$ true. So $h$ is entailed, and line L9 keeps (I2).

If line L9 changes $val[h]$ from false to true, then exactly the occurrences of $\neg x_h$ change from "variable false" to "variable true". Lines L10 and L11 decrease the count of their clause by one for each such occurrence, with one entry of the list for each occurrence, so (I1) holds again. If line L8 finds $val[h]$ already true, nothing changes, and (I1) holds.

For (I3): a count only decreases, and by (I1) it never drops below 0. Line L12 puts a clause in the queue when its count reaches 0. A count that is 0 stays 0, so the clause cannot reach 0 a second time. A clause with a count of 0 at the start was put in the queue by line L3 and never by line L12, because line L12 runs only after a decrease. So each clause is put in the queue at most once, and the queue holds the clauses with count 0 that are not yet taken out.

**Termination.** By (I3), each clause is taken out of the queue at most once, so the loop of line L4 runs at most $m$ times. Each run does a finite amount of work, because line L9 sets each variable at most once and the list of line L10 is finite.

**Theorem.** FORWARD-CHAIN$(F)$ stops. It returns UNSAT if and only if $F$ has no model. When it returns $val$, the assignment $val$ is a model of $F$, and $val \le \alpha$ for each model $\alpha$ of $F$. So $val$ is the least model of $F$.

*Proof.* Termination is shown above, and the maintenance step shows that an answer UNSAT at line L6 is right. Now assume that the loop ends at line L13 with an empty queue. Take a clause $C$.

- If $count[C] > 0$, then by (I1) the body of $C$ has an occurrence $\neg x_v$ with $val[v]$ false. This literal is true, so $C$ is true.
- If $count[C] = 0$, then by (I3) $C$ was put in the queue, and since the queue is empty, line L5 took it out. Line L6 did not return, so $C$ has a head $h$. After that step $val[h]$ is true, by line L9 or because it was true before, and no line sets a variable back to false. So $C$ is true.

So $val$ is a model of $F$. By (I2), each variable true under $val$ is true under each model $\alpha$, which is $val \le \alpha$.

If $F$ has no model, the algorithm cannot reach line L13, because there it returns a model. So it returns UNSAT. If $F$ has a model, the answer UNSAT is never given, because the maintenance step shows that UNSAT implies no model. $\blacksquare$

**Corollary.** The models of a satisfiable Horn formula are closed under intersection, and the least model is the intersection of all models. This follows from the theorem: the least model is a model and lies below each model.

**Cost.** Lines L1 to L3 take $\Theta(n + m + |F|)$ time to fill $val$, $count$, the occurrence lists and the queue. Line L5 runs at most $m$ times. The body of lines L10 to L12 runs once for each entry of the list of $h$, and only when $val[h]$ changes, which happens at most once for each $h$. So it runs at most $\sum_h |occ[h]| \le |F|$ times in total. The time is $\Theta(n + m + |F|)$ in the worst case.
