CREATE TABLE public.test_table
(
    ticket_id   integer integer PRIMARY KEY,
    last_name   text ,
    first_name  text NOT NULL,
    tech_id     integer,
    issue_type  text NOT NULL,
    customer_details  text,
    callback_method   text NOT NULL,
    callback_details  text,
    que_notes   text
)
