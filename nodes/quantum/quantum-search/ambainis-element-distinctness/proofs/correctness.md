---
title: AMBAINIS-K-DISTINCTNESS has one-sided error and stays in a (2k+1)-dimensional subspace
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page: $|S| = r$ with $k \le r < N - k$, $y \notin S$, and the data register holds $x_i$ for $i \in S$. The proof has three parts. Parts 1 and 2 are complete here. Part 3 bounds the success probability with Lemmas 2 and 3 of Ambainis's paper, which we state and do not prove again.

**Claim.** (a) Every answer of the form "$i_1, \ldots, i_k$" is a $k$-collision, and an input with no $k$-collision always gives "no k-collision". (b) Under the promise of exactly one $k$-collision $K$, the state of the algorithm stays in the span of $2k + 1$ fixed vectors, the uniform type states. (c) Under the same promise, there is $t_1 = O((N/r)^{k/2})$ such that the measured $S$ contains $K$ with probability $\Omega(1)$.

*Proof.* **Part 1: one-sided error.** The data register always holds $\bigotimes_{i \in S}|x_i\rangle$: line L2 writes it for the start state, line L7 writes $x_y$ when $y$ joins $S$, and line L9 erases $x_y$ by a second query, $|x_y \oplus x_y\rangle = |0\rangle$, before $y$ leaves $S$. Line L10 measures $S$ and reads the values of the data register, so it returns $i_1, \ldots, i_k$ only if $x_{i_1} = \cdots = x_{i_k}$. If the input has no $k$-collision, no $S$ passes this check, and the answer is "no k-collision" with probability 1. This proves (a).

**Part 2: the invariant subspace.** Fix $K = \{i_1, \ldots, i_k\}$. A state $|S, y\rangle$ of $\mathcal{H}$ has type $(j, l)$ with $j = |S \cap K|$ and $l = [y \in K]$. If $j = k$ then $y \notin K$, so the types are $(j, 0)$ for $0 \le j \le k$ and $(j, 1)$ for $0 \le j \le k - 1$, which is $2k + 1$ types. In $\mathcal{H}'$, where $|S| = r + 1$ and $y \in S$, the type $(j, 0)$ needs $j \le r$ and the type $(j, 1)$ needs $j \ge 1$, which again gives $2k + 1$ types. Let $\psi_{j,l}$ and $\varphi_{j,l}$ be the uniform superpositions of the states of each type. The bounds on $r$ make every type nonempty.

*Line L6.* Fix $S$ with $|S \cap K| = j$. The set $[N] \setminus S$ splits into $A_1 = K \setminus S$ with $a_1 = k - j$ elements and $A_0$ with $a_0 = N - r - k + j$ elements. Let $|A_l\rangle$ be the uniform state on $A_l$ and $m = a_0 + a_1 = N - r$. The uniform state on $[N] \setminus S$ is $|u\rangle = \sqrt{a_0/m}\,|A_0\rangle + \sqrt{a_1/m}\,|A_1\rangle$, and L6 applies $2|u\rangle\langle u| - I$ to $y$. On the span of $|A_0\rangle, |A_1\rangle$ this is the real matrix
$$R(a_0, a_1) = \begin{pmatrix} 2a_0/m - 1 & 2\sqrt{a_0a_1}/m \\ 2\sqrt{a_0a_1}/m & 2a_1/m - 1 \end{pmatrix},$$
which depends on $S$ only through $j$. Now $\psi_{j,l} = c_j^{-1/2} \sum_{S} |S\rangle|A_l(S)\rangle$, where the sum runs over the $c_j$ sets with $|S \cap K| = j$. So L6 maps the pair $(\psi_{j,0}, \psi_{j,1})$ by $R(N - r - k + j, k - j)$. For $j = k$ we have $a_1 = 0$, and $\psi_{k,0}$ is fixed.

*Line L7.* The map $|S, y\rangle \mapsto |S \cup \{y\}, y\rangle$ is a bijection from the basis of $\mathcal{H}$ onto the basis of $\mathcal{H}'$; its inverse removes $y$. It sends type $(j, 0)$ onto type $(j, 0)$ and type $(j, 1)$ onto type $(j + 1, 1)$, because $y$ joins $S$. A bijection between two sets of basis states sends the uniform state on the first to the uniform state on the second, so $\psi_{j,0} \mapsto \varphi_{j,0}$ and $\psi_{j,1} \mapsto \varphi_{j+1,1}$. The query only writes $x_y$, which is a function of the new $S$.

