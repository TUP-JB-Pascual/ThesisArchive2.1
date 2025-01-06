from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import os
import pymupdf
import datetime
import random
import string
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from .models import TempURL
from .forms import RequestForm, ThesisRejectReasonForm, RequestRejectReasonForm

from django.http import FileResponse, HttpResponse, JsonResponse
from django.conf import settings

User = get_user_model()

from .forms import ThesisForm
from .models import Thesis

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.template.loader import render_to_string

from taggit.models import Tag

def custom_404(request, exception):
    return HttpResponseNotFound(render_to_string('404.html', {}))

@login_required(login_url='user/login/')
def DashboardView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        current_user = request.user
        # Pending Proj
        thesis_pending_count = Thesis.objects.filter(status='PENDING').count()
        # Pending Req
        request_pending_count = TempURL.objects.filter(status='PENDING').count()

        # TODAY'S DATE
        today_date = datetime.date.today()
        this_month = today_date.month

        ### WEEKLY REPORT ###
        # This week's START and END date
        # Calculate the start of the week (Sunday is day 0)
        start_of_week = today_date - datetime.timedelta(days=today_date.weekday())  # Adjust to Sunday - 6
        # Calculate the end of the week (Saturday is day 6)
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Saturday is 6 days after Sunday

        modified_thesis_this_week = Thesis.objects.filter(
            decision_date__gte=datetime.datetime.combine(start_of_week, datetime.time.min),  # Start of the week
            decision_date__lte=datetime.datetime.combine(end_of_week, datetime.time.max)   # End of the week
        )
        modified_request_this_week = TempURL.objects.filter(
            decision_date__gte=datetime.datetime.combine(start_of_week, datetime.time.min),  # Start of the week
            decision_date__lte=datetime.datetime.combine(end_of_week, datetime.time.max)   # End of the week
        )
        # Thesis Week Mod Count
        modified_thesis_this_week_rejected_count = modified_thesis_this_week.filter(status='REJECTED').count()
        modified_thesis_this_week_approved_count = modified_thesis_this_week.filter(status='APPROVED').count()
        # Request Week Mod Count
        modified_request_this_week_rejected_count = modified_request_this_week.filter(status='REJECTED').count()
        modified_request_this_week_approved_count = modified_request_this_week.filter(status='APPROVED').count()

        
        ### MONTHLY REPORT ###
        modified_thesis_this_month = Thesis.objects.filter(decision_date__month=this_month)
        modified_request_this_month = TempURL.objects.filter(decision_date__month=this_month)
        # Thesis Month Mod Count
        modified_thesis_this_month_rejected_count = modified_thesis_this_month.filter(status='REJECTED').count()
        modified_thesis_this_month_approved_count = modified_thesis_this_month.filter(status='APPROVED').count()
        # Request Month Mod Count
        modified_request_this_month_rejected_count = modified_request_this_month.filter(status='REJECTED').count()
        modified_request_this_month_approved_count = modified_request_this_month.filter(status='APPROVED').count()


        context = {'thesis_pending_count': thesis_pending_count, 
                   'request_pending_count': request_pending_count,

                   'modified_thesis_this_week_approved_count': modified_thesis_this_week_approved_count,
                   'modified_thesis_this_week_rejected_count': modified_thesis_this_week_rejected_count,

                   'modified_request_this_week_approved_count': modified_request_this_week_approved_count,
                   'modified_request_this_week_rejected_count': modified_request_this_week_rejected_count,

                   'modified_thesis_this_month_approved_count': modified_thesis_this_month_approved_count,
                   'modified_thesis_this_month_rejected_count': modified_thesis_this_month_rejected_count,

                   'modified_request_this_month_approved_count': modified_request_this_month_approved_count,
                   'modified_request_this_month_rejected_count': modified_request_this_month_rejected_count,
                   }
        return render(request, 'dashboard.html', context)
    else:
        return RepositoryView(request)

@login_required(login_url='user/login/')
def RepositoryView(request):
    if request.user.is_authenticated:
        current_user = request.user
        current_user_thesis = Thesis.objects.filter(poster=current_user)
        rejectedThesisList = current_user_thesis.filter(status=Thesis.STATE_REJECTED)
        pendingThesisList = current_user_thesis.filter(status=Thesis.STATE_PENDING)
        approvedThesisList = current_user_thesis.filter(status=Thesis.STATE_APPROVED)
        context = {'rejectedThesisList': rejectedThesisList, 'pendingThesisList': pendingThesisList, 'approvedThesisList': approvedThesisList}
        return render(request, 'repository.html', context)

class ThesisPublishView(LoginRequiredMixin, generic.CreateView):
    model = Thesis
    template_name = 'thesis_publish.html'
    form_class = ThesisForm
    login_url = '/user/login/'
    #messages.success(request, "Upload Successful.")

    def form_valid(self, form):
        form.instance.poster = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['poster'] = self.request.user.id
        return initial
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)

