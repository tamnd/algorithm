---
title: Proof of Ladner's theorem
proves: [statement]
status: full
---

All logarithms are to base 2. Machines are deterministic multitape Turing machines over the alphabet $\{0, 1\}$ that halt with output 0 or 1. Let $M_1, M_2, \ldots$ be a list of all such machines in which every machine appears infinitely often. For example, let $M_i$ be the machine whose code is the binary expansion of $i$ up to a fixed end marker, with the bits after the marker ignored, and a machine that always outputs 0 when there is no valid code. Given $i$, a universal machine simulates $t$ steps of $M_i$ in time polynomial in $t$ and $\log i$.

**The definition.** For $n < 4$ let $H(n) = 1$. For $n \ge 4$, say that $i \ge 1$ is *good for $n$* when $i < \log \log n$ and, for every string $x$ with $|x| \le \log n$, the machine $M_i$ on input $x$ halts within $i (|x| + 1)^i$ steps and outputs $1$ if $x \in \text{SAT}_H$ and $0$ otherwise. Let $H(n)$ be the smallest $i$ that is good for $n$, and $H(n) = \lfloor \log \log n \rfloor$ if no $i$ is good for $n$. Let

$$\text{SAT}_H = \{ \psi \, 0 \, 1^{m^{H(m)}} : \psi \in \text{SAT}, \ m = |\psi| \}.$$

Here SAT is the set of strings that encode satisfiable CNF formulas. A string $y$ has at most one decomposition $y = \psi \, 0 \, 1^k$: the block $1^k$ is the maximal run of ones at the end of $y$, and the $0$ before it is the last $0$ of $y$. In all cases $1 \le H(n) \le \max(1, \log \log n)$.

**Step 0: the definition is well founded.** To decide whether $x \in \text{SAT}_H$ we need $H(m)$ only for $m = |\psi| < |x|$. To compute $H(n)$ we need membership in $\text{SAT}_H$ only for strings with $|x| \le \log n < n$. So $H(n)$ depends only on values $H(m)$ with $m < n$, and $H$ and $\text{SAT}_H$ are defined by induction on $n$.

**Step 1: $H$ is computable in polynomial time.** Let $T(n)$ be the time to compute $H(n)$. First compute $H(m)$ for all $m \le \log n$, in time at most $\sum_{m \le \log n} T(m)$. Then, for each of the fewer than $2n$ strings $x$ with $|x| \le \log n$, decide whether $x \in \text{SAT}_H$: find the decomposition $x = \psi \, 0 \, 1^k$, check that $k = m^{H(m)}$ for $m = |\psi|$, and decide $\psi \in \text{SAT}$ by trying all assignments. A formula of length $m$ has at most $m$ variables, so this takes $2^m \operatorname{poly}(m) \le n \operatorname{poly}(\log n)$ steps. Finally, for each $i < \log \log n$ and each such $x$, simulate $M_i$ on $x$ for $i (|x| + 1)^i$ steps. This is at most $\log \log n \cdot (\log n + 1)^{\log \log n} = 2^{O((\log \log n)^2)}$ steps, which is $n^{o(1)}$. Together,

$$T(n) \le \sum_{m \le \log n} T(m) + 2n \left( n \operatorname{poly}(\log n) + n^{o(1)} \right).$$

The second term is $O(n^{2 + o(1)})$. By induction, $T(n) \le n^3$ for all large $n$: the sum is at most $\log n \cdot (\log n)^3 = o(n)$. So $H(n)$ is computable in time $O(n^3)$.

**Step 2: $\text{SAT}_H \in \mathsf{NP}$.** On input $y$, find the decomposition $y = \psi \, 0 \, 1^k$, and reject if there is none. Let $m = |\psi|$. Compute $H(m)$ in time $O(m^3)$ and check $k = m^{H(m)}$ by counting, in time polynomial in $|y|$. Then guess an assignment for $\psi$ and accept when it satisfies $\psi$. This is a nondeterministic polynomial-time machine for $\text{SAT}_H$.

