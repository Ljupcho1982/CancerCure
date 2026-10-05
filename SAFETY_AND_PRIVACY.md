# CancerCompanion Safety and Privacy

> **Status: draft v0.1.** This document describes how CancerCompanion handles
> safety and privacy today, and the rules any future change must follow. It
> supports the [Ethics Charter](ETHICS_CHARTER.md). It is not medical or legal
> advice, and clinicians and a privacy professional should review it before it
> is treated as final.

## 1. What the app is, and is not

CancerCompanion is a free, no-install web app that helps people with cancer and
their support circle keep a symptom log, a medication checklist, appointments
with questions to ask, and a list of tasks for friends and family.

It is **not** a medical device. It does not diagnose, treat, interpret results,
recommend treatments or doses, or predict outcomes. It is not an emergency
service.

## 2. Privacy: how it works today

| Question | Answer |
|---|---|
| Where is data stored? | Only in the user's own browser (`localStorage`). |
| Is there a server or account? | No. |
| Is anything sent anywhere? | No. The app makes no network requests of its own. The page and scripts are loaded from GitHub Pages, and nothing the user enters leaves their device. |
| Analytics, cookies, trackers, ads? | None. |
| Third-party scripts, fonts or embeds? | None. |
| Who can see the data? | Anyone with access to that browser profile on that device. |

The language choice is also stored locally.

### What is stored
Symptoms (name, severity, date, notes), medications (name, dose, daily
checkmarks), appointments (who, when, questions), support-circle tasks, and the
selected language. This is sensitive health information.

### User control
- **Export backup** downloads a JSON file the user owns.
- **Import backup** restores from such a file.
- **Print summary** produces a printout for a clinician.
- **Delete all data** wipes everything stored by the app (after confirmation).
  Clearing the browser's site data does the same.

### Limits users should know about
These are honest limits, and the app should say them in plain language.
- **Shared or public devices.** Anyone who uses the same browser profile can open
  the app and see the data. People should avoid using it on shared computers or
  should delete data afterward.
- **No encryption at rest by the app.** Browser storage is not encrypted by
  CancerCompanion. Device-level protection (screen lock, disk encryption) is the
  user's protection.
- **No automatic backup.** Clearing browser data, switching browsers or losing a
  device loses the data unless the user exported a backup.
- **Backup files are not encrypted.** A downloaded file can be read by anyone
  who gets it. Treat it like a medical record. The same applies to printouts and
  to anything shared with friends and family.
- **Private browsing** may not keep data between sessions.

### Rules for any future change to data handling
1. **No server, accounts, analytics or third-party services** until this document
   and the Ethics Charter have been updated first and the change has been
   reviewed.
2. **Minimum data.** Collect only what a feature needs, and say why.
3. **Explicit, separate, revocable opt-in** for anything beyond providing the
   service, including analytics, research and model training. Saying no never
   reduces the service.
4. **Never sell or share health data.** No advertisers, brokers, insurers or
   employers.
5. **Real deletion.** If data ever leaves the device, users must be able to
   export and delete it completely, including backups on a stated schedule.
6. **Encryption** in transit and at rest, strict access controls and access
   logging for any stored server-side data.
7. **Legal compliance** with the rules that apply to the users served (for
   example GDPR, and HIPAA where relevant), confirmed by a professional before
   launch in a region.
8. **Children and people who may lack capacity** need parental or guardian
   involvement and age-appropriate content.
9. **Breach plan.** If personal data is ever exposed, notify affected people
   promptly and plainly, and report to regulators where required.

## 3. Safety: what the app does today

### Urgent symptoms warning
The app shows a standing message telling users that severe symptoms (fever
during chemotherapy, trouble breathing, uncontrolled pain or vomiting) need a
call to their care team or emergency services right away.

### Known gaps
We list these openly so they get fixed.
- The warning is static. The symptom log does **not** react to what a user
  enters, for example a high severity score. It does not tell a user a symptom
  is or is not serious.
- The warning does not give country-specific emergency or crisis numbers.
- There is no crisis or self-harm support information in the app yet.
- Translations, including the safety warning, have not yet been reviewed by
  clinicians or native speakers.

## 4. Safety rules for future features

### Never
- Say or imply that a symptom is "nothing to worry about", or that a user does
  not need to contact their care team.
- Interpret test results, scans or pathology as a diagnosis.
- Recommend, rank or change treatments, drugs or doses.
- Predict an individual's survival, response or prognosis.
- Promote unproven cures, supplements or paid products.
- Present itself as a clinician, therapist or human.

