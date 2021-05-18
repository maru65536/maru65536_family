drop database if exists app_development;
create database app_development;

use app_development;

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