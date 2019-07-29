from app import app
from flask import Flask, flash, render_template, request, redirect, url_for
from db_config import mysql
from flask import jsonify
from flask import flash, request
from flask_mysqldb import MySQL

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")    #get all products
    rows = cursor.fetchall()
    cursor.close()
    return render_template('index.html',products = rows)

#Add or update.  if updateID is -1, add product,  and if updateID is 1, then update the product
@app.route('/process',methods=['POST'])
def process():
    try:
        pro_id = request.form.get('updateID')
        pro_name = request.form.get('name')
        pro_price = request.form.get('price')
        pro_picture = request.form.get('picture')
        print(pro_id)
        cursor = mysql.connection.cursor()
        if int(pro_id) == -1:
            cursor.execute("INSERT INTO products (name,price,picture) VALUES ('"+pro_name+"',"+str(pro_price)+",'"+pro_picture+"')")
            print("add !")
            flash('new product was successfully added !')
        else:
            cursor.execute("UPDATE products SET name='"+str(pro_name)+"', price='"+str(pro_price)+"', picture='"+str(pro_picture)+"' WHERE id="+str(pro_id))
            print("update !")
            flash('the product was successfully updated !')
        mysql.connection.commit()
        cursor.close()
        print("successfully proceed!")
    except Exception as e:
        print(e)
    return redirect(url_for('Index'))

#get product details by id(primary key)
@app.route('/getProduct')
def getProduct():
    try:
        pro_id = request.args.get('id', 0, type=int)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id="+str(pro_id))
        rows = cursor.fetchall()
        resp = jsonify(rows[0])
        resp.status_code = 200
        print(resp)
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

#delete one product
@app.route('/delete',methods=['POST'])
def delete():
    pro_id = request.form.get('deleteID')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id="+str(pro_id))
        mysql.connection.commit()
        cursor.close()
        print("deleted !")
        flash('the product was successfully deleted !')
    except Exception as e:
        print(e)
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)