---
title: The vantage-point tree has logarithmic height and its range and nearest neighbor searches are exact
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. $(U, d)$ is a metric space and $P \subseteq U$ a finite set of $n$ objects; $\mathrm{obj}(N)$ is the set of vantage points of the nodes in the subtree of $N$.

**Lemma 1 (structure).** BUILD$(S)$ returns a tree whose nodes have the objects of $S$ as vantage points, each exactly once, and each node $N = (v, \mu, \mathit{in}, \mathit{out})$ satisfies $d(v, x) \le \mu$ for $x \in \mathrm{obj}(\mathit{in})$ and $d(v, x) \ge \mu$ for $x \in \mathrm{obj}(\mathit{out})$.

*Proof.* By induction on $|S|$. For $S$ empty, line L1 returns nil. Otherwise line L2 takes $v \in S$, and the two lists of line L6 partition $S' = S \setminus \{v\}$, each shorter than $S$, so by induction the children hold their objects once each; with $v$ at the root, $S$ is covered once. If $S'$ is empty, line L4 returns a node with empty children, and the claim holds vacuously. Otherwise $S'$ is sorted by $d(v, \cdot)$ and $\mu = d(v, S'[m])$; for $i \le m$, $d(v, S'[i]) \le \mu$, and for $i > m$, $d(v, S'[i]) \ge \mu$. $\square$

**Lemma 2 (height).** The tree built from $n \ge 1$ objects has height $h(n) = \lfloor \log_2 n \rfloor + 1$, counting nodes on a longest root-to-leaf path. BUILD makes at most $n \cdot h(n)$ evaluations.

*Proof.* The children have $\lceil (n-1)/2 \rceil = \lfloor n/2 \rfloor$ and $\lfloor (n-1)/2 \rfloor$ objects. So $h(1) = 1$ and $h(n) = 1 + h(\lfloor n/2 \rfloor)$ for $n \ge 2$, since $h$ is nondecreasing by induction. For $n \ge 2$, $\lfloor \log_2 \lfloor n/2 \rfloor \rfloor = \lfloor \log_2 n \rfloor - 1$: if $2^j \le n < 2^{j+1}$ then $2^{j-1} \le \lfloor n/2 \rfloor < 2^j$. Induction gives $h(n) = \lfloor \log_2 n \rfloor + 1$. Line L3 makes $|S| - 1$ evaluations at a node with subtree set $S$, and the line L5 distance is already known. The subtree sets of the nodes at one depth are disjoint, so each depth costs at most $n$ evaluations, and there are $h(n)$ depths. $\square$

**Theorem 1 (range).** RANGE$(\text{root}, q, r, \mathit{out})$ adds to $\mathit{out}$ exactly the objects $x \in P$ with $d(q, x) \le r$, each once.

*Proof.* We show by induction on the tree that RANGE$(N, q, r, \cdot)$ adds exactly $\{x \in \mathrm{obj}(N) : d(q, x) \le r\}$. For $N$ = nil, line L7 adds nothing. Otherwise let $t = d(q, v)$. Line L8 adds $v$ if and only if $d(q, v) \le r$. If line L9 recurses, the induction hypothesis gives the answers in $\mathit{in}$. If it does not, then $t - r > \mu$, and for each $x \in \mathrm{obj}(\mathit{in})$, by the triangle inequality and Lemma 1, $d(q, x) \ge d(q, v) - d(v, x) \ge t - \mu > r$, so $\mathit{in}$ has no answer. If line L10 does not recurse, then $\mu - t > r$, and for $x \in \mathrm{obj}(\mathit{out})$, $d(q, x) \ge d(v, x) - d(q, v) \ge \mu - t > r$. Lemma 1 says that $v$, $\mathrm{obj}(\mathit{in})$ and $\mathrm{obj}(\mathit{out})$ are disjoint, so nothing is added twice. $\square$

**Theorem 2 (nearest).** If $P$ is nonempty, after NEAREST$(\text{root}, q)$ with $\tau = \infty$ at the start, $b \in P$ and $\tau = d(q, b) = \min_{x \in P} d(q, x)$.

*Proof.* Line L12 is the only line that changes $(b, \tau)$; it sets them to a visited object and its distance, and only when the distance is smaller. So at every moment $\tau = \min$ of the distances of the visited objects, $\tau$ never increases, and $b$ attains it. The root is visited, so $b \in P$ at the end. Let $\tau_f$ be the final value. Suppose some $x \in P$ has $d(q, x) < \tau_f$. Then $x$ was not visited, since otherwise $\tau_f \le d(q, x)$. So $x$ lies in a subtree $C$ of a visited node $N$ that line L15 skipped at a moment when $\tau$ had a value $\tau_0 \ge \tau_f$. If $C = \mathit{in}$, then $t - \tau_0 > \mu$ and $d(q, x) \ge t - \mu > \tau_0 \ge \tau_f$. If $C = \mathit{out}$, then $t + \tau_0 < \mu$ and $d(q, x) \ge \mu - t > \tau_0 \ge \tau_f$. Both contradict $d(q, x) < \tau_f$. So $\tau_f$ is the least distance. $\blacksquare$
