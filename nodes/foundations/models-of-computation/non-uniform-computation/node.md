---
tag: GN5381
kind: concept
slug: non-uniform-computation
name: Non-uniform computation
aliases:
- Nonuniform complexity
- advice
- advice model
- circuit families
- non-uniform model
- nonuniform computation
area: foundations/models-of-computation
level: advanced
summary: Computation where each input length gets its own circuit or advice string, separating model power from uniformity.
prereqs: [boolean-circuit, p, asymptotic-notation]
see_also: [p-poly, bpp, adleman-theorem, karp-lipton-theorem, polynomial-hierarchy, self-reducibility, branching-program, circuit-complexity]
sources:
  - paper: "Richard M. Karp and Richard J. Lipton, Some connections between nonuniform and uniform complexity classes, Proceedings of the 12th ACM Symposium on Theory of Computing (STOC 1980)"
    locator: the theorem that NP in P/poly collapses the polynomial hierarchy, and the definition of advice classes
  - paper: "Leonard Adleman, Two theorems on random polynomial time, Proceedings of the 19th IEEE Symposium on Foundations of Computer Science (FOCS 1978)"
    locator: the theorem that RP has polynomial-size circuits
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 6, Boolean circuits (P/poly, Karp-Lipton); Section 7.5.1 (BPP is in P/poly); Chapter 5 (the collapse of the polynomial hierarchy)
  - paper: "Russell Impagliazzo and Avi Wigderson, P = BPP if E requires exponential circuits: Derandomizing the XOR lemma, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC 1997)"
    locator: the main theorem
  - paper: "Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1) (1949)"
    locator: the counting argument for the number of functions that circuits of a given size compute
  - paper: "Charles H. Bennett and John Gill, Relative to a random oracle A, P^A ≠ NP^A ≠ co-NP^A with probability 1, SIAM Journal on Computing 10(1) (1981)"
    locator: the remark that BPP languages have polynomial-size circuits
  - paper: "O. B. Lupanov, A method of circuit synthesis, Izvestiya VUZ Radiofizika 1 (1958)"
    locator: the upper bound of (1 + o(1)) 2^n / n on the circuit size of every function
  - paper: "Ravi Kannan, Circuit-size lower bounds and non-reducibility to sparse sets, Information and Control 55 (1982)"
    locator: the theorem that Sigma_2 is not in SIZE(n^k) for any fixed k
  - paper: "Leonard Berman and Juris Hartmanis, On isomorphisms and density of NP and other complete sets, SIAM Journal on Computing 6(2) (1977)"
    locator: the result of Meyer that P/poly is the class of languages that reduce to sparse sets
  - paper: "David A. Mix Barrington, Neil Immerman and Howard Straubing, On uniformity within NC1, Journal of Computer and System Sciences 41(3) (1990)"
    locator: the definition of DLOGTIME uniformity and its comparison with logspace uniformity
---

Non-uniform computation lets the algorithm for inputs of length $n$ depend on $n$ in an arbitrary way. The algorithm for each length is a separate [Boolean circuit](/boolean-circuit/), or a fixed *advice* string that a machine reads together with the input. The class [P/poly](/p-poly/) is the main example. It contains all languages that polynomial-size circuits decide, and it also contains undecidable languages, so it is not a model of efficient algorithms that someone can write down.

## In plain words

A normal algorithm is one finite program that works for inputs of every length. A non-uniform algorithm is a whole list of programs, one for each input length. Nobody needs to say how to find the program for a given length, and the list may be impossible to compute. Each program in the list must be small and fast.

Another way to see the same idea is a helper. Before the work starts, a helper who knows only the input length hands a short note to the algorithm. The note depends on the length and on nothing else. Two inputs of the same length get the same note.

The model is strong enough to hold random algorithms, because a lucky choice of random bits can serve as the note. Each program is a fixed finite object, so one can count them, and this is how lower bounds are proved.

## The idea

**Circuit families.** A *circuit family* is a sequence $(C_n)_{n \ge 1}$ where $C_n$ is a [Boolean circuit](/boolean-circuit/) with $n$ inputs and one output. It *decides* a language $L \subseteq \{0,1\}^*$ if $C_{|x|}(x) = 1 \iff x \in L$ for every string $x$. The family has *size* $s(n)$ if $C_n$ has at most $s(n)$ gates. The family is not required to have a finite description: the map from $n$ to $C_n$ can be any function, even a function that no algorithm computes.

