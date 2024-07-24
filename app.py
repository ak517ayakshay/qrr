from flask import Flask, request, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
import qrcode
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

class QRForm(FlaskForm):
    data = StringField('Data', validators=[DataRequired()])
    submit = SubmitField('Generate QR Code')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = QRForm()
    if form.validate_on_submit():
        data = form.data.data
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = os.path.join('static', 'qrcode.png')
        img.save(img_path)
        return send_file(img_path, mimetype='image/png')
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
