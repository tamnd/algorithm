---
tag: 7HS2XM
kind: definition
slug: termination-insensitive-noninterference
name: Termination-insensitive noninterference
aliases:
- TINI
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Noninterference that only compares runs that both terminate, so a program may leak secrets through whether it halts.
prereqs: [noninterference, implicit-flow]
see_also: [security-type-system, hyperproperty, self-composition, no-sensitive-upgrade, secure-multi-execution, faceted-execution, covert-channel, quantitative-information-flow]
sources:
  - paper: doi:10.1007/978-3-540-88313-5_22
    title: Aslan Askarov, Sebastian Hunt, Andrei Sabelfeld and David Sands, Termination-insensitive noninterference leaks more than just a bit, ESORICS 2008, LNCS 5283
    locator: "pp. 333 to 348; Section 2 (Definition 1, batch-job TINI; Definitions 4 and 5, termination-sensitive and termination-insensitive noninterference for programs with output; Proposition 1), Section 3 (Theorem 1), Section 4 (Theorem 2), Section 5 (Theorem 3)"
  - paper: doi:10.3233/JCS-1996-42-304
    title: Dennis Volpano, Cynthia Irvine and Geoffrey Smith, A sound type system for secure flow analysis, Journal of Computer Security 4(2-3), 1996
    locator: pp. 167 to 187, the soundness theorem, which is termination-insensitive
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, the termination channel and the termination-sensitive and termination-insensitive definitions
  - paper: doi:10.1007/11547662_24
    title: Tachio Terauchi and Alex Aiken, Secure information flow as a safety problem, Proceedings of SAS 2005, LNCS 3672
    locator: pp. 352 to 367, 2-safety and the reduction of termination-insensitive noninterference to a safety property by self-composition
---

Termination-insensitive noninterference (TINI) is the form of [noninterference](/noninterference/) that compares only runs that both stop. If two runs start with the same public inputs and both stop, they must end with the same public outputs. A run that does not stop is not compared with anything, so the secret may decide *whether* the program stops. This is the guarantee of the [security type system](/security-type-system/) of Volpano, Irvine and Smith, of the [no-sensitive-upgrade](/no-sensitive-upgrade/) monitor and of [faceted execution](/faceted-execution/), and of the languages Jif and FlowCaml. Askarov, Hunt, Sabelfeld and Sands (2008) showed that the leak it allows can be the whole secret, but only in time exponential in the size of the secret.

## Definition

**Setting.** A deterministic program $c$ runs over variables with labels in a security lattice; take the two-point lattice $L \le H$. Two stores are low-equivalent, $s_1 =_L s_2$, if they agree on every variable with label $L$. $[\![c]\!](s)$ is the final store of the run from $s$, or $\bot$ if the run does not stop.

**TINI.** $c$ is TINI if for all $s_1 =_L s_2$ with $[\![c]\!](s_1) \ne \bot$ and $[\![c]\!](s_2) \ne \bot$, we have $[\![c]\!](s_1) =_L [\![c]\!](s_2)$. This is the base definition of the page [noninterference](/noninterference/).

**TSNI.** $c$ is termination-sensitive noninterferent (TSNI) if it is TINI and, for all $s_1 =_L s_2$, $[\![c]\!](s_1) = \bot$ exactly when $[\![c]\!](s_2) = \bot$. Each TSNI program is TINI. Neither definition says anything about running time.

**Programs with output.** Askarov et al. call the definition above *batch-job* TINI (their Definition 1). For a program that writes public outputs while it runs, the observer sees a sequence of outputs and may see that the program diverges. Their Definition 5 says, in terms of the knowledge of the observer, that an observer who has seen the outputs $\vec{o}$ and then one more output learns nothing from the value of that output, only from the fact that there is one. For deterministic programs this is equivalent (their Proposition 1) to: for each public input, the output sequences of the runs on all secrets form a chain under the prefix order. Two runs may differ only in where one of them stops producing output. Batch-job TINI is the case of programs with at most one output, at the end.

