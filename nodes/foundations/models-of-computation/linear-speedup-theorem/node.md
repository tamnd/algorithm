---
tag: E29K03
kind: theorem
slug: linear-speedup-theorem
name: Linear speedup theorem
aliases:
- linear speedup
area: foundations/models-of-computation
level: advanced
summary: A multitape machine running in time t(n) >= n can be replaced by one running in time eps*t(n) + n + 2, for any eps > 0, by compressing blocks of tape cells into single symbols.
prereqs: [multitape-turing-machine, turing-machine, asymptotic-notation]
see_also: [multitape-simulation-theorem, time-hierarchy-theorem, time-complexity, polynomial-time, p]
sources:
  - title: J. Hartmanis and R. E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117, 1965
    locator: pp. 285 to 306, the theorem on the speedup of a machine by a constant factor
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 2, the section on linear speedup
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 1, the discussion of the dependence of running time on the machine model
---

The linear speedup theorem says that a deterministic multitape [Turing machine](/turing-machine/) that runs in time $t(n)$ can be replaced by one that runs in time $\varepsilon\, t(n) + n + 2$, for every $\varepsilon > 0$. The new machine has a larger tape alphabet and more states. The theorem is the reason that [time complexity](/time-complexity/) classes on Turing machines use $O(\cdot)$ and ignore constant factors. Hartmanis and Stearns proved it in 1965.

## Statement

Machines are the deterministic $k$-tape machines of the [multitape Turing machine](/multitape-turing-machine/) page, with $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$, and the blank is $\sqcup$. A machine *halts within $T(n)$ steps* if on every input of length $n$ it reaches accept or reject in at most $T(n)$ steps.

**Theorem A (exact form).** Let $k \ge 2$. Let $M$ be a deterministic $k$-tape machine that decides $L$. Let $n_0 \ge 0$ and $m \ge 1$ be integers. Let $t : \mathbb{N} \to \mathbb{N}$ satisfy $t(n) \ge n$ for all $n$, and let $M$ halt within $t(n)$ steps on every input of length $n \ge n_0$. (Short inputs may take longer.) Then there is a deterministic $k$-tape machine $M'$ that decides $L$ and halts on every input of length $n$ within $T'(n)$ steps, where

$$
T'(n) \le n + 1 \ \ (n < n_0), \qquad T'(n) \le n + \left\lceil \frac{n}{m} \right\rceil + 6 \left\lceil \frac{t(n)}{m} \right\rceil - 1 \ \ (n \ge n_0).
$$

**Theorem B (the usual form).** Let $k \ge 2$, let $\varepsilon > 0$, let $t(n) \ge n$ for all $n$, and let $L$ be decided by a $k$-tape machine that halts within $t(n)$ steps for all $n \ge n_1$. Then some $k$-tape machine decides $L$ and halts within $\varepsilon\, t(n) + n + 2$ steps for every $n \ge 0$. In terms of classes, if $f(n) \ge n$ then

$$
\mathrm{DTIME}(f(n)) \subseteq \mathrm{DTIME}(\varepsilon f(n) + n + 2) .
$$

Theorem B follows from Theorem A with $m = \lceil 14/\varepsilon \rceil$ and $n_0 = \max(n_1, \lceil 8/\varepsilon \rceil)$. The machine $M'$ depends on $\varepsilon$, and its alphabet has size about $|\Gamma|^m$.

## In plain words

A Turing machine reads one symbol per step. Make a new machine whose symbols are blocks, where each block stands for a fixed number of old symbols. The new machine can look at a whole block in one step. In a few steps it reads the block under the head and its two neighbors, and it works out in its memory what the old machine does in the next block-length of steps. Then it writes the result back.

The old machine can move out of a block in that time, but it can reach only the neighbor blocks. So a constant number of new steps replaces a block-length of old steps. The larger the block, the greater the saving.

The new machine must first copy the input into blocks. This costs about one step per input symbol, and it explains the term for the input length in the bound.

## Proof

The full proof is in [the proof of the linear speedup](proofs/linear-speedup.md). The idea has four parts.

- *Copy.* Machine $M'$ reads the input and writes it in blocks of $m$ symbols on tape 2, and then it moves the head to the start of tape 2. Tapes $1$ and $2$ of $M$ are kept on tapes $2$ and $1$ of $M'$. This swap needs $k \ge 2$ and takes $n + \lceil n/m \rceil$ steps. Every other tape starts empty.
- *Round.* Each round has a read phase of 4 steps and a write phase of 2 steps. The read phase reads the block under each head and its two neighbors. The control then computes $m$ steps of $M$ on these blocks without using the tapes. The write phase writes the changed blocks back.
- *Why three blocks are enough.* In $m$ steps a head moves at most $m$ cells. It starts inside a block, so it stays in that block and one neighbor, and it cannot reach both neighbors.
- *Count.* The copy costs $n + \lceil n/m \rceil$, and each of at most $\lceil t/m \rceil$ rounds costs at most 6. An input shorter than $n_0$ is decided from a table in the finite control, in $n + 1$ steps.

## Consequences

- Constant factors in a running time $f(n)$ with $f(n)/n \to \infty$ have no meaning for multitape machines. Because of this theorem, it does no harm to define $\mathrm{DTIME}(f)$ with $O(f)$, as many textbooks do.
- If $f(n)/n \to \infty$, then $n + 2 \le \varepsilon f(n)$ for large $n$. So the new machine halts within $2\varepsilon f(n)$ steps for all large $n$, and the factor in front of $f$ is as small as one wants.
- For linear time, let $c \ge 1$ and $\varepsilon > 0$. A machine with time at most $\lceil c n \rceil$ is replaced by one with time $(1 + \varepsilon) n + 2$ (apply Theorem B with $t(n) = \lceil c n \rceil$ and $\varepsilon / (c + 1)$, which gives $\varepsilon\lceil cn \rceil/(c+1) \le \varepsilon n$ for $n \ge 1$). Time $(1 + \varepsilon) n + 2$ for each $\varepsilon > 0$ is the limit of the method.
- The theorem does not touch exponents. Hierarchy results need a factor that grows. See the [time hierarchy theorem](/time-hierarchy-theorem/), whose gap is a logarithmic factor.

## Tightness

- *The term $n$ cannot be removed.* Let $L_1$ be the set of words over $\{0, 1\}$ that end in $1$. A machine must read the last symbol of an input of length $n$. Its head starts on cell $0$ and moves one cell in a step, so it needs at least $n - 1$ steps. The factor $\varepsilon$ cannot apply to the input length.
- *The proof needs a second tape.* Step 1 of the proof uses tape 1 to read the input and tape 2 to build the blocks. This page does not claim the theorem for one-tape machines. On a one-tape machine, compressing the input costs $\Theta(n^2)$ steps, so the same method gives a speedup by any constant factor only when $t(n)/n^2 \to \infty$. Blum's speedup theorem is a different result with a similar name.
- *The exponent does not change.* The theorem gives a smaller constant factor and nothing else. A speedup of a growing factor needs a different argument, and the [time hierarchy theorem](/time-hierarchy-theorem/) shows that some such gains are impossible.

## History

Hartmanis and Stearns introduced time-bounded classes of Turing machines in "On the computational complexity of algorithms" (1965), and they proved the speedup there for multitape machines. Their version assumes that $T(n)/n \to \infty$ and concludes that $T$ and $cT$ define the same class. The form $\varepsilon t(n) + n + 2$ is the textbook form, as in Papadimitriou (1994). The exact constants on this page (the 6-step round, the table for short inputs and $m = \lceil 14/\varepsilon \rceil$) come from the proof on this page, not from the paper.

## References
