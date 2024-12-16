import cv2
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from datetime import datetime
import numpy as np
from ImageEditor.models import SelectedImage
from django.conf import settings



def home(request):
    return render(request, 'index.html')


@login_required
def getImage(request):
    if 'imageToEdit' in request.FILES:
        image_file = request.FILES['imageToEdit']
        try:
            setPic = SelectedImage.objects.get(user=request.user)
            setPic.image = image_file
            setPic.editImage = image_file
            setPic.save()
        except:
            obj = SelectedImage()
            obj.user = request.user
            obj.editImage = image_file
            obj.image = image_file
            obj.save()

        return redirect('canvas')


@login_required
def canvas(request):
    obg = SelectedImage.objects.get(user=request.user)
    img = obg.editImage.name

    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    x, y, z = img.shape
    return render(request, 'canvas.html', {'obg': obg, 'x': x, 'y': y})


def gray(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save(str(datetime.now()) + ".png", content)
    return redirect('canvas')


def negative(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    img = 255 - img

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def add_bright(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, 20)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def remove_bright(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.subtract(v, 20)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def GaussianBlur(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    img = cv2.GaussianBlur(img, (7, 7), 0)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def medianBlur(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    img = cv2.medianBlur(img, 5)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def meanfilter(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if the image is loaded properly
    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    # Apply mean filter (box filter) to the image
    filtered_img = cv2.blur(img, (5, 5))  # (5, 5) is the kernel size, which can be adjusted

    # Save the mean-filtered image
    ret, buf = cv2.imencode('.jpg', filtered_img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('mean_filtered_output.jpg', content)

    return redirect('canvas')


def midpoint_filter(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if the image is loaded properly
    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    # Define kernel size for filtering
    kernel_size = (5, 5)

    # Apply maximum filter
    max_img = cv2.dilate(img, np.ones(kernel_size, np.uint8))

    # Apply minimum filter
    min_img = cv2.erode(img, np.ones(kernel_size, np.uint8))

    # Midpoint filter: average of max and min images
    midpoint_img = ((max_img.astype(np.float32) + min_img.astype(np.float32)) / 2).astype(np.uint8)

    # Save the midpoint-filtered image
    ret, buf = cv2.imencode('.jpg', midpoint_img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('midpoint_filtered_output.jpg', content)

    return redirect('canvas')


def crop_left(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if y > 20:
        img = img[:, 20:]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def crop_right(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if y > 20:
        img = img[:, :y - 20]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def crop_up(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if x > 20:
        img = img[20:, :]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def crop_down(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if x > 20:
        img = img[:x - 20, :]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def undo(request):
    object = SelectedImage.objects.get(user=request.user)
    object.editImage = object.image
    object.save()
    return redirect('canvas')


def resize(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape

    if request.method == 'POST':
        height = int(request.POST['height'])
        width = int(request.POST['width'])

        if height > 0 and width > 0:
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)

    return redirect('canvas')


def rotate_left(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if image is loaded properly
    if img is None:
        return redirect('canvas')  # handle error gracefully if the image is not found or fails to load

    # Rotate the image 90 degrees counter-clockwise
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Save the rotated image
    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('rotated_output.jpg', content)

    return redirect('canvas')


def rotate_right(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if the image is loaded properly
    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    # Rotate the image 90 degrees clockwise
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # Save the rotated image
    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('rotated_output_right.jpg', content)

    return redirect('canvas')


def detect_edge(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray_img, threshold1=100, threshold2=200)

    edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    ret, buf = cv2.imencode('.jpg', edges_color)
    content = ContentFile(buf.tobytes())
    object.editImage.save('edge_detected_output.jpg', content)

    return redirect('canvas')





def save(request):
    obj = SelectedImage.objects.get(user=request.user)
    img = obj.editImage
    photo = cv2.imread(img.url)
    imaj = cv2.resize(photo, (600, 600))
    obj.editImage = imaj
    obj.save()
    return redirect('canvas')