## Examples and non-examples

Take $h$ high and $l$ low.

| program | TINI | TSNI | why |
|---|---|---|---|
| `l := h` | no | no | $l$ copies $h$ |
| `if h then l := 1 else l := 0` | no | no | an [implicit flow](/implicit-flow/) |
| `if h then l := 0 else l := 0` | yes | yes | $l = 0$ after each run |
| `while h = 0 do skip; l := 1` | yes | no | each run that stops ends with $l = 1$, but the run stops only when $h \ne 0$ |
| `while h > 0 do skip` | yes | no | the same channel, with no public output at all |
| `if l then (while true do skip)` | yes | yes | termination depends only on $l$ |

- **The whole secret through termination.** Askarov et al. give this program, for a secret $h$ in $\{0, \dots, 2^N - 1\}$: "for $i = 0$ to $2^N - 1$: output $i$; if $i = h$ then loop forever". It is TINI and is accepted by a Denning-style type system with output (their Theorem 1). The last output before the program hangs is $h$. But to reveal $h = 2^N - 1$ the observer must wait for $2^N$ outputs.
- **Not TINI with output.** "output $h \bmod 2$; $h := h$ div 2", repeated $N$ times, reveals the $N$ low binary digits of $h$ in $N$ outputs. Two secrets that differ in the last digit give two output sequences that are not prefixes of each other.

**Theorem (Askarov, Hunt, Sabelfeld and Sands 2008).** *Hypotheses:* a deterministic program with public output that is TINI in the sense of Definition 5; a secret $h$ in $\{0, \dots, 2^N - 1\}$; an observer who chooses the public input, sees the outputs of one run up to $t_N$ outputs, and sees divergence.

1. (Theorem 2.) If the observer learns $h$ exactly for every $h$ (the program *leaks reliably*), then $t_N \ge 2^N - 1$. So a TINI program does not leak reliably within any running time polynomial in $N$.
2. (Theorem 3.) If $h$ is uniform, the probability $G_N$ that the observer guesses $h$ after the run is at most $(t_N + 1)/2^N$. So the advantage $G_N - 1/2^N$ is at most $t_N / 2^N$, which is negligible when $t_N$ is polynomial in $N$.

The proof: for a TINI program, at each output step all runs that go on make the same output, so the tree of observations is a comb with at most one non-divergent branch at each node. It has at most $t_N + 1$ leaves, and each leaf gives one guess. The proof uses determinism, and the theorem says nothing about an observer who also measures time.

## Related definitions

- **[Noninterference](/noninterference/).** TINI is the termination-insensitive form fixed there. The page shows that it is a 2-safety property and that the termination-sensitive form is not.
- **[Hyperproperty](/hyperproperty/).** Both forms are hyperproperties, sets of sets of traces. TINI is 2-safety: each violation is shown by two finite runs. A TSNI violation can need a run that does not stop.
- **[Self-composition](/self-composition/).** TINI of $c$ holds exactly when the program $c; c'$, with $c'$ a renamed copy of $c$, satisfies the safety property "if the low parts agree at the start, they agree at the end", for runs that stop. [Constant-time verification](/constant-time-verification/) uses the same construction for a different observation, the sequence of branches and addresses.
- **Enforcement.** The [security type system](/security-type-system/), [no-sensitive-upgrade](/no-sensitive-upgrade/) and [faceted execution](/faceted-execution/) give TINI. [Secure multi-execution](/secure-multi-execution/) gives TSNI. A type system that allows only public loop conditions outside secret branches also gives TSNI.
- **[Covert channels](/covert-channel/).** Termination is one covert channel and time is another. TINI closes neither, and TSNI closes only the first.
- **[Quantitative information flow](/quantitative-information-flow/)** measures how much a program leaks. The theorem above bounds the leak of a TINI program per unit of running time: after $t$ outputs, the observer can tell apart at most $t + 1$ classes of secrets.

## References
