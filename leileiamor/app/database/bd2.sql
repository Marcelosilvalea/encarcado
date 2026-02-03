--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2026-02-03 08:33:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4882 (class 0 OID 16416)
-- Dependencies: 222
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categoria (id_categoria, nome, tipo, id_usuario) FROM stdin;
\.


--
-- TOC entry 4880 (class 0 OID 16401)
-- Dependencies: 220
-- Data for Name: conta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.conta (id_conta, nome, saldo, tipo, id_usuario) FROM stdin;
\.


--
-- TOC entry 4884 (class 0 OID 16431)
-- Dependencies: 224
-- Data for Name: transacao; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.transacao (id_transacao, valor, data, descricao, tipo, id_usuario, id_conta, id_categoria) FROM stdin;
\.


--
-- TOC entry 4878 (class 0 OID 16390)
-- Dependencies: 218
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuario (id_usuario, nome, email, senha) FROM stdin;
\.


--
-- TOC entry 4894 (class 0 OID 0)
-- Dependencies: 221
-- Name: categoria_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categoria_id_categoria_seq', 1, false);


--
-- TOC entry 4895 (class 0 OID 0)
-- Dependencies: 219
-- Name: conta_id_conta_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.conta_id_conta_seq', 1, false);


--
-- TOC entry 4896 (class 0 OID 0)
-- Dependencies: 223
-- Name: transacao_id_transacao_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.transacao_id_transacao_seq', 1, false);


--
-- TOC entry 4897 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 1, false);


-- Completed on 2026-02-03 08:33:56

--
-- PostgreSQL database dump complete
--

