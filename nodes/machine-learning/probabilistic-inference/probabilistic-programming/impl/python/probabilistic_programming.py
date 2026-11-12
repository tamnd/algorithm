# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-programming/. The authors are listed in prov/KGYEAS.jsonl.

"""A small probabilistic programming language embedded in Python, with three generic engines.

A model is a Python function of one argument, ctx. It makes random choices with
ctx.sample(address, dist), adds evidence with ctx.observe(dist, value) or ctx.condition(test),
and returns a value. The address names the choice; it must be unique within one run, so a loop
uses addresses such as ("x", i). The model must be deterministic apart from these calls.

One run is a trace: the random choices by address, in the order of execution, the product of
the observed likelihoods, and the return value. The model defines the unnormalized density
P(trace) = (product of the prior probabilities of the choices) * (product of the likelihoods).

The engines work for every model and know nothing about it:
  enumerate_posterior   exact, by depth-first replay of prefixes of choices (finite models)
  likelihood_weighting  importance sampling with the prior as the proposal
  lmh                   single-site Metropolis-Hastings on traces (Wingate, Stuhlmueller and
                        Goodman 2011), which allows the set of choices to change between runs
"""

import random
from fractions import Fraction


# ---- Distributions with finite support ----

class Categorical:
    def __init__(self, values, probs):
        self.values = list(values)
        self.probs = list(probs)

    def support(self):
        return [v for v, p in zip(self.values, self.probs) if p > 0]

    def prob(self, value):
        return sum((p for v, p in zip(self.values, self.probs) if v == value), 0)

    def sample(self, rng: random.Random):
        return rng.choices(self.values, weights=[float(p) for p in self.probs])[0]


def flip(p):
    return Categorical([True, False], [p, 1 - p])


def uniform_draw(values):
    return Categorical(values, [Fraction(1, len(values))] * len(values))


# ---- Traces and the context that a model calls ----

def _product(xs):
    out = 1
    for x in xs:
        out = out * x
    return out


class Trace:
    def __init__(self):
        self.choices = {}  # address -> (dist, value), in the order of execution
        self.likelihood = 1
        self.value = None

    def prior(self):
        return _product(d.prob(v) for d, v in self.choices.values())

    def joint(self):
        """The unnormalized posterior density of the trace."""
        return self.prior() * self.likelihood

    def key(self):
        return tuple((a, v) for a, (_, v) in self.choices.items())


class Context:
    def __init__(self, choose):
        self.choose = choose
        self.trace = Trace()

    def sample(self, address, dist):
        if address in self.trace.choices:
            raise ValueError("the address %r is used twice in one run" % (address,))
        value = self.choose(address, dist)
        self.trace.choices[address] = (dist, value)
        return value

    def observe(self, dist, value):
        self.trace.likelihood = self.trace.likelihood * dist.prob(value)

    def condition(self, test):
        if not test:
            self.trace.likelihood = self.trace.likelihood * 0


def run(model, choose):
    """Run the model once. choose(address, dist) supplies the value of each random choice."""
    ctx = Context(choose)
    ctx.trace.value = model(ctx)
    return ctx.trace


def prior_chooser(rng: random.Random):
    return lambda address, dist: dist.sample(rng)


# ---- Engine 1: exact enumeration by replay ----

class _NeedChoice(Exception):
    def __init__(self, dist):
        super().__init__()
        self.dist = dist


def _replayer(prefix, before=None):
    """Return the values of prefix in order; at the first choice past the prefix, stop the run.
    before(address, dist) can supply a value first, as (True, value)."""
    pos = [0]

    def choose(address, dist):
        if before is not None:
            hit, value = before(address, dist)
            if hit:
                return value
        if pos[0] < len(prefix):
            pos[0] += 1
            return prefix[pos[0] - 1]
        raise _NeedChoice(dist)

    return choose


def enumerate_traces(model, before=None):
    """Yield every complete trace with a positive prior probability, once each. The model must
    stop on every path. A run that reaches a new choice is stopped, and one prefix for each
    value in the support goes on the stack."""
    stack = [[]]
    while stack:
        prefix = stack.pop()
        try:
            trace = run(model, _replayer(prefix, before))
        except _NeedChoice as need:
            for value in reversed(need.dist.support()):
                stack.append(prefix + [value])
            continue
        yield trace


def enumerate_posterior(model):
    """The exact posterior of the return value, and the evidence Z (the sum of P(trace))."""
    mass, z = {}, 0
    for trace in enumerate_traces(model):
        w = trace.joint()
        if w:
            mass[trace.value] = mass.get(trace.value, 0) + w
            z = z + w
    if z == 0:
        raise ValueError("the evidence has probability 0")
    return {v: w / z for v, w in mass.items()}, z


# ---- Engine 2: likelihood weighting ----

def likelihood_weighting(model, s, rng: random.Random):
    """s runs with every choice drawn from its prior; the weight of a run is its likelihood."""
    out = []
    for _ in range(s):
        trace = run(model, prior_chooser(rng))
        out.append((trace.value, trace.likelihood))
    return out


