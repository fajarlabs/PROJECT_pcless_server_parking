-- Table: public.ticket_log

-- DROP TABLE public.ticket_log;

CREATE TABLE public.ticket_log
(
    id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    image character varying(50) COLLATE pg_catalog."default",
    in_gate timestamp without time zone DEFAULT now(),
    out_gate timestamp without time zone,
    CONSTRAINT ticket_log_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ticket_log
    OWNER to postgres;