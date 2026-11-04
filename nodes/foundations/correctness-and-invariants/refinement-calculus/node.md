---
tag: 3DNMQJ
kind: concept
slug: refinement-calculus
name: Refinement calculus
aliases:
- Stepwise refinement calculus
area: foundations/correctness-and-invariants
level: research
summary: A method for deriving a correct implementation from an abstract specification by stepwise refinement.
prereqs: [weakest-precondition, guarded-commands, specification]
see_also: [hoare-logic, program-verification, total-correctness, loop-invariant, variant-function, integer-square-root]
sources:
  - book: isbn:9780131232747
    title: Carroll Morgan, Programming from Specifications, second edition, Prentice Hall (1994)
    locator: Chapter 1 (the specification statement, Laws 1.1 to 1.3, Section 1.7 on infeasible programs), Chapter 3 (Law 3.3, sequential composition), Chapter 4 (Law 4.1, alternation), Chapter 5 (Law 5.5, iteration), Chapter 7 (case study, square root)
  - url: "https://www.cs.ox.ac.uk/publications/books/PfS/"
    locator: Morgan, Programming from Specifications, the free web edition of the second edition
  - paper: doi:10.1145/44501.44503
    title: Carroll Morgan, The specification statement, ACM Transactions on Programming Languages and Systems 10(3) (1988)
    locator: pp. 403 to 419
  - paper: doi:10.1016/0167-6423(87)90011-6
    title: Joseph M. Morris, A theoretical basis for stepwise refinement and the programming calculus, Science of Computer Programming 9(3) (1987)
    locator: pp. 287 to 306
  - paper: "R. J. R. Back, On the correctness of refinement steps in program development, PhD thesis, Department of Computer Science, University of Helsinki (1978), Report A-1978-4"
    locator: the whole thesis
  - book: isbn:9780387984179
    title: Ralph-Johan Back and Joakim von Wright, Refinement Calculus, A Systematic Introduction, Springer (1998)
    locator: Part II (Statements), Chapters 11 (Predicate Transformers) and 12 (The Refinement Calculus Hierarchy); Part III (Recursion and Iteration)
  - paper: doi:10.1145/362575.362577
    title: Niklaus Wirth, Program development by stepwise refinement, Communications of the ACM 14(4) (1971)
    locator: pp. 221 to 227
---

The refinement calculus is a method to derive a program from its [specification](/specification/) by a chain of small steps, each of which keeps the program correct. A specification is itself a command, the specification statement $w:[\mathit{pre}, \mathit{post}]$, and a step replaces a command by one that is *at least as good*. The meaning of a command is its [weakest precondition](/weakest-precondition/) transformer, and "at least as good" has an exact definition in these terms. Laws of refinement turn a specification into code, and the [loop invariants](/loop-invariant/) appear during the derivation.

## In plain words

Most verification starts with a finished program and asks if it is correct. The refinement calculus goes the other way. You start with a statement of what you want, written as a command that the computer cannot yet run. Then you improve it in steps. Each step replaces a part by a part that is more concrete and promises at least as much. The last step gives code that runs.

A step is allowed only if a law says so. A law has a small side condition, which is a fact of logic that you must show. If all steps obey the laws, the final program meets the first specification, and you need no second proof of the whole program.

You do not guess the loop invariant after the code is written. It appears during the derivation.

## The idea

**History.** The idea of stepwise refinement comes from Wirth (1971). Back (1978) gave it a formal basis in weakest preconditions. Morris (1987) and Morgan (1988, "The specification statement") developed the calculus further, and Morgan's book (1990, second edition 1994) made it widely known. Back and von Wright (1998) give the lattice theory of the calculus.

**States and commands.** As in the page on [weakest preconditions](/weakest-precondition/), a state gives a value to each variable, and a predicate is a condition on states. A command $C$ has a predicate transformer $R \mapsto \mathrm{wp}(C, R)$, the set of states from which $C$ is sure to stop in a state that satisfies $R$. Commands can be nondeterministic.

**The specification statement.** Let $w$ be a list of variables (the *frame*), and let $\mathit{pre}$ and $\mathit{post}$ be predicates. Informally, the command $w:[\mathit{pre}, \mathit{post}]$ means: if $\mathit{pre}$ holds, change only the variables of $w$ so that $\mathit{post}$ holds at the end, else do anything. In this page $\mathit{post}$ does not mention the initial values of the variables. (Morgan writes $w_0$ for the initial value of $w$ and treats it with more general laws, in his Chapter 5 and Chapter 8.) The exact meaning is

