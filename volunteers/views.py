import datetime

from models import Volunteer, VolunteerTask, VolunteerCategory, VolunteerTalk, TaskCategory, TaskTemplate, Task, Track, Talk, Edition
from forms import EditProfileForm, SignupForm

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from summit.schedule.models import Summit

#from userena.utils import get_user_model
#from userena.forms import SignupFormOnlyEmail
#from userena.decorators import secure_required
#from userena import signals as userena_signals
#from userena import settings as userena_settings
#from userena.views import ExtraContextTemplateView, get_profile_model

#from guardian.decorators import permission_required_or_403

import csv
import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape

# decorators

def edition_required(func):
    def inner(request, edition_name, *args, **kwds):
        edition = get_object_or_404(Edition, name=edition_name)
        return func(request, edition, *args, **kwds)
    inner.__name__ = func.__name__
    return inner

def volunteer_required(func):
    def inner(request, edition_name, *args, **kwds):
        edition = get_object_or_404(Edition, name=edition_name)
        try:
            if request.user.is_authenticated():
                volunteer = get_object_or_404(Volunteer, user=request.user)
            else:
                return redirect('promo', edition_name)
        except ObjectDoesNotExist:
            return redirect('promo', edition_name)
        return func(request, edition, volunteer, *args, **kwds)
    inner.__name__ = func.__name__
    return inner

def summit_of(edition):
    try:
        return Summit.objects.get(name=edition.name)
    except ObjectDoesNotExist:
        return None

def volunteer_of(user):
    try:
        return Volunteer.objects.get(user__username__iexact=user.username)
    except Volunteer.DoesNotExist:
        return None


def check_profile_completeness(request, volunteer):
    if request.user != volunteer.user:
        return True
    if not volunteer.check_mugshot():
        messages.warning(request, _("Looks like we don't have your beautiful smile in our system. Be so kind to upload a mugshot in your profile page. :)"), fail_silently=True)
    if not volunteer.mobile_nbr:
        messages.warning(request, _("Hey there! It seems you didn't give us a phone number. Please update your profile, or be the last to know the pizza's here..."), fail_silently=True)

@edition_required
def faq(request, edition):
    context = { 'edition': edition }
    return render(request, 'static/faq.html', context)

@edition_required
def promo(request, edition):
    context = { 'edition': edition }
    return render(request, 'static/promo.html', context)

@volunteer_required
def talk_detailed(request, edition, volunteer, talk_id):
    talk = get_object_or_404(Talk, id=talk_id)
    context = { 'talk': talk, 'edition': edition }
    return render(request, 'volunteers/talk_detailed.html', context)

