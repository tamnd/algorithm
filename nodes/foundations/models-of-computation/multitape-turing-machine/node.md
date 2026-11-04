---
tag: WQP1MA
kind: model
slug: multitape-turing-machine
name: Multitape Turing machine
aliases:
- k-tape Turing machine
area: foundations/models-of-computation
level: core
summary: Turing machine with several independent tapes and heads, used to measure running time more naturally.
prereqs: [turing-machine]
see_also: [multitape-simulation-theorem, linear-speedup-theorem, nondeterministic-turing-machine, random-access-machine, palindrome, time-hierarchy-theorem]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 3.2, multitape Turing machines
  - title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 2, the sections on Turing machines with multiple strings and on linear speedup
  - paper: doi:10.1145/321356.321362
    title: Frederick C. Hennie and Richard E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM, volume 13, issue 4
    locator: pp. 533 to 546
  - title: Frederick C. Hennie, One-tape, off-line Turing machine computations, Information and Control, volume 8, issue 6, 1965
    locator: pp. 553 to 578
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society, volume 117
    locator: pp. 285 to 306
---

A multitape Turing machine is a [Turing machine](/turing-machine/) with $k$ tapes, each with its own head, and one finite control that reads the $k$ scanned symbols together. In one step it writes a symbol on each tape and moves each head by at most one cell. It decides the same languages as the one-tape machine, but many tasks are faster on it: a [palindrome](/palindrome/) test takes linear time on two tapes and quadratic time on one tape. Hartmanis and Stearns (1965) introduced it as the model for time complexity, and most texts define classes such as [P](/p/) with it.

## The machine

A $k$-tape machine $M$, for a fixed $k \ge 1$, has these parts:

- a finite set $Q$ of states, with a start state $q_0$ and two halting states, *accept* and *reject*;
- a finite tape alphabet $\Gamma$ that contains a blank symbol $\sqcup$, and an input alphabet $\Sigma \subseteq \Gamma \setminus \{\sqcup\}$;
- a transition function $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$.

Each tape has cells numbered $0, 1, 2, \ldots$ and is infinite to the right. At the start, the input $w \in \Sigma^*$ is in cells $0$ to $|w|-1$ of tape 1. All other cells hold the blank, and all $k$ heads are on cell $0$. A step works like this. The machine is in state $q$, and head $i$ reads the symbol $a_i$. If $\delta(q, a_1, \ldots, a_k) = (p, b_1, \ldots, b_k, D_1, \ldots, D_k)$, then for every $i$ at the same time the machine writes $b_i$ on tape $i$ and moves head $i$ by $D_i$, and it enters state $p$. The move $S$ keeps the head in place. A head on cell $0$ with the move $L$ also stays, as in the one-tape machine. The language $L(M)$, a computation, and the terms *decides* and *recognizes* are defined as for the one-tape machine.

Two common variants have the same power and the same time up to a constant factor, for time bounds $t(n) \ge n$. The first has a read-only input tape and a write-only output tape, with $k-2$ work tapes between them. The second has tapes that are infinite in both directions. The input tape variant is the one used to define sublinear space.

**Example: palindromes.** Let $\mathrm{PAL} = \{ w \in \{0,1\}^* : w = w^R \}$, where $w^R$ is $w$ written backwards. The two-tape machine below decides $\mathrm{PAL}$. It first copies $w$ to tape 2, after a marker $\$$ in cell 0 of tape 2. Then it moves head 2 back to the marker. Last, it reads tape 1 from right to left and tape 2 from left to right, and it compares the two symbols at each step. The head of tape 1 ends on cell $0$ when the comparison ends, and the machine uses the left-end rule to stay there. The table lists the rules. Here $a, x \in \{0, 1\}$, and a pair that the table does not list goes to reject.

| State | Reads | Writes | Moves | Next state |
|---|---|---|---|---|
| $s$ | $(\sqcup, \sqcup)$ | $(\sqcup, \sqcup)$ | $(S, S)$ | accept |
| $s$ | $(a, \sqcup)$ | $(a, \$)$ | $(S, R)$ | $c$ |
| $c$ | $(a, \sqcup)$ | $(a, a)$ | $(R, R)$ | $c$ |
| $c$ | $(\sqcup, \sqcup)$ | $(\sqcup, \sqcup)$ | $(S, L)$ | $b$ |
| $b$ | $(\sqcup, x)$ | $(\sqcup, x)$ | $(S, L)$ | $b$ |
| $b$ | $(\sqcup, \$)$ | $(\sqcup, \$)$ | $(L, R)$ | $d$ |
| $d$ | $(a, a)$ | $(a, a)$ | $(L, R)$ | $d$ |
| $d$ | $(a, \sqcup)$ | $(a, \sqcup)$ | $(S, S)$ | accept |

