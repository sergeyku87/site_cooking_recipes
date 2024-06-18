from django.shortcuts import redirect, render
from django.urls import path

import csv
from common.forms import CsvImportForm


class CSVMixin():
    def get_urls(self):
        urls = super().get_urls()
        urls.extend([path('csv-upload/', self.upload_csv)])
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf8').splitlines()
            reader = csv.DictReader(
                decoded_file,
                delimiter=',',
                fieldnames=self.csv_fields,
            )
            for row in reader:
                try:
                    self.model.objects.create(**row)
                except Exception as err:
                    self.message_user(request, f'Ошибка {err}')
                    pass
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(
            request, 'admin/csv_import.html', payload
        )
