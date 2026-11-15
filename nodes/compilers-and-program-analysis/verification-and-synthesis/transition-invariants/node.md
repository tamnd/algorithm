---
tag: D0628W
kind: theorem
slug: transition-invariants
name: Transition invariant theorem
aliases:
- disjunctive well-foundedness
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: A program terminates iff its transition relation has a transition invariant that is a finite union of well-founded relations.
prereqs: [well-founded-relation, ramsey-theorem, termination-proof]
see_also: [ranking-function-synthesis, size-change-termination, lexicographic-order, variant-function, liveness-property, safety-property, halting-problem, total-correctness]
sources:
  - paper: doi:10.1109/LICS.2004.1319598
    title: Andreas Podelski and Andrey Rybalchenko, Transition invariants, Proceedings of the 19th IEEE Symposium on Logic in Computer Science (LICS 2004)
    locator: the definitions of transition invariant and disjunctive well-foundedness, and the theorem that a program terminates if and only if it has a disjunctively well-founded transition invariant, proved with Ramsey's theorem
  - paper: doi:10.1145/1133981.1134029
    title: Byron Cook, Andreas Podelski and Andrey Rybalchenko, Termination proofs for systems code, Proceedings of PLDI 2006
    locator: the Terminator tool, which builds a disjunctively well-founded transition invariant one ranking function at a time and checks it as a safety property
  - paper: doi:10.1145/360204.360210
    title: Chin Soon Lee, Neil D. Jones and Amir M. Ben-Amram, The size-change principle for program termination, Proceedings of POPL 2001
    locator: pp. 81 to 92, the earlier use of Ramsey's theorem to prove termination from the idempotent size-change graphs of the closure
  - paper: doi:10.1112/plms/s2-30.1.264
    title: F. P. Ramsey, On a problem of formal logic, Proceedings of the London Mathematical Society s2-30(1), 264 to 286 (1930)
    locator: the infinite form of the theorem on colorings of the r-subsets of an infinite set
---

