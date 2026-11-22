---
tag: B355TH
kind: algorithm
slug: constant-time-verification
name: Constant-time verification
aliases:
- ct-verif
area: security-and-privacy/side-channel-attacks
level: research
summary: Proves that a program is constant time by reducing the two-run property to a safety check on a product program.
model: word-ram
complexity:
  vars: {n: the size of the program, m: the number of start pairs with equal public inputs, t: the number of steps of one run of the product}
  time: {worst: O(n^2 + m t)}
  space: {extra: O(n^2)}
properties: {deterministic: true}
history:
  year: 2016
  people: [José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir, Michael Emmi]
  note: "Almeida, Barbosa, Barthe, Dupressoir and Emmi gave the reduction to a product program and the ct-verif tool at USENIX Security 2016, and proved the reduction in Coq."
prereqs: [self-composition, timing-attack, safety-property]
see_also: [constant-time-programming, noninterference, hyperproperty, security-type-system, symbolic-execution, set-associative-cache, test-vector-leakage-assessment, spectre-attack]
sources:
  - paper: "José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir and Michael Emmi, Verifying constant-time implementations, 25th USENIX Security Symposium, 2016, pages 53-70"
    locator: "Section 3 (the leakage models and Definition 1), Section 4 (the output-insensitive product of Figures 7 and 8 with Theorem 1, and the output-sensitive product with Theorem 2) and Section 5 (the ct-verif tool on LLVM through SMACK and Boogie)"
  - paper: doi:10.1109/CSFW.2004.1310735
    title: "Gilles Barthe, Pedro R. D'Argenio and Tamara Rezk, Secure information flow by self-composition, 17th IEEE Computer Security Foundations Workshop, 2004"
    locator: the reduction of noninterference to a property of one program that runs two copies of the original
  - paper: "Tachio Terauchi and Alex Aiken, Secure information flow as a safety problem, SAS 2005, LNCS 3672"
    locator: the notion of a 2-safety property and its check as a safety property of a composed program
  - paper: "Gilles Barthe, Juan Manuel Crespo and César Kunz, Relational verification using product programs, FM 2011, LNCS 6664"
    locator: the definition of product programs, which run two copies in lockstep where their control flow agrees
  - paper: doi:10.23919/DATE.2017.7927267
    title: "Oscar Reparaz, Josep Balasch and Ingrid Verbauwhede, Dude, is my code constant time?, DATE 2017, pages 1697-1702"
    locator: the dudect method, a Welch t-test on measured run times for two classes of inputs (a test, not a proof)
---

Constant-time verification proves that a program is constant time: for any two runs with the same public inputs, the program takes the same branches, accesses the same memory addresses and gives the same operands to variable-time instructions. This is a property of two runs, a [hyperproperty](/hyperproperty/) of the 2-safety class. The algorithm of Almeida et al. (2016) builds one product program that runs two copies of the input program in lockstep and asserts before each statement that the two copies leak the same thing. The input program is constant time exactly when the product can never fail an assert, which is an ordinary safety question for a standard verifier.

## In plain words

A program that handles a key must not let the key change what an observer can see from outside. The observer cannot read the data, but can see which way each branch goes and which memory cells the program touches, for example through the cache. To check this, think of two copies of the program. Both get the same public data, but each gets a different key. Run them side by side, one step at a time. Before each step, check that the two copies are about to show the same thing to the observer. If this holds for every possible pair of keys, the key never shows. The product program is this side-by-side run, written as one program, so a normal program checker can prove it safe.

## The problem

The input is a program $P$, a set $X$ of public inputs and a leakage model. The leakage model says what one step of a run shows to the observer. The output is "constant time", or a pair of start states that agree on $X$ and give two different leakage traces.

The *observer* of this page sees, for each run, the trace of leakage events and nothing else. In the toy language of the code these events are: the decision of each branch, the count of each loop, the array and the index of each memory access, and the two operands of each division. The values that the program computes are not in the trace. This is the constant-time policy of Almeida et al.: the sequence of branch decisions and memory addresses does not depend on secret inputs. Formally, $P$ is constant time when

$$\sigma =_X \hat\sigma \implies \tau(P, \sigma) = \tau(P, \hat\sigma)$$

for all start states $\sigma, \hat\sigma$, where $\tau$ is the leakage trace and $=_X$ means equal on the public inputs. This is [noninterference](/noninterference/) with the trace as the output.

## The algorithm

Each variable and array $x$ gets a fresh *shadow* copy $x'$, and $e'$ is the expression $e$ with every name replaced by its shadow. The *leak terms* of an expression are the subexpressions whose values its evaluation shows: the index of each load and both operands of each division. The joined state $\sigma \oplus \hat\sigma'$ holds the first run in the plain names and the second run in the shadow names.

