# Illustration: a consultant selling time

### Scenario: independent tech consultant / SME

**Profile**
Alex is an independent systems & AI consultant. He doesn’t want a full booking platform, mailing list, or CRM. He just wants to say:

> "Here’s when I’m available. If you want my attention, pay for it."

ChronoLock lets Alex publish **three tiers of access** to the *same calendar*, priced by depth of engagement.

---

### 🟢 Bronze Tier: "Rubber Duck"

**USD $25 / 10 minutes**

**What you get**

* Quick clarification
* Sanity check on an idea
* "Am I crazy or is this plausible?"

**Constraints**

* Alex listens, responds briefly
* No prep, no follow-ups
* No screen-sharing

**Typical buyers**

* Engineers stuck on a decision
* Founders wanting a fast gut-check
* Someone who just needs to talk it out

**Mental model**

> *You’re paying for Alex's attention, not his full brain.*

---

### 🟡 Silver Tier: "Working Session"

**USD $120 / 30 minutes**

**What you get**

* Active problem-solving
* Whiteboarding or screen-share
* Direct answers based on experience

**Constraints**

* Alex is engaged, focused, present
* Limited prep, but real thinking
* One concrete outcome expected

**Typical buyers**

* Teams debugging an architecture choice
* Product leads validating a direction
* SMEs who want an expert in the room

**Mental model**

> *You're renting Alex's expertise for a bounded slice of time.*

---

### 🔴 Gold Tier: "Deep Consult"

**USD $400 / 60 minutes**

**What you get**

* Full attention
* Context-switching beforehand
* Strategic advice, not just answers

**Constraints**

* Alex reviews materials in advance
* May include follow-up notes
* Slot density is intentionally low

**Typical buyers**

* Execs making high-stakes decisions
* Companies paying to avoid a mistake
* Situations where being wrong is expensive

**Mental model**

> *You’re buying judgment, not minutes.*

---

### What ChronoLock does behind the scenes

1. Alex advertises availability once, directly from his calendar
2. Each tier maps to:

   * slot length
   * price
   * booking rules
3. A client selects a tier and a time
4. ChronoLock places a **temporary hold**
5. x402 settles payment
6. The hold atomically converts into a confirmed event

No back-and-forth, invoices, payment disputes, or "are you free Tuesday?"
