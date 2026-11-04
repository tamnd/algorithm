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
see_also: [multitape-simulation-theorem, linear-speedup-theorem, nondeterministic-turing-machine, random-access-machine, ram-turing-equivalence, palindrome, time-hierarchy-theorem, boolean-circuit]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 3.2 (multitape Turing machines) and Section 7.1 (Theorem 7.8, the quadratic simulation)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 2.3 (Turing machines with multiple strings) and Section 2.4 (linear speedup)
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society, volume 117, 1965
    locator: pp. 285 to 306
  - paper: doi:10.1145/321356.321362
    title: Frederick C. Hennie and Richard E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM, volume 13, issue 4, 1966
    locator: pp. 533 to 546
  - paper: doi:10.1016/S0019-9958(65)90399-2
    title: Frederick C. Hennie, One-tape, off-line Turing machine computations, Information and Control, volume 8, issue 6, 1965
    locator: pp. 553 to 578
  - paper: doi:10.1145/322123.322138
    title: Nicholas Pippenger and Michael J. Fischer, Relations among complexity measures, Journal of the ACM, volume 26, issue 2, 1979
    locator: pp. 361 to 381 (the oblivious two-tape simulation and the circuits of size O(t log t))
  - paper: doi:10.1145/322003.322015
    title: John Hopcroft, Wolfgang Paul and Leslie Valiant, On time versus space, Journal of the ACM, volume 24, issue 2, 1977
    locator: pp. 332 to 337
  - paper: "Ryan Williams, Simulating time with square-root space, Proceedings of the 57th Annual ACM Symposium on Theory of Computing (STOC 2025)"
    locator: abstract (the simulation of time t in space O(sqrt(t log t)))
  - paper: doi:10.1145/800070.802172
    title: Martin Fürer, The tight deterministic time hierarchy, Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC 1982)
    locator: pp. 8 to 16
  - paper: doi:10.1109/SFCS.1983.39
    title: Wolfgang J. Paul, Nicholas Pippenger, Endre Szemerédi and William T. Trotter, On determinism versus non-determinism and related problems, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983)
    locator: pp. 429 to 438
---

A multitape Turing machine is a [Turing machine](/turing-machine/) with $k$ tapes, each with its own head, and one finite control that reads the $k$ scanned symbols together. In one step it writes a symbol on each tape and moves each head by at most one cell. It decides the same languages as the one-tape machine, but many tasks are faster on it: a [palindrome](/palindrome/) test takes linear time on two tapes and quadratic time on one tape. Hartmanis and Stearns (1965) used it as the model for their study of time complexity, and many complexity texts define the time classes, and so the class [P](/p/), with it.

## The machine

A $k$-tape machine $M$, for a fixed $k \ge 1$, has these parts:

- a finite set $Q$ of states, with a start state $q_0$ and two halting states, *accept* and *reject*;
- a finite tape alphabet $\Gamma$ that contains a blank symbol $\sqcup$, and an input alphabet $\Sigma \subseteq \Gamma \setminus \{\sqcup\}$;
- a transition function $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$.

Each tape has cells numbered $0, 1, 2, \ldots$ and is infinite to the right. At the start, the input $w \in \Sigma^*$ is in cells $0$ to $|w|-1$ of tape 1. All other cells hold the blank, and all $k$ heads are on cell $0$. A step works like this. The machine is in state $q$, and head $i$ reads the symbol $a_i$. If $\delta(q, a_1, \ldots, a_k) = (p, b_1, \ldots, b_k, D_1, \ldots, D_k)$, then for every $i$ at the same time the machine writes $b_i$ on tape $i$ and moves head $i$ by $D_i$, and it enters state $p$. The move $S$ keeps the head in place. A head on cell $0$ with the move $L$ also stays, as in the one-tape machine. The language $L(M)$, a computation, and the terms *decides* and *recognizes* are defined as for the one-tape machine. With $k = 1$ and no move $S$ this is the machine of the [Turing machine](/turing-machine/) page.

Two common variants have the same power and the same time up to a constant factor, for time bounds $t(n) \ge n$. The first has a read-only input tape and a write-only output tape, with $k-2$ work tapes between them. The second has tapes that are infinite in both directions. The input tape variant is the one used to define sublinear space.

**Example: palindromes.** Let $\mathrm{PAL} = \{ w \in \{0,1\}^* : w = w^R \}$, where $w^R$ is $w$ written backwards. The two-tape machine below decides $\mathrm{PAL}$. It first copies $w$ to tape 2, after a marker $\$$ in cell 0 of tape 2. Then it moves head 2 back to the marker. Last, it reads tape 1 from right to left and tape 2 from left to right, and it compares the two symbols at each step. The head of tape 1 ends on cell $0$ when the comparison ends, and the machine uses the left-end rule to stay there. The table lists the rules. Here $a, x \in \{0, 1\}$, and a pair that the table does not list goes to reject in one step.

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

