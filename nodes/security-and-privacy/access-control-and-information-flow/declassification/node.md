---
tag: GKERSF
kind: concept
slug: declassification
name: Declassification
aliases:
- intended release
- downgrading
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: A controlled release of some secret information, such as a password check result, stated by what, who, where and when it may be released.
prereqs: [noninterference, security-type-system]
see_also: [decentralized-label-model, termination-insensitive-noninterference, quantitative-information-flow, min-entropy-leakage, hyperproperty, denning-lattice-model, password-hashing, trust-management]
sources:
  - paper: doi:10.3233/JCS-2009-0352
    title: Andrei Sabelfeld and David Sands, Declassification, dimensions and principles, Journal of Computer Security 17(5), 2009
    locator: pp. 517 to 548, the four dimensions (what, who, where, when) and the principles of semantic consistency, conservativity, monotonicity of release and non-occlusion
  - paper: doi:10.1109/CSFW.2005.15
    title: Andrei Sabelfeld and David Sands, Dimensions and principles of declassification, Proceedings of the 18th IEEE Computer Security Foundations Workshop, 2005
    locator: pp. 255 to 269, the conference version
  - paper: doi:10.1007/978-3-540-37621-7_9
    title: Andrei Sabelfeld and Andrew C. Myers, A model for delimited information release, Software Security, Theories and Systems (ISSS 2003), LNCS 3233, 2004
    locator: pp. 174 to 191, escape hatches and the definition of delimited release
  - paper: doi:10.1109/CSFW.2001.930133
    title: Steve Zdancewic and Andrew C. Myers, Robust declassification, Proceedings of the 14th IEEE Computer Security Foundations Workshop, 2001
    locator: pp. 15 to 23, the definition of robust declassification
  - paper: doi:10.1109/CSFW.2004.1310740
    title: Andrew C. Myers, Andrei Sabelfeld and Steve Zdancewic, Enforcing robust declassification, Proceedings of the 17th IEEE Computer Security Foundations Workshop, 2004
    locator: pp. 172 to 186, a type system for robust declassification
  - paper: doi:10.1145/363516.363526
    title: Andrew C. Myers and Barbara Liskov, Protecting privacy using the decentralized label model, ACM Transactions on Software Engineering and Methodology 9(4), 2000
    locator: pp. 410 to 442, Section 3.6, declassification by the authority of the owners of a label
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, the section on declassification as an open problem
---

Declassification is a release of secret information that the policy allows on purpose. [Noninterference](/noninterference/) forbids every flow from secret to public data, but useful programs must release some of it: a login program tells whether the password was right, a payroll system publishes the average salary, and an encryption program publishes the ciphertext. A declassification lowers the level of one value, and a declassification policy says which releases are allowed. Sabelfeld and Sands (2009) sort these policies by four dimensions: *what* is released, *who* releases it, *where* in the program, and *when*.

## In plain words

A secret should stay secret, but sometimes a small part of it must come out. A login screen must say "wrong password". That answer tells something about the real password. If the program may release some secrets, the hard part is to stop it from releasing more than that. A careless rule such as "the programmer may mark any value as public" lets a bug or an attacker mark the whole password as public. So a good policy says exactly what may come out (only the yes or no answer), who may decide this (only the owner of the password), where in the program it may happen (only in the login function), and when (only after the user typed a password).

## The idea

**The construct.** A language for information flow adds an expression declassify$(e, \ell)$. Its value is the value of $e$, and its label is $\ell$, which can be lower than $\mathrm{label}(e)$. The [security type system](/security-type-system/) accepts it under conditions that depend on the policy. Without conditions, "$l$ := declassify$(h, L)$" releases everything, and the program is secure only in name.

**What.** The policy names the information that may be released. In *delimited release* (Sabelfeld and Myers 2004) the policy is a set of *escape hatches*, expressions such as $h = g$ or the average of the salaries. A program satisfies delimited release if, for two initial stores that agree on the public variables and on the values of the escape hatches, the runs give the same public outputs. So the program releases at most the escape hatch values *in the initial state*. The program "for each candidate $g$: $l$ := declassify$(h = g)$" uses only the escape hatch $h = g$, but evaluates it for many values of $g$ and so finds $h$; delimited release rejects it, because the hatch is evaluated on states other than the initial one.

