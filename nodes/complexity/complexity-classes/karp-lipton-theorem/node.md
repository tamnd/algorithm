---
tag: REX9MR
kind: theorem
slug: karp-lipton-theorem
name: Karp-Lipton theorem
aliases:
- Karp-Lipton collapse
area: complexity/complexity-classes
level: advanced
summary: If NP has polynomial-size circuits, that is NP is in P/poly, then the polynomial hierarchy collapses to its second level, Sigma_2^p.
prereqs: [p-poly, polynomial-hierarchy, self-reducibility]
see_also: [p-poly, polynomial-hierarchy, adleman-theorem, non-uniform-computation, circuit-complexity, self-reducibility, sipser-gacs-theorem, kernel-lower-bounds]
sources:
  - paper: doi:10.1145/800141.804678
    title: Richard M. Karp and Richard J. Lipton, Some connections between nonuniform and uniform complexity classes, 12th ACM Symposium on Theory of Computing, 302 to 309 (1980)
    locator: the collapse theorem (with the improvement to the second level credited to Sipser), the theorem credited to Meyer on EXP, and the result on logarithmic advice
  - paper: "Richard M. Karp and Richard J. Lipton, Turing machines that take advice, L'Enseignement Mathématique 28 (1982), 191 to 209"
    locator: the journal version of the same results
  - paper: doi:10.1016/S0019-9958(82)90382-5
    title: Ravi Kannan, Circuit-size lower bounds and non-reducibility to sparse sets, Information and Control 55(1-3), 40 to 56 (1982)
    locator: the fixed-polynomial circuit lower bound for the second level, proved with the collapse
  - paper: doi:10.1137/S0097539795296206
    title: Johannes Köbler and Osamu Watanabe, New collapse consequences of NP having small circuits, SIAM Journal on Computing 28(1), 311 to 324 (1998)
    locator: the collapse of PH to ZPP^NP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 6, Boolean circuits (the Karp-Lipton theorem and Meyer's theorem)
---

The Karp-Lipton theorem says that if every problem in [NP](/np/) has Boolean circuits of polynomial size, then the [polynomial hierarchy](/polynomial-hierarchy/) collapses to its second level: $\mathsf{NP} \subseteq \mathsf{P/poly}$ implies $\mathsf{PH} = \Sigma_2^p$. Most researchers believe the hierarchy does not collapse, so the theorem is the main evidence that NP-complete problems have no small circuits, even non-uniform ones that nobody knows how to build. The proof guesses the circuit with an existential quantifier and uses [self-reducibility](/self-reducibility/) to make a wrong guess harmless. Karp and Lipton published it in 1980 with a collapse to the third level, and the paper credits Michael Sipser with the improvement to the second.

## Statement

**Theorem (Karp and Lipton 1980).** If $\mathsf{NP} \subseteq \mathsf{P/poly}$, then $\Pi_2^p = \Sigma_2^p$, and so $\mathsf{PH} = \Sigma_2^p$.

Here [P/poly](/p-poly/) is the class of languages with circuit families of polynomial size, and $\Sigma_2^p$ and $\Pi_2^p$ are the second level of the hierarchy. A language $L$ is in $\Pi_2^p$ if there are a polynomial-time predicate $R$ and a polynomial $q$ with

$$x \in L \iff \forall y \in \{0,1\}^{q(|x|)}\ \exists z \in \{0,1\}^{q(|x|)}\ R(x, y, z).$$

$\Sigma_2^p$ is the same with $\exists$ before $\forall$.

**Theorem (Meyer, in the same paper).** If $\mathsf{EXP} \subseteq \mathsf{P/poly}$, then $\mathsf{EXP} = \Sigma_2^p$.

## In plain words

Suppose that for each input size there is a small circuit that solves an NP-complete problem. Nobody needs to know how to build it. Take a question of the form "for every choice, is there an answer?". Turn it around: "is there a small circuit such that, for every choice, the circuit finds an answer?". If the circuit exists, the second question is true whenever the first is. If the first is false, some choice has no answer at all, and then no circuit can find one, so the second question is false too. The second question has the quantifiers in the opposite order. When the two orders give the same power, all higher levels of the hierarchy fall down to this level.

## Proof

Assume $\mathsf{NP} \subseteq \mathsf{P/poly}$. It suffices to prove $\Pi_2^p \subseteq \Sigma_2^p$. Then $\Sigma_2^p = \Pi_2^p$ by taking complements, and an induction on $k$ gives $\Sigma_k^p = \Sigma_2^p$ for all $k \ge 2$: a $\Sigma_{k+1}^p$ formula is an $\exists$ block in front of a $\Pi_k^p$ predicate, which is $\Pi_2^p = \Sigma_2^p$ by induction, and two adjacent $\exists$ blocks merge into one.

Let $L \in \Pi_2^p$ with $R$ and $q$ as in the statement. Let $n = |x|$ and $m = q(n)$.

*Step 1: a decision circuit.* Consider the language

$$A = \{ (x, y, w) : \exists z \in \{0,1\}^m \text{ with prefix } w \text{ such that } R(x, y, z) \}.$$

$A$ is in NP: guess the rest of $z$ and evaluate $R$. By assumption $A \in \mathsf{P/poly}$, so for each $n$ there is a circuit $D_n$ of size polynomial in $n$ that decides $A$ on all triples with $|x| = n$, $|y| = m$ and $|w| \le m$. Inputs of different lengths can be padded to one length.

*Step 2: a search circuit, by self-reducibility.* Build a circuit $W_n$ that on input $(x, y)$ computes a string $z$ as follows. Start with the empty $w$. For $i = 1, \ldots, m$: if $D_n(x, y, w0) = 1$, set $w = w0$, otherwise set $w = w1$. Output $z = w$. $W_n$ is $m$ copies of $D_n$ and some selection gates, so it has size polynomial in $n$. If some $z$ with $R(x, y, z)$ exists and $D_n$ is correct, then every prefix $w$ that $W_n$ keeps can be extended to such a $z$, and so $R(x, y, W_n(x, y))$ holds.

*Step 3: the $\Sigma_2^p$ formula.* Let $s(n)$ bound the size of $W_n$. Claim:

$$x \in L \iff \exists \text{ circuit } C \text{ of size } \le s(n)\ \ \forall y \in \{0,1\}^m:\ R(x, y, C(x, y)).$$

The right-hand side is a $\Sigma_2^p$ predicate: the circuit $C$ is a string of polynomial length, and evaluating $C$ and then $R$ takes polynomial time.

- If $x \in L$, then for every $y$ some $z$ with $R(x, y, z)$ exists, and $C = W_n$ outputs one, by Step 2.
- If $x \notin L$, there is a $y$ such that $R(x, y, z)$ is false for every $z$. For that $y$, $R(x, y, C(x, y))$ is false whatever $C$ is.

So $L \in \Sigma_2^p$. $\square$

The guessed circuit is never checked for being a correct SAT circuit. The formula checks only its outputs, and a false output is caught by $R$. This is why self-reducibility is used: a decision circuit could lie, but the answers of a search circuit can be verified.

**Example.** Take the $\Pi_2$ statement "every $y \in \{1, \ldots, N-1\}$ has an inverse $z \in \{0, \ldots, 7\}$ with $y z \equiv 1 \pmod N$", with $z$ written in 3 bits. For $N = 7$ and $y = 3$, the prefix queries of Step 2 ask whether an inverse exists with prefix $0$ (no), so $w = 1$; with prefix $10$ (yes), so $w = 10$; with prefix $100$ (no), so $w = 101$. The output is $z = 5$, and $3 \cdot 5 = 15 \equiv 1 \pmod 7$. The same search gives $z = 1, 4, 5, 2, 3, 6$ for $y = 1, \ldots, 6$, and this table is a circuit $C$ that makes the $\forall y$ check pass. For $N = 8$ and $y = 2$, no prefix query says yes, the search outputs $111$, and $2 \cdot 7 = 14 \equiv 6 \pmod 8$. Since $2$ has no inverse modulo $8$, every candidate $C$ fails at $y = 2$, and the $\Sigma_2$ formula is false, as it must be. The values $y = 4$ and $y = 6$ also fail.

**Proof of Meyer's theorem (sketch).** Let $L \in \mathsf{EXP}$ be decided by a machine $M$ in time $2^{n^k}$. The tableau of $M$ on $x$ has $2^{n^k} \times 2^{n^k}$ cells, and the function "content of cell $(i, j)$" is computable in exponential time, so by assumption it has a circuit $C$ of polynomial size. Then $x \in L$ if and only if there is a circuit $C$ such that for all cells $(i, j)$, the value $C(x, i, j)$ agrees with the values $C$ gives for the three cells above it under the rules of $M$, the first row is the start configuration, and the last cell shows acceptance. This is a $\Sigma_2^p$ formula, so $\mathsf{EXP} \subseteq \Sigma_2^p$.

## Consequences

- *Evidence against small circuits for NP.* A polynomial-size circuit family for SAT would collapse PH to $\Sigma_2^p$. So results that rest on "PH is infinite", a conjecture, also rest on $\mathsf{NP} \not\subseteq \mathsf{P/poly}$.
- *Randomized algorithms for NP.* $\mathsf{BPP} \subseteq \mathsf{P/poly}$ ([Adleman's theorem](/adleman-theorem/)), so $\mathsf{NP} \subseteq \mathsf{BPP}$ would also give $\mathsf{PH} = \Sigma_2^p$.
- *Fixed-polynomial lower bounds.* For each fixed $k$, $\Sigma_2^p \cap \Pi_2^p$ contains a language without circuits of size $O(n^k)$ (Kannan 1982). The proof splits into two cases. If NP is not in P/poly, SAT is such a language for large enough inputs. If it is, the hierarchy collapses, and a language in a higher level that diagonalizes against circuits of size $n^k$ falls into the second level.
- *P versus NP and EXP.* If $\mathsf{P} = \mathsf{NP}$, then $\Sigma_2^p = \mathsf{P}$. If also $\mathsf{EXP} \subseteq \mathsf{P/poly}$, Meyer's theorem would give $\mathsf{EXP} = \mathsf{P}$, which the [time hierarchy theorem](/time-hierarchy-theorem/) rules out. So $\mathsf{P} = \mathsf{NP}$ implies $\mathsf{EXP} \not\subseteq \mathsf{P/poly}$.
- *Smaller collapses.* The same assumption gives $\mathsf{PH} \subseteq \mathsf{ZPP}^{\mathsf{NP}}$ (Köbler and Watanabe 1998, after Bshouty, Cleve, Gavaldà, Kannan and Tamon), and later $\mathsf{PH} = \mathsf{S}_2^p$, a class inside $\Sigma_2^p \cap \Pi_2^p$ (Cai, from an observation of Sengupta). It also gives $\mathsf{AM} = \mathsf{MA}$.
- *Variants.* The same method shows that $\mathsf{coNP} \subseteq \mathsf{NP/poly}$ collapses PH to $\Sigma_3^p$ (Yap 1983). This weaker form is the basis of [kernel lower bounds](/kernel-lower-bounds/) in parameterized complexity.

## Tightness

- *Logarithmic advice.* Karp and Lipton also proved that $\mathsf{NP} \subseteq \mathsf{P}/\log$ implies $\mathsf{P} = \mathsf{NP}$: with $O(\log n)$ bits of advice, a polynomial-time machine can try all $n^{O(1)}$ advice strings and use self-reducibility to check each result. With polynomial advice this search is impossible, and only the collapse to $\Sigma_2^p$ is known.
- *Uniform circuits.* If the circuits for SAT could be printed in polynomial time, then $\mathsf{P} = \mathsf{NP}$. The theorem is about circuits that exist but may be hard to find.
- *The level of the collapse.* No proof is known that $\mathsf{NP} \subseteq \mathsf{P/poly}$ collapses PH to $\mathsf{P}^{\mathsf{NP}}$, let alone to NP. The known collapses are to classes that contain $\mathsf{P}^{\mathsf{NP}}$, such as $\mathsf{S}_2^p$ and $\mathsf{ZPP}^{\mathsf{NP}}$.
- *Relativization.* The proof relativizes: for every oracle $A$, $\mathsf{NP}^A \subseteq \mathsf{P}^A/\mathsf{poly}$ implies $\mathsf{PH}^A = \Sigma_2^{p,A}$.

## History

Karp and Lipton presented the theorem at STOC 1980, with the journal version in 1982 under the title "Turing machines that take advice". Their own argument collapsed PH to $\Sigma_3^p$, and the paper credits Michael Sipser with the improvement to $\Sigma_2^p$. The same paper introduced advice classes $\mathcal{C}/f$ in general, proved the result on logarithmic advice and gave Albert Meyer's theorem on EXP. Kannan (1982) combined the collapse with diagonalization to get fixed-polynomial circuit lower bounds. Köbler and Watanabe (1998) and Cai, with an idea of Sengupta, lowered the collapse further.

## References
