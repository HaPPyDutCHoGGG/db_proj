import psycopg2;
import aspose.pdf as ap;

con = psycopg2.connect(
    database = 'market',
    user = 'postgres',
    password = '1234',
    host = 'localhost',
    port = '5432');
cur = con.cursor();

def map_json(id_order):
    
    cur.execute('select * from orders where id_order=%s', (str(id_order),)); 
    order = cur.fetchone(); 
    id_cl = order[1]; id_prod = order[2]#done
    
    cur.execute('select * from client where id_client=%s', (str(id_cl),));
    client = cur.fetchone();
    id_adrs_cl = client[3];#done
    
    cur.execute('select * from product where id_product=%s', (str(id_prod),));
    prod = cur.fetchone();
    name = prod[1];## 
    
    cur.execute('select * from address where id_address=%s', (str(id_adrs_cl),));
    address = cur.fetchone();
    adress_cl = address[3];##
    
    ###
    
    cur.execute('select * from availability_status_producer where  id_product=%s and availability=%s', (str(id_prod),"True"));
    status = cur.fetchone(); 
    avail, id_stck = status[2], status[0]; 
    
    cur.execute('select * from stock_producer where id_stock=%s', (str(id_stck),));
    address = cur.fetchone();
    address_pr = address[2];
    
    cur.execute('select * from address where id_address=%s', (str(address_pr),));
    address = cur.fetchone();
    address_pr = address[3]; 
    
    json_map = {
        'client':{
            'adress': adress_cl,
            'order': name
        },
        'producer':{
            'addresses': address_pr,
            'availability': avail
        }
    }
    
    return json_map
    #print(names,prices)
    
        


def show_availibility(json):
        _json = json
        _adresses = _json['producer']['addresses']
        _availibility = _json['producer']['availability']
        print(_adresses,_availibility)
show_availibility(map_json(9))