def weighted_posterior(samples):
    total = sum(w for _, w in samples)
    if total == 0:
        raise ValueError("every sample has weight 0")
    post = {}
    for v, w in samples:
        post[v] = post.get(v, 0) + w / total
    return post


def evidence_estimate(samples):
    """The mean weight, an unbiased estimate of Z."""
    return sum(w for _, w in samples) / len(samples)


# ---- Engine 3: lightweight Metropolis-Hastings on traces ----

def _proposal_chooser(old, site, new_value, fresh):
    """Run with site set to new_value, every other address of old reused, and the new
    addresses drawn by fresh."""
    def choose(address, dist):
        if address == site:
            return new_value
        if address in old.choices:
            return old.choices[address][1]
        return fresh(address, dist)
    return choose


def acceptance(old, new, site):
    """The MH acceptance probability of the move old -> new that redrew site from its prior.
    q(new | old) = (1 / |old|) * (product of the prior probabilities of the site and of the
    fresh choices of new); q(old | new) is the same with the stale choices of old."""
    p_new = new.joint()
    if p_new == 0:
        return 0
    fresh = _product(d.prob(v) for a, (d, v) in new.choices.items()
                     if a == site or a not in old.choices)
    stale = _product(d.prob(v) for a, (d, v) in old.choices.items()
                     if a == site or a not in new.choices)
    ratio = (p_new * len(old.choices) * stale) / (old.joint() * len(new.choices) * fresh)
    return min(1, ratio)


def lmh_step(model, trace, rng: random.Random):
    if not trace.choices:
        return trace
    site = rng.choice(list(trace.choices))
    dist = trace.choices[site][0]
    new = run(model, _proposal_chooser(trace, site, dist.sample(rng), prior_chooser(rng)))
    return new if rng.random() < acceptance(trace, new, site) else trace


def initial_trace(model, rng: random.Random, tries=100000):
    """A first trace with a positive density, by running the prior until one fits."""
    for _ in range(tries):
        trace = run(model, prior_chooser(rng))
        if trace.joint() > 0:
            return trace
    raise ValueError("no trace with a positive density found")


def lmh(model, steps, rng: random.Random, burn=0):
    """The return values of the chain after burn steps."""
    trace = initial_trace(model, rng)
    values = []
    for i in range(steps):
        trace = lmh_step(model, trace, rng)
        if i >= burn:
            values.append(trace.value)
    return values


def lmh_kernel_exact(model, trace, accept=acceptance):
    """The exact transition probabilities of lmh_step from trace: a dict from trace keys to
    probabilities, and a dict from keys to the traces. accept can be replaced to study a
    wrong acceptance rule."""
    n = len(trace.choices)
    out, traces = {}, {trace.key(): trace}
    stay = 0
    for site, (dist, _) in trace.choices.items():
        for value in dist.support():
            def before(address, d, site=site, value=value):
                if address == site:
                    return True, value
                if address in trace.choices:
                    return True, trace.choices[address][1]
                return False, None
            for new in enumerate_traces(model, before):
                fresh = _product(d.prob(v) for a, (d, v) in new.choices.items()
                                 if a not in trace.choices)
                p = Fraction(1, n) * dist.prob(value) * fresh
                a = accept(trace, new, site)
                out[new.key()] = out.get(new.key(), 0) + p * a
                traces[new.key()] = new
                stay = stay + p * (1 - a)
    out[trace.key()] = out.get(trace.key(), 0) + stay
    return out, traces


# ---- Models used on the page ----

def trick_coin(ctx):
    """A coin is a trick coin with probability 1/10, with the heads probability 4/5 or 1.
    Three heads are observed. Return whether the coin is a trick coin."""
    trick = ctx.sample("trick", flip(Fraction(1, 10)))
    if trick:
        p = ctx.sample("bias", uniform_draw([Fraction(4, 5), Fraction(1)]))
    else:
        p = Fraction(1, 2)
    for _ in range(3):
        ctx.observe(flip(p), True)
    return trick


def flips_until_heads(ctx, limit=4):
    """Flip a coin with P(heads) = 1/3 until heads, at most limit times. Condition on at least
    two flips. Return the number of flips. The number of choices is random."""
    n = 0
    while n < limit:
        n += 1
        if ctx.sample(("flip", n), flip(Fraction(1, 3))):
            break
    ctx.condition(n >= 2)
    return n


def sprinkler(ctx):
    """The sprinkler network of the likelihood weighting page, with C = 1 and W = 1 observed."""
    c = True
    ctx.observe(flip(Fraction(1, 2)), c)
    s = ctx.sample("S", flip(Fraction(1, 10) if c else Fraction(1, 2)))
    r = ctx.sample("R", flip(Fraction(4, 5) if c else Fraction(1, 5)))
    pw = {(False, False): Fraction(0), (False, True): Fraction(9, 10),
          (True, False): Fraction(9, 10), (True, True): Fraction(99, 100)}[(s, r)]
    ctx.observe(flip(pw), True)
    return r
