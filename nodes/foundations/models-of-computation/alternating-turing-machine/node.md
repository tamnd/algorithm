---
tag: 12W6M0
kind: model
slug: alternating-turing-machine
name: Alternating Turing machine
aliases:
- ATM
area: foundations/models-of-computation
level: advanced
summary: Nondeterministic machine whose states are existential or universal; characterizes PSPACE and the polynomial hierarchy.
prereqs: [turing-machine, nondeterministic-turing-machine, multitape-turing-machine]
see_also: [nondeterministic-turing-machine, polynomial-hierarchy, pspace, exptime, qbf, p, np]
sources:
  - title: A. K. Chandra and L. J. Stockmeyer, Alternation, and D. C. Kozen, On parallelism in Turing machines, 17th Annual Symposium on Foundations of Computer Science, 1976
    locator: the two conference papers in which the model was introduced
  - title: L. J. Stockmeyer and A. R. Meyer, Word problems requiring exponential time, 5th Annual ACM Symposium on Theory of Computing, 1973
    locator: the PSPACE-completeness of the evaluation of quantified Boolean formulas
  - title: Walter L. Ruzzo, On uniform circuit complexity, Journal of Computer and System Sciences 22(3), 1981
    locator: the characterization of uniform NC^1 by alternating machines
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM, volume 28, issue 1
    locator: pp. 114 to 133
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 10.3, Alternation
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 5, the section on alternating Turing machines
---

An alternating Turing machine is a [nondeterministic Turing machine](/nondeterministic-turing-machine/) whose non-halting states are of two kinds: existential states accept if some successor accepts, and universal states accept if all successors accept. Chandra and Stockmeyer, and Kozen separately, introduced it in 1976, and Chandra, Kozen and Stockmeyer published the joint journal version in 1981. It gives machine definitions of the [polynomial hierarchy](/polynomial-hierarchy/) and of the classes [PSPACE](/pspace/) and [EXP](/exptime/): polynomial time on this machine is exactly PSPACE, and polynomial space is exactly EXP.

## The machine

An alternating machine $M$ has the parts of the nondeterministic machine: a finite set $Q$ of states with a start state $q_0$, a tape alphabet $\Gamma \ni \sqcup$, an input alphabet $\Sigma$, and a transition function

$$
\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma \to \mathcal{P}(Q \times \Gamma \times \{L, R\}).
$$

We assume that $\delta(q, a) \ne \emptyset$ for every non-halting $q$ and every $a \in \Gamma$, so that each non-halting configuration has a successor. (Add a move to the reject state where the set is empty.) The extra part is a partition of the non-halting states

$$
Q \setminus \{\text{accept}, \text{reject}\} = Q_\exists \,\sqcup\, Q_\forall .
$$

A configuration is *existential* or *universal* by its state, and we write $C \vdash C'$ as for the [nondeterministic machine](/nondeterministic-turing-machine/). The start configuration on input $w$ is $q_0\,w$.

**Acceptance.** Let $\mathcal{A}_w$ be the least set of configurations (for the machine $M$) with these three properties:

- every configuration with state accept is in $\mathcal{A}_w$;
- an existential configuration $C$ is in $\mathcal{A}_w$ if some $C'$ with $C \vdash C'$ is in $\mathcal{A}_w$;
- a universal configuration $C$ is in $\mathcal{A}_w$ if every $C'$ with $C \vdash C'$ is in $\mathcal{A}_w$.

The machine *accepts* $w$ if $q_0\,w \in \mathcal{A}_w$. The language of $M$ is $L(M) = \{ w \in \Sigma^* : M \text{ accepts } w\}$. The least set exists because the three rules are monotone. A configuration is in $\mathcal{A}_w$ exactly when it has a finite *accepting subtree*: a finite tree in which the root is the configuration, each existential node keeps one child, each universal node keeps all its children, and every leaf is an accepting configuration. So an infinite path never helps a universal node to accept. The computation tree is the same tree as for the nondeterministic machine, with a different rule for the verdict.

The machine *decides* $L$ if $L(M) = L$ and every path on every input is finite. If $Q_\forall = \emptyset$, the rule is the nondeterministic rule. If $Q_\exists = \emptyset$ and every path is finite, the machine accepts exactly when all paths end in accept. Then it decides the complement of the language of the nondeterministic machine with accept and reject exchanged.

