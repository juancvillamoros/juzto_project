import django
from django.shortcuts import redirect
from django.test import TestCase
from .views import sign_out


# Create your tests here.
class MyTestCase(TestCase):
    # Tests that the user is successfully logged out and redirected to the home page. 
    def test_sign_out_successful(self, mocker):
        # Arrange
        request = mocker.Mock()
        redirect_mock = mocker.patch('django.shortcuts.redirect')

        # Act
        result = sign_out(request)

        # Assert
        assert result == redirect_mock.return_value
        redirect_mock.assert_called_once_with('home')
        request.user.logout.assert_called_once()
    
    # Tests that the user is not logged in and is redirected to the login page. 
    def test_sign_out_already_logged_out(self, mocker):
        # Arrange
        request = mocker.Mock()
        request.user.is_authenticated = False
        redirect_mock = mocker.patch('django.shortcuts.redirect')

        # Act
        result = sign_out(request)

        # Assert
        assert result == redirect_mock.return_value
        redirect_mock.assert_called_once_with('login')
    
    # Tests that the user is already logged out and is not redirected. 
    def test_sign_out_not_logged_in(self, mocker):
        # Arrange
        request = mocker.Mock()
        request.user.is_authenticated = False
        redirect_mock = mocker.patch('django.shortcuts.redirect')

        # Act
        result = sign_out(request)

        # Assert
        assert result == redirect_mock.return_value
        redirect_mock.assert_not_called()

    # Tests that the user is redirected to the correct page after logging out.  
    def test_sign_out_redirect_correct_page(self, mocker):
        # Mock the redirect function to return a specific URL
        mocker.patch('django.shortcuts.redirect', return_value='/login/')
        
        # Call the sign_out function with a mock request object
        response = sign_out(mocker.Mock())
        
        # Assert that the redirect function was called with the correct URL
        redirect.assert_called_once_with('home')
        
        # Assert that the response is a redirect to the correct URL
        assert response.url == '/login/'
    
    # Tests that the user session is properly cleared after logging out.  
    def test_sign_out_clears_session(self, mocker):
        # Mock the logout function to do nothing
        mocker.patch('django.contrib.auth.logout')
        
        # Call the sign_out function with a mock request object
        sign_out(mocker.Mock())
        
        # Assert that the logout function was called with the mock request object
        django.contrib.auth.logout.assert_called_once_with(mocker.Mock())
        
        # Assert that the session is empty
        assert not mocker.Mock().session
    
    # Tests that the user data is properly cleared from cache after logging out.  
    def test_sign_out_cache_cleared(self, mocker):
        # Mock the cache clear function to do nothing
        mocker.patch('django.core.cache.cache.clear')
        
        # Call the sign_out function with a mock request object
        sign_out(mocker.Mock())
        
        # Assert that the cache clear function was called
        django.core.cache.cache.clear.assert_called_once()