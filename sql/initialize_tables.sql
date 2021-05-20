drop database if exists family_development;
create database family_development;

use family_development;

drop table if exists family;
create table family (
  id          varchar(40),
  is_using    boolean,
  main_id     varchar(40),
  atcoder_id  varchar(40),
  rating      int,
  is_hidden   boolean,
  rate_hidden boolean,
  comment     varchar(280),
  birthday    date
);

drop table if exists youbo;
create table youbo (
  IP         varchar(15),
  content    text,
  created_at timestamp
);
