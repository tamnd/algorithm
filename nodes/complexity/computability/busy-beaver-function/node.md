---
tag: 63B63B
kind: definition
slug: busy-beaver-function
name: Busy beaver function
aliases:
- Rado's busy beaver
- BB(n)
area: complexity/computability
level: advanced
summary: "The most ones, Sigma(n), or steps, S(n), of a halting n-state Turing machine started on a blank tape. It grows faster than every computable function; S(5) = 47,176,870."
prereqs: [turing-machine, halting-problem, uncomputable-function]
see_also: [halting-problem, uncomputable-function, turing-machine, ackermann-function, godel-incompleteness-theorem, kolmogorov-complexity, chaitins-constant, universal-turing-machine]
sources:
  - paper: doi:10.1002/j.1538-7305.1962.tb00480.x
    title: Tibor Rado, On non-computable functions, Bell System Technical Journal 41(3) (1962)
    locator: pp. 877 to 884
  - title: Shen Lin and Tibor Rado, Computer studies of Turing machine problems, Journal of the ACM 12(2) (1965)
    locator: pp. 196 to 212 (the values for three states)
  - paper: doi:10.1090/S0025-5718-1983-0689479-6
    title: Allen H. Brady, The determination of the value of Rado's noncomputable function Sigma(k) for four-state Turing machines, Mathematics of Computation 40(162) (1983)
    locator: pp. 647 to 665
  - paper: arxiv:2509.12337
    title: The bbchallenge Collaboration, Determination of the fifth Busy Beaver value, 2025
    locator: the main theorem, S(5) = 47,176,870, proved in Coq
  - paper: doi:10.1145/3427361.3427369
    title: Scott Aaronson, The busy beaver frontier, SIGACT News 51(3) (2020)
    locator: pp. 32 to 54
---

The busy beaver function measures how long a small Turing machine can run, or how much it can write, before it halts. Tibor Rado defined it in 1962. Among all Turing machines with $n$ states and two symbols that halt when started on a blank tape, $\Sigma(n)$ is the largest number of ones left on the tape, and $S(n)$ is the largest number of steps. Both are well defined, because there are only finitely many such machines, yet neither is computable: each grows faster than every computable function. The known values are tiny for small $n$ and then explode: $S(4) = 107$, while $S(5) = 47{,}176{,}870$, a value proved in 2024 by the bbchallenge collaboration with a proof checked by the Coq proof assistant. The name $\mathrm{BB}(n)$ is used for both functions in the literature; this page writes $\Sigma$ and $S$.

## Definition

Use Rado's machine model. A machine has states $A, B, \ldots$ (here $n$ of them), a halt state, and a tape over $\{0, 1\}$ that is infinite in both directions. Each of the $2n$ pairs (state, symbol read) has one transition: write $0$ or $1$, move left or right, and go to one of the $n$ states or halt. The halting transition also writes and moves, and it counts as a step. The machine starts in state $A$ on an all-zero tape.

For each $n \ge 1$, let $H_n$ be the set of such machines with $n$ states that halt. Then
$$\Sigma(n) = \max_{M \in H_n} (\text{number of ones on the tape when } M \text{ halts}),$$
$$S(n) = \max_{M \in H_n} (\text{number of steps } M \text{ makes before it halts}).$$

Each transition has $2 \cdot 2 \cdot (n + 1) = 4(n + 1)$ choices, so there are $(4(n+1))^{2n}$ machines with $n$ states: $64$ for $n = 1$, $20{,}736$ for $n = 2$, $16{,}777{,}216$ for $n = 3$, $25{,}600{,}000{,}000$ for $n = 4$, and $63{,}403{,}380{,}965{,}376$ for $n = 5$. The set $H_n$ is finite, and it contains the machine that halts at once, so both maxima exist.

**Notation.** Machines are written as in the bbchallenge project: for each state in order, two transitions, for reading $0$ and reading $1$, each as write, move, next state, with $Z$ for halt. So `1RB1LB_1LA1RZ` means: in $A$ reading $0$, write $1$, move right, go to $B$; in $A$ reading $1$, write $1$, move left, go to $B$; in $B$ reading $0$, write $1$, move left, go to $A$; in $B$ reading $1$, write $1$, move right, halt.

**Known values.**

| $n$ | $S(n)$ | $\Sigma(n)$ |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 6 | 4 |
| 3 | 21 | 6 |
| 4 | 107 | 13 |
| 5 | 47,176,870 | 4098 |

The values for three states are due to Lin and Rado (1965), for four states to Brady (1983), and for five states to the bbchallenge collaboration (2024). For $n = 6$ the values are unknown and known to be enormous; Aaronson (2020) surveys the lower bounds.

**Theorem (Rado 1962).** For every total computable function $f$, there is an $m_0$ with $\Sigma(m) > f(m)$ for all $m \ge m_0$. In particular, $\Sigma$ is not computable. Since a machine writes at most one new one per step, $S(n) \ge \Sigma(n)$, so the same holds for $S$.

