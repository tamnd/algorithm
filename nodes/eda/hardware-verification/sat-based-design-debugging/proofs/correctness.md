---
title: The debug instance is satisfiable exactly when the selected gates can fix the tests, and the loop reports all fixes of least size
proves: [correctness]
status: full
---

**Setting.** The circuit $C$ has inputs $x_1, \ldots, x_n$, gates $g_1, \ldots, g_m$ in topological order, each with a Boolean function $\mathrm{op}_g$ of earlier signals, and a list of outputs. The tests are pairs $(v_j, y_j)$, $j = 1, \ldots, T$, of an input vector and the expected output values. $\Sigma$ is the set of suspect gates. For $S \subseteq \Sigma$:

- *Correction values* for $S$ are values $\omega(g, j) \in \{0, 1\}$ for $g \in S$ and every test $j$ such that, for every $j$, simulating $C$ on $v_j$ with the value of each $g \in S$ replaced by $\omega(g, j)$ gives $y_j$ at the outputs.
- A *fix* for $S$ is a family of Boolean functions $f_g : \{0, 1\}^n \to \{0, 1\}$, $g \in S$, such that the circuit $C[S \leftarrow f]$, in which each $g \in S$ is replaced by new logic that computes $f_g$ of the primary inputs, gives $y_j$ on $v_j$ for every test.

The debug formula $F$ of lines L1 to L3 has, for each test $j$, a variable $u_j$ for every signal $u$, unit clauses $x_{i,j} = v_j(x_i)$ and $y_{j} = y_j(y)$ for the outputs $y$, the Tseitin clauses of $g_j = \mathrm{op}_g(\text{fanins}_j)$ for $g \notin \Sigma$, and for $g \in \Sigma$ the Tseitin clauses of $o_{g,j} = \mathrm{op}_g(\text{fanins}_j)$ and the four multiplexer clauses

$$(\neg s_g \vee \neg w_{g,j} \vee g_j)\,(\neg s_g \vee w_{g,j} \vee \neg g_j)\,(s_g \vee \neg o_{g,j} \vee g_j)\,(s_g \vee o_{g,j} \vee \neg g_j),$$

which say $g_j = w_{g,j}$ if $s_g$ and $g_j = o_{g,j}$ otherwise. The selects $s_g$ are shared by all tests, and the $w_{g,j}$ are free.

**Lemma 1 (Tseitin clauses).** For fixed values of the inputs $\mathit{ins}$ and the output $\mathit{out}$ of a gate, its clauses, with their auxiliary variables, are satisfiable if and only if $\mathit{out} = \mathrm{op}(\mathit{ins})$.

*Proof.* For AND, the clauses $(\neg \mathit{out} \vee x)$ for each input and $(\mathit{out} \vee \bigvee \neg x)$ say $\mathit{out} \Rightarrow \bigwedge x$ and $\bigwedge x \Rightarrow \mathit{out}$. OR is dual, NAND and NOR use $\neg \mathit{out}$ in place of $\mathit{out}$, and NOT and BUF are two clauses of an equivalence. For XOR and XNOR, each auxiliary $t$ gets four clauses, one per row of the truth table of $\mathit{acc} \oplus x$, which force $t = \mathit{acc} \oplus x$. So the auxiliaries are determined, the last one is the XOR of all inputs, and the two final clauses say $\mathit{out}$ equals it or its negation. The tests check all gate types on all input values. $\square$

**Theorem 2 (selects and correction values).** For $S \subseteq \Sigma$, $F$ together with the units $s_g$ for $g \in S$ and $\neg s_g$ for $g \in \Sigma \setminus S$ is satisfiable if and only if $S$ has correction values.

*Proof.* ($\Rightarrow$) Take a model and put $\omega(g, j) = w_{g,j}$. Fix a test $j$ and let $\mathrm{val}$ be the simulation of $C$ on $v_j$ with the values of $S$ replaced by $\omega$. By induction over the topological order, $u_j = \mathrm{val}(u)$ in the model for every signal $u$. The inputs agree by the unit clauses. For a gate $g \notin \Sigma$, Lemma 1 gives $g_j = \mathrm{op}_g$ of the fanin variables, which agree with $\mathrm{val}$ by induction. For $g \in \Sigma \setminus S$, $s_g$ is false, so $g_j = o_{g,j} = \mathrm{op}_g(\ldots)$ in the same way. For $g \in S$, $g_j = w_{g,j} = \omega(g, j) = \mathrm{val}(g)$. The output units then say that $\mathrm{val}$ gives $y_j$.

($\Leftarrow$) Set $s_g$ by $S$, $w_{g,j} = \omega(g, j)$ for $g \in S$ and $w_{g,j} = 0$ for the other suspects, each $u_j$ to $\mathrm{val}(u)$ of test $j$, each $o_{g,j}$ to $\mathrm{op}_g$ of the fanin values, and the auxiliaries as in Lemma 1. The gate clauses hold by Lemma 1, the multiplexer clauses hold because $g_j = w_{g,j}$ for $g \in S$ and $g_j = o_{g,j}$ for the other suspects, and the unit clauses hold because the inputs are $v_j$ and $\omega$ is a set of correction values. $\square$

