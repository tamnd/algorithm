---
tag: XWP8SM
kind: model
slug: turing-machine
name: Turing machine
aliases: [Turing machines, TM]
area: foundations/models-of-computation
level: intro
summary: A finite control with one head that reads and writes symbols on an infinite tape. It is the standard model of general computation.
prereqs: []
see_also: [multitape-turing-machine, nondeterministic-turing-machine, universal-turing-machine, church-turing-thesis, halting-problem, lambda-calculus, ram-turing-equivalence, multitape-simulation-theorem]
sources:
  - title: Martin Davis, Computability and Unsolvability, McGraw-Hill, 1958
    locator: the treatment of the halting problem
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society, series 2, volume 42
    locator: pp. 230 to 265
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 3, sections "Turing Machines" and "Variants of Turing Machines"
  - paper: doi:10.1145/321356.321362
    title: Frederick C. Hennie and Richard E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM, volume 13, issue 4
    locator: pp. 533 to 546
  - paper: doi:10.1002/j.1538-7305.1962.tb00480.x
    title: Tibor Rado, On non-computable functions, Bell System Technical Journal, volume 41, issue 3
    locator: pp. 877 to 884
  - paper: doi:10.1016/S0019-9958(65)90399-2
    title: Frederick C. Hennie, One-tape, off-line Turing machine computations, Information and Control, volume 8, issue 6, 1965
    locator: pp. 553 to 578
  - paper: doi:10.1109/FOCS.1965.11
    title: Richard E. Stearns, Juris Hartmanis and Philip M. Lewis, Hierarchies of memory limited computations, IEEE Conference Record on Switching Circuit Theory and Logical Design, 1965
    locator: pp. 179 to 190
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society, volume 117
    locator: pp. 285 to 306
---

A Turing machine is a model of computation with a finite control and one head that reads and writes symbols on a tape that is infinite to the right. In each step it reads one symbol, writes one symbol, moves the head one cell and changes its state, by a fixed table of rules. Alan Turing described this kind of machine in 1936 to give a precise meaning to a mechanical procedure. It is the standard model of general computation, and the time and space bounds of complexity theory are stated on it. The [Church-Turing thesis](/church-turing-thesis/) says that it computes everything that a mechanical procedure computes.

## The machine

A Turing machine $M$ has four parts:

- a finite set $Q$ of states, with a start state $q_0$ and two distinct halting states, *accept* and *reject*;
- a finite tape alphabet $\Gamma$ that contains a blank symbol $\sqcup$;
- a finite input alphabet $\Sigma \subseteq \Gamma \setminus \{\sqcup\}$;
- a transition function $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma \to Q \times \Gamma \times \{L, R\}$.

The tape has cells numbered $0, 1, 2, \ldots$.
Cell $0$ is the left end, and the tape is infinite to the right.
Each cell holds one symbol from $\Gamma$.
At the start, the input $w = w_1 w_2 \cdots w_n$ fills cells $0$ to $n-1$ (the symbol $w_i$ is in cell $i-1$), every other cell holds the blank, and the head is on cell $0$.

One step works like this.
The machine is in state $q$, and the head reads the symbol $a$ in its cell.
If $\delta(q, a) = (p, b, D)$, the machine writes $b$ over $a$, moves the head one cell in direction $D$, and enters state $p$.
If the head is on cell $0$ and the move is $L$, the head stays where it is.
This convention only fixes a case that the tape does not otherwise allow, so it does not change what the model can compute.

A **configuration** records everything that decides the next step.
It has three parts: the state, the tape content and the head position.
We write it as $u\,q\,v$.
Here $q$ is the state, $u$ is the tape to the left of the head, and $v$ is the tape from the head to the right.
The head reads the first symbol of $v$.
Blanks at the right end of $v$ are dropped, and blanks in $u$ are kept, so an empty $v$ means that the head reads a blank.
The start configuration on input $w$ is $q_0\,w$.
A configuration is *accepting* if its state is accept, and *halting* if its state is accept or reject.

