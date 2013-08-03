

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