```pseudo id=main
CT-VERIF(P, X, D)                 ▷ X: the public inputs, D: the finite domain of the inputs
L1  Q ← PRODUCT(P)
L2  for each pair (σ, σ̂) of start states over D with σ(x) = σ̂(x) for each x in X do
L3      run Q from the joined state σ ⊕ σ̂'
L4      if an assert of Q fails then
L5          return (false, σ, σ̂)
L6  return true

PRODUCT(B)                        ▷ B is a block of statements
L7  for x ← e: emit assert G(e); x ← e; x' ← e'
L8  for a[i] ← e: emit assert G(i) ∧ G(e) ∧ i = i'; a[i] ← e; a'[i'] ← e'
L9  for if c then B1 else B2:
L10     emit assert G(c) ∧ (c ≠ 0) = (c' ≠ 0); if c then PRODUCT(B1) else PRODUCT(B2)
L11 for repeat e times B1: emit assert G(e) ∧ e = e'; repeat e times PRODUCT(B1)
L12 do this for each statement of B in order, and return the emitted block

G(e)                              ▷ the leakage of e is the same in both copies
L13 return the conjunction of l = l' over the leak terms l of e
```

The asserts of lines L10 and L11 make the two copies take the same branch and the same number of iterations. So the product needs only one copy of the control structure, and it has as many paths as $P$. A plain [self-composition](/self-composition/) $P; \hat P$ has the product of the two path counts.

Lines L2 to L5 are the safety check. The code of this page does it by brute force over a small domain $D$, which is enough for a toy program and for the test. The ct-verif tool proves the same product safe for every input with a deductive verifier: it gives each loop of the product the invariant that each variable equals its shadow where the copies must agree, and it sends the verification conditions to an SMT solver.

## Example

Take values mod 4, one public input $p$, one secret input $s$ and a public table $T = [3, 1, 0, 2]$. The product of the one-line program $y \leftarrow T[s]$ is

$$\text{assert } s = s';\quad y \leftarrow T[s];\quad y' \leftarrow T'[s'].$$

The pair $s = 0$, $s' = 1$ with $p = 0$ fails the assert, and the two traces are the accesses to $T[0]$ and to $T[1]$. The verifier finds the five verdicts below.

| program | verdict | first witness |
|---|---|---|
| $y \leftarrow T[s]$ | not constant time | $s = 0$ and $s = 1$, with $p = 0$ |
| if $s$ then $y \leftarrow 1$ else $y \leftarrow 2$ | not constant time | $s = 0$ and $s = 1$ |
| $y \leftarrow p \operatorname{div} s$ | not constant time | $s = 0$ and $s = 1$ |
| $y \leftarrow 0$, then for $j = 0, 1, 2, 3$: $y \leftarrow y \mid (T[j] \mathbin{\&} (0 - (j = s)))$ | constant time | none |
| if $s \oplus s$ then $y \leftarrow T[s]$ else $y \leftarrow 2$ | constant time | none |

The fourth program reads every cell of $T$ and keeps the right one with a mask that is all ones or all zeros, so it computes $T[s]$ with the same four accesses for every $s$. This is the full-scan lookup of [constant-time programming](/constant-time-programming/). The last program is constant time because $s \oplus s = 0$ for every $s$, so the branch is always the same. A [security type system](/security-type-system/) rejects it, because the guard has a secret type. The product accepts it, because it reasons about values.

The trace also fixes the cost in an abstract cache. With 4 sets, 1 way, lines of 1 cell and costs of 1 for a hit and 10 for a miss, the program $x \leftarrow T[0];\ y \leftarrow T[s]$ costs 11 units when $s = 0$ and 20 units otherwise. The verifier rejects it. The masked lookup has the same cost for every $s$.

## Correctness

The proof is a lockstep simulation. Run PRODUCT$(B)$ from the joined state of $\sigma$ and $\hat\sigma$. By structural induction on $B$, either the product ends with no failed assert, the two runs of $B$ have the same trace and the product ends in the joined state of the two final states, or an assert fails and the two traces differ. The key step is that the events a statement emits before it enters a sub-block have a length fixed by the program text, and the assert before the statement holds exactly when these events are equal in the two copies. A failure therefore comes after two equal prefixes of equal length, so the traces differ. Line L2 enumerates every pair with equal public inputs, so CT-VERIF returns true if and only if $P$ is constant time on $D$, and every witness it returns is a real pair of distinguishable runs. This is the toy form of Theorem 1 of Almeida et al., which they proved in Coq. The full proof is below.

## Complexity

