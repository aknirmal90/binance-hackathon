from django.shortcuts import render
from django.views.generic.base import TemplateView
from forms import MainForm
from services.models import get_address_risk_score


class MainFormView(TemplateView):

	template_name = 'form.html'

	def get(self, request):
		context = {'form': MainForm(), 'risk_score': None}
		return render(request, self.template_name, context)

	def post(self, request):
		form = MainForm(request.POST)
		if not form.is_valid():
			context = {'form': MainForm(), 'risk_score': None}
			return render(request, self.template_name, context)

		address = request.POST['destination_address']
		risk_score = get_address_risk_score(address)
		context = {'form': form, 'risk_score': risk_score}
		return render(request, self.template_name, context)
