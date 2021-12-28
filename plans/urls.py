from django.urls import path, include
from rest_framework.routers import DefaultRouter

from plans.views import SectionViewSets, QuestionViewSet, AnswerViewSet, UserSectionAnswersViewSet, ConfirmAndCreatePlan

router = DefaultRouter()
router.register(
    'section', SectionViewSets, basename='section'
)
router.register(
    'question', QuestionViewSet, basename='question'
)
router.register(
    'answer', AnswerViewSet, basename='answer'
)

router.register(
    'user-section-answer', UserSectionAnswersViewSet, basename='user_section_answer'
)

urlpatterns = [
    path('plan/', include(router.urls)),
    path('confirme_answers/', ConfirmAndCreatePlan.as_view())
]