class ThesisListView(LoginRequiredMixin, generic.ListView):
    model = Thesis
    template_name = 'thesis_list.html'
    context_object_name = 'thesis_list'
    login_url = '/user/login/'
    #paginate_by = 10

    def get_queryset(self):
        status_filter = self.kwargs.get('status_filter')
        thesis_list = Thesis.objects.filter(status=status_filter)
        return thesis_list

    def get_context_data(self, **kwargs):
        status_filter = self.kwargs.get('status_filter')
        context = super().get_context_data(**kwargs)
        context['status_filter'] = status_filter.title()
        context['reject_choices'] = Thesis.reject_choices
        return context

class XFrameOptionsExemptMixin:
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def ThesisDetailView(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug)
    abstract_pdf_name = thesis.pdf_file.name
    abstract_pdf_name = abstract_pdf_name.split('.')
    abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
    if thesis.status == thesis.STATE_APPROVED:
        thesis.visits += 1
        thesis.save()
    apa_citation = thesis.generate_apa()
    mla_citation = thesis.generate_mla()
    print(thesis.pdf_file)
    thesis_authors = []
    authors_list = thesis.authors.splitlines()
    if len(authors_list) > 1:
        thesis_authors = ', '.join(authors_list[:-1]) + ' and ' + authors_list[-1]
    else:
        thesis_authors = authors_list[0]
    context = {'thesis': thesis, 'thesis_authors': thesis_authors, 'abstract_pdf_name': abstract_pdf_name, 'apa_citation':apa_citation, 'mla_citation':mla_citation, 'reject_choices': Thesis.reject_choices}
    if request.method == 'POST':
        form = ThesisRejectReasonForm(request.POST, instance=thesis)
        if form.is_valid():
            form.save()
            ThesisReject(request, slug)
            context['form'] = form
            return render(request, 'thesis_detail.html', context)
    else:
        form = ThesisRejectReasonForm(instance=thesis)
        context['form'] = form
    return render(request, 'thesis_detail.html', context)

def ThesisApprove(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug)
    thesis.status = thesis.STATE_APPROVED
    thesis.save()
    messages.success(request, f"You have approved {thesis.title}.")
    return redirect('thesis_detail', slug=slug)  # Redirect to a user list or user detail page

def ThesisReject(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug)
    thesis.status = thesis.STATE_REJECTED
    thesis.save()
    messages.success(request, f"You have rejected {thesis.title}.")
    return redirect('thesis_detail', slug=slug)  # Redirect to a user list or user detail page

def ThesisUpdateView(request, slug):
    if request.user.is_authenticated:
        instance = Thesis.objects.get(slug=slug)
        form = ThesisForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            current_val = Thesis.objects.get(slug=slug)
            update_delete(current_val.pdf_file.name)
            form.save()
            create_update_pdf(instance.pdf_file.name)
            return redirect('thesis_detail', slug = instance.slug)
        context = {'form': form}
        return render(request, 'thesis_update.html', context)
    else:
        messages.success(request, "You must be logged in")
        return ('login')
    
def update_delete(pdf_name):
    pdf_name = 'media/' + pdf_name
    if os.path.exists(pdf_name):
        os.remove(pdf_name)
        print(pdf_name, " has been deleted.")
        abstract_pdf_name = pdf_name.split('.')
        abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
        if os.path.exists(abstract_pdf_name):
            os.remove(abstract_pdf_name)
            print(abstract_pdf_name, " has been deleted.")
        # FOR WATERMARK
        water_pdf_name = pdf_name.split('.')
        water_pdf_name = water_pdf_name[0] + '_water.' + water_pdf_name[1]
        if os.path.exists(water_pdf_name):
            os.remove(water_pdf_name)
            print(water_pdf_name, " has been deleted.")

def create_update_pdf(pdf_name):
    pdf_name = 'media/' + pdf_name
    doc = pymupdf.open(pdf_name)
    # GET ABSTRACT PAGE
    abstract_page_num = 0
    for i in range(doc.page_count):
        if doc.search_page_for(i, 'Abstract', quads=False):
            abstract_page_num = i
            break
    # WATERMARK
    for page_index in range(abstract_page_num + 1, doc.page_count): # iterate over pdf pages
        page = doc[page_index] # get the page
        # insert an image watermark from a file name to fit the page bounds
        # page.insert_image(page.bound(),filename="watermark.png", overlay=True)
        page.insert_image(page.bound(),filename='media/samplemark.png', overlay=True)
    water_pdf_name = pdf_name.split('.')
    water_pdf_name = water_pdf_name[0] + '_water.' + water_pdf_name[1]
    doc.save(water_pdf_name) # save the document with a new filename
    # WATERMARK END

    # SAVE ABSTRACT
    doc.select([abstract_page_num])
    abstract_pdf_name = pdf_name.split('.')
    abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
    doc.save(abstract_pdf_name)