A **step** turns one configuration into the next, and we write $C \vdash C'$ when $C'$ follows $C$ in one step.
Let $q$ be the state, let $v = a\,v'$ (if $v$ is empty, then $a$ is the blank and $v'$ is empty), and let $\delta(q, a) = (p, b, D)$.
- If $D = R$, then $u\,q\,v \vdash u\,b\,p\,v'$, because the head writes $b$ and moves right.
- If $D = L$ and $u = u'\,c$ for a symbol $c$, then $u\,q\,v \vdash u'\,p\,c\,b\,v'$, because the head writes $b$ and moves left onto $c$.
- If $D = L$ and $u$ is empty, then $q\,v \vdash p\,b\,v'$, by the convention for cell $0$.

In each case, drop any blanks at the right end of the new $v$.

A **computation** on $w$ is a sequence $C_0 \vdash C_1 \vdash C_2 \vdash \cdots$ with $C_0 = q_0\,w$, in which each configuration follows the one before it.
It stops at the first halting configuration, if there is one.

The language $L(M)$ of $M$ is the set of words $w \in \Sigma^*$ whose computation reaches an accepting configuration.
The machine *decides* a language $L$ if it halts on every input and $L(M) = L$.
It *recognizes* $L$ if $L(M) = L$, but it may run forever on words outside $L$.
A machine *computes* a function $f$ if, on every input $w$ in the domain of $f$, the computation halts in state accept and the tape then holds $f(w)$ followed by blanks.

The machine has many equivalent variants, and each of them has the same power as the model above.
- **Stay move.** A rule may move the head $S$, which keeps it in place.
  A stay move is a right move followed by a left move through one extra state for each target state, so it costs two steps instead of one.
- **Two-way infinite tape.** The cells may extend to the left as well, so that cell $0$ is not an end.
  Fold the tape at cell $0$: the two halves sit on two tracks, cell $0$ carries a marker, and the state records which track the head is on.
- **Binary alphabet.** If $\Sigma = \{0,1\}$, the tape alphabet may be reduced to the symbols $0$, $1$ and the blank.
  Each symbol of $\Gamma$ is coded by a fixed block of $\lceil \lg |\Gamma| \rceil$ cells. Each step of $M$ costs $O(\log |\Gamma|)$ steps.
  Coding the input first costs $O(n^2)$ steps on one tape ($O(n)$ on two tapes).

An example shows the rules at work.
The machine below decides the language $\{0^n 1^n : n \ge 0\}$, with $\Sigma = \{0, 1\}$ and $\Gamma = \{0, 1, X, Y, \sqcup\}$.
Each round marks the leftmost unmarked $0$ with $X$, and then the leftmost unmarked $1$ after it with $Y$.
The head then walks back to the $X$ and starts the next round.
A pair (state, symbol) that the table does not list goes to reject.

| State | Reads | Writes | Moves | Next state |
|---|---|---|---|---|
| $q_0$ | $0$ | $X$ | $R$ | $q_1$ |
| $q_0$ | $Y$ | $Y$ | $R$ | $q_3$ |
| $q_0$ | $\sqcup$ | $\sqcup$ | $R$ | accept |
| $q_1$ | $0$ | $0$ | $R$ | $q_1$ |
| $q_1$ | $Y$ | $Y$ | $R$ | $q_1$ |
| $q_1$ | $1$ | $Y$ | $L$ | $q_2$ |
| $q_2$ | $0$ | $0$ | $L$ | $q_2$ |
| $q_2$ | $Y$ | $Y$ | $L$ | $q_2$ |
| $q_2$ | $X$ | $X$ | $R$ | $q_0$ |
| $q_3$ | $Y$ | $Y$ | $R$ | $q_3$ |
| $q_3$ | $\sqcup$ | $\sqcup$ | $R$ | accept |

Let the input be $0^a 1^b$ with $a, b \ge 0$. After $k$ rounds, for $k \le \min(a,b)$, the tape is $X^k\,0^{a-k}\,Y^k\,1^{b-k}$, and the head is on cell $k$ in state $q_0$, which holds a $0$ if $k < a$, a $Y$ if $0 < k = a$, and the first symbol of $1^b$ (a $1$ or a blank) if $k = a = 0$. We now show that every accepted word has the form $0^n 1^n$.

