
import os 
import cv2
import json
import base64
from django.core import files
from django.dispatch.dispatcher import receiver
from django.http.response import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from home.forms import CommentForm
from deeporacles import settings
from contrib.forms import MessageForm
from home.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import PermissionDenied
from profiles.models import Profile, ProfilePic
from django.contrib.auth.signals import user_logged_in, user_logged_out
from settings.models import Area, City, Country, Region
from .forms import (EducationForm, FileForm, PotfolioForm, ProfileUpdateForm, SkillForm,
                    ProfilePictureForm, EditUserForm, ProfileWallForm )
from .models import AddressBook, Education, Files, Potfolio, Profile, ProfilePic, Skill

SYMBOL_DONT_HAVE_NAME = ['#', '6', ')', '{', '=', '-', '.', ':', '%', '_', '+', '>', '5', '&', ',', '!', '@', '/', '7',
                         ']', '0', '9', '^', '8', ';', '}', '*', '|', '?', '2', '(', '3', '$', '<', '[', '1', '4', "'",
                         '"']
# Create your views here.

TEMP_IMAGE_NAME = "temp_image.png"

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()


@require_http_methods(["GET", "POST"])
@login_required
def update_profile_picture(request):
	if request.is_ajax():
		mode = request.GET.get('mode')
		if mode == 'remove-picture':
			request.user.profile.picture = 'profile_pics/default-avatar.png'
			request.user.profile.save()
			messages.success(request,'Profile picture has been successfully removed')
			message = 'removed'
		return JsonResponse({ 'message' : message })


@require_http_methods(["GET", "POST"])
@login_required
def update_wallpaper(request):
	if request.is_ajax():
		mode = request.GET.get('mode')
		if mode == 'remove-picture':
			request.user.profile.image = 'profile_pics/014.jpeg'
			request.user.profile.save()
			messages.success(request,'Wallpaper has been successfully removed')
			message = 'removed'
		return JsonResponse({ 'message' : message })


def user_timeline(request, profile_slug, *args, **kwargs):
	profile = Profile.objects.get(slug=profile_slug)
	user = profile.user
	followers = user.circles.followers.all()

	if len(followers) == 0:
		is_following = False

	for follower in followers:
		if follower == request.user:
			is_following = True
			break
		else:
			is_following = False

	page_number = request.GET.get('page', 1)
	post_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=False, user=user).order_by('-DatePublished'), 3)
	posts = post_paginator.get_page(page_number)
	question_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=True, user=user).order_by('-DatePublished'), 5)
	questions = question_paginator.get_page(page_number)
	form = CommentForm()
	context = {
		'user': user,
		'is_following': is_following,
		'posts': posts,
		'questions': questions,
		'form': form,
	}
	context['user_timeline_seg'] = 'user_timeline_seg'
	context['segment'] = 'Profile'
	return render(request, "profiles/my_timeline.html", context)

@login_required
def my_timeline(request):
	profile = request.user.profile
	user = profile.user
	followers = user.circles.followers.all()

	if len(followers) == 0:
		is_following = False

	for follower in followers:
		if follower == request.user:
			is_following = True
			break
		else:
			is_following = False

	page_number = request.GET.get('page', 1)
	post_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=False, user=user).order_by('-DatePublished'), 3)
	posts = post_paginator.get_page(page_number)
	question_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=True, user=user).order_by('-DatePublished'), 5)
	questions = question_paginator.get_page(page_number)
	form = CommentForm()

	context = {
		'profile': profile,
		'form': form,
		'user': user,
		'is_following': is_following,
		'posts': posts,
		'questions': questions,
	}
	context['timeline_seg'] = 'timeline_seg'
	context['segment'] = 'Profile'
	return render(request, "profiles/my_timeline.html", context)


def getTimelinePosts(request, profile_slug):
	if request.is_ajax():
		pk = request.POST.get('pk')
		counter = request.POST.get('counter')
		profile = Profile.objects.get(slug=profile_slug)
		user = profile.user
		if not user:
			raise HttpResponseNotFound()
		posts = Post.objects.filter(user=user)[int(counter):][:2]
		return JsonResponse([render_to_string("home/posts.html", {'post':post}, request) for post in posts], safe=False)
	return PermissionDenied()


def GetRegion(request):
	region_list = []
	for region in Country.objects.get(id = request.POST['id']).region.all():
		region_list.append((region.name, region.id))
	return JsonResponse(data = region_list, safe=False)

def GetCity(request):
	city_list = []
	for city in Region.objects.get(id = request.POST['id']).city.all():
		city_list.append((city.name, city.id))
	return JsonResponse(data = city_list, safe=False)

def GetArea(request):
	area_list = []
	for area in City.objects.get(id = request.POST['id']).area.all():
		area_list.append((area.name, area.id))
	return JsonResponse(data = area_list, safe=False)