@edition_required
def task_detailed(request, edition, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.talk:
        current_tasks = Task.objects.filter(talk=task.talk)
    else:
        current_tasks = Task.objects.filter(id = task_id)

    if request.user.is_authenticated():
        volunteer = Volunteer.objects.get(user=request.user)
    else:
        volunteer = None

    if request.method == 'POST' and volunteer:
        # get the checked tasks
        task_ids = request.POST.getlist('task')
        # unchecked boxes, delete him/her from the task
        for task in current_tasks.exclude(id__in=task_ids):
            VolunteerTask.objects.filter(task=task, volunteer=volunteer).delete()
        # checked boxes, add the volunteer to the tasks when he/she is not added
        for task in current_tasks.filter(id__in=task_ids):
            VolunteerTask.objects.get_or_create(task=task, volunteer=volunteer)
        return redirect('task_detailed', edition_name=edition.name, task_id=task_id)
    context = { 'task': task, 'volunteer': volunteer, 'edition': edition }
    if volunteer:
        context['checked'] = {}
        for task in current_tasks:
            context['checked'][task.id] = 'checked' if volunteer in task.volunteers.all() else ''
    context['related_tasks'] = current_tasks
    return render(request, 'volunteers/task_detailed.html', context)

@volunteer_required
def talk_list(request, edition, volunteer):
    # when the user submitted the form
    if request.method == 'POST':
        # get the checked tasks
        talk_ids = request.POST.getlist('talk')

        # go trough all the talks that were checked
        for talk in Talk.objects.filter(id__in=talk_ids):
            # add the volunteer to the talk when he/she is not added
            VolunteerTalk.objects.get_or_create(talk=talk, volunteer=volunteer)

        # go trough all the not checked tasks
        for talk in Talk.objects.exclude(id__in=talk_ids):
            # delete him/her
            VolunteerTalk.objects.filter(talk=talk, volunteer=volunteer).delete()

#        # show success message when enabled
#        if userena_settings.USERENA_USE_MESSAGES:
#            messages.success(request, _('Your talks have been updated.'), fail_silently=True)

        # redirect to prevent repost
        return redirect('talk_list', edition_name=edition.name)

    # group the talks according to tracks
    context = { 'tracks': {}, 'checked': {}, 'edition': edition }
    tracks = Track.objects.filter(edition=edition)
    for track in tracks:
        context['tracks'][track.title] = Talk.objects.filter(track=track)

    # mark checked, attending talks
    for talk in Talk.objects.filter(volunteers=volunteer):
        context['checked'][talk.id] = 'checked'

    return render(request, 'volunteers/talks.html', context)

@login_required
@edition_required
def category_schedule_list(request, edition):
    categories = TaskCategory.objects.filter(active=True)
    context = {'categories': SortedDict.fromkeys(categories, []), 'edition': edition}
    for category in context['categories']:
        context['categories'][category] = TaskTemplate.objects.filter(category=category)
    return render(request, 'volunteers/category_schedule_list.html', context)

@login_required
@edition_required
def task_schedule(request, edition, template_id):
    template = TaskTemplate.objects.filter(id=template_id)[0]
    tasks = Task.objects.filter(template=template, edition=Edition.get_current).order_by('date', 'start_time', 'end_time')
    context = {
        'template': template,
        'edition': edition,
        'tasks': SortedDict.fromkeys(tasks, {}),
    }
    for task in context['tasks']:
        context['tasks'][task] = Volunteer.objects.filter(tasks=task)
    return render(request, 'volunteers/task_schedule.html', context)

@login_required
@edition_required
def task_schedule_csv(request, edition, template_id):
    template = TaskTemplate.objects.filter(id=template_id)[0]
    tasks = Task.objects.filter(template=template, edition=Edition.get_current).order_by('date', 'start_time', 'end_time')
    response = HttpResponse(content_type='text/csv')
    filename = "schedule_%s.csv" % template.name
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    writer = csv.writer(response)
    writer.writerow(['Task', 'Volunteers', 'Day', 'Start', 'End', 'Volunteer', 'Nick', 'Email', 'Mobile'])
    for task in tasks:
        row = [
            task.name,
            "(%s/%s)" % (task.assigned_volunteers(), task.nbr_volunteers),
            task.date.strftime('%a'),
            task.start_time.strftime('%H:%M'),
            task.end_time.strftime('%H:%M'),
            '','','','',
        ]
        writer.writerow([unicode(s).encode("utf-8") for s in row])
        volunteers = Volunteer.objects.filter(tasks=task)
        for number, volunteer in enumerate(volunteers):
            row = [
                '', '', '', '', '',
                "%s %s" % (volunteer.user.first_name, volunteer.user.last_name),
                volunteer.user.username,
                volunteer.user.email,
                volunteer.mobile_nbr,
            ]
            writer.writerow([unicode(s).encode("utf-8") for s in row])
        row = [''] * 9
        writer.writerow([unicode(s).encode("utf-8") for s in row])
    return response

@edition_required
def task_list(request, edition):
    summit = get_object_or_404(Summit, name=edition.name)
    # get the signed in volunteer
    if request.user.is_authenticated():
        volunteer = Volunteer.objects.get(user=request.user)
    else:
        volunteer = None
        is_dr_manhattan = False
    current_tasks = Task.objects.filter(edition=edition)
    if volunteer:
        is_dr_manhattan, dr_manhattan_task_sets = volunteer.detect_dr_manhattan()
        dr_manhattan_task_ids = [x.id for x in set.union(*dr_manhattan_task_sets)] if dr_manhattan_task_sets else []
        ok_tasks = current_tasks.exclude(id__in=dr_manhattan_task_ids)
    else:
        ok_tasks = current_tasks
    throwaway = current_tasks.order_by('date').distinct('date')
    days = [x.date for x in throwaway]

    # when the user submitted the form
    if request.method == 'POST' and volunteer:
        # get the checked tasks
        task_ids = request.POST.getlist('task')

        # unchecked boxes, delete him/her from the task
        for task in current_tasks.exclude(id__in=task_ids):
            VolunteerTask.objects.filter(task=task, volunteer=volunteer).delete()

        # checked boxes, add the volunteer to the tasks when he/she is not added
        for task in current_tasks.filter(id__in=task_ids):
            VolunteerTask.objects.get_or_create(task=task, volunteer=volunteer)

#        # show success message when enabled
#        if userena_settings.USERENA_USE_MESSAGES:
#            messages.success(request, _('Your tasks have been updated.'), fail_silently=True)

        # redirect to prevent repost
        return redirect('task_list', edition_name=edition.name)

    # get the preferred and other tasks, preserve key order with srteddict for view
    context = {
        'tasks': SortedDict({}),
        'checked': {},
        'attending': {},
        'is_dr_manhattan': is_dr_manhattan,
        'edition': edition,
    }
    # get the categories the volunteer is interested in
    if volunteer:
        categories_by_task_pref = {
            'preferred tasks': TaskCategory.objects.filter(volunteer=volunteer, active=True),
            'other tasks': TaskCategory.objects.filter(active=True).exclude(volunteer=volunteer),
        }
        context['volunteer'] = volunteer
        context['dr_manhattan_task_sets'] = dr_manhattan_task_sets
        context['tasks']['preferred tasks'] = SortedDict.fromkeys(days, {})
        context['tasks']['other tasks'] = SortedDict.fromkeys(days, {})
    else:
        categories_by_task_pref = {
            # 'preferred tasks': [],
            'tasks': TaskCategory.objects.filter(active=True),
        }
        context['tasks']['tasks'] = SortedDict.fromkeys(days, {})
    context['user'] = request.user
    for category_group in context['tasks']:
        for day in context['tasks'][category_group]:
            context['tasks'][category_group][day] = SortedDict.fromkeys(categories_by_task_pref[category_group], [])
            for category in context['tasks'][category_group][day]:
                dct = ok_tasks.filter(template__category=category, date=day)
                context['tasks'][category_group][day][category] = dct

    # mark checked, attending tasks
    if volunteer:
        for task in current_tasks:
            context['checked'][task.id] = 'checked' if volunteer in task.volunteers.all() else ''
            context['attending'][task.id] = False

        # take the moderation tasks to talks the volunteer is attending
        for task in current_tasks.filter(talk__volunteers=volunteer):
            context['attending'][task.id] = True
        check_profile_completeness(request, volunteer)
    else:
        for task in current_tasks:
            context['attending'][task.id] = False
    
    context['days'] = [date.strftime("%Y-%m-%d") for date in summit.days()]
    return render(request, 'volunteers/tasks.html', context)


@volunteer_required
@edition_required
def task_grid(request, edition, volunteer, date):
    summit = get_object_or_404(Summit, name=edition.name)
    start_day = summit.as_localtime(
        datetime.datetime.strptime(date, "%Y-%m-%d")
    )
    next_day = start_day + datetime.timedelta(days=1)

    current_tasks = Task.objects.filter(edition=edition, date=date).order_by('start_time')
    rooms = sorted(set(current_tasks.values_list('room', flat=True).distinct()))
    #keys = sorted(set(current_tasks.values_list('start_time', flat=True)) & set(current_tasks.values_list('end_time', flat=True)))
    #slots = SortedDict(((key.hour, key.minute), [None]*len(rooms)) for key in keys)
    last_time = None
    slots = []

    for task in current_tasks:
        time = (task.start_time.hour, task.start_time.minute)
        talk = task.talk
        room = rooms.index(task.room)
        if time != last_time:
            slot = [time, [None]*len(rooms)]
            slots.append(slot)
            last_time = time
        else:
            slot = slots[-1]
        if not slot[1][room]:
            slot[1][room] = {'talk': talk, 'tasks': [], 'me': False}
        tsk = {'task': task, 'me_task': False, 'signin': False, 'needed': 0, 'optimal': 0, 'extra': 0, 'missing': 0}
        slot[1][room]['tasks'].append(tsk)
        if not slot[1][room]['me']:
           if VolunteerTask.objects.filter(task=task, volunteer=volunteer).exists():
               tsk['me_task'] = True
               slot[1][room]['me'] = True
        count = task.volunteers.count()
        if count < task.nbr_volunteers_min:
            tsk['needed'] = task.nbr_volunteers_min - count
            tsk['optimal'] = task.nbr_volunteers - task.nbr_volunteers_min
            tsk['extra'] = task.nbr_volunteers_max - task.nbr_volunteers
        elif count < task.nbr_volunteers:
            tsk['needed'] = 0
            tsk['optimal'] = task.nbr_volunteers - count
            tsk['extra'] = task.nbr_volunteers_max - task.nbr_volunteers
        elif count < task.nbr_volunteers_max:
            tsk['needed'] = 0
            tsk['optimal'] = 0
            tsk['extra'] = task.nbr_volunteers_max - count
        tsk['missing'] = tsk['needed'] + tsk['optimal'] + tsk['extra']
        if tsk['missing'] > 0:
            tsk['signin'] = not slot[1][room]['me']

    days = [date.strftime("%Y-%m-%d") for date in summit.days()]
    context = {'edition': edition, 'user': request.user, 'date': start_day, 'day': date, 'days': days,
               'rooms': rooms, 'slots': slots, 'container_size': "large-container"}
    return render(request, 'volunteers/tasks_grid.html', context)


def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

@login_required
@edition_required
def task_list_detailed(request, edition, username):
    context = {'edition': edition}
    current_tasks = Task.objects.filter(edition=Edition.get_current)
    # get the requested users tasks
    context['tasks'] = current_tasks.filter(volunteers__user__username=username)
    context['user'] = request.user
    context['profile_user'] = User.objects.filter(username=username)[0]
    volunteer = Volunteer.objects.filter(user__username=username)[0]
    context['volunteer'] = volunteer
    check_profile_completeness(request, volunteer)

    if request.POST:
        if 'print_pdf' in request.POST:
            # create the HttpResponse object with the appropriate PDF headers.
            context.update({ 'pagesize':'A4'})
            return render_to_pdf(request, 'volunteers/tasks_detailed.html', context)
        elif 'mail_schedule' in request.POST:
            volunteer.mail_schedule()
            messages.success(request, _('Your shedule has been mailed to %s.' % (volunteer.user.email,)),
                fail_silently=True)

    return render(request, 'volunteers/tasks_detailed.html', context)

@login_required
@edition_required
def signup(request, edition, signup_form=SignupForm,
           template_name='userena/signup_form.html', success_url=None,
           extra_context=None):
    """
        Signup of an account.

        Signup requiring a username, email and password. After signup a user gets
        an email with an activation link used to activate their account. After
        successful signup redirects to ``success_url``.

        :param signup_form:
            Form that will be used to sign a user. Defaults to userena's
            :class:`SignupForm`.

        :param template_name:
            String containing the template name that will be used to display the
            signup form. Defaults to ``userena/signup_form.html``.

        :param success_url:
            String containing the URI which should be redirected to after a
            successful signup. If not supplied will redirect to
            ``userena_signup_complete`` view.

        :param extra_context:
            Dictionary containing variables which are added to the template
            context. Defaults to a dictionary with a ``form`` key containing the
            ``signup_form``.

        **Context**

        ``form``
            Form supplied by ``signup_form``.
    """

    user = request.user
    volunteer = volunteer_of(user)

    if not volunteer:
        #summit = summit_of(edition)

        volunteer = Volunteer(
              user=user,
        )

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            volunteer = form.save()
            if edition in volunteer.editions.all():
                volunteer.editions.add(edition)
                volunteer = form.save()

            redirect_to = reverse('profile_detail', kwargs={'username': volunteer.user.username, 'edition_name': edition.name})
            return redirect(redirect_to)
    else:
        form = EditProfileForm(instance=volunteer)

    if not extra_context: extra_context = dict()
    extra_context['form'] = form
    extra_context['edition'] = edition
    return ExtraContextTemplateView.as_view(template_name=template_name, extra_context=extra_context)(request)

@secure_required
@login_required
@permission_required_or_403('change_profile', (get_profile_model(), 'user__username', 'username'))
@volunteer_required
def profile_edit(request, edition, volunteer, username, edit_profile_form=EditProfileForm,
                 template_name='userena/profile_form.html', success_url=None,
                 extra_context=None, **kwargs):
    """
        Edit profile.

        Edits a profile selected by the supplied username. First checks
        permissions if the user is allowed to edit this profile, if denied will
        show a 404. When the profile is successfully edited will redirect to
        ``success_url``.

        :param username:
            Username of the user which profile should be edited.

        :param edit_profile_form:

            Form that is used to edit the profile. The :func:`EditProfileForm.save`
            method of this form will be called when the form
            :func:`EditProfileForm.is_valid`.  Defaults to :class:`EditProfileForm`
            from userena.

        :param template_name:
            String of the template that is used to render this view. Defaults to
            ``userena/edit_profile_form.html``.

        :param success_url:
            Named URL which will be passed on to a django ``reverse`` function after
            the form is successfully saved. Defaults to the ``userena_detail`` url.

        :param extra_context:
            Dictionary containing variables that are passed on to the
            ``template_name`` template.  ``form`` key will always be the form used
            to edit the profile, and the ``profile`` key is always the edited
            profile.

        **Context**

        ``form``
            Form that is used to alter the profile.

        ``profile``
            Instance of the ``Profile`` that is edited.
    """
    user = get_object_or_404(User, username__iexact=username)

    profile = volunteer_of(user)

    user_initial = {'first_name': user.first_name, 'last_name': user.last_name}

    form = edit_profile_form(instance=profile, initial=user_initial)

    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=profile, initial=user_initial)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            # # go trough all the task categories for this volunteer
            # for category in TaskCategory.objects.all():
            # 	exists = VolunteerCategory.objects.filter(volunteer=profile, category=category)
            #     selected = form.cleaned_data.get('categories').filter(name=category.name)
            #     # when the category does not exist and was selected, add it
            #     if not exists and selected:
            #         profilecategory = VolunteerCategory(volunteer=profile, category=category)
            #         profilecategory.save()
            #     # when the category exists and was deselected, delete it
            #     elif exists and not selected:
            #         profilecategory = VolunteerCategory.objects.filter(volunteer=profile, category=category)
            #         profilecategory.delete()

            if success_url:
                # Send a signal that the profile has changed
                redirect_to = success_url
            else: redirect_to = reverse('profile_detail', kwargs={'username': volunteer.user.username, 'edition_name': edition.name})
            return redirect(redirect_to)

    if not extra_context: extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = profile
    extra_context['edition'] = edition
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)

