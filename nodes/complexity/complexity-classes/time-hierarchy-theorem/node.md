---
tag: DYTE78
kind: theorem
slug: time-hierarchy-theorem
name: Time hierarchy theorem
aliases:
- deterministic time hierarchy
area: complexity/complexity-classes
level: core
summary: "More time decides more problems: if g is time-constructible and f log f = o(g), then DTIME(f) is a proper subset of DTIME(g). It gives P different from EXP."
prereqs: [time-complexity, multitape-turing-machine, multitape-simulation-theorem]
see_also: [space-hierarchy-theorem, diagonalization-argument, universal-turing-machine, linear-speedup-theorem, p, exptime, nexptime, complexity-class]
sources:
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117, 285 to 306 (1965)
    locator: the time hierarchy, with a larger gap than f log f
  - paper: doi:10.1145/321356.321362
    title: F. C. Hennie and R. E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM 13(4), 533 to 546 (1966)
    locator: the simulation in time O(t log t), which gives the condition f log f = o(g)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 1 (the efficient universal machine) and Section 3.1, Time Hierarchy Theorem; Section 3.2 for the nondeterministic version
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 9.1, Hierarchy Theorems
  - paper: doi:10.1145/800070.802172
    title: Martin Fürer, The tight deterministic time hierarchy, Proceedings of the 14th Annual ACM Symposium on Theory of Computing, 8 to 16 (1982)
    locator: the hierarchy with f = o(g) for machines with a fixed number of at least two tapes
  - paper: doi:10.1016/0304-3975(83)90015-4
    title: Stanislav Žák, A Turing machine time hierarchy, Theoretical Computer Science 26(3), 327 to 333 (1983)
    locator: the nondeterministic time hierarchy with f(n+1) = o(g(n))
---

The time hierarchy theorem says that a deterministic multitape Turing machine can decide more languages when it is given sufficiently more time. If $g$ is time-constructible and $f(n) \log f(n) = o(g(n))$, then some language is decided in time $O(g(n))$ but not in time $O(f(n))$. The proof is a diagonalization: a machine $D$ runs every machine $M$ on inputs that encode $M$, for $g(n)$ steps, and answers the opposite. The factor $\log f$ is the cost of the simulation by one universal machine with a fixed number of tapes. The theorem gives $\mathsf{DTIME}(n^a) \subsetneq \mathsf{DTIME}(n^b)$ for $1 \le a < b$ and $\mathsf{P} \subsetneq \mathsf{EXP}$, which are among the few separations of classes that are known. The [space hierarchy theorem](/space-hierarchy-theorem/) is the analogue for space, without the log factor.

## Statement

The model is the deterministic [multitape Turing machine](/multitape-turing-machine/). $\mathsf{DTIME}(t(n))$ is the class of languages decided by such a machine, with any number of tapes, in $O(t(n))$ steps on every input of length $n$. A function $g$ with $g(n) \ge n$ is *time-constructible* if a deterministic machine, on input $1^n$, writes $g(n)$ in binary in $O(g(n))$ steps. The functions $n \lceil \log_2 n \rceil$, $n^k$ and $2^n$ are time-constructible.

**Theorem (Hartmanis and Stearns 1965; Hennie and Stearns 1966).** Let $f, g : \mathbb{N} \to \mathbb{N}$ with $f(n) \ge 1$, let $g$ be time-constructible, and let

$$f(n) \log f(n) = o(g(n)).$$

Then $\mathsf{DTIME}(f(n)) \subsetneq \mathsf{DTIME}(g(n))$.

The inclusion $\mathsf{DTIME}(f) \subseteq \mathsf{DTIME}(g)$ holds because $f = o(g)$; the content is that it is proper.

## In plain words

Give a computer more time and it can solve problems that it could not solve before, as long as the extra time is large enough.

The proof builds a contrary machine. Given an input, it reads the input as the description of some other machine. It runs that machine on this same input, with a time limit, and then gives the opposite answer. Any fast machine you name will meet an input where the contrary machine has time to finish the run, and there the two machines disagree. So no fast machine solves the problem of the contrary machine, but the contrary machine itself solves it within its time limit.

