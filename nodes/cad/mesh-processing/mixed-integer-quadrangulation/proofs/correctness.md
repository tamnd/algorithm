---
title: Greedy rounding on the toy grid stops with a feasible integer solution whose energy lies between the relaxed and the rounded energies, and it can miss the optimum
proves: [correctness, termination]
status: full
---

This proof is about the rounding step of MIQ on the toy problem of the page, not about the full method with a cross field, seams and singularities.

**Setting.** There are variables $x_0, \ldots, x_{n-1}$ and terms $(a, b, t)$ with $a \ne b$ and $t$ rational. The energy is $E(x) = \sum (x_b - x_a - t)^2$. The *term graph* has the variables as nodes and an edge for each term; it is connected. A set $P$ of variables is pinned to integers, with $P \ne \emptyset$, and a set $I \supseteq P$ of variables must be integers. The greedy rounding of the page is: solve the relaxed problem with $P$ fixed; then, while some variable of $I$ is not fixed, fix the one whose current value is closest to an integer at that integer and solve again with all fixed variables held.

**Claim.**

1. For any set $S \supseteq P$ of fixed variables with any fixed values, the energy has a unique minimizer over the other variables, and the code computes it exactly.
2. Greedy rounding stops after $|I \setminus P|$ rounds, and the result $x^g$ has $x^g_k \in \mathbb{Z}$ for every $k \in I$ and $x^g_k$ equal to the pin for every $k \in P$.
3. Let $x^r$ be the relaxed minimizer, $x^*$ a minimizer of $E$ with the integer constraints, and $x^d$ the result of rounding all of $I$ at once. Then $E(x^r) \le E(x^*) \le E(x^g)$ and $E(x^*) \le E(x^d)$.
4. If $x^r_k$ is an integer for every $k \in I$, then $x^g = x^r$ and greedy rounding is optimal.
5. Greedy rounding is not optimal in general: the example of the page has $E(x^g) = 9/10 > 1/2 = E(x^*)$.

**Step 1 (part 1).** With the variables in $S$ held, $E$ is $y^\top L y - 2 c^\top y + \text{const}$ in the free variables $y$, where $L$ is the submatrix, on the free rows and columns, of the Laplacian of the term graph (an edge counted once per term). So $y^\top L y = \sum (y_b - y_a)^2$ over the terms, with $y_a = 0$ for a fixed $a$. If $y^\top L y = 0$, every term has $y_b = y_a$, so $y$ is constant on each connected component of the term graph, which is the whole graph, and it is 0 at a fixed variable because $S \ne \emptyset$. So $y = 0$, $L$ is positive definite, and the minimizer is the unique solution of $L y = c$. The entries are rational and Gaussian elimination in exact rational arithmetic returns that solution exactly, with no zero pivot since $L$ is nonsingular.

**Step 2 (part 2).** Each round fixes one variable of $I$ that was not fixed, and no round unfixes one, so after $|I \setminus P|$ rounds the loop stops. A fixed variable keeps its value in every later solve, because the solve of Step 1 changes only the free variables. Each variable of $I \setminus P$ is fixed at an integer, and each variable of $P$ is never changed from its pin.

**Step 3 (part 3).** $x^r$ minimizes $E$ over the set $\{x : x_P = \text{pins}\}$, which contains every point that also has integer values on $I$, so $E(x^r) \le E(x^*)$. $x^g$ and $x^d$ are such points by part 2 (the same argument applies to $x^d$, which fixes all of $I$ at integers and solves once), so $E(x^*) \le E(x^g)$ and $E(x^*) \le E(x^d)$.

**Step 4 (part 4).** If $x^r$ is integer on $I$, the first round fixes a variable at its current value. The minimizer with that value held is still $x^r$, because $x^r$ is the minimizer over a larger set and it satisfies the new constraint. By induction every round keeps $x^r$, so $x^g = x^r$, and $E(x^g) = E(x^r) \le E(x^*)$ gives optimality.

**Step 5 (part 5).** In the example, $E(a, b) = 2(a - 18/5)^2 + 2(b - a - 27/10)^2$ with $a, b$ integers. The relaxed solution is $(18/5, 63/10)$, whose distances to the nearest integers are $2/5$ and $3/10$, so $b$ is rounded first to 6. Then $a = (18/5 + 33/10)/2 = 69/20$ minimizes $(a - 18/5)^2 + (6 - a - 27/10)^2$, and $a$ is rounded to 3. So $E(x^g) = 2(9/25 + 9/100) = 9/10$. The point $(4, 7)$ gives $2(4/25 + 9/100) = 1/2$. $\blacksquare$

**What is not proved.** Greedy rounding has no bound on $E(x^g) / E(x^*)$, and how often it is optimal is only measured: on the 40 random grids of the tests it matched the best integer point in a box around $x^r$ in 35 cases. Minimizing a positive definite quadratic over integer points is the closest vector problem of lattices, which is NP-hard in general, so no fast exact method is expected.
