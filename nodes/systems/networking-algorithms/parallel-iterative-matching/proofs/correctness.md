---
title: PIM returns a maximal matching, resolves 3/4 of the open requests per iteration in expectation, and needs at most log2 N + 4/3 iterations on average
proves: [correctness]
status: full
---

We use the pseudocode of the page. A *request* is a pair $(i, j)$ with $req[i][j]$ true. Before an iteration, a request is *unresolved* when both input $i$ and output $j$ are unmatched. Let $R_t$ be the number of unresolved requests after $t$ iterations, so $R_0$ is the number of requests and $R_0 \le N^2$.

**Lemma 1 (a matching).** After each iteration, the matched pairs form a matching, and each matched pair is a request.

*Proof.* An output grants only to an input that requested it (line L5), and it is unmatched, so the input is unmatched too. An input accepts only a grant that it received (line L7). Each unmatched output grants at most one input, and each input accepts at most one grant. So the new pairs of one iteration use each port at most once, and they use only ports that were unmatched before. Matched ports never request or grant again (line L3 and line L4 skip them). By induction on the iterations, no port is in two pairs. $\square$

**Lemma 2 (progress and maximality).** If $R_t > 0$, then iteration $t + 1$ adds at least one pair. So the loop of line L2 stops after at most $N$ iterations, and at that point the matching is maximal.

*Proof.* If $R_t > 0$, there is an unresolved request $(i, j)$. Input $i$ requests output $j$ in line L3, so output $j$ gets at least one request and grants some input $i'$ in line L5. Input $i'$ has at least one grant, so it accepts one in line L7 and becomes matched. So each iteration with $R_t > 0$ adds at least one pair. A matching has at most $N$ pairs, so at most $N$ such iterations occur. The loop stops when $R_t = 0$: no request joins an unmatched input to an unmatched output, which is the definition of a [maximal matching](/maximal-matching/). $\square$

**Lemma 3 (three quarters, Anderson et al. 1993).** For each state before an iteration, $\mathbb{E}[R_{t+1} \mid \text{state}] \le R_t / 4$.

*Proof.* Fix the state. For an unmatched output $j$, let $K_j$ be the set of unmatched inputs that request $j$, and $k_j = |K_j|$. Each unresolved request is counted at exactly one output, so $R_t = \sum_j k_j$. We show that the expected number of requests to $j$ that are still unresolved after the iteration is at most $k_j / 4$.

Fix the grants of all outputs other than $j$. They do not depend on the random choice of $j$. Let $U \subseteq K_j$ be the inputs of $K_j$ that get no grant from another output, and $q = |U|$. Each input that gets at least one grant accepts one and is matched, so each input of $K_j \setminus U$ is matched, and its request to $j$ is resolved. Output $j$ grants a uniform input of $K_j$.

- With probability $q / k_j$, output $j$ grants an input of $U$. That input has only this grant, so it accepts $j$. Then $j$ is matched, and all $k_j$ requests to $j$ are resolved.
- With probability $(k_j - q)/k_j$, output $j$ grants an input outside $U$. The only requests to $j$ that can stay unresolved are the $q$ requests from $U$.

So the conditional expectation is at most $\frac{k_j - q}{k_j}\, q \le \frac{k_j}{4}$, because $q(k_j - q) \le k_j^2/4$ for each real $q$. This bound holds for each choice of the other grants, so it holds without the condition. Summing over $j$ gives $\mathbb{E}[R_{t+1}] \le \sum_j k_j/4 = R_t/4$. $\square$

**Theorem (expected number of iterations).** Let $T$ be the number of iterations until $R_T = 0$. Then $\mathbb{E}[T] \le \lceil \log_2 N \rceil + 4/3$.

*Proof.* By Lemma 3 and the tower rule, $\mathbb{E}[R_t] \le R_0 / 4^t \le N^2 / 4^t$. The event $T > t$ is the event $R_t \ge 1$, so by the [Markov inequality](/markov-inequality/) $\Pr[T > t] \le \min(1, N^2 4^{-t})$. Let $t_0 = \lceil \log_2 N \rceil$, so $4^{t_0} \ge N^2$. Then

$$\mathbb{E}[T] = \sum_{t \ge 0} \Pr[T > t] \le \sum_{t < t_0} 1 + \sum_{t \ge t_0} \frac{N^2}{4^t} \le t_0 + \frac{N^2}{4^{t_0}} \cdot \frac{4}{3} \le t_0 + \frac43. \qquad \blacksquare$$