**Advice.** Let $f : \mathbb{N} \to \mathbb{N}$. A language $L$ is in $\mathrm{P/}f$ if there are a deterministic polynomial-time machine $M$ and strings $a_1, a_2, \dots$ with $|a_n| \le f(n)$ such that, for every string $x$, $x \in L \iff M(x, a_{|x|}) = 1$. The string $a_n$ is the *advice* for length $n$. The class $\mathrm{P/poly}$ is the union of $\mathrm{P/}n^c$ over all constants $c$. The same definition with another machine gives other classes, for example $\mathrm{L/poly}$ for a logarithmic-space machine that reads the advice on a read-only tape.

**Theorem 1.** $L \in \mathrm{P/poly}$ if and only if $L$ is decided by a circuit family of polynomial size.

*Proof.* Suppose $L \in \mathrm{P/poly}$ with machine $M$ and advice $a_n$ of length at most $n^c$. The machine runs in time polynomial in $n + |a_n|$, hence in time polynomial in $n$. A computation of a polynomial-time machine on an input of a given length is simulated by a circuit of polynomial size that has the input bits as inputs (the standard simulation of a Turing machine by a circuit, see Arora and Barak, Chapter 6). Take the circuit for inputs of length $n + |a_n|$ and fix the last $|a_n|$ inputs to the bits of $a_n$. This gives $C_n$. Conversely, suppose that $(C_n)$ decides $L$ and has size at most $p(n)$. Let $a_n$ be a description of $C_n$ in a fixed encoding, of length $O(p(n) \log p(n))$. The machine $M$ reads $x$ and $a_{|x|}$ and evaluates the circuit that $a_{|x|}$ describes on $x$ in polynomial time. $\square$

**Uniformity.** A circuit family is *uniform* if some machine computes $C_n$ from $1^n$ with a resource bound, for example in polynomial time. The languages with polynomial-size circuit families that are uniform in polynomial time are exactly $\mathrm{P}$. In one direction, $\mathrm{P}$ has such families by the simulation in Theorem 1. In the other, the machine computes $C_{|x|}$ and then evaluates it on $x$. So the whole gap between $\mathrm{P}$ and $\mathrm{P/poly}$ is uniformity, and not size.

**Theorem 2.** $\mathrm{P/poly}$ contains an undecidable language.

*Proof.* Let $A \subseteq \mathbb{N}$ be an undecidable set (for example, the set of $n$ such that the $n$-th [Turing machine](/turing-machine/) halts on the empty input). Let $U = \{1^n : n \in A\}$. Use the advice $a_n = 1$ if $n \in A$ and $a_n = 0$ otherwise. The machine rejects every input that is not of the form $1^n$. On $1^n$ it outputs $a_n$. This machine decides $U$. If $U$ were decidable, then $A$ would be decidable. $\square$

**Counting.** Circuits cannot do everything. Count circuits with $n$ inputs and $s$ gates, each gate being any of the $16$ functions of two inputs. A gate has $16$ choices of function, and each of its two inputs is one of at most $n + s$ nodes. Choose also the output gate. So there are at most $s \cdot (16 (n+s)^2)^s$ such circuits. There are $2^{2^n}$ functions on $n$ bits. For $n = 10$ and $s = 62$ the number of circuits is at most $2^{1020}$, which is less than $2^{1024}$. A circuit with fewer than $62$ gates can be padded to $62$ gates without changing its function. So some function of $10$ inputs needs at least $63$ gates. The same counting, done with care for large $n$, shows that almost all functions on $n$ bits need circuits of size $\Omega(2^n / n)$. Shannon (1949) gave this argument for switching circuits. Lupanov (1958) showed that every function on $n$ bits has a circuit of size $(1+o(1))2^n/n$, so the bound is tight. Hence $\mathrm{P/poly}$ is a proper subclass of the set of all languages, and non-uniformity does not give every language.