In state $d$, the pair $(a, x)$ with $a \ne x$ has no rule, so the machine rejects. After $j$ comparisons, head 2 is on cell $j + 1$ of tape 2, so it reads a blank exactly when $j = n$. At that time head 1 is on cell $0$, which holds a symbol of $\{0,1\}$. So the rule $(a, \sqcup)$ of state $d$ fires after all $n$ pairs matched. On a palindrome of length $n \ge 1$ the machine makes $3n + 4$ steps, for example $7$ steps on $0$, $10$ steps on $11$ and $16$ steps on $0110$. On the empty word it makes $1$ step. On a word of length $n$ it makes at most $3n + 4$ steps. So $\mathrm{PAL}$ is decided in time $O(n)$ with two tapes.

## What it counts

The time of $M$ on an input $w$ is the number of steps before it halts, and one step costs one unit, whatever $k$ is. The worst-case time $T(n)$ is the largest time over the inputs of length $n$.

The space of a run is the number of distinct cells that the heads visit on the work tapes. With a read-only input tape, the input cells do not count, so the space can be smaller than $n$. Without that tape, the input cells that a head visits count.

A time class such as $\mathrm{DTIME}(f(n))$ is the set of languages decided in time $O(f(n))$ by a $k$-tape machine for some $k$. Papadimitriou and most complexity texts define it with multitape machines, and Sipser uses one-tape machines. The two definitions agree on polynomial time but not on classes such as $\mathrm{DTIME}(n)$. The choice of $k$ matters for the exact class: $\mathrm{PAL} \in \mathrm{DTIME}(n)$ with two tapes, but not with one tape (see below). It does not matter for [polynomial time](/polynomial-time/), because of the simulation below.

## Relation to other models

The one-tape machine simulates the $k$-tape machine with a quadratic loss of time. The [multitape simulation theorem](/multitape-simulation-theorem/) has its own page. The proof below is complete; the theorem page gives more detail.

**Claim.** Let $M$ be a deterministic $k$-tape machine that decides $L$ and halts in at most $t(n) \ge n$ steps on every input of length $n$. Then a one-tape machine $S$ decides $L$ in $O(t(n)^2)$ steps, where the constant depends only on $k$.

**Construction.** The tape of $S$ has the cells $0, 1, 2, \ldots$, and cell $j$ holds one symbol of a finite alphabet $\Gamma'$. The symbol records, for each tape $i$ of $M$:

