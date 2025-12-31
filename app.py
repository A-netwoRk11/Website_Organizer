# type: ignore
from flask import Flask, render_template, request, jsonify, redirect, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///organizer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

db = SQLAlchemy(app)

# Database Models
class EmailAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    purpose = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    websites = db.relationship('Website', backref='email_account', cascade='all, delete-orphan')

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(150))
    email_id = db.Column(db.Integer, db.ForeignKey('email_account.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submissions = db.relationship('Submission', backref='website', cascade='all, delete-orphan')

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, completed, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DayPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    task_title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    priority = db.Column(db.String(50), default='medium')  # high, medium, low
    category = db.Column(db.String(100))  # work, personal, study, exercise, etc.
    status = db.Column(db.String(50), default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    emails = EmailAccount.query.all()
    upcoming_submissions = Submission.query.filter(
        Submission.due_date >= datetime.now(),
        Submission.status == 'pending'
    ).order_by(Submission.due_date).limit(10).all()
    
    overdue_submissions = Submission.query.filter(
        Submission.due_date < datetime.now(),
        Submission.status == 'pending'
    ).all()
    
    stats = {
        'total_emails': EmailAccount.query.count(),
        'total_websites': Website.query.count(),
        'pending_submissions': Submission.query.filter_by(status='pending').count(),
        'overdue': len(overdue_submissions)
    }
    
    return render_template('index.html', emails=emails, upcoming=upcoming_submissions, 
                         stats=stats, overdue=overdue_submissions)

@app.route('/emails')
def emails():
    emails = EmailAccount.query.all()
    return render_template('emails.html', emails=emails)

@app.route('/add_email', methods=['POST'])
def add_email():
    data = request.form
    new_email = EmailAccount(
        email=data['email'],
        purpose=data.get('purpose', '')
    )
    db.session.add(new_email)
    db.session.commit()
    return redirect(url_for('emails'))

@app.route('/delete_email/<int:id>', methods=['POST'])
def delete_email(id):
    email = EmailAccount.query.get_or_404(id)
    db.session.delete(email)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/websites/<int:email_id>')
def websites(email_id):
    email = EmailAccount.query.get_or_404(email_id)
    websites = Website.query.filter_by(email_id=email_id).all()
    return render_template('websites.html', email=email, websites=websites)

@app.route('/add_website', methods=['POST'])
def add_website():
    data = request.form
    new_website = Website(
        name=data['name'],
        url=data['url'],
        username=data.get('username', ''),
        email_id=data['email_id']
    )
    db.session.add(new_website)
    db.session.commit()
    return redirect(url_for('websites', email_id=data['email_id']))

@app.route('/delete_website/<int:id>', methods=['POST'])
def delete_website(id):
    website = Website.query.get_or_404(id)
    email_id = website.email_id
    db.session.delete(website)
    db.session.commit()
    return jsonify({'success': True, 'email_id': email_id})

@app.route('/submissions')
def submissions():
    all_submissions = Submission.query.order_by(Submission.due_date).all()
    websites = Website.query.all()
    return render_template('submissions.html', submissions=all_submissions, websites=websites)

@app.route('/add_submission', methods=['POST'])
def add_submission():
    data = request.form
    due_date = datetime.strptime(data['due_date'], '%Y-%m-%dT%H:%M')
    
    new_submission = Submission(
        title=data['title'],
        description=data.get('description', ''),
        due_date=due_date,
        website_id=data['website_id']
    )
    db.session.add(new_submission)
    db.session.commit()
    return redirect(url_for('submissions'))

@app.route('/update_submission_status/<int:id>', methods=['POST'])
def update_submission_status(id):
    submission = Submission.query.get_or_404(id)
    data = request.get_json()
    submission.status = data['status']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete_submission/<int:id>', methods=['POST'])
def delete_submission(id):
    submission = Submission.query.get_or_404(id)
    db.session.delete(submission)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        emails = EmailAccount.query.filter(
            (EmailAccount.email.contains(query)) | 
            (EmailAccount.purpose.contains(query))
        ).all()
        
        websites = Website.query.filter(
            (Website.name.contains(query)) | 
            (Website.url.contains(query))
        ).all()
        
        submissions = Submission.query.filter(
            (Submission.title.contains(query)) | 
            (Submission.description.contains(query))
        ).all()
        
        return render_template('search.html', query=query, emails=emails, 
                             websites=websites, submissions=submissions)
    return render_template('search.html', query='')

@app.route('/day-planner')
def day_planner():
    selected_date = request.args.get('date')
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    tasks = DayPlan.query.filter_by(date=selected_date).order_by(DayPlan.start_time).all()
    
    # Get submissions due on this date
    submissions_today = Submission.query.filter(
        db.func.date(Submission.due_date) == selected_date,
        Submission.status == 'pending'
    ).all()
    
    # Calculate statistics for the day
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'completed'])
    pending_tasks = len([t for t in tasks if t.status == 'pending'])
    high_priority = len([t for t in tasks if t.priority == 'high'])
    
    stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'high_priority': high_priority
    }
    
    return render_template('day_planner.html', tasks=tasks, selected_date=selected_date,
                         submissions_today=submissions_today, stats=stats)

@app.route('/add_day_plan', methods=['POST'])
def add_day_plan():
    data = request.form
    plan_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    
    start_time = None
    end_time = None
    if data.get('start_time'):
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    if data.get('end_time'):
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    
    new_plan = DayPlan(
        date=plan_date,
        task_title=data['task_title'],
        description=data.get('description', ''),
        start_time=start_time,
        end_time=end_time,
        priority=data.get('priority', 'medium'),
        category=data.get('category', ''),
        status='pending'
    )
    db.session.add(new_plan)
    db.session.commit()
    
    return redirect(url_for('day_planner', date=data['date']))

@app.route('/update_day_plan_status/<int:id>', methods=['POST'])
def update_day_plan_status(id):
    plan = DayPlan.query.get_or_404(id)
    data = request.get_json()
    plan.status = data['status']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete_day_plan/<int:id>', methods=['POST'])
def delete_day_plan(id):
    plan = DayPlan.query.get_or_404(id)
    date = plan.date.strftime('%Y-%m-%d')
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'success': True, 'date': date})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