**Who.** The policy names the principals that may release the information. In the [decentralized label model](/decentralized-label-model/) only a process with the authority of an owner may relax that owner's policy. *Robust declassification* (Zdancewic and Myers 2001) asks that an attacker who controls the untrusted (low-integrity) inputs cannot change what is declassified. Myers, Sabelfeld and Zdancewic (2004) give a type system for it: the decision to declassify and the data released must be trusted.

**Where.** The policy names the program points that may release, such as one function, or the locality of the release in the code. In systems with several domains, intransitive noninterference (Rushby) lets information go from $A$ to $C$ only through a downgrader $B$.

**When.** The policy names the time or the condition of the release: after a payment, after a fixed date, or after the key of a ciphertext is released.

**Principles.** Sabelfeld and Sands give four tests for a definition of secure declassification:

- *Semantic consistency.* The security of a program does not change when a part without declassification is replaced by a part with the same meaning.
- *Conservativity.* For a program with no declassification, the definition is noninterference.
- *Monotonicity of release.* Adding a declassification to a secure program cannot make it insecure.
- *Non-occlusion.* A declassification must not hide a leak that it does not cause.

**Declassification and the decentralized label model.** Declassification is the general question: which releases are allowed. The [decentralized label model](/decentralized-label-model/) is one data model that answers its *who* dimension: a label lists the policies of several owners, and each owner can declassify only its own policy.

## Examples

**A password check.** The secret $p$ is uniform on $\{0, 1, \dots, 7\}$, and the program releases the result of one check $p = g$ for a public guess $g$. Before the check, the best guess of an observer succeeds with probability $V = 1/8$. After the check, the observer knows $p$ with probability $1/8$ (a match), and otherwise $p$ is uniform on the 7 other values:

$$V_{\text{after}} = \tfrac{1}{8} \cdot 1 + \tfrac{7}{8} \cdot \tfrac{1}{7} = \tfrac{2}{8}.$$

The [min-entropy leakage](/min-entropy-leakage/) is $\log_2 (V_{\text{after}} / V) = \log_2 2 = 1$ bit. With $k$ checks on distinct guesses, the observer knows $p$ if one matches, and else picks from the $8 - k$ others, so $V_{\text{after}} = (k + 1)/8$ and the leakage is $\log_2 (k + 1)$ bits. After 7 checks the secret is known. This is why a login system limits the number of attempts: the policy "release the check result" is safe only together with a *when* or *how often* condition.

| checks $k$ | $V_{\text{after}}$ | leakage in bits |
|---|---|---|
| 0 | 1/8 | 0 |
| 1 | 2/8 | 1 |
| 3 | 4/8 | 2 |
| 7 | 8/8 | 3 |

**An average.** A program releases the average of the salaries $h_1, \dots, h_n$, with the escape hatch $(h_1 + \dots + h_n)/n$. The program "$h_2 := h_1$; ...; $h_n := h_1$; release the average" breaks delimited release: the value it releases is $h_1$, not the average of the initial salaries. Sabelfeld and Myers use this kind of example to show why the escape hatch is evaluated in the initial state.

## Where it is used

- **Languages.** Jif has a declassify construct checked against the authority of the owners in the decentralized label model. Many research languages add delimited release or robust declassification to their type systems.
- **Login and access checks.** The result of a password check is released, together with a limit on the number of attempts. Real systems also store only a hash of the password; see [password hashing](/password-hashing/).
- **Encryption.** A ciphertext computed from a secret is released, on the assumption that the key stays secret.
- **Statistics.** Aggregates such as averages and counts are released; how much they leak is measured by [quantitative information flow](/quantitative-information-flow/).
- **Termination.** [TINI](/termination-insensitive-noninterference/) can be seen as a declassification of the termination behaviour, a release that most type systems allow without saying so.

## References
