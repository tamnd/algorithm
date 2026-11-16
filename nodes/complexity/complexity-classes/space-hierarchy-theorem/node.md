---
tag: 85C1ZJ
kind: theorem
slug: space-hierarchy-theorem
name: Space hierarchy theorem
aliases:
- deterministic space hierarchy
area: complexity/complexity-classes
level: advanced
summary: "More space decides more problems: if g is space-constructible, g(n) is at least log n and f = o(g), then DSPACE(f) is a proper subset of DSPACE(g)."
prereqs: [space-complexity, multitape-turing-machine, logspace]
see_also: [time-hierarchy-theorem, savitch-theorem, immerman-szelepcsenyi-theorem, diagonalization-argument, pspace, expspace, nondeterministic-logspace, universal-turing-machine]
sources:
  - paper: doi:10.1109/FOCS.1965.11
    title: Richard E. Stearns, Juris Hartmanis and Philip M. Lewis II, Hierarchies of memory limited computations, 6th Annual Symposium on Switching Circuit Theory and Logical Design, 179 to 190 (1965)
    locator: the space hierarchy for off-line machines
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 9.1, Hierarchy Theorems (space constructibility and the space hierarchy)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity (the space hierarchy theorem)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 7, Relations between Complexity Classes (the hierarchy theorems)
---

The space hierarchy theorem says that a deterministic Turing machine can decide more languages when it is given asymptotically more space. If $g$ is space-constructible, $g(n) \ge \log n$ and $f(n) = o(g(n))$, then some language is decided in space $O(g(n))$ but not in space $O(f(n))$. The proof is a diagonalization, as for the [time hierarchy theorem](/time-hierarchy-theorem/), but the simulation of one machine by another costs only a constant factor in space, so the condition is $f = o(g)$ and not $f \log f = o(g)$. The theorem gives $\mathsf{L} \subsetneq \mathsf{DSPACE}(\log^2 n)$, $\mathsf{L} \subsetneq \mathsf{PSPACE}$ and $\mathsf{PSPACE} \subsetneq \mathsf{EXPSPACE}$, and with Savitch's theorem $\mathsf{NL} \subsetneq \mathsf{PSPACE}$.

## Statement

The model is the deterministic [multitape Turing machine](/multitape-turing-machine/) with a read-only input tape; only the work tapes count. $\mathsf{DSPACE}(s(n))$ is the class of languages decided by such a machine that halts on every input and uses $O(s(n))$ work cells on inputs of length $n$; see [L](/logspace/). A function $g$ is *space-constructible* if a deterministic machine, on input $1^n$, writes $g(n)$ in binary using $O(g(n))$ work cells. The functions $\lceil \log_2 n \rceil$, $\lceil \log_2 n \rceil^2$, $n^k$ and $2^n$ are space-constructible.

**Theorem (Stearns, Hartmanis and Lewis 1965).** Let $f, g : \mathbb{N} \to \mathbb{N}$ with $f(n) \ge 1$, let $g$ be space-constructible with $g(n) \ge \log_2 n$, and let $f(n) = o(g(n))$. Then

$$\mathsf{DSPACE}(f(n)) \subsetneq \mathsf{DSPACE}(g(n)).$$

## In plain words

Give a computer more memory and it can solve problems that it could not solve before, as long as the extra memory grows faster than any fixed multiple of the old amount.

The proof builds a contrary machine. It reads its input as the description of another machine, runs that machine on the same input inside a fixed amount of memory, and gives the opposite answer. Every machine that uses less memory meets an input where the contrary machine has enough room to finish the run, and there the two disagree.

Running one machine inside another costs only a constant factor in memory, so the gap can be smaller than for time. The contrary machine also counts steps, so that it stops a machine that runs for ever in a loop.

## Proof

**Configurations.** Let $M$ be a machine with $k$ work tapes, states $Q_M$ and work alphabet $\Gamma_M$, that uses at most $S$ work cells on an input of length $n$. A configuration of $M$ is fixed by the state, the input head position, the work head positions and the work tape contents, so $M$ has at most

$$|Q_M| \cdot (n + 2) \cdot S^k \cdot |\Gamma_M|^{k S} \le (n + 2) \cdot 2^{a_M S}$$

configurations, for a constant $a_M$ that depends on $M$ and for $S \ge 1$. A halting deterministic machine never repeats a configuration, so if $M$ halts, it halts within this many steps.

**The diagonal machine.** Fix an encoding $\langle M \rangle$ of machines as binary strings. On an input $x$ of length $n$, the machine $D$ works as follows. It has a simulation tape and a counter tape.

```pseudo id=diag
D(x)
L1  n ← |x|; compute g(n) and mark g(n) cells on the simulation tape
L2  if x is not 1^k 0 w with w = ⟨M⟩ for a machine M then reject
L3  copy ⟨M⟩ into the marked cells, or reject if it does not fit; set the counter, of ⌈log2(n+2)⌉ + g(n) bits, to 0
L4  repeat
L5      if the next step of M needs a cell outside the marked region then reject
L6      if the counter overflows then reject
L7      simulate one step of M on x; add 1 to the counter
L8  until M halts
L9  if M accepted x then reject else accept
```

