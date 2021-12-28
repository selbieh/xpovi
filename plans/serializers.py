from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from plans.models import QuestionSection, Question, Answer, UserSectionAnswers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Answer


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Question


class SectionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = QuestionSection


class UserSectionAnswersSerializer(serializers.ModelSerializer):
    """
    status should not be changed with put or patch request
    while other end point will change it and fire signal to form plan for the user
    """
    customer = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=User.objects.all(),
        default=CurrentUserDefault(),
    )
    status = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'
        model = UserSectionAnswers
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=UserSectionAnswers.objects.all(),
                fields=('status', 'user','section'),
                message=("This competency already exists in your academy"),
            )
        ]


class SimpleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSection
        fields = ['id', 'order', 'title', 'description']


class UserSectionAnswersReadSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    section = SimpleSectionSerializer()

    class Meta:
        fields = ['id', 'answers', 'section']
        model = UserSectionAnswers


class ConfirmSerializer(serializers.Serializer):
    status = serializers.CharField()

    def validate_status(self, vlaue):
        if vlaue == 'confirmed':
            user_answers = UserSectionAnswers.objects.filter(user=self.context['request'].user,status=UserSectionAnswers.INIT)
            if user_answers.count() < 2:
                raise serializers.ValidationError('some section answer is missing')
        else:
            raise serializers.ValidationError('change state string should be {confirmed}')
    def save(self, **kwargs):
        UserSectionAnswers.objects.filter(user=self.context['request'].user).update(status=UserSectionAnswers.CONFIRMED)
        """
        logic of creating plan should implemented here 
        """
        return