The transition invariant theorem of Podelski and Rybalchenko says that a program terminates if and only if the transitive closure of its step relation, on reachable states, is contained in a finite union of [well-founded relations](/well-founded-relation/). Each relation in the union can be proved well-founded alone, often with one linear [ranking function](/ranking-function-synthesis/), and no single order for the whole program is needed. The "if" direction rests on the infinite form of [Ramsey's theorem](/ramsey-theorem/). The theorem is the basis of the Terminator tool and of many automatic [termination provers](/termination-proof/).

## Statement

**Programs.** A program is a set of states $S$, a set of initial states $I \subseteq S$ and a transition relation $R \subseteq S \times S$. A *computation* is a finite or infinite sequence $s_0, s_1, \ldots$ with $s_0 \in I$ and $(s_j, s_{j+1}) \in R$ for each step. A state is *reachable* if it occurs in a computation; $\mathrm{Acc}$ is the set of reachable states. The program *terminates* if it has no infinite computation.

**Relations.** A relation $T \subseteq S \times S$ is *well-founded* if there is no infinite sequence $x_0, x_1, x_2, \ldots$ with $(x_j, x_{j+1}) \in T$ for all $j$. $T$ is *disjunctively well-founded* if $T = T_1 \cup \cdots \cup T_k$ for some finite $k$ and well-founded $T_1, \ldots, T_k$. $R^+$ is the transitive closure of $R$: the pairs $(s, s')$ such that $s'$ is reached from $s$ in one or more steps.

**Transition invariant.** $T$ is a *transition invariant* of the program if $R^+ \cap (\mathrm{Acc} \times S) \subseteq T$, that is, if $(s, s') \in T$ whenever $s$ is reachable and $s'$ is reached from $s$ in at least one step.

**Theorem.** A program terminates if and only if it has a disjunctively well-founded transition invariant.

## In plain words

To show that a loop stops, the classic way is one measure that drops on every step and cannot drop for ever. For a program with many paths, one such measure can be hard to find. This theorem says that you can use several simple measures instead. The condition is: for any two moments of a run, an earlier one and a later one, at least one of the measures has dropped between them. If each measure cannot drop for ever, the run must stop. The important detail is "any two moments", not only "two moments next to each other". With only next steps, two measures can take turns going down and up, and the run never stops.

## Proof

**Lemma (infinite Ramsey for pairs).** Color every pair $\{i, j\}$ of natural numbers, $i < j$, with one of $k$ colors. Then there is an infinite set $H \subseteq \mathbb{N}$ and a color $m$ such that every pair of $H$ has color $m$.

*Proof of the lemma.* Put $A_0 = \mathbb{N}$. Given an infinite set $A_t$, let $a_t = \min A_t$. The infinitely many $x \in A_t \setminus \{a_t\}$ fall into $k$ classes by the color of $\{a_t, x\}$, so one class is infinite, by the [pigeonhole principle](/pigeonhole-principle/). Let $A_{t+1}$ be that class and $c_t$ its color. Then $a_0 < a_1 < \cdots$, since $A_{t+1} \subseteq A_t \setminus \{a_t\}$ and $a_t$ is the least element of $A_t$, and for $t < u$ the element $a_u$ lies in $A_{t+1}$, so $\{a_t, a_u\}$ has color $c_t$. The colors $c_0, c_1, \ldots$ take only $k$ values, so some color $m$ equals $c_t$ for infinitely many $t$, say $t_0 < t_1 < \cdots$. Put $H = \{a_{t_0}, a_{t_1}, \ldots\}$. For $p < q$, the pair $\{a_{t_p}, a_{t_q}\}$ has color $c_{t_p} = m$. $\square$

*If.* Let $T = T_1 \cup \cdots \cup T_k$ be a disjunctively well-founded transition invariant, and suppose that $s_0, s_1, \ldots$ is an infinite computation. For $i < j$, $s_i$ is reachable and $s_j$ is reached from $s_i$ in $j - i \ge 1$ steps, so $(s_i, s_j) \in R^+ \cap (\mathrm{Acc} \times S) \subseteq T$. Color the pair $\{i, j\}$ with the least $m$ such that $(s_i, s_j) \in T_m$. By the lemma there are indices $h_0 < h_1 < h_2 < \cdots$ whose pairs all have the same color $m$. In particular $(s_{h_l}, s_{h_{l+1}}) \in T_m$ for every $l$, so $s_{h_0}, s_{h_1}, \ldots$ is an infinite descending sequence of $T_m$. This contradicts the well-foundedness of $T_m$. So there is no infinite computation.

*Only if.* Suppose the program terminates. Take $k = 1$ and $T_1 = R^+ \cap (\mathrm{Acc} \times S)$. It is a transition invariant by definition. Suppose it is not well-founded, with an infinite sequence $x_0, x_1, \ldots$ and $(x_j, x_{j+1}) \in T_1$. Then $x_0$ is reachable, so a computation $s_0, \ldots, s_r = x_0$ reaches it. Each pair $(x_j, x_{j+1})$ is in $R^+$, so a path of one or more $R$ steps leads from $x_j$ to $x_{j+1}$. Join the computation to $x_0$ and all these paths. The result is an infinite computation, since every path adds at least one step. This contradicts termination. $\blacksquare$

## Consequences

- **Termination proofs by parts.** To prove termination it is enough to cover $R^+$ by finitely many relations and give each a ranking function. Terminator by Cook, Podelski and Rybalchenko does this: it guesses $T$, asks a model checker for a pair in $R^+$ that is not covered, synthesizes a ranking function for the loop path of that pair with [linear ranking function synthesis](/ranking-function-synthesis/), adds it to $T$, and repeats.
- **The check is a safety property.** "$T$ is a transition invariant" is a [safety property](/safety-property/) of a program that runs $P$, at some point saves a copy of the current state, and keeps running; the assertion is that the pair (saved state, current state) is in $T$. So termination, a [liveness property](/liveness-property/), is reduced to one safety check plus $k$ separate well-foundedness checks.
- **No lexicographic order needed.** A [lexicographic](/lexicographic-order/) ranking function asks for a fixed priority among the measures. A disjunctive one needs none, so it is easier to find and to compose. The price is that the inductive check must be about $R^+$, not about $R$.
- **The same argument as size-change termination.** [Size-change termination](/size-change-termination/) by Lee, Jones and Ben-Amram uses Ramsey's theorem in the same way, on the size-change graphs of the closure.
- **No decision procedure.** Termination is undecidable, by the [halting problem](/halting-problem/) and [Rice's theorem](/rice-theorem/). The theorem does not change that: it says what a proof looks like, not how to find one. Tools search for $T$ in a restricted class, such as unions of linear ranking relations, and can fail.

## Tightness

- **$R$ instead of $R^+$ is not enough.** Take $S = I = \{a, b\}$ and $R = \{(a, b), (b, a)\}$. Then $R = \{(a, b)\} \cup \{(b, a)\}$ is a union of two well-founded relations, each with one pair, but $a, b, a, b, \ldots$ is an infinite computation. The closure $R^+$ contains $(a, a)$, and no well-founded relation contains a pair $(a, a)$, so no disjunctively well-founded $T$ covers $R^+$. A union of well-founded relations is not well-founded in general, and the theorem uses the closure exactly to get around this.
- **The union must be finite.** Take $S = I = \mathbb{N}$ and $R = \{(x, x + 1)\}$. The program does not terminate. But $R^+ = \{(x, y) : x < y\}$ is the union of the infinitely many one-pair relations $\{(x, y)\}$, and each is well-founded. The proof needs $k$ finite to apply Ramsey's theorem with $k$ colors.
- **The restriction to reachable states is needed for "only if".** Add to a terminating program a state $c \notin I$ with $(c, c) \in R$ that no computation reaches. The program still terminates, but $R^+$ contains $(c, c)$, so without the restriction to $\mathrm{Acc} \times S$ no disjunctively well-founded relation would cover it.
- **The proof is not constructive.** The "if" direction uses the infinite Ramsey theorem and gives no bound on the length of a run in terms of the $k$ ranking functions, unlike one ranking function, which bounds the run by its starting value.

## History

Floyd proved termination in 1967 with a function into a well-founded set, which is one relation that covers $R$. Lee, Jones and Ben-Amram used Ramsey's theorem in 2001 to prove the size-change termination principle. Podelski and Rybalchenko defined transition invariants and proved this theorem at LICS 2004, and gave the linear ranking function synthesis that it uses in the same year. Cook, Podelski and Rybalchenko built Terminator on it and reported termination proofs of Windows device drivers at PLDI 2006. Ramsey's theorem is from 1930.

## References
