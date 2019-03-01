drop table if exists sheet;
drop table if exists student;
drop table if exists current_class_no;

create table current_class_no(cc int not null);
insert into current_class_no values(0);

create table student(roll int primary key, name varchar(50), finger_pos int not null);
insert into student values (1507022, 'Hannan Tech', 0);
insert into student values (1507021, 'Salahuddin Ahmed', 1);
insert into student values (1507028, 'Mushfiqur Rahman', 2);
insert into student values (1507030, 'Sadia', 3);
insert into student values (1507007, 'Sakib Reza', 4);
insert into student values (1507038, 'Raihanul Islam', 5);
insert into student values (1507033, 'Potl Sadman', 6);
insert into student values (1507039, 'Nahid Lipstick', 7);

create table sheet(class_no int, roll int, attend varchar(10), primary key(class_no, roll), foreign key(roll) references student(roll));