**Step 3: if $\text{SAT}_H \in \mathsf{P}$, then $H$ is bounded.** Let $M$ decide $\text{SAT}_H$ and halt within $c (|x| + 1)^c$ steps on every input $x$. Since $M$ appears infinitely often in the list, $M = M_i$ for some $i \ge c$. For every $n$ with $\log \log n > i$, the number $i$ is good for $n$, because $c (|x| + 1)^c \le i (|x| + 1)^i$, so $H(n) \le i$. For every other $n$, $H(n) \le \max(1, \log \log n) \le i$. So $H(n) \le i$ for all $n$.

**Step 4: if $\text{SAT}_H \notin \mathsf{P}$, then $H(n) \to \infty$.** Suppose not. Then there is a constant $C$ with $H(n) \le C$ for infinitely many $n$, and so some value $i \le C$ with $H(n) = i$ for infinitely many $n$. Only finitely many $n$ have $n < 4$ or $\lfloor \log \log n \rfloor = i$. For the other $n$ with $H(n) = i$, the number $i$ is good for $n$: $M_i$ answers correctly within $i (|x| + 1)^i$ steps on every $x$ with $|x| \le \log n$. These $n$ are unbounded, so $M_i$ answers correctly within $i (|x| + 1)^i$ steps on every string $x$. Then $M_i$ decides $\text{SAT}_H$ in polynomial time, a contradiction.

**Main argument.** Assume $\mathsf{P} \ne \mathsf{NP}$. By the [Cook-Levin theorem](/cook-levin-theorem/), SAT is NP-complete, so $\text{SAT} \notin \mathsf{P}$.

*(a) $\text{SAT}_H \notin \mathsf{P}$.* Suppose $\text{SAT}_H \in \mathsf{P}$. By Step 3, $H(n) \le C$ for all $n$. Let $f(\psi) = \psi \, 0 \, 1^{n^{H(n)}}$ with $n = |\psi|$. By Step 1, $f$ is computable in time $O(n^3 + n^C)$. By the definition of $\text{SAT}_H$ and the uniqueness of the decomposition, $\psi \in \text{SAT}$ if and only if $f(\psi) \in \text{SAT}_H$. So $f$ is a polynomial-time reduction from SAT to a language in P, and $\text{SAT} \in \mathsf{P}$, a contradiction.

*(b) $\text{SAT}_H$ is not NP-complete.* Suppose it is. Then $\text{SAT} \le_p \text{SAT}_H$ by a map $f$ and there is $i \ge 1$ such that $f$ runs in at most $n^i$ steps on inputs of length $n \ge 2$, so $|f(\psi)| \le |\psi|^i$. By (a) and Step 4, $H(m) \to \infty$, so there is $m_0 \ge 2$ with $H(m) > 2i$ for all $m > m_0$. The following algorithm decides SAT. Store the answers for all strings of length at most $m_0$ in a finite table. On input $\psi$:

1. Let $n = |\psi|$. If $n \le m_0$, answer from the table.
2. Compute $y = f(\psi)$. If $y$ has no decomposition $y = \psi' \, 0 \, 1^{k}$ with $k = m^{H(m)}$ for $m = |\psi'|$, then $y \notin \text{SAT}_H$, so $\psi \notin \text{SAT}$: answer no.
3. Otherwise $\psi \in \text{SAT}$ if and only if $y \in \text{SAT}_H$, if and only if $\psi' \in \text{SAT}$. If $m \le m_0$, answer from the table. If $m > m_0$, then $m^{2i} < m^{H(m)} < |y| \le n^i$, so $m < \sqrt{n}$. Replace $\psi$ by $\psi'$ and go to step 1.

Each round replaces a formula of length $n$ by one of length less than $\sqrt{n}$, so after $r$ rounds the length is less than $n^{1/2^r}$. All lengths in a round that continues are greater than $m_0 \ge 2$, so there are at most $\log \log n + 1$ rounds. Each round takes time polynomial in $n$: $f$ takes at most $n^i$ steps, and the check in step 2 computes $H(m)$ for $m \le n^i$, in time $O(n^{3i})$ by Step 1. So the algorithm runs in polynomial time and $\text{SAT} \in \mathsf{P}$, a contradiction.

*(c)* By Step 2, $\text{SAT}_H \in \mathsf{NP}$.

So $\text{SAT}_H$ is in NP, not in P and not NP-complete. $\blacksquare$
