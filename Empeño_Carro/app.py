from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from models import db, Car
from utils import calculate_loan_amount, generate_contract

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def setup():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        plates = request.form['plates']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        brand = request.form['brand']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        loan_amount = calculate_loan_amount(model, year, mileage, brand)

        car = Car(plates=plates, model=model, year=year, mileage=mileage, brand=brand, image=filename,
                  loan_amount=loan_amount)
        db.session.add(car)
        db.session.commit()

        return redirect(url_for('contract', car_id=car.id))

    return render_template('add_car.html')


@app.route('/contract/<int:car_id>')
def contract(car_id):
    car = Car.query.get(car_id)
    if not car:
        return redirect(url_for('index'))
    contract_text = generate_contract(car)
    return render_template('contract.html', contract_text=contract_text)


@app.route('/admin')
def admin():
    cars = Car.query.all()
    return render_template('admin.html', cars=cars)


if __name__ == '__main__':
    app.run(debug=True)
