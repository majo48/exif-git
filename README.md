# pyPicDTO
Set picture file attribute 'DateTimeCreated' to EXIF/IPTC/XMP attribute 'DateTimeOriginal' (when the picture was taken with the camera).

# Standards
JPEG files are the predominant image type in general use today. JPEG is an acronym for “Joint Photographic Experts Group,” which is the name of the committee that created the JPEG standard in 1992. JPEG images use a “lossy” compression format designed to minimize the size of photographs and other realistic image content while retaining the bulk of visual information.

JPEG image files can be rich with metadata. The “JPEG File Interchange Format (JFIF)” extended the JPEG format to include a minimal amount of metadata, including pixel density and aspect ratio, and optionally a small embedded thumbnail of the image to be used by gallery display applications.

In addition to JPEG-specific JFIF metadata, JPEG files may also contain EXIF, IPTC, or XMP metadata.

# EXIF (Exchangeable Image File Format) 
Was developed to embed information about the device capturing the image (typically a camera) into the image itself. EXIF metadata consist of a series of Tags and Values, which can include things such as the make and model of the camera used to generate the image, the date and time the image was captured, and the geolocation information about the capturing device.

# IPTC (Information Interchange Model) 
Developed by the International Press Telecommunications Council (IPTC). This standard, sometimes referred to as “IPTC Headers,” was designed originally to embed information about images used by newspapers and news agencies. It is used primarily by photojournalists and other industries producing digital images for print.

# XMP (XML-based “eXensible Metadata Platform”) 
Developed by Adobe in 2001. It largely supersedes the earlier metadata schemes and is open and extensible. While used most commonly for image metadata, its extensibility allows it to be used for other types of files as well.
