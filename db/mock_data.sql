BEGIN;

INSERT INTO web_app_contact VALUES (1, 'Innopolis, Universitetskaya 1', '+7(800) 555-35-35', '', 'Vasiliy', 'Petrov', '', '') ON CONFLICT DO NOTHING;

ALTER TABLE web_app_userrole DISABLE TRIGGER ALL;
INSERT INTO web_app_userrole VALUES (1, 'CEO', 1) ON CONFLICT DO NOTHING;
ALTER TABLE web_app_userrole ENABLE TRIGGER ALL;

COMMIT;
