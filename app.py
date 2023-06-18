from flask import Flask, render_template,request, flash, redirect
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://praveen200040109:praveen@cluster0.2l505lx.mongodb.net/myDataAccount1"
db = PyMongo(app).db



chats = db.inventory.find()
myChats = [chat for chat in chats]

@app.route('/')
def home():
    global myChats 
    return render_template("index.html", myChats=myChats)


@app.route("/customer/<customer_id>")
def view_customer(customer_id):
    chats = db.inventory.find()
    myChat1 = {}
    print("customer_id:", customer_id,chats)
    for ch in chats:
        print("chat account_number:", ch["account_number"])
        if ch['account_number'] == str(customer_id):
            myChat1 = ch
            break

    print("myChat1:", myChat1)
    return render_template("customer.html", myChat=myChat1, customer_id=customer_id)

    

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    transfers = db.transaction.find()
    myCh = [chat for chat in transfers]
    success_message = ""
    if request.method == "POST":
        sender = request.form.get('sender_account_number')
        receiver = request.form.get('to_account_number')
        amount = request.form.get('Amount')
        status = "Success"
        if sender == receiver:
            print("Same Account")
            status = "Failed: Same Account"
        else:
            chats = db.inventory.find()
            sender1 = {}
            receiver1 = {}
            for ch in chats:
                if ch['account_number'] == str(sender):
                    sender1 = ch
                elif ch['account_number'] == str(receiver):
                    receiver1 = ch
            
            print(sender1, receiver1)
            if sender1 == {} or receiver1 == {}:
                status = "Failed: Put Correct Account No."
                print("Put Correct Account No.")
            elif sender1['balance'] >= float(amount):
                sender1['balance'] -= float(amount)
                receiver1['balance'] += float(amount)
                db.inventory.update_one(
                    {"_id": sender1["_id"]},
                    {"$set": {"balance": sender1['balance']}}
                )
                db.inventory.update_one(
                    {"_id": receiver1["_id"]},
                    {"$set": {"balance": receiver1['balance']}}
                )
                print("Transaction successful")
                success_message = "Transaction Successful"
            else:
                status = "Failed: Balance Not Sufficient"
                print("Balance Not Sufficient")
                success_message = ""

        db.transaction.insert_one({
            "From": sender,
            "To": receiver,
            "Status": status,
            "Amount": amount,
            "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        })
        return render_template("transfer.html", myChat=myCh, success_message=success_message,sure = True)
    else:
        return render_template("transfer.html", myChat=myCh,success_message= success_message,sure = False)
    

@app.route("/transactions")
def transactions():
    transfers = db.transaction.find()
    Transac = [chat for chat in transfers]
    return render_template("transaction.html", myChat=Transac)



if __name__ == '__main__':
    app.run(debug=True)


