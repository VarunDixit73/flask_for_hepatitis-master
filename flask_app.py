from flask import Flask, render_template, request
from joblib import load
from data_set import creatuser, db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
with app.app_context():
    db.init_app(app)
    db.create_all()

def load_model():
    filepath = 'ml_src/hepatitis.pkl'
    return load(filepath)

def pred(age,sex,steroid,antivirals,fatigue,malaise,anorexia,liver_big,liver_firm,spleen_palable,
            spiders,ascites,varices,bilirubin,alk_phosphate,sgot,albumin,protime,histology):
    userinp = [[age,sex,steroid,antivirals,fatigue,malaise,anorexia,liver_big,liver_firm,spleen_palable,
            spiders,ascites,varices,bilirubin,alk_phosphate,sgot,albumin,protime,histology]]
    x = load_model().get('scaler').transform(userinp)
    print(type(x),x,x.shape)
    p= load_model().get('classifier').predict(x)

    if p[0] == 1:
        return 'Suffering from Hepatitis'
    else:
        return 'Not Suffering from Hepatitis'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=="POST":
        form = request.form
        print(form)
        age = int(form.get('age'))
        sex = int(form.get('sex'))
        steroid = int(form.get('steroid'))
        antivirals = int(form.get('antivirals'))
        fatigue = int(form.get('fatigue'))
        malaise = int(form.get('malaise'))
        anorexia = int(form.get('anorexia'))
        liver_big = int(form.get('liver_big'))
        liver_firm = int(form.get('liver_firm'))
        spleen_palable = int(form.get('spleen_palable'))
        spiders = int(form.get('spiders'))
        ascites = form.get('ascites')
        varices = int(form.get('varices'))
        bilirubin = float(form.get('bilirubin'))
        alk_phosphate = int(form.get('alk_phosphate'))
        sgot = int(form.get('sgot'))
        albumin = float(form.get('albumin'))
        protime = int(form.get('protime'))
        histology = int(form.get('histology'))
        result = pred(age,sex,steroid,antivirals,fatigue,malaise,anorexia,liver_big,liver_firm,spleen_palable,
            spiders,ascites,varices,bilirubin,alk_phosphate,sgot,albumin,protime,histology)
        
        user = creatuser(age,sex,steroid,antivirals,fatigue,malaise,anorexia,liver_big,liver_firm,spleen_palable,
            spiders,ascites,varices,bilirubin,alk_phosphate,sgot,albumin,protime,histology)
        
        return render_template('index.html',age=age, sex=sex, steroid=steroid, antivirals=antivirals,
                    fatigue=fatigue, malaise=malaise, anorexia=anorexia, liver_big=liver_big,
                    liver_firm=liver_firm, spleen_palable=spleen_palable, spiders=spiders,
                    ascites=ascites, varices=varices, bilirubin=bilirubin, alk_phosphate=alk_phosphate,
                    sgot=sgot, albumin=albumin, protime=protime, histology=histology, result=result,user=user)
    return render_template('index.html')

@app.route('/data')
def display():
    data = User.query.all()
    return render_template('data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)