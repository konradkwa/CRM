import random
from django.views import generic
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.core.mail import send_mail


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f'{random.randint(0, 1000000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject='You are invated to be an agent',
            message='you were added as an agent on CRM',
            from_email='admin@crm.com',
            recipient_list=[user.email]
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
