create table address
(
	id_address serial primary key, 
	city_name varchar unique not null,
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