Let $w = w_1 \cdots w_n$ with $n \ge 1$. State $s$ takes 1 step, state $c$ copies $w$ in $n$ steps and sees the end in 1 more, and state $b$ walks back over the $n$ copied symbols in $n$ steps and reaches the marker in 1 more. Then head 1 is on cell $n-1$ and head 2 on cell $1$. Comparison number $j$, for $j = 1, \ldots, n$, reads $w_{n-j+1}$ on tape 1 (the cell $\max(n-j, 0)$, by the left-end rule) and $w_j$ on tape 2. So the machine reaches comparison $j + 1$ exactly when $w_{n-i+1} = w_i$ for all $i \le j$. After $n$ comparisons, head 2 is on cell $n + 1$, which is blank, and head 1 is on cell $0$, which holds $w_1$. So the rule $(a, \sqcup)$ of state $d$ accepts exactly when all $n$ pairs matched, that is, when $w = w^R$. On a palindrome of length $n \ge 1$ the machine makes $3n + 4$ steps: $7$ steps on $0$, $10$ steps on $11$ and $16$ steps on $0110$. On the empty word it makes $1$ step. On a word that is not a palindrome it rejects at the first mismatch, within $3n + 4$ steps: $8$ steps on $01$ and $13$ steps on $0100$. So $\mathrm{PAL}$ is decided in time $3n + 4$ with two tapes.

## What it counts

The time of $M$ on an input $w$ is the number of steps before it halts, and one step costs one unit, whatever $k$ is. A step that moves all $k$ heads still costs 1. The worst-case time $t(n)$ is the largest time over the inputs of length $n$.

The space of a run is the number of distinct cells that the heads visit on the work tapes. With a read-only input tape, the input cells do not count, so the space can be smaller than $n$. Without that tape, the input cells that a head visits count.

A time class such as $\mathrm{DTIME}(f(n))$ is the set of languages decided in time $O(f(n))$ by a $k$-tape machine for some $k$. Papadimitriou and many other complexity texts define it with multitape machines, and Sipser defines the class $\mathrm{TIME}(t(n))$ with one-tape machines. The two definitions agree on polynomial time but not on classes such as $\mathrm{DTIME}(n)$: $\mathrm{PAL}$ is decided in linear time with two tapes, but not with one tape (see below). For [polynomial time](/polynomial-time/) the choice does not matter, because of the simulation below. For space it matters even less: the simulation below keeps the space within a constant factor, so a $k$-tape machine with space $s(n) \ge n$ has a one-tape equivalent with space $O(s(n))$.

## Relation to other models

The one-tape machine simulates the $k$-tape machine with a quadratic loss of time. The [multitape simulation theorem](/multitape-simulation-theorem/) has its own page. The proof below is complete.

**Claim.** Let $M$ be a deterministic $k$-tape machine that decides $L$ and halts in at most $t(n) \ge n$ steps on every input of length $n$. Then a one-tape machine $S$ decides $L$ in at most $2t(n)^2 + 6t(n) + 2n + 2 = O(t(n)^2)$ steps, and the constant in the $O$ does not depend on $M$.

**Construction.** The tape of $S$ has the cells $0, 1, 2, \ldots$, and cell $j$ holds one symbol of a finite alphabet $\Gamma'$. The symbol records, for each tape $i$ of $M$:

