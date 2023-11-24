#streamlit run streamlit_sql_controlls.py
import folium;
from geopy.geocoders import Nominatim;
from geopy.distance import geodesic;
import streamlit as st;
import psycopg2;
from streamlit_folium import st_folium;
import time;
import base64;
import pandas as pd;
import numpy as np;
import random as rand;

con = psycopg2.connect(
    database = 'market',
    user = 'postgres',
    password = '1234',
    host = 'localhost',
    port = '5432');
cur = con.cursor();

def order_info(order_id):
    cur.execute("select * from orders where id_order=%s;", (order_id));
    order_info = cur.fetchone();
    
    return order_info;

def client_info(client_id):
    cur.execute("select * from client where id_client=%s;", (client_id));
    client_info = cur.fetchone();
    
    return client_info;
    

def main():
    
    geolocator = Nominatim(user_agent="Tester")
    #Region DB
    
    def all_clients():
        
        ids = [];
        cur.execute('select * from orders')
        ord = cur.fetchall();
        for item in ord:
            ids.append(item[1])
        #print(ids,prod_id)
        
        names = []; emails = []; address_id = []
        for id in ids:
            cur.execute('select * from client where id_client=%s',(str(id),))
            clients = cur.fetchone()
            names.append(clients[1]);emails.append(clients[2]);address_id.append(clients[3])
        
        addresses = []; region = []
        for id in address_id:
            cur.execute('select * from address where id_address=%s',(str(id),))
            address = cur.fetchone()
            addresses.append(address[3]);region.append(address[4])

        prepare = {'client number': ids, 'client name': names, 'email': emails, 'address': addresses, 'region': region}
        
        return prepare
    
    def all_orders():
        
        ids = []; prod_id = []  
        cur.execute('select * from orders')
        ord = cur.fetchall();
        for item in ord:
            ids.append(item[0]);prod_id.append(item[2])
        #print(ids,prod_id)
        
        names = []; prices = []
        for id in prod_id:
            cur.execute('select * from product where id_product=%s',(str(id),))
            products = cur.fetchone()
            names.append(products[1]);prices.append(products[2])
        print(products)
        prepare = {'order number': ids, 'product': names, 'price': prices}
        
        return prepare
    
    def displayPDF(file):
    # Opening file from file path
        with open(file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # Embedding PDF in HTML
        pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

        # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        
    def get_prod_cat(id_cat):
        cur.execute("select * from product where id_category=%s;", (str(id_cat)))
        product = cur.fetchall();
        
        return product

    def order_present(order_id):
        check = []; check.append(order_id)
        cur.execute("select * from orders where id_order=%s;", (order_id,))
        
        order = cur.fetchone();
        _Idclient, _Idproduct = order[1],order[2]; #print(_Idclient, Idproduct)
        
        cur.execute("select * from client where id_client=%s;", (str(_Idclient),))
        client = cur.fetchone(); 
        _Clname, _Clmail= client[1],client[2]; #print(_Clname, _Clmail)
        check.append(_Clname);check.append(_Clmail)
        
        cur.execute("select * from product where id_product=%s;", (str(_Idproduct),))
        product = cur.fetchone();
        _Prname, _Prprice, _Prcategory = product[1],product[2],product[4]; #print(_Prname, _Prprice,_Prcategory)
        check.append(_Prname);check.append(_Prprice);
        
        cur.execute("select * from category where id_category=%s;", (str(_Prcategory),))
        category = cur.fetchone();
        check.append(category[1]);
        #[1, 'John B', 'john@mail.com', 'Ibanez SA260FM-VLS', Decimal('22000'), 'Guitar']
        ######
        
        return check


    #End region
    

    #Region Map
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
    
    def get_coord(adress):
        _adress = adress
        location = geolocator.geocode(_adress)
        #print(location)
        #print(location.latitude, location.longitude)

        return location.latitude, location.longitude

    def show_availibility(json):
        _json = json
        _adresses = _json['producer']['addresses'][0]
        map = folium.Map(location=get_coord(_adresses),
                    tiles='openstreetmap',
                    zoom_start=20)

        for item in _adresses:
                folium.Marker(
                location=get_coord(item),
                tooltip='muztorg',
                popup=f"order: {_json['client']['order']}\n availability: in stock",
                icon=folium.Icon(color="green")).add_to(map)

        return map
    #End region
    #streamlit run streamlit_sql_controlls.py
    #Region Input

    
    input = str(st.text_input("enter CLIENT ID and PRODUCT ID with space between to add order")); data = f"{rand.randint(1,30)}.{rand.randint(1,12)}.2024"; 
    if input != '':  
        buffer = input.split(); #print(buffer, input,data); 
        client = buffer[0]; product = buffer[1]  
        cur.execute("insert into orders(id_client,id_product,production_date) values(%s,%s,%s)",(client,product,data));
        con.commit();
        st.write(f'the order contributed successfully');
        time.sleep(3)
    
    order = str(st.text_input("type threre the number of the order to DELETE it")); print(type(order))
    if order != '':
        cur.execute("delete from orders where id_order=%s;",(order,))
        con.commit();
        st.write('the order deleted successfully');
    
    find = str(st.text_input("type threre the number of the order to FIND it on stock"));
    if find != '':
        json_map = map_json(int(find))
        #[1, 'John B', 'john@mail.com', 'Ibanez SA260FM-VLS', Decimal('22000'), 'Guitar']
        labels = ['order number:','client:','email:','product:','price in rubles:','category:'];
        info = order_present(find);
        
        with st.sidebar:
            i = 0
            for item in info:
                st.write(labels[i],item); i+=1
        
        st.write('check out map, there is it');
        map = show_availibility(json_map);
        # call to render Folium map in Streamlit
        st_data = st_folium(map, width=725); time.sleep(100);
        
        
    st.write("Choose the option");
    if st.button("show report"):
        displayPDF('report.pdf');    
    
    if st.button("show products"):
        option = st.selectbox('choose category',('Guitar', 'drumm', 'amp','hardware')); #1 2 3 4
        
        if option == "Guitar":
            id_cat = 1;
            all = get_prod_cat(id_cat);
            
            prod = [];ids = [];price = []
            for item in all:
                ids.append(item[0]); prod.append(item[1]);price.append(item[2])
            prepare = {'ids': ids, 'product': prod, 'price': price}
            df = pd.DataFrame(prepare)
            st.dataframe(df)  # Same as st.write(df)
            
                            
        elif option == "drumm":
            id_cat = 2;
            all = get_prod_cat(id_cat);
            
            prod = [];ids = [];price = []
            for item in all:
                ids.append(item[0]); prod.append(item[1]);price.append(item[2])
            prepare = {'ids': ids, 'product': prod, 'price': price}
            df = pd.DataFrame(prepare)
            st.dataframe(df)  # Same as st.write(df)
            
            
        elif option == "amp":
            id_cat = 3;
            all = get_prod_cat(id_cat);
            
            prod = [];ids = [];price = []
            for item in all:
                ids.append(item[0]); prod.append(item[1]);price.append(item[2])
            prepare = {'ids': ids, 'product': prod, 'price': price}
            df = pd.DataFrame(prepare)
            st.dataframe(df)  # Same as st.write(df)
            
            
        elif option == "hardware":
            id_cat = 4;
            all = get_prod_cat(id_cat);
            
            prod = [];ids = [];price = []
            for item in all:
                ids.append(item[0]); prod.append(item[1]);price.append(item[2])
            prepare = {'ids': ids, 'product': prod, 'price': price}
            df = pd.DataFrame(prepare)
            st.dataframe(df)  # Same as st.write(df)
            
        time.sleep(3)
    if st.button("show all orders"):   
        df = pd.DataFrame(all_orders())
        st.dataframe(df)  # Same as st.write(df)all_orders()
    
    if st.button("show all clients"):   
        df = pd.DataFrame(all_clients())
        st.dataframe(df)  # Same as st.write(df)all_orders()
        
         
    #End region
    #streamlit run streamlit_sql_controlls.py
   
   

    
        

if __name__ == "__main__":
    try:
        main();
    except SystemExit:
        pass;

con.close();

