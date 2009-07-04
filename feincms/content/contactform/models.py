from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(label=_('name'))
    email = forms.EmailField(label=_('email'))
    subject = forms.CharField(label=_('subject'))

    content = forms.CharField(widget=forms.Textarea, required=False,
        label=_('content'))


class ContactFormContent(models.Model):
    form = ContactForm

    email = models.EmailField()
    subject = models.CharField(max_length=200)

    class Meta:
        abstract = True
        verbose_name = _('contact form')
        verbose_name_plural = _('contact forms')

    @classmethod
    def initialize_type(cls, form=None):
        if form:
            cls.form = form

    def render(self, **kwargs):
        request = kwargs.get('request')

        if request.method=='POST':
            form = self.form(request.POST)

            if form.is_valid():
                send_mail(
                    self.subject,
                    render_to_string('content/contactform/email.txt', {
                        'data': form.cleaned_data,
                        }),
                    form.cleaned_data['email'],
                    [self.email],
                    fail_silently=True)

                return render_to_string('content/contactform/thanks.html')
        else:
            form = self.form(initial={'subject': self.subject})

        return render_to_string('content/contactform/form.html', {
            'content': self,
            'form': form,
            })