@login_required
def my_profile(request):
    profile = request.user.profile
    user = profile.user
    address_book = AddressBook.objects.filter(user = user)
    studies = Education.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile).order_by('-score')
    files = Files.objects.filter(profile=profile).order_by('-title')
    potfolio = Potfolio.objects.filter(profile=profile)[:4]
    educ_form = EducationForm(request.POST)
    skill_form = SkillForm(request.POST, request.FILES, instance=request.user.profile)
    pf_form = PotfolioForm(request.POST, request.FILES, instance=request.user.profile)
    file_form = FileForm(request.POST, request.FILES, instance=request.user.profile)
    wall_form = ProfileWallForm(request.POST, request.FILES, instance=request.user.profile)
    dp_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
    context = {
        'profile': profile,
        'address_book':address_book,
        'skills':skills,
        'files':files,
        'studies':studies,
        'potfolio':potfolio,
        'educ_form': educ_form,
        'file_form':file_form,
        'skill_form': skill_form,
        'pf_form': pf_form,
        'wall_form': wall_form,
        'dp_form': dp_form,
        'user': user,
        'my_profile': user,
    }
    context['MAX_IMAGE_SIZE'] = settings.MAX_IMAGE_SIZE
    context['profile_seg'] = 'profile_seg'
    context['segment'] = 'Profile'

    return render(request, "profiles/my_profile.html", context)


@login_required
def ProfileView(request):
	if request.method == 'POST':
		if 'ab-name' in request.POST:
			if request.POST.get('default') == 'on':
				default = True
				for ab in AddressBook.objects.filter(default = 'True'):
					ab.default = False
					ab.save()
			else: default = False
			user = request.user
			name = request.POST['ab-name']
			phone = request.POST['ab-phone']
			if request.POST['ab-country'] != 'null':
				country = Country.objects.get(id = request.POST['ab-country'])
			else: country = None
			if request.POST['ab-region'] != 'null':
				region = Region.objects.get(id = request.POST['ab-region'])
			else: region = None
			if request.POST['ab-city'] != 'null':
				city = City.objects.get(id = request.POST['ab-city'])
			else: city = None
			if request.POST['ab-area'] != 'null':
				area = Area.objects.get(id = request.POST['ab-area'])
			else: area = None
			address = request.POST['ab-address']
			address_book = AddressBook(
				user=user, name=name, phone=phone, country=country, region=region, city=city, area=area, address=address, default=default
			)
			address_book.save()
			return redirect(request.path_info)
		if 'id' in request.POST:
			ab = AddressBook.objects.get(id = request.POST['id'])
			ab.name = request.POST['name']
			ab.phone = request.POST['phone']
			ab.address = request.POST['address']
			ab.country = Country.objects.get(id = request.POST['country'])
			ab.region = Region.objects.get(id = request.POST['region'])
			ab.city = City.objects.get(id = request.POST['city'])
			ab.area = Area.objects.get(id = request.POST['area'])
			ab.save()
			return redirect(request.path_info)
		if 'fname' in request.POST:
			usr = request.user.profile
			usr.first_name = request.POST['fname']
			usr.middle_name = request.POST['mname']
			usr.last_name = request.POST['lname']
			usr.picture = request.POST['picture']
			usr.image = request.POST['image']
			usr.save()
			return redirect(request.path_info)
		if 'phone' in request.POST:
			usr = request.user.profile
			usr.phone = request.POST['phone']
			usr.email = request.POST['email']
			usr.gender = request.POST['gender']
			usr.birth_date = request.POST['birth_date']
			usr.bio = request.POST['bio']
			usr.hide_sensitive = request.POST['hide_sensitive']
			usr.save()
			return redirect(request.path_info)
	total_cost = 0
	item = 0
	countrys = Country.objects.all()
	address_book = AddressBook.objects.filter(user = request.user)
	context = {
		'address_book': address_book,
		'countrys': countrys,
		'category_disable': True,
        'profset_seg': True
	}
	return render(request, 'profiles/profile.html', context)


def profile_view(request, profile_slug, *args, **kwargs):
    profile = Profile.objects.get(slug=profile_slug)
    user = profile.user
    p = Profile.objects.filter(slug=profile_slug).first()
    files = Files.objects.filter(profile=profile).order_by('-title')
    potfolio = Potfolio.objects.filter(profile=profile)[:4]
    studies = Education.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile)
    address_book = AddressBook.objects.filter(user = user)

    followers = user.circles.followers.all()

    if len(followers) == 0:
        is_following = False

    for follower in followers:
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False

    number_of_followers = len(followers)

    you = user
    user_posts = Post.objects.filter(user=you)
    contact_form = MessageForm()
    confirm_message = None

    if request.method=='POST':
        contact_form = MessageForm(request.POST or None)
        if contact_form.is_valid():
            contact_form = contact_form.save(commit=False)
            contact_form.sender = request.user
            contact_form.receiver = user
            contact_form.content_object = profile
            contact_form.save()
            messages.success(request, 'Your message has been sent!')
            contact_form = None
        confirm_message = "Thanks for reaching me. I will get right back to you very soon."
    context = {
        'skills':skills,
        'files':files,
        'studies':studies,
        'potfolio':potfolio,
        'address_book':address_book,
        'confirm_message': confirm_message,
        'profile': profile,
        'contact_form': contact_form,
        'user': user,
        'number_of_followers': number_of_followers,
        'is_following': is_following,
        'post_count': user_posts.count,
    }
    context['segment'] = 'Profile'

    return render(request, "profiles/user_profile.html", context)


