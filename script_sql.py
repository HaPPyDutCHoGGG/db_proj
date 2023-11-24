import psycopg2;
import aspose.pdf as ap;

con = psycopg2.connect(
    database = 'market',
    user = 'postgres',
    password = '1234',
    host = 'localhost',
    port = '5432');
cur = con.cursor();

def get_products():
    cur.execute("select * from product;")
    res = cur.fetchall();
    return res

def get_orders():
    cur.execute("select * from orders;")
    res = cur.fetchall();
    return res

def get_producer():
    cur.execute("select * from producer;")
    res = cur.fetchall();
    return res

def get_supplier():
    cur.execute("select * from supplier;")
    res = cur.fetchall();
    return res


def create_report():
    document = ap.Document()

    page1 = document.pages.add()
    text_fragment = ap.text.TextFragment("Hello,here is your report")
    
    page1.paragraphs.add(text_fragment)
    lable = ap.text.TextFragment("Available products")
    page1.paragraphs.add(lable)
    products = get_products()
    for item in products:
        text = ap.text.TextFragment(f"\n({item[0]})product: {item[1]} \nprice: {item[2]}rub\navailability: available")
        page1.paragraphs.add(text)
    
    page2 = document.pages.add()    
    lable = ap.text.TextFragment("Actual orders")
    page2.paragraphs.add(lable)
    orders = get_orders()
    for item in orders:
        text = ap.text.TextFragment(f"\n(order_num: {item[0]} \nclient: {item[1]}\nproduct: {item[2]}\nproduction_date: {item[3]}")
        page2.paragraphs.add(text)
        
    page3 = document.pages.add()    
    lable = ap.text.TextFragment("Available producers")
    page3.paragraphs.add(lable)
    producers = get_producer()
    for item in producers:
        text = ap.text.TextFragment(f"\nproducer: {item[1]} \ncontact: {item[2]}\nsite: {item[3]}\nemail: {item[4]}")
        page3.paragraphs.add(text)
        
    page4 = document.pages.add()    
    lable = ap.text.TextFragment("Available producers")
    page4.paragraphs.add(lable)
    suppliers = get_supplier()
    for item in producers:
        text = ap.text.TextFragment(f"\nsupplier: {item[1]} \ncontact: {item[2]}\nemail: {item[3]}")
        page4.paragraphs.add(text)
   
    return document

create_report().save("report.pdf")