---
tag: 71155N
kind: theorem
slug: savitch-theorem
name: Savitch's theorem
aliases:
- NL in DSPACE(log^2 n)
area: complexity/complexity-classes
level: advanced
summary: A nondeterministic machine with space s(n) at least log n can be simulated by a deterministic one with space O(s(n)^2). So NL is in DSPACE(log^2 n) and NPSPACE = PSPACE.
prereqs: [nondeterministic-logspace, pspace, graph-reachability, space-complexity]
see_also: [immerman-szelepcsenyi-theorem, space-hierarchy-theorem, logspace, sc-class, expspace, nondeterministic-turing-machine, symmetric-logspace]
sources:
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2), 177 to 192 (1970)
    locator: the main theorem (simulation of an L(n) tape-bounded nondeterministic machine in [L(n)]^2 deterministic tape, for L(n) at least log n)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 8.1, Savitch's Theorem
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity (Savitch's theorem)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 7, Relations between Complexity Classes (the reachability method)
---

Savitch's theorem says that nondeterminism saves at most a square in space: a nondeterministic machine that uses space $s(n) \ge \log n$ can be simulated by a deterministic machine that uses space $O(s(n)^2)$. The proof decides [reachability](/graph-reachability/) in a directed graph with $N$ vertices in $O(\log^2 N)$ space, by recursion on a midpoint, and applies it to the graph of configurations of the machine. The consequences are $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n)$ and $\mathsf{NPSPACE} = \mathsf{PSPACE}$. For time, no result of this kind is known: the best known deterministic simulation of nondeterministic time $t$ takes time $2^{O(t)}$.

## Statement

The model is the multitape Turing machine with a read-only input tape, and the space counts only the work tapes; see [L](/logspace/). A function $s$ is *space-constructible* if a deterministic machine, on input $1^n$, writes $s(n)$ in binary using $O(s(n))$ space. The functions $\lceil \log_2 n \rceil$, $n^k$ and $2^n$ are space-constructible.

**Lemma (reachability).** Reachability in a directed graph with $N$ vertices can be decided by a deterministic machine in $O(\log^2 N)$ space.

**Theorem (Savitch 1970).** Let $s(n) \ge \log_2 n$ be space-constructible. Then

$$\mathsf{NSPACE}(s(n)) \subseteq \mathsf{DSPACE}(s(n)^2).$$

**Corollaries.** $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n)$, $\mathsf{NPSPACE} = \mathsf{PSPACE}$ and $\mathsf{NEXPSPACE} = \mathsf{EXPSPACE}$.

## In plain words

Suppose a machine that may guess solves a problem with some amount of memory. Then a machine that never guesses can solve it with the square of that memory.

The key question is whether one state of the guessing machine can lead to another within a given number of steps. To answer it, try every possible state for the halfway point. For each one, ask two smaller questions: can the first state reach the halfway state in half the steps, and can the halfway state reach the last state in the other half? Answer them one after the other with the same memory. Each question halves the number of steps, so the chain of open questions stays short, and each open question needs only a little memory.

The price is time. The machine solves the same small questions again and again, so it is very slow.

## Proof

**The recursion.** Let $G = (V, E)$ be a directed graph with $N$ vertices. For vertices $u, v$ and an integer $t \ge 0$, let $\mathrm{REACH}(u, v, t)$ be true if $G$ has a path from $u$ to $v$ with at most $t$ edges.

```pseudo id=reach
REACH(u, v, t)
L1  if t = 0 then return (u = v)
L2  if t = 1 then return (u = v or (u, v) ∈ E)
L3  for each vertex w ∈ V do
L4      if REACH(u, w, ⌈t/2⌉) and REACH(w, v, ⌊t/2⌋) then
L5          return true
L6  return false
```

*Correctness, by induction on $t$.* Lines L1 and L2 are correct by definition. Let $t \ge 2$. If a path from $u$ to $v$ has $\ell \le t$ edges, let $w$ be its vertex after $\min(\ell, \lceil t/2 \rceil)$ edges. Then the part from $u$ to $w$ has at most $\lceil t/2 \rceil$ edges and the part from $w$ to $v$ has at most $\ell - \min(\ell, \lceil t/2 \rceil) \le \lfloor t/2 \rfloor$ edges, so both calls at L4 return true for this $w$, by the induction hypothesis. Conversely, if both calls return true for some $w$, the two paths join into a walk from $u$ to $v$ with at most $\lceil t/2 \rceil + \lfloor t/2 \rfloor = t$ edges, and a walk contains a path that is no longer. So the result is correct.

