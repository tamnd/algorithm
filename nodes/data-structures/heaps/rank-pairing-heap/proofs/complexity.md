---
title: Amortized cost of the type-2 rank-pairing heap
proves: [time.amortized]
status: full
---

We prove Theorem 6.1 of Haeupler, Sen and Tarjan for type-2 rank-pairing heaps with multipass linking: find-min, insert, meld and decrease-key take $O(1)$ amortized time, and delete-min takes $O(\log n)$ amortized time. The proof follows the paper, with the accounting written out.

**The rank bound.** A child of rank $k$ has at least $F_{k+3} - 1$ nodes in its subtree, with $F_0 = 0$, $F_1 = 1$. By induction on height: a missing node of rank $-1$ has $0 = F_2 - 1$ nodes, and a leaf has $1 = F_3 - 1$. A 0,$i$-node of rank $k$ has a child of rank $k$, and so at least $F_{k+3} - 1$ nodes. A 1,1- or 1,2-node of rank $k$ has children of ranks at least $k - 1$ and $k - 2$, so at least $1 + (F_{k+2} - 1) + (F_{k+1} - 1) = F_{k+3} - 1$ nodes. A root of rank $k$ has a left child of rank $k - 1$, so its half tree has at least $F_{k+2} \ge \varphi^k$ nodes. So every rank is at most $\log_\varphi n$.

**The potential.** For a node $x$, let $\sigma(x)$ be the sum of the rank differences of its children, where a missing child counts with its rank $-1$, but the missing right child of a root does not count. Let $\psi(x) = \sigma(x) - 1$ for every node. For a root, $\sigma(x) = 1$ and $\psi(x) = 0$. Define the potential of a node as $\phi(x) = 1$ for a root, $\phi(x) = 0$ for a 1,1-node, and $\phi(x) = \sigma(x) - 1$ for every other non-root. This is the potential of the paper: a root with a 1-child has potential 1, a 1,1-node has 0, and an $i,j$-node other than a 1,1-node has $i + j - 1$. Every $\phi(x) \ge 0$: a 1,2-node has 2, and a 0,$i$-node with $i > 1$ has at least 1. Let $\Phi$ be the sum over all nodes. The empty heap has $\Phi = 0$.

Count one unit of time for each operation, each half tree processed in delete-min, each link and each iteration of the rank-reduction loop.

**Insert, meld, find-min.** Insert adds a root, $\Delta\Phi = 1$, so the amortized cost is 2. Meld and find-min do not change $\Phi$.

**Delete-min.** Deleting the root $z$ lowers $\Phi$ by 1. The disassembly makes each node on the right spine of $z.left$ a root, with $\phi = 1$. Each spine node that was not a 1,1-node had $\phi \ge 1$, and its children do not change, so its potential does not increase. For a 1,1-node $s$ on the spine, its right child, the next spine node, has rank $r(s) - 1$. Ranks along the spine never increase, because rank differences are not negative. So the 1,1-nodes on the spine have distinct ranks, all less than $r(z) \le \log_\varphi n$, and there are at most $\log_\varphi n$ of them. The disassembly raises $\Phi$ by at most $\log_\varphi n$.

Let $h$ be the number of half trees after the disassembly. The rest of the operation takes $h + O(1)$ units plus one per link. Each link turns a root ($\phi = 1$) into a 1,1-node ($\phi = 0$) and does not change the children of any other node, except that the winner gets a new left child. The winner is a root, with $\phi = 1$ before and after. So each link lowers $\Phi$ by 1, which pays for the link. After multipass linking, the roots have distinct ranks in $\{0, \ldots, \lfloor \log_\varphi n \rfloor\}$, so at most $\log_\varphi n + 1$ remain, and there were at least $h - \log_\varphi n - 1$ links. The amortized cost is at most
$$h + O(1) + \log_\varphi n - (h - \log_\varphi n - 1) = 2 \log_\varphi n + O(1).$$

**Decrease-key.** If $x$ is a root, the cost is 1 and $\Phi$ does not change. Otherwise let $u_1 = u$ be the parent of $x$, let $y$ be its right child, and let $u_1, u_2, \ldots, u_m$ be the non-roots whose ranks decrease, in this order; $u_{i+1}$ is the parent of $u_i$. Let $\delta_i \ge 1$ be the decrease at $u_i$, and let $w$ be the node at which the loop ends (a non-root whose rank does not change, or a root).

*Claim A: at most one of $u_1, \ldots, u_m$ is a 1,1-node before the operation, and every $\delta_i$ after the first 1,1-node among them is 1.* A 1,1-node of rank $k$ has children of rank $k - 1$; if one of them loses rank, $f$ gives $k$ (if the child has rank $k - 2$) or $k - 1$ (if less), so a 1,1-node decreases by at most 1. By Lemma 2 of the correctness proof, a node whose child decreased by 1 decreases by at most 1. So once a 1,1-node $t$ decreases, every later decrease is by exactly 1. A later 1,1-node whose child decreases by exactly 1 has children of ranks $k - 1$ and $k - 2$, so $f = k$ and it does not decrease. So it is $w$, not one of the $u_i$.

*Accounting.* Let $\Psi = \sum_x \psi(x)$ over all nodes, where $\psi(x) = \sigma(x) - 1$ for every node, root or not. Let $N$ be the number of 1,1-nodes. Since $\phi(x) = \psi(x)$ for all nodes except 1,1-nodes and roots, and $\phi = \psi - 1$ for a 1,1-node and $\phi = \psi + 1$ for a root, we have $\Phi = \Psi - N + R$, where $R$ is the number of roots.

- $\Delta R = +1$ (the root $x$).
- $-\Delta N$ is at most the number of nodes that stop being 1,1-nodes. Only nodes whose children's rank differences change can change type: $x$, the $u_i$, and $w$. By Claim A at most one $u_i$ is a 1,1-node. So $-\Delta N \le 3$.
- $\Delta\Psi$. Before, $\psi(x) = \Delta(x.left) + \Delta(y) - 1$, where $\Delta(y) = r(x) - r(y)$; after, $x$ is a root, with $\psi(x) = 0$. When $y$ replaces $x$ as a child of $u_1$, the rank difference of that child of $u_1$ grows from $\Delta(x)$ to $\Delta(x) + \Delta(y)$, so $\psi(u_1)$ grows by $\Delta(y)$. When the rank of $u_i$ drops by $\delta_i$, the rank differences of both its children drop by $\delta_i$, so $\psi(u_i)$ drops by $2\delta_i$, and the rank difference of $u_i$ as a child of $u_{i+1}$ (or of $w$) grows by $\delta_i$, which raises $\psi$ of the parent by $\delta_i$. If $w$ is a root, its rank is reset to make it a 1-node, so $\psi(w) = 0$ before and after the operation. Adding up,
$$\Delta\Psi \le 1 - \Delta(x.left) - \Delta(y) + \Delta(y) - \sum_{i=1}^{m} 2\delta_i + \sum_{i=1}^{m} \delta_i \le 1 - m,$$
because $\Delta(x.left) \ge 0$ and every $\delta_i \ge 1$.

So $\Delta\Phi \le (1 - m) + 3 + 1 = 5 - m$. The actual cost is 1 for the cut and $m + 1$ for the iterations of the loop. The amortized cost of decrease-key is at most $(m + 2) + (5 - m) = 7$, which is $O(1)$. $\blacksquare$
