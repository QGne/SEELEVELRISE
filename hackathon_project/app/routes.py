from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash, send_file
from werkzeug.utils import secure_filename
main = Blueprint('main', __name__)
import os
from .image_processing import apply_underwater_effect, apply_underwater_effect_ai


# Route for root and page 1
@main.route('/', methods=['GET', 'POST'])
@main.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        username = request.form.get('username', 'Guest')
        session['username'] = username  # Store username in session
        return redirect(url_for('main.todirect'))
    return render_template('page1.html')

# Route to handle form submission and display page 2
@main.route('/todirect', methods=['GET', 'POST'])
def todirect():
    if request.method == 'POST':
        # Handle POST-specific actions if needed
        username = request.form.get('username', 'Guest')
        session['username'] = username  # Optionally update session with form data

    # Render the page for both GET and POST requests
    username = session.get('username', 'Guest')
    return render_template('todirect.html', username=username)

# @main.route('/photo')
# def photo():
#     username = session.get('username', 'Guest')  # Retrieve username from session
#     return render_template('photo/photo.html', username=username)

@main.route('/underwater')
def underwater():
    username = session.get('username', 'Guest')  # Retrieve username from session
    return render_template('underwater/underwater.html', username=username)


@main.route('/welcome')
def welcome():
    return render_template('welcome.html')

@main.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to page1
    return redirect(url_for('main.page1'))


@main.route('/photo', methods=['GET', 'POST'])
def photo():
    username = session.get('username', 'Guest')
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('app/static/uploads', filename)
            file.save(filepath)

            # Store the uploaded filename in session for later use in photoai
            session['uploaded_image'] = filename

            # Apply underwater effect and get relative processed image path
            processed_filepath = apply_underwater_effect(filepath)

            return render_template('photo/photo.html', username=username, uploaded_image=filename, processed_image=processed_filepath)
    return render_template('photo/photo.html', username=username)

@main.route('/photoai', methods=['GET', 'POST'])
def photoai():
    print("photoai route accessed")  # Debugging statement
    username = session.get('username', 'Guest')

    # Check if there's an uploaded image from the initial upload step
    uploaded_image = session.get('uploaded_image')

    if request.method == 'POST':
        print("On the way in post")  # Debugging statement

        if not uploaded_image:
            flash("No uploaded image found for enhancement.")
            return redirect(url_for('main.photo'))

        filepath = os.path.join('app/static/uploads', uploaded_image)

        # Pass the API key to the function
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            flash("API key not found in configuration.")
            return redirect(url_for('main.photoai'))

        elevation_before = 10
        elevation_after = -100

        try:
            processed_image_path = apply_underwater_effect_ai(filepath, elevation_before, elevation_after, api_key)
            print("Processed image path:", processed_image_path)  # Debugging statement
            if processed_image_path:
                return render_template(
                    'photo/photo.html',
                    username=username,
                    uploaded_image=uploaded_image,
                    processed_image=processed_image_path
                )
            else:
                flash("Image processing failed.")
                print("Error: API did not return a processed image.")
        except Exception as e:
            flash("An error occurred during processing.")
            print("Error in photoai route:", e)

        return render_template('photo/photo.html', username=username)
    print("If nothing before this message and the accessed, we skipped alot")  # Debugging statement

    return render_template('photo/photo.html', username=username)

@main.route('/notebook')
def serve_pdf():
    return send_file('sea.pdf', mimetype='application/pdf')

# @main.route('/photoai', methods=['GET', 'POST'])
# def photoai():
#     username = session.get('username', 'Guest')
#
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return "No file part"
#
#         file = request.files['file']
#
#         if file.filename == '':
#             return "No selected file"
#
#         if file:
#             # Save the uploaded file to a specific directory
#             filename = secure_filename(file.filename)
#             filepath = os.path.join('app/static/uploads', filename)
#             file.save(filepath)
#
#             # Call the AI function to apply the underwater effect
#             elevation_before = 10  # Example elevation before
#             elevation_after = 15  # Example underwater elevation
#             api_key = current_app.config['OPENAI_API_KEY']
#             processed_image_path = apply_underwater_effect_ai(filepath, elevation_before, elevation_after, api_key)
#
#             return render_template('photo/photo.html', username=username, uploaded_image=filename,
#                                    processed_image=processed_image_path)
#
#     return render_template('photo/photo.html', username=username)

# @main.route('/photo', methods=['GET', 'POST'])
# def photo():
#     # Retrieve username from session with 'Guest' as default
#     username = session.get('username', 'Guest')
#
#     # Handle file upload if request is POST
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return "No file part"
#         file = request.files['file']
#         if file.filename == '':
#             return "No selected file"
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join('app/static/uploads', filename)
#             file.save(filepath)
#
#             # Apply underwater effect to the uploaded image
#             processed_filepath = apply_underwater_effect(filepath)
#
#             # Render photo.html with uploaded and processed image paths
#             return render_template('photo/photo.html', username=username, uploaded_image=filename,
#                                    processed_image=processed_filepath)
#
#     # For GET requests, just render the page with the username
#     return render_template('photo/photo.html', username=username)