1. Each round writes one $X$ at the head cell, and $q_2$ moves left only over $0$ and $Y$ and stops on the first $X$. So $q_0$ always reads the cell just right of the block of $X$s.
2. The machine accepts in two ways: $q_0$ reads a blank, or $q_3$ reads a blank. If $k \ge 1$ rounds are done, the last round wrote a $Y$ to the right of the block of $X$s, and $q_1$ moved only over $0$ and $Y$ to reach it. So the cell just right of the block holds a $0$ or a $Y$, and $q_0$ reads a blank only when $k = 0$, that is, on the empty input.
3. State $q_3$ is entered only from $q_0$ reading a $Y$, and it accepts only if every cell from there up to the first blank is $Y$.
4. The machine never writes a blank, so the first blank is the end of the input.
5. So an accepted nonempty tape is $X^k Y^m$. Each round makes one $X$ and one $Y$, so $m = k$. Each $X$ was a $0$ and each $Y$ was a $1$, so the input was $0^k 1^k$.

Conversely, on $0^k 1^k$ the machine makes $k$ rounds and reaches $q_3$ on the first $Y$, and the empty word is accepted at once. So the machine accepts exactly the words $0^n 1^n$.
Here is the computation on $01$.

$$
q_0\,01 \vdash X\,q_1\,1 \vdash q_2\,XY \vdash X\,q_0\,Y \vdash XY\,q_3 \vdash XY\sqcup\,\mathrm{accept}
$$

## What it counts

The time on an input $w$ is the number of steps before the machine halts.
A machine that does not halt on $w$ has no finite time on $w$.
The worst-case time $T(n)$ is the largest time over all inputs of length $n$.

The space on an input $w$ is the number of distinct tape cells that the head visits during the computation.
On the one-tape machine the input is on the tape, so the input cells that the head visits count as space.
A machine that reads every cell of an input of length $n$ has space at least $n$ on that input.
Some texts give the machine a separate read-only input tape, and the space then counts only the cells of the work tapes that the head visits.
This read-only input model is the one that allows sublinear space, such as $\log n$.

Each complexity class is a set of languages defined by a bound on a machine.
$\mathrm{DTIME}(f(n))$ is the set of languages that a machine decides in time $O(f(n))$, on a multitape machine. Some texts, such as Sipser, define the class (named $\mathrm{TIME}(t(n))$ there) on the one-tape machine instead. The two classes can differ, but P is the same under both.
$\mathrm{DSPACE}(f(n))$ is the set of languages that a machine decides with space $O(f(n))$ on the read-only input model.
For $f(n) \ge n$ the two space measures give the same class, because a copy of the input costs only $n$ extra cells.
The class $\mathrm{L} = \mathrm{DSPACE}(\log n)$ uses the read-only input model.
The class of polynomial time is the union of $\mathrm{DTIME}(n^k)$ over all $k \ge 1$.
It is the class [P](/p/).

Because a step is one unit, the time counts single-symbol moves.
A model with unit-cost arithmetic on whole words counts differently, so a bound must name its model.

## Relation to other models

A [multitape Turing machine](/multitape-turing-machine/) has $k$ tapes, each with its own head.
It has the same power as the one-tape model.
The [multitape simulation theorem](/multitape-simulation-theorem/) gives a one-tape machine that runs in $O(T(n)^2)$ steps for each multitape machine that runs in $T(n) \ge n$ steps.
Hennie and Stearns showed that a two-tape machine can simulate a $k$-tape machine that runs in time $T(n)$ in $O(T(n)\log T(n))$ steps.

Nondeterministic, probabilistic, alternating and oracle machines keep the tape and the head.
They change only the rules of the transition: several choices, random choices, a set of branches or a query to a fixed language.
Each has its own page: [nondeterministic Turing machine](/nondeterministic-turing-machine/), [probabilistic Turing machine](/probabilistic-turing-machine/), [alternating Turing machine](/alternating-turing-machine/) and [oracle Turing machine](/oracle-turing-machine/).
A [quantum Turing machine](/quantum-turing-machine/) is different: it changes a superposition of configurations by a unitary map.

The [random-access machine](/random-access-machine/) can read and write any register in one step.
[RAM and Turing machine equivalence](/ram-turing-equivalence/) shows that a Turing machine computes the same functions as a RAM.
Under the [logarithmic cost model](/logarithmic-cost-model/), each model simulates the other with only a polynomial loss of time, so polynomial time is the same in both.

