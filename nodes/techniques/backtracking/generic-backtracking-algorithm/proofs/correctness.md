---
title: Backtracking visits exactly the reachable prefixes and outputs exactly the solutions
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A sequence $x_1 \ldots x_k$ with $0 \le k \le n$ is *reachable* when, for each $j$ from 1 to $k$, $x_j \in D_j(x_1 \ldots x_{j-1})$ and $P_j(x_1 \ldots x_j)$ hold. The empty sequence is reachable. We assume that each set $D_j$ is finite and that each test returns true or false.

**Lemma.** Let $x_1 \ldots x_k$ be reachable, and call BACKTRACK$(x, k)$ with $x[1 \ldots k] = x_1 \ldots x_k$. The call terminates. During the call, BACKTRACK is called (directly or deeper) exactly once for each reachable proper extension $x_1 \ldots x_k y_{k+1} \ldots y_m$ with $m \le n$, these calls start in lexicographic order of the candidate orders, the call outputs exactly the reachable extensions of length $n$ (including $x_1 \ldots x_n$ itself when $k = n$), and on return $x[1 \ldots k]$ is unchanged and $x$ has length $k$.

*Proof.* By induction on $n - k$.

*Base, $k = n$.* Line L1 is true. Line L2 outputs $x_1 \ldots x_n$, which is the only reachable extension of length $n$, and line L3 returns without a call and without a change to $x$. A sequence of length $n$ has no proper extension of length at most $n$.

*Step, $k < n$.* Assume the lemma for all reachable prefixes of length $k + 1$. Line L1 is false. Let $c_1, \ldots, c_r$ be the candidates of $D_{k+1}(x_1 \ldots x_k)$ in their order. The loop of line L4 handles them one at a time. We show by induction on $i$ that, before the iteration for $c_i$, $x$ has length $k$ and $x[1 \ldots k] = x_1 \ldots x_k$. This holds for $i = 1$. In the iteration for $c_i$, line L5 sets $x[k+1] = c_i$, so $x[1 \ldots k+1] = x_1 \ldots x_k c_i$.

- If $P_{k+1}(x_1 \ldots x_k c_i)$ is false, the sequence $x_1 \ldots x_k c_i$ is not reachable, and neither is any extension of it, because reachability needs the test at position $k + 1$. Line L7 does not run, and no call is made for these sequences.
- If the test is true, $x_1 \ldots x_k c_i$ is reachable. Line L7 calls BACKTRACK$(x, k+1)$. By the induction hypothesis, this call terminates, makes exactly one call for each reachable proper extension of $x_1 \ldots x_k c_i$, in lexicographic order, outputs exactly the reachable extensions of $x_1 \ldots x_k c_i$ of length $n$, and leaves $x$ of length $k + 1$ with prefix $x_1 \ldots x_k c_i$.

In both cases line L8 removes $x[k+1]$, so $x$ has length $k$ and prefix $x_1 \ldots x_k$ before the next iteration. Each reachable proper extension of $x_1 \ldots x_k$ starts with exactly one $c_i$, so it is either $x_1 \ldots x_k c_i$ itself, for which line L7 makes the call, or a proper extension of it, which the inner call handles. So each one gets exactly one call. The calls under $c_i$ start before the calls under $c_{i+1}$, and within one $c_i$ they are in lexicographic order by the hypothesis, so all calls are in lexicographic order. The outputs are the union over $i$ of the reachable extensions of length $n$ under $c_i$, which is the set of reachable extensions of length $n$ of $x_1 \ldots x_k$. The loop has $r$ iterations and each one terminates, so the call terminates, and on return $x$ is as it was at the start. $\square$

**Theorem.** BACKTRACK$(x, 0)$ with $x$ empty terminates and outputs exactly the reachable sequences of length $n$, each one once, in lexicographic order of the candidate orders. If the tests are prefix-closed, that is, $P_{k+1}(x_1 \ldots x_{k+1})$ implies $P_k(x_1 \ldots x_k)$ for each $k \ge 1$, then the output is the set of sequences $x_1 \ldots x_n$ with $x_j \in D_j(x_1 \ldots x_{j-1})$ for each $j$ and $P_n(x_1 \ldots x_n)$.

*Proof.* The empty sequence is reachable, so the lemma with $k = 0$ gives termination and the output, each sequence once because each reachable sequence of length $n$ gets exactly one call, and each call outputs only its own sequence at line L2. For the second part, let $x_1 \ldots x_n$ satisfy the domain conditions and $P_n$. Prefix closure applied $n - 1$ times gives $P_j(x_1 \ldots x_j)$ for each $j \le n$, so the sequence is reachable. Conversely, a reachable sequence of length $n$ satisfies $P_n$ by definition. $\blacksquare$

**Number of calls.** By the lemma, the number of calls is the number $T$ of reachable sequences of length 0 to $n$. Each call runs line L6 once for each candidate, so the number of tests is $\sum |D_{k+1}(x_1 \ldots x_k)|$ over the reachable $x_1 \ldots x_k$ with $k < n$, which is at most $T d$.
