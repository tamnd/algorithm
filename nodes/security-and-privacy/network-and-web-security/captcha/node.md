---
tag: 2BBR5Y
kind: concept
slug: captcha
name: CAPTCHA
aliases:
- completely automated public Turing test
area: security-and-privacy/network-and-web-security
level: core
summary: "A test that humans pass and current programs fail, used to keep bots from creating accounts or sending spam."
history:
  year: 2003
  people: [Luis von Ahn, Manuel Blum, Nicholas J. Hopper, John Langford]
  note: "Von Ahn, Blum, Hopper and Langford named the CAPTCHA and gave its formal definition and the link to hard AI problems at EUROCRYPT 2003. Von Ahn and others turned the solving effort into book digitization with reCAPTCHA in 2008."
prereqs: [binomial-distribution]
see_also: [geometric-distribution, token-bucket, honeywords, expected-value, intrusion-detection-problem, misuse-detection]
sources:
  - url: "https://iacr.org/archive/eurocrypt2003/26560294/26560294.pdf"
    title: "Luis von Ahn, Manuel Blum, Nicholas J. Hopper and John Langford, CAPTCHA, using hard AI problems for security, EUROCRYPT 2003, LNCS 2656, pages 294 to 311"
    locator: "the definitions of a test that is (alpha, beta)-human executable, of an AI problem and of a (delta, tau)-hard AI problem, the definition of an (alpha, beta, eta)-CAPTCHA, the hardness assumption, and the argument that a break of a CAPTCHA solves an AI problem"
  - paper: "Luis von Ahn, Benjamin Maurer, Colin McMillen, David Abraham and Manuel Blum, reCAPTCHA, human-based character recognition via web security measures, Science 321(5895), 2008, pages 1465 to 1468"
    locator: "the pair of a control word with a known answer and an unknown word from scanned text, and the use of the answers to transcribe books"
---

A CAPTCHA, a Completely Automated Public Turing test to tell Computers and Humans Apart, is a test that a program can generate and grade, that most humans pass, and that current programs fail. Sites use it to slow down automated abuse, such as mass sign-ups, comment spam and the guessing of passwords. Von Ahn, Blum, Hopper and Langford (2003) gave the formal definition. A CAPTCHA is built on an AI problem, such as reading distorted text, for which no known program does well. The test is public: the code and the data that make the challenges are known, and only the random choices of each challenge are secret. They showed a win-win property: a program that passes the test with good probability also solves the underlying AI problem, so either the test is secure or AI has made progress. In practice, programs did learn to read most distorted text, and people paid to solve challenges defeat any CAPTCHA, so today it is a cost on abuse and not a proof that a client is human.

## In plain words

Some web forms show a picture of bent, noisy letters and ask you to type them. A person can read them with a little effort, but for a long time programs could not. This kind of test is called a CAPTCHA.

The site uses it to make life harder for programs that try to create many accounts or post spam. The site makes a new puzzle each time and knows the answer, so it can check you at once. The idea is that a machine that passes the test has learned to do something that only people could do before.

Programs have since learned to read most such pictures, and some people are paid to solve puzzles for others. So the test now only adds cost and delay for misuse. It also makes sites harder to use for people who cannot see or hear well.

## The idea

**The definitions of von Ahn et al.** A test $V$ is $(\alpha, \beta)$-human executable if at least a fraction $\alpha$ of the human population passes $V$ with probability greater than $\beta$. An AI problem is a triple $P = (S, D, f)$, where $S$ is a set of instances, $D$ is a probability distribution on $S$, and $f$ maps each instance to its answer. A program $A$ $\delta$-solves $P$ if $\Pr_{x \sim D}[A(x) = f(x)] \ge \delta$. The problem is $(\delta, \tau)$-hard if, by the state of the art, no program that runs in time $\tau$ is known to $\delta$-solve it. An $(\alpha, \beta, \eta)$-CAPTCHA is a test $V$ that is $(\alpha, \beta)$-human executable, such that any program that passes $V$ with probability greater than $\eta$ can be used to solve a hard AI problem.

**The hardness assumption.** The security is not a proof from a number-theory assumption. It rests on the assumption that the community has tried hard to solve the AI problem and failed. If a program does break the test, the problem is no longer hard and the test must change, but the break is useful progress on the AI problem. The authors called this a win-win.

**Public and automated.** The program that makes and grades the challenges is public, as in [Kerckhoffs' principle](/kerckhoffs-principle/) for ciphers. Each challenge draws a fresh random instance $x \sim D$, and the server keeps $f(x)$ to grade the reply. A test that depends on a secret set of images is not a CAPTCHA in this sense, because the secret can leak.

**Kinds of tests.**

| kind | the task for the user | the AI problem behind it |
| --- | --- | --- |
| distorted text | type the letters of a warped, noisy image | reading text under distortion |
| image choice | pick the images that show a named object | object recognition |
| audio | type the words of a noisy recording | speech recognition in noise |
| behavior score | no puzzle; the service scores the session from how it behaves | telling human use from scripted use |

The last kind is not a test in the strict sense of the definition: it is a risk score with a threshold, and its errors are those of an [intrusion detector](/intrusion-detection-problem/).

**Limits.** A CAPTCHA tells a human from a program, not an honest user from an abuser. Paid human solvers relay challenges to people and pass them at low cost. Research programs read many distorted-text tests: Mori and Malik (2003) read most challenges of an early distorted-text test with shape matching, and later learning methods read most others. Each test also excludes some honest users, for example people with low vision for image tests, so a site needs another way in, such as an audio test, which has its own weaknesses.

## Examples

**The number of challenges.** A test shows 4 characters from an alphabet of 32. There are $32^4 = 1{,}048{,}576$ answers, so a blind guess passes with probability about $10^{-6}$. That is not the limit on security. A program that reads each character right with probability $0.3$, independently, passes with probability $0.3^4 = 0.0081$, or about 1 in 123.

**Humans against programs.** A test asks for two words. A human reads each word right with probability $0.9$, so passes with $0.9^2 = 0.81$. A program reads each word with probability $0.3$, so passes with $0.3^2 = 0.09$. The number of tries until the program first passes follows a [geometric distribution](/geometric-distribution/) with mean $1/0.09 \approx 11.1$. In 100 tries, the number of passes follows a [binomial distribution](/binomial-distribution/) with mean $9$. So the test does not stop the program; it makes each account cost about 11 challenges. If the site also limits each client to a few challenges per hour with a [token bucket](/token-bucket/), the cost grows to hours.

**reCAPTCHA.** Each challenge shows two words. One, the control word, has a known answer. The other comes from a scanned book where text recognition failed, and its answer is unknown. If the user types the control word right, the system counts the answer for the unknown word as a vote, and when enough users agree, the word is taken as read. So the human effort spent on the test also does useful work. The control word grades the user; the unknown word is not graded.

## Where it is used

- **Sign-up and login forms.** A CAPTCHA after several failed logins slows online password guessing, together with rate limits and lockouts.
- **Comment and contact forms.** Sites use it to cut automated spam, often only for clients that look risky.
- **Ticket and stock sales.** Sites that sell scarce items use it to slow scripts that buy in bulk.
- **Digitization of text.** reCAPTCHA used the answers to transcribe scanned books and newspapers.
- **Research on AI.** Each widely used test is a benchmark, and its breaks track progress in text, image and speech recognition, as the win-win argument predicted.

## References
