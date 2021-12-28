from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView

# Create your views here.
from plans.models import QuestionSection, Question, Answer, UserSectionAnswers
from plans.serializers import SectionSerializer, QuestionSerializer, AnswerSerializer, UserSectionAnswersSerializer, \
    UserSectionAnswersReadSerializer, ConfirmSerializer


class SectionViewSets(ModelViewSet):
    # permission_classes = [DjangoModelPermissions]
    queryset = QuestionSection.objects.all()
    serializer_class = SectionSerializer


class QuestionViewSet(ModelViewSet):
    # permission_classes = [DjangoModelPermissions]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section__id']


class AnswerViewSet(ModelViewSet):
    # permission_classes = [DjangoModelPermissions]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question__id']


class UserSectionAnswersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    """
    no need to handel is owner permission while query_set filter by user
    NOTE : remove is authed permission may return server error 500 
    """

    def get_queryset(self):
        return UserSectionAnswers.objects.filter(status=UserSectionAnswers.INIT, user=self.request.user)

    def get_serializer_class(self):
        if  self.request.method.lower() == 'get':
            return UserSectionAnswersReadSerializer
        else:
            return UserSectionAnswersSerializer


class ConfirmAndCreatePlan(GenericAPIView):
    serializer_class = ConfirmSerializer
    queryset = UserSectionAnswers.objects.all()
    #permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = ConfirmSerializer(data=self.request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"confirmed and plan created"})