The extra time must cover the cost of running one machine inside another. That cost is a small factor, and it is why the gap must be a bit more than the fast time.

## Proof

**The universal machine.** Fix an encoding $\langle M \rangle$ of multitape machines as binary strings. There is a universal machine $U$ with a fixed number of tapes with this property: for every machine $M$ there is a constant $C_M$ such that, if $M$ halts on $x$ within $t$ steps, then $U$ on input $(\langle M \rangle, x)$ halts with the same answer within $C_M\, t \log t$ steps, for $t \ge 2$. $C_M$ depends on the number of tapes, states and symbols of $M$, but not on $x$. This is the two-tape simulation of Hennie and Stearns (1966), done by a universal machine; Arora and Barak (Chapter 1) give the proof. See [universal Turing machine](/universal-turing-machine/) and the [multitape simulation theorem](/multitape-simulation-theorem/).

**The diagonal machine.** On an input $x$ of length $n$, the machine $D$ works as follows.

```pseudo id=diag
D(x)
L1  n ← |x|; write g(n) in binary on the clock tape
L2  if x is not 1^k 0 w with w = ⟨M⟩ for a machine M then reject
L3  run U on (⟨M⟩, x), and decrement the clock after each step of U
L4  if the clock runs out before U halts then accept
L5  if U says that M accepts x then reject else accept
```

The prefix $1^k 0$ gives each machine $M$ the inputs $1^k 0 \langle M \rangle$ for all $k \ge 0$, so each $M$ has arbitrarily long inputs that encode it.

**D runs in time $O(g(n))$.** Line L1 takes $O(g(n))$ steps because $g$ is time-constructible. Line L2 takes $O(n)$ steps. The clock is a binary counter on its own tape, with the head at the low-order end. A sequence of $g(n)$ decrements of a binary counter moves the head $O(g(n))$ times in total, because the bit at position $j$ changes only once in every $2^j$ decrements. The clock runs out when a borrow runs past the highest bit. So lines L3 and L4 run at most $g(n)$ steps of $U$ with $O(g(n))$ steps of overhead. Since $g(n) \ge n$, the total is $O(g(n))$, and $D$ halts on every input. So $L(D) \in \mathsf{DTIME}(g(n))$.

**$L(D)$ is not in $\mathsf{DTIME}(f(n))$.** Suppose a machine $M$ decides $L(D)$ in time $O(f(n))$. Then $M$ halts on every input of length $n$ within $T(n) = c f(n) + c$ steps, for a constant $c \ge 2$. By the property of $U$, the simulation in line L3 halts within $C_M T(n) \log T(n)$ steps of $U$.

This number is $o(g(n))$. If $f$ is bounded, then $T$ is bounded, while $g(n) \ge n$ grows. If $f$ is not bounded, then for the $n$ with $f(n) \ge 2c$, $T(n) \le 2c f(n) \le f(n)^2$ and so $T(n) \log T(n) \le 4c\, f(n) \log f(n)$; on the other $n$, $T(n)$ is bounded by a constant. In both cases $C_M T(n) \log T(n) = o(g(n))$ because $f \log f = o(g)$ and $g(n) \to \infty$.

So there is an $n_0$ with $C_M T(n) \log T(n) < g(n)$ for all $n \ge n_0$. Choose $k$ such that $x = 1^k 0 \langle M \rangle$ has length $n \ge n_0$. On this $x$, $U$ halts before the clock runs out, so $D$ reaches line L5 and answers the opposite of $M$ on $x$. Then $x \in L(D)$ if and only if $x \notin L(M)$, which contradicts $L(M) = L(D)$. $\blacksquare$

## Consequences

The ratio $f \log f / g$ decides whether the theorem applies to a pair of bounds. The table gives it at three input lengths, with $\log = \log_2$.

| $f(n)$ | $g(n)$ | $n = 2^{10}$ | $n = 2^{20}$ | $n = 2^{40}$ | applies |
|---|---|---|---|---|---|
| $n$ | $n^2$ | 0.0098 | $1.9 \times 10^{-5}$ | $3.6 \times 10^{-11}$ | yes |
| $n^2$ | $n^2 \log^2 n$ | 0.2 | 0.1 | 0.05 | yes |
| $n^2$ | $n^2 \log n$ | 2 | 2 | 2 | no |

