---
tag: DWXYHV
kind: concept
slug: certificate
name: Certificate
aliases:
- Certificate (witness)
- Proof of optimality certificate
- Witness
- proof string
- witness
area: complexity/np-completeness
level: intro
summary: A string that proves an instance is a yes-instance to a fixed checker. NP is the class of problems with certificates of polynomial length that a polynomial-time verifier checks.
prereqs: [decision-problem, polynomial-time]
see_also: [polynomial-time-verifier, np, co-np, certificate-complexity, pratt-certificate, search-problem, lp-duality, zero-knowledge-proof]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.1 (the class NP defined by certificates and verifiers) and Section 2.6 (coNP)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.3 (the class NP, verifiers and certificates)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.2 (polynomial-time verification)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 2.3 (nondeterministic computation and NP, the guessing stage and the checking stage)
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4(3), 214 to 220 (1975)
    locator: the main theorem (PRIMES is in NP)
---

A certificate for an instance $x$ of a [decision problem](/decision-problem/) is a string $y$ that proves that $x$ is a yes-instance to a fixed checking procedure. A satisfying assignment proves that a formula is satisfiable, and a factor proves that a number is composite. The class [NP](/np/) holds exactly the problems in which every yes-instance has a certificate of length polynomial in $|x|$ that a [polynomial-time verifier](/polynomial-time-verifier/) checks, and no no-instance has one. This page is about the string; the verifier page is about the checking machine, and the NP page proves that the certificate definition agrees with the one by [nondeterministic Turing machines](/nondeterministic-turing-machine/). The query notion of [certificate complexity](/certificate-complexity/) is a different measure.

## In plain words

A certificate is a short proof that the answer is yes. Finding it can be hard, but checking it must be easy. To show that a large number is not prime, you give one factor; anyone can divide and check. To show that a map can be colored with three colors so that no two neighbors match, you give the coloring; anyone can look at every border. A problem belongs to [NP](/np/) when every yes answer has such a short proof that a fast program can check, and when no false proof can pass the check for a no answer. A proof that the answer is no is a different thing, and for many problems nobody knows a short one.

## The idea

**The certificate relation.** Fix a relation $R \subseteq \{0,1\}^* \times \{0,1\}^*$. A string $y$ is a certificate for $x$ when $(x, y) \in R$. The relation defines the language
$$L_R = \{\, x : \exists y\ (x, y) \in R \,\}.$$
$R$ is an NP relation when two conditions hold:
- it is polynomially balanced: there is a polynomial $p$ with $|y| \le p(|x|)$ for every $(x, y) \in R$;
- it is decidable in polynomial time: a deterministic [multitape Turing machine](/multitape-turing-machine/) decides, given $(x, y)$, whether $(x, y) \in R$ in time polynomial in $|x| + |y|$.

A language $L$ is in NP exactly when $L = L_R$ for some NP relation $R$. Two properties make $R$ a correct proof system for $L$. Completeness: every $x \in L$ has at least one certificate. Soundness: no $x \notin L$ has a certificate, so no string fools the checker on a no-instance. The machine that decides $R$ is the [verifier](/polynomial-time-verifier/).

**The certificate depends on the relation.** A problem has many certificate systems. A composite number $N$ has the factor $d$ with $1 < d < N$ and $d \mid N$; it also has the bases that make the Miller-Rabin test fail (see [compositeness certificates](/compositeness-witness/)). PRIMES has the [Pratt certificate](/pratt-certificate/): a primitive root $a$ modulo $N$, the prime factors of $N - 1$, and a Pratt certificate for each factor, of $O(\log^2 N)$ bits in total. Pratt (1975) used it to show that PRIMES is in NP, long before PRIMES was shown to be in P.

**Why the length bound is the real restriction.** Without the bound $|y| \le p(|x|)$, every [decidable language](/decidable-language/) has certificates that are checkable in time polynomial in $|x| + |y|$: take $y$ to be the full run of a deciding machine on $x$, step by step, and check each step. The run can be exponentially long, so the check is fast only relative to the long certificate. The polynomial bound on $|y|$, together with the polynomial bound on the checking time in $|x|$, is what makes NP a small class.

