

drop database if exists duanlian;
create database duanlian character set = utf8 collate = utf8_bin;
use duanlian;


create table url
(
        urlkey char(24) not null,
        url text not null,
        dt_created datetime not null,

        primary key (urlkey)
) character set = utf8 collate = utf8_bin;

create table urlid
(
        urlid bigint unsigned not null auto_increment primary key
) character set = utf8 collate = utf8_bin;

create table urlstat_total
(
        urlkey char(24) not null,
        numpv bigint unsigned not null, -- 总访问次数
        dtlast datetime not null, -- 上次访问时间

        primary key (urlkey)
) character set = utf8 collate = utf8_bin;

create table urlstat_refer
(
        urlkey char(24) not null,
        refer char(64) not null,
        num bigint unsigned not null,

        primary key(urlkey, refer)
) character set = utf8 collate = utf8_bin;

create table urlstat_country
(
        urlkey char(24) not null,
        country char(64) not null,
        num bigint unsigned not null,

        primary key(urlkey, country)
) character set = utf8 collate = utf8_bin;

create table urlstat_browser
(
        urlkey char(24) not null,
        browser char(64) not null,
        num bigint unsigned not null,

        primary key(urlkey, browser)
) character set = utf8 collate = utf8_bin;

create table urlstat_os
(
        urlkey char(24) not null,
        os char(64) not null,
        num bigint unsigned not null,

        primary key(urlkey, os)
) character set = utf8 collate = utf8_bin;