In line L7, $D$ keeps the $k$ work tapes of $M$ on $k$ tracks of the simulation tape, with a mark for each head. It stores each symbol of $\Gamma_M$ in a block of $d_M$ cells, where $d_M$ depends only on $M$, so $S$ cells of $M$ take $d_M S$ cells of $D$, plus the copy of $\langle M \rangle$ that $D$ reads to find the next move. $M$ reads the same input $x$ as $D$, so $D$ uses its own input head as the input head of $M$; it does not need to store the input position.

**D uses space $O(g(n))$ and halts.** Line L1 uses $O(g(n))$ cells because $g$ is space-constructible. The simulation tape never leaves the $g(n)$ marked cells, because of line L5. The counter has $\lceil \log_2(n+2) \rceil + g(n)$ bits, which is $O(g(n))$ because $g(n) \ge \log_2 n$. This is where the condition $g(n) \ge \log n$ is used. Line L6 stops the loop after at most $2^{\lceil \log_2(n+2) \rceil + g(n)}$ steps, so $D$ halts on every input. So $L(D) \in \mathsf{DSPACE}(g(n))$.

**$L(D)$ is not in $\mathsf{DSPACE}(f(n))$.** Suppose a machine $M$ decides $L(D)$ and uses at most $S(n) = c f(n)$ work cells, for a constant $c$. The simulation of $M$ on an input of length $n$ needs at most $d_M c f(n) + e_M$ cells of $D$, where the constant $e_M$ covers the copy of $\langle M \rangle$ and the current state of $M$. $M$ halts within $(n + 2) \cdot 2^{a_M c f(n)}$ steps. Since $f = o(g)$ and $g(n) \to \infty$, there is an $n_0$ such that for all $n \ge n_0$:

$$d_M c f(n) + e_M \le g(n) \quad\text{and}\quad a_M c f(n) < g(n).$$

Choose $k$ such that $x = 1^k 0 \langle M \rangle$ has length $n \ge n_0$. On this $x$, the simulation stays in the marked cells by the first inequality, and $M$ halts before the counter overflows by the second, because $(n+2) \cdot 2^{a_M c f(n)} < 2^{\lceil \log_2(n+2) \rceil + g(n)}$. So $D$ reaches line L9 and gives the opposite answer of $M$ on $x$. Then $x \in L(D)$ if and only if $x \notin L(M)$, which contradicts $L(M) = L(D)$. $\blacksquare$

## Consequences

- **Logarithmic space.** $\mathsf{L} \subsetneq \mathsf{DSPACE}(\log^2 n)$, since $\log n = o(\log^2 n)$. More generally $\mathsf{DSPACE}(\log^a n) \subsetneq \mathsf{DSPACE}(\log^b n)$ for integers $1 \le a < b$.
- **Polynomial space.** $\mathsf{DSPACE}(n^a) \subsetneq \mathsf{DSPACE}(n^b)$ for rational numbers $1 \le a < b$.
- **PSPACE.** Every power of $\log n$ is $o(n)$, so $\mathsf{L} \subseteq \mathsf{DSPACE}(\log^2 n) \subsetneq \mathsf{DSPACE}(n) \subseteq \mathsf{PSPACE}$, and polylogarithmic space is a proper subset of [PSPACE](/pspace/). With [Savitch's theorem](/savitch-theorem/), $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n) \subsetneq \mathsf{PSPACE}$. So no PSPACE-complete problem, such as [QSAT](/qsat/), is in NL.
- **EXPSPACE.** $\mathsf{PSPACE} \subseteq \mathsf{DSPACE}(2^n) \subsetneq \mathsf{DSPACE}(2^{2n}) \subseteq \mathsf{EXPSPACE}$, since every polynomial is $o(2^n)$. So every EXPSPACE-complete problem is outside PSPACE; see [EXPSPACE](/expspace/).
- **Nondeterministic space.** The same proof works for nondeterministic machines once $D$ can flip the answer of a nondeterministic run in the same space, and the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/) gives that. So $\mathsf{NSPACE}(f(n)) \subsetneq \mathsf{NSPACE}(g(n))$ under the same conditions. For example $\mathsf{NL} \subsetneq \mathsf{NSPACE}(\log^2 n)$.

## Tightness

- **A constant factor is not enough.** A machine can pack $r$ cells into one cell of a larger alphabet, so $\mathsf{DSPACE}(f) = \mathsf{DSPACE}(f / r)$ for every constant $r$. The condition $f = o(g)$ cannot be weakened to $f \le g / 2$.
- **No log factor.** Unlike the time hierarchy, the gap needs no extra factor: the space simulation in line L7 costs the constant factor $d_M$, and the step counter costs $O(g(n))$ bits.
- **Constructibility.** The condition on $g$ cannot be dropped. Borodin's gap theorem holds for space as well as time: there are computable functions $g$ with $\mathsf{DSPACE}(g(n)) = \mathsf{DSPACE}(2^{g(n)})$, and such $g$ are not space-constructible.
- **Very small space.** A machine that uses $o(\log \log n)$ space uses constant space and accepts a regular language (Stearns, Hartmanis and Lewis 1965), so there is no hierarchy at all below $\log \log n$. The proof above needs $g(n) \ge \log n$ to count the input positions in the step counter.

## History

Stearns, Hartmanis and Lewis proved the space hierarchy in 1965, at the same time as the time hierarchy of Hartmanis and Stearns, and for the same off-line model with a read-only input tape that is used here. The step counter that makes $D$ halt is the standard device of textbook proofs, such as those of Sipser and of Arora and Barak. The short proof of the nondeterministic form uses the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/) of 1987 and 1988.

## References
