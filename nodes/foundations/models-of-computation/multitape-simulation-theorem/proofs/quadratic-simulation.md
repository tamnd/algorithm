---
title: A one-tape machine simulates a k-tape machine in time t^2 + (2k+4)t
id: quadratic-simulation
proves: [quadratic-simulation]
method: induction
form: full
sources:
  - {book: "isbn:9781133187790", locator: "Sipser 3rd ed., Section 7.1, Theorem 7.8"}
  - {title: "Hartmanis and Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117, 1965", locator: "pp. 285 to 306"}
---

**Statement.** Let $M$ be a deterministic $k$-tape machine with input alphabet $\Sigma$ that decides $L \subseteq \Sigma^*$ and halts within $t(n)$ steps on every input of length $n$, where $t(n) \ge \max(n, 1)$. Then there is a deterministic one-tape machine $S$ that decides $L$ and halts on every input of length $n$ within $t(n)^2 + (2k+4)\,t(n)$ steps. In particular $S$ halts within $(2k+5)\,t(n)^2$ steps.

**Setup.** The machines are as on the [multitape Turing machine](/multitape-turing-machine/) page. Tape cells are numbered $0, 1, \ldots$. A head on cell $0$ with the move $L$ stays. Let $\Gamma$ be the tape alphabet of $M$, with blank $\sqcup$. Fix an input $w$ of length $n$. Let $t' \ge 1$ be the number of steps of $M$ on $w$. We have $t' \ge 1$ because the start state is not halting. We have $t' \le t(n)$.

*The alphabet of $S$.* The tape alphabet of $S$ is $\Sigma$ together with the tuples $(c_1, \ldots, c_k, f_1, \ldots, f_k, e)$. Here $c_i \in \Gamma$, $f_i \in \{0, H\}$, and $e \in \{0, 1\}$. The blank of $S$ is the tuple with all $c_i = \sqcup$, all $f_i = 0$ and $e = 0$. The input symbols of $S$ are those of $\Sigma$. The alphabet is finite. The blank tuple also stands for blank cells of $M$ in later sweeps.

*Meaning.* Cell $j$ of the tape of $S$ is a column. It holds the content $c_i$ of cell $j$ of tape $i$ of $M$ for each $i$. The flag $f_i = H$ means that head $i$ of $M$ is on cell $j$. The bit $e$ is $1$ exactly in cell $0$, so that $S$ can find the left end.

*The state of $S$.* It holds a state of $M$, a phase name, and a bounded buffer: the at most $k$ symbols $a_i$ read, and the at most $k$ pending flags described below. All of these come from finite sets.

**Invariant $I_s$.** After $s$ simulated steps, $S$ is on cell $0$, its state holds the state of $M$ after $s$ steps, and for every $i$ and $j$: the component $c_i$ of cell $j$ is the content of cell $j$ of tape $i$ of $M$, and $f_i = H$ in cell $j$ exactly when head $i$ is on cell $j$.

**Proof.**

*Step 1: start.* Let $n \ge 1$. $S$ moves right from cell $0$. In cell $j < n$ it reads $w_{j+1}$ and writes the tuple with $c_1 = w_{j+1}$, all other $c_i = \sqcup$, all $f_i = 0$ except that $f_i = H$ for all $i$ in cell $0$, and $e = 1$ in cell $0$ only. It does this in $n$ transitions and arrives at cell $n$. There it reads the blank of $S$ (a tuple that is not a symbol of $\Sigma$) and moves left. It moves left once in each of cells $n, n-1, \ldots, 1$, which is $n$ transitions, and arrives at cell $0$. It finds the cell by $e = 1$ when the next phase starts. If $n = 0$, $S$ writes in one transition, on cell $0$, the tuple with all $c_i = \sqcup$, all $f_i = H$ and $e = 1$, and stays. So the start takes at most $2n + 2$ transitions. Now $I_0$ holds, since all heads of $M$ are on cell $0$.

*Step 2: one simulated step.* Assume $I_s$ with $M$ in a state $q$ that is not accept or reject. Let $p_i$ be the cell of head $i$ of $M$ and $P = \max_i p_i$. Each head starts on cell $0$ and moves at most one cell in each step, so $P \le s$.

