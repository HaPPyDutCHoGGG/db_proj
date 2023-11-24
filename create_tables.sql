create table address
(
	id_address serial primary key, 
	city_name varchar not null,
	country_name varchar not null,
	actual_address varchar not null,
	world_region varchar not null
);
/*changed table city to table address*/

create table client
(
	id_client serial primary key, 
	client_name varchar not null,
	client_email varchar unique not null,
	id_address int references address(id_address)
);

create table producer
(
	id_producer serial primary key, 
	producer_name varchar not null,
	producer_contact varchar unique not null,
	producer_site varchar unique not null,
	producer_email varchar unique not null,
	id_address int references address(id_address)
);

create table stock_producer
(
	id_stock serial primary key,
	id_owner int references producer(id_producer),
	id_address int references address(id_address)
);

/*done--*/

create table category
(
	id_category serial primary key,
	category_name varchar unique not null
);

create table product 
(
	id_product serial primary key,
	product_name varchar not null,
	product_price decimal not null,
	fragility bool not null,
	id_category int references category(id_category),
	id_producer int references producer(id_producer)
);

create table availability_status_producer
(
	id_stock int references stock_producer(id_stock),
	id_product int references product(id_product), 
	availability bool not null
);

create table orders
(
	id_order serial primary key, 
	id_client int references client(id_client),
	id_product int references product(id_product),
	production_date varchar unique not null
);
/*done--*/

create table supplier 
(
	id_supplier serial primary key,
	supplier_name varchar unique not null,
	supplier_contact varchar unique not null,
	supplier_email varchar unique not null,
	id_address int references address(id_address)	
);

create table stock_supplier
(
	id_stock serial primary key,
	id_owner int references supplier(id_supplier),
	id_address int references address(id_address)
);

create table material 
(
	id_material serial primary key,
	material_name varchar unique not null,
	material_price decimal not null,
	weight_of_unit decimal not null,
	units_in_bunch int not null,
	id_supplier int references supplier(id_supplier)
);

create table availability_status_supplier
(
	id_stock int references stock_supplier(id_stock),
	id_product int references material(id_material), 
	availability bool not null
);
/*done--*/

create table compound
(
	id_product int references product(id_product),
	id_material int references material(id_material)
);

/*inserts*/
        /*address*/
insert insert into address (city_name, country_name, actual_address, world_region)
values ('New York', 'USA', 'New York, William st, 150', 'NA'), ('New York', 'USA', 'New York, Hudson st, 675', 'NA'), ('London', 'Great Britain', 'London, Southhampton Row, 92', 'eurasia'), ('London', 'Great Britain', 'London, Victoria st, 105', 'eurasia'), ('Washington', 'USA', 'Washington, Massachusetts Ave Northwest, 1775 ', 'NA'), ('Washington', 'USA', 'Washington, South Hayes st, 1201', 'NA'), ('Tokyo', 'Japan', 'Tokyo, Tio-Dori st, 41', 'eurasia'), ('Detroit', 'USA', 'Detroit, West Lafayette Blvd, 600', 'NA'), ('Chicago', 'USA', 'Chicago, South Canal st, 1101', 'NA'), ('Chicago', 'USA', 'Chicago, North Green st, 333', 'NA');
		/*producer*/
insert into producer(producer_name, producer_contact, producer_site, producer_email, id_address) values('Ibanez', '+79221234411', 'ibanez.ru', 'sm@m.com', 1), ('Jackson', '+79994223511', 'jacksonguitars.com', 'jack@gmail.com', 2), ('ESP', '+79726236487', 'www.espguitars.ru', 'espguitars@m.com', 3), ('Fender', '+7 (906) 990-32-94', 'fender.ru', 'yakov5377@hotmail.com', 4), ('Lepsky', '+7 (945) 758-35-63', 'lepskyguitars.com', 'asya5257@outlook.com', 5), ('Shamray', '+7 (924) 406-90-54', 'shamray.ru', 'aad9276f0', 1), ('Behringer', '+7 (922) 577-96-22', 'behringer.com', 'milana5221@rambler.ru', 6), ('Stagy', '+7 (924) 834-91-71', 'staggmusic.com', 'gennadiy30@hotmail.com', 7), ('Pearl', '+7 (993) 859-45-44', 'pearldrum.com', 'asya44@rambler.ru', 8), ('Marshal', '+7 (907) 412-68-67', 'marshall.com.ru', 'timofey11031983@mail.ru', 9), ('Orange', '+7 (908) 360-11-28', 'orange.com', 'lana20091960@yandex.ru', 10);
		/*client*/
insert into client(client_name,client_email,id_address) values('John B','john@mail.com','2');
		/*category*/
insert into category (category_name) values ('guitar'), ('drumm'), ('amp'), ('hardware');

		/*product*/
insert into product (product_name, product_price, fragility, id_category, id_producer)
values ('USA Soloist SK2H', 43999, true, 1, 2), ('Horizon 2NT BLK', 15000, false, 1, 8), ('Jazzmaster MW IBM', 25300, false, 1, 4), ('Custom', 100000, true, 1, 6), ('UMC204HD', 49990, false, 1, 7), ('Custom', 49990, true, 1, 3), ('TIM120B WR', 70000, true, 2, 9), ('masters maple complete', 90000, true, 2, 9), ('emberton 2', 20000, false, 3, 10), ('or30', 15000, false, 3, 11);

		/*stock_producer*/
insert into stock_producer (id_owner, id_address) 
values (6, 4), (7, 1), (8, 9), (10, 10), (11, 9), (3, 4) , (9, 7) , (1, 10), (5, 9), (4, 9), (3, 1);

		/*availability supplier*/
insert into availability_status_supplier(id_stock, id_product, availability) 
values(1, 1, true), (1, 1, true), (1, 2, false), (1, 3, false), (2, 4, false), (2, 5, true), (2, 5, true), (2, 2, true), (3, 1, true), (1, 3, false), (5, 4, false), (5, 4, true) ;
		/*availability producer*/
insert into availability_status_producer(id_stock, id_product, availability) 
values(12, 11, true), (13, 12, true), (13, 13, false), (15, 14, false), (16, 15, false), (17, 16, true), (18, 17, true), (19, 18, true), (20, 19, true), (21, 20, false), (22, 11, false), (12, 12, true) ;

		/*orders*/
insert into orders(id_client, id_product, production_date) 
values(1, 20,'09-04-2023'), (2, 11, '20-01-2023'), (5, 12, '29-07-2023'), (5, 19, '04-04-2023'), (1, 18, '12-03-2023'), (2, 17, '08-04-2023'), (4, 16, '19-04-2023') ;

		/*material*/
insert into material (material_name, material_price, weight_of_unit, units_in_bunch, id_supplier)
values ('upper maple deck', 15000, 5, 1, 1), ('ash neck', 10000, 0.8, 2, 2),  ('drum plastics', 17000, 0.3, 5, 7),  ('drum stands', 20000, 4, 3, 8),  ('electronic', 44990, 4, 10, 9);

		/*compound*/
insert into compound(id_product, id_material) 
values(11, 1), (11, 2) , (12, 1) , (12, 2), (13, 1),(13, 2), (14, 1) ,(14, 2) , (15, 5), (16, 2), (16, 1) , (17, 3), (17, 4), (18, 3) , (18, 4), (19, 5), (20, 5);

		/*stock_supplier*/
insert into stock_supplier(id_owner, id_address) 
values(1, 7), (2, 9), (3, 4), (4, 10) , (5, 5), (6, 3), (7, 7), (8, 8), (9, 2) ;









