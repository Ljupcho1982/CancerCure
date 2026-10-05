# CancerCompanion Ethics Charter

> **Status: draft v0.1.** This charter is meant to be reviewed and changed by
> patients, caregivers and clinicians before it is treated as final. Nothing here
> is legal or medical advice.

## Mission

CancerCompanion is a free, honest, privacy-respecting companion that helps people
with cancer and their families keep track of their care, prepare for
conversations with their care team, and feel less alone. It always points toward
real human help.

It does not diagnose, treat, predict outcomes, or promise cures.

## Principles

1. **Patient first.** Every feature must help someone feel safer, better
   informed or less alone. If it serves growth, money or novelty instead, we
   leave it out.
2. **Support, not replacement.** CancerCompanion never replaces a doctor, nurse,
   counselor or loved one. It helps people use those relationships better.
3. **Honesty with compassion.** We do not lie, overstate or give false hope. We
   also do not deliver hard information coldly or without being asked.
4. **Dignity and autonomy.** People decide how much they want to know, what they
   record, and what they share. Their data is theirs.
5. **Free at the point of need.** Core features are never paywalled.
6. **Equity.** The people with the least access to oncology care are the people
   we most want to serve.
7. **Humility.** We expect to be wrong. We listen, publish our mistakes and fix
   them.

## Red lines (we will never)

- Sell, rent or share personal health data, or use it for advertising, profiling,
  or decisions about insurance or employment.
- Recommend a specific treatment, drug, dose change or clinical trial as a
  personal medical recommendation, or predict an individual's survival or
  prognosis.
- Promote unproven cures, supplements, products or paid services.
- Pretend to be a human, a clinician or a therapist.
- Use manipulative design: streaks, guilt notifications, fake urgency, or
  anything built to maximize time spent or dependence.
- Leave a person in crisis without a clear route to human help.
- Launch in a new language or region without review by local clinicians and
  community members.
- Accept funding or partnerships that would require breaking any of the above.

## What we commit to

### Honesty about what this is
- The app states plainly that it is not medical advice and cannot diagnose or
  treat anything.
- If AI is ever used, the app says so clearly and explains what it can and
  cannot do. It never claims to feel, or to be something it is not.
- When it does not know, it says so and points to the person's care team.

### Respect for the person
- Users control how much detail they see. Nothing hard is pushed on someone who
  has not asked.
- Language is plain, calm and respectful of culture, faith and family decision-
  making norms, while keeping safety-critical facts accurate.
- Features for advanced illness, palliative care and grief are designed with
  palliative-care professionals and with patients and families, not for them.

### Privacy and data
- **Today:** all data stays in the user's browser (`localStorage`). There is no
  server, no account and no tracking.
- Collect the minimum. If a server is ever introduced, this charter must be
  updated first and the change must be reviewed under "Changing this charter".
- Any use of data beyond providing the service, including analytics, research
  or model training, needs separate, plain-language, revocable opt-in. Saying no
  never reduces the service.
- Users can export and delete everything, easily and completely.
- Extra care for minors and for people who may lack capacity to consent.

### Safety
- Anything that could involve urgent symptoms (for example fever during
  treatment, bleeding, breathing difficulty, severe pain) or thoughts of
  self-harm must have a clear, rule-based path to emergency or crisis help
  localized to the user's country. It must not depend on an AI model's judgment.
- If AI is added, answers on medical facts must come from vetted sources and be
  cited. When sources do not cover a question, the answer is to ask the care
  team. The default failure mode is to defer or escalate, never to guess.
- Safety features are tested before every release, and every incident adds a
  regression test.

### Equity and accessibility
- Languages are chosen with the communities who use them, and translations are
  reviewed by native speakers and clinicians.
- Support low bandwidth, older devices and offline use where possible.
- Meet accessibility needs: screen readers, large text, plain language and
  cognitive accessibility.
- Measure outcomes by group. A disparity is treated as a bug.

### Independence and money
- Prefer a non-profit or public-benefit structure that legally locks in this
  charter.
- Disclose all funders publicly. No single funder, especially pharmaceutical
  companies or insurers, may steer the product.
- If the project winds down, user data is deleted and any assets go to a
  mission-aligned non-profit.

## Governance

- **Advisory board.** Patients, caregivers, oncology and palliative-care
  clinicians, an ethicist, a privacy expert, and someone representing a
  marginalized community. The board has the authority to pause a feature or the
  product. Founders cannot override that silently.
- **Ethics review before building.** Any major feature is reviewed against this
  charter before development starts, not after release.
- **Independent audits.** Safety, bias and security audits at least yearly,
  with results published.
- **Public decision log.** Significant ethical decisions and their reasons are
  recorded in the repository.
- **Whistleblowing.** Anyone on the team can raise a concern without penalty.

## Accountability

- **Measure what matters:** patient understanding, distress, preparedness for
  appointments and caregiver burden, not engagement or time in app.
- **Track harms:** incorrect information, missed escalations, complaints and
  near-misses.
- **Publish results,** including failures, and share evaluation methods openly.
- **Research ethics.** Any study using user data requires independent ethics
  review and informed consent.
- **Harm reporting.** Provide a channel anyone can use, with a stated response
  time.
- **Incident response.** If harm occurs: stop the harm, support the person,
  disclose honestly, fix the cause, and record what we learned.

## Test for every feature

1. Would a patient be glad they used it?
2. Would their oncologist be comfortable with it?
3. Would we be comfortable if everything about it were public, including how it
   uses data and how it is funded?

If any answer is no, change it or drop it.

## Open questions we have not resolved

These are real tensions. They need patients and clinicians in the room, case by
case.

- How much hard truth to share with someone who has not asked.
- How much emotional closeness from a tool is healthy.
- What to do when a person wants something the evidence does not support.
- How to serve people in regions where local clinical review is hard to get.

## Changing this charter

Changes are proposed in a pull request, reviewed by the advisory board once it
exists, and recorded in the decision log. Changes may strengthen protections
freely. Weakening a red line requires the board's explicit approval and a public
explanation.

## Version history

- v0.1 — initial draft.