**Other facts on circuit size.** Kannan (1982) proved that for every fixed $k$ the class $\Sigma_2$ contains a language that has no circuits of size $O(n^k)$. So the lower bound that is open for $\mathrm{NP}$ is known one level higher, for each fixed polynomial. Meyer (in Berman and Hartmanis 1977) showed that $\mathrm{P/poly}$ is exactly the class of languages that reduce by a polynomial-time Turing reduction to a sparse set, a set with at most a polynomial number of strings of each length.

**Weaker uniformity.** For small classes, uniformity in polynomial time is too strong, because the machine that builds the circuit can do more than the circuit. Classes such as [NC](/nc/)$^1$ and [AC](/ac0/)$^0$ use logspace uniformity, where a [logarithmic-space](/logspace/) machine builds $C_n$ from $1^n$, or DLOGTIME uniformity, where a machine answers questions about the gates of $C_n$ in time $O(\log n)$. Barrington, Immerman and Straubing (1990) defined DLOGTIME uniformity for these classes and compared it with logspace uniformity.

## Examples

**Karp and Lipton (1980).** If [NP](/np/) is contained in $\mathrm{P/poly}$, then $\Pi_2 \subseteq \Sigma_2$, and so the [polynomial hierarchy](/polynomial-hierarchy/) equals its second level $\Sigma_2$. This is the main evidence that $\mathrm{NP}$ does not have small circuits.

*Proof.* Assume $\mathrm{NP} \subseteq \mathrm{P/poly}$. Let $L \in \Pi_2$. There are a polynomial-time predicate $\varphi$ and a polynomial $q$ such that, for $|x| = n$, $x \in L$ if and only if for all $y \in \{0,1\}^{q(n)}$ there is a $z \in \{0,1\}^{q(n)}$ with $\varphi(x, y, z) = 1$. Define the language
$$L' = \{(x, y, w) : \text{there is a } z \text{ with } w \text{ a prefix of } z \text{ and } \varphi(x, y, z) = 1\},$$
where $w$ is a string of length at most $q(n)$. The language $L'$ is in $\mathrm{NP}$ (guess the rest of $z$), so it has circuits $D_m$ of polynomial size, where $D_m$ takes inputs of length $m$. Pad the inputs so that all the triples with $|x| = n$ have one length $m(n)$, a polynomial. Let $E_n$ be this circuit for $L'$ on inputs of length $m(n)$.

From $E_n$ we make a circuit $S_n$ that computes a $z$ from $(x, y)$ by self-reduction: it builds the bits $z_1, \dots, z_{q(n)}$ one at a time. The bit $z_i$ is $1$ if $E_n$ accepts $(x, y, z_1 \cdots z_{i-1} 1)$, and $0$ otherwise. The circuit $S_n$ uses $q(n)$ copies of $E_n$, so its size is polynomial.

Claim: $x \in L$ if and only if there is a circuit $S$ of size at most $r(n)$ (the size of $S_n$) such that, for all $y$, $\varphi(x, y, S(x, y)) = 1$. If $x \in L$, take $S = S_n$. Fix $y$. Because $x \in L$ there is a $z$ with $\varphi(x, y, z) = 1$, so $(x, y, \epsilon) \in L'$, where $\epsilon$ is the empty prefix. Inductively, if the prefix $z_1 \cdots z_{i-1}$ built so far can be extended to a witness, then one of the two prefixes $z_1 \cdots z_{i-1} 0$ and $z_1 \cdots z_{i-1} 1$ can be. If the prefix with $1$ can be extended, $S_n$ takes it. If it cannot, the prefix with $0$ can, and $S_n$ takes it. So the bits that $S_n$ builds form a witness, and $\varphi(x, y, S_n(x, y)) = 1$. In the other direction, if such an $S$ exists, then for each $y$ the string $S(x, y)$ is a witness $z$, so $x \in L$.

The claim says that $x \in L$ if and only if $\exists S\, \forall y\, \varphi(x, y, S(x,y)) = 1$, where $S$ ranges over descriptions of size at most $r(n)$ and the evaluation of $S$ takes polynomial time. That is a $\Sigma_2$ form, so $L \in \Sigma_2$. Hence $\Pi_2 \subseteq \Sigma_2$. Taking complements gives $\Sigma_2 \subseteq \Pi_2$, so $\Sigma_2 = \Pi_2$. By the standard induction, $\Sigma_k = \Pi_k$ implies $\Sigma_j = \Sigma_k$ for every $j \ge k$ (Arora and Barak, Chapter 5), so the hierarchy equals $\Sigma_2$. $\square$

