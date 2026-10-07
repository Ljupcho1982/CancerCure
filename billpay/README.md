# billpay — прототип (dry run)

Тек: `inbox → classifier (брз филтер) → extractor (LLM-замена) → guard (безбедносни проверки) → PaymentDraft`.
Ништо не се плаќа; резултатот е нацрт за рачно одобрување.

    python -m billpay            # демо со fixtures/inbox.json
    python -m unittest discover tests

Следно: `classifier.classify` → мал модел; `extractor.extract` → LLM со JSON излез (истите `guard` проверки);
Gmail читање (OAuth, read-only scope) наместо `load_inbox`; банкарска интеграција само по човечко одобрување.
