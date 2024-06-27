# admin.py
import csv
import io
from django.contrib import admin
from django.http import HttpResponse
from .models import Event, Coordinator, Registration
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0  # To prevent extra empty forms
    fields = ('team_name', 'members_display')
    readonly_fields = ('members_display',)

    def members_display(self, obj):
        members_list = []
        for member in obj.members:
            member_display = f"{member['name']} ({member.get('vtu_number', '')}, {member.get('year', '')})"
            members_list.append(member_display)
        return ', '.join(members_list)
    members_display.short_description = 'Members'

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'registration_deadline', 'whatsapp_group_link', 'registered_teams_count')
    search_fields = ('title', 'location')
    prepopulated_fields = {'event_link': ('title',)}
    inlines = [RegistrationInline]

    actions = ['download_registrations_csv', 'download_registrations_pdf']

    def download_registrations_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="registrations_details.csv"'

        writer = csv.writer(response)
        writer.writerow(['TEAM NAME', 'MEMBER NAME', 'VTU NUMBER', 'YEAR', 'TEAM NUMBER'])

        for event in queryset:
            registrations = event.registration_set.all()
            for i, registration in enumerate(registrations, start=1):
                for member in registration.members:
                    writer.writerow([registration.team_name, member['name'], member.get('vtu_number', ''), member.get('year', ''), f'Team {i}'])

        return response

    download_registrations_csv.short_description = 'Download Registrations CSV for selected Events'

    def download_registrations_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="registrations_details.pdf"'

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        date_style = ParagraphStyle(name='DateStyle', parent=styles['Normal'], alignment=2)  # Alignment 2 is for right align

        for event in queryset:
            registrations = event.registration_set.all()

            # Add Event Name (centered at the top)
            event_name = Paragraph(event.title, title_style)
            elements.append(event_name)

            # Add Event Date (right aligned at the top)
            event_date = Paragraph(event.event_date.strftime('%Y-%m-%d'), date_style)
            elements.append(event_date)

            # Add Event Time (right aligned below date)
            event_time = Paragraph(event.event_time.strftime('%H:%M:%S'), date_style)
            elements.append(event_time)

            # Add a spacer
            elements.append(Spacer(1, 20))

            # Prepare data for the table
            data = []
            data.append(['TEAM NAME', 'MEMBER NAME', 'VTU NUMBER', 'YEAR', 'TEAM NUMBER'])
            for i, registration in enumerate(registrations, start=1):
                for member in registration.members:
                    data.append([registration.team_name, member['name'], member.get('vtu_number', ''), member.get('year', ''), f'Team {i}'])

            # Calculate available width for the table
            available_width = letter[0] - 72  # 1 inch margin on each side (72 points)
            
            # Create the table with full width
            table = Table(data, colWidths=[available_width/5]*5)  # Divide available width into 5 equal parts
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add border lines
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))  # Add space between tables in PDF

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    download_registrations_pdf.short_description = 'Download Registrations PDF for selected Events'

    def registered_teams_count(self, obj):
        return obj.registration_set.count()
    registered_teams_count.short_description = 'Registered Teams'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['general_rules'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 10})
        form.base_fields['prizes'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 10})
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        if obj:
            extra_context['registrations'] = obj.registration_set.all()
            extra_context['event_date'] = obj.event_date
            extra_context['event_time'] = obj.event_time
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

admin.site.register(Event, EventAdmin)
admin.site.register(Coordinator)
admin.site.register(Registration)
