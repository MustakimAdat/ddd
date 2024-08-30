from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
#import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database file path

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model
class User(db.Model, UserMixin):
    Uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255))
    designation = db.Column(db.String(255))
    roll = db.Column(db.String(255))

    def get_id(self):
        return str(self.Uid)


# Report model
class Report(db.Model):
    Rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    _5stag = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    problem_type = db.Column(db.String(255),nullable=False)
    note = db.Column(db.String(255), nullable=True)
    solved_date = db.Column(db.DateTime, nullable=True)
    solver_id = db.Column(db.Integer, db.ForeignKey('user.Uid'), nullable=True)
    solver = db.relationship('User', foreign_keys=[solver_id], backref='solved_reports', lazy=True)
    Uid = db.Column(db.Integer, db.ForeignKey('user.Uid'), nullable=False)
    user = db.relationship('User', foreign_keys=[Uid], backref='reports', lazy=True)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    
    

#@app.route('/')
#def home():
    #return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html')


@app.route('/')
@login_required
def dashboard():
    #reports = Report.query.filter_by(Uid=current_user.Uid).all()
    
    #reports = Report.query.all()
    
    if current_user.roll == 'Maintenance':
        reports = Report.query.filter_by(department=current_user.department).all()
        total_reports = Report.query.filter_by(department=current_user.department).count()
        pending_reports = Report.query.filter_by(department=current_user.department, solved_date=None).count()
        solved_reports = Report.query.filter_by(department=current_user.department).filter(Report.solved_date.isnot(None)).count()
    elif current_user.roll == 'Super Admin':
        reports = Report.query.all()
        total_reports = Report.query.count()
        pending_reports = Report.query.filter_by(solved_date=None).count()
        solved_reports = Report.query.filter(Report.solved_date.isnot(None)).count()
    else:
        reports = Report.query.filter_by(Uid=current_user.Uid).all()
        total_reports = Report.query.filter_by(Uid=current_user.Uid).count()
        pending_reports = Report.query.filter_by(Uid=current_user.Uid, solved_date=None).count()
        solved_reports = Report.query.filter_by(Uid=current_user.Uid).filter(Report.solved_date.isnot(None)).count()

    
    
    return render_template('dashboard.html', reports=reports, total_reports=total_reports, pending_reports=pending_reports, solved_reports=solved_reports)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        description = request.form.get('comment')
        date = request.form.get('date')
        location = request.form.get('location')
        _5stag = request.form.get('_5stag')
        department = request.form.get('drop1')
        problem_type = request.form.get('drop2')

        new_report = Report(description=description,
                            date=date,
                            location=location,
                            _5stag=_5stag,
                            department=department,
                            problem_type=problem_type,
                            solved_date=None,
                            solver_id=None,
                            user=current_user)
        db.session.add(new_report)
        db.session.commit()
        flash('Report submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('index2.html')


@app.route('/report/<int:report_id>')
@login_required
def report_details(report_id):
    report = Report.query.get(report_id)
    if report:
        return render_template('report_details.html', report=report)
    else:
        flash('Report not found!', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/solve_report/<int:report_id>', methods=['POST'])
@login_required
def solve_report(report_id):
    report = Report.query.get(report_id)
    if report and current_user.roll == 'Maintenance' and not report.solved_date:
        report.solved_date = datetime.now()
        report.solver_id = current_user.Uid
        report.note = request.form.get('note')
        db.session.commit()
        flash('Report solved successfully!', 'success')
    elif report.solved_date:
        flash('Report already solved!', 'info')
    else:
        flash('Report not found or you do not have the permission to solve it!', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/download_excel')
@login_required
def download_excel():
	pass
	"""
    if current_user.designation == 'Maintenance':
        reports = Report.query.filter_by(department=current_user.department).all()
    elif current_user.designation == 'SuperAdmin':
        reports = Report.query.all()
    else:
        reports = Report.query.filter_by(Uid=current_user.Uid).all()

    # Create a DataFrame from the reports
    df = pd.DataFrame([(report.Rid, report.description, report.date, report.location,
                        report._5stag, report.department, report.problem_type,
                        report.solved_date, report.solver.Name if report.solver else None)
                       for report in reports],
                      columns=['Report ID', 'Description', 'Date', 'Location',
                               '5S Tag', 'Department', 'Problem Type', 'Solved Date', 'Solver'])

    # Convert the DataFrame to an in-memory Excel file
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, engine='openpyxl')
    excel_file.seek(0)

    return send_file(excel_file, download_name='reports.xlsx', as_attachment=True)
    """

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add a test user for demonstration purposes
        # test_user = User(Name='Test User', email='test@example.com', password='testpassword', department='IT', designation='Developer', roll='user')
        # test_user = User(Name='M it', email='itm@example.com', password='testpassword', department='IT', designation='Maintenance', roll='Maintenance')
        # test_user = User(Name='Test User', email='elm@example.com', password='testpassword', department='Electrical', designation='Maintenance', roll='Maintenance')
        # db.session.add(test_user)
        # db.session.commit()

    app.run(debug=True, host="0.0.0.0")
