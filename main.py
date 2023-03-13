from flask import Flask, jsonify,render_template,request,redirect,url_for
from multiprocessing import Queue
from flask import request

app = Flask(__name__)
data = {}
g_state = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phoneNumber']
        code_number = request.form['codeNumber']
        print(phone_number,code_number)
        if code_number:
            return redirect(url_for('putCode', phoneNumber=phone_number,codeNumber=code_number))
        return redirect(url_for('putPhone', phoneNumber=phone_number))
    return render_template('index.html')

@app.route('/putPhone')
def putPhone():
    global data
    phoneNumber = request.args.get('phoneNumber')
    if data.get(phoneNumber) == None:
        data[phoneNumber]={"statusPhone": "NEW","codeNumber":None}
        return str(phoneNumber)
    else:
        return str(phoneNumber + " available")

@app.route('/putCode')
def putCode():
    global data
    phoneNumber = request.args.get('phoneNumber')
    codeNumber = request.args.get('codeNumber')
    data[phoneNumber]["statusPhone"]="RECEVED"
    data[phoneNumber]["codeNumber"]=codeNumber
    return str({phoneNumber:data[phoneNumber]})

@app.route('/getPhoneNone')
def getPhoneNone():
    global data
    output = {}
    for key,value in data.items():
        if value.get("statusPhone") == "NEW":
            output["phoneNumber"] = key
            data[key]["statusPhone"] = "WAITCODE"
            # return output
            return key
    # return jsonify({})
    return ""

@app.route('/getCode')
def getCode():
    global data
    phoneNumber = request.args.get('phoneNumber')
    # return jsonify(data.get(phoneNumber))
    res = data.get(phoneNumber).get("codeNumber")
    return "" if res == None else res

@app.route('/getAll')
def getAll():
    global data
    return jsonify(data)



@app.route('/clearAll')
def clearAll():
    global data
    data = {}
    return jsonify(data)

@app.route('/state')
def state():
    global g_state
    state = request.args.get("setState")
    if state != None and state != "":
        g_state = str(state)
    return str(g_state)


@app.route('/count')
def count():
    global data
    return str(data.qsize())


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
