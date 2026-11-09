---
title: Greedy path relinking on bit strings walks a shortest path from the initiating to the guiding solution and returns its best point
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The solutions are bit strings of length $n$, $f$ is a cost to minimize, $x^s$ is the initiating solution and $x^t$ is the guiding solution. Write $\Delta(x, y) = \{ i : x_i \ne y_i \}$, so $|\Delta(x, y)|$ is the [Hamming distance](/hamming-distance/) of $x$ and $y$, and write $h = |\Delta(x^s, x^t)|$. Let $x^{(0)} = x^s$ and let $x^{(k)}$ be the value of $x$ after the $k$-th pass of the loop.

**Lemma 1 (invariant).** Before and after each pass of the loop, the set $\Delta$ held by the algorithm equals $\Delta(x, x^t)$.

*Proof.* Line L2 sets $\Delta = \Delta(x^s, x^t)$ with $x = x^s$. Suppose $\Delta = \Delta(x, x^t)$ before a pass, and line L4 picks $i \in \Delta$. Then $x_i \ne x^t_i$, and since the values are bits, flipping $x_i$ makes $x_i = x^t_i$. No other position changes. So the new set of differing positions is $\Delta(x, x^t) \setminus \{i\}$, which is what line L5 stores. $\square$

**Lemma 2 (termination and the path).** The loop makes exactly $h$ passes and ends with $x = x^t$. The points $x^{(0)}, \ldots, x^{(h)}$ are distinct, consecutive points differ in one bit, and $x^{(k)}$ is at Hamming distance $h - k$ from $x^t$ and $k$ from $x^s$.

*Proof.* By Lemma 1, each pass removes one element from $\Delta$, which starts with $h$ elements, and the loop stops when $\Delta$ is empty. Then $\Delta(x, x^t) = \emptyset$, so $x = x^t$. After pass $k$, $|\Delta| = h - k$, so the distance to $x^t$ is $h - k$; these distances are different for different $k$, so the points are distinct. Each pass flips one bit that differs from $x^s$ and has not been flipped before, so after $k$ passes exactly $k$ bits differ from $x^s$. $\square$

So the walk is a shortest path from $x^s$ to $x^t$ in the one-flip neighborhood graph of the hypercube: no path has fewer than $h$ one-bit steps.

**Lemma 3 (the greedy step).** At pass $k$, $f(x^{(k)}) = \min_{i \in \Delta} f(\text{flip}(x^{(k-1)}, i))$, where $\Delta = \Delta(x^{(k-1)}, x^t)$.

*Proof.* This is line L4, with Lemma 1 for the value of $\Delta$. $\square$

**Theorem (correctness).** PATH-RELINKING stops after $h$ passes and returns a point $b$ of the path $x^{(0)}, \ldots, x^{(h)}$ with $f(b) = \min_k f(x^{(k)})$. In particular $f(b) \le \min(f(x^s), f(x^t))$.

*Proof.* Termination is Lemma 2. Line L1 sets $b = x^{(0)}$, and line L6 replaces $b$ by $x^{(k)}$ exactly when $f(x^{(k)}) < f(b)$, so after pass $k$, $f(b) = \min_{j \le k} f(x^{(j)})$. After the last pass this is the minimum over the whole path, which includes $x^{(0)} = x^s$ and $x^{(h)} = x^t$. $\blacksquare$

**What is not claimed.** The path is one of $h!$ shortest paths between $x^s$ and $x^t$, chosen greedily one step at a time; the best point of another path can be better. The returned point need not be a local minimum of the one-flip neighborhood, which is why codes often run a local search from it. Path relinking has no guarantee of finding a global minimum, and the path between two solutions can miss every good point between them.
