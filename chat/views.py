from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, reverse
from rest_framework import status
from django.db.models import Q
from .models import Conversation, Message
from users.models import User
from .serializers import ConversationListSerializer, ConversationSerializer, MessageSerializer


from rest_framework.pagination import PageNumberPagination

class ConversationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
# Представление для начала нового разговора или перенаправления на существующий
class StartConvoView(ListCreateAPIView):
    """
    начало нового диалога или перенаправления к существующему.

    Параметры:
    - email: Электронная почта участника разговора.

    Возвращает:
    - 201 Created: Если новый разговор начат успешно.
    - Redirect: Если найден существующий разговор, перенаправляет на него.

    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        participant = get_object_or_404(User, email=email)

        conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                                   Q(initiator=participant, receiver=request.user)).first()

        if conversation:
            return Response(ConversationSerializer(instance=conversation, context={"request": request}).data,
                            status=status.HTTP_302_FOUND)
        else:
            conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
            serializer = ConversationSerializer(instance=conversation, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Представление для получения разговора по его идентификатору
class GetConversationView(RetrieveAPIView):
    """
    получение диалога по его айди

    Параметры:
    - pk: Идентификатор разговора.

    Возвращает:
    - 200 OK: Возвращает детали разговора
    P.S.

    """
    serializer_class = ConversationSerializer
    pagination_class = ConversationPagination
    #permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Получаем все сообщения
        messages = Message.objects.filter(conversation_id=instance.id).order_by('-timestamp')

        # Пагинируем сообщения, используя указанный класс пагинации
        paginated_messages = self.paginate_queryset(messages)

        # Сериализуем разговор с пагинированными сообщениями
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data
        serialized_data['messages'] = MessageSerializer(instance=paginated_messages, many=True).data

        return self.get_paginated_response(serialized_data)


