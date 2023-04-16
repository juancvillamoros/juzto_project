from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from reportarbugs.forms import ReporteForm
from .models import Reporte
import pytest


# Create your tests here.
class MyTestCase(TestCase):
    # Tests that a Reporte object can be created with all required fields. 
    def test_create_reporte_with_required_fields(self, mocker):
        # Arrange
        user = User.objects.create(username='testuser')
        mocker.patch('django.contrib.auth.models.User.objects.get', return_value=user)
        reporte_data = {
            'user': user,
            'nombre': 'Test Reporte',
            'descripcion': 'This is a test reporte',
        }

        # Act
        reporte = Reporte.objects.create(**reporte_data)

        # Assert
        assert reporte.user == user
        assert reporte.nombre == 'Test Reporte'
        assert reporte.descripcion == 'This is a test reporte'

    # Tests that a Reporte object can be updated with valid data. 
    def test_update_reporte_with_valid_data(self, mocker):
        # Arrange
        user = User.objects.create(username='testuser')
        mocker.patch('django.contrib.auth.models.User.objects.get', return_value=user)
        reporte_data = {
            'user': user,
            'nombre': 'Test Reporte',
            'descripcion': 'This is a test reporte',
        }
        reporte = Reporte.objects.create(**reporte_data)
        updated_reporte_data = {
            'nombre': 'Updated Test Reporte',
            'descripcion': 'This is an updated test reporte',
            'resuelto': True,
        }

        # Act
        reporte.nombre = updated_reporte_data['nombre']
        reporte.descripcion = updated_reporte_data['descripcion']
        reporte.resuelto = updated_reporte_data['resuelto']
        reporte.save()

        # Assert
        updated_reporte = Reporte.objects.get(id=reporte.id)
        assert updated_reporte.nombre == 'Updated Test Reporte'
        assert updated_reporte.descripcion == 'This is an updated test reporte'
        assert updated_reporte.resuelto == True

    # Tests that an error is raised when trying to upload a file with a size greater than the allowed limit. 
    def test_upload_file_with_size_greater_than_allowed_limit(self, mocker):
        # Arrange
        user = User.objects.create(username='testuser')
        mocker.patch('django.contrib.auth.models.User.objects.get', return_value=user)
        reporte_data = {
            'user': user,
            'nombre': 'Test Reporte',
            'descripcion': 'This is a test reporte',
        }
        reporte = Reporte.objects.create(**reporte_data)
        file_mock = mocker.Mock(spec=pytest.File)
        file_mock.size = 1024 * 1024 * 11  # 11 MB file size

        # Act & Assert
        with pytest.raises(ValidationError):
            reporte.archivo.save('test_file.pdf', file_mock)

    # Tests that an error is raised when trying to create a Reporte object with a null user field.  
    def test_create_reporte_with_null_user_field(self, mocker):
        # Arrange
        mocker.patch('django.db.models.Model.save')
        reporte = Reporte(nombre='Test Reporte', descripcion='This is a test reporte', archivo=None, resuelto=False)

        # Act and Assert
        with pytest.raises(ValueError):
            reporte.save()

    # Tests that an error is raised when trying to create a Reporte object with a blank nombre field.  
    def test_create_reporte_with_blank_nombre_field(self, mocker):
        # Arrange
        mocker.patch('django.db.models.Model.save')
        user = User.objects.create_user(username='testuser', password='testpass')
        reporte = Reporte(user=user, nombre='', descripcion='This is a test reporte', archivo=None, resuelto=False)

        # Act and Assert
        with pytest.raises(ValueError):
            reporte.save()

    # Tests that the creado_en and actualizado_en fields are automatically set when creating or updating a Reporte object.  
    def test_confirm_creado_en_and_actualizado_en_fields_are_automatically_set(self, mocker):
        # Arrange
        mocker.patch('django.db.models.Model.save')
        user = User.objects.create_user(username='testuser', password='testpass')
        reporte = Reporte(user=user, nombre='Test Reporte', descripcion='This is a test reporte', archivo=None, resuelto=False)

        # Act
        reporte.save()

        # Assert
        assert reporte.creado_en is not None
        assert reporte.actualizado_en is not None

    # Tests that a logged in user can submit a valid report form. 
    def test_report_bug_valid_submission(self, client, user):
        # Setup
        client.force_login(user)
        data = {
            'nombre': 'Test Report',
            'descripcion': 'This is a test report',
            'archivo': 'test_file.txt'
        }

        # Exercise
        response = client.post('/report_bug/', data=data)

        # Verify
        assert response.status_code == 302
        assert response.url == '/report_list/'

    # Tests that a non-logged in user is redirected to the login page when trying to submit a report form. 
    def test_report_bug_redirect_to_login(self, client):
        # Exercise
        response = client.get('/report_bug/')

        # Verify
        assert response.status_code == 302
        assert response.url == '/login/?next=/report_bug/'

    # Tests that a user is unable to submit a report form with a large file. 
    def test_report_bug_large_file_submission(self, client, user, mocker):
        # Setup
        client.force_login(user)
        data = {
            'nombre': 'Test Report',
            'descripcion': 'This is a test report',
            'archivo': mocker.MagicMock(size=1024*1024*10)  # 10 MB file
        }

        # Exercise
        response = client.post('/report_bug/', data=data)

        # Verify
        assert response.status_code == 200
        assert 'archivo' in response.context['form'].errors.keys()

    # Tests that a user is unable to submit an invalid report form.  
    def test_report_bug_invalid_submission(self, mocker):
        """
        Tests that a user is unable to submit an invalid report form.
        """
        mock_form = mocker.Mock()
        mock_form.is_valid.return_value = False
        mocker.patch('app.forms.ReporteForm', return_value=mock_form)

        response = self.client.post('/report_bug/', {'nombre': '', 'descripcion': '', 'archivo': ''})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    # Tests that a user is unable to submit a report form with a file type not allowed.  
    def test_report_bug_file_type_not_allowed(self, mocker):
        """
        Tests that a user is unable to submit a report form with a file type not allowed.
        """
        mock_form = mocker.Mock()
        mock_form.is_valid.return_value = False
        mocker.patch('app.forms.ReporteForm', return_value=mock_form)

        response = self.client.post('/report_bug/', {'nombre': 'Test', 'descripcion': 'Test', 'archivo': 'test.exe'})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    # Tests that a user is unable to submit a report form with no file attached.  
    def test_report_bug_no_file_attached(self, mocker):
        """
        Tests that a user is unable to submit a report form with no file attached.
        """
        mock_form = mocker.Mock()
        mock_form.is_valid.return_value = False
        mocker.patch('app.forms.ReporteForm', return_value=mock_form)

        response = self.client.post('/report_bug/', {'nombre': 'Test', 'descripcion': 'Test', 'archivo': ''})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    # Tests that the form is valid and can be saved to the database. 
    def test_form_valid(self):
        form_data = {
            'nombre': 'Test Reporte',
            'descripcion': 'Este es un reporte de prueba',
            'archivo': None
        }
        form = ReporteForm(data=form_data)
        assert form.is_valid() == True

    # Tests that the form is invalid due to missing required fields. 
    def test_form_invalid(self):
        form_data = {
            'nombre': '',
            'descripcion': '',
            'archivo': None
        }
        form = ReporteForm(data=form_data)
        assert form.is_valid() == False

    # Tests that the form is invalid when the file size is greater than 10MB. 
    def test_file_size_limit(self):
        file = open('test_file.pdf', 'rb')
        form_data = {
            'nombre': 'Test Reporte',
            'descripcion': 'Este es un reporte de prueba',
            'archivo': file
        }
        form = ReporteForm(data=form_data)
        assert form.is_valid() == False

    # Tests that the form is invalid when the file type is not supported.  
    def test_file_type_not_supported(self):
        form_data = {
            'nombre': 'Test Reporte',
            'descripcion': 'This is a test reporte',
            'archivo': 'test.txt'
        }
        form = ReporteForm(data=form_data)
        assert not form.is_valid()
    
    # Tests that the form fields are rendered with correct HTML attributes.  
    def test_form_fields_rendered(self):
        form = ReporteForm()
        assert str(form['nombre']) == '<input type="text" name="nombre" class="form-control" required id="id_nombre">'

    # Tests that form validation errors are displayed correctly.  
    def test_form_validation_errors_displayed(self):
        form_data = {
            'nombre': '',
            'descripcion': '',
            'archivo': ''
        }
        form = ReporteForm(data=form_data)
        assert not form.is_valid()
        assert str(form.errors['nombre']) == '<ul class="errorlist"><li>This field is required.</li></ul>'