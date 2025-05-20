from flask import Flask,render_template,request,url_for,redirect
from collections import Counter
import time 
import threading

app = Flask(__name__)

class MenuItem:
    def __init__(self,name,category,price,description):
        self.name=name
        self.category=category
        self.price=price
        self.description=description
    def __str__(self):
        return f"{self.name} - {self.category} - {self.price} - {self.description}"
    
class Menu:
    menu_items=[]
    def add_item(self,item):
        self.menu_items.append(item)
    def display_menu(self):
        print("The selected items are:")
        for i in self.menu_items:
            print(i)
    def remove_item(self,item):
        if item in self.menu_items:
            self.menu_items.remove(item)
        else:
            print("ITEM NOT FOUND")
    def find_item_by_name(self,item):
        for i in self.menu_items:
            if i.name.lower()==item:
                return item

class Order:
    def __init__(self,menu):
        self.ordered_item=[]
        self.menu=menu
    def add_item(self,item):
        for i in self.menu.menu_items:
            if i.name.lower()==item.lower():
                self.ordered_item.append(i)
    def remove_item(self,item):
        for i in self.ordered_item:
            if i.name.lower()==item.lower():
                #print(i)
                self.ordered_item.remove(i)
                print(self.ordered_item)
                break
        else:
            print("ITEM  NOT FOUND")
    def calculate_total(self):
        total_price=0
        for i in self.ordered_item:
            total_price+=i.price
        return total_price
    def display_order(self):
        for i in self.ordered_item:
            print(i.name)
    def find_item_by_name(self,item):
        for i in self.menu_items:
            if i.name.lower()==item:
                return item
    def count_item(self):
        item_count=Counter(self.ordered_item)
        return dict(item_count)

class Kitchen:
    def process_order(self,item):
        print("cooking...")
        time.sleep(2)
        print("Ready..")


pizza = MenuItem("PIZZA","Main Course",100,"A ved delicious pizza")
fries = MenuItem("FRIES","Side dish",80,"A tasty pluffy french fries")
coke = MenuItem("COKE","DRINK",30,"A soft drink")
choco_cake = MenuItem("CHOCO CAKE","Dessert",50,"A yammy cake dessert")
menu = Menu()
menu.add_item(pizza)
menu.add_item(fries)
menu.add_item(coke)
menu.add_item(choco_cake)
order = Order(menu)
count={}
kitchen = Kitchen()

@app.route('/')
def home():
    return render_template('index.html',menu=Menu.menu_items)

@app.route('/menu')
def menupage():
    count=order.count_item()
    return render_template('menu.html',menu=Menu.menu_items,count=count)

@app.route("/add_to_order",methods=["POST"])
def orderpage():
    selected_item=request.form.get("item_name")
    print(selected_item)
    order.add_item(selected_item)
    count=order.count_item()
    print(order.ordered_item)
    return redirect(url_for("menupage"))

@app.route("/remove_from_order",methods=["POST"])
def removepage():
    selected_item=request.form.get("remove_item")
    print(selected_item)
    for i in order.ordered_item:
        if i.name.lower() == selected_item.lower():
            print("yes")
            order.remove_item(selected_item)
    return redirect(url_for("menupage"))

@app.route("/order")
def order_page():
    final_order={}
    final_quatity={}
    for i in order.ordered_item:
        if i.name not in final_order:
            final_order[i.name]=i.price
            final_quatity[i.name]=1
        else:
            final_order[i.name]+=i.price
            final_quatity[i.name]+=1
    return render_template('order.html',order_item=final_order,total=order.calculate_total(),quantity=final_quatity)

@app.route("/order_placed",methods=["GET"])
def order_placed_page():
    threading.Thread(target=kitchen.process_order).start()
    return render_template("order_placed.html")


if __name__=="__main__":
    app.run(debug=True)