@login_required
@edition_required
def profile_detail(request, edition, username,
    template_name="userena/profile_detail.html", #userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE,
    extra_context=None, **kwargs):
    """
        Detailed view of an user.

        :param username:
            String of the username of which the profile should be viewed.

        :param template_name:
            String representing the template name that should be used to display
            the profile.

        :param extra_context:
            Dictionary of variables which should be supplied to the template. The
            ``profile`` key is always the current profile.

        **Context**

        ``profile``
            Instance of the currently viewed ``Profile``.
    """
    user = get_object_or_404(User, username__iexact=username)
    current_tasks = Task.objects.filter(edition=edition)

    profile = volunteer_of(user)

    if not profile.can_view_profile(request.user):
        raise PermissionDenied
    if not extra_context: extra_context = dict()
    extra_context['edition'] = edition
    extra_context['profile'] = user.volunteer
    extra_context['tasks'] = current_tasks.filter(volunteers__user=user)
    extra_context['hide_email'] = True # userena_settings.USERENA_HIDE_EMAIL
    check_profile_completeness(request, user.volunteer)
    return ExtraContextTemplateView.as_view(template_name=template_name, extra_context=extra_context)(request)

class ProfileListView(ListView):
    """ Lists all profiles """
    context_object_name='profile_list'
    page=1
    paginate_by=50
    template_name="userena/profile_list.html" #userena_settings.USERENA_PROFILE_LIST_TEMPLATE
    extra_context=None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileListView, self).get_context_data(**kwargs)
        try:
            page = int(self.request.GET.get('page', None))
        except (TypeError, ValueError):
            page = self.page

#        if userena_settings.USERENA_DISABLE_PROFILE_LIST \
#           and not self.request.user.is_staff:
#            raise Http404

        if not self.extra_context: self.extra_context = dict()

        edition = Edition.objects.get(name=self.kwargs['edition_name'])
        context['edition'] = edition
        context['page'] = page
        context['paginate_by'] = self.paginate_by
        context['extra_context'] = self.extra_context

        return context

    def get_queryset(self):
        edition = Edition.objects.get(name=self.kwargs['edition_name'])
        queryset = Volunteer.objects.get_visible_profiles(self.request.user).select_related().extra(\
            select={'lower_name': 'lower(first_name)'}).order_by('lower_name')
        return queryset


# From Userena
class ExtraContextTemplateView(TemplateView):
    """ Add extra context to a simple template view """
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super(ExtraContextTemplateView, self).get_context_data(*args, **kwargs)
        if self.extra_context:
            context.update(self.extra_context)
        return context

    # this view is used in POST requests, e.g. signup when the form is not valid
    post = TemplateView.get

