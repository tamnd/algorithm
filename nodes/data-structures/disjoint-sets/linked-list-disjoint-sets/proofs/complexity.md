---
title: With weighted union, m operations on n elements take O(m + n log n) time
proves: [time.amortized, time.total]
status: full
---

Consider a sequence of $m$ operations MAKE-SET, FIND and UNION, of which $n$ are MAKE-SET, on linked-list disjoint sets with the weighted-union rule of line L6. We prove that the sequence takes $O(m + n \log n)$ time.

**Cost of each operation.** MAKE-SET and FIND do a constant number of steps. A UNION with $S = T$ does a constant number of steps. A UNION with $S \ne T$ does a constant number of steps outside line L7, and line L7 does one step for each element of the list of the smaller set $S$, each of which gets a new value of `set`. So the total time is $O(m + M)$, where $M$ is the total number of times that some element gets a new value of `set` at line L7.

**Each element moves at most $\lfloor \lg n \rfloor$ times.** Fix an element $x$. Let $\sigma(x)$ be the size of the set of $x$; it never falls, because sets only merge. Suppose $x$ moves at line L7 of some union. Then $x$ is in the set $S$ after line L6, so $|S| \le |T|$, and after the union $x$ is in a set of size $|S| + |T| \ge 2|S|$. So each move of $x$ at least doubles $\sigma(x)$. Before its first move $\sigma(x) \ge 1$, so after $k$ moves $\sigma(x) \ge 2^k$. A set has at most $n$ elements, so $2^k \le n$, and $k \le \lfloor \lg n \rfloor$.

**Sum.** Each of the $n$ elements moves at most $\lfloor \lg n \rfloor$ times, so $M \le n \lfloor \lg n \rfloor$, and the total time is $O(m + n \log n)$. Since $m \ge n$, this is at most $O(\log n)$ per operation on average, which gives the amortized bound: with the [accounting method](/accounting-method/), charge $1 + \lfloor \lg n \rfloor$ to each MAKE-SET and $1$ to each other operation; each move at line L7 is paid by one unit of the element that moves, and no element runs out. $\blacksquare$

**The bound is tight.** Let $n = 2^k$, and do the unions in $k$ rounds: in round $j$, pair up the $2^{k-j+1}$ sets of size $2^{j-1}$ and merge each pair. Each union of two sets of size $2^{j-1}$ moves $2^{j-1}$ elements, and there are $2^{k-j}$ such unions, so each round moves $n/2$ elements, and the $k$ rounds move $(n/2) \lg n$. With $m = 2n - 1$ operations, the total is $\Theta(m + n \log n)$.
