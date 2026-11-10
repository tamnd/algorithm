---
title: Floyd's algorithm returns each k-subset with probability 1 over C(n, k)
proves: [correctness, termination]
status: full
---

**Statement.** Let $0 \le k \le n$, and assume that line L3 draws a uniform integer in $\{0, \ldots, j\}$, independently each time. Then FLOYD-SAMPLE$(n, k)$ draws exactly $k$ integers and returns each $k$-subset of $\{0, \ldots, n-1\}$ with probability $1/\binom{n}{k}$.

**Termination.** The loop of line L2 runs exactly $k$ times, once for each $j = n - k, \ldots, n - 1$, and each round draws one integer.

**Claim.** For $i = 0, 1, \ldots, k$, after $i$ rounds the set $S$ is a uniform random $i$-subset of $\{0, \ldots, n - k + i - 1\}$. For $i = k$ this is the statement.

**Base, $i = 0$.** $S$ is empty, the only 0-subset.

**Step.** Suppose that after $i$ rounds $S$ is a uniform $i$-subset of $\{0, \ldots, j - 1\}$, where $j = n - k + i$ is the value of the next round, and $i \le j$. The round draws $t$ uniform in $\{0, \ldots, j\}$. If $t \notin S$, it adds $t$. If $t \in S$, it adds $j$, which is not in $S$ since $S \subseteq \{0, \ldots, j-1\}$. In both cases the new set $S'$ has $i + 1$ elements in $\{0, \ldots, j\}$.

Fix a set $B \subseteq \{0, \ldots, j\}$ with $|B| = i + 1$. Each $i$-subset of $\{0, \ldots, j-1\}$ has probability $1/\binom{j}{i}$.

- *Case $j \in B$.* $S' = B$ happens exactly when $S = B \setminus \{j\}$ and then either $t = j$ (first branch, $j \notin S$) or $t \in S$ (second branch adds $j$). That is $1 + i$ values of $t$ out of $j + 1$. So $\Pr[S' = B] = \frac{1}{\binom{j}{i}} \cdot \frac{i + 1}{j + 1}$.
- *Case $j \notin B$.* Then $B \subseteq \{0, \ldots, j - 1\}$, and the second branch cannot give $B$, since it adds $j$. The first branch gives $B$ exactly when $S = B \setminus \{x\}$ and $t = x$ for some $x \in B$. These are $i + 1$ disjoint events, each of probability $\frac{1}{\binom{j}{i}} \cdot \frac{1}{j + 1}$. So $\Pr[S' = B] = \frac{1}{\binom{j}{i}} \cdot \frac{i + 1}{j + 1}$.

In both cases,
$$\Pr[S' = B] = \frac{(i + 1)\, i!\, (j - i)!}{(j + 1)\, j!} = \frac{(i + 1)!\, (j - i)!}{(j + 1)!} = \frac{1}{\binom{j + 1}{i + 1}},$$
so $S'$ is a uniform $(i + 1)$-subset of $\{0, \ldots, j\}$, which is the claim for $i + 1$. $\blacksquare$