**Example: a quantified Boolean formula.** Take the formula $\varphi = \forall x\, \exists y\, \big((x \lor y) \land (\lnot x \lor \lnot y)\big)$. An alternating machine writes the value of $x$ in a universal state, with two successors: $x = 0$ and $x = 1$. It then writes $y$ in an existential state, with two successors. It then evaluates the quantifier-free part deterministically and accepts if the part is true. For $x = 0$ the choice $y = 1$ accepts, and for $x = 1$ the choice $y = 0$ accepts. So both branches of the universal node accept and the machine accepts. Swap the quantifiers to get $\exists x\, \forall y$ with the same part. Then each choice of $x$ has a value of $y$ that fails, so the machine rejects. The same construction works for each [quantified Boolean formula](/qbf/): one state kind for each quantifier, one branching step for each variable, and a polynomial number of steps in all.

## What it counts

The **time** of $M$ on an input is the length of its longest computation path, as for the nondeterministic machine. $M$ runs in time $t(n)$ if on every input of length $n$ every path has at most $t(n)$ steps. The **space** is the largest number of work-tape cells that the heads visit on any path (the read-only input tape is not counted when the space is below $n$). For a function $t$, $\mathrm{ATIME}(t(n))$ and $\mathrm{ASPACE}(t(n))$ are the sets of languages that a multitape alternating machine decides in time $O(t(n))$ and in space $O(t(n))$. For space below $n$, the input is on a read-only tape, as in the [Turing machine](/turing-machine/) page. Define

$$
\mathrm{AP} = \bigcup_{k \ge 1} \mathrm{ATIME}(n^k), \qquad \mathrm{APSPACE} = \bigcup_{k \ge 1} \mathrm{ASPACE}(n^k), \qquad \mathrm{AL} = \mathrm{ASPACE}(\log n).
$$

A third measure is the number of **alternations** on a path: the number of times that the path goes from a state of one kind to a state of the other kind. A machine is $\Sigma_k$ if every path starts in an existential state and has at most $k - 1$ alternations.

## Relation to other models

A [nondeterministic Turing machine](/nondeterministic-turing-machine/) is an alternating machine with only existential states, so $\mathrm{NP} \subseteq \mathrm{AP}$ and $\mathrm{coNP} \subseteq \mathrm{AP}$. The machine with no alternation bound sits above the whole [polynomial hierarchy](/polynomial-hierarchy/). With a bound on the alternations, a language is in $\Sigma_k^p$ if and only if a polynomial-time machine of type $\Sigma_k$ decides it. This is the machine form of the hierarchy, and Chandra, Kozen and Stockmeyer give it in the paper.

The model has a game form. An accepting subtree is a winning strategy for an existential player in a game. The existential player chooses the move at an existential configuration, and the universal player chooses it at a universal configuration. The existential player wins if the play reaches accept. With plays of polynomial length, deciding who wins is PSPACE-complete, and the evaluation of quantified Boolean formulas is the standard example.

The model does not add power in the sense of computability. A language that an alternating machine recognizes is recursively enumerable, because a deterministic machine can search for a finite accepting subtree, level by level. So alternation changes the cost of a computation and not what is computable. For time, the gain is large: polynomial time on the alternating machine is polynomial space on the deterministic one.

## Known results in the model

**Theorem 1.** $\mathrm{AP} = \mathrm{PSPACE}$.

*Proof of $\mathrm{AP} \subseteq \mathrm{PSPACE}$.* Let $M$ decide $L$ in time $p(n)$, where $p$ is a polynomial. A deterministic machine evaluates the tree depth-first. The procedure EVAL$(C)$ returns true if $C$ is accepting, false if $C$ has state reject, and otherwise it calls EVAL on the successors of $C$ one after the other. At an existential configuration it returns true as soon as one call returns true, and false if none does. At a universal configuration it returns false as soon as one call returns false, and true if none does. By induction on the height of the finite subtree below $C$, EVAL$(C)$ is true if and only if $C \in \mathcal{A}_w$. The recursion is at most $p(n) + 1$ calls deep. A configuration on a path has at most $n + p(n) + 1$ cells, and each call keeps its configuration and the index of the next successor. So the space is $O(p(n)(n + p(n)))$, a polynomial. $\square$