- the symbol $c_i \in \Gamma$ in cell $j$ of tape $i$, and
- a flag $f_i \in \{0, H, R'\}$. The flag $H$ means that head $i$ of $M$ is on cell $j$. The flag $R'$ is a temporary mark that is used inside one simulated step. The flag $0$ means neither.

It also records a bit $e$ that is $1$ exactly in cell $0$. The blank of $S$ is the symbol with $c_i = \sqcup$, $f_i = 0$ and $e = 0$ for all $i$. The alphabet $\Gamma'$ also contains $\Sigma$, so that the input can be read. The state of $S$ holds the state of $M$ and a bounded amount of other data (at most the $k$ symbols read, a set of indices, and a phase name).

**Invariant $I_s$.** After $s$ simulated steps, $S$ is in cell $0$ in a state that holds the state of $M$, and the flags $H$ and the symbols $c_i$ in the tape of $S$ describe the configuration of $M$ after $s$ steps. No flag $R'$ is present.

**Steps.**

1. *Start (phase 0).* $S$ reads the input $w$ from left to right. In cell $0$ it always writes $e = 1$ and $f_i = H$ for all $i$, with $c_1 = w_1$ if $n \ge 1$ and $c_1 = \sqcup$ if $n = 0$. In cell $j$ with $1 \le j < n$ it writes $c_1 = w_{j+1}$, $f_i = 0$ and $e = 0$. In all cells $c_i = \sqcup$ for $i \ge 2$. If $n = 0$ it stays on cell $0$ and this phase ends after one step. Otherwise it stops at the first blank, which is in cell $n$, and moves left to cell $0$, which it finds by the bit $e$. This takes at most $2n + 2$ steps and makes $I_0$ true.
2. *Scan right (phase 1).* Assume $I_s$ with $M$ in a non-halting state $q$. $S$ moves right from cell $0$. On each cell it reads, for every $i$ with $f_i = H$, the symbol $c_i$ and stores it. It stops when it has seen $k$ flags. Let $P = \max_i p_i$, where $p_i$ is the cell of head $i$. The step that reads cell $P$ completes the list, so this phase takes at most $P + 1$ steps. Each head moves at most one cell in a step of $M$, and starts on cell $0$, so $P \le s$.
3. *Decide.* In the step that reads cell $P$, $S$ knows $q$ and the scanned symbols $a_1, \ldots, a_k$. Its finite control computes $\delta(q, a_1, \ldots, a_k) = (q', b_1, \ldots, b_k, D_1, \ldots, D_k)$. If $q'$ is accept or reject, $S$ halts in the same way, and the claim is true for this input by $I_s$.
4. *Scan left (phase 2).* The step that reads cell $P$ also starts this phase. $S$ moves left from cell $P$ to cell $0$, which it detects by $e = 1$, and it stays there by the rule for cell $0$. In each cell, and for each $i$ for which the cell held the flag $H$ when $S$ arrived, it writes $b_i$ in place of $c_i$, and it changes the flag $f_i$ by the move $D_i$:
   - if $D_i = S$, the flag stays $H$;
   - if $D_i = R$, the flag becomes $R'$;
   - if $D_i = L$ and $e = 0$, the flag becomes $0$, and the state records that the next cell to the left (cell $j - 1$) gets the flag $H$ for tape $i$;
   - if $D_i = L$ and $e = 1$, the flag stays $H$, by the rule for cell $0$.

   When $S$ writes cell $j - 1$, it also sets the flags $H$ that the state recorded. A flag that is set in this way is not handled again, because $S$ only moves left in this phase and handles only the flags that it reads. Two flags of different tapes in one cell do not clash, because each tape has its own field. This phase takes at most $P + 1$ steps.
5. *Scan right for the marks (phase 3).* If no $D_i$ is $R$, skip to step 7. Else $S$ moves right from cell $0$. At a cell with a flag $R'$ it sets that flag to $0$, and it sets the flag $H$ for the same tape in the next cell to the right, which it writes in the next step. It stops after it has handled all indices $i$ with $D_i = R$. The marks are in cells at most $P$, so this takes at most $P + 2$ steps.
6. *Return.* $S$ moves left to cell $0$, found by $e = 1$, in at most $P + 2$ steps.
7. *End of the step.* The state of $S$ now holds $q'$, and $I_{s+1}$ is true: every symbol was written, every head moved as $D_i$ says, and no mark $R'$ is left.

**Time.** Simulated step number $s + 1$ uses at most $4P + 6 \le 4s + 6 < 4(s + 2)$ steps of $S$. If $M$ halts after $t' \le t(n)$ steps, the total is at most

$$
(2n + 2) + \sum_{s=0}^{t'-1} 4(s+2) = (2n + 2) + 2t'(t'-1) + 8t' = 2t'^2 + 6t' + 2n + 2,
$$

which is $O(t(n)^2)$ because $t(n) \ge n$ and $t(n) \ge 1$ (the start state is not halting, so $M$ takes at least one step), so that $2n + 2 \le 4t(n)$. By $I_s$ at the end, $S$ accepts exactly when $M$ accepts. $\blacksquare$

For the palindrome machine above on $0110$, $t' = 16$ and $n = 4$, so the one-tape machine makes at most $2 \cdot 16^2 + 6 \cdot 16 + 2 \cdot 4 + 2 = 618$ steps. The space of $S$ is the largest cell index that a head of $M$ reaches, plus a constant, so the space is kept within a constant factor.

The other links are these.

- **Random-access machine.** A [random-access machine](/random-access-machine/) with the [logarithmic cost](/logarithmic-cost-model/) rule and a multitape machine simulate each other with a polynomial loss of time: $O(t^2)$ steps in one direction and $O(t \log t)$ cost in the other. The proofs are on the page [RAM and Turing machine equivalence](/ram-turing-equivalence/).
- **Nondeterminism.** A [nondeterministic Turing machine](/nondeterministic-turing-machine/) has the same tapes and a transition relation in place of the function. For nondeterministic machines, two tapes are enough with only a constant-factor loss of time (Book, Greibach and Wegbreit, 1970; see that page).
- **Circuits.** Pippenger and Fischer (1979) made the two-tape simulation of Hennie and Stearns *oblivious*: the head moves depend only on the input length, not on the input. From such a machine one builds a family of [Boolean circuits](/boolean-circuit/) of size $O(t(n) \log t(n))$ that decides the same language.

## Known results in the model

- **Fewer tapes, a log factor.** A two-tape machine simulates a $k$-tape machine that runs in time $t(n)$ in $O(t(n) \log t(n))$ steps (Hennie and Stearns, 1966). So the number of tapes beyond two changes the time by at most a log factor.
- **One tape is slower on some tasks.** Every one-tape machine that decides $\mathrm{PAL}$, with the input on its only tape, makes $\Omega(n^2)$ steps on some input of each length $n$ (Hennie, 1965, by the crossing sequence method). The two-tape machine above takes $3n + 4$ steps. So the quadratic loss of the simulation cannot be removed for the one-tape model in general.
- **Linear speedup.** Hartmanis and Stearns (1965) showed that a constant factor in the time can be removed. In the form of Papadimitriou (Section 2.4), for every $\varepsilon > 0$, a language decided by a multitape machine in time $t(n)$ is decided by another multitape machine, with a larger alphabet, in time $\varepsilon t(n) + n + 2$. The term $n + 2$ is the cost of reading the input and cannot be sped up. See the [linear speedup theorem](/linear-speedup-theorem/).
- **Time hierarchy.** Hartmanis and Stearns (1965) proved the first time hierarchy, with a gap of a square. The two-tape simulation of Hennie and Stearns improves it to this form: for time-constructible $g$ and $f(n) \log f(n) = o(g(n))$, $\mathrm{DTIME}(f) \subsetneq \mathrm{DTIME}(g)$. See the [time hierarchy theorem](/time-hierarchy-theorem/). For a fixed number $k \ge 2$ of tapes, Fürer (1982) removed the log factor: under a constructibility condition on $g$, $f = o(g)$ is enough for $k$-tape machines.
- **Time versus space.** Hopcroft, Paul and Valiant (1977) showed that a deterministic multitape machine of time $t(n)$ can be simulated by a deterministic machine with space $O(t(n)/\log t(n))$. With the space hierarchy theorem, this gives a language that is decided in space $O(t(n))$ but not in time $O(t(n))$, for space-constructible $t$. Williams (2025) improved the space of the simulation to $O(\sqrt{t(n) \log t(n)})$.
- **Determinism versus nondeterminism.** Paul, Pippenger, Szemerédi and Trotter (1983) proved $\mathrm{DTIME}(n) \ne \mathrm{NTIME}(n)$ for multitape machines. This is one of the few unconditional separations of deterministic and nondeterministic time. It is proved for this model only, and it does not extend in an obvious way to the RAM.

### Pitfalls

- **A linear-time bound must name the number of tapes.** $\mathrm{PAL}$ is in linear time on two tapes and needs quadratic time on one. A class such as $\mathrm{DTIME}(n)$ depends on the model, and the two textbook definitions (one tape in Sipser, many tapes in Papadimitriou) give different classes.
- **The simulation needs $t(n) \ge n$.** A machine with sublinear time does not read its whole input, but the simulation spends $\Theta(n)$ steps to lay out the input. For $t(n) < n$ the bound is $O(t(n)^2 + n)$, not $O(t(n)^2)$.
- **A step is one unit for all heads.** It is wrong to charge $k$ per step. The number of tapes changes the time only through the simulations above.
- **Hennie's bound is for one tape with the input on it.** With a separate read-only input tape and one work tape, the machine is a different model, and the $\Omega(n^2)$ bound of Hennie does not apply to it as stated.
- **Linear speedup does not beat the input length.** The speedup needs a larger alphabet, and it gives $\varepsilon t(n) + n + 2$, not $\varepsilon t(n)$. A machine that reads all of its input needs at least $n$ steps, whatever the constant factor.

## References
