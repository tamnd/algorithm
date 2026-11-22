---
title: Reluplex terminates, a SAT answer is a solution, and an UNSAT answer is a proof
proves: [correctness]
status: full
---

A query has variables $x_1, \dots, x_n$, a tableau $T$ in which each basic variable $x_i$ equals $\sum_j a_{ij} x_j$ over the non-basic variables, bounds $l_j \le x_j \le u_j$ (either may be absent), and a set $R$ of pairs $(b, f)$ with the constraint $f = \max(0, b)$. A solution is an assignment that meets all equations, bounds and pairs. Arithmetic is exact. We assume that the start assignment $\beta$ meets every equation, which holds for the encoding of the page, since every basic variable is computed from its row.

**Lemma 1 (the equations stay true).** Every step of RELUPLEX and SPLIT keeps $\beta$ a solution of all equations of the current tableau, and the tableaux before and after a pivot have the same solutions.

*Proof.* UPDATE$(x_j, v)$ changes the non-basic $x_j$ by $\delta = v - \beta(x_j)$ and each basic $x_i$ by $a_{ij}\delta$, so each row $x_i = \sum_j a_{ij} x_j$ stays true. PIVOT-AND-UPDATE first does the same with $\theta = (v - \beta(x_i))/a_{ij}$ for the non-basic $x_j$, then pivots. A pivot solves the row of $x_i$ for $x_j$ (possible because $a_{ij} \ne 0$) and substitutes the result into the other rows. These are equivalent rewritings of the same linear system, so they have the same solutions and $\beta$ stays one. Line L17 adds a new basic variable $e$ whose row is the row of $f$ minus the row of $b$, written in the current non-basic variables, and sets $\beta(e)$ from it, so the new row holds. Changes of bounds do not touch the equations. $\square$

**Lemma 2 (SAT is a solution).** If RELUPLEX returns at line L14, $\beta$ is a solution of the current query. If SPLIT returns SAT, the returned assignment, restricted to the variables of its input query, is a solution of that query.

*Proof.* Line L14 is reached only when no non-basic variable (line L3) and no basic variable (line L5) is out of its bounds and no pair is broken (line L9). With Lemma 1, $\beta$ meets all equations, all bounds and all pairs of $R$.

For SPLIT, let $p = (b, f)$. The branch of line L15 has the bounds of the input query, made tighter, and the pairs $R - \{p\}$. A solution of it also has $b \le 0$ and $f = 0$, so $f = \max(0, b)$ and $p$ holds as well. The branch of line L17 adds the variable $e = f - b$ fixed to $0$, and the bound $b \ge 0$; a solution of it has $f = b \ge 0$, so again $f = \max(0, b)$. In both cases the other equations and bounds of the input query are among those of the branch, so dropping $e$ leaves a solution of the input query. By induction on the depth of the recursion, every SAT answer is a solution of the query at the top. $\square$

**Lemma 3 (the simplex failure is a proof).** If line L7 returns UNSAT, the current query has no solution, not even without the pairs.

*Proof.* Line L5 is reached only when every non-basic variable is within its bounds, since line L3 comes first. Say that the basic $x_i$ is below its lower bound, $\beta(x_i) < l_i$ (the other case is symmetric). No candidate exists at line L6, so every non-basic $x_j$ with $a_{ij} > 0$ has $\beta(x_j) = u_j$ (it has an upper bound and is at it), and every non-basic $x_j$ with $a_{ij} < 0$ has $\beta(x_j) = l_j$. Take any assignment $\gamma$ that meets the bounds and the equations. Then
$$\gamma(x_i) = \sum_j a_{ij}\gamma(x_j) \le \sum_{a_{ij} > 0} a_{ij} u_j + \sum_{a_{ij} < 0} a_{ij} l_j = \sum_j a_{ij}\beta(x_j) = \beta(x_i) < l_i,$$
so $\gamma$ breaks the lower bound of $x_i$. Hence no assignment meets the equations and the bounds. $\square$

**Lemma 4 (the split covers every solution).** Let $p = (b, f) \in R$. Every solution of the query is a solution of the branch of line L15 or, after setting $e = f - b$, of the branch of line L17.

*Proof.* Let $\gamma$ be a solution, so $\gamma(f) = \max(0, \gamma(b))$. If $\gamma(b) \le 0$, then $\gamma(f) = 0$, so $\gamma$ meets $b \le 0$ and $0 \le f \le 0$ together with the old bounds, which are the bounds of line L15; it meets the pairs $R - \{p\}$ and the equations. If $\gamma(b) > 0$, then $\gamma(f) = \gamma(b)$, so $\gamma(e) = 0$ and $\gamma$ meets $b \ge 0$ and $0 \le e \le 0$, the bounds of line L17. The row of $e$ is the row of $f$ minus the row of $b$, so it holds for any assignment that meets the other equations. $\square$

**Lemma 5 (termination).** For $\tau \ge 1$, every call of RELUPLEX returns.

*Proof.* By induction on $|R|$. Consider one call. Between two executions of lines L9 to L13 (or before the first one), the loop runs lines L3 to L8 only. Line L4 puts one non-basic variable on a bound, and lines L5 to L8 never move a non-basic variable out of its bounds: PIVOT-AND-UPDATE puts $x_i$, which becomes non-basic, on a bound, and changes no other non-basic variable. So line L4 runs at most $n$ times in a row, after which lines L5 to L8 are the simplex procedure of Dutertre and de Moura with Bland's rule, the least index both for the variable to fix and for the variable to pivot with. That procedure terminates (the theorem of the simplex for SMT page), so this stretch of the loop ends at line L7, at line L14, or at line L9.

Each time line L11 runs, the counter of one pair grows by one, and line L10 splits as soon as a counter reaches $\tau$. Lines L12 and L13 run only after line L11. So line L11 runs at most $\tau |R|$ times in one call, and after that the call returns at line L7, line L10 or line L14. A split at line L10 makes two calls, each with $|R| - 1$ pairs, which return by the induction hypothesis (with $R = \emptyset$, line L9 never fires and the call is a plain simplex run, which terminates). $\square$

**Theorem.** For $\tau \ge 1$, RELUPLEX terminates. If it returns SAT, the assignment is a solution of the query. If it returns UNSAT, the query has no solution. So for a network query, SAT gives an input in the region that meets the output condition, and UNSAT proves that no such input exists.

*Proof.* Termination is Lemma 5, and the SAT case is Lemma 2. For UNSAT, use induction on the depth of the recursion. An UNSAT answer comes from line L7, which is a proof by Lemma 3 (a query without solutions of its linear part has no solutions at all), or from line L10, where both branches of SPLIT returned UNSAT. By the induction hypothesis neither branch has a solution, so by Lemma 4 the query has none. Lemma 1 shows that the tableau of each call has the same solutions as the query it was given. For a network query, the encoding has one equation per hidden unit and one for the output, the input bounds of the region, and one pair per ReLU, so its solutions are exactly the inputs of the region that meet the output condition, together with the values of the hidden units. $\blacksquare$
