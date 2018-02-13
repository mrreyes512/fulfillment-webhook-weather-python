CREATE TABLE public.example_table
(
    ticket_id   integer PRIMARY KEY,
    last_name   text ,
    first_name  text NOT NULL,
    tech_id     integer,
    issue_type  text NOT NULL,
    issue_details  text,
    callback_method   text NOT NULL,
    callback_details  text,
    que_notes   text
);

INSERT INTO public.example_table
  (
    ticket_id,first_name,last_name,tech_id,issue_type,issue_details,callback_method,callback_details,que_notes
  )
VALUES
  (
    1,'Mark','Reyes',423,'testing','I''m testing','phone','512 485 5555',NULL
  ),
  (
    2,'Sandra','Reyes',324,'port turnup','gotta turn up a port','phone','512 485 2222',NULL
  ),
  (
    3,'Aidan','Reyes',73839,'cpe config issues','i''m missing my config','email','tech.name@charter.com',NULL
  ),
  (
    4,'Olivia','Reyes',8882,'firmeware upgrade','upgrade me','phone','316 987 0901',NULL
  ),
  (
    5,'Sqoop','Reyes',6543,'other','i''m not too sure','phone','316 987 0901',NULL
  );
