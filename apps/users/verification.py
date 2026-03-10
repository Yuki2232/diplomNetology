from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    
    if user.is_email_verified:
        return Response({'message': 'Email уже подтвержден'}, status=status.HTTP_200_OK)
    
    user.is_email_verified = True
    user.email_verification_token = None
    user.save()
    
    return Response({'message': 'Email успешно подтвержден'}, status=status.HTTP_200_OK)