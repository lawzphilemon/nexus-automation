# Antislop core rules used by NEXUS (verbatim excerpt)

Source: miqdadbadjuber/anti-slop skills/antislop/SKILL.md. Only the rules that govern prose are copied. UI, layout, accessibility, mode-asking and asset rules are left out on purpose.

### C-5 — Evidence Over Claims

Anything presented as fact (testimonials, statistics, security claims) is real and verifiable, or it is not shown at all.

---

### Copywriting & Content

| Pattern | Telltale Signs |
|---------|---------------|
| **Em Dash (—)** | "Fast, secure — and built for developers." |
| **Generic CTAs** | Get Started, Learn More, Try Now, Explore, Discover |
| **AI Marketing Buzzwords** | AI Powered, Revolutionary, Next Generation, Seamless, Cutting Edge |
| **Fake Statistics** | 10K+ Users, 99.9% Uptime, 500M Requests, 120+ Countries |
| **Fake Testimonials** | AI avatars, random names, random job titles, fictional reviews |
| **Fabricated Trust Claims** | "SOC 2 compliant", "ISO 27001", "Enterprise-grade security", "300% faster" for a product with no such evidence |
| **Demo Without a Product** | Sells a product that is never shown working: no real demo, no Terms of Service, no Privacy Policy |

#### R-02 — Copywriting

- **FORBIDDEN**: em dash character (`—`) in any text
- Use comma (`,`), period (`.`), colon (`:`), or parentheses `()` instead
- Text must feel natural and human
- **Scope**: the ban governs text the agent writes. A user's own writing sample is a direction, not agent copy, so a sample that uses em dashes goes through R-37's conflict protocol: name the character, name the rule, ask. Never keep or cut them silently.
- **Carve-out**: documentation of this rule is exempt: the numbered section headings in this file (`R-XX — Title` rules and `C-1` to `C-5` principles), the em dash example in Part 1, the rule's own definition, any Delivery Gate item that quotes it, and the `Em Dashes` section in the copywriting skill (`skills/antislop-copywriting/SKILL.md`). These are documentation structure, not UI text.

#### R-15 — CTA (Call to Action)

- **FORBIDDEN**: "Get Started", "Learn More", "Try Now", "Explore", "Discover" as default CTAs
- CTAs must be **specific to the product context and the intended action**
- Better examples: "Start Your Free Trial", "Watch Live Demo", "Create Free Account"

#### R-16 — Copywriting & Buzzwords

- **FORBIDDEN**: "AI Powered", "Next Generation", "Revolutionary", "Seamless", "Cutting Edge", "Intelligent", "Ultimate", "Powerful", "Effortless"
- Use **specific language** that explains real benefits
- Show evidence, not claims

#### R-17 — Data & Numbers

- **FORBIDDEN**: numbers and statistics without a real source
- If real data is not available, display no numbers at all
- Empty is better than deceptive

#### R-18 — Testimonials

- **FORBIDDEN**: AI avatars, random names, random job titles, fictional reviews
- If you have no real testimonials, do not create a testimonials section
- Use social proof that can be verified

#### R-36 — No Fabricated Claims

- **FORBIDDEN**: inventing security, compliance, or performance claims ("SOC 2 compliant", "ISO 27001", "300% faster") without real evidence
- **FORBIDDEN**: fake testimonials, fake statistics, fake names (see R-17, R-18)
- If there is no real data, show no claim

#### R-38 — Real Content or Honest Placeholder

- Every claim, feature, testimonial, statistic, nav item, or visual element must come from real information OR be an explicitly labeled placeholder
- **FORBIDDEN**: fabricating content that looks realistic (fake testimonials, invented features, fake statistics, ghost links, fictional team or people)
- Placeholders are written as what they are: `[REAL DATA]`, "Coming soon", never disguised as final (see R-23)
- An empty section is better than a fabricated one
