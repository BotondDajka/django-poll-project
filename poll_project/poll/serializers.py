from rest_framework.serializers import ModelSerializer

from .models import Poll


class PollSerializer(ModelSerializer):
   
    class Meta:
        model = Poll
        fields = '__all__'
        read_only_fields = ["option_one_count", "option_two_count", "option_three_count", "date_lastvote"]

class ResultsPollSerializer(ModelSerializer):
    
    class Meta:
        model = Poll
        #fields = [model.option_one_count, model.option_two_count, model.option_three_count]
        fields = ("id","option_one_count", "option_two_count", "option_three_count", "date_created", "date_lastvote")
        #fields = '__all__'


class VotePollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = ["id","option_one_count","option_two_count","option_three_count"]


