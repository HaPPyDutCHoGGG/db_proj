create table city
(
	id_city serial primary key, 
	city_name varchar unique not null,
	city_country varchar not null	
);

create table client
(
	id_client serial primary key, 
	client_name varchar not null,
	client_email varchar unique not null,
	id_city int references city(id_city)
);

create table producer
(
	id_producer serial primary key, 
	producer_name varchar not null,
	producer_contacts varchar unique not null,
	id_city int references city(id_city)
);
/**/

create table category
(
	id_category serial primary key,
	category_name varchar unique not null
)

create table product 
(
	id_product serial primary key,
	product_name varchar not null,
	product_price decimal not null,
	fragility bool not null,
	id_category int references category(id_category),
	id_producer int references producer(id_producer)
)

create table orders
(
	id_client int references client(id_client),
	id_product int references product(id_product),
	production_date varchar unique not null,
	constraint orders_pk primary key (id_client,id_product)
)
/**/

create table supplier 
(
	id_supplier serial primary key,
	supplier_name varchar unique not null,
	supplier_email varchar unique not null
)
***

create table material 
(
	id_material serial primary key,
	material_name varchar unique not null,
	material_price decimal not null,
	material_weight decimal not null,
	delivery_number int not null,
	id_supplier int references supplier(id_supplier)
)
/*mb should make delivery_number uniquee*/

create table compound
(
	id_product int references product(id_product),
	id_material int references material(id_material)
)
