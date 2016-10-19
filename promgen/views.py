from django.http import JsonResponse
from django.views.generic import ListView, View
from django.views.generic import DetailView
from promgen import models


class ServiceList(ListView):
    model = models.Service


class ServiceDetail(DetailView):
    model = models.Service


class ProjectDetail(DetailView):
    model = models.Project


class RulesList(ListView):
    model = models.Rule


class ApiConfig(View):
    def get(self, request):
        data = []
        for exporter in models.Exporter.objects.all():
            labels = {
                'project': exporter.project.name,
                'service': exporter.project.service.name,
                'farm': exporter.project.farm.name,
                'job': exporter.job,
            }
            if exporter.path:
                labels['__metrics_path__'] = exporter.path

            hosts = []
            for host in models.Host.objects.filter(farm=exporter.project.farm):
                hosts.append('{}:{}'.format(host.name, exporter.port))

            data.append({
                'labels': labels,
                'targets': hosts,
            })

        return JsonResponse(data, safe=False)