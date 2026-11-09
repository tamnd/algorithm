---
title: Expected time of Schöning's algorithm, and Papadimitriou's n^2 bound for 2-SAT
proves: [time.expected]
status: full
---

We use the pseudocode of the page and the theorem of the correctness proof. $F$ has $n$ variables, $m$ clauses and clauses of at most $k$ literals, $k \ge 3$.

**Cost of one try.** Line L2 and the set up of the counts of true literals take $O(n + mk)$ time. The implementation keeps, for each clause, the number of its true literals, and a list of the false clauses with the position of each clause in it. Then line L4 is a test of an empty list, and line L5 takes $O(1)$ time. A flip of $x_v$ at line L7 updates the clauses that contain $v$, in $O(k)$ time each, so $O(mk)$ time in the worst case. A try has at most $3n$ flips, so it takes $O(n m k)$ time.

**Theorem 1.** If $F$ has a model, then running tries until one succeeds takes expected time $O\big((2(k-1)/k)^n \, n^2 m k\big)$.

*Proof.* The tries are independent, and each succeeds with probability at least $p = c_k (k/(2(k-1)))^n / (3n+1)$ with $c_k \ge 1/e$, by the correctness proof. The number of tries is geometric, with mean at most $1/p \le e (3n+1) (2(k-1)/k)^n$. Multiply by the cost $O(nmk)$ of a try. $\square$

For $k = 3$ this is $O((4/3)^n n^2 m)$. With the fixed number $T = \lceil \ln(1/\varepsilon)/p \rceil$ of tries of the page, the worst case time is $O\big((2(k-1)/k)^n n^2 m k \log(1/\varepsilon)\big)$, on satisfiable and unsatisfiable formulas alike.

**Theorem 2 (Papadimitriou 1991).** Let $F$ be a satisfiable formula with clauses of at most 2 literals. Start from any assignment and repeat: if $x$ satisfies $F$, stop; else pick any false clause and flip a uniformly random variable of it. The expected number of flips until it stops is at most $n^2$. So a walk of $2n^2$ flips finds a model with probability at least $1/2$.

*Proof.* Fix a model $a^*$ and let $d_t$ be the distance from $x$ to $a^*$ after $t$ flips. As in Step 1 of the correctness proof, a false clause has at most 2 positions, and at least one is good. So a flip decreases $d$ with probability $g \ge 1/2$. If $d_t = n$, then $x$ differs from $a^*$ in every variable, so each literal that is false under $x$ is true under $a^*$, and $g = 1$.

Let $Y$ be the walk on $\{0, 1, \ldots, n\}$ with $Y_0 = d_0$ that steps from $n$ to $n - 1$, and from $0 < y < n$ steps down when $U_t < 1/2$ and up otherwise, where the $U_t$ are the uniform numbers that also choose the flips, with the good positions first, as in Step 2 of the correctness proof. We claim that $d_t \le Y_t$ for each $t$ before both have stopped, where $Y$ stops at 0. Both start equal, and both change by exactly 1 at each step, so $d_t$ and $Y_t$ have the same parity. Suppose $d_t \le Y_t$.

- If $d_t < Y_t$, then $d_t \le Y_t - 2$ by parity, so $d_{t+1} \le d_t + 1 \le Y_t - 1 \le Y_{t+1}$.
- If $d_t = Y_t = n$, both step down.
- If $d_t = Y_t < n$ and $Y$ steps down, then $U_t < 1/2 \le g$, so $d$ steps down too. If $Y$ steps up, $d_{t+1} \le d_t + 1 = Y_{t+1}$.

So the walk on $F$ stops no later than the first time $Y$ reaches 0. Let $h_j$ be the expected time for $Y$ to reach 0 from $j$. Then $h_0 = 0$, $h_n = 1 + h_{n-1}$, and $h_j = 1 + (h_{j-1} + h_{j+1})/2$ for $0 < j < n$. The function $h_j = 2 n j - j^2$ satisfies all three equations: $h_0 = 0$; $h_n - h_{n-1} = n^2 - (n^2 - 1) = 1$; and $(h_{j-1} + h_{j+1})/2 = 2nj - j^2 - 1$. These equations have only one solution, because the differences $h_j - h_{j-1}$ are fixed one by one from $j = n$ down. So the expected time is at most $\max_j h_j = h_n = n^2$. By [Markov's inequality](/markov-inequality/), the walk has not stopped after $2n^2$ flips with probability at most $1/2$. $\blacksquare$

**Why the same walk is exponential for $k = 3$.** For $k \ge 3$ the down probability is only guaranteed to be $1/k < 1/2$, so the comparison walk drifts away from 0. Restarts after $3n$ flips fix this: a short walk that starts close to $a^*$ has a fair chance to reach it before it drifts away, and a random start is close with probability large enough to give the base $2(k-1)/k$.
