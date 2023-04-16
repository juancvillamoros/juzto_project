import datetime
from typing import ByteString
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from mysqlx import Client
from django.core.exceptions import PermissionDenied
from .views import *
from .utils import *
from .forms import VideoForm
from .models import Video
from django.contrib.auth.models import User
import pytest
import pytz

class MyTestCase(TestCase):
    # Tests that the function returns a list of videos for a logged in user who has uploaded videos. 
    def test_video_list_logged_in_with_videos(self, mocker):
        # Setup
        user = User.objects.create_user(username='testuser', password='testpass')
        video1 = Video.objects.create(user=user, cedula='123456', id_audiencia='789', id_comparendo='456', video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        video2 = Video.objects.create(user=user, cedula='654321', id_audiencia='321', id_comparendo='987', video_url='https://www.youtube.com/watch?v=oHg5SJYRHA0')
        request = RequestFactory().get('/videos/')
        request.user = user

        # Mock
        mock_render = mocker.patch('django.shortcuts.render')

        # Exercise
        response = video_list(request)

        # Assert
        assert response.status_code == 200
        assert mock_render.called_once_with(request, 'video_list.html', {'videos': [video2, video1]})

    #Tests that the function returns an empty list for a logged in user who has not uploaded any videos. 
    def test_video_list_logged_in_no_videos(self, mocker):
        # Setup
        user = User.objects.create_user(username='testuser', password='testpass')
        request = RequestFactory().get('/videos/')
        request.user = user

        # Mock
        mock_render = mocker.patch('django.shortcuts.render')

        # Exercise
        response = video_list(request)

        # Assert
        assert response.status_code == 200
        assert mock_render.called_once_with(request, 'video_list.html', {'videos': []})

    # Tests that the function redirects to the login page if the user is not logged in. 
    def test_video_list_not_logged_in(self, mocker):
        # Setup
        request = RequestFactory().get('/videos/')

        # Mock
        mock_login_required = mocker.patch('django.contrib.auth.decorators.login_required')

        # Exercise
        response = video_list(request)

        # Assert
        assert response.status_code == 302
        assert response.url == '/accounts/login/?next=/videos/'
        assert mock_login_required.called_once_with(video_list)

    # Tests that the function returns a list of videos ordered by date correctly.  
    def test_video_list_order_by_date(self, mocker):
        # Setup
        user = User.objects.create_user(username='testuser', password='testpass')
        mocker.patch('django.contrib.auth.decorators.login_required', return_value=lambda x: x)
        mocker.patch('django.contrib.auth.decorators.permission_required', return_value=lambda x: x)
        mocker.patch('django.shortcuts.render', return_value='rendered')
        video1 = Video.objects.create(user=user, cedula='123', id_audiencia='456', id_comparendo='789', video_url='https://example.com/video1', fecha_subida=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=pytz.UTC))
        video2 = Video.objects.create(user=user, cedula='123', id_audiencia='456', id_comparendo='789', video_url='https://example.com/video2', fecha_subida=datetime.datetime(2022, 1, 2, 0, 0, tzinfo=pytz.UTC))
        video3 = Video.objects.create(user=user, cedula='123', id_audiencia='456', id_comparendo='789', video_url='https://example.com/video3', fecha_subida=datetime.datetime(2022, 1, 3, 0, 0, tzinfo=pytz.UTC))

        # Exercise
        request = HttpRequest()
        request.user = user
        response = video_list(request)

        # Verify
        assert response == 'rendered'
        assert response.context_data['videos'] == [video3, video2, video1]

    # Tests that the function raises a permission error if the user does not have permission to view videos.  
    def test_video_list_no_permission(self, mocker):
        # Setup
        user = User.objects.create_user(username='testuser', password='testpass')
        mocker.patch('django.contrib.auth.decorators.login_required', return_value=lambda x: x)
        mocker.patch('django.contrib.auth.decorators.permission_required', side_effect=PermissionDenied)
        mocker.patch('django.shortcuts.render', return_value='rendered')

        # Exercise and Verify
        with pytest.raises(PermissionDenied):
            request = HttpRequest()
            request.user = user
            video_list(request)

    # Tests that the function returns an empty list if the user ID is not valid.  
    def test_video_list_invalid_user_id(self, mocker):
        # Setup
        user = User.objects.create_user(username='testuser', password='testpass')
        mocker.patch('django.contrib.auth.decorators.login_required', return_value=lambda x: x)
        mocker.patch('django.contrib.auth.decorators.permission_required', return_value=lambda x: x)
        mocker.patch('django.shortcuts.render', return_value='rendered')

        # Exercise
        request = HttpRequest()
        request.user = user
        response = video_list(request)

        # Verify
        assert response == 'rendered'
        assert response.context_data['videos'] == []

    # Tests that a video is successfully uploaded and saved to the database, compressed and uploaded to S3, and the user is redirected to the dashboard with a success message displayed. 
    def test_upload_video_success(self, mocker):
        # Mocking the form and video file
        form_data = {'cedula': '123456789', 'id_audiencia': '123', 'id_comparendo': '456', 'video_url': 'test.mp4'}
        form = VideoForm(data=form_data)
        video_file = mocker.Mock()
        video_file.size = 1024 * 1024 * 2

        # Mocking the compress_and_upload_to_s3 function
        mocker.patch('app.views.compress_and_upload_to_s3', return_value='https://s3.amazonaws.com/test-bucket/1.mp4')

        # Mocking the request and user
        request = mocker.Mock()
        request.method = 'POST'
        request.user = mocker.Mock()
        request.FILES = {'video_url': video_file}
        request.POST = form_data

        # Testing the view function
        response = upload_video(request)
        assert response.status_code == 302
        assert response.url == '/dashboard/'
        assert Video.objects.count() == 1
        assert Video.objects.first().cedula == '123456789'
        assert Video.objects.first().id_audiencia == '123'
        assert Video.objects.first().id_comparendo == '456'
        assert Video.objects.first().video_url == 'https://s3.amazonaws.com/test-bucket/1.mp4'
        assert messages.get_messages(request).first().message == "¡El video ha sido cargado correctamente!"

    # Tests that an error message is displayed and the user is redirected to the upload page when an invalid form is submitted. 
    def test_upload_video_invalid_form(self, mocker):
        # Mocking an invalid form
        form_data = {'cedula': '', 'id_audiencia': '', 'id_comparendo': '', 'video_url': ''}
        form = VideoForm(data=form_data)

        # Mocking the request and user
        request = mocker.Mock()
        request.method = 'POST'
        request.user = mocker.Mock()
        request.POST = form_data
        request.FILES = {}

        # Testing the view function
        response = upload_video(request)
        assert response.status_code == 302
        assert response.url == '/upload_video/'
        assert Video.objects.count() == 0
        assert messages.get_messages(request).first().message == "Por favor corrija los errores en el formulario."

    # Tests that an error message is displayed and the user is redirected to the upload page when a video file larger than 3GB is submitted. 
    def test_upload_video_large_file(self, mocker):
        # Mocking a large video file
        form_data = {'cedula': '123456789', 'id_audiencia': '123', 'id_comparendo': '456', 'video_url': 'test.mp4'}
        form = VideoForm(data=form_data)
        video_file = mocker.Mock()
        video_file.size = 1024 * 1024 * 4

        # Mocking the request and user
        request = mocker.Mock()
        request.method = 'POST'
        request.user = mocker.Mock()
        request.POST = form_data
        request.FILES = {'video_url': video_file}

        # Testing the view function
        response = upload_video(request)
        assert response.status_code == 302
        assert response.url == '/upload_video/'
        assert Video.objects.count() == 0
        assert messages.get_messages(request).first().message == "El tamaño del video no puede ser mayor a 3GB"

    # Tests that an error message is displayed and the user is redirected to the upload page when a form is submitted with missing fields.  
    def test_upload_video_missing_fields(self, client):
        # Test that an error message is displayed and the user is redirected to the upload page when a form is submitted with missing fields.
        user = User.objects.create_user(username='testuser', password='testpass')
        client.force_login(user)
        response = client.post('/upload_video/', {'cedula': '123456', 'id_audiencia': '', 'id_comparendo': '', 'video_url': ''})
        assert response.status_code == 200
        assert b'This field is required.' in response.content

    # Tests that an error message is displayed and the video instance is deleted when an exception is raised while compressing and uploading the video to S3.  
    @pytest.mark.parametrize("exception", [ValueError("El tamaño del video no puede ser mayor a 3GB"), Exception])
    @pytest.patch('video_app.views.compress_and_upload_to_s3')
    def test_upload_video_s3_exception(self, mock_upload, exception, client):
        # Test that an error message is displayed and the video instance is deleted when an exception is raised while compressing and uploading the video to S3.
        user = User.objects.create_user(username='testuser', password='testpass')
        client.force_login(user)
        mock_upload.side_effect = exception
        with open('tests/test_video.mp4', 'rb') as video_file:
            response = client.post('/upload_video/', {'cedula': '123456', 'id_audiencia': '789', 'id_comparendo': '456', 'video_url': video_file})
        assert response.status_code == 302
        assert Video.objects.count() == 0
        assert b'Error al subir el archivo' in response.content

    # Tests that the form widget attributes are correctly set for each field.  
    def test_upload_video_form_widget_attributes(self):
        # Test that the form widget attributes are correctly set for each field.
        form = VideoForm()
        assert 'class="form-control"' in str(form['cedula'])
        assert 'class="form-control"' in str(form['id_audiencia'])
        assert 'class="form-control"' in str(form['id_comparendo'])
        assert 'class="form-control"' in str(form['video_url'])

    # Tests that a Video object can be created with all required fields. 
    def test_creating_video_with_all_required_fields(self):
        user = User.objects.create(username='testuser')
        video = Video.objects.create(user=user, cedula='123456789', id_audiencia='A123', id_comparendo='C456', video_url='https://example.com/video')
        assert video.id is not None

    # Tests that a Video object cannot be created with empty cedula, id_audiencia, or id_comparendo fields. 
    def test_creating_video_with_empty_fields(self):
        user = User.objects.create(username='testuser')
        with pytest.raises(Exception):
            Video.objects.create(user=user, cedula='', id_audiencia='', id_comparendo='', video_url='')
    
    # Tests that the __str__ method returns the expected string representation of the Video object. 
    def test_video_str_representation(self):
        user = User.objects.create(username='testuser')
        video = Video.objects.create(user=user, cedula='123456789', id_audiencia='A123', id_comparendo='C456', video_url='https://example.com/video')
        assert str(video) == '123456789 - A123 - C456'

    # Tests that a Video object cannot be created with a very long cedula, id_audiencia, or id_comparendo field.  
    def test_creating_video_with_long_fields(self):
        with pytest.raises(Exception):
            Video.objects.create(user=User.objects.create(), cedula='a'*256, id_audiencia='b'*256, id_comparendo='c'*256)

    # Tests that the fecha_subida field is automatically set to the current date and time when a Video object is created.  
    def test_fecha_subida_auto_set(self):
        video = Video.objects.create(user=User.objects.create(), cedula='123', id_audiencia='456', id_comparendo='789')
        assert video.fecha_subida is not None
    
    # Tests that the video_url field can accept valid URLs and reject invalid ones.  
    def test_video_url_validity(self, mocker):
        mock_validator = mocker.patch('django.core.validators.URLValidator')
        video = Video.objects.create(user=User.objects.create(), cedula='123', id_audiencia='456', id_comparendo='789', video_url='https://www.example.com')
        mock_validator.assert_called_once_with()
        assert video.video_url == 'https://www.example.com'

    # Tests that the form is valid and all fields are filled correctly. 
    def test_form_valid_all_fields(self):
        data = {
            'cedula': '123456789',
            'id_audiencia': 'A123',
            'id_comparendo': 'C456',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        form = VideoForm(data=data)
        assert form.is_valid() == True

    # Tests that the form is valid and only required fields are filled. 
    def test_form_valid_required_fields(self):
        data = {
            'cedula': '123456789',
            'id_audiencia': 'A123',
            'id_comparendo': 'C456',
        }
        form = VideoForm(data=data)
        assert form.is_valid() == True

    # Tests that the form is valid and video_url is left blank. 
    def test_form_valid_blank_video_url(self):
        data = {
            'cedula': '123456789',
            'id_audiencia': 'A123',
            'id_comparendo': 'C456',
            'video_url': ''
        }
        form = VideoForm(data=data)
        assert form.is_valid() == True

    # Tests that the form is valid and video_url is uploaded successfully.  
    def test_form_valid_uploaded_video_url(self, mocker):
        # Happy path test
        form_data = {
            'cedula': '1234567890',
            'id_audiencia': '1234567890',
            'id_comparendo': '1234567890',
            'video_url': 'https://www.example.com/video.mp4'
        }
        form = VideoForm(data=form_data)
        assert form.is_valid() is True

    # Tests that the form is invalid and required fields are left blank.  
    def test_form_invalid_blank_fields(self, mocker):
        # Edge case test
        form_data = {
            'cedula': '',
            'id_audiencia': '',
            'id_comparendo': '',
            'video_url': ''
        }
        form = VideoForm(data=form_data)
        assert form.is_valid() is False
        assert 'cedula' in form.errors
        assert 'id_audiencia' in form.errors
        assert 'id_comparendo' in form.errors
        assert 'video_url' in form.errors

    # Tests that the form is invalid and cedula, id_audiencia, and id_comparendo fields contain invalid characters.  
    def test_form_invalid_invalid_characters(self, mocker):
        # Edge case test
        form_data = {
            'cedula': 'abc123',
            'id_audiencia': '!@#$%',
            'id_comparendo': '123abc',
            'video_url': ''
        }
        form = VideoForm(data=form_data)
        assert form.is_valid() is False
        assert 'cedula' in form.errors
        assert 'id_audiencia' in form.errors
        assert 'id_comparendo' in form.errors
