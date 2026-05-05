from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        try:
            m1 = int(request.form['m1'])
            m2 = int(request.form['m2'])
            m3 = int(request.form['m3'])
            m4 = int(request.form['m4'])
            m5 = int(request.form['m5'])

            # Validate that all marks are <= 100
            if m1 > 100 or m2 > 100 or m3 > 100 or m4 > 100 or m5 > 100:
                result = {"error": "Input numbers should be less than or equal to 100"}
            else:
                total = m1 + m2 + m3 + m4 + m5
                percentage = total / 5

                # Grade Logic
                if percentage >= 90:
                    grade = "A+"
                elif percentage >= 75:
                    grade = "A"
                elif percentage >= 60:
                    grade = "B"
                elif percentage >= 50:
                    grade = "C"
                else:
                    grade = "Fail"

                result = {
                    "total": total,
                    "percentage": round(percentage, 2),
                    "grade": grade
                }

        except:
            result = {"error": "Invalid input"}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)