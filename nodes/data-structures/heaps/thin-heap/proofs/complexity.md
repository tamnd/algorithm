---
title: Amortized cost of the thin heap
proves: [time.amortized]
status: full
---

We prove that insert, meld, find-min and decrease-key take $O(1)$ amortized time and that delete-min takes $O(\log n)$ amortized time, where $n$ is the number of items at the time of the operation.

**Cost units.** Count one unit for each operation, one unit for each root that delete-min puts into the buckets, one unit for each link, and one unit for each iteration of the loop of decrease-key. Every other step of an operation takes constant time per unit.

**Potential.** Let $t$ be the number of trees and $h$ the number of thin nodes, and let $\Phi = 2t + 4h$. The empty heap has $\Phi = 0$, and $\Phi \ge 0$ always, so the total actual cost of any sequence that starts from an empty heap is at most the total amortized cost.

**Insert and meld.** Insert has actual cost 1 and adds one tree, so its amortized cost is $1 + 2 = 3$. Meld has actual cost 1 and does not change $t$ or $h$ of the union. Find-min has actual cost 1.

**Decrease-key.** If $x$ is a root, the actual cost is 1 and $\Phi$ does not change. Otherwise the cut at line L9 adds one tree, $\Delta\Phi \le +2$ (and $-4$ more if $x$ was thin). Consider the iterations of the loop.
- An iteration that ends at line L14 cuts a thin node $y$ (a parent defect with $r(y) - c = 3$ means that $y$ was thin before the operation started the iteration, with first child of rank $c + 1 = r(y) - 2$) and makes it a normal root: $\Delta t = +1$, $\Delta h = -1$, $\Delta\Phi = -2$. With the actual cost of 1, the amortized cost is $-1$.
- An iteration at line L16 makes the thin node $y$ normal: $\Delta\Phi = -4$, amortized $-3$.
- The last iteration returns at line L12, L13 or L15. Line L12 changes only the rank of a root, which stays normal. Lines L13 and L15 make $y$ thin. So $\Delta\Phi \le +4$, and the amortized cost is at most 5.

So the amortized cost of decrease-key is at most $1 + 2 + 5 = 8$.

**Delete-min.** Let $t$ be the number of trees before, let $d$ be the number of children of the minimum $z$, and let $t'$ be the number of trees after. Lemma 1 of the correctness proof gives $d = r(z) \le \log_\varphi n + 1$. The operation puts $t - 1 + d$ roots into the buckets, and each link removes one tree, so it makes $\ell = t - 1 + d - t'$ links. It may make thin children normal (line L4), and it makes no node thin, so $\Delta h \le 0$. The actual cost is $1 + (t - 1 + d) + \ell + t'$, where the last term pays for building the new root list, and
$$\text{amortized} \le 1 + (t - 1 + d) + (t - 1 + d - t') + t' + 2(t' - t) = 2d - 1 + 2t'.$$
After the links, the roots have distinct ranks, all at most $\log_\varphi n + 1$ by Lemma 1, so $t' \le \log_\varphi n + 2$. The amortized cost is at most $4 \log_\varphi n + 5 = O(\log n)$. $\blacksquare$