*Proof.* Let $F(x) = 1 + \max_{i \le x} f(i)$. Then $F$ is computable, $F(x) > f(x)$, and $F$ is nondecreasing. Fix three machines:

- for each $n$, a machine $W_n$ with $n$ states that writes a block of $n$ ones and halts next to it (state $i$ writes $1$, moves right and goes to state $i + 1$, and state $n$ halts);
- a machine $D$ with $d$ states that turns a block of $k$ ones into a block of $2k$ ones;
- a machine $P$ with $p$ states that turns a block of $x$ ones into a block of $F(x)$ ones, which exists because $F$ is computable.

Join them in sequence by sending the halting transitions of each part to the start state of the next. The result has $n + c$ states with $c = d + p$, halts on the blank tape, and leaves $F(2n)$ ones. So $\Sigma(n + c) \ge F(2n)$. For $n \ge c$ we have $2n \ge n + c$, so $\Sigma(n + c) \ge F(2n) \ge F(n + c) > f(n + c)$. Thus $\Sigma(m) > f(m)$ for every $m \ge 2c$. $\blacksquare$

**Link to halting.** If $S(n)$ were known, halting on the blank tape would be decidable for all machines with $n$ states: run the machine for $S(n)$ steps, and if it has not halted, it never will. This is why $S$ cannot be computable, and why each new value needs a proof that every remaining machine runs forever.

## Examples and non-examples

**The two-state champion.** The machine `1RB1LB_1LA1RZ` halts after $6$ steps with $4$ ones on the tape:

| step | state before | symbol read | action | ones after |
|---|---|---|---|---|
| 1 | A | 0 | write 1, right, to B | 1 |
| 2 | B | 0 | write 1, left, to A | 2 |
| 3 | A | 1 | write 1, left, to B | 2 |
| 4 | B | 0 | write 1, left, to A | 3 |
| 5 | A | 0 | write 1, right, to B | 4 |
| 6 | B | 1 | write 1, right, halt | 4 |

Running all $20{,}736$ two-state machines for $100$ steps each finds no halting machine with more than $6$ steps or more than $4$ ones, in line with $S(2) = 6$ and $\Sigma(2) = 4$.

**Three states.** The machine `1RB1RZ_1LB0RC_1LC1LA` halts after $21$ steps with $5$ ones, which gives $S(3) = 21$. The machines `1RB1RZ_0RC1RB_1LC1LA` (14 steps) and `1RB1LC_1LA1RB_1LB1RZ` (13 steps) each leave $6$ ones, which gives $\Sigma(3) = 6$. So the machine that runs longest is not the one that writes most.

**Four and five states.** The machine `1RB1LB_1LA0LC_1RZ1LD_1RD0RA` halts after $107$ steps with $13$ ones. The five-state champion `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA`, found by Marxen and Buntrock in 1989, halts after $47{,}176{,}870$ steps with $4098$ ones. The bbchallenge proof enumerated $181{,}385{,}789$ five-state machines, up to symmetries and machines that cannot matter, and decided for each one whether it halts.

**Non-example: a computable "busy beaver".** For a language in which every program halts, such as LOOP programs or primitive recursive definitions, the largest output of a program of size $n$ is computable: run all of them. It still grows fast, faster than every function in that language, but it is not a busy beaver function in Rado's sense.

**Non-example: the Ackermann function.** The [Ackermann function](/ackermann-function/) grows faster than every primitive recursive function, but it is computable, so by the theorem $\Sigma$ eventually exceeds it.

## Related definitions

- **More symbols.** $S(n, k)$ and $\Sigma(n, k)$ use machines with $n$ states and $k$ symbols. The bbchallenge paper also proves $S(2, 4) = 3{,}932{,}964$.
- **Halting problem.** $S$ is computable from an oracle for the [halting problem](/halting-problem/), and the halting problem for blank-tape machines is computable from $S$. So $S$ has the [Turing degree](/turing-degrees/) $\mathbf{0}'$.
- **Uncomputable functions.** $\Sigma$ is the standard example of an [uncomputable function](/uncomputable-function/) with a simple definition, and of a function that grows faster than every computable one.
- **Kolmogorov complexity and Chaitin's constant.** [Kolmogorov complexity](/kolmogorov-complexity/) measures the shortest description of a string, and [Chaitin's constant](/chaitins-constant/) packs the halting behavior of all programs into one real number. All three encode the halting problem in a different shape.
- **Independence.** A formal theory that proves only true statements can determine $\Sigma(n)$ and $S(n)$ for only finitely many $n$; see [Gödel's incompleteness theorems](/godel-incompleteness-theorem/). Yedidia and Aaronson built a machine with $7918$ states whose halting is equivalent to the inconsistency of ZFC set theory, so ZFC, if consistent, cannot determine $S(7918)$ (Aaronson 2020).

## References
