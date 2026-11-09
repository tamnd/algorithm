---
title: Correctness of Shostak's method for linear arithmetic with uninterpreted functions
proves: [correctness, termination]
status: full
---

We prove that the procedure SHOSTAK of the main page terminates, and that its answer is correct, for the Shostak theory $T$ of linear equations over $\mathbb{Q}$ combined with uninterpreted function symbols. The proof is a simple case of the result of Rueß and Shankar (2001), who proved the method for any convex Shostak theory with uninterpreted functions.

## Setting

A *linear form* is $c_0 + c_1 x_1 + \cdots + c_m x_m$ with rational $c_i$ and distinct variables $x_i$. The canonizer $\mathrm{canon}$ writes a linear form with the variables in a fixed order and drops the zero coefficients. Two linear forms have the same canonical form exactly when they are equal as polynomials, that is, exactly when they have the same value under every assignment of rationals to the variables.

The solver $\mathrm{solve}(p = 0)$ returns $\bot$ if $p$ is a nonzero constant, $\emptyset$ if $p$ is the zero form, and otherwise $\{x = r\}$, where $x$ is a variable of $p$ with coefficient $a \ne 0$ and $r = x - p/a$ does not contain $x$. In each case the result is equivalent to $p = 0$: no assignment satisfies $\bot$ or $1 = 0$, every assignment satisfies $0 = 0$, and $p = 0$ holds exactly when $x = r$ holds.

A *solved form* $S$ is a set of equations $x = r$ where each left side $x$ (a *solitary* variable) occurs once in $S$ and in no right side. $S(p)$ is the result of replacing each solitary variable in $p$ by its right side. If an assignment satisfies $S$, then $p$ and $S(p)$ have the same value under it.

**Abstraction (line L1).** Each application $f(t_1, \ldots, t_n)$ of the input, innermost first, is replaced by a *name* $u$, a fresh variable, and the *definition* $u \mapsto f(a_1, \ldots, a_n)$ is recorded, where $a_i$ is the linear form of the abstracted $t_i$. Two applications with the same symbol and the same canonical arguments get the same name. After this step, every input term is a linear form over the input variables and the names. We write $\Gamma$ for the abstracted equations, $\Delta$ for the abstracted disequations and $D$ for the definitions.

A *model* of the input is an assignment of rationals to the variables together with a function on $\mathbb{Q}^n$ for each $n$-ary symbol $f$. It extends to the names by $u \mapsto$ the value of the application that $u$ names. Under this extension each input term has the value of its abstraction, and every definition $u \mapsto f(\bar a)$ holds: the value of $u$ is $f$ applied to the values of $\bar a$.

## Lemma 1 (invariant of soundness)

*At every point of the run, every model of the input, extended to the names, satisfies $S$.*

*Proof.* At line L2, $S$ is empty. Let a model $M$ satisfy $S$ before line L7, and let $s = t$ be the equation taken at line L4 or L5.

- If it comes from $\Gamma$ (line L4), $M$ satisfies it, because it is an input equation.
- If it comes from line L5, it is $u = v$ for definitions $u \mapsto f(\bar a)$ and $v \mapsto f(\bar b)$ with $\mathrm{canon}(S(a_i)) = \mathrm{canon}(S(b_i))$ for all $i$. In $M$, which satisfies $S$, $a_i$ and $S(a_i)$ have the same value, and so do $b_i$ and $S(b_i)$. So $\bar a$ and $\bar b$ have the same values, and $u$ and $v$, both values of $f$ at these arguments, are equal.

In both cases $M$ satisfies $S(s) = S(t)$, that is, $p = 0$ with $p = S(s) - S(t)$. The solver result $S^*$ is equivalent to $p = 0$, so $M$ satisfies $S^*$. If $S^* = \{x = r\}$, the new solved form is $S^*(S) \cup S^*$: each equation $y = S^*(r_y)$ follows from $y = r_y$ and $x = r$, so $M$ satisfies it. If $S^* = \emptyset$, $S$ does not change. $\square$

**Corollary (UNSAT is correct).** If the procedure returns UNSAT at line L8, the solver returned $\bot$, so no assignment satisfies $p = 0$, and by Lemma 1 no model of the input exists. If it returns UNSAT at line L10, there is $s \ne t$ in $\Delta$ with $\mathrm{canon}(S(s)) = \mathrm{canon}(S(t))$. A model would satisfy $S$, so $s$ and $t$ would have the same value in it, which contradicts $s \ne t$. So no model exists.

## Lemma 2 (invariant of the solved form)

*After an equation $s = t$ has been processed without $\bot$, $\mathrm{canon}(S(s)) = \mathrm{canon}(S(t))$ holds, and stays true until the end of the run.*

*Proof.* Right after line L9, the new solved form $S'$ satisfies $S'(s) - S'(t) = S^*(S(s) - S(t)) = S^*(p)$ as polynomials, because $S$ is idempotent and $S'$ applies $S$ and then $S^*$. If $S^* = \{x = r\}$, then $S^*(p)$ replaces $x$ in $p$ by $x - p/a$, which gives $p - a \cdot p / a = 0$. If $S^* = \emptyset$, then $p$ is already $0$. So $S'(s)$ and $S'(t)$ are equal polynomials. A later step replaces $S'$ by $S''$ with $S''(q) = S^{**}(S'(q))$ for every form $q$. It applies the same substitution to two equal polynomials, so they stay equal. $\square$