- the symbol $c_i \in \Gamma$ in cell $j$ of tape $i$, and
- a flag $f_i \in \{0, H, R'\}$. The flag $H$ means that head $i$ of $M$ is on cell $j$. The flag $R'$ is a temporary mark that is used inside one simulated step. The flag $0$ means neither.

It also records a bit $e$ that is $1$ exactly in cell $0$. The blank of $S$ is the symbol with $c_i = \sqcup$, $f_i = 0$ and $e = 0$ for all $i$. The state of $S$ holds the state of $M$ and a bounded amount of other data (at most the $k$ symbols read, a set of indices, and a phase name).

**Invariant $I_s$.** After $s$ simulated steps, $S$ is in cell $0$ in a state that holds the state of $M$, and the flags $H$ and the symbols $c_i$ in the tape of $S$ describe the configuration of $M$ after $s$ steps. No flag $R'$ is present.

**Steps.**

1. *Start (phase 0).* $S$ reads the input $w$ from left to right. In cell $0$ it always writes $e = 1$ and $f_i = H$ for all $i$, with $c_1 = w_1$ if $n \ge 1$ and $c_1 = \sqcup$ if $n = 0$. In cell $j$ with $1 \le j < n$ it writes $c_1 = w_{j+1}$, $f_i = 0$ and $e = 0$. In all cells $c_i = \sqcup$ for $i \ge 2$. If $n = 0$ it stays on cell $0$ and this phase ends after one step. Otherwise it stops at the first blank, which is in cell $n$, and moves left to cell $0$, which it finds by the bit $e$. This takes at most $2n + 2$ steps and makes $I_0$ true.
2. *Scan right (phase 1).* Assume $I_s$ with $M$ in a non-halting state $q$. $S$ moves right from cell $0$. On each cell it reads, for every $i$ with $f_i = H$, the symbol $c_i$ and stores it. It stops when it has seen $k$ flags. Let $P = \max_i p_i$, where $p_i$ is the cell of head $i$. The step that reads cell $P$ completes the list, so this phase takes at most $P + 1$ steps. Each head moves at most one cell in a step of $M$, and starts on cell $0$, so $P \le s$.
3. *Decide.* In the step that reads cell $P$, $S$ knows $q$ and the scanned symbols $a_1, \ldots, a_k$. Its finite control computes $\delta(q, a_1, \ldots, a_k) = (q', b_1, \ldots, b_k, D_1, \ldots, D_k)$. If $q'$ is accept or reject, $S$ halts in the same way, and the claim is true for this input by $I_s$.
4. *Scan left (phase 2).* The step that reads cell $P$ also starts this phase. $S$ moves left from cell $P$ to cell $0$, which it detects by $e = 1$, and it stays there by the rule for cell $0$. In each cell, and for each $i$ with $f_i = H$, it writes $b_i$ in place of $c_i$, and it changes the flag $f_i$ by the move $D_i$:
   - if $D_i = S$, the flag stays $H$;
   - if $D_i = R$, the flag becomes $R'$;
   - if $D_i = L$ and $e = 0$, the flag becomes $0$, and the state records that the next cell to the left (cell $j - 1$) gets the flag $H$ for tape $i$;
   - if $D_i = L$ and $e = 1$, the flag stays $H$, by the rule for cell $0$.

   When $S$ writes cell $j - 1$, it also sets the flags $H$ that the state recorded. The two kinds of flag in one cell do not clash, because each tape has one head. This phase takes at most $P + 1$ steps.
5. *Scan right for the marks (phase 3).* If no $D_i$ is $R$, skip to step 7. Else $S$ moves right from cell $0$. At a cell with a flag $R'$ it sets that flag to $0$, and it sets the flag $H$ for the same tape in the next cell to the right, which it writes in the next step. It stops after it has handled all indices $i$ with $D_i = R$. The marks are in cells at most $P$, so this takes at most $P + 2$ steps.
6. *Return.* $S$ moves left to cell $0$, found by $e = 1$, in at most $P + 2$ steps.
7. *End of the step.* The state of $S$ now holds $q'$, and $I_{s+1}$ is true: every symbol was written, every head moved as $D_i$ says, and no mark $R'$ is left.

**Time.** By step 2, simulated step number $s + 1$ uses at most $4(s + 2)$ steps of $S$. If $M$ halts after $t' \le t(n)$ steps, the total is at most

$$
(2n + 2) + \sum_{s=0}^{t'-1} 4(s+2) = (2n + 2) + 2t'(t'-1) + 8t' = 2t'^2 + 6t' + 2n + 2,
$$

which is $O(t(n)^2)$ because $t(n) \ge n$ and $t(n) \ge 1$ (the start state is not halting, so $M$ takes at least one step), so that $2n + 2 \le 4t(n)$. By $I_s$ at the end, $S$ accepts exactly when $M$ accepts. $\blacksquare$

## Known results in the model

- **Fewer tapes, a log factor.** A two-tape machine simulates a $k$-tape machine that runs in time $t(n)$ in $O(t(n) \log t(n))$ steps (Hennie and Stearns, 1966). So the number of tapes beyond two changes the time by at most a log factor.
- **One tape is slower on some tasks.** Every one-tape machine that decides $\mathrm{PAL}$ makes $\Omega(n^2)$ steps on some input of length $n$ (Hennie, 1965, by the crossing sequence method). The two-tape machine above takes $O(n)$. So the quadratic loss of the simulation cannot be removed for the one-tape model in general.
- **Linear speedup.** For every $\varepsilon > 0$ (Hartmanis and Stearns, 1965), a $k$-tape machine with $k \ge 2$ and time $t(n)$ has an equivalent one with time $\varepsilon t(n) + n + 2$. See the [linear speedup theorem](/linear-speedup-theorem/).
- **Hierarchy.** For time-constructible $f, g$ with $f(n) \log f(n) = o(g(n))$, $\mathrm{DTIME}(f) \subsetneq \mathrm{DTIME}(g)$ on multitape machines. See the [time hierarchy theorem](/time-hierarchy-theorem/).
- **Other models.** A [nondeterministic Turing machine](/nondeterministic-turing-machine/) changes the transition function, not the tapes. The [random-access machine](/random-access-machine/) and the multitape machine simulate each other with a polynomial loss, as [RAM and Turing machine equivalence](/ram-turing-equivalence/) shows.

## References
