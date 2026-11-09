---
title: The Fu-Malik algorithm returns an optimal assignment of a partial MaxSAT instance after exactly OPT cores
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. An instance $\varphi = (H, S)$ has a set $H$ of hard clauses and a list $S$ of soft clauses, over some set of variables. For an assignment $x$ that satisfies $H$, $\mathrm{cost}_\varphi(x)$ is the number of clauses of $S$ that $x$ makes false. If $H$ is satisfiable, $\mathrm{OPT}(\varphi)$ is the least cost over the assignments that satisfy $H$. A *core* is a sublist $K$ of $S$ such that $H \cup K$ is unsatisfiable.

**Lemma 1 (one relaxation step).** Let $\varphi = (H, S)$ with $H$ satisfiable, and let $K$ be a core. Form $\varphi' = (H', S')$: take a fresh variable $r_c$ for each $c$ in $K$, replace each $c$ in $K$ by $c \vee r_c$ in $S'$, keep the other soft clauses, and let $H' = H \cup \mathrm{EO}$, where $\mathrm{EO}$ is the CNF of "exactly one of the $r_c$ is true". Then $H'$ is satisfiable and

$$\mathrm{OPT}(\varphi') = \mathrm{OPT}(\varphi) - 1.$$

Moreover, for every assignment $y$ that satisfies $H'$, the restriction $x$ of $y$ to the variables of $\varphi$ satisfies $H$ and $\mathrm{cost}_\varphi(x) \le \mathrm{cost}_{\varphi'}(y) + 1$.

*Proof.* (Upper bound.) Let $x$ satisfy $H$ with $\mathrm{cost}_\varphi(x) = \mathrm{OPT}(\varphi)$. Since $H \cup K$ is unsatisfiable and $x$ satisfies $H$, $x$ makes some clause $c_0$ of $K$ false. Extend $x$ to $y$ by $r_{c_0} = 1$ and $r_c = 0$ for the other $c$ in $K$. Then $y$ satisfies $\mathrm{EO}$, and it satisfies $H$, which does not contain the fresh variables, so it satisfies $H'$; in particular $H'$ is satisfiable. The clause $c_0 \vee r_{c_0}$ is true. For each other $c$ in $K$, $c \vee r_c$ has the value of $c$, and the soft clauses outside $K$ are unchanged. So $\mathrm{cost}_{\varphi'}(y) = \mathrm{cost}_\varphi(x) - 1$, and $\mathrm{OPT}(\varphi') \le \mathrm{OPT}(\varphi) - 1$.

(Lower bound.) Let $y$ satisfy $H'$, and let $x$ be its restriction. Then $x$ satisfies $H$. By $\mathrm{EO}$, exactly one $r_{c_0}$ is true. For every soft clause other than $c_0$, the clause of $\varphi'$ has the same value under $y$ as the clause of $\varphi$ under $x$: outside $K$ they are the same clause, and inside $K$ the added literal $r_c$ is false. Only $c_0$ can be false in $\varphi$ while $c_0 \vee r_{c_0}$ is true. So $\mathrm{cost}_\varphi(x) \le \mathrm{cost}_{\varphi'}(y) + 1$. Taking $y$ optimal for $\varphi'$ gives $\mathrm{OPT}(\varphi) \le \mathrm{OPT}(\varphi') + 1$. $\square$

Only the "at most one" half of $\mathrm{EO}$ is used in the lower bound, and the upper bound holds with or without the "at least one" clause. So both choices are correct.

**Lemma 2 (the oracle and the cores).** The DPLL procedure of the implementation returns a model exactly when its input is satisfiable. The deletion procedure returns a core $K$ that is minimal: $H \cup K$ is unsatisfiable, and removing any one clause makes it satisfiable.

*Proof.* DPLL with unit propagation and chronological backtracking explores, for each decision variable, both values before it backtracks above it, and unit propagation only sets values that every model below the current decisions must have, so it returns "unsatisfiable" only after it has excluded every assignment; a returned assignment satisfies every clause because propagation has checked each clause. For the cores: the procedure starts with all of $S$, which is a core, and removes a clause only when the rest is still unsatisfiable, so the result stays a core. If removing a clause $c$ from the final $K$ made it unsatisfiable, then removing $c$ from the larger set that was current when $c$ was tested would also have given an unsatisfiable set, since a subset of a satisfiable clause set is satisfiable, and $c$ would have been removed. $\square$

**Theorem.** Let $\varphi_0 = (H_0, S_0)$ be the input.
1. If $H_0$ is unsatisfiable, the algorithm returns "no solution" (line L1).
2. Otherwise the loop runs exactly $\mathrm{OPT}(\varphi_0) \le |S_0|$ times through lines L6 to L9, and line L5 returns $(\mathrm{OPT}(\varphi_0), x)$ where $x$ satisfies $H_0$ and $\mathrm{cost}_{\varphi_0}(x) = \mathrm{OPT}(\varphi_0)$.

*Proof.* (1) is line L1 and Lemma 2. For (2), let $\varphi_i$ be the instance after $i$ relaxation steps; line L9 keeps $\mathrm{cost} = i$. By induction with Lemma 1, $H_i$ is satisfiable and $\mathrm{OPT}(\varphi_i) = \mathrm{OPT}(\varphi_0) - i$, as long as line L6 found a core in each earlier round. In round $i$, line L4 asks whether $H_i \cup S_i$ is satisfiable, which holds exactly when $\mathrm{OPT}(\varphi_i) = 0$, that is, when $i = \mathrm{OPT}(\varphi_0)$. If not, $H_i \cup S_i$ is unsatisfiable, so $S_i$ itself is a core, and line L6 finds a core by Lemma 2, so Lemma 1 applies again. Hence the loop ends exactly when $i = \mathrm{OPT}(\varphi_0)$, which is at most $|S_0|$ because no assignment makes more than $|S_0|$ soft clauses false.

At that point line L4 gives a model $y_i$ of $H_i \cup S_i$, so $\mathrm{cost}_{\varphi_i}(y_i) = 0$. Applying the "moreover" part of Lemma 1 $i$ times, the restriction $x$ of $y_i$ to the variables of $\varphi_0$ satisfies $H_0$ and has $\mathrm{cost}_{\varphi_0}(x) \le i = \mathrm{OPT}(\varphi_0)$. By the definition of $\mathrm{OPT}$, equality holds. $\blacksquare$

Minimality of the cores is not needed for correctness: Lemma 1 holds for any core. It only keeps the cardinality constraints small.
