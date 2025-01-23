# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Consent
#
# class BotActionView(APIView):
#     def post(self, request):
#         user_id = request.data.get("user_id")
#
#         try:
#             # Получаем согласие пользователя
#             consent = Consent.objects.get(user_id=user_id)
#
# # Проверяем, дано ли согласие if not consent.consent_given: return
# Response( {"message": "К сожалению, вы не можете продолжить без
# согласия."}, status=status.HTTP_403_FORBIDDEN, ) except
# Consent.DoesNotExist: return Response( {"message": "Согласие не найдено.
# Пожалуйста, примите условия."}, status=status.HTTP_404_NOT_FOUND, )
#
# # Если согласие есть, продолжаем действие return Response({"message": "Вы
# успешно продолжили!"}, status=status.HTTP_200_OK)

