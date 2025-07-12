import os
from flask import render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# REMOVED: Unused wtforms imports
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from . import admin_bp
# REMOVED: Unused Collaborator model import
from pkg.models import db, Project
from .auth import login_required

# --- Form Definitions ---

# REMOVED: CollaboratorForm is no longer needed.

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=100)])
    date = DateField('Completion Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    
    video = FileField('Project Video (MP4)', validators=[
        Optional(), FileAllowed(['mp4'], 'Only MP4 videos are allowed!')
    ])
    poster = FileField('Poster Image (JPG, PNG)', validators=[
        Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images are allowed!')
    ])
    
    project_type = SelectField('Project Type', choices=[
        ('Personal', 'Personal'), 
        ('Client', 'Client'), 
        ('Collaborative', 'Collaborative')
    ], validators=[DataRequired()])
    
    tech_tags = StringField('Tech Used (comma-separated)', validators=[Optional(), Length(max=255)])
    role = StringField('Your Role', validators=[DataRequired(), Length(max=100)])
    client_name = StringField('Client Name (if applicable)', validators=[Optional(), Length(max=100)])
    
    ai_used = BooleanField('AI Was Used in this Project')
    ai_desc = StringField('How was AI used?', validators=[Optional(), Length(max=255)])
    
    project_value = StringField('Project Value (e.g., $5,000 or Market Value)', validators=[Optional(), Length(max=100)])
    live_site_url = StringField('Live Site URL', validators=[Optional(), URL()])
    github_url = StringField('GitHub Repository URL', validators=[Optional(), URL()])
    case_study_url = StringField('Full Case Study URL', validators=[Optional(), URL()])
    
    # REMOVED: collaborators FieldList is gone.
    
    submit = SubmitField('Save Project')

# --- Helper Functions ---
def save_file(file, upload_folder):
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return filename
    return None

def delete_file(filename, upload_folder):
    if filename:
        try:
            os.remove(os.path.join(upload_folder, filename))
        except OSError as e:
            current_app.logger.error(f"Error deleting file {filename}: {e}")

# --- Routes ---

@admin_bp.route('/projects')
@login_required
def manage_projects():
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('admin/manage_projects.html', projects=projects)

@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        video_filename = save_file(form.video.data, current_app.config['UPLOAD_FOLDER_VIDEO'])
        poster_filename = save_file(form.poster.data, current_app.config['UPLOAD_FOLDER_IMAGE'])

        new_project = Project(
            title=form.title.data,
            date=form.date.data,
            description=form.description.data,
            video_filename=video_filename,
            poster_filename=poster_filename,
            project_type=form.project_type.data,
            tech_tags=form.tech_tags.data,
            role=form.role.data,
            client_name=form.client_name.data,
            ai_used=form.ai_used.data,
            ai_desc=form.ai_desc.data,
            project_value=form.project_value.data,
            live_site_url=form.live_site_url.data,
            github_url=form.github_url.data,
            case_study_url=form.case_study_url.data
        )
        db.session.add(new_project)
        
        # REMOVED: Loop for adding collaborators.
        
        db.session.commit()
        flash('Project has been successfully created!', 'success')
        return redirect(url_for('admin.manage_projects'))

    return render_template('admin/add_edit_project.html', form=form, legend='Add New Project', project=None)

@admin_bp.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project) 

    if form.validate_on_submit():
        if form.video.data:
            delete_file(project.video_filename, current_app.config['UPLOAD_FOLDER_VIDEO'])
            project.video_filename = save_file(form.video.data, current_app.config['UPLOAD_FOLDER_VIDEO'])
        
        if form.poster.data:
            delete_file(project.poster_filename, current_app.config['UPLOAD_FOLDER_IMAGE'])
            project.poster_filename = save_file(form.poster.data, current_app.config['UPLOAD_FOLDER_IMAGE'])

        project.title = form.title.data
        project.date = form.date.data
        project.description = form.description.data
        project.project_type = form.project_type.data
        project.tech_tags = form.tech_tags.data
        project.role = form.role.data
        project.client_name = form.client_name.data
        project.ai_used = form.ai_used.data
        project.ai_desc = form.ai_desc.data
        project.project_value = form.project_value.data
        project.live_site_url = form.live_site_url.data
        project.github_url = form.github_url.data
        project.case_study_url = form.case_study_url.data

        # REMOVED: Logic for clearing and re-adding collaborators.

        db.session.commit()
        flash('Project has been successfully updated!', 'success')
        return redirect(url_for('admin.manage_projects'))

    return render_template('admin/add_edit_project.html', form=form, legend=f'Edit "{project.title}"', project=project)

@admin_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    delete_file(project.video_filename, current_app.config['UPLOAD_FOLDER_VIDEO'])
    delete_file(project.poster_filename, current_app.config['UPLOAD_FOLDER_IMAGE'])
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project has been deleted.', 'success')
    return redirect(url_for('admin.manage_projects'))
