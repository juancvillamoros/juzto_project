from django.test import TestCase
from capacitaciones.models import Playlist
from capacitaciones.views import *
import pytest

# Create your tests here.
class MyTestCase(TestCase):
    # Tests that the 'index.html' template is rendered with the correct context. 
    def test_index_renders_correct_template(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'capacitaciones/index.html' in [template.name for template in response.templates]

    # Tests that the returned context only contains Playlist objects with a certain attribute value. 
    def test_index_only_returns_specific_playlists(self):
        playlist1 = Playlist.objects.create(name='Playlist 1', attribute='value1')
        playlist2 = Playlist.objects.create(name='Playlist 2', attribute='value2')
        response = self.client.get('/')
        assert playlist1 in response.context['playlists']
        assert playlist2 not in response.context['playlists']
    
    # Tests that the function handles the case where no Playlist objects exist in the database. 
    def test_index_no_playlists(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert len(response.context['playlists']) == 0

    # Tests that the function handles the case where the request is not a GET request.  
    def test_index_not_get_request(self, rf):
        # Arrange
        request = rf.post('/index/')
        
        # Act
        response = index(request)
        
        # Assert
        assert response.status_code == 200
        assert response.content == b""

    # Tests that the returned context contains all Playlist objects.  
    def test_index_returns_all_playlists(self, rf):
        # Arrange
        Playlist.objects.create(name="Playlist 1")
        Playlist.objects.create(name="Playlist 2")
        request = rf.get('/index/')
        
        # Act
        response = index(request)
        
        # Assert
        assert response.status_code == 200
        assert len(response.context['playlists']) == 2
    
    # Tests that the returned context contains Playlist objects in a specific order.  
    def test_index_returns_playlists_in_specific_order(self, rf):
        # Arrange
        Playlist.objects.create(name="Playlist 1")
        Playlist.objects.create(name="Playlist 2")
        request = rf.get('/index/')
        
        # Act
        response = index(request)
        
        # Assert
        assert response.status_code == 200
        assert response.context['playlists'][0].name == "Playlist 1"
        assert response.context['playlists'][1].name == "Playlist 2"
    
    # Tests that the function returns a rendered template with the correct context when given a valid video_id. 
    def test_happy_path_videoTutorial(self, mocker):
        # Setup
        video = Video.objects.create(title="Test Video", video_id="123")
        playlist = Playlist.objects.create(name="Test Playlist")
        playlist.videos.add(video)
        request = mocker.Mock()
        request.method = 'GET'

        # Exercise
        response = videoTutorial(request, video.id)

        # Assert
        assert response.status_code == 200
        assert response.template_name == 'capacitaciones/video.html'
        assert response.context_data['video'] == video
        assert response.context_data['previous'] is None
        assert response.context_data['next'] is None
    
    # Tests that the function returns a rendered template with the correct context when given an invalid video_id. 
    def test_edge_case_videoTutorial(self, mocker):
        # Setup
        request = mocker.Mock()
        request.method = 'GET'

        # Exercise
        with pytest.raises(Video.DoesNotExist):
            videoTutorial(request, 999)

    # Tests that the function returns a rendered template with the correct context when given a video_id that belongs to an empty playlist. 
    def test_edge_case_empty_playlist_videoTutorial(self, mocker):
        # Setup
        playlist = Playlist.objects.create(name="Test Playlist")
        request = mocker.Mock()
        request.method = 'GET'

        # Exercise
        with pytest.raises(Video.DoesNotExist):
            videoTutorial(request, playlist.id)

    # Tests that the function returns a rendered template with the expected context keys and values.  
    def test_videoTutorial(self, mocker):
        # Setup
        request = mocker.Mock()
        video = Video.objects.create(title="Test Video", video_id="123")
        playlist = Playlist.objects.create(name="Test Playlist")
        playlist.videos.add(video)
        video.playlist = playlist
        video.save()

        # Execution
        response = videoTutorial(request, video.id)

        # Assertion
        assert response.status_code == 200
        assert 'video' in response.context
        assert 'previous' in response.context
        assert 'next' in response.context
        assert response.context['video'] == video
        assert response.context['previous'] is None
        assert response.context['next'] is None

    # Tests that the function handles multiple videos with the same video_id correctly.  
    def test_multiple_videos_same_id_videoTutorial(self, mocker):
        # Setup
        request = mocker.Mock()
        video1 = Video.objects.create(title="Test Video 1", video_id="123")
        video2 = Video.objects.create(title="Test Video 2", video_id="123")
        playlist = Playlist.objects.create(name="Test Playlist")
        playlist.videos.add(video1, video2)
        video1.playlist = playlist
        video2.playlist = playlist
        video1.save()
        video2.save()

        # Execution
        response = videoTutorial(request, video1.id)

        # Assertion
        assert response.status_code == 200
        assert 'video' in response.context
        assert 'previous' in response.context
        assert 'next' in response.context
        assert response.context['video'] == video1
        assert response.context['previous'] is None
        assert response.context['next'] == video2

    # Tests that the function correctly uses mocked Video and Playlist models.  
    def test_mock_models_videoTutorial(self, mocker):
        # Setup
        request = mocker.Mock()
        video = mocker.Mock()
        playlist = mocker.Mock()
        videos = mocker.Mock()
        playlist.videos.all.return_value = videos
        video.playlist = playlist
        videos.index.return_value = 0
        videos.__len__.return_value = 1

        # Execution
        response = videoTutorial(request, video.id)

        # Assertion
        assert response.status_code == 200
        assert 'video' in response.context
        assert 'previous' in response.context
        assert 'next' in response.context
        assert response.context['video'] == video
        assert response.context['previous'] is None
        assert response.context['next'] is None

    # Tests that a Video object can be created with a valid Playlist object. 
    def test_create_video_with_valid_playlist(self, mocker):
        # Arrange
        playlist = Playlist.objects.create(name="Test Playlist")
        mocker.patch('django.db.models.fields.related_descriptors.create_forward_many_to_one_manager', return_value=None)

        # Act
        video = Video.objects.create(playlist=playlist, title="Test Video", video_id="12345")

        # Assert
        assert video.title == "Test Video"
        assert video.video_id == "12345"
        assert video.playlist == playlist

    # Tests that the title and video_id of a Video object can be retrieved. 
    def test_retrieve_title_and_video_id(self, mocker):
        # Arrange
        playlist = Playlist.objects.create(name="Test Playlist")
        video = Video.objects.create(playlist=playlist, title="Test Video", video_id="12345")
        mocker.patch('django.db.models.fields.related_descriptors.create_forward_many_to_one_manager', return_value=None)

        # Act
        retrieved_video = Video.objects.get(id=video.id)

        # Assert
        assert retrieved_video.title == "Test Video"
        assert retrieved_video.video_id == "12345"

    # Tests that a Video object can be deleted. 
    def test_delete_video(self, mocker):
        # Arrange
        playlist = Playlist.objects.create(name="Test Playlist")
        video = Video.objects.create(playlist=playlist, title="Test Video", video_id="12345")
        mocker.patch('django.db.models.fields.related_descriptors.create_forward_many_to_one_manager', return_value=None)

        # Act
        video.delete()

        # Assert
        assert not Video.objects.filter(id=video.id).exists()

    # Tests that a Video object cannot be created without a Playlist object.  
    def test_create_video_without_playlist(self, mocker):
        # Mock Playlist object
        playlist = mocker.Mock(spec=Playlist)
        playlist.id = 1

        # Attempt to create Video object without Playlist
        with pytest.raises(TypeError):
            Video.objects.create(title="Test Video", video_id="123")

    # Tests that attempting to retrieve a non-existent Video object raises an error.  
    def test_retrieve_nonexistent_video(self):
        # Attempt to retrieve non-existent Video object
        with pytest.raises(Video.DoesNotExist):
            Video.objects.get(id=999)

    # Tests that attempting to update a non-existent Video object raises an error.  
    def test_update_nonexistent_video(self):
        # Attempt to update non-existent Video object
        with pytest.raises(Video.DoesNotExist):
            video = Video(title="Test Video", video_id="123")
            video.save()
            video.id = 999
            video.title = "Updated Test Video"
            video.save()

    # Tests creating a Video object with a valid Playlist object and valid title and video_id. 
    def test_create_video_with_valid_playlist(self, mocker):
        playlist = Playlist.objects.create(name="Test Playlist")
        mocker.patch('django.db.models.Model.save', return_value=None)
        video = Video.objects.create(playlist=playlist, title="Test Video", video_id="12345")
        assert video.title == "Test Video"
        assert video.video_id == "12345"
        assert video.playlist == playlist

    # Tests updating the title or video_id of a Video object. 
    def test_update_title_or_video_id(self, mocker):
        playlist = Playlist.objects.create(name="Test Playlist")
        mocker.patch('django.db.models.Model.save', return_value=None)
        video = Video.objects.create(playlist=playlist, title="Test Video", video_id="12345")
        video.title = "Updated Title"
        video.video_id = "67890"
        video.save()
        assert video.title == "Updated Title"
        assert video.video_id == "67890"

    # Tests retrieving the title and playlist of a Video object. 
    def test_retrieve_title_and_playlist(self, mocker):
        playlist = Playlist.objects.create(name="Test Playlist")
        mocker.patch('django.db.models.Model.save', return_value=None)
        video = Video.objects.create(playlist=playlist, title="Test Video", video_id="12345")
        retrieved_video = Video.objects.get(id=video.id)
        assert retrieved_video.title == "Test Video"
        assert retrieved_video.playlist == playlist

    # Tests creating a Video object with a null Playlist object.  
    def test_create_video_with_null_playlist(self, mocker):
        # Arrange
        playlist = None
        title = "Test Video"
        video_id = "12345"

        # Act
        with pytest.raises(Exception):
            Video.objects.create(playlist=playlist, title=title, video_id=video_id)

        # Assert
        assert Video.objects.filter(title=title).count() == 0

    # Tests creating a Video object with a title or video_id that exceeds the maximum length.  
    def test_create_video_with_exceeding_title_or_video_id_length(self, mocker):
        # Arrange
        playlist = Playlist.objects.create(name="Test Playlist")
        title = "a" * 256
        video_id = "b" * 256

        # Act
        with pytest.raises(Exception):
            Video.objects.create(playlist=playlist, title=title, video_id=video_id)

        # Assert
        assert Video.objects.filter(title=title).count() == 0

    # Tests retrieving a Video object that does not exist.  
    def test_retrieve_nonexistent_video(self, mocker):
        # Arrange
        playlist = Playlist.objects.create(name="Test Playlist")
        title = "Test Video"
        video_id = "12345"

        # Act
        video = Video.objects.filter(title=title, video_id=video_id).first()

        # Assert
        assert video is None

    