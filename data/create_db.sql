/* database creation script*/

drop table if exists news;
drop table if exists member;

/* create tables*/
create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

insert into member( name, email, password, authorisation)
values('David', 'david@nzhandball.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values('Rowan', 'rowan@nzhandball.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values('Joyce', 'joyce@marsden.com', 'temp', 1 );
insert into member( name, email, password, authorisation)
values('Amelia', 'amelia@qmc.com', 'temp', 1 );

insert into news(title, subtitle, content, newsdate, member_id)
values('Amazing news for the U19 NZ Men''s team',
      'The U19 NZ Men''s handball team make it through to compete in the world championship in August.',
      'They made the cut after placing 2nd in the Oceania Championship that took place in December 2022.' || char(10) ||
      'If you want to help support the team, donations would be appreciated',
      '2023-06-22 15:38:00',
      (select member_id from member where name='David' )
      );


insert into news(title, subtitle, content, newsdate, member_id)
values('NZ Beach Handball Womens Team Selection 2023',
      'Following is the NZ Beach Handball team that will be representing NZ in the Oceania Championships',
      'Lily Smith' || char(10) ||
      'We wish this team good luck as they head to the Gold Coast, Australia to compete in the Oceania Championships.',
      '2023-06-15 11:23:00',
      (select member_id from member where name='Rowan' )
      );