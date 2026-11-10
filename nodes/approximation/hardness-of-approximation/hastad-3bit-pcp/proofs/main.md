---
title: Håstad's 3-bit PCP from label cover, with the full long code analysis
proves: [statement]
status: full
---

This file proves the statement from one cited input, the NP-hardness of label cover with small soundness. That input comes from the PCP theorem and the parallel repetition theorem, and it is not proved here. Everything after it, the verifier, its completeness, the exact acceptance formula and the decoding of a labeling, is proved in full. The proof follows Håstad (2001) and O'Donnell, Section 7.4.

## The cited input

A label cover instance has a bipartite graph with sides $U$ and $V$, a probability distribution on its edges, label sets $[L]$ for $U$ and $[R]$ for $V$, and a map $\pi_e : [L] \to [R]$ on each edge $e$. A labeling $\ell$ satisfies $e = (u, v)$ if $\pi_e(\ell(u)) = \ell(v)$, and the value of the instance is the largest probability, over a random edge, that a labeling satisfies it.

**Theorem (cited).** For every $\gamma > 0$ there are $L, R$ depending only on $\gamma$ such that it is NP-hard to tell label cover instances of value $1$ from those of value at most $\gamma$.

This is the clause-variable game of the PCP theorem after [parallel repetition](/parallel-repetition-theorem/).

## Notation

We use the $\pm 1$ notation of Fourier analysis: functions on $\{-1,1\}^n$, $\chi_S(x) = \prod_{i \in S} x_i$ and $\hat f(S) = \mathbb{E}[f \chi_S]$. For $x \in \{-1,1\}^R$ and $\pi : [L] \to [R]$ let $x \circ \pi \in \{-1,1\}^L$ be the point with $(x \circ \pi)_i = x_{\pi(i)}$. For $S \subseteq [L]$ let

$$\pi_2(S) = \{ j \in [R] : |\pi^{-1}(j) \cap S| \text{ is odd} \}.$$

Then $\chi_S(x \circ \pi) = \prod_{i \in S} x_{\pi(i)} = \chi_{\pi_2(S)}(x)$, because $x_j^2 = 1$ cancels each pair of elements of $S$ that map to the same $j$.

## The verifier

Fix $\delta \in (0, \tfrac12)$. The proof has a folded table $f_u : \{-1,1\}^L \to \{-1,1\}$ for each $u \in U$ and a folded table $g_v : \{-1,1\}^R \to \{-1,1\}$ for each $v \in V$. *Folded* means $f(-w) = -f(w)$. The verifier stores only the entries with first coordinate $1$ and reads $f(w) = -f(-w)$ for the others, so every table it reads is folded. A folded table has $\hat f(S) = 0$ for every $S$ of even size, in particular for $S = \emptyset$, as shown on the [long code](/long-code/) page.

1. Pick a random edge $e = (u, v)$ with map $\pi = \pi_e$.
2. Pick $x \in \{-1,1\}^R$ and $y \in \{-1,1\}^L$ uniformly, and $z \in \{-1,1\}^L$ with independent coordinates, $z_i = -1$ with probability $\delta$.
3. Read $g_v(x)$, $f_u(y)$ and $f_u((x \circ \pi) \circ y \circ z)$, where $\circ$ between two points of $\{-1,1\}^L$ is the coordinatewise product.
4. Accept if $g_v(x) \, f_u(y) \, f_u((x \circ \pi) \circ y \circ z) = 1$.

Each read is one stored bit, possibly negated by folding, so the test is a linear equation over $\mathbb{F}_2$ in at most three stored bits. The tables have $2^{L-1}$ and $2^{R-1}$ stored entries, which is a constant, so the verifier uses $O(\log n)$ random bits for the edge and, for a rational $\delta$, a number of random bits for the points that depends only on $L$, $R$ and $\delta$.

## Completeness

Let $\ell$ be a labeling that satisfies every edge. Let $f_u$ be the dictator $w \mapsto w_{\ell(u)}$ and $g_v$ the dictator $x \mapsto x_{\ell(v)}$. Dictators are folded. On an edge $e = (u, v)$ with $a = \ell(u)$ we have $\ell(v) = \pi(a)$, so the product in step 4 is

$$x_{\pi(a)} \cdot y_a \cdot x_{\pi(a)} y_a z_a = z_a ,$$

which is $1$ with probability $1 - \delta$. So the verifier accepts with probability $1 - \delta$.

## The acceptance formula

**Claim.** For fixed tables and a fixed edge $e = (u, v)$ with $f = f_u$, $g = g_v$ and $\pi = \pi_e$,

$$\Pr[\text{accept} \mid e] = \tfrac12 + \tfrac12 \eta_e, \qquad \eta_e = \sum_{S \subseteq [L]} \hat g(\pi_2(S)) \, \hat f(S)^2 \, (1 - 2\delta)^{|S|} .$$

