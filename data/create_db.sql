/* database creation script*/
drop table if exists news;
drop table if exists member;
drop table if exists draw;
drop table if exists results;


/* create tables*/
/* member table */
create table member(
    member_id integer primary key autoincrement not null,
    firstname text not null,
    secondname text not null,
    username text not null unique,
    password text not null,
    authorisation integer not null
);

/* news table */
create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

/* draw table */
create table draw(
    draw_id integer primary key autoincrement not null,
    gamedate date not null,
    teamone text not null,
    teamtwo text not null,
    location text not null,
    gametime integer not null
);

/* results table */
create table results(
result_id integer primary key autoincrement not null,
gamedate date not null,
teamone text not null,
teamtwo text not null,
teamonescore integer not null,
teamtwoscore integer not null,
winner text not null
);


/* inserting information into the member table */
insert into member(firstname, secondname, username, password, authorisation)
values('Paul', 'Smith', 'paulsmith','temp', 0 );
insert into member(firstname, secondname, username, password, authorisation)
values('Jess', 'Door','JessDoor', 'temp', 0 );
insert into member(firstname, secondname, username, password, authorisation)
values('Joyce', 'Chan', 'JoyceChan', 'temp', 1 );
insert into member(firstname, secondname, username, password, authorisation)
values('Amelia','Rodd','AmeliaRodd', 'temp', 1 );


/* inserting information into the news table */
insert into news(title, subtitle, content, newsdate, member_id)
values('Amazing news for the U19 NZ Men''s team',
      'The U19 NZ Men''s handball team make it through to compete in the world championship in August.',
      'They made the cut after placing 2nd in the Oceania Championship that took place in December 2022.' || char(10) ||
      'If you want to help support the team, donations would be appreciated',
      '2023-06-22 15:38:00',
      (select member_id from member where firstname='Paul')
      );

insert into news(title, subtitle, content, newsdate, member_id)
values('NZ Beach Handball Womens Team Selection 2023',
      'Following is the NZ Beach Handball team that will be representing NZ in the Oceania Championships:',
      'Lily Smith' || char(10) ||
      'Paula Gold' || char(10) ||
      'Tina Walker ' || char(10) ||
      'Milly Thumb' || char(10) ||
      'We wish this team good luck as they head to the Gold Coast, Australia to compete in the Oceania Championships.',
      '2023-06-15 11:23:00',
      (select member_id from member where firstname='Jess')
      );

/* inserting information into the draw table */

insert into draw(gamedate, teamone, teamtwo, location, gametime)
values('2023-08-05',
      'Vic Uni',
      'Spartans',
      'Akau Tangi',
       '16:00'
       );

insert into draw(gamedate, teamone, teamtwo, location, gametime)
values('2023-08-05',
      'Hunters',
      'Bye',
      'N/A',
       'N/A'
       );

insert into draw(gamedate, teamone, teamtwo, location, gametime)
values('2023-08-12',
      'Hunters',
      'Spartans',
      'Akau Tangi',
       '15:00'
       );

insert into draw(gamedate, teamone, teamtwo, location, gametime)
values('2023-08-12',
      'Vic Uni',
      'Bye',
      'N/A',
       'N/A'
       );

insert into draw(gamedate, teamone, teamtwo, location, gametime)
values('2023-08-19',
      'Vic Uni',
      'Hunters',
      'Akau Tangi',
       '15:00'
       );

insert into draw(gamedate, teamone, teamtwo, location, gametime)
values('2023-08-19',
      'Spartans',
      'Bye',
      'N/A',
       'N/A'
       );

/* inserting information into the results table */

insert into results(gamedate, teamone, teamtwo, teamonescore, teamtwoscore, winner )
values('2023-08-19',
       'Vic Uni',
       'Spartans',
      50,
       37,
       'Vic Uni'
       );

insert into results(gamedate, teamone, teamtwo, teamonescore, teamtwoscore, winner )
values('2023-08-05',
       'Hunters',
       'Spartans',
      22,
       15,
       'Hunters'
       );
