-- 1. Upsert Procedure (Insert or Update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Bulk Insert with Validation
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[], 
    p_phones VARCHAR[],
    INOUT p_errors TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        -- Simple check: phone must be digits only and at least 7 chars
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 7 THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            p_errors := array_append(p_errors, 'Invalid: ' || p_names[i] || ' (' || p_phones[i] || ')');
        END IF;
    END LOOP;
END;
$$;

-- 3. Delete Procedure (By name or phone)
CREATE OR REPLACE PROCEDURE delete_contact(p_search_term VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_search_term OR phone = p_search_term;
END;
$$;
