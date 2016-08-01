from django.shortcuts import render
from django.template import RequestContext

from website.models import Category
from website.models import Page
from django.contrib.auth.models import User
from website.models import UserProfile
from website.models import UserForm, UserProfileForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from amikar2.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'index.html', context_dict)

def product_view(request):
    return render(request, 'product.html')

def login_view(request):
    return render(request, 'login.html')


def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'category.html', context_dict)

def register(request):
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
                uform = UserForm(data = request.POST)
                pform = UserProfileForm(data = request.POST)
                if uform.is_valid() and pform.is_valid():
                        user = uform.save()
                        # form brings back a plain text string, not an encrypted password
                        pw = user.password
                        # thus we need to use set password to encrypt the password string
                        user.set_password(pw)
                        user.save()
                        profile = pform.save(commit = False)
                        profile.user = user
                        registered = True
                else:
                        print uform.errors, pform.errors
        else:
                uform = UserForm()
                pform = UserProfileForm()

        return render_to_response('register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect("/")
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.",RequestContext(request))
          else:
              # Return an 'invalid login' error message.
              print  "invalid login details"
              return render_to_response('login.html',{},context)

    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('login.html', {}, RequestContext(request))

@login_required
def restricted(request):
    return HttpResponse('since you are an authenticated user you can view this restricted page.',RequestContext(request))