- *Right sweep.* $S$ moves right from cell $0$. In each cell it reads the tuple. For each $i$ with $f_i = H$ it stores $c_i$ as $a_i$. It moves right in cells $0, \ldots, P - 1$, which is $P$ transitions. It does not need to know $P$. It knows that it is in cell $P$ when it has stored all $k$ symbols $a_1, \ldots, a_k$ after reading that cell.
- *Decision.* After reading cell $P$, the control computes $\delta(q, a_1, \ldots, a_k) = (q', b_1, \ldots, b_k, D_1, \ldots, D_k)$. If $q'$ is accept or reject, $S$ halts in the same way, in the same transition. By $I_s$, $S$ then gives the verdict of $M$. Otherwise $S$ starts the left sweep in cell $P$, in this same transition.
- *Left sweep.* $S$ moves left from cell $P$ to cell $0$. In each cell $j$ it reads the tuple and writes it again with these changes, for every $i$ with $f_i = H$ (a cell with $f_i = H$ for some $i$ is a cell where a head of $M$ stands). It sets $c_i = b_i$. Then it changes the flag by $D_i$.
  - If $D_i = S$, the flag stays $H$.
  - If $D_i = L$ and $e = 0$, the flag becomes $0$, and the control remembers that the flag $f_i = H$ must be written in cell $j - 1$ when $S$ gets there.
  - If $D_i = L$ and $e = 1$, the flag stays $H$, by the rule for cell $0$.
  - If $D_i = R$, the flag becomes $0$. The control remembers that cell $j + 1$ needs $f_i = H$. This is the *detour* below.

  The changes apply to the flags that $S$ reads in cell $j$. A pending flag is added after them, so it is not processed again in this sweep. A pending flag for cell $j - 1$ is for a tape $i$ whose head was on cell $j$. Cell $j - 1$ holds no flag $f_i = H$ for this tape, since each tape has one head. So the new flag does not clash with an old one.
- *Detour.* Let cell $j$ have heads with $D_i = R$ (at least one). The cell $j$ is written in the way above, and $S$ moves right instead of left. In cell $j + 1$ it sets $f_i = H$ for all those $i$, without other change, and moves left. In cell $j$ it moves left again, without change (it has already written the cell), and goes on with the left sweep. A detour takes 2 transitions beyond the ones counted in the sweep. In a step of $M$ at most $k$ heads move right, so there are at most $k$ cells with a detour, and the detours cost at most $2k$ transitions.
- *Return.* In cell $0$ the left sweep ends: $S$ reads $e = 1$, writes the cell, and the left-move rule keeps it on cell $0$. Now $I_{s+1}$ holds. Every head of $M$ has moved by $D_i$ and every symbol is written.

The sweeps use $P$ right-moves, then $P + 1$ transitions in the cells $P, \ldots, 0$, so $2P + 1$ transitions, plus at most $2k$ for the detours. So simulated step number $s + 1$ takes at most $2s + 1 + 2k$ transitions of $S$.

*Step 3: correctness.* Base: $I_0$ holds by step 1. Step: assume $I_s$ (the induction hypothesis) and that $M$ has not halted after $s$ steps; step 2 gives $I_{s+1}$. So $I_s$ holds for $s = 0, 1, \ldots, t' - 1$, and the simulation does not halt before the step in which $M$ halts. In the last step, step number $t'$, $S$ halts with the verdict of $M$.

*Step 4: time.* The total number of transitions of $S$ is at most

$$
(2n + 2) + \sum_{s=0}^{t'-1} (2s + 1 + 2k) = 2n + 2 + t'(t'-1) + t' + 2k t' = t'^2 + 2k\,t' + 2n + 2 .
$$

Since $n \le t(n)$ and $1 \le t(n)$ we have $2n + 2 \le 4 t(n)$, and $t' \le t(n)$. So the total is at most $t(n)^2 + (2k + 4)\, t(n)$. Since $t(n) \ge 1$, this is at most $(2k + 5)\, t(n)^2$. $\blacksquare$
