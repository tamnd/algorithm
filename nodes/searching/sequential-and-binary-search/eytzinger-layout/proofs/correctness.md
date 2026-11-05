---
title: The Eytzinger lower bound search returns the slot of the first item not less than x, or 0
proves: [correctness, termination, complexity]
status: full
---

Let $B[1 \ldots n]$, $n \ge 0$, be built by EYTZINGER-BUILD from a sorted array $A[0 \ldots n-1]$. The implicit tree has the slots $1, \ldots, n$, and slot $k$ has the children $2k$ and $2k + 1$ when they are at most $n$. For a slot $k$, write $\pi(k)$ for its position in the in-order walk (left subtree, node, right subtree) from the root. Let $x$ be a key and $\ell = |\{j : A[j] < x\}|$.

**The build.** FILL visits the slots in in-order and writes $A[0], A[1], \ldots$ in that order, so $B[k] = A[\pi(k)]$ and $R[k] = \pi(k)$. Hence items in in-order are sorted, and the slot with $\pi(k) = \ell$, when $\ell < n$, holds the lower bound of $x$. We prove that EYTZINGER-LOWER-BOUND returns that slot when $\ell < n$ and 0 when $\ell = n$.

**In-order facts.** For a slot $k$, every slot in the left subtree of $k$ has a smaller $\pi$ than $k$, and every slot in the right subtree a larger one. Since $B[k] = A[\pi(k)]$ and $A$ is sorted, $\pi(k) < \ell$ holds exactly when $B[k] < x$.

**The walk.** Let $k_0 = 1, k_1, \ldots, k_h$ be the values of $k$ at the tests of line L9, so $k_0, \ldots, k_{h-1} \le n$ and $k_h > n$, and let $c_t = [B[k_t] < x]$, so $k_{t+1} = 2k_t + c_t$. The walk stops: $k$ at least doubles in each pass, so $h \le \lfloor \lg n \rfloor + 1$. Each $k_{t+1}$ with $t + 1 < h$ is a child of $k_t$, so $k_0, \ldots, k_{h-1}$ is a path from the root; and $k_h$ is the number of a missing child of $k_{h-1}$. If $n = 0$ then $h = 0$, $k_0 = 1$, and the result below is 0, which is correct.

**Claim.** Let $S$ be the set of steps $t < h$ with $c_t = 0$. If $S$ is empty then $\ell = n$. Otherwise, with $s = \max S$, $\pi(k_s) = \ell$.

*Proof of the claim.* Every slot $q$ of the tree is either some $k_t$ with $t < h$, or lies in the subtree of the child of some $k_t$ that the walk did not take; for $t = h - 1$ the walk leaves the tree, so the other child of $k_{h-1}$ is the only one not taken there. Take such a $q$.

- If $q = k_t$ with $c_t = 1$, then $\pi(q) < \ell$.
- If $q$ is in the left subtree of $k_t$ and the walk went right at $k_t$ ($c_t = 1$), then $\pi(q) < \pi(k_t) < \ell$.
- If $q = k_t$ with $c_t = 0$, then $\pi(q) \ge \ell$.
- If $q$ is in the right subtree of $k_t$ and the walk went left ($c_t = 0$), then $\pi(q) > \pi(k_t) \ge \ell$.

So the slots with $\pi \ge \ell$ are exactly the nodes $k_t$ with $t \in S$ and the right subtrees of those nodes. If $S$ is empty, no slot has $\pi \ge \ell$, so $\ell = n$. Otherwise, let $s = \max S$. For $t \in S$ with $t < s$, the walk went left at $k_t$, so $k_s$ is in the left subtree of $k_t$, and so is the right subtree of $k_s$; hence $\pi(k_s) < \pi(k_t)$ and $\pi(k_s)$ is less than every $\pi$ in the right subtree of $k_t$. Also every slot in the right subtree of $k_s$ has $\pi > \pi(k_s)$. So $k_s$ has the smallest $\pi$ among the slots with $\pi \ge \ell$. Since $\pi$ takes every value $0, \ldots, n - 1$ once and the slots with $\pi \ge \ell$ are those with $\pi \in \{\ell, \ldots, n-1\}$, this smallest value is $\ell$. $\square$

**The bits.** By $k_{t+1} = 2k_t + c_t$ and $k_0 = 1$, the binary form of $k_h$ is $1\, c_0\, c_1 \cdots c_{h-1}$, and the binary form of $k_s$ is $1\, c_0 \cdots c_{s-1}$. If $S$ is empty, $k_h = 2^{h+1} - 1$ has all its $h + 1$ bits equal to 1, so it has $t = h + 1$ trailing 1 bits, and line L11 gives $k_h >> (h + 2) = 0$. If $S$ is not empty, the bits after $c_s = 0$ are all 1, since $s$ is the last left turn, so $k_h$ has exactly $t = h - 1 - s$ trailing 1 bits, preceded by the 0 bit $c_s$. Shifting right by $t + 1 = h - s$ removes $c_s, \ldots, c_{h-1}$ and leaves $1\, c_0 \cdots c_{s-1} = k_s$.

With the claim, line L12 returns $k_s$, the slot with $\pi(k_s) = \ell$, when $\ell < n$, and 0 when $\ell = n$.

**The count.** The walk makes $h$ comparisons, where $h = \lfloor \lg k_h \rfloor$ is the depth of the external position $k_h$. Since $n < k_h \le 2n + 1$, we get $\lfloor \lg(n+1) \rfloor \le h \le \lfloor \lg(2n+1) \rfloor = \lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$ for $n \ge 1$. $\blacksquare$