## Lemma 3 (termination)

*The loop of lines L3 to L9 runs at most $|\Gamma| + V$ times, where $V$ is the number of variables and names.*

*Proof.* A step that takes its equation from $\Gamma$ happens at most $|\Gamma|$ times. Consider a step that takes $u = v$ at line L5. There $\mathrm{canon}(S(u)) \ne \mathrm{canon}(S(v))$, so $p = S(u) - S(v)$ is not the zero form, and the solver returns $\bot$, which ends the loop, or $\{x = r\}$. In the second case, $x$ occurs in $p$, so it is not solitary in $S$, because $p$ is a combination of right sides of $S$ and non-solitary variables. After the step it is solitary, and a solitary variable stays solitary: later right sides never contain it, so later steps never solve for it. So each such step makes one more variable solitary, and there are at most $V$ of them. New names are made only at line L1, so $V$ does not grow. $\square$

## Theorem (SAT is correct)

*If the procedure returns SAT, the input has a model.*

*Proof.* At line L10 the loop has ended at line L6. So $\Gamma$ has been processed, and no pair of definitions has equal canonical arguments under $S$ and different canonical values. Call the variables that are not solitary in $S$ *free*. Let $P$ be the finite set of the linear forms $\mathrm{canon}(S(q))$, for $q$ any variable, any name, any argument $a_i$ of a definition, and any side of an equation of $\Gamma$ or a disequation of $\Delta$. These forms contain only free variables.

*Step 1: a generic assignment.* Choose rational values for the free variables such that any two distinct forms of $P$ get distinct values. Such values exist. For two distinct forms $p, q \in P$, the difference $p - q$ is a nonzero polynomial of degree at most 1. If it is a nonzero constant, it is never 0. Otherwise its zero set is a hyperplane of $\mathbb{Q}^k$, where $k$ is the number of free variables. A finite union of hyperplanes is not all of $\mathbb{Q}^k$. To see this, take the curve $\{(t, t^2, \ldots, t^k) : t \in \mathbb{Q}\}$. A hyperplane $c_0 + c_1 x_1 + \cdots + c_k x_k = 0$ with some $c_i \ne 0$ meets it in at most $k$ points, because $c_0 + c_1 t + \cdots + c_k t^k$ is a nonzero polynomial in $t$. So finitely many hyperplanes contain only finitely many points of the curve, and any other point of the curve works. (For $k = 0$ there is nothing to choose: then every form of $P$ is a constant, and distinct constants have distinct values.)

Extend the assignment to the solitary variables by $S$: give $x = r$ the value of $r$, which contains only free variables. Then every equation of $S$ holds, and every form $q$ has the value of $\mathrm{canon}(S(q))$.

*Step 2: the functions.* For each definition $u \mapsto f(a_1, \ldots, a_n)$, set $f(\text{values of } a_1, \ldots, a_n) = \text{value of } u$. Let $f$ be $0$ at all other points. This is well defined. Let $u \mapsto f(\bar a)$ and $v \mapsto f(\bar b)$ give the same argument values. The value of $a_i$ is the value of $\mathrm{canon}(S(a_i)) \in P$, and likewise for $b_i$. Distinct forms of $P$ have distinct values, so $\mathrm{canon}(S(a_i)) = \mathrm{canon}(S(b_i))$ for each $i$. As the loop has ended, $\mathrm{canon}(S(u)) = \mathrm{canon}(S(v))$, so $u$ and $v$ have the same value.

*Step 3: the input holds.* By induction on terms, each input term has the value of its abstraction. For an application $f(\bar t)$ with name $u$ and definition $u \mapsto f(\bar a)$, the arguments $\bar t$ have the values of $\bar a$ by induction, and $f$ at these values is the value of $u$ by Step 2. For each equation $s = t$ of $\Gamma$, Lemma 2 gives $\mathrm{canon}(S(s)) = \mathrm{canon}(S(t))$, so both sides have the same value. For each disequation $s \ne t$ of $\Delta$, the test of line L10 failed, so $\mathrm{canon}(S(s))$ and $\mathrm{canon}(S(t))$ are distinct forms of $P$, and they have distinct values. So the assignment and the functions are a model of the input. $\square$

## Conclusion

By Lemma 3 the procedure terminates. By the corollary of Lemma 1 its answer UNSAT is correct, and by the theorem its answer SAT is correct. So SHOSTAK decides satisfiability of conjunctions of literals in linear arithmetic over $\mathbb{Q}$ with uninterpreted functions. With no function symbols, $D$ is empty, line L5 never applies, and the procedure is Algorithm S1 of the Handbook for this theory; the proof then shows that S1 is correct for it.

The proof uses two facts about the theory: its solver is exact (Lemma 1), and its models are rich enough to separate any finite set of distinct canonical forms (Step 1). The second fact implies convexity. For a non-convex Shostak theory, Step 1 fails, and line L10 can miss a conflict among several disequations; the Handbook states that S1 is complete only for convex theories or with at most one disequation. $\blacksquare$