*Line L8.* Fix $S'$ with $|S'| = r + 1$ and $|S' \cap K| = j$. Then $S'$ splits into $S' \cap K$ with $j$ elements ($l = 1$) and $S' \setminus K$ with $r + 1 - j$ elements ($l = 0$). As for L6, the reflection maps the pair $(\varphi_{j,0}, \varphi_{j,1})$ by $R(r + 1 - j, j)$, and it fixes $\varphi_{0,0}$.

*Line L9.* This is the inverse of the map of L7, so $\varphi_{j,0} \mapsto \psi_{j,0}$ and $\varphi_{j,1} \mapsto \psi_{j-1,1}$, and the query erases $x_y$.

*Line L4.* The stored values of $S$ hold $k$ equal values if and only if $K \subseteq S$, by the promise, which is the type $(k, 0)$. So L4 maps $\psi_{k,0} \mapsto -\psi_{k,0}$ and fixes the other $2k$ vectors.

*The start.* The state after L2 is the uniform state on all $|S, y\rangle$, which is $\sum_{(j,l)} \sqrt{n_{j,l}/n}\,\psi_{j,l}$, with $n = \binom{N}{r}(N - r)$, $n_{j,0} = \binom{k}{j}\binom{N-k}{r-j}(N - k - r + j)$ and $n_{j,1} = \binom{k}{j}\binom{N-k}{r-j}(k - j)$. So the start state is in the span, and each line maps the span into itself (or into the span of the $\varphi_{j,l}$ and back). This proves (b), which is Lemma 1 of the paper. It also shows that the walk is a real orthogonal matrix on a space of dimension $2k + 1$, which is how the reduced simulation of the page works.

**Part 3: the success probability.** Let $U$ be one walk step (lines L6 to L9) on the span. The start state $\psi_{\mathrm{start}}$ is fixed by $U$, since each reflection fixes the uniform state and L7, L9 map the uniform state of $\mathcal{H}$ to the uniform state of $\mathcal{H}'$ and back. Lemma 2 of the paper: the other $2k$ eigenvalues of $U$ are $e^{\pm i\theta_j}$ with $\theta_j = (2\sqrt{j} + o(1))/\sqrt{r}$, $j = 1, \ldots, k$. With $t_2 = \lceil \pi\sqrt{r}/(3\sqrt{k}) \rceil$, the eigenphases of $U_2 = U^{t_2}$ are $\pm(2\pi\sqrt{j}/(3\sqrt{k}) + o(1))$, so they lie in $[\epsilon, 2\pi - \epsilon]$ for a constant $\epsilon > 0$ that depends only on $k$. Let $U_1$ be the sign flip of L4 on $\psi_{\mathrm{good}} = \psi_{k,0}$. Lemma 3 of the paper: for real states and a real $U_2$ with these properties, some $t = O(1/\alpha)$ gives $|\langle \psi_{\mathrm{good}}|(U_2U_1)^t|\psi_{\mathrm{start}}\rangle| = \Omega(1)$, where $\alpha = \langle \psi_{\mathrm{good}}|\psi_{\mathrm{start}}\rangle$. Here
$$\alpha^2 = \frac{n_{k,0}}{n} = \frac{\binom{N-k}{r-k}}{\binom{N}{r}} = \prod_{i=0}^{k-1}\frac{r - i}{N - i} = (1 - o(1))\Big(\frac{r}{N}\Big)^k$$
for constant $k$, so $t_1 = O((N/r)^{k/2})$. The measurement of L10 gives a set $S \supseteq K$ with probability $|\langle \psi_{\mathrm{good}}|\cdot\rangle|^2 = \Omega(1)$, and then L10 returns $K$. This proves (c). $\blacksquare$

**Query count.** Line L2 makes $r$ queries, lines L7 and L9 make one each, and the other lines make none. So the count is $r + 2t_1t_2 = O(r + (N/r)^{k/2}\sqrt{r})$, which is $O(N^{k/(k+1)})$ for $r = N^{k/(k+1)}$.