The [word RAM](/word-ram/) does arithmetic on a whole word in one step.
A Turing machine needs one step for each cell it touches, so the two models give different running times for the same task.
A bound on a word RAM therefore does not transfer to a Turing machine by a constant factor.

The [lambda calculus](/lambda-calculus/) and the Turing machine compute the same functions.
The [Church-Turing thesis](/church-turing-thesis/) says that this class is the class of all functions that a mechanical procedure can compute.
The thesis is an informal claim, not a theorem.

[Boolean circuits](/boolean-circuit/) are a different kind of model.
A family of circuits has one circuit for each input size, so it is non-uniform, and the [non-uniform computation](/non-uniform-computation/) page explains the difference.

## Known results in the model

- **The machine and its universal form.** Turing defined the machine in 1936.
  Turing's original machines print infinite binary sequences. The accept and reject form used here is the later textbook convention.
  He also gave a [universal Turing machine](/universal-turing-machine/), which reads the description of another machine and simulates it on an input. Each machine $M$ has a description $\langle M\rangle$, a string over a fixed alphabet that lists its transition table.
- **The halting problem.** No Turing machine decides whether a given machine halts on a given input.
  Turing proved in the same 1936 paper that no machine decides whether a given machine is circle-free, or whether it ever prints a given symbol. The [halting problem](/halting-problem/) is the later, equivalent form of this result, popularized by Davis (1958).
  The same paper applies the machine to the [Entscheidungsproblem](/entscheidungsproblem/).
- **Rice's theorem.** For every non-trivial property $P$ of languages (some recognizable language has $P$ and some does not), the set of descriptions $\langle M\rangle$ with $L(M)\in P$ is undecidable.
  See [Rice's theorem](/rice-theorem/).
- **Busy beaver.** The busy beaver function counts the most $1$s that a halting machine with $n$ states and two symbols leaves on a blank tape. Radó (1962) defined it. It is not computable, and it grows faster than every computable function. See the [busy beaver function](/busy-beaver-function/).
- **The quadratic simulation is tight.** The [multitape simulation theorem](/multitape-simulation-theorem/) is stated above. Every one-tape machine whose input is on its work tape and that decides the even-length palindromes $\{w w^R : w \in \{0,1\}^*\}$ takes $\Omega(n^2)$ steps on some input of each even length $n$ (Hennie 1965, by crossing sequences), while a two-tape machine takes $O(n)$. So the $O(T(n)^2)$ simulation cannot be improved in general.
- **Time and space hierarchies.** Hartmanis and Stearns began the study of time bounds on multitape machines in 1965, and Stearns, Hartmanis and Lewis did the same for space in the same year.
  The hierarchy results need conditions on the bounds.
  For time-constructible $f,g$ with $f(n)\log f(n)=o(g(n))$, $\mathrm{DTIME}(f)\subsetneq\mathrm{DTIME}(g)$ on multitape machines.
  For space-constructible $f,g \ge \log n$ with $f=o(g)$, $\mathrm{DSPACE}(f)\subsetneq\mathrm{DSPACE}(g)$ on the read-only input model.
  Without such conditions, a larger bound can add no new languages, so the claim "more time or more space decides more languages" is false in general.
  See the [time hierarchy theorem](/time-hierarchy-theorem/) and the [space hierarchy theorem](/space-hierarchy-theorem/).
- **Linear speedup.** For $\varepsilon>0$, a $k$-tape machine with $k\ge 2$ that runs in time $T(n)$ can be rebuilt, with a larger tape alphabet, to run in time $\varepsilon T(n)+n+2$.
  This is not a one-tape statement.
  See the [linear speedup theorem](/linear-speedup-theorem/).

## References

- Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society, series 2, volume 42, pp. 230 to 265. doi:10.1112/plms/s2-42.1.230
- Michael Sipser, Introduction to the Theory of Computation, third edition, Chapter 3. isbn:9781133187790
- Frederick C. Hennie and Richard E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM, volume 13, issue 4, pp. 533 to 546. doi:10.1145/321356.321362
- Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society, volume 117, pp. 285 to 306. doi:10.1090/S0002-9947-1965-0170805-7