*Proof of $\mathrm{PSPACE} \subseteq \mathrm{AP}$.* Let a deterministic machine $D$ decide $L$ in space $s(n) \ge n$, where $s$ is a polynomial. Since $s$ is a polynomial, $M$ computes $s(n)$ and $J$ (defined below) deterministically in polynomial time before it starts. $D$ halts on every input, and a computation does not repeat a configuration. The number of configurations is at most $|Q|\,(s(n)+1)\,|\Gamma|^{s(n)}$, so there is a constant $c$ such that $D$ halts within $2^{c\,s(n)}$ steps. Write $J = c\,s(n)$. Let REACH$(C, C', j)$ mean that $C'$ follows from $C$ in at most $2^j$ steps of $D$. The alternating machine $M$ works as follows on $w$.

1. In existential states, $M$ writes a configuration $C_{acc}$ with state accept, symbol by symbol.
2. $M$ checks REACH$(q_0\,w, C_{acc}, J)$ by the recursion below.
3. For $j = 0$, $M$ checks $C = C'$ or $C \vdash_D C'$ in $O(s(n))$ steps and accepts if the check succeeds.
4. For $j > 0$, $M$ writes a configuration $C''$ in existential states. Then in a universal state it picks one of two branches. One branch checks REACH$(C, C'', j-1)$, and the other checks REACH$(C'', C', j-1)$.

By induction on $j$, a branch of the recursion accepts if and only if REACH$(C, C', j)$ holds. The recursion has $J + 1$ levels, and each level takes $O(s(n))$ steps to write and copy configurations. So $M$ runs in time $O(s(n)^2)$, which is a polynomial. It accepts $w$ if and only if some accepting configuration is reachable from $q_0\,w$, that is, if and only if $D$ accepts $w$. $\square$

**Theorem 2.** $\mathrm{APSPACE} = \mathrm{EXP}$, where $\mathrm{EXP} = \bigcup_{k \ge 1} \mathrm{DTIME}(2^{n^k})$.

*Proof of $\mathrm{APSPACE} \subseteq \mathrm{EXP}$.* Let $M$ decide $L$ in space $s(n)$, a polynomial. The configurations that are reachable from the start have at most $s(n)$ cells, so there are at most $N \le |Q|\,(s(n)+1)\,|\Gamma|^{s(n)} = 2^{O(s(n))}$ of them. A deterministic machine builds the graph of these configurations. It then computes $\mathcal{A}_w$ by iteration: begin with the accepting configurations, and in each round add each existential configuration with a successor in the set and each universal configuration whose successors are all in the set. The set grows in each round that changes it, so there are at most $N$ rounds, and each round takes time polynomial in $N$. The result is the least set with the three properties. The total time is $N^{O(1)} = 2^{O(s(n))}$, which is exponential in a polynomial. $\square$

*Proof of $\mathrm{EXP} \subseteq \mathrm{APSPACE}$ (outline).* Let a deterministic multitape machine decide $L$ in time $2^{p'(n)}$. A one-tape machine simulates it in time $O(2^{2p'(n)})$ by the [multitape simulation theorem](/multitape-simulation-theorem/), which is again of the form $2^{\mathrm{poly}(n)}$. So let a one-tape deterministic machine $D$ decide $L$ in time $T = 2^{p(n)}$. Let it stay in its halting state once it halts. Consider the table in which entry $(t, x)$ is the content of cell $x$ at time $t$, together with the state if the head is on the cell. The entry $(t, x)$ is a fixed function of the three entries $(t-1, x-1)$, $(t-1, x)$, $(t-1, x+1)$, with a small change at $x = 0$ for the left-end rule. The row $t = 0$ is given by the input. The alternating machine $M$ checks VAL$(t, x, a)$, "entry $(t, x)$ is $a$", as follows. For $t = 0$, it moves the input head to cell $x$ and compares. For $t > 0$, it guesses in existential states three entries $a_{-1}, a_0, a_1$ for which the fixed function gives $a$. Then it chooses in a universal state one of the three claims VAL$(t-1, x+d, a_d)$ and checks it. At the start, $M$ guesses a cell $x$ and an entry $a$ with the state accept, and checks VAL$(T, x, a)$. The numbers $t$ and $x$ are written in binary with $p(n) + 1$ bits, so the space is $O(p(n))$. By induction on $t$, VAL$(t, x, a)$ accepts if and only if the entry is $a$, since the entries of the table are unique. So $M$ accepts $w$ if and only if $D$ accepts $w$. $\square$

More results, the first three from the paper of Chandra, Kozen and Stockmeyer:

- **Logarithmic space.** $\mathrm{AL} = \mathrm{P}$. In general $\mathrm{ASPACE}(s(n)) = \bigcup_{c} \mathrm{DTIME}(c^{s(n)})$ for $s(n) \ge \log n$.
- **Time and space.** For $t(n) \ge n$, $\mathrm{ATIME}(t(n)) \subseteq \mathrm{DSPACE}(t(n))$ and $\mathrm{DSPACE}(t(n)) \subseteq \mathrm{ATIME}(t(n)^2)$. Theorem 1 is the polynomial case.
- **The hierarchy.** A language is in $\Sigma_k^p$ if and only if a polynomial-time alternating machine of type $\Sigma_k$ decides it, for each $k \ge 1$.
- **Complete problem.** Evaluation of [quantified Boolean formulas](/qbf/) is PSPACE-complete (Stockmeyer and Meyer, 1973), so a polynomial-time alternating machine decides it, as the example above shows.
- **Circuits.** Ruzzo (1981) showed that alternating machines with logarithmic time and random access to the input characterize uniform $\mathrm{NC}^1$.

## References
