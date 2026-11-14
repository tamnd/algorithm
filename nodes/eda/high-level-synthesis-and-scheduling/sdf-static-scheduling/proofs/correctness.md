---
title: Correctness of static SDF scheduling
proves: [correctness]
status: full
---

We use the notation of the page. The graph is connected, with actors $1, \ldots, n$ and edges $e = (a, b)$ with rates $p_e, c_e \ge 1$ and $d_e \ge 0$ initial tokens. After an admissible sequence in which actor $a$ fires $x_a$ times, the token count of edge $e$ is $d_e + p_e x_a - c_e x_b$ (for a self loop, $d_e + (p_e - c_e) x_a$), whatever the order of the firings. We write this as $d + \Gamma x$.

## Lemma 1 (the repetition vector)

If line L2 passes, the vector $q$ of line L3 has positive integer entries with gcd 1, and the integer solutions of $\Gamma x = 0$ are exactly the multiples of $q$. If line L2 fails, $\Gamma x = 0$ has no solution other than $x = 0$, and no PASS exists.

*Proof.* Let $\Gamma x = 0$ with $x$ real. The row of a tree edge $e = (a, b)$ says $p_e x_a = c_e x_b$, so the walk of line L1 forces $x = x_1 \cdot y$, where $y$ is the vector of line L1 with $y_1 = 1$; every entry of $y$ is a positive rational. If some edge fails line L2, then $y$ is not a solution, so only $x_1 = 0$ is, and $x = 0$. A PASS with counts $x$ ends in the state $d + \Gamma x = d$, so $\Gamma x = 0$ with $x \ne 0$; hence no PASS exists. If every edge passes, $y$ is a solution, and the solutions are its real multiples. Line L3 makes the entries integers with gcd 1. An integer solution $x = r q$ with $r = u / v$ in lowest terms has $v \mid u q_a$, so $v \mid q_a$ for all $a$, so $v = 1$. $\square$

## Lemma 2 (the simulation is admissible)

Every firing that line L8 makes is enabled, and no actor fires more than $q_a$ times.

*Proof.* Line L7 checks both conditions just before line L8 fires $a$. $\square$

## Lemma 3 (the queue misses nothing)

When the loop of lines L5 to L10 ends, no actor $a$ has $\mathrm{count}_a < q_a$ and is enabled.

*Proof.* We show that at the start of each iteration of the loop, every actor that has $\mathrm{count}_a < q_a$ and is enabled is in $W$. At the start, $W$ holds every actor. Consider one iteration that pops $a$.

- If $a$ does not fire, then $a$ is not enabled or has reached its count, and nothing else changes, so the claim still holds.
- If $a$ fires, the tokens change only on the edges at $a$. An actor $b \ne a$ that was not enabled can become enabled only if one of its input edges gains tokens, so it reads an output edge of $a$, and line L10 pushes it. Taking tokens from the input edges of $a$ can disable $a$ but no other actor, because each edge has exactly one reader. The count changes only for $a$, which line L10 pushes too.

When $W$ is empty, the claim says that no actor is enabled with $\mathrm{count}_a < q_a$. $\square$

## Lemma 4 (a PASS can be cut to counts q)

If a PASS exists, then there is an admissible sequence in which each actor $a$ fires exactly $q_a$ times.

*Proof.* Let $\sigma$ be a PASS. By Lemma 1 its counts are $J q$ for an integer $J \ge 1$. Let $\sigma'$ be $\sigma$ with every firing of $a$ after the $q_a$-th one deleted, for each actor $a$. Take a firing in $\sigma'$, the $k$-th of actor $b$ with $k \le q_b$, and an input edge $e = (a, b)$ of $b$ with $a \ne b$. Let $m$ be the number of firings of $a$ before it in $\sigma$; in $\sigma'$ the number is $\min(m, q_a)$. In $\sigma$ the firing was enabled, so $d_e + p_e m - c_e (k - 1) \ge c_e$. If $m \le q_a$, the count in $\sigma'$ is the same. If $m > q_a$, the count in $\sigma'$ is
$$d_e + p_e q_a - c_e (k - 1) \ge p_e q_a - c_e (q_b - 1) = c_e,$$
using $k \le q_b$ and the balance equation $p_e q_a = c_e q_b$. For a self loop, the balance equation gives $p_e = c_e$, so the count is $d_e$ at every firing of $b$ in both sequences. So every firing of $\sigma'$ is enabled, and $\sigma'$ has the counts $q$. $\square$

## Theorem

The algorithm returns "inconsistent" exactly when the balance equations have no positive solution, and then no PASS exists. Otherwise it returns a PASS whenever one exists, and reports a deadlock only when none exists.

*Proof.* The first sentence is Lemma 1. Suppose line L2 passes. If line L11 finds $\mathrm{count} = q$, then by Lemma 2 seq is admissible, every actor fires $q_a \ge 1$ times, and the final state is $d + \Gamma q = d$, so seq is a PASS.

Now suppose a PASS exists but the simulation stops with counts $x \ne q$, where $x \le q$ by Lemma 2. By Lemma 4 there is an admissible sequence $\sigma'$ with counts exactly $q$. Since $x \ne q$, some firing of $\sigma'$ is the $k$-th firing of an actor $b$ with $k > x_b$. Let it be the first such firing in $\sigma'$. Then $k = x_b + 1 \le q_b$, so $\mathrm{count}_b = x_b < q_b$ at the end of the simulation. Before this firing, $\sigma'$ has fired each actor $a$ at most $x_a$ times, by the choice of the first such firing. For an input edge $e = (a, b)$ with $a \ne b$, the firing is enabled in $\sigma'$, so with $m \le x_a$ earlier firings of $a$,
$$c_e \le d_e + p_e m - c_e x_b \le d_e + p_e x_a - c_e x_b,$$
and the right side is the token count of $e$ at the end of the simulation. For a self loop, $p_e = c_e$ and the count is $d_e$ in both runs. So $b$ is enabled at the end of the simulation with $\mathrm{count}_b < q_b$, which contradicts Lemma 3. Hence the simulation reaches $\mathrm{count} = q$ whenever a PASS exists. $\blacksquare$

## What is not proved

The proof does not depend on the order in which line L6 picks actors, and it says nothing about which PASS is returned. In particular, the returned schedule need not have the least buffer memory, the shortest looped form, or the best period on several processors; the example of the page has a schedule with buffer 6 on one edge where another PASS needs 4.
