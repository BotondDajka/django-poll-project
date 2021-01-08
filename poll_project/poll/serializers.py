from rest_framework.serializers import ModelSerializer, IntegerField, ValidationError
from .models import Poll
from datetime import datetime


class PollSerializer(ModelSerializer):

    class Meta:
        model = Poll
        fields = '__all__'
        read_only_fields = ["option_one_count", "option_two_count", "option_three_count", "date_lastvote"]

def validate_option(option_index):
    if option_index < 1 or option_index > 3:
        raise ValidationError
class ResultsPollSerializer(ModelSerializer):
    option = IntegerField(write_only=True, validators=[validate_option])
    
    class Meta:
        model = Poll
        fields = ("id","option_one_count", "option_two_count", "option_three_count", "date_created", "date_lastvote", "option")
        read_only_fields = ["id","option_one_count", "option_two_count", "option_three_count", "date_created", "date_lastvote"]

    def update(self, instance, validated_data):
        options = ["option_one_count", "option_two_count", "option_three_count"]

        option_index = validated_data["option"]-1     
        chosen_option = options[option_index]
        option_count = getattr(instance, chosen_option)

        option_count +=1

        setattr(instance, chosen_option, option_count)
        instance.date_lastvote = datetime.now()
        instance.save()

        return instance


class VotePollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = ["id","option_one_count","option_two_count","option_three_count"]


