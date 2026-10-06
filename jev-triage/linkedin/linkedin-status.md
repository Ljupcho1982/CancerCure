# LinkedIn статус (македонски)

⚡ Направив прототип на **Јев**, мал и брз модел за „System 1“ одлучување, применет на тријаж на мејлови.

Идејата е едноставна: не секоја одлука бара длабоко размислување. За мејл од типот „production is down“ или „победи на лотарија“ не ми треба бавен модел, ми треба брз одговор.

За секој мејл Јев враќа:
🔹 категорија (хитно, одговори денес, рутинско, информативно, спам)
🔹 предложена акција
🔹 сигурност во проценти
🔹 причина во една реченица

Најважниот дел е ескалацијата. Кога сигурноста е под прагот (80%), Јев не погодува: мејлот оди во „За човек“. Тој само предлага, никогаш не брише и не праќа сам. Ако му кажам дека погрешил, поправката му се враќа како пример.

Тоа е целата идеја на System 1 + System 2: брзо кога е јасно, внимателно кога не е.

Ова е демо прототип. Без API-клуч тријажата е симулирана со правила во прелистувачот, а со клуч користи Claude модел. Градено со Claude Code.

Што би додале вие во еден таков тријаж? 👇

#AI #LLM #Productivity #Email #Automation #ClaudeCode

---

# LinkedIn status (English)

⚡ I built a prototype of **Jev**, a small, fast "System 1" decision model, applied to email triage.

Not every decision needs deep reasoning. For "production is down" or "you won the lottery", I don't need a slow model, I need a fast answer.

For each email Jev returns a category, a suggested action, a confidence score and a one-line reason.

The key part is escalation: below the confidence threshold (80%) Jev doesn't guess, it routes the email to a human. It only suggests; it never deletes or sends anything. Corrections are fed back as examples.

Fast when it's clear, careful when it's not.

This is a demo prototype: without an API key triage is simulated with rules in the browser; with a key it uses a Claude model. Built with Claude Code.

What would you add to an email triage like this? 👇

#AI #LLM #Productivity #Automation #ClaudeCode

---

Слика: `jev-linkedin.png` (1200×627, 2x, погодна за LinkedIn објава). Чист скриншот на апликацијата: `jev-app-screenshot.png`.