def pot_detail(request, slug):
    pot_detail = get_object_or_404(Potfolio, slug=slug)
    profile = pot_detail.profile
    potfolio = Potfolio.objects.filter(profile=profile)[:4]
    user = pot_detail.profile.user
    context = {
        'potfolio': potfolio,
        'pot_detail': pot_detail,
    }
    pot_detail.view_count += 1
    pot_detail.save()
    context['segment'] = 'Profile'
    
    return render(request, 'profiles/fragments/potfolio_details.html', context)



@login_required(login_url="login")
def create_education(request):
    """
    Handle form submission to create new education entries for the user's profile.
    """
    education_form = EducationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and education_form.is_valid():
        user_profile = request.user.profile
        education_form.instance.profile = user_profile
        education_form.save()
        messages.success(request, 'Education details updated.')

    studies = Education.objects.filter(profile=request.user.profile)
    return render(request, 'profiles/fragments/education.html', {'studies': studies})


@require_http_methods(['DELETE'])
def delete_educ(request: HttpRequest, pk: int) -> HttpResponse:
    education = get_object_or_404(Education, pk=pk)
    profile = request.user.profile
    education.delete()
    studies = Education.objects.filter(profile=profile)
    return render(request, 'profiles/fragments/education.html', {'studies': studies})


@login_required(login_url="login")
def create_skill(request):
	skill_form = SkillForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if skill_form.is_valid():
			skill_form = skill_form.save(commit=False)
			skill_form.profile = request.user.profile
			skill_form.save()
			messages.success(request,f'Your profile has been updated!')
			return redirect('my_profile')
		else:
			return redirect('my_profile')
	else:
		return redirect('my_profile')


@login_required(login_url="login")
def create_potfolio(request):
	pf_form = PotfolioForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if pf_form.is_valid():
			pf_form = pf_form.save(commit=False)
			pf_form.profile = request.user.profile
			pf_form.save()
			messages.success(request,f'Your profile has been updated!')
			return redirect('my_profile')
		else:
			return redirect('my_profile')
	else:
		return redirect('my_profile')


@login_required(login_url="login")
def create_file(request):
	file_form = FileForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if file_form.is_valid():
			file_form = file_form.save(commit=False)
			file_form.profile = request.user.profile
			file_form.save()
			messages.success(request,f'Your profile has been updated!')
			return redirect('my_profile')
		else:
			return redirect('my_profile')
	else:
		return redirect('my_profile')


@login_required(login_url="login")
def create_wall(request):
    if request.method=='POST':
        wall_form = ProfileWallForm(request.POST, request.FILES, instance=request.user.profile)
        if wall_form.is_valid():
            wall_form.save()
            messages.success(request, 'Your wall paper has been updated!')
            return redirect('my_profile')
        else:
            return redirect('my_profile')
    else:
        return redirect('my_profile')


def save_temp_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect Padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
            os.mkdir(settings.TEMP + "/" + str(user.pk))
        url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_IMAGE_NAME)
        storage = files.FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print("exception: " + str(e))
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_temp_image_from_base64String(imageString, user)
    return None


def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get('image')
            url = save_temp_image_from_base64String(imageString, user)
            img = cv2.imread(url)
            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            cv2.imwrite(url, crop_img)
            user.profile.picture.delete()
            user.profile.picture.save("profile_image.png", files.File(open(url, 'rb')))
            user.profile.save()

            payload['result'] = "Success"
            payload['cropped_profile_image'] = user.profile.picture.url
            os.remove(url)
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    return HttpResponse(json.dumps(payload), content_type="application/json")


def crop_wall_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get('image')
            url = save_temp_image_from_base64String(imageString, user)
            img = cv2.imread(url)
            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            cv2.imwrite(url, crop_img)
            user.profile.image.delete()
            user.profile.image.save("profile_cover_image.png", files.File(open(url, 'rb')))
            user.profile.save()

            payload['result'] = "Success"
            payload['cropped_profile_image'] = user.profile.image.url
            os.remove(url)
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    return HttpResponse(json.dumps(payload), content_type="application/json")
