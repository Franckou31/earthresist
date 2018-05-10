from django.forms import ModelForm
from member.models import Member, Don

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class AdhesionForm(ModelForm):
    class Meta:
        model = Don
        fields = ['type_paiement', 'montant']