For $f = n$ and $g = n^2$ the ratio is $\log n / n$; for $g = n^2 \log^2 n$ it is $2 / \log n$, which tends to 0 slowly; for $g = n^2 \log n$ it is the constant 2, so the theorem says nothing about $\mathsf{DTIME}(n^2)$ against $\mathsf{DTIME}(n^2 \log n)$.

- **Polynomial time has no fixed exponent.** For $1 \le a < b$, $\mathsf{DTIME}(n^a) \subsetneq \mathsf{DTIME}(n^b)$, since $n^a \log n^a = o(n^b)$. So no single $k$ gives $\mathsf{P} = \mathsf{DTIME}(n^k)$. See [P](/p/).
- **P is different from EXP.** $\mathsf{P} \subseteq \mathsf{DTIME}(2^n) \subsetneq \mathsf{DTIME}(2^{2n}) \subseteq \mathsf{EXP}$, since $2^n \cdot n = o(2^{2n})$; the ratio is $n / 2^n$. So some problem in [EXP](/exptime/) is not in P, and every EXP-complete problem is outside P. In the same way $\mathsf{EXP} \subsetneq \mathsf{2EXP}$.
- **Nondeterministic time.** The same diagonalization does not work directly for nondeterministic machines, because $D$ cannot flip the answer of a nondeterministic run in the same time. Cook (1973) proved $\mathsf{NTIME}(n^a) \subsetneq \mathsf{NTIME}(n^b)$ for $1 \le a < b$, and Seiferas, Fischer and Meyer (1978) and Žák (1983) proved $\mathsf{NTIME}(f(n)) \subsetneq \mathsf{NTIME}(g(n))$ for time-constructible $g$ with $f(n+1) = o(g(n))$, by a lazy diagonalization. This gives $\mathsf{NP} \subsetneq \mathsf{NEXP}$; see [NEXPTIME](/nexptime/).
- **Relativization.** The proof treats $M$ as a black box that $U$ runs, so it works the same with any oracle. Such a proof cannot settle P versus NP, by the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/).

## Tightness

- **A constant factor is never enough.** $\mathsf{DTIME}(t)$ is defined with $O(t)$, so $\mathsf{DTIME}(t) = \mathsf{DTIME}(2t)$ by definition. The [linear speedup theorem](/linear-speedup-theorem/) shows that this is not only a convention: a machine with time $t(n) \ge n$ can be sped up to time $\varepsilon t(n) + n + 2$ for any $\varepsilon > 0$.
- **The log factor.** The factor comes from the universal machine, which has a fixed number of tapes and must simulate machines with more tapes. For machines with a fixed number $k \ge 2$ of tapes, Fürer (1982) proved the hierarchy with $f = o(g)$ only. For the class $\mathsf{DTIME}$ over all multitape machines, whether the factor $\log f$ can be removed is open. So it is not known, for example, whether $\mathsf{DTIME}(n^2) \ne \mathsf{DTIME}(n^2 \log n)$ on multitape machines.
- **Constructibility.** The condition on $g$ cannot be dropped. Borodin's gap theorem gives computable functions $g$ with $\mathsf{DTIME}(g(n)) = \mathsf{DTIME}(2^{g(n)})$; such $g$ are not time-constructible.
- **Other models.** On the random-access machine the universal simulation costs only a constant factor, and Cook and Reckhow (1973) proved a hierarchy with a constant factor between the bounds for their random-access machine.

## History

Hartmanis and Stearns defined time complexity classes in 1965 and proved the first time hierarchy, with a larger gap between $f$ and $g$. Hennie and Stearns gave the simulation of $k$ tapes by two tapes in time $O(t \log t)$ in 1966, which gives the form with $f \log f = o(g)$. Fürer gave the tight form for a fixed number of tapes in 1982. Cook proved the first nondeterministic hierarchy in 1972 (journal version 1973), and Seiferas, Fischer and Meyer, and then Žák, gave the form with $f(n+1) = o(g(n))$. Hartmanis and Stearns received the Turing Award in 1993 for the foundations of complexity theory.

## References