*Proof.* The indicator of acceptance is $\tfrac12 + \tfrac12 g(x) f(y) f((x \circ \pi) \circ y \circ z)$, so it suffices to compute $\mathbb{E}[g(x) f(y) f((x \circ \pi) \circ y \circ z)]$. Expand the third factor as $\sum_S \hat f(S) \chi_S((x \circ \pi) \circ y \circ z)$ and use $\chi_S((x \circ \pi) \circ y \circ z) = \chi_{\pi_2(S)}(x) \chi_S(y) \chi_S(z)$. The three points $x$, $y$, $z$ are independent, so the expectation of the term for $S$ factors as

$$\hat f(S) \cdot \mathbb{E}_x[g(x) \chi_{\pi_2(S)}(x)] \cdot \mathbb{E}_y[f(y) \chi_S(y)] \cdot \mathbb{E}_z[\chi_S(z)] = \hat f(S) \cdot \hat g(\pi_2(S)) \cdot \hat f(S) \cdot (1 - 2\delta)^{|S|} ,$$

where $\mathbb{E}[\chi_S(z)] = \prod_{i \in S} \mathbb{E}[z_i] = (1 - 2\delta)^{|S|}$. Summing over $S$ gives $\eta_e$. $\square$

## Soundness

**Claim.** If the verifier accepts with probability at least $\tfrac12 + \eta$ with $\eta > 0$, then the label cover instance has value at least $16 \delta \eta^2$.

*Proof.* By the acceptance formula, $\mathbb{E}_e[\eta_e] \ge 2\eta$.

*A random labeling.* For each $u \in U$ independently, pick $S \subseteq [L]$ with probability $\hat f_u(S)^2$, which is a probability distribution by Parseval, and let $\ell(u)$ be a uniformly random element of $S$. Since $f_u$ is folded, every $S$ with $\hat f_u(S) \ne 0$ has odd size, so $S$ is not empty. For each $v \in V$ independently, pick $T \subseteq [R]$ with probability $\hat g_v(T)^2$ and let $\ell(v)$ be a uniformly random element of $T$, which again is not empty.

*One edge.* Fix $e = (u, v)$ with map $\pi$. Consider the event that the set chosen for $u$ is $S$ and the set chosen for $v$ is $T = \pi_2(S)$, which has probability $\hat f_u(S)^2 \hat g_v(\pi_2(S))^2$. If $\pi_2(S) = \emptyset$ this is $0$, because $\hat g_v(\emptyset) = 0$. Otherwise $\ell(v) = j$ for some $j \in \pi_2(S)$. By the definition of $\pi_2$, the set $\pi^{-1}(j) \cap S$ has odd size, so it is not empty, and a random $\ell(u) \in S$ lies in it with probability at least $1/|S|$. Then $\pi(\ell(u)) = j = \ell(v)$. Summing over $S$,

$$\Pr[\ell \text{ satisfies } e] \ge \sum_S \frac{\hat f_u(S)^2 \hat g_v(\pi_2(S))^2}{|S|} .$$

*Link to $\eta_e$.* The weights $\hat f_u(S)^2$ sum to $1$, so the Cauchy-Schwarz inequality gives

$$\eta_e^2 = \Big( \sum_S \hat f_u(S)^2 \cdot \hat g_v(\pi_2(S)) (1 - 2\delta)^{|S|} \Big)^2 \le \sum_S \hat f_u(S)^2 \, \hat g_v(\pi_2(S))^2 \, (1 - 2\delta)^{2|S|} .$$

For $|S| \ge 1$, $(1 - 2\delta)^{2|S|} \le e^{-4\delta |S|} \le \frac{1}{4\delta|S|}$, using $1 - t \le e^{-t}$ and $e^{-t} \le 1/t$ for $t > 0$. So $\eta_e^2 \le \frac{1}{4\delta} \Pr[\ell \text{ satisfies } e]$.

*Average over edges.* The expected fraction of satisfied edges is

$$\mathbb{E}_e \Pr[\ell \text{ satisfies } e] \ge 4\delta \, \mathbb{E}_e[\eta_e^2] \ge 4 \delta \, (\mathbb{E}_e[\eta_e])^2 \ge 4\delta \cdot 4\eta^2 = 16 \delta \eta^2 ,$$

by Jensen's inequality. Some labeling reaches the expectation, so the value is at least $16 \delta \eta^2$. $\square$

## Putting it together

Given $\varepsilon \in (0, \tfrac12)$, set $\delta = \varepsilon$ and $\eta = \varepsilon$, and take the cited label cover hardness with $\gamma < 16 \varepsilon^3$. If the label cover instance has value $1$, the verifier accepts some proof with probability at least $1 - \varepsilon$. If it has value at most $\gamma$, the soundness claim shows that every proof is accepted with probability less than $\tfrac12 + \varepsilon$. The reduction from the label cover instance to the verifier, and from the verifier to the system of its equations (one equation per random string, weighted by its probability), runs in polynomial time because $L$ and $R$ are constants. So it is NP-hard to tell systems of linear equations over $\mathbb{F}_2$ with three variables per equation that have an assignment satisfying a $1 - \varepsilon$ fraction of the weight from those where every assignment satisfies less than a $\tfrac12 + \varepsilon$ fraction. This is the statement. $\blacksquare$