*Space.* A deterministic machine runs the recursion with a stack on a work tape. A frame holds $u$, $v$, $w$ and $t$, and one bit that says which of the two calls at L4 is open. With $t \le N$, a frame has $O(\log N)$ bits. Each call replaces $t$ by at most $\lceil t/2 \rceil$, so after $\lceil \log_2 t \rceil$ levels $t$ is at most 1, and the stack never has more than $\lceil \log_2 t \rceil + 1$ frames. When a call returns, its frame is erased and the space is used again. For $t = N - 1$, a shortest path has at most $N - 1$ edges, so $\mathrm{REACH}(s, t', N-1)$ decides reachability from $s$ to $t'$ in $O(\log^2 N)$ space. This proves the lemma.

*On a small graph.* Take the directed path $0 \to 1 \to \cdots \to 7$, with $N = 8$. The call $\mathrm{REACH}(0, 7, 7)$ returns true, its recursion goes 3 levels below the top call, and it makes 458 calls in total. The call $\mathrm{REACH}(7, 0, 7)$ returns false after 811 calls, which try every midpoint. For the path on 16 vertices, the two calls make 52947 and 88724 calls with 4 levels. The depth grows like $\log_2 N$, and the number of calls grows like $N^{O(\log N)}$: the time satisfies $T(t) \le 2N\, T(\lceil t/2 \rceil) + O(N)$, so $T(N) = N^{O(\log N)}$.

**The simulation.** Let a nondeterministic machine $M$ decide $A$ in space $s(n) \ge \log_2 n$. As on the page for [NL](/nondeterministic-logspace/), change $M$ so that it has a single accepting configuration $C_{\mathrm{acc}}$: before it accepts, it erases its work tapes and moves its heads to the left end.

A configuration of $M$ on an input $x$ of length $n$ is the state, the input head position, which takes $\lceil \log_2(n+2) \rceil$ bits, the work head positions and the work tape contents. So it fits in $d \cdot s(n)$ bits for a constant $d$ that depends on $M$. Here the condition $s(n) \ge \log_2 n$ is used: for smaller $s$, the input head position alone would not fit. The number of configurations is at most $2^{d\, s(n)}$.

The deterministic machine $D$ works as follows on input $x$. It computes $s(n)$, which it can do in space $O(s(n))$ because $s$ is space-constructible. Then it runs $\mathrm{REACH}(C_0, C_{\mathrm{acc}}, 2^{d\, s(n)})$ on the configuration graph of $M$ on $x$, where $C_0$ is the start configuration, and it accepts if the result is true. $D$ never writes the configuration graph down. To test an edge $C \to C'$ at line L2, it reads the input symbol at the input head position of $C$ and checks the fixed transition table of $M$. To go through all vertices $w$ at line L3, it goes through all strings of $d \cdot s(n)$ bits.

$M$ accepts $x$ if and only if $C_{\mathrm{acc}}$ is reachable from $C_0$. A shortest path visits each configuration at most once, so it has fewer than $2^{d\, s(n)}$ edges, and the call is correct by the analysis above. Each frame has $O(s(n))$ bits and the recursion has at most $d\, s(n) + 1$ levels, so $D$ uses $O(s(n)^2)$ space. $\blacksquare$

**Without constructibility.** The condition that $s$ is space-constructible can be removed. $D$ tries $b = 1, 2, 3, \ldots$ in turn. For each $b$, it decides with REACH, restricted to configurations of space at most $b$, whether $C_{\mathrm{acc}}$ is reachable; if so, it accepts. Otherwise it decides whether some configuration that uses $b + 1$ work cells is reachable in one step from a configuration of space at most $b$ that is itself reachable. If not, $M$ never uses more than $b$ cells on $x$, so $D$ rejects. Otherwise it goes on with $b + 1$. It stops with $b \le s(n)$, so the space is still $O(s(n)^2)$.

## Consequences

- $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n)$. This does not settle L against NL: the space hierarchy theorem gives $\mathsf{L} \subsetneq \mathsf{DSPACE}(\log^2 n)$, so NL can lie anywhere between the two. See [L](/logspace/) and [NL](/nondeterministic-logspace/).
- $\mathsf{NSPACE}(n^k) \subseteq \mathsf{DSPACE}(n^{2k})$, so $\mathsf{NPSPACE} = \mathsf{PSPACE}$. This is why [PSPACE](/pspace/) has no separate nondeterministic version. In the same way, $\mathsf{NEXPSPACE} = \mathsf{EXPSPACE}$; see [EXPSPACE](/expspace/).
- The context-sensitive languages are $\mathsf{NSPACE}(n)$, so they are in $\mathsf{DSPACE}(n^2)$.
- $\mathsf{NL} \subsetneq \mathsf{PSPACE}$: with the [space hierarchy theorem](/space-hierarchy-theorem/), $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n) \subsetneq \mathsf{DSPACE}(n) \subseteq \mathsf{PSPACE}$.
- The deterministic reachability algorithm takes $n^{O(\log n)}$ time. Whether reachability can be solved in polynomial time and polylogarithmic space at the same time, that is whether $\mathsf{NL} \subseteq \mathsf{SC}$, is open; see [SC](/sc-class/).

## Tightness

Nobody knows whether the square is needed. No simulation of $\mathsf{NSPACE}(s)$ in $\mathsf{DSPACE}(s^{2-\varepsilon})$ for a constant $\varepsilon > 0$ is known, and none is ruled out; such a simulation for $s = \log n$ would already be a new result about NL. For undirected graphs the answer is better: reachability is in L by Reingold's theorem ([SL](/symmetric-logspace/)), so no square is needed there.

The condition $s(n) \ge \log n$ is part of the statement. Below $\log n$ the proof breaks, because a configuration must record the input head position.

The theorem trades time for space. The recursion takes $2^{O(s(n)^2)}$ time in general, while a breadth-first search of the configuration graph takes $2^{O(s(n))}$ time but $2^{O(s(n))}$ space.

## History

Walter Savitch proved the theorem in 1970, in terms of threading mazes, which is the reachability problem. The same paper notes a padding consequence: if nondeterministic and deterministic space agree at a small bound, then they agree at every larger bound. The first "LBA problem", whether $\mathsf{NSPACE}(n) = \mathsf{DSPACE}(n)$, is still open. The second, whether $\mathsf{NSPACE}(n)$ is closed under complement, was solved in 1987 and 1988 by the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/).

## References