### Urgent-symptom escalation
- Escalation uses **fixed, rule-based logic** that does not depend on an AI model.
- Rules are written and reviewed by oncology clinicians, such as oncology nurses
  and doctors, before use.
- When a rule fires, the message is short, calm and clear: contact the care team
  or emergency services now, with the right local numbers shown.
- Rules **err on the side of escalating.** A false alarm is better than a missed
  emergency.
- Each region and language needs localized emergency numbers and clinician-
  reviewed wording before it launches.

Starting list for clinician review (not final, and not a substitute for a
treating team's instructions):
- Fever or chills during cancer treatment
- Difficulty breathing or chest pain
- Uncontrolled bleeding
- Severe or uncontrolled pain
- Persistent vomiting, or inability to keep fluids or medicines down
- Sudden confusion, severe weakness, fainting
- Signs of a severe allergic reaction
- Any symptom the user's own care team told them to report immediately

### Crisis and self-harm
- Show supportive, non-judgmental text and local crisis lines, and encourage
  contacting a trusted person or health professional.
- Never argue, minimize or give instructions that could be harmful.
- Crisis wording and resources are reviewed by mental-health and palliative-care
  professionals and checked for each country.

### If AI or an LLM is ever added
All of the above still applies, plus:
1. **Disclose** clearly that the user is talking to an AI, and what it can and
   cannot do.
2. **Grounded answers.** Medical facts come from vetted sources (for example
   national cancer institutes and patient-guideline organizations) and are cited.
   If sources do not cover a question, the answer is to ask the care team.
3. **Safe failure.** When unsure, defer or escalate. Never guess.
4. **Escalation outside the model.** Red-flag and crisis detection run as
   separate, tested checks, not only as instructions to the model.
5. **No training on conversations** without separate opt-in consent, and never
   on data from people who did not consent.
6. **Evaluate before release** with clinicians and patient advocates using
   realistic scenarios, including emotional and edge cases, and re-evaluate
   before any model, prompt or source change.
7. **Human review** of sampled and flagged conversations (with privacy
   protections), and a simple way for users to say "this felt wrong."
8. **Bias testing** across languages, dialects, ages, genders and literacy
   levels, with results published and gaps fixed before launch in that language.

## 5. Security basics

- Escape or sanitize every value from user input or imported files before
  showing it. Avoid inserting raw HTML.
- Imported backups and saved data are rebuilt field by field (`sanitize` in
  `src/app.js`): unknown fields are dropped, types are enforced, severity is
  clamped to 0–10, and file size and item counts are limited. Keep this in step
  with any new field.
- Keep the site free of third-party scripts. If one is ever added, review it
  first, pin versions and consider Subresource Integrity.
- Serve over HTTPS only (GitHub Pages does this).
- Keep dependencies minimal and updated. Run a security review for each
  release that changes data handling.
- Report vulnerabilities privately (add a contact or GitHub private
  vulnerability reporting before wider promotion).

## 6. Accessibility and equity

- Support screen readers, keyboard use, large text and high contrast.
- Use plain language and short sentences, suited to someone under stress.
- Work on low bandwidth and older devices, and keep the app usable offline.
- Add languages with native speakers and clinicians reviewing safety-critical
  text, and say clearly when a translation is not yet reviewed.

## 7. Incidents and reporting

- Provide a way for anyone to report a safety or privacy problem, with a stated
  response time. *(To do: set up a contact address or GitHub issue template.)*
- If harm or a near-miss occurs: stop the harm, support the person, fix the
  cause, add a regression test, and record what happened and what changed.
- Disclose honestly, including mistakes.

## 8. Before launching in a new region or language

- [ ] Local oncology clinicians reviewed the safety wording and escalation rules
- [ ] Correct local emergency and crisis numbers added and checked
- [ ] Native-speaker review of all text, especially safety messages
- [ ] Legal and privacy requirements checked for that region
- [ ] Community or patient group consulted
- [ ] Accessibility checked

## 9. Open items

- [ ] Add country-aware emergency and crisis information
- [ ] Clinician review of the urgent-symptom list and wording
- [ ] Gentle, rule-based prompt when a high-severity symptom is logged
- [x] Validate and escape imported data
- [ ] Plain-language privacy notice shown in the app
- [ ] Optional passcode or encryption for local data and backups
- [ ] Vulnerability reporting channel
- [ ] Accessibility audit

## Version history

- v0.1 — initial draft.
