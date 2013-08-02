

drop database if exists duanlian;
create database duanlian character set = utf8 collate = utf8_bin;
use duanlian;


create table url
(
        urlid bigint unsigned not null auto_increment primary key,
        urlkey varchar(64) not null,
        url text not null,
        dt_created datetime not null,

        unique key (urlkey)
) character set = utf8 collate = utf8_bin;



