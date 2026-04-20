import pytest
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from app.models import Music, Album, Producer, Category


# ---------- Fixtures ----------
@pytest.fixture
def dummy_audio():
    return SimpleUploadedFile(
        "test_audio.mp3",
        b"file_content",
        content_type="audio/mpeg"
    )


@pytest.fixture
def dummy_image_data():
    return b"fake_image_bytes"


# ---------- Tests ----------
@pytest.mark.django_db
@patch('app.utils.extract_music_metadata')
def test_save_with_full_metadata_creates_relations(mock_extract, dummy_audio, dummy_image_data):
    mock_extract.return_value = {
        'title': 'Test Song Title',
        'album': 'Test Album Name',
        'cover_image_data': dummy_image_data,
        'cover_mime_type': 'image/jpeg',
        'producer': 'DJ Test',
        'artist': 'Singer Test'
    }

    music = Music(file=dummy_audio)
    music.save()

    mock_extract.assert_called_once()

    assert music.title == 'Test Song Title'
    assert music.album.name == 'Test Album Name'

    assert music.cover_image.name.startswith('cover_')
    assert music.cover_image.name.endswith('.jpg')

    assert music.producer.filter(user__username='DJTest').exists()
    assert music.artist.filter(user__username='SingerTest').exists()


@pytest.mark.django_db
@patch('app.utils.extract_music_metadata')
def test_save_does_not_override_existing_data(mock_extract, dummy_audio):
    mock_extract.return_value = {
        'title': 'Metadata Title',
        'album': 'Metadata Album',
    }

    custom_album = Album.objects.create(name="Custom Album")
    user_producer = User.objects.create_user(email="ali@gmail.com", password="123456myadmin", username="aliorg")
    custom_producer = Producer.objects.create(user=user_producer)

    music = Music(
        title="Custom Title",
        album=custom_album,
        file=dummy_audio
    )
    music.save()
    music.producer.add(custom_producer)

    music.save()

    assert music.title == "Custom Title"
    assert music.album == custom_album
    assert music.producer.filter(user__username='aliorg').exists()

    assert not music.producer.filter(user__username='MetadataDJ').exists()


@pytest.mark.django_db
@patch('app.utils.extract_music_metadata')
def test_save_with_no_metadata(mock_extract, dummy_audio):
    mock_extract.return_value = None

    music = Music(file=dummy_audio)
    music.save()

    assert music.title is None
    assert music.album is None
    assert not bool(music.cover_image)
    assert music.producer.count() == 0
    assert music.artist.count() == 0


@pytest.mark.django_db
@patch('app.utils.extract_music_metadata')
def test_png_cover_image_extension(mock_extract, dummy_audio, dummy_image_data):
    mock_extract.return_value = {
        'title': 'PNG Cover Song',
        'cover_image_data': dummy_image_data,
        'cover_mime_type': 'image/png',
    }

    music = Music(file=dummy_audio)
    music.save()

    assert music.cover_image.name.endswith('.png')
