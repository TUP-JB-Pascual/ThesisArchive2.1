from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
import os
import pymupdf
import datetime
from django.db import transaction
from django.db.models.signals import post_delete, pre_delete, post_save, pre_save
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from taggit.managers import TaggableManager

def rename_pdf(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.title, ext)
    #filename = "%s_%s.%s" % (instance.title, filetype, ext)
    return os.path.join('thesis_pdf', filename)

class Thesis(models.Model):
    STATE_APPROVED = 'APPROVED'
    STATE_REJECTED = 'REJECTED'
    STATE_PENDING = 'PENDING'
    
    status_choices = (
        (STATE_APPROVED, 'Approved'),
        (STATE_REJECTED, 'Rejected'),
        (STATE_PENDING, 'Pending')
    )
    
    REJECT_TITLE_ERROR = 'Invalid Title'
    REJECT_AUTHOR_ERROR = 'Invalid Name'    
    REJECT_FILE_ERROR = 'Invalid File'
    REJECT_SUBMIT_ERROR = 'Incomplete Detail'


    reject_choices = (
        (REJECT_TITLE_ERROR, 'Incorrect Title was submitted'),
        (REJECT_AUTHOR_ERROR, 'Typographical Error in the name of one or more Author(s)'),
        (REJECT_FILE_ERROR, 'Problem with the Uploaded File'),
        (REJECT_SUBMIT_ERROR, 'Information that was submitted was either incomplete or incorrect')
    )

    upload_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField()
    title = models.TextField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    authors = models.TextField(max_length=255)
    poster = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='thesis')
    pdf_file = models.FileField(upload_to=rename_pdf, max_length=500, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    tags = TaggableManager()
    visits = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    status = models.CharField(max_length=10, choices=status_choices, default=STATE_PENDING)
    decision_date = models.DateField(default=datetime.date.today())
    rejection_reason = models.CharField(max_length=50, choices=reject_choices, default="", blank=True, null=True)

    def __str__(self):
        return(f"{self.title} by {self.poster}")
    
    def get_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        number = 1
        while Thesis.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{number}'
            number += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('thesis_detail', kwargs={'slug': self.slug})
    
    def generate_apa(self):
        """Generates an APA citationith multiple authors."""
        publisher = 'Technological University of the Philippines - Cavite'
        url = 'https://jerichogianjohn1.pythonanywhere.com'
        year = self.published_date.year
        author_list = self.authors.splitlines()
        formatted_authors = []
        for author in author_list:
            author = author.split(', ')
            print(author)
            formatted_authors.append(f"{author[0]}, {author[1][0]}.")
            print(formatted_authors)
            #author[0] - last name
            #author[1] - first name

        # Combine authors with "&" in APA format
        if len(formatted_authors) > 1:
            authors_str = ', '.join(formatted_authors[:-1]) + ' & ' + formatted_authors[-1]
        else:
            authors_str = formatted_authors[0]

        apa_citation = f"{authors_str} ({year}). {self.title}. *{publisher}*. {url}"
        return apa_citation
    
    def generate_mla(self):
        """Generates MLA formatted citation with multiple authors."""
        publisher = 'Technological University of the Philippines - Cavite'
        url = 'https://jerichogianjohn1.pythonanywhere.com'
        year = self.published_date.year
        author_list = self.authors.splitlines()
        if len(author_list) > 1:
            authors_str = ', '.join(author_list[:-1]) + ' and ' + author_list[-1]
        else:
            authors_str = author_list[0]
        mla_citation = f"{authors_str}. \"{self.title}.\" *{publisher}*, {year}, {url}."
        return mla_citation
       

@receiver(post_save, sender=Thesis)
def create_extra_pdf(sender, instance, created, *args, **kwargs):
    if created:
        pdf_name = str(settings.MEDIA_ROOT) + '/' + instance.pdf_file.name
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
            watermark_img = str(settings.MEDIA_ROOT) + '/' + 'samplemark.png'
            page.insert_image(page.bound(),filename=watermark_img, overlay=True)
        water_pdf_name = pdf_name.split('.')
        water_pdf_name = water_pdf_name[0] + '_water.' + water_pdf_name[1]
        doc.save(water_pdf_name) # save the document with a new filename
        # WATERMARK END

        # SAVE ABSTRACT
        doc.select([abstract_page_num])
        abstract_pdf_name = pdf_name.split('.')
        abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
        doc.save(abstract_pdf_name)
        doc.close()

@receiver(post_delete, sender=Thesis)
def delete_extra_pdf(sender, instance, *args, **kwargs):
    pdf_name = str(settings.MEDIA_ROOT) + '/' + instance.pdf_file.name
    # FOR ABSTRACT
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
        # FOR PDF
    if os.path.exists(pdf_name):
        os.remove(pdf_name)
        print(pdf_name, "has been deleted.")

class TempURL(models.Model):
    STATE_EXPIRED = 'Expired'
    STATE_USED = 'Used'
    STATE_VALID = 'Valid'
    STATE_DNE = 'Does Not Exist'

    STATE_APPROVED = 'Approved'
    STATE_REJECTED = 'Rejected'
    STATE_PENDING = 'Pending'
    
    url_state_choices = (
        (STATE_EXPIRED, 'Expired'),
        (STATE_USED, 'Used'),
        (STATE_VALID, 'Valid'),
        (STATE_DNE, 'Does Not Exist'),
    )

    status_choices = (
        (STATE_APPROVED, 'Approved'),
        (STATE_REJECTED, 'Rejected'),
        (STATE_PENDING, 'Pending')
    )

    REJECT_EMAIL_ERROR = 'Invalid Email'
    REJECT_NAME_ERROR = 'Invalid Name'    
    REJECT_FILE_ERROR = 'Invalid File'
    REJECT_CLARITY_ERROR = 'Blurred ID'

    url_reject_choices = (
        (REJECT_EMAIL_ERROR, 'Invalid Email is used'),
        (REJECT_NAME_ERROR, 'Typographical Error in the name of the requestor'),
        (REJECT_FILE_ERROR, 'Problem in the Uploaded File'),
        (REJECT_CLARITY_ERROR, 'ID Submitted is blurred/pixelated/unreadable')
    )

    url_key = models.CharField(max_length=100, unique=True)
    title = models.TextField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    pdf_file = models.FileField(upload_to='temporary_pdfs/', max_length=500)
    request_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=datetime.datetime.today())
    # null=True, default=None

    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_pic = models.ImageField(upload_to='request_id/',
                                validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
                                null=False, blank=False)

    status = models.CharField(max_length=10, choices=status_choices, default=STATE_PENDING)
    url_status = models.CharField(max_length=15, choices=url_state_choices, default=STATE_DNE)
    decision_date = models.DateTimeField(default=datetime.date.today())
    rejection_reason = models.CharField(max_length=50, choices=url_reject_choices, default="", blank=True, null=True)

    # null=True, default=None

    def is_expired(self):
        """Check if the URL has expired."""
        return timezone.now() > self.expiration_date
    
    def __str__(self):
        return f"PDF File: {self.pdf_file.name} (Expires: {self.expiration_date})"
    
    def get_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        number = 1
        while Thesis.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{number}'
            number += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        return super().save(*args, **kwargs)