PRODUCT visits each statement once. The guard $G(e)$ repeats each leak term, and a leak term can contain other leak terms, so the product has size $O(n^2)$ in the worst case and $O(n)$ when the nesting depth of the expressions is bounded. Each run of the product takes $O(t)$ steps. The brute-force check runs the product on $m = |D|^{p + 2s}$ start pairs, for $p$ public and $s$ secret inputs, so the total time is $O(n^2 + m t)$ and the extra space is the size of the product.

The number $m$ grows exponentially with the number of inputs, so the brute-force check is only a model. With a deductive verifier the cost is the cost of the safety proof of one program of the size of $P$. For programs with unbounded loops and memory, the safety of a program is undecidable in general, so no checker is complete and fast on every input.

## Properties

- **Sound and complete for programs without public outputs (theorem).** Theorem 1 of Almeida et al. states that a safe program without public outputs is constant time if and only if its output-insensitive product is safe. The guarantee holds against an observer who sees the leakage trace of the model in each run.
- **Sound only when outputs are public (theorem).** If a program declares some outputs public, for example the length of a decrypted message, the output-insensitive product rejects some correct programs. The output-sensitive product of their Theorem 2 accepts more programs, and it is sound but not complete.
- **The paths of $P$, not the square.** The product keeps the control flow of $P$, so a path-based verifier sees no more paths in $Q$ than in $P$.
- **The model decides the meaning.** "Constant time" is relative to the leakage model. A model with branches and addresses only says nothing about a multiplication or a division that takes a data-dependent time on a given processor. Add their operands to the model to cover them, as the code does for division.
- **No speculation.** The model describes the paths that the program really takes. A processor that runs a wrong path for a short time, as in a [Spectre attack](/spectre-attack/), can leak secrets that no real path touches. A proof of this page does not cover that observer.

## Variants and improvements

- **Output-sensitive product.** Some branches may depend on values that are public outputs. The output-sensitive product lets the copies take different paths there, and records the public outputs in history variables.
- **Type systems.** A [security type system](/security-type-system/) for constant time gives each variable a level and rejects a secret guard or a secret index. It is fast and modular but rejects programs such as the $s \oplus s$ example.
- **Symbolic execution and model checking.** A [symbolic execution](/symbolic-execution/) or [bounded model checking](/bounded-model-checking/) of the product finds witnesses on bounded runs.
- **Quantitative checks.** A cache-aware [abstract interpretation](/abstract-interpretation/) can bound how many different cache states a program can reach, which gives a bound on the leak in bits instead of a yes or no answer.
- **Statistical tests.** dudect (Reparaz et al. 2017) runs the binary on two classes of inputs and applies a [Welch t-test](/welch-t-test/) to the measured times, in the style of [TVLA](/test-vector-leakage-assessment/). It is a measurement on one machine, not a proof, and it can miss a leak that its inputs do not trigger.
- **Speculative constant time.** Later work extends the observer with mispredicted paths, so that a verified program also resists the Spectre class of attacks.

## When to use it

Use it on the core routines of cryptographic code, such as field arithmetic, table lookups, comparisons of tags and padding checks, where the code is small, the secret inputs are clear and a leak is a key. Check the lowest level that you can, such as LLVM code or the binary, because a compiler can turn a masked select back into a branch. For a whole application, a type system or a taint check is cheaper; for code that you cannot change, a statistical test gives a measurement.

## Pitfalls

- **Checking the source only.** A proof on C source says nothing about the machine code if the compiler adds a branch or a table. ct-verif works on optimized LLVM code for this reason.
- **A leakage model that is too weak.** If the model leaves out variable-time instructions, the proof holds for a machine that does not exist.
- **Forgetting public outputs.** A program that reveals a public output, such as a message length, fails the output-insensitive check. Declare the output and use the output-sensitive product; do not weaken the leakage model.
- **Confusing this with a timing test.** The verifier proves a property of a model. A [timing attack](/timing-attack/) is a measurement on real hardware. The two meet only if the model covers every source of time variation on that hardware.
- **Exhaustive checks on a tiny domain.** The brute-force check of the code is complete only for the domain that it enumerates. A larger word size needs a symbolic proof.

## Implementations

## History

Barthe, D'Argenio and Rezk (2004) reduced noninterference to a property of one program by self-composition. Terauchi and Aiken (2005) named the class of 2-safety properties and showed that a smarter composition makes them easier to check. Barthe, Crespo and Kunz (2011) defined product programs that run the two copies in lockstep where their control flow agrees. Almeida, Barbosa, Barthe, Dupressoir and Emmi (2016) used this for the constant-time policy. Their product needs no lockstep search, because the policy forces the two copies to take the same branches. They proved the reduction in Coq and verified code from NaCl, OpenSSL, FourQlib and curve25519-donna with ct-verif. Reparaz, Balasch and Verbauwhede (2017) gave dudect, a statistical test of the same policy on real timings.

## References
