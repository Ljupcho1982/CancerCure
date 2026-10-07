# billpay — прототип (dry run)

Тек: `inbox → classifier (брз филтер) → extractor (LLM-замена) → guard (безбедносни проверки) → PaymentDraft`.
Ништо не се плаќа; резултатот е нацрт за рачно одобрување.

    python -m billpay            # демо со fixtures/inbox.json
    python -m unittest discover tests

Следно: `classifier.classify` → мал модел; `extractor.extract` → LLM со JSON излез (истите `guard` проверки);
Gmail читање (OAuth, read-only scope) наместо `load_inbox`; банкарска интеграција само по човечко одобрување.

## Ollama (локален модел, без Claude API)

    ollama pull qwen2.5:7b
    BILLPAY_BACKEND=ollama BILLPAY_MODEL=qwen2.5:7b python -m billpay

`OLLAMA_HOST` (default `http://localhost:11434`). Невалиден излез од моделот → `BLOCKED`; `guard` останува иста.

## Веб демо

`billpay/demo/index.html` — самостојна страница (отвори ја во прелистувач или преку GitHub Pages: `/billpay-demo/`).
Истиот тек во JS, уредлив сандаче/поставки, копче „Одобри“ е само симулација. Опционално користи локален Ollama.
Тест: `node billpay/tests/pipeline.test.js`.

## Gmail (read-only)

    pip install -r requirements.txt
    python -m billpay --gmail

Еднаш: Google Cloud Console → нов проект → овозможи Gmail API → OAuth consent screen (External, додади се како test user) →
Credentials → OAuth client ID (Desktop app) → симни JSON како `billpay/credentials.json`.
Првото стартување отвора прелистувач за одобрување; токенот се чува во `billpay/token.json` (двете се во `.gitignore`).

- Scope е само `gmail.readonly`: кодот не може да испраќа, брише или менува пошта. Мејловите се чуваат само во меморија.
- Пребарување по default: `newer_than:30d (сметка OR фактура OR invoice OR bill)` (`DEFAULT_QUERY`).
- Ако Gmail јави SPF/DKIM грешка за испраќачот, нацртот е `BLOCKED` (заштита од лажен испраќач).
- Не се читаат прилози (PDF сметки) засега.