**Adleman's theorem: BPP is in P/poly.** Adleman (1978) proved it for [RP](/rp/). The same argument with amplification gives [BPP](/bpp/) (Bennett and Gill 1981). Let $L \in \mathrm{BPP}$. There are a polynomial-time machine $M$ and a polynomial $m$ such that, for every $x$ of length $n$ and a uniformly random $r \in \{0,1\}^{m(n)}$, $\Pr_r[M(x, r) \ne L(x)] \le 1/3$. Here $L(x)$ is $1$ if $x \in L$ and $0$ otherwise.

*Proof.* Fix $n$. Let $k$ be the smallest odd integer with $k \ge 13n$. Choose $r_1, \dots, r_k$ independently and uniformly from $\{0,1\}^{m(n)}$. Call a string $x$ of length $n$ *bad* for $(r_1, \dots, r_k)$ if $M(x, r_i) \ne L(x)$ for at least $k/2$ of the indices $i$. The majority vote of $M(x, r_1), \dots, M(x, r_k)$ is wrong only if $x$ is bad, since $k$ is odd.

Fix $x$. Let $X_i = 1$ if $M(x, r_i) \ne L(x)$ and $X_i = 0$ otherwise. The $X_i$ are independent with values in $\{0, 1\}$ and $\Pr[X_i = 1] \le 1/3$. Let $S = \sum_i X_i$. Then $\mathbb{E}[S] \le k/3$, so $S \ge k/2$ implies $S - \mathbb{E}[S] \ge k/6$. Hoeffding's inequality for a sum of $k$ independent variables with values in $[0,1]$ states $\Pr[S - \mathbb{E}[S] \ge t] \le e^{-2t^2/k}$. With $t = k/6$ we get
$$\Pr[x \text{ is bad}] \le e^{-2 (k/6)^2 / k} = e^{-k/18} \le e^{-13n/18} < 2^{-n}.$$
The last step holds because $13/18 > \ln 2$ (the first is $0.7222$ and the second is $0.6931$ to four digits).

There are $2^n$ strings of length $n$. By the union bound, $\Pr[\text{some } x \text{ of length } n \text{ is bad}] < 2^n \cdot 2^{-n} = 1$. So there is a choice of $(r_1, \dots, r_k)$ for which no string of length $n$ is bad. Let $a_n$ be this tuple. It has length $k \cdot m(n)$, which is polynomial in $n$. The machine that reads $x$ and $a_{|x|}$, runs $M(x, r_i)$ for each $i$ and outputs the majority is deterministic and runs in polynomial time. It decides $L$. So $L \in \mathrm{P/poly}$. $\square$

The proof is not constructive: it shows that a good tuple exists and does not say how to find one. The result has its own page, [Adleman's theorem](/adleman-theorem/).

## Where it is used

- **Circuit lower bounds.** Since $\mathrm{P} \subseteq \mathrm{P/poly}$, a proof that some language in $\mathrm{NP}$ has no polynomial-size circuits would show $\mathrm{P} \ne \mathrm{NP}$. This is the reason that [circuit complexity](/circuit-complexity/) is a main approach to the problem. The Karp-Lipton theorem says that such a lower bound is expected, because the opposite would collapse the hierarchy.
- **Derandomization.** Adleman's theorem puts randomized algorithms inside the non-uniform model. Impagliazzo and Wigderson (1997) proved a converse type of result: if some language decidable in time $2^{O(n)}$ requires circuits of size $2^{\epsilon n}$ for a constant $\epsilon > 0$ on all large input lengths, then $\mathrm{P} = \mathrm{BPP}$. So a non-uniform lower bound gives a uniform derandomization.
- **Space-bounded models.** Polynomial-size [branching programs](/branching-program/) are the non-uniform form of logarithmic space: they decide exactly $\mathrm{L/poly}$.

## References
