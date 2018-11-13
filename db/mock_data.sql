BEGIN;

INSERT INTO web_app_contact VALUES (1, 'Innopolis, Universitetskaya 1', '+7(800) 555-35-35', '', 'Vasiliy', 'Petrov', '', '') ON CONFLICT DO NOTHING;

ALTER TABLE web_app_userrole DISABLE TRIGGER ALL;
INSERT INTO web_app_userrole VALUES (1, 'CEO', 1) ON CONFLICT DO NOTHING;
ALTER TABLE web_app_userrole ENABLE TRIGGER ALL;

INSERT INTO web_app_contact VALUES (2, 'Innopolis, Sportivnaya 10', '+7(900) 666-35-35', '', 'Egor', 'Baba', '', '') ON CONFLICT DO NOTHING;
INSERT INTO web_app_acmecustomer VALUES(1, 2);

-- todo
-- INSERT INTO web_app_acmeorder VALUES (1, '1970-01-01T10:10:10', '', 10);

COMMIT;