**Certificates for no-instances.** A certificate for the answer no of $L$ is a certificate for the complement of $L$. The class of languages whose no-instances have short checkable certificates is [coNP](/co-np/). A problem in NP and in coNP has short certificates for both answers. Linear programming feasibility is an example: a feasible point certifies yes, and by [LP duality](/lp-duality/) (Farkas' lemma) a dual vector certifies no. The same duality gives a certificate of optimality: a primal solution and a dual solution with equal values prove that both are optimal. Edmonds called problems with such two-sided certificates [good characterizations](/good-characterization/). For a [coNP-complete](/co-np-complete/) problem such as unsatisfiability, a short certificate for every no-instance of its complement would give NP = coNP, which is open.

**Finding a certificate.** The [search problem](/search-problem/) of an NP relation asks for a certificate, not only for the answer; these search problems form [FNP](/fnp/). For SAT and the other [self-reducible](/self-reducibility/) problems, a [search to decision reduction](/search-to-decision-reduction/) finds a certificate with polynomially many calls to the decision problem. Counting the certificates is a harder task in general; see [model counting](/model-counting/) and [parsimonious reductions](/parsimonious-reduction/), which keep the number of certificates.

**Other proof models.** An [interactive proof](/interactive-proofs/) replaces the fixed string by a conversation with a prover. A [probabilistically checkable proof](/probabilistically-checkable-proof/) is a certificate in a special format that a randomized verifier checks by reading a constant number of its bits. A [zero-knowledge proof](/zero-knowledge-proof/) convinces the verifier that a certificate exists without showing it.

## Examples

**A factor of a composite number.** For $N = 8051$, the certificate $d = 83$ is checked with one division: $8051 = 83 \times 97$. A search by trial division from 2 upward finds 83 after 82 divisions. For a number of $b$ bits, the check takes time polynomial in $b$, but no algorithm is known that finds a factor in time polynomial in $b$; see [integer factorization](/integer-factorization/).

**A 3-coloring of the Petersen graph.** Number the outer cycle $0, 1, 2, 3, 4$, join $i$ to $i + 5$, and join the inner vertex $5 + i$ to $5 + ((i + 2) \bmod 5)$. The graph has 15 edges. A certificate for "the graph is 3-colorable" is a list of 10 colors, and the check looks at each of the 15 edges once. A script went through all $3^{10} = 59049$ color lists: 120 of them are proper colorings, and the first in lexicographic order is $(0, 1, 0, 1, 2, 1, 0, 2, 2, 1)$. Any of the 120 is a valid certificate. See [three-coloring](/three-coloring/).

**Subset sum.** For the numbers $(3, 34, 4, 12, 5, 2)$ and the target 9, the script found 2 certificates among the $2^6 = 64$ subsets: $\{4, 5\}$ and $\{3, 4, 2\}$. Each check is one addition per chosen number and one comparison. See [subset sum](/subset-sum-problem/).

**A satisfying assignment.** For the [CNF](/conjunctive-normal-form/) formula $(x_1 \lor x_2) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_2 \lor \lnot x_3)$, the assignment $x_1 = 0, x_2 = 1, x_3 = 0$ is a certificate for [SAT](/sat/). The check evaluates each clause once, in time linear in the length of the formula.

**A no-answer without a short certificate.** The CNF formula with all 8 clauses $(\pm x_1 \lor \pm x_2 \lor \pm x_3)$ has no satisfying assignment; a script checked all 8 assignments and each one falsifies exactly one clause. A single assignment cannot prove this. The truth table is a proof, but it has $2^n$ rows for $n$ variables. Unsatisfiability is coNP-complete, so a short certificate for every unsatisfiable formula would give NP = coNP.

## Where it is used

- The definition of [NP](/np/) by verifiers, and of [coNP](/co-np/) by certificates for no-instances. The [Cook-Levin theorem](/cook-levin-theorem/) builds a formula whose satisfying assignments encode a certificate together with the run of the verifier on it.
- [NP-completeness proofs](/np-completeness-proof/): the membership step gives the certificate and the verifier, and a [Levin reduction](/levin-reduction/) also maps certificates in both directions.
- SAT solvers return a satisfying assignment as a certificate of the answer yes, so a user can check it independently of the solver.
- Number theory: [Pratt certificates](/pratt-certificate/) and the other [primality certificates](/primality-certificate/) prove that a number is prime, and a factor proves that it is composite.
- Optimization: a dual solution is a certificate of optimality for a linear program ([LP duality](/lp-duality/)).
- Cryptography: a [one-way function](/one-way-function/) makes certificates easy to check but hard to find, and [zero-knowledge proofs](/zero-knowledge-proof/) prove that a certificate exists without showing it.

## References