class ThesisDeleteView(generic.DeleteView):
    model = Thesis
    template_name = 'thesis_delete.html'
    success_url = reverse_lazy('thesis_list')

def generate_random_key(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_temp_url(slug, email, first_name, last_name):
    requested_pdf = get_object_or_404(Thesis, slug=slug)
    requested_pdf.downloads += 1
    requested_pdf.save()
    title = requested_pdf.title
    pdf_file_path = requested_pdf.pdf_file.name
    pdf_file_path = pdf_file_path.split('.')
    pdf_file_path = pdf_file_path[0] + '_water.' + pdf_file_path[1]
    url_key = generate_random_key()
    expiration_date = timezone.now() + timedelta(days=3)
    pdf_file = TempURL.objects.create(
        url_key=url_key,
        title=title,
        pdf_file=pdf_file_path,
        expiration_date=expiration_date,
        email = email,
        first_name = first_name,
        last_name = last_name
    )

def temp_url_redirect(request, url_key):
    try:
        temp_pdf = get_object_or_404(TempURL, url_key=url_key)
        if temp_pdf.status == temp_pdf.STATE_PENDING:
            return render(request, 'request_status.html', {'temp_pdf': temp_pdf})
        elif temp_pdf.status == temp_pdf.STATE_REJECTED:
            return render(request, 'request_status.html', {'temp_pdf': temp_pdf})
        elif temp_pdf.status == temp_pdf.STATE_APPROVED:
            if temp_pdf.is_expired():
                if temp_pdf.url_status != temp_pdf.STATE_EXPIRED:
                    temp_pdf.url_status = temp_pdf.STATE_EXPIRED
                    temp_pdf.save()
                # GO TO EXPIRED PAGE
                return render(request, 'request_status.html', {'temp_pdf': temp_pdf})
            elif temp_pdf.url_status == temp_pdf.STATE_EXPIRED:
                return render(request, 'request_status.html', {'temp_pdf': temp_pdf})
            elif temp_pdf.url_status == temp_pdf.STATE_USED:
                return render(request, 'request_status.html', {'temp_pdf': temp_pdf})
            else:
                pdf_file_name = temp_pdf.pdf_file.name.split('_water')
                pdf_file = "".join(pdf_file_name)
                if os.path.exists(temp_pdf.pdf_file.path):
                    thesis_obj = Thesis.objects.get(pdf_file=pdf_file)
                    context = {'thesis_obj': thesis_obj, 'pdf': temp_pdf, 'temp_url': url_key}
                    return render(request, 'request_pdf.html', context)
                    #return render(request, 'thesis_detail.html', {'thesis': thesis, 'abstract_pdf_name': abstract_pdf_name})
                    #return FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
                # GO TO PDF NOT FOUND / REQUEST AGAIN
                return render(request, 'request_status.html', {'status': 'DOES NOT EXIST'})
        else:
            return render(request, 'request_status.html', {'status': 'DOES NOT EXIST'})
    except TempURL.DoesNotExist:
        # GO TO URL NOT EXIST
        return render(request, 'request_status.html', {'status': 'DOES NOT EXIST'})

def ThesisDownload(request, source, slug):
    if source == 'thesis':
        thesis = get_object_or_404(Thesis, slug=slug)
    elif source == 'request':
        thesis = get_object_or_404(TempURL, slug=slug)
    else:
        raise Http404("Invalid Request.")
    pdf = thesis.pdf_file.path
    file_path = os.path.join(settings.MEDIA_ROOT, pdf)  # Use the path where your file is stored
    with open(file_path, 'rb') as file:
        # Create an HTTP response with the appropriate content type for PDF
        response = HttpResponse(file.read(), content_type='application/pdf')
        # Optionally, set the filename for the downloaded file
        response['Content-Disposition'] = 'attachment; filename="thesis.pdf"'
    return response

@login_required(login_url='user/login/')
def ThesisRequestView(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug)
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            generate_temp_url(slug, email, first_name, last_name)
            messages.success(request, f'Thank you, {first_name} {last_name}! Your request has been sent.')
            return redirect('thesis_detail', slug=slug)
        else:
            messages.error(request, 'There was an error with your form submission. Please try again.')
    else:
        form = RequestForm()
    return render(request,'thesis_request.html', {'form': form, 'thesis': thesis})

class ThesisRequestListView(LoginRequiredMixin, generic.ListView):
    model = TempURL
    template_name = 'request_list.html'
    context_object_name = 'request_list'
    login_url = '/user/login/'
    #paginate_by = 10

    def get_queryset(self):
        status_filter = self.kwargs.get('status_filter')
        request_list = TempURL.objects.filter(status=status_filter)
        return request_list

    def get_context_data(self, **kwargs):
        status_filter = self.kwargs.get('status_filter')
        context = super().get_context_data(**kwargs)
        context['status_filter'] = status_filter.title()
        context['url_state_choices'] = TempURL.url_state_choices
        context['url_reject_choices'] = TempURL.url_reject_choices
        return context

# ACCEPT
@login_required(login_url='user/login/')
def RequestDetailView(request, slug):
    thesis_request = get_object_or_404(TempURL, slug=slug)
    context = {'thesis_request': thesis_request}
    if request.method == 'POST':
        form = RequestRejectReasonForm(request.POST, instance=thesis_request)
        if form.is_valid():
            form.save()
            RequestReject(request, slug)
            context['form'] = form
            return redirect('request_list', status_filter=thesis_request.STATE_REJECTED)
    else:
        form = RequestRejectReasonForm(instance=thesis_request)
        context['form'] = form
    return render(request, 'request_detail.html', context)

def RequestApprove(request, slug):
    thesis_request = get_object_or_404(TempURL, slug=slug)
    # Email content
    subject = "Thesis Request Approved"
    message = "Good day! {} {}, your request for a PDF copy of the thesis titled {} has been accepted. DO NOT CLICK ON ANOTHER TAB UNTIL YOU HAVE CLICKED 'DOWNLOAD', IT WILL CLOSE!!! This link will expire in three days. http://127.0.0.1:8000/temp/pdf/{}".format(thesis_request.first_name, thesis_request.last_name, thesis_request.title, thesis_request.url_key)
    recipient_list = [thesis_request.email]  # The recipient's email

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
    messages.success(request, f"You have approved the Request ID #{thesis_request.pk}.")
    messages.success(request, "Request Acceptance Email has been sent to {}.".format(thesis_request.email))
    thesis_request.status = thesis_request.STATE_APPROVED
    thesis_request.url_status = thesis_request.STATE_VALID
    thesis_request.save()
    return redirect('request_list', status_filter=thesis_request.STATE_APPROVED)  # Redirect to a user list or user detail page

def RequestReject(request, slug):
    thesis_request = get_object_or_404(TempURL, slug=slug)
    print(thesis_request.rejection_reason)
    reason = ''
    if thesis_request.rejection_reason != '':
        reason = thesis_request.rejection_reason
        for value, name in thesis_request.url_reject_choices:
            if reason == value:
                reason = name
    print(reason)
    # Email content
    subject = "Thesis Request Denied"
    message = "Good day! {} {}, I'm sorry to inform you that your request for a PDF copy of the thesis titled {} has been rejected. Please re-submit a new request with correct information. \nReason: \n   -{}".format(thesis_request.first_name, thesis_request.last_name, thesis_request.title, reason)
    recipient_list = [thesis_request.email]  # The recipient's email
    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
    messages.success(request, f"You have rejected the Request ID #{thesis_request.pk}.")
    messages.success(request, "Request Rejection Email has been sent to {}.".format(thesis_request.email))
    thesis_request.status = thesis_request.STATE_REJECTED
    thesis_request.save()
    return redirect('request_list', status_filter=thesis_request.STATE_REJECTED)

def window_blur_method(request, temp_url):
    try:
        temp_pdf = TempURL.objects.get(url_key=temp_url)
        if request.method == 'POST':
            # You can process any data sent from the client here
            message = request.POST.get('message', 'No message')
            print(f"Received message: {message}")
            temp_pdf.url_status = temp_pdf.STATE_USED
            temp_pdf.save()
            # You can trigger other server-side actions here (e.g., logging, saving data, etc.)
            # Returning a response to the client
            return JsonResponse({'status': 'success', 'message': 'Method triggered successfully!'})
        
    except TempURL.DoesNotExist:
        raise Http404("Temporary PDF URL does not exist.")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

def tags_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'tags_list.html', context)

def tags_filter(request, tag_slug):
    current_tag = Tag.objects.filter(slug=tag_slug).values_list('name', flat=True)
    filtered_thesis_by_tag = Thesis.objects.filter(tags__name__in=current_tag)
    context = {'tag_slug': tag_slug, 'filtered_thesis_by_tag': filtered_thesis_by_tag}
    return render(request, 'tags_filter.html', context)

'''
class tags_filter(generic.ListView):
    model = Thesis
    template_name = 'tags_filter.html'
    context_object_name = 'thesis'
    
    def get_queryset(self):
        return Thesis.objects.filter(tags__slug=self.kwargs.get('tag_slug'))
'''

#improvement
    # Reason for rejection
    # CRON - after some delay - do code -> DELETE -> APPROVE
        # DELETE = date.today > expire -> DELETE (delay 7 days)
        # APPROVE = date.today < expire -> APPROVE
