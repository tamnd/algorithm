---
title: Schöning's walk returns only models, and one try finds a model with probability at least (k/(2(k-1)))^n/(3n+1), up to a constant
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$ with clauses of at most $k$ literals, and $k \ge 3$. (A formula with shorter clauses is also a formula with clauses of at most 3 literals, so we may take $k = \max(3, \text{longest clause})$.) One *try* is lines L2 to L7: a random start and at most $3n$ flips.

**Termination.** The loop of line L1 runs at most $T$ times, and the loop of line L3 at most $3n + 1$ times. Each step does a finite amount of work. So the algorithm stops.

**One-sided correctness.** The algorithm returns an assignment only at line L4, after the check that it satisfies $F$. So each returned assignment is a model. If $F$ has no model, line L4 never returns, and the algorithm reaches line L8. The answer at line L8 can be wrong only when $F$ has a model; we bound the probability of this now.

**Theorem.** Let $F$ have a model. Then one try returns a model with probability at least

$$p = \frac{c_k}{3n + 1} \left( \frac{k}{2(k-1)} \right)^n, \qquad c_k = \left( \frac{k-1}{k} \right)^{k-3} \ge \frac{1}{e}.$$

So after $T = \lceil \ln(1/\varepsilon) / p \rceil$ tries the algorithm misses a model with probability at most $(1 - p)^T \le e^{-pT} \le \varepsilon$.

*Proof.* Fix one model $a^*$. Let $d_t$ be the Hamming distance between $a^*$ and the assignment $x$ after $t$ flips of the try.

*Step 1: each flip moves closer with probability at least $1/k$.* At line L5 the clause $C$ is false under $x$, so each literal of $C$ is false under $x$. The model $a^*$ makes $C$ true, so some literal of $C$ is true under $a^*$. Call a position of $C$ *good* when its literal is true under $a^*$. The variable of a good literal has different values in $x$ and $a^*$, so flipping it decreases $d$ by 1. Each other flip changes $d$ by $+1$ or $-1$. At least one of the at most $k$ positions is good, so line L6 picks a good position with probability $g \ge 1/k$, whatever happened before.

*Step 2: coupling with a simple walk.* Let $U_1, U_2, \ldots$ be independent and uniform on $[0, 1)$. At flip $t$, list the positions of $C$ with the good ones first, and let line L6 take position $\lfloor U_t |C| \rfloor$. This is a uniform choice, so the try has the same distribution as before, and the flip moves closer whenever $U_t < g$. Define the walk $Y_0 = d_0$ and $Y_t = Y_{t-1} - 1$ if $U_t < 1/k$, else $Y_t = Y_{t-1} + 1$, on all integers. Since $1/k \le g$, a down step of $Y$ is a down step of $d$, so $d_t - d_{t-1} \le Y_t - Y_{t-1}$ for each $t$ before the try stops. Then by induction $d_t \le Y_t$. If $Y_t = 0$ for some $t \le 3n$, then the try has stopped with a model by flip $t$, or $d_t \le 0$, which means $x = a^*$ and line L4 returns. So

$$\Pr[\text{the try succeeds} \mid d_0 = j] \ \ge\ q_j := \Pr[Y_t = 0 \text{ for some } t \le 3n \mid Y_0 = j].$$

*Step 3: a lower bound on $q_j$.* Write $j = (k-2) i + r$ with $i = \lfloor j / (k-2) \rfloor$ and $0 \le r \le k - 3$. Consider the event that the first $r$ steps of $Y$ go down, and that the next $N = (k-2)i + 2i = k i$ steps have exactly $i$ up steps and $(k-1) i$ down steps, in any order. On this event $Y$ is at 0 after $r + N$ steps, and $r + N = j + 2i \le j + 2j/(k-2) = j k/(k-2) \le 3j \le 3n$, since $k \ge 3$ and $j \le n$. The walk moves by $\pm 1$, so it is at 0 at the step $r + N \le 3n$. Hence

$$q_j \ \ge\ k^{-r} \binom{N}{i} \left(\frac{1}{k}\right)^{(k-1) i} \left(\frac{k-1}{k}\right)^{i}.$$

For the binomial coefficient we use $\binom{N}{\alpha N} \ge \frac{1}{N + 1} 2^{N H(\alpha)}$, where $H$ is the [binary entropy function](/binary-entropy-function/). (Proof: the $N + 1$ terms $\binom{N}{s} \alpha^s (1 - \alpha)^{N-s}$ sum to 1, and the term $s = \alpha N$ is the largest, so it is at least $1/(N+1)$; and $\alpha^{\alpha N} (1-\alpha)^{(1-\alpha)N} = 2^{-N H(\alpha)}$.) With $\alpha = i/N = 1/k$,

$$2^{N H(1/k)} = k^{i} \left(\frac{k}{k-1}\right)^{(k-1) i}.$$

Multiply:

$$\binom{N}{i} \left(\frac{1}{k}\right)^{(k-1) i} \left(\frac{k-1}{k}\right)^{i} \ \ge\ \frac{1}{N+1} \cdot k^{i} \cdot \frac{k^{(k-1) i}}{(k-1)^{(k-1) i}} \cdot \frac{1}{k^{(k-1) i}} \cdot \frac{(k-1)^{i}}{k^{i}} = \frac{(k-1)^{-(k-2) i}}{N+1}.$$

With $(k-2) i = j - r$ and $N + 1 \le 3n + 1$,

$$q_j \ \ge\ \frac{k^{-r} (k-1)^{-(j - r)}}{3n + 1} = \frac{(k-1)^{-j}}{3n+1} \left( \frac{k-1}{k} \right)^{r} \ \ge\ \frac{c_k (k-1)^{-j}}{3n+1}.$$

The case $i = 0$ is included: then $N = 0$ and the bound is $k^{-r}$.

*Step 4: the random start.* Line L2 draws each variable uniformly and independently, so $d_0$ has the binomial distribution with $\Pr[d_0 = j] = \binom{n}{j} 2^{-n}$. By the binomial theorem,

$$\Pr[\text{the try succeeds}] \ \ge\ \sum_{j=0}^{n} \binom{n}{j} 2^{-n} \frac{c_k (k-1)^{-j}}{3n+1} = \frac{c_k}{3n+1} \cdot 2^{-n} \left(1 + \frac{1}{k-1}\right)^n = \frac{c_k}{3n+1} \left(\frac{k}{2(k-1)}\right)^n.$$

Finally $c_k = (1 - 1/k)^{k-3} \ge (1 - 1/k)^{k-1} \ge 1/e$. The tries are independent, which gives the bound on $T$. $\blacksquare$

**Remark.** For $k = 3$, $c_3 = 1$ and $r = 0$, and the bound is $p = (3/4)^n / (3n + 1)$. Schöning's original analysis uses the first-passage probabilities of the walk and gives the factor $1/\mathrm{poly}(n)$ in a slightly different form; the exponential base $2(k-1)/k$ is the same.