**Theorem 3 (correction values and fixes).** If $S$ has a fix, it has correction values. If the input vectors $v_1, \ldots, v_T$ are pairwise distinct, the converse holds.

*Proof.* Given a fix, simulate $C[S \leftarrow f]$ on $v_j$ and put $\omega(g, j) = f_g(v_j)$. The simulation of $C$ with these replaced values computes the same values at every signal, by induction over the topological order, so it gives $y_j$. Conversely, with distinct $v_j$ the definition $f_g(v_j) = \omega(g, j)$, and $f_g = 0$ on the other input vectors, is a function, and the same induction shows that $C[S \leftarrow f]$ gives $y_j$ on each $v_j$. $\square$

Without distinct vectors the converse fails: two tests with the same inputs and different expected outputs have correction values for the set of output gates, but no circuit passes both. The tests show this case.

**Lemma 4 (monotone).** If $S$ has correction values and $S \subseteq S' \subseteq \Sigma$, then $S'$ has correction values.

*Proof.* For $g \in S' \setminus S$ put $\omega(g, j)$ equal to the value of $g$ in the simulation of test $j$ with the replaced values of $S$. Replacing a value by itself changes nothing. $\square$

**Lemma 5 (sequential counter).** For $k < N$, the counter clauses of line L5 on $s_1, \ldots, s_N$ with auxiliaries $r_{i,j}$ ($1 \le i \le N - 1$, $1 \le j \le k$) are satisfiable together with a 0-1 assignment of the $s_i$ if and only if $\sum_i s_i \le k$. For $k = 0$ they are the units $\neg s_i$, and for $k \ge N$ there are none.

*Proof.* The clauses are $s_1 \Rightarrow r_{1,1}$, $\neg r_{1,j}$ for $j > 1$, and for $1 < i < N$: $s_i \Rightarrow r_{i,1}$, $r_{i-1,j} \Rightarrow r_{i,j}$, $s_i \wedge r_{i-1,j-1} \Rightarrow r_{i,j}$ for $j > 1$, and $\neg(s_i \wedge r_{i-1,k})$, and last $\neg(s_N \wedge r_{N-1,k})$. Let $c_i = \sum_{t \le i} s_t$. ($\Leftarrow$) Put $r_{i,j} = [c_i \ge j]$. Each implication holds because $c_i \ge c_{i-1}$ and $c_i = c_{i-1} + 1$ when $s_i = 1$. $\neg r_{1,j}$ for $j > 1$ holds as $c_1 \le 1$. The clause $\neg(s_i \wedge r_{i-1,k})$ fails only if $c_i = c_{i-1} + 1 \ge k + 1$, which $c_N \le k$ excludes. ($\Rightarrow$) In any model, $r_{i,j}$ is true whenever $c_i \ge j$, by induction on $i$ with the implications. If $c_N > k$, let $i$ be the index of the $(k+1)$-th true $s$. Then $i > 1$ (for $k \ge 1$), $c_{i-1} = k$ gives $r_{i-1,k}$, and $s_i \wedge r_{i-1,k}$ contradicts a clause. $\square$

**Theorem 6 (the loop).** Let $k$ be the first value of line L4 at which line L6 finds a model. Then lines L6 to L8 report, each once, exactly the sets $S \subseteq \Sigma$ with $\lvert S \rvert = k$ that have correction values, and no smaller set has correction values. If no $k \le k_{\max}$ finds a model, no set of at most $k_{\max}$ suspects has correction values.

*Proof.* For $k' < k$ the formula $F \wedge (\sum s \le k')$ is unsatisfiable. If a set $S$ with $\lvert S \rvert \le k'$ had correction values, Theorem 2 and Lemma 5 would give a model. So no set of size below $k$ has correction values, which also proves the last claim.

At $k$, a model has a select set $S$ with $\lvert S \rvert \le k$ by Lemma 5, and the model itself satisfies the formula of Theorem 2 for $S$, so $S$ has correction values. Hence $\lvert S \rvert = k$. The blocking clause $\bigvee_{g \in S} \neg s_g$ of line L8 excludes exactly the models whose select set contains $S$, and among sets of size at most $k$ that is $S$ alone. So no set is reported twice. Conversely, let $S$ have size $k$ and correction values. By Theorem 2 there is a model of $F$ with select set exactly $S$. It satisfies the counter by Lemma 5, and every blocking clause of a reported set $S' \ne S$, because $\lvert S' \rvert = \lvert S \rvert$ gives some $g \in S' \setminus S$ with $s_g$ false. So the loop cannot stop at line L6 before $S$ is reported. Each round adds a clause that removes the reported set, there are finitely many sets, and so the loop ends. $\blacksquare$

**Corollary.** With pairwise distinct test inputs, the sets of Theorem 6 are exactly the sets of $k$ suspects that have a fix for the tests (Theorem 3), and by Lemma 4 every superset of a reported set also has one. A fix for the tests need not be a fix for the specification on inputs outside the tests.
