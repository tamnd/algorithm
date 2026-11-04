---
tag: JE7NXX
kind: theorem
slug: multitape-simulation-theorem
name: Multitape simulation theorem
aliases:
- one-tape simulation of multitape Turing machines
area: foundations/models-of-computation
level: advanced
summary: Any k-tape Turing machine running in time t can be simulated by a single-tape machine in time O(t^2).
prereqs: [multitape-turing-machine, turing-machine, asymptotic-notation]
see_also: [linear-speedup-theorem, polynomial-time, p, ram-turing-equivalence, time-hierarchy-theorem, time-complexity]
sources:
  - title: J. Hartmanis and R. E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117, 1965
    locator: pp. 285 to 306, the simulation of a multitape machine by a one-tape machine in quadratic time
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage, 2013
    locator: Section 7.1, Theorem 7.8
  - paper: doi:10.1145/321356.321362
    title: F. C. Hennie and R. E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM 13(4), 1966
    locator: pp. 533 to 546
  - paper: doi:10.1016/S0019-9958(65)90399-2
    title: F. C. Hennie, One-tape, off-line Turing machine computations, Information and Control 8(6), 1965
    locator: pp. 553 to 578, the quadratic lower bound for the recognition of palindromes
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 2.3, Theorem 2.1
---

The multitape simulation theorem says that a deterministic one-tape [Turing machine](/turing-machine/) can simulate a deterministic $k$-tape machine that runs in time $t(n)$, with a loss of time that is at most quadratic. A two-tape machine can do it with a loss of a logarithmic factor (Hennie and Stearns, 1966). The quadratic loss cannot be removed for one tape in general, because one-tape machines need $\Omega(n^2)$ steps to recognize palindromes.

## Statement

Machines are those of the [multitape Turing machine](/multitape-turing-machine/) page, with $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$. The blank is $\sqcup$.

**Theorem.** Let $k \ge 1$. Let $M$ be a deterministic $k$-tape machine that decides $L \subseteq \Sigma^*$ and halts within $t(n)$ steps on every input of length $n$, where $t(n) \ge \max(n, 1)$. Then there is a deterministic one-tape machine $S$ that decides $L$ and halts within $t(n)^2 + (2k+4)\,t(n)$ steps on every input of length $n$. So $S$ runs in time $O(t(n)^2)$, where the constant depends on $k$ only: it is at most $2k + 5$.

**Two cited results.**

- *Two tapes (Hennie and Stearns, 1966).* A deterministic $k$-tape machine with time $t(n)$ is simulated by a deterministic two-tape machine in time $O(t(n) \log t(n))$. This page does not prove it.
- *One tape is slower on some tasks (Hennie, 1965).* Let $\mathrm{PAL} = \{w \in \{0,1\}^* : w = w^R\}$. Every one-tape machine that decides $\mathrm{PAL}$ makes $\Omega(n^2)$ steps on some input of length $n$. This page does not prove it.

## In plain words

A machine with several tapes has several heads. A machine with one tape has one head. To copy the first machine on the second, put the tapes side by side as the rows of one tape. Each cell of the new tape then holds one column: a symbol from each old tape. Mark the places where the old heads stand.

To copy one old step, the new head sweeps from the left end to the farthest mark and reads the symbols under the marks. Then it sweeps back and makes the changes. Each old step moves a head by at most one cell, so a sweep is no longer than the number of old steps done so far.

Adding the cost of all steps gives a sum like one plus two plus three, up to the running time. This sum grows like the square of the running time.

## Proof

The full proof is in [the proof of the quadratic simulation](proofs/quadratic-simulation.md). The machine $S$ keeps the $k$ tapes as $k$ tracks on one tape, with a flag in each track that marks the head. The proof has four parts.

- *Start.* $S$ rewrites the input as columns and returns to cell $0$ in at most $2n + 2$ steps.
- *One step of $M$.* $S$ sweeps right to the farthest head, reads the symbols under the flags, and chooses the transition from $\delta$. Then it sweeps left, writes the new symbols, and moves the flags. A flag that moves right needs a short detour of 2 steps. The sweeps cost $2P + 1$, where $P$ is the farthest head cell, and the detours cost at most $2k$.
- *Bound on $P$.* Each head moves at most one cell in each step, so after $s$ steps $P \le s$. Step number $s + 1$ costs at most $2s + 1 + 2k$.
- *Sum.* Over $t' \le t(n)$ steps the cost is at most $t'^2 + 2k\,t' + 2n + 2$, which is at most $t(n)^2 + (2k+4)\,t(n)$ because $n \le t(n)$ and $1 \le t(n)$.

## Consequences

- The class [P](/p/) is the same for one-tape and multitape machines, because a polynomial of a polynomial is a polynomial. This is one step in the argument that [polynomial time](/polynomial-time/) does not depend on the machine model, with [RAM and Turing machine equivalence](/ram-turing-equivalence/).
- Exact time classes do depend on the number of tapes. The language $\mathrm{PAL}$ is decided in $O(n)$ steps by a two-tape machine: it copies the input to tape 2 (about $n$ steps, both heads end at the right end), moves head 1 back to the start (about $n$ steps), and compares the tapes with head 1 moving right and head 2 moving left (about $n$ steps). A one-tape machine needs $\Omega(n^2)$ steps for it.
- A claim of the form "time $t$ on a multitape machine" gives a claim "time $O(t^2)$ on one tape" for free. The factor $\log t$ is enough if two tapes are allowed.

## Tightness

- *At linear time the quadratic bound is tight.* Take $M$ to be the two-tape machine for $\mathrm{PAL}$ with $t(n) = O(n)$. By the result of Hennie (1965) every one-tape machine needs $\Omega(n^2) = \Omega(t(n)^2)$ steps. So the exponent 2 cannot be lowered in the theorem when $t(n) = \Theta(n)$.
- *More than one tape.* The upper bound $O(t \log t)$ of Hennie and Stearns is for two tapes, and it shows that more than two tapes never give more than a logarithmic factor.
- *The constant is not tight.* The factor $2k+5$ comes from the simple sweep construction on this page. The proof does not try to minimize it.

## History

Hartmanis and Stearns gave the quadratic simulation of $k$ tapes by one tape in 1965 (Transactions of the American Mathematical Society 117), in the paper that founded time complexity. Hennie proved the quadratic lower bound for palindromes on one tape in 1965 (Information and Control 8). Hennie and Stearns showed in 1966 (Journal of the ACM 13) that two tapes are enough to simulate any number of tapes with a logarithmic loss. The exact constants on this page are from the proof on this page.

## References