$$ \mathrm{wp}(w:[\mathit{pre}, \mathit{post}], R) \;=\; \mathit{pre} \;\wedge\; \forall w' \cdot \bigl(\mathit{post}[w'/w] \implies R[w'/w]\bigr), $$

where $w'$ is a list of fresh variables. Variables outside $w$ keep their values. In words: $\mathit{pre}$ must hold, and each state that $\mathit{post}$ allows must satisfy $R$. Three special cases show the range of the construct.

- $w:[\mathit{false}, \mathit{true}]$ has $\mathrm{wp} = \mathit{false}$ for each $R$. This is $\mathbf{abort}$, the command that guarantees nothing.
- $w:[\mathit{true}, \mathit{false}]$ has $\mathrm{wp} = \mathit{true}$ for each $R$. This is the *miracle* $\mathbf{magic}$, which meets each postcondition. No machine can run it, and it is the best command in the order below.
- The command $\mathbf{skip}$ has $\mathrm{wp}(\mathbf{skip}, R) = R$, and it is the statement with an empty frame and with $\mathit{pre}$ and $\mathit{post}$ equal to $\mathit{true}$.

**Feasibility.** The informal reading "change $w$ so that $\mathit{post}$ holds" hides one case: there may be no such values. The statement $w:[\mathit{pre}, \mathit{post}]$ is *feasible* when

$$ \mathit{pre} \implies \exists w' \cdot \mathit{post}[w'/w] $$

is valid. By the formula above, $\mathrm{wp}(w:[\mathit{pre}, \mathit{post}], \mathit{false}) = \mathit{pre} \wedge \forall w' \cdot \neg \mathit{post}[w'/w]$, so the statement is feasible exactly when this predicate is $\mathit{false}$ in every state. In a state where it is true, the statement acts as $\mathbf{magic}$. Code never acts as magic: each command $C$ of the programming language has $\mathrm{wp}(C, \mathit{false}) = \mathit{false}$. If code $C$ refined an infeasible statement, then $\mathrm{wp}(C, \mathit{false})$ would be true in some state, which is impossible. So only feasible statements refine to code (Morgan, Section 1.7).

**Refinement.** The command $P$ is *refined by* $Q$, written $P \sqsubseteq Q$, when

$$ P \sqsubseteq Q \iff \forall R : \ \mathrm{wp}(P, R) \implies \mathrm{wp}(Q, R), $$

where $R$ ranges over all predicates and "$\implies$" holds in each state. If $P$ guarantees $R$ from a state, then $Q$ guarantees $R$ from that state. Every use that $P$ allows is also safe with $Q$. So $Q$ can replace $P$ in each program, and the new program meets every total-correctness triple that the old one met. The relation is reflexive and transitive, because implication is. In this order $\mathbf{abort}$ is refined by each command, and each command is refined by $\mathbf{magic}$. Refinement is monotone: if $Q$ refines $P$, a program that uses $Q$ in place of $P$ refines the program that uses $P$ (Morgan 1990, Back and von Wright 1998).

**Laws.** Each law below gives a refinement $\sqsubseteq$ under a condition. Here $\mathit{pre}$, $\mathit{post}$ and the other predicates do not mention initial values. Write $X(R)$ for $\forall w' \cdot (\mathit{post}[w'/w] \implies R[w'/w])$, so that $\mathrm{wp}(w:[\mathit{pre}, \mathit{post}], R) = \mathit{pre} \wedge X(R)$. The numbers in parentheses are those of Morgan's book.

1. *Strengthen the postcondition* (Law 1.1). If $\mathit{post}' \implies \mathit{post}$ is valid, then $w:[\mathit{pre}, \mathit{post}] \sqsubseteq w:[\mathit{pre}, \mathit{post}']$.
2. *Weaken the precondition* (Law 1.2). If $\mathit{pre} \implies \mathit{pre}'$ is valid, then $w:[\mathit{pre}, \mathit{post}] \sqsubseteq w:[\mathit{pre}', \mathit{post}]$.
3. *Assignment* (Law 1.3). If $\mathit{pre} \implies \mathit{post}[E/x]$ is valid, then $w, x:[\mathit{pre}, \mathit{post}] \sqsubseteq x \leftarrow E$.
4. *Skip* (Law 3.2). If $\mathit{pre} \implies \mathit{post}$ is valid, then $w:[\mathit{pre}, \mathit{post}] \sqsubseteq \mathbf{skip}$.
5. *Sequence* (Law 3.3). For each predicate $\mathit{mid}$, $w:[\mathit{pre}, \mathit{post}] \sqsubseteq w:[\mathit{pre}, \mathit{mid}] \,;\, w:[\mathit{mid}, \mathit{post}]$.
6. *Alternation* (Law 4.1). If $\mathit{pre} \implies g_1 \vee \cdots \vee g_n$ is valid, then $w:[\mathit{pre}, \mathit{post}]$ is refined by the [guarded-command](/guarded-commands/) alternation $\mathbf{if}\ g_1 \to w:[g_1 \wedge \mathit{pre}, \mathit{post}] \mathbin{[\,]} \cdots \mathbin{[\,]} g_n \to w:[g_n \wedge \mathit{pre}, \mathit{post}]\ \mathbf{fi}$.
7. *Iteration* (Law 5.5). Let $\mathit{inv}$ be a predicate, $G$ a guard, and $V$ an integer expression, the [variant](/variant-function/). Let $c$ be a fresh variable, not in $w$ and not free in $\mathit{inv}$, $G$ or $V$. If $w:[\mathit{inv} \wedge G \wedge V = c,\ \mathit{inv} \wedge 0 \le V < c] \sqsubseteq S$ for each integer value of $c$, then
$$ w:[\mathit{inv},\ \mathit{inv} \wedge \neg G] \;\sqsubseteq\; \mathbf{do}\ G \to S\ \mathbf{od}. $$
Morgan writes the body as $w:[\mathit{inv} \wedge G,\ \mathit{inv} \wedge 0 \le V < V_0]$, where $V_0$ is the value of $V$ at the start of the body. With several guards, $G$ is their disjunction.

