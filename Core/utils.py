from io import BytesIO
from PIL import Image
from django.core.files import File


# image = r"C:\Users\suyas\Pictures\IDcard\ee_passport_40x50mm.jpg"
# im = Image.open(image)
# # im.show()
# # create a BytesIO object
# im_io = BytesIO() 
# # save image to BytesIO object
# im.save(im_io, 'JPEG', quality=15) 
# contents = im_io.getvalue()
# image_filesize = len(contents)
# # create a django-friendly Files object
# # new_image = File(im_io, name=r"C:\Users\suyas\Pictures\IDcard\compressed.jpg")
# im_io.seek(0)
# im = im_io.read()
# new_image = Image.open(BytesIO(im))
# new_image.show()

def compress(image):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=15) 
    # contents = im_io.getvalue()
    # image_filesize = len(contents)
    # print(f"After {image_filesize}")

    # create a django-friendly Files object
    new_image = File(im_io, name=f"compressed.jpg")
    return new_image

# img = Image.open(BytesIO(im_io))
# img.show()

