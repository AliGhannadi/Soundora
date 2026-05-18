import mutagen


def extract_music_metadata(file_path):
    """
    Extract metadata and embedded cover art from an audio file.

    Supported formats: MP3 (ID3), FLAC, OGG, and MP4/M4A.
    Returns a dict with text fields (title, artist, album, producer)
    and binary cover data (cover_image_data, cover_mime_type).
    """
    metadata = {
        "title": None,
        "artist": None,
        "album": None,
        "producer": None,
        "cover_image_data": None,
        "cover_mime_type": None,
    }

    try:
        audio = mutagen.File(file_path)

        # Unrecognized format or file without tags — return empty metadata
        if audio is None or audio.tags is None:
            return metadata

        def get_tag_value(tags, id3_key, generic_key, mp4_key=None):
            """
            Read a tag value across Mutagen's three common tag layouts.

            - id3_key:    ID3 frame name (MP3), e.g. TIT2, TPE1
            - generic_key: Vorbis/FLAC-style key, e.g. title, artist
            - mp4_key:    Apple MP4 atom, e.g. \\xa9nam, \\xa9ART
            """
            # ID3 (MP3): frames expose a .text list
            if id3_key in tags:
                frame = tags[id3_key]
                if hasattr(frame, "text") and frame.text:
                    return str(frame.text[0])
                return str(frame)

            # Vorbis comment / FLAC / OGG: plain string or list of strings
            if generic_key in tags:
                val = tags[generic_key]
                if isinstance(val, list) and len(val) > 0:
                    return str(val[0])
                return str(val)

            # MP4/M4A (Apple tags): atom values are usually single-item lists
            if mp4_key and mp4_key in tags:
                val = tags[mp4_key]
                if isinstance(val, list) and len(val) > 0:
                    return str(val[0])
                return str(val)

            return None

        # Text metadata — each call tries ID3 → generic → MP4 in order
        metadata["title"] = get_tag_value(audio.tags, "TIT2", "title", "\xa9nam")
        metadata["artist"] = get_tag_value(audio.tags, "TPE1", "artist", "\xa9ART")
        metadata["album"] = get_tag_value(audio.tags, "TALB", "album", "\xa9alb")
        # TPE4 is the standard ID3 producer frame; MP4 has no universal producer atom
        metadata["producer"] = get_tag_value(
            audio.tags, "TPE4", "producer", "----:com.apple.iTunes:producer"
        )

        # Embedded cover art — extraction path depends on the tag system
        if hasattr(audio.tags, "getall"):
            # MP3: cover stored as APIC (attached picture) frames
            apic_frames = audio.tags.getall("APIC")
            if apic_frames:
                metadata["cover_image_data"] = apic_frames[0].data
                metadata["cover_mime_type"] = apic_frames[0].mime

        elif hasattr(audio, "pictures") and audio.pictures:
            # FLAC / OGG: cover stored in the .pictures list
            metadata["cover_image_data"] = audio.pictures[0].data
            metadata["cover_mime_type"] = audio.pictures[0].mime

        elif "covr" in audio.tags:
            # MP4/M4A: cover stored in the covr atom
            covr_data = audio.tags["covr"]
            if isinstance(covr_data, list) and len(covr_data) > 0:
                metadata["cover_image_data"] = bytes(covr_data[0])
                # MP4Cover.imageformat: 13 = JPEG, 14 = PNG
                image_format = getattr(covr_data[0], "imageformat", 13)
                metadata["cover_mime_type"] = (
                    "image/png" if image_format == 14 else "image/jpeg"
                )

        # Normalize text fields — strip whitespace from all string values
        for key in ["title", "artist", "album", "producer"]:
            if metadata[key] is not None:
                metadata[key] = str(metadata[key]).strip()

    except Exception as e:
        # Log and return partial/empty metadata rather than raising
        print(
            f"Error extracting metadata from {file_path}: Type -> {type(e).__name__}, Message -> {e}"
        )

    return metadata