Law 1 needs care: it can turn a feasible statement into an infeasible one. With $\mathit{post}' = \mathit{false}$ it gives $w:[\mathit{pre}, \mathit{post}] \sqsubseteq w:[\mathit{pre}, \mathit{false}]$, which is $\mathbf{magic}$ where $\mathit{pre}$ holds. That step is a correct refinement, and it leads nowhere.

**Proofs of the laws.** Each proof starts with $\mathrm{wp}$ of the left side and shows that it implies $\mathrm{wp}$ of the right side, for each $R$.

1. Let $X'(R)$ be $X(R)$ for $\mathit{post}'$. A state $w'$ that satisfies $\mathit{post}'$ satisfies $\mathit{post}$, and then it satisfies $R$ when $X(R)$ holds. So $X(R) \implies X'(R)$, and $\mathit{pre} \wedge X(R) \implies \mathit{pre} \wedge X'(R)$.
2. $\mathit{pre} \wedge X(R) \implies \mathit{pre}' \wedge X(R)$ because $\mathit{pre} \implies \mathit{pre}'$.
3. $\mathrm{wp}(x \leftarrow E, R) = R[E/x]$. Assume $\mathit{pre}$ and $X(R)$. Take $x' := E$ and $w' := w$ in $X(R)$: this gives $\mathit{post}[E/x] \implies R[E/x]$. By the assumption on the law, $\mathit{post}[E/x]$ holds, so $R[E/x]$ holds.
4. $\mathrm{wp}(\mathbf{skip}, R) = R$. Take $w' := w$ in $X(R)$: this gives $\mathit{post} \implies R$. With $\mathit{pre} \implies \mathit{post}$ we get $R$.
5. Let $A = w:[\mathit{pre}, \mathit{mid}]$ and $B = w:[\mathit{mid}, \mathit{post}]$. Then $\mathrm{wp}(B, R) = \mathit{mid} \wedge X(R)$, and $\mathrm{wp}(A, \mathrm{wp}(B, R)) = \mathit{pre} \wedge \forall w' \cdot \bigl(\mathit{mid}[w'/w] \implies (\mathit{mid}[w'/w] \wedge X(R))\bigr)$. Here $X(R)$ has no free $w$ because $w$ is bound in it, so it is the same for each $w'$. This formula follows from $\mathit{pre} \wedge X(R)$.
6. Let $S_i = w:[g_i \wedge \mathit{pre}, \mathit{post}]$, so $\mathrm{wp}(S_i, R) = g_i \wedge \mathit{pre} \wedge X(R)$. By the rule for alternation in the page on weakest preconditions, the right side has $\mathrm{wp} = (g_1 \vee \cdots \vee g_n) \wedge \bigwedge_i \bigl(g_i \implies (g_i \wedge \mathit{pre} \wedge X(R))\bigr)$. Assume $\mathit{pre} \wedge X(R)$. Then each implication holds, and $g_1 \vee \cdots \vee g_n$ holds by the condition of the law.
7. Fix $R$. Here $X(R) = \forall w' \cdot \bigl((\mathit{inv} \wedge \neg G)[w'/w] \implies R[w'/w]\bigr)$, and let $J = \mathit{inv} \wedge X(R)$, the $\mathrm{wp}$ of the left side. Write $\mathrm{DO}$ for the loop. The page on weakest preconditions gives, for commands with bounded nondeterminism, $\mathrm{wp}(\mathrm{DO}, R) = \exists k \cdot H_k$ with $H_0 = \neg G \wedge R$ and $H_{k+1} = H_0 \vee (G \wedge \mathrm{wp}(S, H_k))$. *Step (a).* Let $Q_c = J \wedge 0 \le V < c$. Since $X(R)$ has no free $w$, the formula $\forall w' \cdot ((\mathit{inv} \wedge 0 \le V < c)[w'/w] \implies Q_c[w'/w])$ follows from $X(R)$. So $J \wedge G \wedge V = c$ implies $\mathrm{wp}(w:[\mathit{inv} \wedge G \wedge V = c,\ \mathit{inv} \wedge 0 \le V < c], Q_c)$, and by the condition of the law it implies $\mathrm{wp}(S, Q_c)$. *Step (b).* By induction on $k \ge 0$: $J \wedge (\neg G \vee V < k) \implies H_{k+1}$. If $\neg G$ holds, take $w' := w$ in $X(R)$: $\mathit{inv} \wedge \neg G$ gives $R$, so $H_0$ holds, and $H_0$ implies $H_{k+1}$. Otherwise $G$ holds and $V = c$ for some $c < k$. By (a), $\mathrm{wp}(S, Q_c)$ holds. If $k = 0$, then $c < 0$, so $Q_c$ is $\mathit{false}$, and $\mathrm{wp}(S, \mathit{false})$ implies $\mathrm{wp}(S, H_0)$ by monotonicity; this gives $H_1$. If $k \ge 1$, then $Q_c$ implies $J \wedge V < k - 1$, which implies $H_k$ by the induction hypothesis, so $\mathrm{wp}(S, H_k)$ holds, and with $G$ this gives $H_{k+1}$. *Conclusion.* In each state $V$ has some value $c$, and $V < k$ for $k = \max(c + 1, 0)$. So $J$ implies some $H_{k+1}$, hence $\mathrm{wp}(\mathrm{DO}, R)$. The bound $0 \le V$ in the body is used only in the case $k = 0$, and without it the loop may run forever.

**Pitfalls.**

- *Infeasible steps.* Law 1 is valid for each stronger postcondition, also for one that no value meets. Check feasibility after each use of law 1.
- *The frame.* A variable outside the frame must not change. The code $t \leftarrow a\ ;\ m \leftarrow t$ does not refine $m:[\mathit{true}, m = a]$ when $t$ is a program variable, because it changes $t$. A helper variable needs a local declaration (Morgan, Chapter 6).
- *Refinement goes one way.* A step can lose freedom that a later step needs. Law 1 allows $m:[\mathit{true}, m \ge a \wedge m \ge b] \sqsubseteq m:[\mathit{true}, m = |a| + |b|]$. After this step no later step can give the smaller result $\max(a, b)$: for $a = b = 1$ the new statement forces $m = 2$.
- *Initial values.* A postcondition such as $x > x_0$ needs the laws of Morgan's Chapter 5 and Chapter 8. The laws on this page assume that $\mathit{post}$ mentions no initial value.

## Examples

**A derivation: the larger of two numbers.** Let $a$ and $b$ be integers that the program does not change, and let $m$ be the result. The first specification is weak: it allows any $m$ that is at least both.

$$ S_0 = m:[\mathit{true},\ m \ge a \wedge m \ge b]. $$

The derivation has three steps. Its result is a chain $S_0 \sqsubseteq S_1 \sqsubseteq S_2 \sqsubseteq S_3$.

1. *Strengthen the postcondition* (law 1). The predicate $m = \max(a, b)$ implies $m \ge a \wedge m \ge b$, so $S_0 \sqsubseteq S_1 = m:[\mathit{true},\ m = \max(a, b)]$. Law 1 could also lose feasibility here, so check it: $\exists m \cdot m = \max(a, b)$ is true, so $S_1$ is feasible. The stronger postcondition $m \ge a \wedge m \ge b \wedge m < a$ would also be allowed by law 1, but it is infeasible.
2. *Alternation* (law 6). The condition $\mathit{true} \implies a \ge b \vee b \ge a$ is valid, so
$$ S_1 \sqsubseteq S_2 = \mathbf{if}\ a \ge b \to m:[a \ge b,\ m = \max(a, b)] \mathbin{[\,]} b \ge a \to m:[b \ge a,\ m = \max(a, b)]\ \mathbf{fi}. $$
3. *Assignment* (law 3, with the monotonicity of refinement for each branch). The condition $a \ge b \implies a = \max(a, b)$ is valid, and so is $b \ge a \implies b = \max(a, b)$. So
$$ S_2 \sqsubseteq S_3 = \mathbf{if}\ a \ge b \to m \leftarrow a \mathbin{[\,]} b \ge a \to m \leftarrow b\ \mathbf{fi}. $$

The program $S_3$ runs, and by transitivity $S_0 \sqsubseteq S_3$. When $a = b$ both guards are true, and both branches give the same $m$.

**A derivation with a loop: the integer square root.** Let $N$ be an integer that the program does not change, and let $r$ be the result. The specification asks for the [integer square root](/integer-square-root/):

$$ T_0 = r:[0 \le N,\ r^2 \le N < (r + 1)^2]. $$

The invariant comes from the postcondition. Keep its first conjunct, add the bound $0 \le r$, and let the negation of the second conjunct be the guard:

$$ \mathit{inv} \equiv 0 \le r \wedge r^2 \le N, \qquad G \equiv (r + 1)^2 \le N, \qquad V \equiv N - r^2. $$

1. *Sequence* (law 5) with $\mathit{mid} = \mathit{inv}$: $T_0 \sqsubseteq r:[0 \le N, \mathit{inv}]\ ;\ r:[\mathit{inv},\ r^2 \le N < (r+1)^2]$.
2. *Assignment* (law 3) for the first part: $0 \le N \implies \mathit{inv}[0/r]$, which is $0 \le 0 \wedge 0 \le N$. So the first part is refined by $r \leftarrow 0$.
3. *Strengthen the postcondition* (law 1) for the second part: $\mathit{inv} \wedge \neg G$ is $0 \le r \wedge r^2 \le N \wedge N < (r+1)^2$, which implies the postcondition. So the second part is refined by $r:[\mathit{inv},\ \mathit{inv} \wedge \neg G]$. It is feasible, since for $N \ge 0$ the value $\lfloor \sqrt{N} \rfloor$ meets it.
4. *Iteration* (law 7) with the body $r \leftarrow r + 1$. By law 3 the condition of law 7 is $\mathit{inv} \wedge G \wedge V = c \implies (\mathit{inv} \wedge 0 \le V < c)[r + 1/r]$. Check each part. $0 \le r + 1$ follows from $0 \le r$. $(r+1)^2 \le N$ is $G$. $0 \le N - (r+1)^2$ is again $G$. And $N - (r + 1)^2 < N - r^2 = c$ because $(r + 1)^2 - r^2 = 2r + 1 > 0$ for $r \ge 0$.

The result is the program

$$ r \leftarrow 0\ ;\ \mathbf{do}\ (r + 1)^2 \le N \to r \leftarrow r + 1\ \mathbf{od}. $$

For $N = 10$ the loop gives $r = 0, 1, 2, 3$ with variant values $10, 9, 6, 1$, and it stops because $(3 + 1)^2 = 16 > 10$. The result $r = 3$ satisfies $9 \le 10 < 16$. The loop runs $\lfloor \sqrt{N} \rfloor$ times. Morgan's Chapter 7 starts from the same kind of specification and chooses another invariant with two bounds, which gives a faster program by bisection.

**The order is strict.** The step $S_0 \sqsubseteq S_1$ is not an equivalence. Take the state with $a = b = 0$ and $R$ equal to $m = 0$. Then $\mathrm{wp}(S_1, R) = \mathit{true}$ in this state, but $\mathrm{wp}(S_0, R)$ is false: $S_0$ may end with $m = 1$. So $S_1 \not\sqsubseteq S_0$.

**A non-example: a step that is not a refinement.** The command $m \leftarrow a$ does not refine $S_1$. The assignment law needs $\mathit{true} \implies a = \max(a, b)$, which fails for $a = 0$, $b = 1$. Indeed $\mathrm{wp}(m \leftarrow a,\ m = \max(a, b)) = (a = \max(a, b))$, and with $R$ equal to $m = \max(a, b)$ we have $\mathrm{wp}(S_1, R) = \mathit{true}$, which does not imply it.

## Where it is used

- Program derivation. Morgan's book derives many small programs from their specifications, among them a square root, insertion sort and heap sort. The loop invariants come out of the derivation, as in the square root example above.
- The theory of data refinement and abstraction: a change of representation is a refinement between commands with different state spaces (see [abstraction function](/abstraction-function/)). Morgan's Chapter 17 treats it.
- The lattice theory of programs: Back and von Wright (1998) study commands as monotone predicate transformers, ordered by refinement.
- The semantic base for checking a refinement step instead of a whole program, as in [program verification](/program-verification/).

## References
